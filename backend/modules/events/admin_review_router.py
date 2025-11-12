"""
Admin Review Router
Story 2.6: Admin Public Event Review Workflow
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from common.database import get_db
from common.rbac import require_role
from modules.auth.dependencies import get_current_user
from modules.auth.models import CurrentUser
from modules.events.admin_review_service import AdminReviewService
from modules.events.admin_review_schemas import (
    ApproveEventRequest,
    RejectEventRequest,
    PendingReviewEventResponse,
    ReviewHistoryResponse,
    EventReviewStatusResponse,
    EventReviewDetailsResponse,
)

router = APIRouter(prefix="/admin/events", tags=["Admin Review"])


@router.get(
    "/pending-review",
    response_model=list[PendingReviewEventResponse],
    summary="Get pending review events",
    description="List all events pending admin review"
)
@require_role("system_admin")
async def get_pending_review_events(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> list[PendingReviewEventResponse]:
    """Get events pending review"""
    service = AdminReviewService(db)
    return service.get_pending_review_events(skip=skip, limit=limit)


@router.get(
    "/{event_id}/review",
    response_model=EventReviewDetailsResponse,
    summary="Get event review details",
    description="Get complete event information for review"
)
@require_role("system_admin")
async def get_event_review_details(
    request: Request,
    event_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> EventReviewDetailsResponse:
    """Get event review details"""
    service = AdminReviewService(db)
    details = service.get_event_review_details(event_id)
    
    if not details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event {event_id} not found"
        )
    
    return details


@router.post(
    "/{event_id}/approve",
    summary="Approve event",
    description="Approve event for public visibility"
)
@require_role("system_admin")
async def approve_event(
    request: Request,
    event_id: int,
    approve_request: ApproveEventRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    """Approve event"""
    service = AdminReviewService(db)
    
    try:
        service.approve_event(
            event_id=event_id,
            admin_user_id=current_user.user_id,
            comment=approve_request.comment,
            public_visibility_date=approve_request.public_visibility_date,
        )
        return {"success": True, "message": "Event approved successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/{event_id}/reject",
    summary="Reject event",
    description="Reject event from public visibility"
)
@require_role("system_admin")
async def reject_event(
    request: Request,
    event_id: int,
    reject_request: RejectEventRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    """Reject event"""
    service = AdminReviewService(db)
    
    try:
        service.reject_event(
            event_id=event_id,
            admin_user_id=current_user.user_id,
            comment=reject_request.comment,
        )
        return {"success": True, "message": "Event rejected successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/{event_id}/review-history",
    response_model=list[ReviewHistoryResponse],
    summary="Get review history",
    description="Get review history for an event"
)
@require_role("system_admin")
async def get_review_history(
    request: Request,
    event_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> list[ReviewHistoryResponse]:
    """Get review history for event"""
    service = AdminReviewService(db)
    return service.get_review_history(event_id=event_id)


@router.get(
    "/{event_id}/review-status",
    response_model=EventReviewStatusResponse,
    summary="Get review status (for creators)",
    description="Get review status for event creators"
)
async def get_event_review_status(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> EventReviewStatusResponse:
    """Get review status (accessible to event creators)"""
    service = AdminReviewService(db)
    status_response = service.get_event_review_status(event_id)
    
    if not status_response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event {event_id} not found"
        )
    
    return status_response
