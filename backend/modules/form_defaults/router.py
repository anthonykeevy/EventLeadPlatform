"""
Form Defaults API Router (Story 5.2)
CRUD for Global Form Defaults; company routes live under /api/companies/{id}/form-defaults
"""
import json
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from common.database import get_db
from common.rbac import require_role
from modules.auth.dependencies import get_current_user
from modules.auth.models import CurrentUser

from .schemas import (
    FormDefaultsResponse,
    FormDefaultsHistoryResponse,
    FormDefaultsVersionEntry,
    UpdateFormDefaultsRequest,
)
from .service import (
    get_global_defaults,
    update_global_defaults,
    get_global_history,
)


router = APIRouter(prefix="/api/form-defaults", tags=["Form Defaults"])


# =============================================================================
# Global Defaults (admin only)
# =============================================================================

@router.get(
    "/global",
    response_model=FormDefaultsResponse,
    summary="Get global defaults",
    description="Get current platform-wide form defaults (admin only)",
)
@require_role("system_admin")
async def get_global(
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> FormDefaultsResponse:
    row = get_global_defaults(db)
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Global form defaults not found. Run migration 039.",
        )
    return FormDefaultsResponse(
        defaults=json.loads(row.DefaultsJSON),
        versionNumber=row.VersionNumber,
    )


@router.put(
    "/global",
    response_model=FormDefaultsResponse,
    summary="Update global defaults",
    description="Update platform-wide form defaults (admin only)",
)
@require_role("system_admin")
async def put_global(
    request: Request,
    body: UpdateFormDefaultsRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> FormDefaultsResponse:
    try:
        row = update_global_defaults(
            db=db,
            defaults=body.defaults,
            user_id=current_user.user_id,
            change_summary=body.changeSummary,
        )
        return FormDefaultsResponse(
            defaults=json.loads(row.DefaultsJSON),
            versionNumber=row.VersionNumber,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/global/history",
    response_model=FormDefaultsHistoryResponse,
    summary="Get global defaults history",
    description="Get version history for global defaults (admin only)",
)
@require_role("system_admin")
async def get_global_history_endpoint(
    request: Request,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> FormDefaultsHistoryResponse:
    rows = get_global_history(db, limit=limit)
    items = [
        FormDefaultsVersionEntry(
            versionNumber=r[0],
            defaults=json.loads(r[1]),
            changeSummary=r[2],
            createdDate=r[3].isoformat() if r[3] else "",
            createdBy=r[4],
        )
        for r in rows
    ]
    return FormDefaultsHistoryResponse(items=items, total=len(items))
