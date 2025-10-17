"""
User Service Module
Business logic for user profile management
"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional
from datetime import datetime

from backend.models.user import User
from backend.models.ref.timezone import Timezone
from backend.models.audit.user_audit import UserAudit
from backend.common.logger import get_logger

logger = get_logger(__name__)


async def update_user_details(
    db: Session,
    user_id: int,
    phone: Optional[str],
    timezone_identifier: str,
    role_title: Optional[str]
) -> User:
    """
    Update user profile details.
    
    Args:
        db: Database session
        user_id: User ID to update
        phone: Phone number (optional)
        timezone_identifier: IANA timezone identifier
        role_title: Job title (optional)
        
    Returns:
        Updated User object
        
    Raises:
        ValueError: If timezone is invalid or user not found
    """
    # Validate timezone exists
    timezone = db.execute(
        select(Timezone).where(Timezone.TimezoneIdentifier == timezone_identifier)
    ).scalar_one_or_none()
    
    if not timezone:
        raise ValueError(f"Invalid timezone: {timezone_identifier}")
    
    # Get user
    user = db.execute(
        select(User).where(User.UserID == user_id)
    ).scalar_one_or_none()
    
    if not user:
        raise ValueError(f"User not found: {user_id}")
    
    # Store old values for audit
    old_values = {
        "Phone": user.Phone,
        "TimezoneIdentifier": user.TimezoneIdentifier,
        "RoleTitle": user.RoleTitle
    }
    
    # Update user details
    user.Phone = phone  # type: ignore
    user.TimezoneIdentifier = timezone_identifier  # type: ignore
    user.RoleTitle = role_title  # type: ignore
    user.UpdatedDate = datetime.utcnow()  # type: ignore
    user.UpdatedBy = user_id  # type: ignore
    
    # Log to audit table
    audit_entry = UserAudit(
        UserID=user_id,
        Action="UPDATE_PROFILE",
        OldValue=str(old_values),
        NewValue=str({
            "Phone": phone,
            "TimezoneIdentifier": timezone_identifier,
            "RoleTitle": role_title
        }),
        ChangedBy=user_id,
        ChangeDate=datetime.utcnow(),
        IPAddress=None,  # TODO: Get from request context if needed
        UserAgent=None   # TODO: Get from request context if needed
    )
    db.add(audit_entry)
    
    db.commit()
    db.refresh(user)
    
    logger.info(f"User details updated: UserID={user_id}, Timezone={timezone_identifier}")
    
    return user


async def get_user_profile(db: Session, user_id: int) -> Optional[User]:
    """
    Get user profile by ID.
    
    Args:
        db: Database session
        user_id: User ID
        
    Returns:
        User object or None if not found
    """
    return db.execute(
        select(User).where(User.UserID == user_id)
    ).scalar_one_or_none()

