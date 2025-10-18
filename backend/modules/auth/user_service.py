"""
User Service Module
Business logic for user management (creation, verification, updates)
"""
from datetime import datetime
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
import json

from models.user import User
from models.ref.user_status import UserStatus
from models.user_invitation import UserInvitation
from models.user_company import UserCompany
from models.ref.user_company_status import UserCompanyStatus
from models.ref.user_invitation_status import UserInvitationStatus
from models.ref.joined_via import JoinedVia
from models.audit.activity_log import ActivityLog
from common.security import hash_password
from common.logger import get_logger

logger = get_logger(__name__)


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
    user.EmailVerified = True  # type: ignore
    user.IsActive = True  # type: ignore
    user.UserStatusID = active_status.UserStatusID if active_status else user.UserStatusID  # type: ignore
    user.UpdatedDate = datetime.utcnow()  # type: ignore
    
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


async def create_user_with_invitation(
    db: Session,
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    invitation_token: str
) -> Tuple[User, UserInvitation, UserCompany]:
    """
    Create user and automatically accept invitation (AC-1.7.5, AC-1.7.6).
    
    Handles signup flow for invited users:
    1. Validate invitation token
    2. Verify email matches invitation
    3. Create user account (activated immediately)
    4. Create UserCompany relationship
    5. Mark invitation as accepted
    6. Skip onboarding (user joins existing company)
    
    Args:
        db: Database session
        email: User's email address
        password: Plain text password (will be hashed)
        first_name: User's first name
        last_name: User's last name
        invitation_token: Invitation token
        
    Returns:
        Tuple of (user, invitation, user_company)
        
    Raises:
        ValueError: If validation fails
    """
    # Get invitation
    invitation = db.execute(
        select(UserInvitation).where(
            and_(
                UserInvitation.InvitationToken == invitation_token,
                UserInvitation.IsDeleted == False
            )
        )
    ).scalar_one_or_none()
    
    if not invitation:
        raise ValueError("Invitation not found")
    
    # Check if expired
    if invitation.ExpiresAt < datetime.utcnow():
        raise ValueError("Invitation has expired")
    
    # Check invitation status
    status = db.execute(
        select(UserInvitationStatus).where(
            UserInvitationStatus.UserInvitationStatusID == invitation.StatusID
        )
    ).scalar_one()
    
    if status.StatusCode != "pending":
        raise ValueError(f"Invitation cannot be accepted (status: {status.StatusName})")
    
    # Verify email matches invitation (security check)
    if invitation.Email.lower() != email.lower():
        raise ValueError("Email does not match invitation")
    
    # Check if user already exists
    existing_user = get_user_by_email(db, email)
    if existing_user:
        raise ValueError("User with this email already exists")
    
    # Hash password
    hashed_password = hash_password(password)
    
    # Get "Active" status (skip pending verification)
    active_status = db.execute(
        select(UserStatus).where(UserStatus.StatusName == "Active")
    ).scalar_one_or_none()
    
    if not active_status:
        raise ValueError("Active status not found in database")
    
    # Create user (immediately activated for invited users)
    user = User(
        Email=email,
        PasswordHash=hashed_password,
        FirstName=first_name,
        LastName=last_name,
        EmailVerified=True,  # Auto-verify invited users
        IsActive=True,  # Immediately active
        UserStatusID=active_status.UserStatusID,
        OnboardingComplete=True,  # Skip onboarding (joining existing company)
        OnboardingStep=3,  # Mark as complete
        CreatedDate=datetime.utcnow(),
        UpdatedDate=datetime.utcnow(),
        IsDeleted=False
    )
    db.add(user)
    db.flush()  # Get user ID
    
    # Get accepted invitation status
    accepted_status = db.execute(
        select(UserInvitationStatus).where(UserInvitationStatus.StatusCode == "accepted")
    ).scalar_one_or_none()
    
    if not accepted_status:
        raise ValueError("Accepted status not found in database")
    
    # Get active status for UserCompany
    uc_active_status = db.execute(
        select(UserCompanyStatus).where(UserCompanyStatus.StatusCode == "active")
    ).scalar_one_or_none()
    
    if not uc_active_status:
        raise ValueError("Active status not found in database")
    
    # Get invitation joined_via
    invitation_via = db.execute(
        select(JoinedVia).where(JoinedVia.MethodCode == "invitation")
    ).scalar_one_or_none()
    
    if not invitation_via:
        raise ValueError("Invitation joined_via not found in database")
    
    # Create UserCompany relationship (AC-1.7.6)
    user_company = UserCompany(
        UserID=user.UserID,  # type: ignore
        CompanyID=invitation.CompanyID,
        UserCompanyRoleID=invitation.UserCompanyRoleID,
        StatusID=uc_active_status.UserCompanyStatusID,
        IsPrimaryCompany=True,  # First company is primary
        JoinedDate=datetime.utcnow(),
        JoinedViaID=invitation_via.JoinedViaID,
        InvitedBy=invitation.InvitedBy,
        InvitedDate=invitation.InvitedAt,
        CreatedBy=user.UserID,  # type: ignore
        CreatedDate=datetime.utcnow(),
        UpdatedBy=user.UserID,  # type: ignore
        UpdatedDate=datetime.utcnow(),
        IsDeleted=False
    )
    db.add(user_company)
    
    # Mark invitation as accepted (AC-1.7.7)
    invitation.StatusID = accepted_status.UserInvitationStatusID  # type: ignore
    invitation.AcceptedAt = datetime.utcnow()  # type: ignore
    invitation.AcceptedBy = user.UserID  # type: ignore
    invitation.UpdatedDate = datetime.utcnow()  # type: ignore
    invitation.UpdatedBy = user.UserID  # type: ignore
    
    db.flush()  # Get IDs
    
    # Log to audit table (AC-1.7.10)
    audit_log = ActivityLog(
        UserID=user.UserID,  # type: ignore
        CompanyID=invitation.CompanyID,
        Action="USER_SIGNUP_WITH_INVITATION",
        EntityType="User",
        EntityID=user.UserID,  # type: ignore
        NewValue=json.dumps({
            "user_id": int(user.UserID),  # type: ignore
            "invitation_id": int(invitation.UserInvitationID),  # type: ignore
            "user_company_id": int(user_company.UserCompanyID),  # type: ignore
            "created_at": datetime.utcnow().isoformat()
        }),
        CreatedDate=datetime.utcnow()
    )
    db.add(audit_log)
    
    db.commit()
    db.refresh(user)
    db.refresh(invitation)
    db.refresh(user_company)
    
    logger.info(
        f"User created with invitation: UserID={user.UserID}, "
        f"InvitationID={invitation.UserInvitationID}, "
        f"CompanyID={invitation.CompanyID}"
    )
    
    return user, invitation, user_company

