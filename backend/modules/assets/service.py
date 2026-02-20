"""
Asset service for background image uploads and runtime URL resolution.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import hashlib
import io
from typing import List, Optional, Tuple

import httpx
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

from .asset_schemas import (
    BackgroundAssetMetadata,
    TermsAssetMetadata,
    TermsUrlValidateResponse,
)
from .storage import (
    AssetStorageProvider,
    LocalAssetStorageProvider,
    load_storage_config,
    get_storage_provider,
)


logger = get_logger(__name__)

THUMBNAIL_MAX_SIZE = 300


def _thumbnail_storage_key(storage_key: str) -> str:
    """Derive thumbnail storage key from main: {base}_TN.jpg (e.g. 1/abc123.png -> 1/abc123_TN.jpg)."""
    if "." in storage_key:
        base, _ = storage_key.rsplit(".", 1)
    else:
        base = storage_key
    return f"{base}_TN.jpg"


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

    def _generate_and_save_thumbnail(self, *, storage_key: str, file_bytes: bytes, mime_type: str) -> None:
        """Generate 300x300 thumbnail (aspect ratio preserved) and save as {base}_TN.jpg."""
        try:
            with Image.open(io.BytesIO(file_bytes)) as img:
                img.load()
                # Preserve aspect ratio, fit within 300x300
                img.thumbnail((THUMBNAIL_MAX_SIZE, THUMBNAIL_MAX_SIZE), Image.Resampling.LANCZOS)
                buf = io.BytesIO()
                if img.mode in ("RGBA", "LA", "P"):
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    if img.mode == "P":
                        img = img.convert("RGBA")
                    if img.mode in ("RGBA", "LA"):
                        background.paste(img, mask=img.split()[-1])
                    else:
                        background.paste(img)
                    img = background
                elif img.mode != "RGB":
                    img = img.convert("RGB")
                img.save(buf, format="JPEG", quality=85)
                thumb_bytes = buf.getvalue()
            thumb_key = _thumbnail_storage_key(storage_key)
            storage = self._get_storage_provider()
            storage.save(storage_key=thumb_key, data=thumb_bytes, content_type="image/jpeg")
        except Exception as e:
            logger.warning(
                "Thumbnail generation failed storage_key=%r error=%s",
                storage_key,
                str(e),
                extra={"event": "asset_thumbnail_failed", "storage_key": storage_key, "error": str(e)},
            )

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

    def _get_asset_type_id(self, type_code: str = "IMAGE") -> int:
        asset_type = (
            self.db.query(AssetType)
            .filter(
                AssetType.TypeCode == type_code,
                AssetType.IsDeleted == False,  # noqa: E712
            )
            .first()
        )
        if not asset_type:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Asset type {type_code} is not configured",
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
            storage = self._get_storage_provider()
            if not storage.exists(existing.StorageKey):
                logger.info(
                    "Hash match but file missing, re-uploading asset_id=%s storage_key=%r",
                    existing.AssetID,
                    existing.StorageKey,
                    extra={"event": "asset_reupload", "asset_id": existing.AssetID},
                )
                storage.save(
                    storage_key=existing.StorageKey,
                    data=file_bytes,
                    content_type=mime_type,
                )
                self._generate_and_save_thumbnail(
                    storage_key=existing.StorageKey,
                    file_bytes=file_bytes,
                    mime_type=mime_type,
                )
            return self._to_metadata(existing), True

        format_map = {"JPEG": "jpg", "JPG": "jpg", "PNG": "png", "WEBP": "webp"}
        extension = format_map.get(image_format.upper(), image_format.lower() or "img")
        storage_key = f"{current_user.company_id}/{sha256}.{extension}"

        storage = self._get_storage_provider()
        storage.save(storage_key=storage_key, data=file_bytes, content_type=mime_type)
        self._generate_and_save_thumbnail(
            storage_key=storage_key,
            file_bytes=file_bytes,
            mime_type=mime_type,
        )

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

    def list_terms_assets_for_company(self, *, company_id: int) -> List[TermsAssetMetadata]:
        """List all TERMS assets for a company (uploaded PDFs and URLs)."""
        terms_type_id = self._get_asset_type_id("TERMS")
        rows = (
            self.db.query(Asset)
            .filter(
                Asset.CompanyID == company_id,
                Asset.AssetTypeID == terms_type_id,
                Asset.IsDeleted == False,  # noqa: E712
            )
            .order_by(Asset.AssetID.desc())
            .all()
        )
        return [self._asset_to_terms_metadata(a) for a in rows]

    async def upload_terms_pdf(
        self,
        *,
        file: UploadFile,
        display_name: Optional[str],
        current_user: CurrentUser,
    ) -> Tuple[TermsAssetMetadata, bool]:
        """Upload a PDF Terms document."""
        if not current_user.company_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current user does not have a company context",
            )
        filename = file.filename or ""
        content_type = getattr(file, "content_type", None) or ""
        file_bytes = await file.read()
        if not file_bytes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Empty file uploaded",
            )
        if content_type not in ("application/pdf", "") and "pdf" not in filename.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are supported for Terms",
            )
        # Accept PDF by extension if MIME is generic
        if not content_type or content_type == "application/octet-stream":
            if filename.lower().endswith(".pdf"):
                content_type = "application/pdf"
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only PDF files are supported for Terms",
                )
        sha256 = hashlib.sha256(file_bytes).hexdigest()
        terms_type_id = self._get_asset_type_id("TERMS")
        existing = (
            self.db.query(Asset)
            .filter(
                Asset.CompanyID == current_user.company_id,
                Asset.AssetTypeID == terms_type_id,
                Asset.Sha256 == sha256,
                Asset.SourceURL == None,  # noqa: E711
                Asset.IsDeleted == False,  # noqa: E712
            )
            .first()
        )
        if existing:
            storage = self._get_storage_provider()
            if not storage.exists(existing.StorageKey):
                storage.save(
                    storage_key=existing.StorageKey,
                    data=file_bytes,
                    content_type="application/pdf",
                )
            return self._asset_to_terms_metadata(existing), True
        extension = "pdf"
        storage_key = f"{current_user.company_id}/{sha256}.{extension}"
        storage = self._get_storage_provider()
        storage.save(storage_key=storage_key, data=file_bytes, content_type="application/pdf")
        asset_kwargs = {}
        if self.db.bind and self.db.bind.dialect.name == "sqlite":
            asset_kwargs["AssetID"] = self._next_asset_id()
        asset = Asset(
            CompanyID=current_user.company_id,
            AssetTypeID=terms_type_id,
            Sha256=sha256,
            MimeType="application/pdf",
            SizeBytes=len(file_bytes),
            WidthPx=None,
            HeightPx=None,
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
        return self._asset_to_terms_metadata(asset), False

    def add_terms_url(
        self,
        *,
        url: str,
        display_name: Optional[str],
        display_mode: str = "popup",
        current_user: CurrentUser,
    ) -> TermsAssetMetadata:
        """Add Terms by external URL."""
        if not current_user.company_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current user does not have a company context",
            )
        url = url.strip()
        if not url.startswith("https://"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Terms URL must use HTTPS",
            )
        sha256 = hashlib.sha256(url.encode()).hexdigest()
        terms_type_id = self._get_asset_type_id("TERMS")
        existing = (
            self.db.query(Asset)
            .filter(
                Asset.CompanyID == current_user.company_id,
                Asset.AssetTypeID == terms_type_id,
                Asset.SourceURL == url,  # noqa: E711
                Asset.IsDeleted == False,  # noqa: E712
            )
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This Terms URL is already added",
            )
        asset_kwargs = {}
        if self.db.bind and self.db.bind.dialect.name == "sqlite":
            asset_kwargs["AssetID"] = self._next_asset_id()
        asset = Asset(
            CompanyID=current_user.company_id,
            AssetTypeID=terms_type_id,
            Sha256=sha256,
            MimeType="text/url",
            SizeBytes=0,
            WidthPx=None,
            HeightPx=None,
            StorageProvider="external",
            StorageKey=f"url:{sha256}",
            SourceURL=url,
            OriginalFileName=None,
            DisplayName=display_name or url[:80] + ("..." if len(url) > 80 else ""),
            TermsDisplayMode=display_mode if display_mode in ("popup", "new_tab") else None,
            CreatedDate=datetime.utcnow(),
            UpdatedDate=datetime.utcnow(),
            CreatedBy=current_user.user_id,
            UpdatedBy=current_user.user_id,
            **asset_kwargs,
        )
        self.db.add(asset)
        self.db.commit()
        self.db.refresh(asset)
        return self._asset_to_terms_metadata(asset)

    def validate_terms_url(self, url: str) -> TermsUrlValidateResponse:
        """Validate whether a Terms URL can be embedded in an iframe.
        Returns blocker_type and next_action to help users resolve issues.
        """
        url = url.strip()
        if not url.startswith("https://"):
            return TermsUrlValidateResponse(
                embeddable=False,
                reason="URL must use HTTPS",
                blocker_type="content",
                next_action="Use an HTTPS URL. HTTP is not allowed for security.",
            )
        try:
            with httpx.Client(follow_redirects=True, timeout=10.0) as client:
                resp = client.head(url)
                resp.raise_for_status()
            xfo = resp.headers.get("X-Frame-Options", "").strip().upper()
            csp = resp.headers.get("Content-Security-Policy", "")
            if xfo == "DENY":
                return TermsUrlValidateResponse(
                    embeddable=False,
                    reason="X-Frame-Options: DENY — page cannot be embedded",
                    blocker_type="embedding",
                    next_action="Ask the host to remove X-Frame-Options or allow framing. Or upload a PDF instead.",
                )
            if xfo == "SAMEORIGIN":
                return TermsUrlValidateResponse(
                    embeddable=False,
                    reason="X-Frame-Options: SAMEORIGIN — only same site can embed",
                    blocker_type="embedding",
                    next_action="The host only allows same-site embedding. Ask them to allow your domain, or upload a PDF instead.",
                )
            csp_lower = csp.lower()
            if "frame-ancestors" in csp_lower:
                if "'none'" in csp_lower or '"none"' in csp_lower:
                    return TermsUrlValidateResponse(
                        embeddable=False,
                        reason="CSP frame-ancestors 'none' — cannot embed",
                        blocker_type="embedding",
                        next_action="Ask the host to allow framing in their Content-Security-Policy, or upload a PDF instead.",
                    )
                if "'self'" in csp_lower or '"self"' in csp_lower:
                    return TermsUrlValidateResponse(
                        embeddable=False,
                        reason="CSP frame-ancestors 'self' — only same site can embed",
                        blocker_type="embedding",
                        next_action="The host only allows same-site embedding. Ask them to add your domain to frame-ancestors, or upload a PDF instead.",
                    )
            return TermsUrlValidateResponse(embeddable=True)
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code if e.response else 0
            if status_code == 404:
                return TermsUrlValidateResponse(
                    embeddable=False,
                    reason="404 Not Found — URL or path may have changed",
                    blocker_type="reachability",
                    next_action="Check the link is correct. If the page moved, update the URL or upload a PDF instead.",
                )
            if status_code in (401, 403):
                return TermsUrlValidateResponse(
                    embeddable=False,
                    reason=f"{status_code} — Cannot display in pop-up: host restricts who can load this URL (may require allowlisting)",
                    blocker_type="reachability",
                    next_action="Ask your IT team or the document host to add our platform's domain to their authorized/allowlist so we can display Terms in a pop-up for form users. Or upload a PDF for full control.",
                )
            return TermsUrlValidateResponse(
                embeddable=False,
                reason=f"HTTP {status_code} — {str(e)}",
                blocker_type="reachability",
                next_action="The host returned an error. Try again later or upload a PDF instead.",
            )
        except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout) as e:
            return TermsUrlValidateResponse(
                embeddable=False,
                reason=f"Could not reach URL: {str(e)}",
                blocker_type="reachability",
                next_action="Check the URL is correct and the site is online. Try again later or upload a PDF as a fallback.",
            )
        except httpx.HTTPError as e:
            return TermsUrlValidateResponse(
                embeddable=False,
                reason=f"Could not validate: {str(e)}",
                blocker_type="unknown",
                next_action="Validate again or upload a PDF instead. External URLs may stop working if the host changes policy.",
            )

    def _asset_to_terms_metadata(self, asset: Asset) -> TermsAssetMetadata:
        return TermsAssetMetadata(
            assetId=asset.AssetID,
            assetKey=f"asset:{asset.AssetID}",
            displayName=asset.DisplayName,
            sourceType="url" if asset.SourceURL else "upload",
            sourceUrl=asset.SourceURL,
            mimeType=asset.MimeType,
            byteSize=asset.SizeBytes or 0,
            embeddable=None,
            termsDisplayMode=getattr(asset, "TermsDisplayMode", None),
            displayWidthPx=getattr(asset, "DisplayWidthPx", None),
            displayHeightPx=getattr(asset, "DisplayHeightPx", None),
            displayRotationDegrees=getattr(asset, "DisplayRotationDegrees", None),
            createdAt=asset.CreatedDate,
            updatedAt=asset.UpdatedDate,
        )

    def list_background_assets(self, *, current_user: CurrentUser) -> List[BackgroundAssetMetadata]:
        """List all background (IMAGE) assets for the current user's company."""
        if not current_user.company_id:
            return []
        return self.list_image_assets_for_company(company_id=current_user.company_id)

    def list_image_assets_for_company(self, *, company_id: int) -> List[BackgroundAssetMetadata]:
        """List all IMAGE assets for a company (e.g. Company Settings Assets page)."""
        asset_type_id = self._get_asset_type_id()
        rows = (
            self.db.query(Asset)
            .filter(
                Asset.CompanyID == company_id,
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

    def get_asset_content_response(
        self, *, asset_id: int, request: Request, size: Optional[str] = None
    ):
        """Serve asset content. size='thumb' prefers 300x300 thumbnail if present, else full.
        For URL-based Terms (SourceURL set), redirect to external URL."""
        asset = (
            self.db.query(Asset)
            .filter(Asset.AssetID == asset_id, Asset.IsDeleted == False)  # noqa: E712
            .first()
        )
        if not asset:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")

        # URL-based Terms: redirect to external URL
        if getattr(asset, "SourceURL", None):
            return RedirectResponse(
                url=asset.SourceURL,
                status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            )

        storage = self._get_storage_provider()
        storage_key = asset.StorageKey
        media_type = asset.MimeType
        if size == "thumb":
            thumb_key = _thumbnail_storage_key(asset.StorageKey)
            if storage.exists(thumb_key):
                storage_key = thumb_key
                media_type = "image/jpeg"

        if isinstance(storage, LocalAssetStorageProvider):
            path = storage.resolve_path(storage_key)
            if not path.exists():
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset file not found")
            return FileResponse(
                path,
                media_type=media_type,
                filename=asset.OriginalFileName or f"asset-{asset.AssetID}",
            )

        url = storage.get_public_url(
            storage_key=storage_key,
            request_base=str(request.base_url),
            asset_id=asset.AssetID,
        )
        return RedirectResponse(url=url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
