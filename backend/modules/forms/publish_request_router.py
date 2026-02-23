"""
Form Publish Request Router (Story 5.6, 5.8)
Endpoints for create publish request, list pending, approve (only or and-publish), unpublish, direct publish.
"""
import json
from datetime import datetime

from fastapi import APIRouter, Body, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from common.database import get_db
from common.logger import get_logger
from common.rbac import require_company_admin_for_company
from modules.auth.dependencies import get_current_user
from modules.auth.models import CurrentUser

from .access_guard import check_form_access_guard
from .readiness_service import check_publish_readiness, get_company_test_config
from .publish_service import publish_form
from models.form import Form
from models.form_publish_request import FormPublishRequest
from models.form_public_link import FormPublicLink
from models import FormStatus, FormApprovalStatus
from models.audit.activity_log import ActivityLog

logger = get_logger(__name__)

router = APIRouter(prefix="/api/forms", tags=["forms", "publish-request"])


def _log_activity(
    db: Session,
    user_id: int,
    company_id: int,
    action: str,
    form_id: int,
    form_name: str,
    details: str,
    user_email: str | None = None,
    **extra,
) -> None:
    """Log to audit.ActivityLog for platform audit trail."""
    try:
        new_value_data = {"form_id": form_id, "form_name": form_name, "details": details, **extra}
        log = ActivityLog(
            UserID=user_id,
            UserEmail=user_email,
            CompanyID=company_id,
            Action=action,
            EntityType="Form",
            EntityID=form_id,
            NewValue=json.dumps(new_value_data),
            CreatedDate=datetime.utcnow(),
        )
        db.add(log)
        db.flush()
    except Exception as e:
        logger.warning(f"Failed to log activity {action}: {e}")


class PublishRequestCreate(BaseModel):
    message: str | None = Field(None, max_length=1000, alias="message")

    class Config:
        populate_by_name = True


class PublishRequestResponse(BaseModel):
    formPublishRequestId: int = Field(..., alias="formPublishRequestId")
    formId: int = Field(..., alias="formId")
    formName: str = Field(..., alias="formName")
    requestedBy: int = Field(..., alias="requestedBy")
    requestedByEmail: str | None = Field(None, alias="requestedByEmail")
    requestedAt: str = Field(..., alias="requestedAt")
    message: str | None = Field(None, alias="message")
    status: str = Field(..., alias="status")

    class Config:
        populate_by_name = True


def _is_company_admin(user: CurrentUser) -> bool:
    return user.role in ("company_admin", "system_admin")


