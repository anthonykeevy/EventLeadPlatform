"""
Form Builder Init API Router (Story 5.2 T03)
POST /api/form-builder/init - single payload for form context
"""
from fastapi import APIRouter, Depends, HTTPException, status

from common.database import get_db
from sqlalchemy.orm import Session

from modules.auth.dependencies import get_current_user
from modules.auth.models import CurrentUser

from .schemas import (
    FormBuilderInitRequest,
    FormBuilderInitResponse,
    FormBuilderInitContext,
    FormBuilderComponentItem,
    FormBuilderDefinitionJSON,
)
from .service import build_init_payload


router = APIRouter(prefix="/api/form-builder", tags=["Form Builder"])


@router.post(
    "/init",
    response_model=FormBuilderInitResponse,
    summary="Initialize Form Builder",
    description="Returns merged defaults, component catalog, and DefinitionJSON skeleton for form context",
)
async def form_builder_init(
    body: FormBuilderInitRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> FormBuilderInitResponse:
    """
    POST /api/form-builder/init
    Body: { companyId, eventId }
    Returns: schemaVersion, context, defaults, components, definitionJSON
    """
    try:
        payload = build_init_payload(
            db=db,
            company_id=body.companyId,
            event_id=body.eventId,
            form_id=body.formId,
        )
        return FormBuilderInitResponse(**payload)
    except ValueError as e:
        msg = str(e)
        if "not found" in msg.lower() or "mismatch" in msg.lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=msg,
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg,
        )
