"""
Public Form Router (Story 3.8)
Resolves a token to the active published DefinitionJSON for rendering.

NOTE: This router is mounted under the shared `/api/public` router (Story 2.12),
so we keep this router's prefix empty and expose `/forms/{token}` paths.
"""
import json
import socket
import asyncio
from datetime import datetime, timezone
from urllib.parse import urlparse

from fastapi import APIRouter, Depends, File, HTTPException, Path, Request, Response, UploadFile, status
from fastapi import Form as FormField
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from sqlalchemy.exc import IntegrityError

from common.database import get_db
from common.logger import get_logger

from models.form import Form
from models.form_version import FormVersion
from models.form_public_link import FormPublicLink
from models.form_submission import FormSubmission
from models.form_republish_request import FormRepublishRequest
from models.ref.form_status import FormStatus
from models.event import Event
from models.log.frontend_event import FrontendEvent

from modules.form_defaults.service import resolve_definition_for_render

from .public_form_schemas import PublicFormResolveResponse
from .public_submission_schemas import (
    PublicAttachmentUploadResponse,
    PublicFormSubmissionRequest,
    PublicFormSubmissionResponse,
    PublicValidationEventRequest,
    PublicUrlDnsValidationRequest,
    PublicUrlDnsValidationResponse,
)
from .submission_attachment_service import (
    create_pending_attachment,
    validate_and_bind_attachments_for_submission,
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

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    else:
        parsed = parsed.astimezone(timezone.utc)

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


def _normalize_url_for_dns_check(raw_url: str) -> tuple[str, str]:
    value = (raw_url or "").strip()
    if not value:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="URL is required.",
        )

    candidate = value if "://" in value else f"https://{value}"
    parsed = urlparse(candidate)
    hostname = (parsed.hostname or "").strip().lower()
    if not hostname:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Please enter a valid URL.",
        )

    if hostname in {"localhost", "127.0.0.1", "::1"} or hostname.endswith(".local"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Local hostnames are not allowed.",
        )

    if parsed.scheme not in {"http", "https"}:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Only http and https URLs are supported.",
        )

    return candidate, hostname


@router.get(
    "/forms/{token}",
    response_model=PublicFormResolveResponse,
    summary="Resolve public form token to active published definition",
)
async def resolve_public_form(
    token: str = Path(..., description="Public form token"),
    db: Session = Depends(get_db),
) -> PublicFormResolveResponse:
    # Find link by token (include inactive for unpublished page - Story 5.8)
    link = db.execute(
        select(FormPublicLink)
        .where(FormPublicLink.Token == token)
        .order_by(desc(FormPublicLink.CreatedDate))
    ).scalars().first()

    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid form link.")

    if link.ExpiresAt and link.ExpiresAt < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Form link has expired.")

    form = db.execute(
        select(Form).where(
            Form.FormID == link.FormID,
            Form.IsDeleted == False,
        )
    ).scalar_one_or_none()

    if not form:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid form link.")

    form_status = db.execute(
        select(FormStatus).where(FormStatus.FormStatusID == form.FormStatusID)
    ).scalars().first()
    status_code = form_status.StatusCode if form_status else ""

    # Story 5.8: Unpublished form - serve dedicated page (no 404)
    if not link.IsActive or status_code == "UNPUBLISHED":
        return PublicFormResolveResponse(
            linkType="UNPUBLISHED",
            definition=None,
            message="This form is no longer active. It has been unpublished.",
        )

    # PRODUCTION: Check activation window (Event.StartDateTime–EndDateTime)
    if str(link.LinkType).upper() == "PRODUCTION" and form.EventID:
        event = db.execute(
            select(Event).where(Event.EventID == form.EventID, Event.IsDeleted == False)
        ).scalars().first()
        if event:
            now = datetime.utcnow()
            if event.StartDateTime and event.StartDateTime > now:
                return PublicFormResolveResponse(
                    linkType="EVENT_ENDED",
                    definition=None,
                    message="This form is not yet active. The event has not started.",
                )
            if event.EndDateTime and event.EndDateTime < now:
                return PublicFormResolveResponse(
                    linkType="EVENT_ENDED",
                    definition=None,
                    message="This form is no longer active. The event has ended.",
                )

    # Get active/published version
    if str(link.LinkType).upper() == "PREVIEW":
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No form version found for this link.")

    try:
        resolved_def = resolve_definition_for_render(db, form.CompanyID, version.definition)
    except ValueError:
        resolved_def = version.definition

    try:
        link.LastAccessedAt = datetime.utcnow()  # type: ignore[assignment]
        db.commit()
    except Exception as e:
        db.rollback()
        logger.warning(f"Failed to update LastAccessedAt for token={token}: {e}")

    return PublicFormResolveResponse(
        linkType=str(link.LinkType),
        definition=resolved_def,
    )


