"""
User Service Module
Business logic for user management (creation, verification, updates)
"""
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session

from models.user import User
from models.ref.user_status import UserStatus
from common.security import hash_password


def create_user(
    db: Session,
    email: str,
    password: str,
    first_name: str,
    last_name: str
) -> User:
    """
    Create new user with hashed password.
    User starts inactive and unverified.
    
    Args:
        db: Database session
        email: User's email address
        password: Plain text password (will be hashed)
        first_name: User's first name
        last_name: User's last name
        
    Returns:
        Created User object
        
    Security Notes:
        - Password is hashed with bcrypt (cost factor 12)
        - User starts with EmailVerified=false, IsActive=false
        - User status set to "Pending Verification"
    """
    # Hash password
    hashed_password = hash_password(password)
    
    # Get "Pending Verification" status
    pending_status = db.query(UserStatus).filter(
        UserStatus.StatusName == "Pending Verification"
    ).first()
    
    # Create user record
    user = User(
        Email=email,
        PasswordHash=hashed_password,
        FirstName=first_name,
        LastName=last_name,
        EmailVerified=False,
        IsActive=False,
        UserStatusID=pending_status.UserStatusID if pending_status else None,
        CreatedDate=datetime.utcnow(),
        UpdatedDate=datetime.utcnow(),
        IsDeleted=False
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


def verify_user_email(db: Session, user_id: int) -> User:
    """
    Verify user's email and activate account.
    
    Args:
        db: Database session
        user_id: ID of user to verify
        
    Returns:
        Updated User object
        
    Changes:
        - EmailVerified set to True
        - IsActive set to True
        - UserStatusID updated to "Active"
    """
    # Find user
    user = db.query(User).filter(User.UserID == user_id).first()
    
    if not user:
        raise ValueError(f"User with ID {user_id} not found")
    
    # Get "Active" status
    active_status = db.query(UserStatus).filter(
        UserStatus.StatusName == "Active"
    ).first()
    
    # Update user
    user.EmailVerified = True
    user.IsActive = True
    user.UserStatusID = active_status.UserStatusID if active_status else user.UserStatusID
    user.UpdatedDate = datetime.utcnow()
    
    db.commit()
    db.refresh(user)
    
    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Find user by email address.
    
    Args:
        db: Database session
        email: Email address to search for
        
    Returns:
        User object if found, None otherwise
    """
    return db.query(User).filter(
        User.Email == email,
        User.IsDeleted == False
    ).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    Find user by ID.
    
    Args:
        db: Database session
        user_id: User ID to search for
        
    Returns:
        User object if found, None otherwise
    """
    return db.query(User).filter(
        User.UserID == user_id,
        User.IsDeleted == False
    ).first()

