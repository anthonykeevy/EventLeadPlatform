"""
Asset service for background image uploads and runtime URL resolution.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import hashlib
import io
from typing import List, Optional, Tuple

from fastapi import HTTPException, UploadFile, status, Request
from fastapi.responses import FileResponse, RedirectResponse
from PIL import Image, UnidentifiedImageError
from sqlalchemy.orm import Session
from sqlalchemy import func

from common.config_service import ConfigurationService
from common.constants import (
    ASSET_IMAGE_MAX_UPLOAD_BYTES_KEY,
    ASSET_IMAGE_MAX_WIDTH_PX_KEY,
    ASSET_IMAGE_MAX_HEIGHT_PX_KEY,
    ASSET_IMAGE_ALLOWED_MIME_TYPES_KEY,
    DEFAULT_ASSET_IMAGE_MAX_UPLOAD_BYTES,
    DEFAULT_ASSET_IMAGE_MAX_WIDTH_PX,
    DEFAULT_ASSET_IMAGE_MAX_HEIGHT_PX,
    DEFAULT_ASSET_IMAGE_ALLOWED_MIME_TYPES,
)
from common.logger import get_logger
from models.asset import Asset
from models.ref.asset_type import AssetType
from modules.auth.models import CurrentUser

from .asset_schemas import BackgroundAssetMetadata
from .storage import (
    AssetStorageProvider,
    LocalAssetStorageProvider,
    load_storage_config,
    get_storage_provider,
)


logger = get_logger(__name__)


@dataclass(frozen=True)
class AssetLimits:
    max_bytes: int
    max_width_px: int
    max_height_px: int
    allowed_mime_types: list[str]


class AssetService:
    def __init__(self, db: Session):
        self.db = db
        self._storage_provider: Optional[AssetStorageProvider] = None

    def _get_storage_provider(self) -> AssetStorageProvider:
        if self._storage_provider is None:
            config = load_storage_config()
            self._storage_provider = get_storage_provider(config)
        return self._storage_provider

    def _get_limits(self) -> AssetLimits:
        config = ConfigurationService(self.db)

        max_bytes = config.get_setting(
            ASSET_IMAGE_MAX_UPLOAD_BYTES_KEY,
            DEFAULT_ASSET_IMAGE_MAX_UPLOAD_BYTES,
        )
        max_width = config.get_setting(
            ASSET_IMAGE_MAX_WIDTH_PX_KEY,
            DEFAULT_ASSET_IMAGE_MAX_WIDTH_PX,
        )
        max_height = config.get_setting(
            ASSET_IMAGE_MAX_HEIGHT_PX_KEY,
            DEFAULT_ASSET_IMAGE_MAX_HEIGHT_PX,
        )
        allowed_mimes = config.get_setting(
            ASSET_IMAGE_ALLOWED_MIME_TYPES_KEY,
            DEFAULT_ASSET_IMAGE_ALLOWED_MIME_TYPES,
        )
        if not isinstance(allowed_mimes, list):
            allowed_mimes = DEFAULT_ASSET_IMAGE_ALLOWED_MIME_TYPES

        return AssetLimits(
            max_bytes=int(max_bytes),
            max_width_px=int(max_width),
            max_height_px=int(max_height),
            allowed_mime_types=[m.strip() for m in allowed_mimes if str(m).strip()],
        )

    def _get_asset_type_id(self) -> int:
        asset_type = (
            self.db.query(AssetType)
            .filter(
                AssetType.TypeCode == "IMAGE",
                AssetType.IsDeleted == False,  # noqa: E712
            )
            .first()
        )
        if not asset_type:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Asset type IMAGE is not configured",
            )
        return int(asset_type.AssetTypeID)

    def _to_metadata(self, asset: Asset) -> BackgroundAssetMetadata:
        return BackgroundAssetMetadata(
            assetId=asset.AssetID,
            assetKey=f"asset:{asset.AssetID}",
            displayName=asset.DisplayName,
            originalFilename=asset.OriginalFileName or "",
            mimeType=asset.MimeType,
            byteSize=asset.SizeBytes,
            widthPx=asset.WidthPx,
            heightPx=asset.HeightPx,
            checksumSha256=asset.Sha256,
            createdAt=asset.CreatedDate,
            updatedAt=asset.UpdatedDate,
        )

    def _next_asset_id(self) -> int:
        current = self.db.query(func.max(Asset.AssetID)).scalar()
        return int(current or 0) + 1

    async def upload_background_asset(
        self,
        *,
        file: UploadFile,
        display_name: Optional[str],
        current_user: CurrentUser,
    ) -> Tuple[BackgroundAssetMetadata, bool]:
        if not current_user.company_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current user does not have a company context",
            )

        limits = self._get_limits()
        filename = file.filename or ""
        content_type = getattr(file, "content_type", None) or ""
        file_bytes = await file.read()
        size_bytes = len(file_bytes)

        # Keys in extra must not clash with logging.LogRecord (e.g. "filename", "message")
        log_ctx = {
            "asset_filename": filename,
            "asset_content_type": content_type,
            "asset_size_bytes": size_bytes,
            "asset_company_id": current_user.company_id,
        }
        logger.info(
            "Background asset upload start filename=%r content_type=%r size=%s",
            filename,
            content_type,
            size_bytes,
            extra={"event": "asset_upload_start", **log_ctx},
        )

        if not file_bytes:
            logger.warning(
                "Upload rejected: empty file filename=%r",
                filename,
                extra={"event": "asset_upload_rejected", **log_ctx, "reason": "empty_file"},
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Empty file uploaded",
            )
        if size_bytes > limits.max_bytes:
            logger.warning(
                "Upload rejected: file too large filename=%r size=%s max=%s",
                filename,
                size_bytes,
                limits.max_bytes,
                extra={"event": "asset_upload_rejected", **log_ctx, "reason": "file_too_large", "asset_max_bytes": limits.max_bytes},
            )
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Max size is {limits.max_bytes} bytes",
            )

        try:
            with Image.open(io.BytesIO(file_bytes)) as image:
                image.load()
                width_px, height_px = image.size
                detected_mime = Image.MIME.get(image.format)
                image_format = image.format or ""
        except UnidentifiedImageError as e:
            logger.warning(
                "Upload rejected: PIL could not identify image filename=%r content_type=%r error=%s",
                filename,
                content_type,
                str(e),
                extra={
                    "event": "asset_upload_rejected",
                    **log_ctx,
                    "reason": "unidentified_image",
                    "asset_error": str(e),
                },
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported or invalid image file",
            )

        mime_type = detected_mime or content_type or "application/octet-stream"
        # Normalize non-standard MIME (e.g. image/jpg -> image/jpeg) so JPGs always pass
        if mime_type == "image/jpg":
            mime_type = "image/jpeg"
        if mime_type not in limits.allowed_mime_types:
            logger.warning(
                "Upload rejected: unsupported mime filename=%r mime_type=%r allowed=%r",
                filename,
                mime_type,
                limits.allowed_mime_types,
                extra={
                    "event": "asset_upload_rejected",
                    **log_ctx,
                    "reason": "unsupported_mime",
                    "asset_detected_mime": detected_mime,
                    "asset_mime_type": mime_type,
                    "asset_allowed_mime_types": limits.allowed_mime_types,
                    "asset_image_format": image_format,
                    "asset_width_px": width_px,
                    "asset_height_px": height_px,
                },
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported mime type: {mime_type}",
            )

        if width_px > limits.max_width_px or height_px > limits.max_height_px:
            logger.warning(
                "Upload rejected: dimensions exceed limit filename=%r %sx%s > %sx%s",
                filename,
                width_px,
                height_px,
                limits.max_width_px,
                limits.max_height_px,
                extra={
                    "event": "asset_upload_rejected",
                    **log_ctx,
                    "reason": "dimensions_exceed_limit",
                    "asset_width_px": width_px,
                    "asset_height_px": height_px,
                    "asset_max_width_px": limits.max_width_px,
                    "asset_max_height_px": limits.max_height_px,
                },
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Image dimensions exceed limits: "
                    f"{width_px}x{height_px} > {limits.max_width_px}x{limits.max_height_px}"
                ),
            )

        sha256 = hashlib.sha256(file_bytes).hexdigest()
        asset_type_id = self._get_asset_type_id()

        existing = (
            self.db.query(Asset)
            .filter(
                Asset.CompanyID == current_user.company_id,
                Asset.AssetTypeID == asset_type_id,
                Asset.Sha256 == sha256,
                Asset.IsDeleted == False,  # noqa: E712
            )
            .first()
        )
        if existing:
            return self._to_metadata(existing), True

        format_map = {"JPEG": "jpg", "JPG": "jpg", "PNG": "png", "WEBP": "webp"}
        extension = format_map.get(image_format.upper(), image_format.lower() or "img")
        storage_key = f"{current_user.company_id}/{sha256}.{extension}"

        storage = self._get_storage_provider()
        storage.save(storage_key=storage_key, data=file_bytes, content_type=mime_type)

        asset_kwargs = {}
        if self.db.bind and self.db.bind.dialect.name == "sqlite":
            asset_kwargs["AssetID"] = self._next_asset_id()

        asset = Asset(
            CompanyID=current_user.company_id,
            AssetTypeID=asset_type_id,
            Sha256=sha256,
            MimeType=mime_type,
            SizeBytes=len(file_bytes),
            WidthPx=width_px,
            HeightPx=height_px,
            StorageProvider=storage.provider_code,
            StorageKey=storage_key,
            OriginalFileName=file.filename,
            DisplayName=display_name or file.filename,
            CreatedDate=datetime.utcnow(),
            UpdatedDate=datetime.utcnow(),
            CreatedBy=current_user.user_id,
            UpdatedBy=current_user.user_id,
            **asset_kwargs,
        )
        self.db.add(asset)
        self.db.commit()
        self.db.refresh(asset)

        return self._to_metadata(asset), False

    def list_background_assets(self, *, current_user: CurrentUser) -> List[BackgroundAssetMetadata]:
        """List all background (IMAGE) assets for the current user's company."""
        if not current_user.company_id:
            return []
        asset_type_id = self._get_asset_type_id()
        rows = (
            self.db.query(Asset)
            .filter(
                Asset.CompanyID == current_user.company_id,
                Asset.AssetTypeID == asset_type_id,
                Asset.IsDeleted == False,  # noqa: E712
            )
            .order_by(Asset.UpdatedDate.desc(), Asset.AssetID.desc())
            .all()
        )
        return [self._to_metadata(a) for a in rows]

    def resolve_asset_url(self, *, asset_id: int, request: Request) -> str:
        asset = (
            self.db.query(Asset)
            .filter(Asset.AssetID == asset_id, Asset.IsDeleted == False)  # noqa: E712
            .first()
        )
        if not asset:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")

        storage = self._get_storage_provider()
        return storage.get_public_url(
            storage_key=asset.StorageKey,
            request_base=str(request.base_url),
            asset_id=asset.AssetID,
        )

    def get_asset_content_response(self, *, asset_id: int, request: Request):
        asset = (
            self.db.query(Asset)
            .filter(Asset.AssetID == asset_id, Asset.IsDeleted == False)  # noqa: E712
            .first()
        )
        if not asset:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")

        storage = self._get_storage_provider()
        if isinstance(storage, LocalAssetStorageProvider):
            path = storage.resolve_path(asset.StorageKey)
            if not path.exists():
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset file not found")
            return FileResponse(
                path,
                media_type=asset.MimeType,
                filename=asset.OriginalFileName or f"asset-{asset.AssetID}",
            )

        url = storage.get_public_url(
            storage_key=asset.StorageKey,
            request_base=str(request.base_url),
            asset_id=asset.AssetID,
        )
        return RedirectResponse(url=url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
