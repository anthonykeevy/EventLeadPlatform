"""
Dashboard Router - Story 1.18
Provides KPI data and dashboard analytics
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from common.database import get_db
from modules.auth.dependencies import get_current_user, CurrentUser

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
    
    For Epic 1: Returns placeholder/zero values (events/forms in Epic 2)
    """
    # TODO Epic 2: Query actual events/forms tables
    # For now, return zeros (no events/forms exist yet)
    
    return JSONResponse(
        status_code=200,
        content={
            "totalForms": 0,
            "totalLeads": 0,
            "activeEvents": 0,
            "companyIds": companyIds
        }
    )



