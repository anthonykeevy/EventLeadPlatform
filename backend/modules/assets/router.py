"""
Asset Router
Endpoints for background asset upload and URL resolution.
"""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile, status, Request, HTTPException
from sqlalchemy.orm import Session

from common.database import get_db
from common.logger import get_logger
from modules.auth.dependencies import get_current_user
from modules.auth.models import CurrentUser
from models.asset import Asset
from models.company import Company

from .asset_schemas import (
    BackgroundAssetListResponse,
    BackgroundAssetMetadata,
    BackgroundAssetUploadResponse,
    AssetResolveResponse,
    AssetUpdateRequest,
    TermsAssetListResponse,
    TermsAssetMetadata,
    TermsUploadResponse,
    TermsUrlAddRequest,
    TermsUrlValidateRequest,
    TermsUrlValidateResponse,
)
from .service import AssetService



logger = get_logger(__name__)

router = APIRouter(prefix="/api/assets", tags=["assets"])


@router.get(
    "/backgrounds",
    response_model=BackgroundAssetListResponse,
    summary="List company background assets",
    description="List all background image assets for the current user's company (shared library)",
)
def list_background_assets(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> BackgroundAssetListResponse:
    service = AssetService(db)
    assets = service.list_background_assets(current_user=current_user)
    return BackgroundAssetListResponse(assets=assets)


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


# -------------------------------------------------------------------------
# Terms Assets (Story 5.7)
# -------------------------------------------------------------------------

@router.post(
    "/terms/upload",
    response_model=TermsUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload Terms PDF",
    description="Upload a PDF document for Terms of Agreement (Story 5.7)",
)
async def upload_terms_pdf(
    file: UploadFile = File(..., description="PDF file"),
    display_name: Optional[str] = Form(None),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TermsUploadResponse:
    service = AssetService(db)
    asset, is_duplicate = await service.upload_terms_pdf(
        file=file,
        display_name=display_name,
        current_user=current_user,
    )
    return TermsUploadResponse(asset=asset, isDuplicate=is_duplicate)


@router.post(
    "/terms/url",
    response_model=TermsAssetMetadata,
    status_code=status.HTTP_201_CREATED,
    summary="Add Terms by URL",
    description="Add Terms of Agreement by external URL (HTTPS only, Story 5.7)",
)
def add_terms_url(
    body: TermsUrlAddRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TermsAssetMetadata:
    service = AssetService(db)
    return service.add_terms_url(
        url=body.url,
        display_name=body.display_name,
        display_mode=body.display_mode or "popup",
        current_user=current_user,
    )


@router.post(
    "/terms/validate-url",
    response_model=TermsUrlValidateResponse,
    summary="Validate Terms URL",
    description="Check if URL can be embedded in iframe (Story 5.7)",
)
def validate_terms_url(
    body: TermsUrlValidateRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TermsUrlValidateResponse:
    service = AssetService(db)
    return service.validate_terms_url(body.url)


@router.get(
    "/{asset_id}/resolve",
    response_model=AssetResolveResponse,
    summary="Resolve asset URL",
    description="Resolve runtime URL for asset access without storing absolute hosts",
)
def resolve_asset_url(
    asset_id: int,
    request: Request,
    db: Session = Depends(get_db),
) -> AssetResolveResponse:
    service = AssetService(db)
    url = service.resolve_asset_url(asset_id=asset_id, request=request)
    return AssetResolveResponse(url=url)


@router.delete(
    "/{asset_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Soft-delete asset",
    description="Soft-delete an asset (Story 5.7 - Company Settings). Requires company admin.",
)
def delete_asset(
    asset_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """DELETE /api/assets/{id} — soft-delete. Requires company admin."""
    from common.rbac import require_company_admin_for_company

    asset = db.query(Asset).filter(
        Asset.AssetID == asset_id,
        Asset.IsDeleted == False,  # noqa: E712
    ).first()
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    require_company_admin_for_company(current_user, int(asset.CompanyID))

    asset.IsDeleted = True
    asset.DeletedDate = datetime.utcnow()
    asset.DeletedBy = current_user.user_id
    # Clear company default if this asset was the default Terms
    company = db.get(Company, int(asset.CompanyID))
    if company and getattr(company, "DefaultTermsAssetID", None) == asset_id:
        company.DefaultTermsAssetID = None
    db.commit()


@router.patch(
    "/{asset_id}",
    response_model=BackgroundAssetMetadata,
    summary="Update asset metadata",
    description="Update asset display name (Story 5.7 - Company Settings)",
)
def update_asset_metadata(
    asset_id: int,
    body: AssetUpdateRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """PATCH /api/assets/{id} — update display name. Requires company admin."""
    from common.rbac import require_company_admin_for_company

    asset = db.query(Asset).filter(
        Asset.AssetID == asset_id,
        Asset.IsDeleted == False,  # noqa: E712
    ).first()
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    require_company_admin_for_company(current_user, int(asset.CompanyID))

    if body.display_name is not None:
        asset.DisplayName = body.display_name
    if body.display_width_px is not None:
        asset.DisplayWidthPx = body.display_width_px
    if body.display_height_px is not None:
        asset.DisplayHeightPx = body.display_height_px
    if body.display_rotation_degrees is not None:
        asset.DisplayRotationDegrees = body.display_rotation_degrees
    if any((
        body.display_name is not None,
        body.display_width_px is not None,
        body.display_height_px is not None,
        body.display_rotation_degrees is not None,
    )):
        asset.UpdatedDate = datetime.utcnow()
        asset.UpdatedBy = current_user.user_id
    db.commit()
    db.refresh(asset)
    svc = AssetService(db)
    return svc._to_metadata(asset)


@router.get(
    "/{asset_id}/content",
    summary="Stream asset content",
    description="Stream or redirect to asset content. Use size=thumb for 300x300 thumbnail when available.",
)
def stream_asset_content(
    asset_id: int,
    request: Request,
    size: Optional[str] = Query(None, description="Use 'thumb' for 300x300 thumbnail"),
    viewer: Optional[str] = Query(None, description="Set to 'inline' to view in browser"),
    db: Session = Depends(get_db),
):
    service = AssetService(db)
    return service.get_asset_content_response(asset_id=asset_id, request=request, size=size, viewer=viewer)
