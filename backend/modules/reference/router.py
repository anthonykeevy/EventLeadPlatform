"""Read-only reference APIs (Story 6.5d clarification dropdowns)."""
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from common.database import get_db
from modules.auth.dependencies import get_current_user
from modules.auth.models import CurrentUser

from . import clarification
from .schemas import RefClarificationItem, RefClarificationListResponse


router = APIRouter(prefix="/api/ref", tags=["Reference"])


def _to_response(payload: clarification.ClarificationListResponse) -> RefClarificationListResponse:
    def _item(row: clarification.ClarificationItem) -> RefClarificationItem:
        return RefClarificationItem(
            code=row.code,
            displayName=row.displayName,
            description=row.description,
            flagEmoji=row.flagEmoji,
            promptHint=row.promptHint,
            clarificationSummary=row.clarificationSummary,
        )

    return RefClarificationListResponse(
        items=[_item(i) for i in payload.items],
        defaultCode=payload.defaultCode,
        resolvedDefault=_item(payload.resolvedDefault),
    )


@router.get("/audience-locales", response_model=RefClarificationListResponse)
async def get_audience_locales(
    formId: Optional[int] = Query(default=None, ge=1),
    code: Optional[str] = Query(default=None, max_length=30),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> RefClarificationListResponse:
    payload = clarification.list_audience_locales(
        db,
        company_id=current_user.company_id,
        form_id=formId,
        request_code=code,
    )
    return _to_response(payload)


@router.get("/form-purposes", response_model=RefClarificationListResponse)
async def get_form_purposes(
    formId: Optional[int] = Query(default=None, ge=1),
    code: Optional[str] = Query(default=None, max_length=50),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> RefClarificationListResponse:
    payload = clarification.list_form_purposes(
        db,
        company_id=current_user.company_id,
        form_id=formId,
        request_code=code,
    )
    return _to_response(payload)


@router.get("/respondent-types", response_model=RefClarificationListResponse)
async def get_respondent_types(
    formId: Optional[int] = Query(default=None, ge=1),
    code: Optional[str] = Query(default=None, max_length=50),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> RefClarificationListResponse:
    payload = clarification.list_respondent_types(
        db,
        company_id=current_user.company_id,
        form_id=formId,
        request_code=code,
    )
    return _to_response(payload)