@router.post(
    "/{form_id}/publish-request",
    response_model=PublishRequestResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create publish request (Story 5.6)",
)
async def post_publish_request(
    form_id: int,
    body: PublishRequestCreate | None = Body(default=None),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Company User creates a publish request when RequirePublishApproval is enabled.
    Validates readiness (test threshold), sets form status to Pending Review.
    Duplicate: returns existing pending request (idempotent).
    """
    form = await check_form_access_guard(db, form_id, current_user.user_id, "EDIT")
    if form.CompanyID != current_user.company_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Form does not belong to your company")

    _, _, require_approval, form_cost_threshold = get_company_test_config(db, form.CompanyID)
    form_cost = float(form.DeploymentCost) if form.DeploymentCost is not None else 0.0
    cost_gate = form_cost_threshold is not None and form_cost > form_cost_threshold
    needs_approval = require_approval or cost_gate

    # Company Admin can publish directly - no need to request (optional: block or allow)
    if _is_company_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Company Admins can publish directly. Use the Publish action instead.",
        )

    if not needs_approval:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Publish approval is not required for this form. You can publish directly.",
        )

    # Validate readiness
    readiness = check_publish_readiness(db, form_id, form.CompanyID)
    if not readiness["canPublish"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=readiness["message"],
        )

    # Check for existing pending request (idempotent)
    existing = (
        db.execute(
            select(FormPublishRequest)
            .where(
                FormPublishRequest.FormID == form_id,
                FormPublishRequest.Status == "pending",
            )
        )
        .scalars().first()
    )
    if existing:
        # Return existing as success (idempotent)
        from models.user import User

        requester = db.execute(select(User).where(User.UserID == existing.RequestedBy)).scalars().first()
        return PublishRequestResponse(
            formPublishRequestId=existing.FormPublishRequestID,
            formId=existing.FormID,
            formName=form.FormName,
            requestedBy=existing.RequestedBy,
            requestedByEmail=requester.Email if requester else None,
            requestedAt=existing.RequestedAt.isoformat() if existing.RequestedAt else "",
            message=existing.Message,
            status=existing.Status,
        )

    # Get PENDING_REVIEW FormStatus and PENDING FormApprovalStatus
    pending_status = (
        db.execute(
            select(FormStatus).where(FormStatus.StatusCode == "PENDING_REVIEW")
        )
        .scalars().first()
    )
    pending_approval = (
        db.execute(
            select(FormApprovalStatus).where(FormApprovalStatus.ApprovalStatusCode == "PENDING")
        )
        .scalars().first()
    )
    if not pending_status:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="PENDING_REVIEW status not configured. Please run migrations.",
        )
    if not pending_approval:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="PENDING approval status not configured. Please run migrations.",
        )

    msg = (body.message if body else None) or ""
    req = FormPublishRequest(
        FormID=form_id,
        RequestedBy=current_user.user_id,
        Message=msg[:1000] if msg else None,
        Status="pending",
        CompanyID=form.CompanyID,
        CreatedBy=current_user.user_id,
    )
    db.add(req)
    form.FormStatusID = pending_status.FormStatusID
    form.FormApprovalStatusID = pending_approval.FormApprovalStatusID
    _log_activity(
        db,
        current_user.user_id,
        form.CompanyID,
        "form.publish_requested",
        form_id,
        form.FormName,
        "Form status → Pending Admin Review; publish request created",
        user_email=current_user.email,
        form_publish_request_id=req.FormPublishRequestID,
        requested_by=current_user.user_id,
    )
    db.commit()
    db.refresh(req)

    from models.user import User

    requester = db.execute(select(User).where(User.UserID == req.RequestedBy)).scalars().first()
    return PublishRequestResponse(
        formPublishRequestId=req.FormPublishRequestID,
        formId=req.FormID,
        formName=form.FormName,
        requestedBy=req.RequestedBy,
        requestedByEmail=requester.Email if requester else None,
        requestedAt=req.RequestedAt.isoformat() if req.RequestedAt else "",
        message=req.Message,
        status=req.Status,
    )


@router.get(
    "/publish-requests/pending",
    response_model=list[PublishRequestResponse],
    summary="List pending publish requests (Story 5.6, Admin only)",
)
async def get_pending_publish_requests(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Returns pending publish requests for current user's company. Admin only."""
    if not current_user.company_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No company context")
    require_company_admin_for_company(current_user, current_user.company_id)

    # Option 1: Exclude deleted/archived forms (soft-delete + FormStatus ARCHIVED/DELETED)
    # Future Option 2: On Form delete/archive, cascade status to related FormPublishRequest etc.
    archived_deleted_ids = db.execute(
        select(FormStatus.FormStatusID).where(
            FormStatus.StatusCode.in_(["ARCHIVED", "DELETED"])
        )
    ).scalars().all()
    # scalars().all() returns flat list of IDs; don't use [r[0]]
    archived_deleted_id_list = list(archived_deleted_ids) if archived_deleted_ids else []

    base_filter = [
        FormPublishRequest.CompanyID == current_user.company_id,
        FormPublishRequest.Status == "pending",
        Form.IsDeleted == False,
    ]
    if archived_deleted_id_list:
        base_filter.append(Form.FormStatusID.notin_(archived_deleted_id_list))

    rows = (
        db.execute(
            select(FormPublishRequest, Form.FormName)
            .join(Form, Form.FormID == FormPublishRequest.FormID)
            .where(*base_filter)
            .order_by(FormPublishRequest.RequestedAt.desc())
        )
        .all()
    )

    from models.user import User

    results = []
    for req, form_name in rows:
        requester = db.execute(select(User).where(User.UserID == req.RequestedBy)).scalars().first()
        results.append(
            PublishRequestResponse(
                formPublishRequestId=req.FormPublishRequestID,
                formId=req.FormID,
                formName=form_name,
                requestedBy=req.RequestedBy,
                requestedByEmail=requester.Email if requester else None,
                requestedAt=req.RequestedAt.isoformat() if req.RequestedAt else "",
                message=req.Message,
                status=req.Status,
            )
        )
    return results


class PublishRequestApproveBody(BaseModel):
    comment: str | None = Field(None, max_length=1000, alias="comment")
    publish: bool = Field(True, alias="publish")  # True = Approve & Publish; False = Approve only
    unpublish_mode: str | None = Field("MANUAL", alias="unpublishMode")  # MANUAL | EVENT_END | SCHEDULED
    scheduled_unpublish_date: str | None = Field(None, alias="scheduledUnpublishDate")  # ISO date when SCHEDULED

    class Config:
        populate_by_name = True


class PublishRequestRejectBody(BaseModel):
    reason: str | None = Field(None, max_length=1000, alias="reason")

    class Config:
        populate_by_name = True


def _parse_scheduled_date(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


@router.post(
    "/{form_id}/publish-request/approve",
    response_model=PublishRequestResponse,
    summary="Approve publish request (Story 5.6, 5.8 — Approve only or Approve & Publish)",
)
async def approve_publish_request(
    form_id: int,
    body: PublishRequestApproveBody | None = Body(default=None),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Company Admin approves a pending publish request.
    publish=True: Approve & Publish (form published, FormPublicLink created).
    publish=False: Approve only (form stays Ready to publish; admin can publish later with one click).
    """
    require_company_admin_for_company(current_user, current_user.company_id)
    form = await check_form_access_guard(db, form_id, current_user.user_id, "MANAGE")
    if form.CompanyID != current_user.company_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Form does not belong to your company")

    req = (
        db.execute(
            select(FormPublishRequest).where(
                FormPublishRequest.FormID == form_id,
                FormPublishRequest.Status == "pending",
                FormPublishRequest.CompanyID == current_user.company_id,
            )
        )
        .scalars().first()
    )
    if not req:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No pending publish request found for this form.",
        )

    do_publish = body.publish if body else True
    unpublish_mode = (body.unpublish_mode or "MANUAL").upper() if body else "MANUAL"
    scheduled_date = _parse_scheduled_date(body.scheduled_unpublish_date if body else None) if body else None

    if unpublish_mode not in ("MANUAL", "EVENT_END", "SCHEDULED"):
        unpublish_mode = "MANUAL"
    if unpublish_mode == "EVENT_END" and not form.EventID:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event end date unpublish requires form to be linked to an event.",
        )
    if unpublish_mode == "SCHEDULED" and not scheduled_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Scheduled unpublish requires a date.",
        )

    req.Status = "approved"
    req.UpdatedBy = current_user.user_id
    req.UpdatedDate = datetime.utcnow()

    approved_approval_status = (
        db.execute(
            select(FormApprovalStatus).where(FormApprovalStatus.ApprovalStatusCode == "APPROVED")
        )
        .scalars().first()
    )
    if not approved_approval_status:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="APPROVED approval status not configured.",
        )

    form.FormApprovalStatusID = approved_approval_status.FormApprovalStatusID
    form.UpdatedBy = current_user.user_id
    form.UpdatedDate = datetime.utcnow()

    if do_publish:
        try:
            publish_form(db, form_id, current_user.user_id, unpublish_mode, scheduled_date)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        _log_activity(
            db,
            current_user.user_id,
            form.CompanyID,
            "form.publish_request_approved",
            form_id,
            form.FormName,
            "Publish request approved and form published",
            user_email=current_user.email,
            form_publish_request_id=req.FormPublishRequestID,
            published=True,
        )
        _log_activity(
            db,
            current_user.user_id,
            form.CompanyID,
            "form.published",
            form_id,
            form.FormName,
            "Form published (via Approve & Publish)",
            user_email=current_user.email,
            form_publish_request_id=req.FormPublishRequestID,
        )
    else:
        # Approve only: set Form Status to APPROVED_FOR_PUBLISH
        approved_for_publish_status = (
            db.execute(
                select(FormStatus).where(FormStatus.StatusCode == "APPROVED_FOR_PUBLISH")
            )
            .scalars().first()
        )
        if approved_for_publish_status:
            form.FormStatusID = approved_for_publish_status.FormStatusID
        _log_activity(
            db,
            current_user.user_id,
            form.CompanyID,
            "form.publish_request_approved",
            form_id,
            form.FormName,
            "Publish request approved (Approve only); form ready to publish",
            user_email=current_user.email,
            form_publish_request_id=req.FormPublishRequestID,
            published=False,
        )

    db.commit()
    db.refresh(req)

    from models.user import User
    requester = db.execute(select(User).where(User.UserID == req.RequestedBy)).scalars().first()
    return PublishRequestResponse(
        formPublishRequestId=req.FormPublishRequestID,
        formId=form_id,
        formName=form.FormName,
        requestedBy=req.RequestedBy,
        requestedByEmail=requester.Email if requester else None,
        requestedAt=req.RequestedAt.isoformat() if req.RequestedAt else "",
        message=req.Message,
        status=req.Status,
    )


@router.post(
    "/{form_id}/publish",
    response_model=PublishRequestResponse,
    summary="Direct publish (Story 5.8 — Admin or when RequirePublishApproval=false)",
)
async def direct_publish(
    form_id: int,
    body: PublishRequestApproveBody | None = Body(default=None),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Publish form directly (no request). Used when: (1) Admin publishes after Approve only,
    (2) RequirePublishApproval=false and any user publishes. Subject to test threshold.
    """
    form = await check_form_access_guard(db, form_id, current_user.user_id, "EDIT")
    if form.CompanyID != current_user.company_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Form does not belong to your company")

    *_, require_approval = get_company_test_config(db, form.CompanyID)
    if require_approval and not _is_company_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Publish approval is required. Request publish for admin review.",
        )

    readiness = check_publish_readiness(db, form_id, form.CompanyID)
    if not readiness["canPublish"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=readiness["message"])

    unpublish_mode = (body.unpublish_mode or "MANUAL").upper() if body else "MANUAL"
    scheduled_date = _parse_scheduled_date(body.scheduled_unpublish_date if body else None) if body else None
    if unpublish_mode not in ("MANUAL", "EVENT_END", "SCHEDULED"):
        unpublish_mode = "MANUAL"
    if unpublish_mode == "EVENT_END" and not form.EventID:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Event end date requires form linked to event.")
    if unpublish_mode == "SCHEDULED" and not scheduled_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Scheduled unpublish requires a date.")

    try:
        link = publish_form(db, form_id, current_user.user_id, unpublish_mode, scheduled_date)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    _log_activity(
        db,
        current_user.user_id,
        form.CompanyID,
        "form.published",
        form_id,
        form.FormName,
        "Form published directly (no publish request)",
        user_email=current_user.email,
    )
    db.commit()

    from models.user import User
    return PublishRequestResponse(
        formPublishRequestId=0,
        formId=form_id,
        formName=form.FormName,
        requestedBy=current_user.user_id,
        requestedByEmail=current_user.email,
        requestedAt=datetime.utcnow().isoformat(),
        message=None,
        status="approved",
    )


@router.post(
    "/{form_id}/unpublish",
    response_model=dict,
    summary="Unpublish form (Story 5.8)",
)
async def unpublish_form(
    form_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Set form to UNPUBLISHED; deactivate FormPublicLink PRODUCTION."""
    require_company_admin_for_company(current_user, current_user.company_id)
    form = await check_form_access_guard(db, form_id, current_user.user_id, "MANAGE")
    if form.CompanyID != current_user.company_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Form does not belong to your company")

    unpublished_status = db.execute(
        select(FormStatus).where(FormStatus.StatusCode == "UNPUBLISHED")
    ).scalars().first()
    if not unpublished_status:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="UNPUBLISHED status not configured.")

    links = db.execute(
        select(FormPublicLink).where(
            FormPublicLink.FormID == form_id,
            FormPublicLink.LinkType == "PRODUCTION",
        )
    ).scalars().all()
    for link in links:
        link.IsActive = False  # type: ignore[assignment]

    form.FormStatusID = unpublished_status.FormStatusID
    form.UpdatedBy = current_user.user_id
    form.UpdatedDate = datetime.utcnow()

    _log_activity(
        db,
        current_user.user_id,
        form.CompanyID,
        "form.unpublished",
        form_id,
        form.FormName,
        "Form unpublished; production link deactivated",
        user_email=current_user.email,
    )
    db.commit()
    return {"success": True, "message": "Form unpublished", "formId": form_id}


@router.get(
    "/{form_id}/review-context",
    response_model=dict,
    summary="Get form review context (Story 5.8)",
)
async def get_form_review_context(
    form_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Returns form status, hasPendingRequest, hasApprovedRequest, productionUrl, event, unpublish settings."""
    require_company_admin_for_company(current_user, current_user.company_id)
    form = await check_form_access_guard(db, form_id, current_user.user_id, "VIEW")
    if form.CompanyID != current_user.company_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Form does not belong to your company")

    from models import FormStatus
    from models.event import Event

    form_status = db.execute(
        select(FormStatus).where(FormStatus.FormStatusID == form.FormStatusID)
    ).scalars().first()
    status_code = form_status.StatusCode if form_status else ""

    pending = db.execute(
        select(FormPublishRequest).where(
            FormPublishRequest.FormID == form_id,
            FormPublishRequest.Status == "pending",
        )
    ).scalars().first()

    # Unified approval: when form is PENDING_REVIEW with no request (e.g. manually changed status),
    # create a retroactive request so FormReviewPage shows buttons.
    if status_code == "PENDING_REVIEW" and pending is None:
        _, _, require_approval, form_cost_threshold = get_company_test_config(db, form.CompanyID)
        form_cost = float(form.DeploymentCost) if form.DeploymentCost is not None else 0.0
        cost_gate = form_cost_threshold is not None and form_cost > form_cost_threshold
        needs_approval = require_approval or cost_gate
        if needs_approval:
            retro = FormPublishRequest(
                FormID=form_id,
                RequestedBy=form.CreatedBy or current_user.user_id,
                Message="Retroactive request (form moved to Pending Admin Review)",
                Status="pending",
                CompanyID=form.CompanyID,
                CreatedBy=current_user.user_id,
            )
            db.add(retro)
            db.commit()
            db.refresh(retro)
            pending = retro

    approved = db.execute(
        select(FormPublishRequest)
        .where(
            FormPublishRequest.FormID == form_id,
            FormPublishRequest.Status == "approved",
        )
        .order_by(FormPublishRequest.FormPublishRequestID.desc())
    ).scalars().first()

    link = db.execute(
        select(FormPublicLink).where(
            FormPublicLink.FormID == form_id,
            FormPublicLink.LinkType == "PRODUCTION",
            FormPublicLink.IsActive == True,
        )
    ).scalars().first()

    import os
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000").rstrip("/")
    production_url = f"{frontend_url}/forms/{link.Token}" if link else None

    event = None
    if form.EventID:
        event = db.execute(
            select(Event).where(Event.EventID == form.EventID, Event.IsDeleted == False)
        ).scalars().first()

    return {
        "formStatus": status_code,
        "hasPendingRequest": pending is not None,
        "hasApprovedRequest": approved is not None,
        "productionUrl": production_url,
        "productionToken": str(link.Token) if link else None,
        "unpublishMode": getattr(form, "UnpublishMode", "MANUAL") or "MANUAL",
        "scheduledUnpublishDate": form.ScheduledUnpublishDate.isoformat() if getattr(form, "ScheduledUnpublishDate", None) else None,
        "eventEndDate": event.EndDateTime.isoformat() if event and event.EndDateTime else None,
    }


@router.get(
    "/{form_id}/public-url",
    response_model=dict,
    summary="Get production URL for published form (Story 5.8)",
)
async def get_form_public_url(
    form_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return production URL and token when form is published."""
    await check_form_access_guard(db, form_id, current_user.user_id, "VIEW")

    link = db.execute(
        select(FormPublicLink).where(
            FormPublicLink.FormID == form_id,
            FormPublicLink.LinkType == "PRODUCTION",
            FormPublicLink.IsActive == True,
        )
    ).scalars().first()

    if not link:
        return {"url": None, "token": None, "isPublished": False}

    import os
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000").rstrip("/")
    url = f"{frontend_url}/forms/{link.Token}"
    return {"url": url, "token": str(link.Token), "isPublished": True}


@router.post(
    "/{form_id}/publish-request/reject",
    response_model=PublishRequestResponse,
    summary="Reject publish request (Story 5.6, Admin only)",
)
async def reject_publish_request(
    form_id: int,
    body: PublishRequestRejectBody | None = Body(default=None),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Company Admin rejects a pending publish request. Sets form back to DRAFT, request to declined.
    """
    require_company_admin_for_company(current_user, current_user.company_id)
    form = await check_form_access_guard(db, form_id, current_user.user_id, "MANAGE")
    if form.CompanyID != current_user.company_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Form does not belong to your company")

    req = (
        db.execute(
            select(FormPublishRequest).where(
                FormPublishRequest.FormID == form_id,
                FormPublishRequest.Status == "pending",
                FormPublishRequest.CompanyID == current_user.company_id,
            )
        )
        .scalars().first()
    )
    if not req:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No pending publish request found for this form.",
        )

    draft_status = db.execute(select(FormStatus).where(FormStatus.StatusCode == "DRAFT")).scalars().first()
    rejected_approval_status = db.execute(
        select(FormApprovalStatus).where(FormApprovalStatus.ApprovalStatusCode == "REJECTED")
    ).scalars().first()
    if not draft_status:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="DRAFT status not configured.")
    if not rejected_approval_status:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="REJECTED approval status not configured.")

    req.Status = "declined"
    req.UpdatedBy = current_user.user_id
    req.UpdatedDate = datetime.utcnow()
    form.FormStatusID = draft_status.FormStatusID
    form.FormApprovalStatusID = rejected_approval_status.FormApprovalStatusID
    form.UpdatedBy = current_user.user_id
    form.UpdatedDate = datetime.utcnow()

    _log_activity(
        db,
        current_user.user_id,
        form.CompanyID,
        "form.publish_request_rejected",
        form_id,
        form.FormName,
        "Publish request rejected; form reverted to Draft",
        user_email=current_user.email,
        form_publish_request_id=req.FormPublishRequestID,
        requested_by=req.RequestedBy,
    )
    db.commit()
    db.refresh(req)

    from models.user import User
    requester = db.execute(select(User).where(User.UserID == req.RequestedBy)).scalars().first()
    return PublishRequestResponse(
        formPublishRequestId=req.FormPublishRequestID,
        formId=form_id,
        formName=form.FormName,
        requestedBy=req.RequestedBy,
        requestedByEmail=requester.Email if requester else None,
        requestedAt=req.RequestedAt.isoformat() if req.RequestedAt else "",
        message=req.Message,
        status=req.Status,
    )
