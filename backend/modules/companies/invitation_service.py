"""
Team Invitation Service
Business logic for team member invitations
"""
import secrets
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, func
from typing import Optional, List, Tuple
from datetime import datetime, timedelta

from models.user_invitation import UserInvitation
from models.user import User
from models.user_company import UserCompany
from models.company import Company
from models.ref.user_invitation_status import UserInvitationStatus
from models.ref.user_company_role import UserCompanyRole
from models.ref.user_company_status import UserCompanyStatus
from models.audit.activity_log import ActivityLog
from common.logger import get_logger
import json

logger = get_logger(__name__)


INVITATION_EXPIRY_DAYS = 7
ALLOWED_INVITATION_ROLES = ["company_admin", "company_user"]


def generate_invitation_token() -> str:
    """
    Generate a cryptographically secure invitation token.
    
    Returns:
        URL-safe token string (64 characters)
    """
    return secrets.token_urlsafe(48)  # 64 characters when base64 encoded


async def check_email_in_company(db: Session, company_id: int, email: str) -> bool:
    """
    Check if email already belongs to the company.
    
    Args:
        db: Database session
        company_id: Company ID
        email: Email to check
        
    Returns:
        True if email is already a company member, False otherwise
    """
    # Check if user exists with this email
    user = db.execute(
        select(User).where(User.Email == email)
    ).scalar_one_or_none()
    
    if not user:
        return False  # Email doesn't have an account
    
    # Check if user is already in the company
    user_company = db.execute(
        select(UserCompany)
        .join(UserCompanyStatus)
        .where(
            and_(
                UserCompany.UserID == user.UserID,
                UserCompany.CompanyID == company_id,
                UserCompany.IsDeleted == False,
                UserCompanyStatus.StatusCode == "active"
            )
        )
    ).scalar_one_or_none()
    
    return user_company is not None


async def check_pending_invitation(db: Session, company_id: int, email: str) -> Optional[UserInvitation]:
    """
    Check if there's already a pending invitation for this email.
    
    Args:
        db: Database session
        company_id: Company ID
        email: Email to check
        
    Returns:
        Pending UserInvitation if exists, None otherwise
    """
    invitation = db.execute(
        select(UserInvitation)
        .join(UserInvitationStatus)
        .where(
            and_(
                UserInvitation.CompanyID == company_id,
                UserInvitation.Email == email,
                UserInvitation.IsDeleted == False,
                UserInvitationStatus.StatusCode == "pending",
                UserInvitation.ExpiresAt > datetime.utcnow()
            )
        )
    ).scalar_one_or_none()
    
    return invitation


async def send_invitation(
    db: Session,
    company_id: int,
    invited_by_user_id: int,
    email: str,
    first_name: str,
    last_name: str,
    role_code: str
) -> UserInvitation:
    """
    Send team invitation to new member.
    
    Args:
        db: Database session
        company_id: Company ID
        invited_by_user_id: User ID of admin sending invitation
        email: Email address of invitee
        first_name: First name of invitee
        last_name: Last name of invitee
        role_code: Role code (company_admin or company_user)
        
    Returns:
        Created UserInvitation
        
    Raises:
        ValueError: If validation fails
    """
    # Validate role
    if role_code not in ALLOWED_INVITATION_ROLES:
        raise ValueError(f"Invalid role. Must be one of: {', '.join(ALLOWED_INVITATION_ROLES)}")
    
    # Check if email already in company (AC-1.6.5)
    if await check_email_in_company(db, company_id, email):
        raise ValueError("This email already belongs to the company")
    
    # Check for pending invitation
    existing = await check_pending_invitation(db, company_id, email)
    if existing:
        raise ValueError("There is already a pending invitation for this email")
    
    # Get role
    role = db.execute(
        select(UserCompanyRole).where(UserCompanyRole.RoleCode == role_code)
    ).scalar_one_or_none()
    
    if not role:
        raise ValueError(f"Role not found: {role_code}")
    
    # Get pending status
    pending_status = db.execute(
        select(UserInvitationStatus).where(UserInvitationStatus.StatusCode == "pending")
    ).scalar_one_or_none()
    
    if not pending_status:
        raise ValueError("Pending status not found in database")
    
    # Generate invitation token (AC-1.6.3)
    token = generate_invitation_token()
    expires_at = datetime.utcnow() + timedelta(days=INVITATION_EXPIRY_DAYS)
    
    # Create invitation (AC-1.6.2)
    invitation = UserInvitation(
        CompanyID=company_id,
        InvitedBy=invited_by_user_id,
        Email=email,
        FirstName=first_name,
        LastName=last_name,
        UserCompanyRoleID=role.UserCompanyRoleID,
        StatusID=pending_status.UserInvitationStatusID,
        InvitationToken=token,
        InvitedAt=datetime.utcnow(),
        ExpiresAt=expires_at,
        ResendCount=0,
        CreatedBy=invited_by_user_id,
        CreatedDate=datetime.utcnow(),
        UpdatedBy=invited_by_user_id,
        UpdatedDate=datetime.utcnow(),
        IsDeleted=False
    )
    
    db.add(invitation)
    db.flush()  # Get invitation ID before commit
    
    # Log to audit table (AC-1.6.10)
    audit_log = ActivityLog(
        UserID=invited_by_user_id,
        CompanyID=company_id,
        Action="INVITATION_SENT",
        EntityType="UserInvitation",
        EntityID=invitation.UserInvitationID,
        NewValue=json.dumps({
            "invitation_id": int(invitation.UserInvitationID),  # type: ignore
            "email": email,
            "role": role_code,
            "expires_at": expires_at.isoformat()
        }),
        CreatedDate=datetime.utcnow()
    )
    db.add(audit_log)
    
    db.commit()
    db.refresh(invitation)
    
    logger.info(
        f"Invitation sent: UserInvitationID={invitation.UserInvitationID}, "
        f"Email={email}, CompanyID={company_id}, Role={role_code}, "
        f"InvitedBy={invited_by_user_id}, ExpiresAt={expires_at}"
    )
    
    return invitation


