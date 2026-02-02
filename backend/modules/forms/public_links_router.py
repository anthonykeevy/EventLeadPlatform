"""
Form Public Links Router (Story 3.8)
Authenticated endpoints for creating/listing/revoking token-based public renderer links.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from datetime import datetime
import secrets
import os

from common.database import get_db
from modules.auth.dependencies import get_current_user
from modules.auth.models import CurrentUser
from common.logger import get_logger
from .access_guard import check_form_access_guard

from models.form_public_link import FormPublicLink

from .public_links_schemas import (
    CreatePublicLinkRequest,
    CreatePublicLinkResponse,
    ListPublicLinksResponse,
    RevokePublicLinkResponse,
    PublicLinkResponse,
    PublicLinkType,
)

logger = get_logger(__name__)

# Mounted by modules/forms/router.py (prefix="/api/forms")
router = APIRouter(prefix="", tags=["forms-public-links"])


def _to_link_response(link: FormPublicLink) -> PublicLinkResponse:
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000").rstrip("/")
    token_str = str(link.Token)
    public_url = f"{frontend_url}/forms/{token_str}"
    return PublicLinkResponse(
        token=token_str,
        linkType=str(link.LinkType),
        url=public_url,
        isActive=bool(link.IsActive),
        expiresAt=link.ExpiresAt,  # type: ignore[arg-type]
        createdDate=link.CreatedDate,  # type: ignore[arg-type]
        lastAccessedAt=link.LastAccessedAt,  # type: ignore[arg-type]
    )


@router.post(
    "/{form_id}/public-links",
    response_model=CreatePublicLinkResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create public renderer link token",
)
async def create_public_link(
    form_id: int,
    request: CreatePublicLinkRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CreatePublicLinkResponse:
    # Require MANAGE for issuing public tokens
    await check_form_access_guard(db, form_id, current_user.user_id, "MANAGE")

    link_type = (request.link_type or "").upper().strip()
    if link_type not in (PublicLinkType.PREVIEW, PublicLinkType.PRODUCTION):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid linkType. Use PREVIEW or PRODUCTION.")

    if request.expires_at and request.expires_at <= datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="expiresAt must be in the future.")

    # Generate token; ensure uniqueness (retry a few times)
    token = None
    for _ in range(5):
        candidate = secrets.token_urlsafe(32)
        exists = db.execute(select(FormPublicLink).where(FormPublicLink.Token == candidate)).scalar_one_or_none()
        if not exists:
            token = candidate
            break
    if not token:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate unique token.")

    link = FormPublicLink(
        FormID=form_id,
        Token=token,
        LinkType=link_type,
        IsActive=True,
        ExpiresAt=request.expires_at,
        CreatedBy=current_user.user_id,
    )
    db.add(link)
    db.commit()
    db.refresh(link)

    logger.info(f"Created public link token for FormID={form_id} LinkType={link_type}")

    return CreatePublicLinkResponse(
        success=True,
        message="Public link created",
        link=_to_link_response(link),
    )


@router.get(
    "/{form_id}/public-links",
    response_model=ListPublicLinksResponse,
    summary="List public renderer link tokens",
)
async def list_public_links(
    form_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ListPublicLinksResponse:
    # VIEW is enough to see existing tokens
    await check_form_access_guard(db, form_id, current_user.user_id, "VIEW")

    links = db.execute(
        select(FormPublicLink)
        .where(FormPublicLink.FormID == form_id)
        .order_by(desc(FormPublicLink.CreatedDate))
    ).scalars().all()

    return ListPublicLinksResponse(
        links=[_to_link_response(l) for l in links],
        total=len(links),
    )


@router.post(
    "/{form_id}/public-links/{token}/revoke",
    response_model=RevokePublicLinkResponse,
    summary="Revoke public renderer link token",
)
async def revoke_public_link(
    form_id: int,
    token: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> RevokePublicLinkResponse:
    # Require MANAGE to revoke
    await check_form_access_guard(db, form_id, current_user.user_id, "MANAGE")

    link = db.execute(
        select(FormPublicLink).where(
            FormPublicLink.FormID == form_id,
            FormPublicLink.Token == token,
        )
    ).scalar_one_or_none()

    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Public link token not found.")

    if not link.IsActive:
        return RevokePublicLinkResponse(success=True, message="Public link already revoked", token=token)

    link.IsActive = False  # type: ignore[assignment]
    db.commit()

    logger.info(f"Revoked public link token for FormID={form_id} token={token}")

    return RevokePublicLinkResponse(success=True, message="Public link revoked", token=token)

