"""
UserInvitation Model (dbo.UserInvitation)
Team member invitations for companies
"""
from sqlalchemy import Column, BigInteger, String, Integer, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from backend.common.database import Base


class UserInvitation(Base):
    """
    User invitation model for team member invitations.
    
    Workflow:
    1. Team admin sends invitation with email, name, and role
    2. Invitation email sent with secure token
    3. Recipient clicks link and creates account (or logs in if existing user)
    4. Upon acceptance, UserCompany record created
    5. Invitations can be resent, declined, cancelled, or expire
    
    Attributes:
        UserInvitationID: Primary key
        CompanyID: Foreign key to dbo.Company
        InvitedBy: Foreign key to dbo.User who sent invitation
        Email: Email address of invitee
        FirstName: First name of invitee
        LastName: Last name of invitee
        UserCompanyRoleID: Foreign key to ref.UserCompanyRole (role to be assigned)
        InvitationToken: Secure token for invitation link
        StatusID: Foreign key to ref.UserInvitationStatus
        InvitedAt: Timestamp when invitation was sent
        ExpiresAt: Timestamp when invitation expires (typically 7-14 days)
        AcceptedAt: Timestamp when invitation was accepted
        AcceptedBy: Foreign key to dbo.User who accepted invitation
        CancelledAt: Timestamp when invitation was cancelled
        CancelledBy: Foreign key to dbo.User who cancelled invitation
        CancellationReason: Reason for cancellation
        DeclinedAt: Timestamp when invitation was declined
        DeclineReason: Reason for declining
        ResendCount: Number of times invitation has been resent
        LastResentAt: Timestamp when invitation was last resent
    """
    
    __tablename__ = "UserInvitation"
    __table_args__ = {"schema": "dbo"}
    
    # Primary Key
    UserInvitationID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    CompanyID = Column(BigInteger, ForeignKey('dbo.Company.CompanyID'), nullable=False, index=True)
    InvitedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=False)
    UserCompanyRoleID = Column(BigInteger, ForeignKey('ref.UserCompanyRole.UserCompanyRoleID'), nullable=False)
    StatusID = Column(BigInteger, ForeignKey('ref.UserInvitationStatus.UserInvitationStatusID'), nullable=False, index=True)
    
    # Invitee Information
    Email = Column(String(255), nullable=False, index=True)
    FirstName = Column(String(100), nullable=False)
    LastName = Column(String(100), nullable=False)
    
    # Invitation Token
    InvitationToken = Column(String(500), nullable=False, unique=True)
    
    # Invitation Lifecycle
    InvitedAt = Column(DateTime, nullable=False, server_default=func.getutcdate())
    ExpiresAt = Column(DateTime, nullable=False, index=True)
    
    # Acceptance
    AcceptedAt = Column(DateTime, nullable=True)
    AcceptedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    
    # Cancellation
    CancelledAt = Column(DateTime, nullable=True)
    CancelledBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    CancellationReason = Column(String(500), nullable=True)
    
    # Decline
    DeclinedAt = Column(DateTime, nullable=True)
    DeclineReason = Column(String(500), nullable=True)
    
    # Resend Tracking
    ResendCount = Column(Integer, nullable=False, default=0)
    LastResentAt = Column(DateTime, nullable=True)
    
    # Audit Columns
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    UpdatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate(), onupdate=func.getutcdate())
    UpdatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    
    # Relationships
    company = relationship("Company", back_populates="invitations")
    invited_by_user = relationship("User", back_populates="invitations_sent", foreign_keys=[InvitedBy])
    role = relationship("UserCompanyRole", back_populates="invitations", foreign_keys=[UserCompanyRoleID])
    status = relationship("UserInvitationStatus", back_populates="invitations", foreign_keys=[StatusID])
    accepted_by_user = relationship("User", foreign_keys=[AcceptedBy])
    cancelled_by_user = relationship("User", foreign_keys=[CancelledBy])
    
    def __repr__(self) -> str:
        return f"<UserInvitation(UserInvitationID={self.UserInvitationID}, Email='{self.Email}', CompanyID={self.CompanyID})>"