async def resend_invitation(
    db: Session,
    invitation_id: int,
    company_id: int,
    resent_by_user_id: int
) -> UserInvitation:
    """
    Resend invitation and extend expiry date (AC-1.6.7).
    
    Args:
        db: Database session
        invitation_id: Invitation ID to resend
        company_id: Company ID (for verification)
        resent_by_user_id: User ID of admin resending
        
    Returns:
        Updated UserInvitation
        
    Raises:
        ValueError: If invitation cannot be resent
    """
    # Get invitation
    invitation = db.execute(
        select(UserInvitation)
        .join(UserInvitationStatus)
        .where(
            and_(
                UserInvitation.UserInvitationID == invitation_id,
                UserInvitation.CompanyID == company_id,
                UserInvitation.IsDeleted == False
            )
        )
    ).scalar_one_or_none()
    
    if not invitation:
        raise ValueError("Invitation not found")
    
    # Get status
    status = db.execute(
        select(UserInvitationStatus).where(
            UserInvitationStatus.UserInvitationStatusID == invitation.StatusID
        )
    ).scalar_one()
    
    # Check if can resend
    if not status.CanResend:
        raise ValueError(f"Cannot resend invitation with status: {status.StatusName}")
    
    # Extend expiry date
    new_expires_at = datetime.utcnow() + timedelta(days=INVITATION_EXPIRY_DAYS)
    
    invitation.ExpiresAt = new_expires_at  # type: ignore
    invitation.ResendCount = (invitation.ResendCount or 0) + 1  # type: ignore
    invitation.LastResentAt = datetime.utcnow()  # type: ignore
    invitation.UpdatedDate = datetime.utcnow()  # type: ignore
    invitation.UpdatedBy = resent_by_user_id  # type: ignore
    
    # Log to audit table (AC-1.6.10)
    audit_log = ActivityLog(
        UserID=resent_by_user_id,
        CompanyID=company_id,
        Action="INVITATION_RESENT",
        EntityType="UserInvitation",
        EntityID=invitation_id,
        NewValue=json.dumps({
            "invitation_id": invitation_id,
            "new_expires_at": new_expires_at.isoformat(),
            "resend_count": invitation.ResendCount
        }),
        CreatedDate=datetime.utcnow()
    )
    db.add(audit_log)
    
    db.commit()
    db.refresh(invitation)
    
    logger.info(
        f"Invitation resent: UserInvitationID={invitation_id}, "
        f"NewExpiresAt={new_expires_at}, ResendCount={invitation.ResendCount}"
    )
    
    return invitation


