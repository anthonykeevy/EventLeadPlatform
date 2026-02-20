"""
Publish Service (Story 5.8)
Shared logic for publish flow: create FormPublicLink PRODUCTION, set FormVersion.IsActive.
Used by approve-and-publish, direct publish.
"""
import secrets
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select, desc

from models.form import Form
from models.form_version import FormVersion
from models.form_public_link import FormPublicLink
from models import FormStatus


def _get_or_create_production_link(db: Session, form_id: int, created_by: int | None) -> FormPublicLink:
    """Get existing PRODUCTION link or create one. Token is stable (never regenerated)."""
    existing = db.execute(
        select(FormPublicLink).where(
            FormPublicLink.FormID == form_id,
            FormPublicLink.LinkType == "PRODUCTION",
        )
    ).scalars().first()

    if existing:
        # Re-activate if was deactivated (re-publish)
        if not existing.IsActive:
            existing.IsActive = True  # type: ignore[assignment]
            db.flush()
        return existing

    # Create new PRODUCTION link with stable token
    for _ in range(5):
        token = secrets.token_urlsafe(32)
        if not db.execute(select(FormPublicLink).where(FormPublicLink.Token == token)).scalars().first():
            link = FormPublicLink(
                FormID=form_id,
                Token=token,
                LinkType="PRODUCTION",
                IsActive=True,
                ExpiresAt=None,
                CreatedBy=created_by,
            )
            db.add(link)
            db.flush()
            return link
    raise RuntimeError("Failed to generate unique token for FormPublicLink")


def publish_form(
    db: Session,
    form_id: int,
    user_id: int,
    unpublish_mode: str = "MANUAL",
    scheduled_unpublish_date: datetime | None = None,
) -> FormPublicLink:
    """
    Publish a form: set Form to PUBLISHED, create/activate FormPublicLink PRODUCTION,
    set latest FormVersion.IsActive. Clear previous active version.
    """
    form = db.execute(
        select(Form).where(Form.FormID == form_id, Form.IsDeleted == False)
    ).scalars().first()
    if not form:
        raise ValueError(f"Form {form_id} not found")

    published_status = db.execute(
        select(FormStatus).where(FormStatus.StatusCode == "PUBLISHED")
    ).scalars().first()
    if not published_status:
        raise ValueError("PUBLISHED status not configured")

    # Get latest version
    version = db.execute(
        select(FormVersion)
        .where(FormVersion.FormID == form_id)
        .order_by(desc(FormVersion.VersionNumber))
    ).scalars().first()
    if not version:
        raise ValueError(f"No form version found for form {form_id}")

    # Clear previous active version for this form
    prev_active = db.execute(
        select(FormVersion).where(
            FormVersion.FormID == form_id,
            FormVersion.IsActive == True,
        )
    ).scalars().all()
    for v in prev_active:
        v.IsActive = False  # type: ignore[assignment]

    # Set this version as active
    version.IsActive = True  # type: ignore[assignment]
    version.Status = "PUBLISHED"  # type: ignore[assignment]
    version.PublishedDate = datetime.utcnow()  # type: ignore[assignment]
    version.PublishedBy = user_id  # type: ignore[assignment]

    # Create or get PRODUCTION link
    link = _get_or_create_production_link(db, form_id, user_id)

    # Update form status and unpublish settings
    form.FormStatusID = published_status.FormStatusID
    form.UnpublishMode = unpublish_mode  # type: ignore[assignment]
    form.ScheduledUnpublishDate = scheduled_unpublish_date  # type: ignore[assignment]
    form.UpdatedBy = user_id
    form.UpdatedDate = datetime.utcnow()

    db.flush()
    return link
