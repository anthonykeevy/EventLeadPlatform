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
    user_id: Optional[int],  # Changed to Optional - can be None for failed auth attempts
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
        Reason=json.dumps(details) if details else None,  # Store details in Reason field
        Email=details.get("email") if details else None,  # Extract email if present
        IPAddress=ip_address,
        UserAgent=user_agent,
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
    change_type: str,
    field_name: Optional[str] = None,
    old_value: Optional[str] = None,
    new_value: Optional[str] = None,
    change_reason: Optional[str] = None,
    changed_by_user_id: Optional[int] = None,
    changed_by_email: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> UserAudit:
    """
    Log user data changes to audit.UserAudit table.
    
    Args:
        db: Database session
        user_id: ID of user being modified
        change_type: Type of change (INSERT, UPDATE, DELETE, STATUS_CHANGE, etc.)
        field_name: Name of field being changed (for UPDATE)
        old_value: Previous value (for UPDATE)
        new_value: New value (for INSERT/UPDATE)
        change_reason: Optional reason for change
        changed_by_user_id: ID of user making the change (optional)
        changed_by_email: Email of user making the change (optional)
        ip_address: IP address of change (optional)
        user_agent: User agent of change (optional)
        
    Returns:
        Created UserAudit record
        
    Example:
        >>> log_user_audit(
        ...     db=db,
        ...     user_id=123,
        ...     change_type="UPDATE",
        ...     field_name="IsEmailVerified",
        ...     old_value="False",
        ...     new_value="True"
        ... )
    """
    # Try to get request context
    try:
        context = get_current_request_context()
        changed_by_user_id = changed_by_user_id or context.user_id
        ip_address = ip_address or context.ip_address
        user_agent = user_agent or context.user_agent
    except RuntimeError:
        # No request context available (e.g., background task)
        pass
    
    # Create audit record
    audit = UserAudit(
        UserID=user_id,
        ChangeType=change_type,
        FieldName=field_name,
        OldValue=old_value,
        NewValue=new_value,
        ChangeReason=change_reason,
        ChangedBy=changed_by_user_id,
        ChangedByEmail=changed_by_email,
        IPAddress=ip_address,
        UserAgent=user_agent,
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
        change_type="INSERT",
        field_name="Email",
        new_value=email
    )
    
    log_user_audit(
        db=db,
        user_id=user_id,
        change_type="INSERT",
        field_name="IsEmailVerified",
        new_value="False"
    )
    
    log_user_audit(
        db=db,
        user_id=user_id,
        change_type="INSERT",
        field_name="StatusID",
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
        change_type="STATUS_CHANGE",
        field_name="IsEmailVerified",
        old_value="False",
        new_value="True"
    )
    
    log_user_audit(
        db=db,
        user_id=user_id,
        change_type="STATUS_CHANGE",
        field_name="StatusID",
        old_value="False",
        new_value="True"
    )


