"""
Public Form Router (Story 3.8)
Resolves a token to the active published DefinitionJSON for rendering.

NOTE: This router is mounted under the shared `/api/public` router (Story 2.12),
so we keep this router's prefix empty and expose `/forms/{token}` paths.
"""
import json
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Path, Request, Response, status
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from sqlalchemy.exc import IntegrityError

from common.database import get_db
from common.logger import get_logger

from models.form import Form
from models.form_version import FormVersion
from models.form_public_link import FormPublicLink
from models.form_submission import FormSubmission
from models.log.frontend_event import FrontendEvent

from .public_form_schemas import PublicFormResolveResponse
from .public_submission_schemas import (
    PublicFormSubmissionRequest,
    PublicFormSubmissionResponse,
    PublicValidationEventRequest,
)

logger = get_logger(__name__)

# Mounted by modules/forms/public_router.py (prefix="/api/public")
router = APIRouter(prefix="", tags=["Public Forms"])


def _raise_invalid_link() -> None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid form link.")


def _parse_submitted_at_client(submitted_at_client: str) -> datetime:
    try:
        normalized = submitted_at_client
        if normalized.endswith("Z"):
            normalized = normalized[:-1] + "+00:00"
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="submittedAtClient must be an ISO-8601 string.",
        ) from exc

    if parsed.tzinfo is not None:
        parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)

    return parsed


def _parse_occurred_at_client(occurred_at_client: str) -> int | None:
    try:
        normalized = occurred_at_client
        if normalized.endswith("Z"):
            normalized = normalized[:-1] + "+00:00"
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None

    if parsed.tzinfo is not None:
        parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)

    return int(parsed.timestamp() * 1000)


def _extract_ip_country_code(request: Request | None) -> str | None:
    if not request:
        return None
    raw = request.headers.get("CF-IPCountry")
    if not raw:
        return None
    normalized = raw.strip().upper()
    if len(normalized) == 2 and normalized.isalpha():
        return normalized
    return None


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


@router.post(
    "/forms/{token}/submissions",
    response_model=PublicFormSubmissionResponse,
    summary="Submit public form responses",
)
async def submit_public_form(
    payload: PublicFormSubmissionRequest,
    request: Request,
    token: str = Path(..., description="Public form token"),
    db: Session = Depends(get_db),
) -> PublicFormSubmissionResponse:
    link = db.execute(
        select(FormPublicLink)
        .where(
            FormPublicLink.Token == token,
            FormPublicLink.IsActive == True,
        )
        .order_by(desc(FormPublicLink.CreatedDate))
    ).scalars().first()

    if not link:
        _raise_invalid_link()

    if link.ExpiresAt and link.ExpiresAt < datetime.utcnow():
        _raise_invalid_link()
    assert link is not None

    form = db.execute(
        select(Form).where(
            Form.FormID == link.FormID,
            Form.IsDeleted == False,
        )
    ).scalar_one_or_none()

    if not form:
        _raise_invalid_link()
    assert form is not None

    link_type = str(link.LinkType).upper()
    if link_type == "PREVIEW":
        version = db.execute(
            select(FormVersion)
            .where(FormVersion.FormID == link.FormID)
            .order_by(desc(FormVersion.VersionNumber))
        ).scalars().first()
    else:
        version = db.execute(
            select(FormVersion).where(
                FormVersion.FormID == link.FormID,
                FormVersion.IsActive == True,
            )
            .order_by(desc(FormVersion.VersionNumber))
        ).scalars().first()

    if not version:
        _raise_invalid_link()
    assert version is not None

    submitted_at_client = _parse_submitted_at_client(payload.submitted_at_client)
    context_payload = payload.context.dict(by_alias=True, exclude_none=True)
    ip_country_code = _extract_ip_country_code(request)
    if ip_country_code:
        context_payload["ipCountryCode"] = ip_country_code

    submission = FormSubmission(
        FormID=link.FormID,
        FormVersionID=version.FormVersionID,
        FormPublicLinkID=link.FormPublicLinkID,
        LinkType=link_type,
        IdempotencyKey=payload.idempotency_key,
        SubmittedAtClient=submitted_at_client,
        AnswersJSON=json.dumps(payload.answers_by_component_id),
        ContextJSON=json.dumps(context_payload),
    )

    try:
        db.add(submission)

        now = datetime.utcnow()
        form.TotalSubmissions = (form.TotalSubmissions or 0) + 1
        form.LastSubmissionDate = now
        if link_type == "PREVIEW":
            form.DemoLeadsCollected = (form.DemoLeadsCollected or 0) + 1
        else:
            form.ProductionLeadsCollected = (form.ProductionLeadsCollected or 0) + 1

        db.commit()
        db.refresh(submission)

        return PublicFormSubmissionResponse(
            submissionId=submission.FormSubmissionID,
            status="ACCEPTED",
        )
    except IntegrityError:
        db.rollback()
        existing = db.execute(
            select(FormSubmission).where(
                FormSubmission.FormPublicLinkID == link.FormPublicLinkID,
                FormSubmission.IdempotencyKey == payload.idempotency_key,
            )
        ).scalars().first()

        if existing:
            return PublicFormSubmissionResponse(
                submissionId=existing.FormSubmissionID,
                status="DUPLICATE",
            )

        logger.error(
            "Submission insert failed with IntegrityError but no duplicate found for token=%s",
            token,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to record submission.",
        )
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.error(f"Failed to record submission for token={token}: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to record submission.",
        )


@router.post(
    "/forms/{token}/telemetry/validation",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Store validation failure telemetry",
)
async def submit_validation_telemetry(
    payload: PublicValidationEventRequest,
    request: Request,
    token: str = Path(..., description="Public form token"),
    db: Session = Depends(get_db),
) -> Response:
    link = db.execute(
        select(FormPublicLink)
        .where(
            FormPublicLink.Token == token,
            FormPublicLink.IsActive == True,
        )
        .order_by(desc(FormPublicLink.CreatedDate))
    ).scalars().first()

    if not link:
        _raise_invalid_link()

    if link.ExpiresAt and link.ExpiresAt < datetime.utcnow():
        _raise_invalid_link()
    assert link is not None

    form = db.execute(
        select(Form).where(
            Form.FormID == link.FormID,
            Form.IsDeleted == False,
        )
    ).scalar_one_or_none()

    if not form:
        _raise_invalid_link()
    assert form is not None

    link_type = str(link.LinkType).upper()
    failures = payload.failures or []
    primary_failure = failures[0] if failures else None

    event_payload = payload.dict(by_alias=True)
    event_payload.update(
        {
            "formId": link.FormID,
            "formPublicLinkId": link.FormPublicLinkID,
            "linkTypeResolved": link_type,
        }
    )

    try:
        frontend_event = FrontendEvent(
            EventType=payload.event_type,
            Level="warn",
            ComponentID=primary_failure.component_id if primary_failure else None,
            ComponentType=primary_failure.component_type if primary_failure else None,
            Payload=json.dumps(event_payload),
            SessionID=payload.client_session_id,
            BrowserInfo=request.headers.get("user-agent") if request else None,
            PageURL=request.headers.get("referer") if request else None,
            ClientTimestamp=_parse_occurred_at_client(payload.occurred_at_client),
        )
        db.add(frontend_event)
        db.commit()
    except Exception as exc:
        db.rollback()
        logger.error("Failed to store validation telemetry for token=%s: %s", token, exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to store validation telemetry.",
        ) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)