async def cancel_invitation(
    db: Session,
    invitation_id: int,
    company_id: int,
    cancelled_by_user_id: int,
    reason: Optional[str] = None
) -> UserInvitation:
    """
    Cancel pending invitation (AC-1.6.8).
    
    Args:
        db: Database session
        invitation_id: Invitation ID to cancel
        company_id: Company ID (for verification)
        cancelled_by_user_id: User ID of admin cancelling
        reason: Optional cancellation reason
        
    Returns:
        Updated UserInvitation
        
    Raises:
        ValueError: If invitation cannot be cancelled
    """
    # Get invitation
    invitation = db.execute(
        select(UserInvitation)
        .join(UserInvitationStatus)
        .where(
            and_(
                UserInvitation.UserInvitationID == invitation_id,
                UserInvitation.CompanyID == company_id,
                UserInvitation.IsDeleted == False
            )
        )
    ).scalar_one_or_none()
    
    if not invitation:
        raise ValueError("Invitation not found")
    
    # Get current status
    current_status = db.execute(
        select(UserInvitationStatus).where(
            UserInvitationStatus.UserInvitationStatusID == invitation.StatusID
        )
    ).scalar_one()
    
    # Check if can cancel
    if not current_status.CanCancel:
        raise ValueError(f"Cannot cancel invitation with status: {current_status.StatusName}")
    
    # Get cancelled status
    cancelled_status = db.execute(
        select(UserInvitationStatus).where(UserInvitationStatus.StatusCode == "cancelled")
    ).scalar_one_or_none()
    
    if not cancelled_status:
        raise ValueError("Cancelled status not found in database")
    
    # Update invitation
    invitation.StatusID = cancelled_status.UserInvitationStatusID  # type: ignore
    invitation.CancelledAt = datetime.utcnow()  # type: ignore
    invitation.CancelledBy = cancelled_by_user_id  # type: ignore
    invitation.CancellationReason = reason  # type: ignore
    invitation.UpdatedDate = datetime.utcnow()  # type: ignore
    invitation.UpdatedBy = cancelled_by_user_id  # type: ignore
    
    # Log to audit table (AC-1.6.10)
    audit_log = ActivityLog(
        UserID=cancelled_by_user_id,
        CompanyID=company_id,
        Action="INVITATION_CANCELLED",
        EntityType="UserInvitation",
        EntityID=invitation_id,
        OldValue=json.dumps({
            "status": current_status.StatusCode
        }),
        NewValue=json.dumps({
            "status": "cancelled",
            "reason": reason
        }),
        CreatedDate=datetime.utcnow()
    )
    db.add(audit_log)
    
    db.commit()
    db.refresh(invitation)
    
    logger.info(
        f"Invitation cancelled: UserInvitationID={invitation_id}, "
        f"CancelledBy={cancelled_by_user_id}, Reason={reason}"
    )
    
    return invitation


async def list_company_invitations(
    db: Session,
    company_id: int,
    status_filter: Optional[str] = None,
    page: int = 1,
    page_size: int = 20
) -> Tuple[List[UserInvitation], int]:
    """
    List all invitations for a company (AC-1.6.9).
    
    Args:
        db: Database session
        company_id: Company ID
        status_filter: Optional status code filter
        page: Page number (1-indexed)
        page_size: Number of items per page
        
    Returns:
        Tuple of (invitations list, total count)
    """
    # Base query
    query = select(UserInvitation).where(
        and_(
            UserInvitation.CompanyID == company_id,
            UserInvitation.IsDeleted == False
        )
    )
    
    # Apply status filter if provided
    if status_filter:
        query = query.join(UserInvitationStatus).where(
            UserInvitationStatus.StatusCode == status_filter
        )
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = db.execute(count_query).scalar()
    
    # Apply pagination and ordering
    query = query.order_by(UserInvitation.InvitedAt.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    # Execute query
    invitations = db.execute(query).scalars().all()
    
    return list(invitations), total or 0


async def get_invitation_details(
    db: Session,
    invitation_id: int,
    company_id: int
) -> Optional[UserInvitation]:
    """
    Get invitation details.
    
    Args:
        db: Database session
        invitation_id: Invitation ID
        company_id: Company ID (for verification)
        
    Returns:
        UserInvitation if found, None otherwise
    """
    invitation = db.execute(
        select(UserInvitation).where(
            and_(
                UserInvitation.UserInvitationID == invitation_id,
                UserInvitation.CompanyID == company_id,
                UserInvitation.IsDeleted == False
            )
        )
    ).scalar_one_or_none()
    
    return invitation