@router.post(
    "/forms/{token}/request-republish",
    status_code=status.HTTP_200_OK,
    summary="Request admin to re-publish form (Story 5.8)",
)
async def request_republish(
    request: Request,
    token: str = Path(..., description="Public form token"),
    db: Session = Depends(get_db),
):
    """
    Visitor on unpublished form page clicks CTA. Creates FormRepublishRequest record.
    In-app notification to Company Admins: placeholder for MVP (no notification system yet).
    """
    link = db.execute(
        select(FormPublicLink).where(FormPublicLink.Token == token)
    ).scalars().first()
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid form link.")

    form = db.execute(
        select(Form).where(Form.FormID == link.FormID, Form.IsDeleted == False)
    ).scalar_one_or_none()
    if not form:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid form link.")

    ip = getattr(request.client, "host", None) if getattr(request, "client", None) else None
    ua = (request.headers.get("user-agent") or "")[:500]

    req = FormRepublishRequest(
        FormID=form.FormID,
        IPAddress=ip,
        UserAgent=ua,
    )
    db.add(req)
    db.commit()

    # TODO: In-app notification to Company Admins - notification system not yet implemented
    logger.info(f"Republish requested for FormID={form.FormID} (FormRepublishRequestID={req.FormRepublishRequestID})")

    return {"success": True, "message": "Your request has been recorded. The administrator will be notified."}


@router.post(
    "/forms/{token}/attachments",
    response_model=PublicAttachmentUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload file for a public form file-upload field (Story 6.2.2)",
)
async def upload_public_form_attachment(
    file: UploadFile = File(..., description="File to upload"),
    component_id: str = FormField(..., alias="componentId"),
    client_session_id: str = FormField(..., alias="clientSessionId"),
    token: str = Path(..., description="Public form token"),
    db: Session = Depends(get_db),
) -> PublicAttachmentUploadResponse:
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

    form = db.execute(
        select(Form).where(
            Form.FormID == link.FormID,
            Form.IsDeleted == False,
        )
    ).scalar_one_or_none()

    if not form:
        _raise_invalid_link()

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

    body = await file.read()
    filename = file.filename or "upload"
    content_type = file.content_type or "application/octet-stream"

    try:
        public_id, is_dup = create_pending_attachment(
            db,
            link=link,
            version=version,
            component_id=component_id,
            file_body=body,
            original_filename=filename,
            content_type=content_type,
            client_session_key=client_session_id,
        )
        db.commit()
    except ValueError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        db.rollback()
        logger.error("Public attachment upload failed for token=%s: %s", token, exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Upload failed.",
        ) from exc

    return PublicAttachmentUploadResponse(
        attachmentId=public_id,
        duplicateOfExisting=is_dup,
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
        IsPreview=(link_type == "PREVIEW"),
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

        db.flush()
        try:
            validate_and_bind_attachments_for_submission(
                db,
                link=link,
                client_session_key=payload.context.client_session_id,
                answers_by_component_id=payload.answers_by_component_id,
                definition_raw=version.definition,
                submission_id=submission.FormSubmissionID,
            )
        except ValueError as exc:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(exc),
            ) from exc

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


@router.post(
    "/forms/{token}/validate-url-dns",
    response_model=PublicUrlDnsValidationResponse,
    summary="Validate URL hostname resolves via DNS",
)
async def validate_public_url_dns(
    payload: PublicUrlDnsValidationRequest,
    token: str = Path(..., description="Public form token"),
    db: Session = Depends(get_db),
) -> PublicUrlDnsValidationResponse:
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

    normalized_url, hostname = _normalize_url_for_dns_check(payload.url)
    if not payload.check_dns:
        return PublicUrlDnsValidationResponse(
            isValid=True,
            normalizedUrl=normalized_url,
            hostname=hostname,
            reason=None,
        )

    try:
        loop = asyncio.get_running_loop()
        records = await asyncio.wait_for(
            loop.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP),
            timeout=2.0,
        )
        if not records:
            return PublicUrlDnsValidationResponse(
                isValid=False,
                normalizedUrl=normalized_url,
                hostname=hostname,
                reason="Hostname could not be resolved by DNS.",
            )
    except asyncio.TimeoutError:
        return PublicUrlDnsValidationResponse(
            isValid=False,
            normalizedUrl=normalized_url,
            hostname=hostname,
            reason="DNS lookup timed out.",
        )
    except socket.gaierror:
        return PublicUrlDnsValidationResponse(
            isValid=False,
            normalizedUrl=normalized_url,
            hostname=hostname,
            reason="Hostname could not be resolved by DNS.",
        )
    except Exception as exc:
        logger.warning("Unexpected DNS validation error for token=%s host=%s: %s", token, hostname, exc)
        return PublicUrlDnsValidationResponse(
            isValid=False,
            normalizedUrl=normalized_url,
            hostname=hostname,
            reason="Unable to verify DNS at this time.",
        )

    return PublicUrlDnsValidationResponse(
        isValid=True,
        normalizedUrl=normalized_url,
        hostname=hostname,
        reason=None,
    )

