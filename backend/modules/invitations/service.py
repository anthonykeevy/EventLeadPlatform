"""
Invitation Acceptance Service
Business logic for viewing and accepting team invitations
"""
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from typing import Optional, Tuple
from datetime import datetime
import json

from models.user_invitation import UserInvitation
from models.user import User
from models.user_company import UserCompany
from models.company import Company
from models.ref.user_company_role import UserCompanyRole
from models.ref.user_company_status import UserCompanyStatus
from models.ref.user_invitation_status import UserInvitationStatus
from models.ref.joined_via import JoinedVia
from models.audit.activity_log import ActivityLog
from common.logger import get_logger

logger = get_logger(__name__)


async def get_invitation_by_token(db: Session, token: str) -> Optional[UserInvitation]:
    """
    Get invitation by token.
    
    Args:
        db: Database session
        token: Invitation token
        
    Returns:
        UserInvitation if found, None otherwise
    """
    invitation = db.execute(
        select(UserInvitation).where(
            and_(
                UserInvitation.InvitationToken == token,
                UserInvitation.IsDeleted == False
            )
        )
    ).scalar_one_or_none()
    
    return invitation


async def get_invitation_details(
    db: Session,
    token: str
) -> Optional[Tuple[UserInvitation, Company, User, UserCompanyRole, UserInvitationStatus]]:
    """
    Get invitation details for display (AC-1.7.1, AC-1.7.2).
    
    Args:
        db: Database session
        token: Invitation token
        
    Returns:
        Tuple of (invitation, company, inviter, role, status) or None if not found
    """
    invitation = await get_invitation_by_token(db, token)
    
    if not invitation:
        return None
    
    # Get related entities
    company = db.execute(
        select(Company).where(Company.CompanyID == invitation.CompanyID)
    ).scalar_one()
    
    inviter = db.execute(
        select(User).where(User.UserID == invitation.InvitedBy)
    ).scalar_one()
    
    role = db.execute(
        select(UserCompanyRole).where(
            UserCompanyRole.UserCompanyRoleID == invitation.UserCompanyRoleID
        )
    ).scalar_one()
    
    status = db.execute(
        select(UserInvitationStatus).where(
            UserInvitationStatus.UserInvitationStatusID == invitation.StatusID
        )
    ).scalar_one()
    
    return invitation, company, inviter, role, status


async def accept_invitation(
    db: Session,
    token: str,
    user_id: int,
    user_email: str
) -> Tuple[UserInvitation, UserCompany]:
    """
    Accept team invitation for existing user (AC-1.7.3, AC-1.7.4, AC-1.7.7).
    
    Args:
        db: Database session
        token: Invitation token
        user_id: User ID accepting invitation
        user_email: User's email address
        
    Returns:
        Tuple of (invitation, user_company)
        
    Raises:
        ValueError: If validation fails
    """
    invitation = await get_invitation_by_token(db, token)
    
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
    
    # Verify email matches (security check)
    if invitation.Email.lower() != user_email.lower():
        raise ValueError("Invitation email does not match your account email")
    
    # Check if user already belongs to this company
    existing = db.execute(
        select(UserCompany)
        .join(UserCompanyStatus)
        .where(
            and_(
                UserCompany.UserID == user_id,
                UserCompany.CompanyID == invitation.CompanyID,
                UserCompany.IsDeleted == False,
                UserCompanyStatus.StatusCode == "active"
            )
        )
    ).scalar_one_or_none()
    
    if existing:
        raise ValueError("You are already a member of this company")
    
    # Get accepted status
    accepted_status = db.execute(
        select(UserInvitationStatus).where(UserInvitationStatus.StatusCode == "accepted")
    ).scalar_one_or_none()
    
    if not accepted_status:
        raise ValueError("Accepted status not found in database")
    
    # Get active status for UserCompany
    active_status = db.execute(
        select(UserCompanyStatus).where(UserCompanyStatus.StatusCode == "active")
    ).scalar_one_or_none()
    
    if not active_status:
        raise ValueError("Active status not found in database")
    
    # Get invitation joined_via
    invitation_via = db.execute(
        select(JoinedVia).where(JoinedVia.MethodCode == "invitation")
    ).scalar_one_or_none()
    
    if not invitation_via:
        raise ValueError("Invitation joined_via not found in database")
    
    # Create UserCompany relationship (AC-1.7.4, AC-1.7.9)
    user_company = UserCompany(
        UserID=user_id,
        CompanyID=invitation.CompanyID,
        UserCompanyRoleID=invitation.UserCompanyRoleID,
        StatusID=active_status.UserCompanyStatusID,
        IsPrimaryCompany=False,  # Not primary unless it's their first company
        JoinedDate=datetime.utcnow(),
        JoinedViaID=invitation_via.JoinedViaID,
        InvitedBy=invitation.InvitedBy,
        InvitedDate=invitation.InvitedAt,
        CreatedBy=user_id,
        CreatedDate=datetime.utcnow(),
        UpdatedBy=user_id,
        UpdatedDate=datetime.utcnow(),
        IsDeleted=False
    )
    db.add(user_company)
    
    # Mark invitation as accepted (AC-1.7.7)
    invitation.StatusID = accepted_status.UserInvitationStatusID  # type: ignore
    invitation.AcceptedAt = datetime.utcnow()  # type: ignore
    invitation.AcceptedBy = user_id  # type: ignore
    invitation.UpdatedDate = datetime.utcnow()  # type: ignore
    invitation.UpdatedBy = user_id  # type: ignore
    
    db.flush()  # Get IDs
    
    # Log to audit table (AC-1.7.10)
    audit_log = ActivityLog(
        UserID=user_id,
        CompanyID=invitation.CompanyID,
        Action="INVITATION_ACCEPTED",
        EntityType="UserInvitation",
        EntityID=invitation.UserInvitationID,
        NewValue=json.dumps({
            "invitation_id": int(invitation.UserInvitationID),  # type: ignore
            "user_company_id": int(user_company.UserCompanyID),  # type: ignore
            "role_id": int(invitation.UserCompanyRoleID),  # type: ignore
            "accepted_at": datetime.utcnow().isoformat()
        }),
        CreatedDate=datetime.utcnow()
    )
    db.add(audit_log)
    
    db.commit()
    db.refresh(invitation)
    db.refresh(user_company)
    
    logger.info(
        f"Invitation accepted: InvitationID={invitation.UserInvitationID}, "
        f"UserID={user_id}, CompanyID={invitation.CompanyID}, "
        f"UserCompanyID={user_company.UserCompanyID}"
    )
    
    return invitation, user_company


