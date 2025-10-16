"""
Multi-Tenant Data Isolation Utilities
Provides helpers for enforcing company-level data isolation (AC-1.8.1, AC-1.8.9)
"""
from sqlalchemy.orm import Query
from fastapi import HTTPException, status
from typing import Optional
import json
from datetime import datetime

from common.logger import get_logger

logger = get_logger(__name__)


def filter_by_company(query: Query, company_id: Optional[int], model_class=None) -> Query:
    """
    Apply company filter to SQLAlchemy query (AC-1.8.1, AC-1.8.9).
    
    Ensures multi-tenant data isolation by filtering queries to only
    return data belonging to the specified company.
    
    Args:
        query: SQLAlchemy Query object
        company_id: Company ID to filter by (from JWT)
        model_class: Optional model class if needed for filtering
        
    Returns:
        Query object with company filter applied
        
    Raises:
        HTTPException: 403 if company_id is None or invalid
        
    Example:
        query = db.query(Event)
        query = filter_by_company(query, current_user.company_id)
        events = query.all()
    """
    if company_id is None:
        logger.warning("Attempted query without company context")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No company context. Please complete onboarding or switch to a company."
        )
    
    if not isinstance(company_id, int) or company_id <= 0:
        logger.error(f"Invalid company_id provided: {company_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid company identifier"
        )
    
    # Apply company filter
    # Assumes model has CompanyID attribute (most company-scoped tables do)
    try:
        return query.filter_by(CompanyID=company_id)
    except Exception as e:
        logger.error(f"Error applying company filter: {str(e)}", exc_info=True)
        # If filter_by fails, try using filter with explicit column
        if model_class and hasattr(model_class, 'CompanyID'):
            return query.filter(model_class.CompanyID == company_id)
        raise


def verify_company_access(
    resource_company_id: int,
    user_company_id: Optional[int],
    resource_type: str = "Resource",
    log_denied_access: bool = True
) -> None:
    """
    Verify user has access to resource's company (AC-1.8.2, AC-1.8.3, AC-1.8.4).
    
    Prevents cross-company data access by verifying the resource
    belongs to the user's current company.
    
    Args:
        resource_company_id: Company ID of the resource being accessed
        user_company_id: Company ID from user's JWT
        resource_type: Type of resource for logging (e.g., "Event", "Form")
        log_denied_access: Whether to log denied access attempts
        
    Raises:
        HTTPException: 403 if companies don't match or user has no company context
        
    Example:
        # Verify user can access event
        event = db.query(Event).filter(Event.EventID == event_id).first()
        verify_company_access(event.CompanyID, current_user.company_id, "Event")
    """
    if user_company_id is None:
        if log_denied_access:
            logger.warning(
                f"Access denied: User attempted to access {resource_type} without company context. "
                f"ResourceCompanyID={resource_company_id}"
            )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No company context. Please complete onboarding or switch to a company."
        )
    
    if resource_company_id != user_company_id:
        if log_denied_access:
            logger.warning(
                f"Cross-company access attempt detected: User with CompanyID={user_company_id} "
                f"attempted to access {resource_type} with CompanyID={resource_company_id}"
            )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied. {resource_type} belongs to a different company."
        )


def log_cross_company_access_attempt(
    db,
    user_id: int,
    user_company_id: Optional[int],
    attempted_company_id: int,
    resource_type: str,
    resource_id: int,
    endpoint: str
) -> None:
    """
    Log cross-company access attempts to audit table (AC-1.8.10).
    
    Creates audit trail for security monitoring and alerting.
    
    Args:
        db: Database session
        user_id: User ID attempting access
        user_company_id: User's actual company ID
        attempted_company_id: Company ID of resource they tried to access
        resource_type: Type of resource (e.g., "Event", "Form")
        resource_id: ID of resource they tried to access
        endpoint: API endpoint where access was attempted
    """
    try:
        from models.audit.activity_log import ActivityLog
        
        audit_log = ActivityLog(
            UserID=user_id,
            CompanyID=user_company_id,  # User's actual company
            Action="CROSS_COMPANY_ACCESS_DENIED",
            EntityType=resource_type,
            EntityID=resource_id,
            OldValue=json.dumps({
                "user_company_id": user_company_id,
                "attempted_company_id": attempted_company_id,
                "endpoint": endpoint,
                "timestamp": datetime.utcnow().isoformat()
            }),
            CreatedDate=datetime.utcnow()
        )
        db.add(audit_log)
        db.commit()
        
        logger.warning(
            f"Cross-company access logged: UserID={user_id}, "
            f"UserCompanyID={user_company_id}, "
            f"AttemptedCompanyID={attempted_company_id}, "
            f"Resource={resource_type}:{resource_id}, "
            f"Endpoint={endpoint}"
        )
    except Exception as e:
        logger.error(f"Failed to log cross-company access attempt: {str(e)}", exc_info=True)


def require_company_context(company_id: Optional[int]) -> int:
    """
    Require valid company context for operation (AC-1.8.1).
    
    Raises exception if user doesn't have a company context.
    Returns company_id if valid.
    
    Args:
        company_id: Company ID from JWT
        
    Returns:
        Valid company_id
        
    Raises:
        HTTPException: 403 if no company context
        
    Example:
        company_id = require_company_context(current_user.company_id)
        events = db.query(Event).filter(Event.CompanyID == company_id).all()
    """
    if company_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No company context. Please complete onboarding or switch to a company."
        )
    
    if not isinstance(company_id, int) or company_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid company identifier"
        )
    
    return company_id


def verify_path_company_matches_user(
    path_company_id: int,
    user_company_id: Optional[int],
    allow_superuser: bool = False
) -> None:
    """
    Verify company_id in URL path matches user's company (AC-1.8.2, AC-1.8.3).
    
    Prevents users from manipulating company_id in URL to access other companies.
    
    Args:
        path_company_id: Company ID from URL path parameter
        user_company_id: Company ID from user's JWT
        allow_superuser: Whether to allow superuser/platform admin access
        
    Raises:
        HTTPException: 403 if companies don't match
        
    Example:
        # Endpoint: POST /api/companies/{company_id}/events
        @router.post("/companies/{company_id}/events")
        async def create_event(
            company_id: int,
            current_user: CurrentUser = Depends(get_current_user),
            ...
        ):
            verify_path_company_matches_user(company_id, current_user.company_id)
            # ... rest of endpoint logic
    """
    if user_company_id is None:
        logger.warning(
            f"User attempted to access company endpoint without company context. "
            f"PathCompanyID={path_company_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No company context. Cannot access company resources."
        )
    
    if path_company_id != user_company_id:
        logger.warning(
            f"Company ID mismatch: User with CompanyID={user_company_id} "
            f"attempted to access CompanyID={path_company_id} via URL path"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access different company's resources"
        )

