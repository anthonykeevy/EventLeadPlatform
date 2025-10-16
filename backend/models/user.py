"""
User Model (dbo.User)
Core user entity with authentication and profile information
"""
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from backend.common.database import Base


class User(Base):
    """
    User model representing platform users with authentication and profile data.
    
    Features:
    - Email/password authentication with bcrypt hashing
    - Email verification workflow
    - Account locking after failed login attempts
    - Session and token version management
    - Multi-company support via UserCompany relationships
    - Timezone and localization preferences
    
    Attributes:
        UserID: Primary key
        Email: Unique email address (used for login)
        PasswordHash: Bcrypt hashed password ($2b$12$...)
        FirstName: User's first name
        LastName: User's last name
        Phone: Contact phone number
        RoleTitle: User's job title/role
        ProfilePictureUrl: URL to profile picture
        TimezoneIdentifier: IANA timezone (e.g., 'Australia/Sydney')
        StatusID: Foreign key to ref.UserStatus (Active, Pending, Locked, Inactive)
        IsEmailVerified: Whether email has been verified
        EmailVerifiedAt: Timestamp when email was verified
        IsLocked: Whether account is locked (failed logins, admin action)
        LockedUntil: Timestamp when lock expires (null = permanent)
        LockedReason: Reason for account lock
        FailedLoginAttempts: Counter for failed login attempts
        LastLoginDate: Timestamp of last successful login
        LastPasswordChange: Timestamp of last password change
        SessionToken: Current session token (nullable)
        AccessTokenVersion: Token version for JWT invalidation
        RefreshTokenVersion: Refresh token version for JWT invalidation
        OnboardingComplete: Whether user has completed onboarding
        OnboardingStep: Current onboarding step (1-5)
        CountryID: Foreign key to ref.Country
        PreferredLanguageID: Foreign key to ref.Language
        UserRoleID: Foreign key to ref.UserRole (system-level role)
    """
    
    __tablename__ = "User"
    __table_args__ = {"schema": "dbo"}
    
    # Primary Key
    UserID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Authentication
    Email = Column(String(255), nullable=False, unique=True, index=True)
    PasswordHash = Column(String(500), nullable=False)
    
    # Profile
    FirstName = Column(String(100), nullable=False)
    LastName = Column(String(100), nullable=False)
    Phone = Column(String(20), nullable=True)
    RoleTitle = Column(String(100), nullable=True)
    ProfilePictureUrl = Column(String(500), nullable=True)
    TimezoneIdentifier = Column(String(50), nullable=False, default='Australia/Sydney', index=True)
    
    # Status and Verification
    StatusID = Column(BigInteger, ForeignKey('ref.UserStatus.UserStatusID'), nullable=False, index=True)
    IsEmailVerified = Column(Boolean, nullable=False, default=False)
    EmailVerifiedAt = Column(DateTime, nullable=True)
    
    # Account Locking
    IsLocked = Column(Boolean, nullable=False, default=False)
    LockedUntil = Column(DateTime, nullable=True)
    LockedReason = Column(String(500), nullable=True)
    FailedLoginAttempts = Column(Integer, nullable=False, default=0)
    
    # Session Management
    LastLoginDate = Column(DateTime, nullable=True)
    LastPasswordChange = Column(DateTime, nullable=True)
    SessionToken = Column(String(255), nullable=True, index=True)
    AccessTokenVersion = Column(Integer, nullable=False, default=1)
    RefreshTokenVersion = Column(Integer, nullable=False, default=1)
    
    # Onboarding
    OnboardingComplete = Column(Boolean, nullable=False, default=False)
    OnboardingStep = Column(Integer, nullable=False, default=1)
    
    # Foreign Keys
    CountryID = Column(BigInteger, ForeignKey('ref.Country.CountryID'), nullable=True, index=True)
    PreferredLanguageID = Column(BigInteger, ForeignKey('ref.Language.LanguageID'), nullable=True)
    UserRoleID = Column(BigInteger, ForeignKey('ref.UserRole.UserRoleID'), nullable=True, index=True)
    
    # Audit Columns
    CreatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate())
    CreatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    UpdatedDate = Column(DateTime, nullable=False, server_default=func.getutcdate(), onupdate=func.getutcdate())
    UpdatedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)
    DeletedDate = Column(DateTime, nullable=True)
    DeletedBy = Column(BigInteger, ForeignKey('dbo.User.UserID'), nullable=True)
    
    # Relationships
    status = relationship("UserStatus", back_populates="users", foreign_keys=[StatusID])
    country = relationship("Country", back_populates="users", foreign_keys=[CountryID])
    preferred_language = relationship("Language", back_populates="users", foreign_keys=[PreferredLanguageID])
    user_role = relationship("UserRole", back_populates="users", foreign_keys=[UserRoleID])
    
    companies = relationship("UserCompany", back_populates="user")
    invitations_sent = relationship("UserInvitation", back_populates="invited_by_user", foreign_keys="[UserInvitation.InvitedBy]")
    verification_tokens = relationship("UserEmailVerificationToken", back_populates="user")
    password_reset_tokens = relationship("UserPasswordResetToken", back_populates="user")
    
    activity_logs = relationship("ActivityLog", back_populates="user", foreign_keys="[ActivityLog.UserID]")
    auth_events = relationship("AuthEvent", back_populates="user")
    api_requests = relationship("ApiRequest", back_populates="user")
    application_errors = relationship("ApplicationError", back_populates="user")
    email_deliveries = relationship("EmailDelivery", back_populates="user")
    
    def __repr__(self) -> str:
        return f"<User(UserID={self.UserID}, Email='{self.Email}', FirstName='{self.FirstName}', LastName='{self.LastName}')>"
