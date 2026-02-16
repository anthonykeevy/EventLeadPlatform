"""
Form Readiness Router (Story 5.5)
Endpoints for test threshold, readiness badge, record test run.
"""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from common.database import get_db
from modules.auth.dependencies import get_current_user
from modules.auth.models import CurrentUser

from .access_guard import check_form_access_guard
from .readiness_service import (
    check_publish_readiness,
    record_test_run,
    get_company_test_config,
)
from models.company_form_test_config import CompanyFormTestConfig

router = APIRouter(prefix="/api/forms", tags=["forms", "readiness"])


class ReadinessResponse(BaseModel):
    canPublish: bool = Field(..., alias="canPublish")
    testRunCount: int = Field(..., alias="testRunCount")
    testThresholdRequired: int = Field(..., alias="testThresholdRequired")
    testRunsNeeded: int = Field(..., alias="testRunsNeeded")
    message: str = Field(..., alias="message")

    class Config:
        populate_by_name = True


class CompanyTestConfigResponse(BaseModel):
    testThresholdEnabled: bool = Field(..., alias="testThresholdEnabled")
    testThresholdValue: int = Field(..., alias="testThresholdValue")
    requirePublishApproval: bool = Field(..., alias="requirePublishApproval")

    class Config:
        populate_by_name = True


class CompanyTestConfigUpdate(BaseModel):
    testThresholdEnabled: bool = Field(..., alias="testThresholdEnabled")
    testThresholdValue: int = Field(..., ge=0, le=100, alias="testThresholdValue")
    requirePublishApproval: bool | None = Field(None, alias="requirePublishApproval")

    class Config:
        populate_by_name = True


@router.get(
    "/{form_id}/readiness",
    response_model=ReadinessResponse,
    summary="Get form publish readiness (Story 5.5)",
)
async def get_form_readiness(
    form_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Returns readiness status for publish (test run count vs threshold)."""
    form = await check_form_access_guard(db, form_id, current_user.user_id, "VIEW")
    result = check_publish_readiness(db, form_id, form.CompanyID)
    return ReadinessResponse(
        canPublish=result["canPublish"],
        testRunCount=result["testRunCount"],
        testThresholdRequired=result["testThresholdRequired"],
        testRunsNeeded=result["testRunsNeeded"],
        message=result["message"],
    )


@router.post(
    "/{form_id}/record-test-run",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Record explicit test run (Story 5.5)",
)
async def post_record_test_run(
    form_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Records explicit 'Record test run' for forms without submission (e.g. static forms)."""
    form = await check_form_access_guard(db, form_id, current_user.user_id, "EDIT")
    try:
        record_test_run(db, form_id, current_user.user_id, current_user.company_id)
        db.commit()
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/company-test-config",
    response_model=CompanyTestConfigResponse,
    summary="Get company test threshold config (Story 5.5)",
)
async def get_company_test_config_endpoint(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Returns test threshold config for current user's company."""
    enabled, value, require_approval = get_company_test_config(db, current_user.company_id)
    return CompanyTestConfigResponse(
        testThresholdEnabled=enabled,
        testThresholdValue=value,
        requirePublishApproval=require_approval,
    )


@router.put(
    "/company-test-config",
    response_model=CompanyTestConfigResponse,
    summary="Update company test threshold config (Story 5.5)",
)
async def put_company_test_config(
    body: CompanyTestConfigUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Updates test threshold config for current user's company. Requires company admin."""
    from common.rbac import require_company_admin_for_company

    require_company_admin_for_company(current_user, current_user.company_id)

    row = db.execute(
        select(CompanyFormTestConfig).where(
            CompanyFormTestConfig.CompanyID == current_user.company_id
        )
    ).scalars().first()

    if row:
        row.TestThresholdEnabled = body.testThresholdEnabled
        row.TestThresholdValue = body.testThresholdValue
        if body.requirePublishApproval is not None:
            row.RequirePublishApproval = body.requirePublishApproval
        row.UpdatedDate = datetime.utcnow()
        row.UpdatedBy = current_user.user_id
    else:
        row = CompanyFormTestConfig(
            CompanyID=current_user.company_id,
            TestThresholdEnabled=body.testThresholdEnabled,
            TestThresholdValue=body.testThresholdValue,
            RequirePublishApproval=body.requirePublishApproval if body.requirePublishApproval is not None else False,
            CreatedBy=current_user.user_id,
        )
        db.add(row)

    db.commit()
    db.refresh(row)
    return CompanyTestConfigResponse(
        testThresholdEnabled=bool(row.TestThresholdEnabled),
        testThresholdValue=int(row.TestThresholdValue),
        requirePublishApproval=bool(getattr(row, "RequirePublishApproval", False)),
    )
