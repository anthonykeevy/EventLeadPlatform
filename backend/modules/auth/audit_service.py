"""
Audit Service Module
Handles audit logging for authentication events and user changes
"""
from datetime import datetime
from typing import Optional, Dict, Any
import json
from sqlalchemy.orm import Session

from models.log.auth_event import AuthEvent
from models.audit.user_audit import UserAudit
from common.request_context import get_current_request_context


def log_auth_event(
    db: Session,
    user_id: int,
    event_type: str,
    success: bool = True,
    details: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> AuthEvent:
    """
    Log authentication event to log.AuthEvent table.
    
    Args:
        db: Database session
        user_id: ID of user associated with event
        event_type: Type of auth event (SIGNUP, LOGIN, LOGOUT, EMAIL_VERIFICATION, etc.)
        success: Whether event was successful
        details: Additional event details (JSON serializable dict)
        ip_address: IP address of request (optional, will try to get from context)
        user_agent: User agent string (optional, will try to get from context)
        
    Returns:
        Created AuthEvent record
        
    Event Types:
        - SIGNUP: User registration
        - EMAIL_VERIFICATION: Email verification completed
        - LOGIN: User login attempt
        - LOGOUT: User logout
        - PASSWORD_RESET_REQUEST: Password reset requested
        - PASSWORD_RESET_COMPLETE: Password reset completed
        - TOKEN_REFRESH: JWT token refreshed
    """
    # Try to get request context
    request_id = None
    try:
        context = get_current_request_context()
        request_id = context.request_id
        ip_address = ip_address or context.ip_address
        user_agent = user_agent or context.user_agent
    except RuntimeError:
        # No request context available (e.g., background task)
        pass
    
    # Create auth event
    auth_event = AuthEvent(
        UserID=user_id,
        EventType=event_type,
        EventStatus="SUCCESS" if success else "FAILURE",
        IPAddress=ip_address,
        UserAgent=user_agent,
        Details=json.dumps(details) if details else None,
        RequestID=request_id,
        CreatedDate=datetime.utcnow()
    )
    
    db.add(auth_event)
    db.commit()
    db.refresh(auth_event)
    
    return auth_event


def log_user_audit(
    db: Session,
    user_id: int,
    table_name: str,
    action: str,
    field_name: Optional[str] = None,
    old_value: Optional[str] = None,
    new_value: Optional[str] = None,
    changed_by_user_id: Optional[int] = None
) -> UserAudit:
    """
    Log user data changes to audit.UserAudit table.
    
    Args:
        db: Database session
        user_id: ID of user being modified
        table_name: Name of table being modified (e.g., "dbo.User")
        action: Type of action (INSERT, UPDATE, DELETE)
        field_name: Name of field being changed (for UPDATE)
        old_value: Previous value (for UPDATE)
        new_value: New value (for INSERT/UPDATE)
        changed_by_user_id: ID of user making the change (optional)
        
    Returns:
        Created UserAudit record
        
    Example:
        >>> log_user_audit(
        ...     db=db,
        ...     user_id=123,
        ...     table_name="dbo.User",
        ...     action="UPDATE",
        ...     field_name="EmailVerified",
        ...     old_value="False",
        ...     new_value="True"
        ... )
    """
    # Try to get request context
    request_id = None
    try:
        context = get_current_request_context()
        request_id = context.request_id
        changed_by_user_id = changed_by_user_id or context.user_id
    except RuntimeError:
        pass
    
    # Create audit record
    audit = UserAudit(
        UserID=user_id,
        TableName=table_name,
        Action=action,
        FieldName=field_name,
        OldValue=old_value,
        NewValue=new_value,
        ChangedByUserID=changed_by_user_id,
        RequestID=request_id,
        CreatedDate=datetime.utcnow()
    )
    
    db.add(audit)
    db.commit()
    db.refresh(audit)
    
    return audit


def log_user_creation(db: Session, user_id: int, email: str) -> None:
    """
    Log user creation with relevant fields.
    
    Args:
        db: Database session
        user_id: ID of newly created user
        email: Email address of new user
    """
    log_user_audit(
        db=db,
        user_id=user_id,
        table_name="dbo.User",
        action="INSERT",
        field_name="Email",
        new_value=email
    )
    
    log_user_audit(
        db=db,
        user_id=user_id,
        table_name="dbo.User",
        action="INSERT",
        field_name="EmailVerified",
        new_value="False"
    )
    
    log_user_audit(
        db=db,
        user_id=user_id,
        table_name="dbo.User",
        action="INSERT",
        field_name="IsActive",
        new_value="False"
    )


def log_email_verification(db: Session, user_id: int) -> None:
    """
    Log email verification completion.
    
    Args:
        db: Database session
        user_id: ID of user whose email was verified
    """
    log_user_audit(
        db=db,
        user_id=user_id,
        table_name="dbo.User",
        action="UPDATE",
        field_name="EmailVerified",
        old_value="False",
        new_value="True"
    )
    
    log_user_audit(
        db=db,
        user_id=user_id,
        table_name="dbo.User",
        action="UPDATE",
        field_name="IsActive",
        old_value="False",
        new_value="True"
    )

