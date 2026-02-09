"""
Asset Router
Endpoints for background asset upload and URL resolution.
"""
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile, status, Request
from sqlalchemy.orm import Session

from common.database import get_db
from common.logger import get_logger
from modules.auth.dependencies import get_current_user
from modules.auth.models import CurrentUser

from .asset_schemas import BackgroundAssetUploadResponse, AssetResolveResponse
from .service import AssetService


logger = get_logger(__name__)

router = APIRouter(prefix="/api/assets", tags=["assets"])


@router.post(
    "/backgrounds/upload",
    response_model=BackgroundAssetUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload background image asset",
    description="Upload a background image asset with validation and deduplication",
)
async def upload_background_image(
    file: UploadFile = File(..., description="Background image file"),
    display_name: Optional[str] = Form(None, description="Optional display name"),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> BackgroundAssetUploadResponse:
    service = AssetService(db)
    asset, is_duplicate = await service.upload_background_asset(
        file=file,
        display_name=display_name,
        current_user=current_user,
    )
    return BackgroundAssetUploadResponse(asset=asset, isDuplicate=is_duplicate)


@router.get(
    "/{asset_id}/resolve",
    response_model=AssetResolveResponse,
    summary="Resolve asset URL",
    description="Resolve runtime URL for asset access without storing absolute hosts",
)
def resolve_asset_url(
    asset_id: int,
    request: Request,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AssetResolveResponse:
    service = AssetService(db)
    url = service.resolve_asset_url(asset_id=asset_id, request=request)
    return AssetResolveResponse(url=url)


@router.get(
    "/{asset_id}/content",
    summary="Stream asset content",
    description="Stream or redirect to asset content based on storage provider",
)
def stream_asset_content(
    asset_id: int,
    request: Request,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = AssetService(db)
    return service.get_asset_content_response(asset_id=asset_id, request=request)
