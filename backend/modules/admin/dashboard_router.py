"""
Admin Dashboard Router
Story 2.6: Admin Public Event Review Workflow
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from common.database import get_db
from common.rbac import require_role
from modules.auth.dependencies import get_current_user
from modules.auth.models import CurrentUser
from modules.admin.dashboard_service import AdminDashboardService
from modules.admin.dashboard_schemas import (
    AdminCompanyResponse,
    AdminKPIsResponse,
    AdminEventsListResponse,
)

router = APIRouter(prefix="/admin/dashboard", tags=["Admin Dashboard"])


@router.get(
    "/companies",
    response_model=list[AdminCompanyResponse],
    summary="Get all companies (Admin)",
    description="Get all companies on the platform (admin-only, no company filter)"
)
@require_role("system_admin")
async def get_all_companies(
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> list[AdminCompanyResponse]:
    """Get all companies (admin-only)"""
    service = AdminDashboardService(db)
    return service.get_all_companies()


@router.get(
    "/kpis",
    response_model=AdminKPIsResponse,
    summary="Get platform KPIs (Admin)",
    description="Get platform-wide KPIs (admin-only)"
)
@require_role("system_admin")
async def get_platform_kpis(
    request: Request,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> AdminKPIsResponse:
    """Get platform-wide KPIs (admin-only)"""
    service = AdminDashboardService(db)
    return service.get_platform_kpis()


@router.get(
    "/events",
    response_model=AdminEventsListResponse,
    summary="Get all events (Admin)",
    description="Get all events on the platform (admin-only, no company filter)"
)
@require_role("system_admin")
async def get_all_events(
    request: Request,
    event_status_id: int | None = None,
    event_type_id: int | None = None,
    public_review_status: str | None = None,
    date_filter: str | None = None,  # 'past', 'current', 'future'
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> AdminEventsListResponse:
    """Get all events (admin-only)"""
    service = AdminDashboardService(db)
    
    skip = (page - 1) * page_size
    events, total = service.get_all_events(
        skip=skip,
        limit=page_size,
        event_status_id=event_status_id,
        event_type_id=event_type_id,
        public_review_status=public_review_status,
        date_filter=date_filter,
    )
    
    return AdminEventsListResponse(
        events=events,
        total=total,
        page=page,
        page_size=page_size,
    )
