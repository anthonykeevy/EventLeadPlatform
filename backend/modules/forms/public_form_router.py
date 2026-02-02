"""
Public Form Router (Story 3.8)
Resolves a token to the active published DefinitionJSON for rendering.

NOTE: This router is mounted under the shared `/api/public` router (Story 2.12),
so we keep this router's prefix empty and expose `/forms/{token}` paths.
"""
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from datetime import datetime

from common.database import get_db
from common.logger import get_logger

from models.form import Form
from models.form_version import FormVersion
from models.form_public_link import FormPublicLink

from .public_form_schemas import PublicFormResolveResponse

logger = get_logger(__name__)

# Mounted by modules/forms/public_router.py (prefix="/api/public")
router = APIRouter(prefix="", tags=["Public Forms"])


@router.get(
    "/forms/{token}",
    response_model=PublicFormResolveResponse,
    summary="Resolve public form token to active published definition",
)
async def resolve_public_form(
    token: str = Path(..., description="Public form token"),
    db: Session = Depends(get_db),
) -> PublicFormResolveResponse:
    # Handle potential duplicate tokens by selecting the most recent active link
    # (shouldn't happen due to unique constraint, but defensive coding)
    link = db.execute(
        select(FormPublicLink)
        .where(
            FormPublicLink.Token == token,
            FormPublicLink.IsActive == True
        )
        .order_by(desc(FormPublicLink.CreatedDate))
    ).scalars().first()

    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid form link.")

    # Check expiration (IsActive is already filtered in query above)
    if link.ExpiresAt and link.ExpiresAt < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Form link has expired.")

    # Validate form exists and is not deleted
    form = db.execute(
        select(Form).where(
            Form.FormID == link.FormID,
            Form.IsDeleted == False,
        )
    ).scalar_one_or_none()

    if not form:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid form link.")

    # Get active/published version
    # PRODUCTION links resolve to active published version.
    # PREVIEW links resolve to the latest version (draft or published) to support builder preview flows.
    if str(link.LinkType).upper() == "PREVIEW":
        # Get the latest version (highest VersionNumber) - use first() since we're ordering
        version = db.execute(
            select(FormVersion)
            .where(FormVersion.FormID == link.FormID)
            .order_by(desc(FormVersion.VersionNumber))
        ).scalars().first()
    else:
        # PRODUCTION: Get the active published version (should be unique, but use first() defensively)
        version = db.execute(
            select(FormVersion).where(
                FormVersion.FormID == link.FormID,
                FormVersion.IsActive == True,
            )
            .order_by(desc(FormVersion.VersionNumber))  # Get most recent if multiple active
        ).scalars().first()

    if not version:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No form version found for this link.")

    # Update last accessed (best-effort)
    try:
        link.LastAccessedAt = datetime.utcnow()  # type: ignore[assignment]
        db.commit()
    except Exception as e:
        db.rollback()
        logger.warning(f"Failed to update LastAccessedAt for token={token}: {e}")

    return PublicFormResolveResponse(
        linkType=str(link.LinkType),
        definition=version.definition,
    )

