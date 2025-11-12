"""
Dashboard Router - Story 1.18
Provides KPI data and dashboard analytics
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import select, func, distinct
from typing import List

from common.database import get_db
from modules.auth.dependencies import get_current_user, CurrentUser
from models.event import Event
from models.ref.event_status import EventStatus
from models.event_company import EventCompany

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get(
    "/kpis",
    summary="Get KPI data for selected companies",
    description="Returns aggregated KPI metrics for specified company IDs"
)
async def get_kpis(
    companyIds: List[int] = [],
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Get KPI data for selected companies.
    AC-1.18.8: KPI components update based on selected company.
    
    Returns actual event counts (including participant events) for specified companies.
    """
    if not companyIds:
        return JSONResponse(
            status_code=200,
            content={
                "totalForms": 0,
                "totalLeads": 0,
                "activeEvents": 0,
                "companyIds": []
            }
        )
    
    # Get Archived status ID to exclude archived events
    archived_status = db.execute(
        select(EventStatus).where(EventStatus.StatusCode == 'ARCHIVED')
    ).scalar_one_or_none()
    
    # Count events for all specified companies
    # Include BOTH:
    # 1. Events directly owned by companies
    # 2. Events where companies are participants (via EventCompany)
    
    # Get event IDs from both sources
    owned_event_ids = db.execute(
        select(Event.EventID).where(
            Event.CompanyID.in_(companyIds),
            Event.IsDeleted == False
        )
    ).scalars().all()
    
    # Get events where companies are participants
    participant_event_ids = db.execute(
        select(EventCompany.EventID).where(
            EventCompany.CompanyID.in_(companyIds),
            EventCompany.IsDeleted == False,
            EventCompany.IsActive == True
        )
    ).scalars().all()
    
    # Combine both lists and get unique event IDs
    all_event_ids = list(set(list(owned_event_ids) + list(participant_event_ids)))
    
    if not all_event_ids:
        active_events = 0
    else:
        # Count unique events, excluding archived
        event_count_stmt = select(func.count(distinct(Event.EventID))).where(
            Event.EventID.in_(all_event_ids),
            Event.IsDeleted == False
        )
        
        # Exclude archived events from count
        if archived_status:
            event_count_stmt = event_count_stmt.where(
                Event.EventStatusID != archived_status.EventStatusID
            )
        
        active_events = db.execute(event_count_stmt).scalar() or 0
    
    return JSONResponse(
        status_code=200,
        content={
            "totalForms": 0,  # TODO: Epic 2
            "totalLeads": 0,  # TODO: Epic 2
            "activeEvents": active_events,
            "companyIds": companyIds
        }
    )




