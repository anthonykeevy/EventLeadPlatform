"""
Form Publish Request Router (Story 5.6)
Endpoints for create publish request and list pending requests.
"""
from datetime import datetime

from fastapi import APIRouter, Body, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from common.database import get_db
from common.rbac import require_company_admin_for_company
from modules.auth.dependencies import get_current_user
from modules.auth.models import CurrentUser

from .access_guard import check_form_access_guard
from .readiness_service import check_publish_readiness, get_company_test_config
from models.form import Form
from models.form_publish_request import FormPublishRequest
from models import FormStatus

router = APIRouter(prefix="/api/forms", tags=["forms", "publish-request"])


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

    _, _, require_approval = get_company_test_config(db, form.CompanyID)

    # Company Admin can publish directly - no need to request (optional: block or allow)
    if _is_company_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Company Admins can publish directly. Use the Publish action instead.",
        )

    if not require_approval:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Publish approval is not required for your company. You can publish directly.",
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

    # Get PENDING_REVIEW FormStatus
    pending_status = (
        db.execute(
            select(FormStatus).where(FormStatus.StatusCode == "PENDING_REVIEW")
        )
        .scalars().first()
    )
    if not pending_status:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="PENDING_REVIEW status not configured. Please run migrations.",
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

    rows = (
        db.execute(
            select(FormPublishRequest, Form.FormName)
            .join(Form, Form.FormID == FormPublishRequest.FormID)
            .where(
                FormPublishRequest.CompanyID == current_user.company_id,
                FormPublishRequest.Status == "pending",
            )
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

    class Config:
        populate_by_name = True


class PublishRequestRejectBody(BaseModel):
    reason: str | None = Field(None, max_length=1000, alias="reason")

    class Config:
        populate_by_name = True


@router.post(
    "/{form_id}/publish-request/approve",
    response_model=PublishRequestResponse,
    summary="Approve publish request (Story 5.6, Admin only)",
)
async def approve_publish_request(
    form_id: int,
    body: PublishRequestApproveBody | None = Body(default=None),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Company Admin approves a pending publish request. Sets form to PUBLISHED, request to approved.
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

    published_status = db.execute(select(FormStatus).where(FormStatus.StatusCode == "PUBLISHED")).scalars().first()
    if not published_status:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="PUBLISHED status not configured.")

    req.Status = "approved"
    req.UpdatedBy = current_user.user_id
    req.UpdatedDate = datetime.utcnow()
    form.FormStatusID = published_status.FormStatusID
    form.UpdatedBy = current_user.user_id
    form.UpdatedDate = datetime.utcnow()

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
    if not draft_status:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="DRAFT status not configured.")

    req.Status = "declined"
    req.UpdatedBy = current_user.user_id
    req.UpdatedDate = datetime.utcnow()
    form.FormStatusID = draft_status.FormStatusID
    form.UpdatedBy = current_user.user_id
    form.UpdatedDate = datetime.utcnow()

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
