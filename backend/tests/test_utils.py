"""
Multi-Tenant Testing Utilities
Helpers for creating test data and scenarios for multi-tenant tests
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import Optional
import secrets

from models.user import User
from models.company import Company
from models.user_company import UserCompany
from models.user_invitation import UserInvitation
from models.ref.user_status import UserStatus
from models.ref.user_company_status import UserCompanyStatus
from models.ref.user_company_role import UserCompanyRole
from models.ref.user_invitation_status import UserInvitationStatus
from models.ref.joined_via import JoinedVia
from common.security import hash_password
from modules.auth.jwt_service import create_access_token


def create_test_company(
    db: Session,
    company_name: str,
    abn: str = "53004085616",
    trading_name: Optional[str] = None
) -> Company:
    """
    Create a test company.
    
    Args:
        db: Database session
        company_name: Company name
        abn: Australian Business Number (valid by default)
        trading_name: Optional trading name
        
    Returns:
        Created Company object
    """
    company = Company(
        CompanyName=company_name,
        CompanyTradingName=trading_name or company_name,
        ABN=abn,
        IsActive=True,
        CreatedDate=datetime.utcnow(),
        UpdatedDate=datetime.utcnow(),
        IsDeleted=False
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def create_test_user(
    db: Session,
    email: str,
    company_id: Optional[int] = None,
    role_code: str = "company_user",
    first_name: str = "Test",
    last_name: str = "User",
    password: str = "TestP@ssw0rd123",
    is_active: bool = True,
    email_verified: bool = True,
    onboarding_complete: bool = False,
    is_primary_company: bool = True
) -> User:
    """
    Create a test user with optional company relationship.
    
    Args:
        db: Database session
        email: User email
        company_id: Optional company ID to associate user with
        role_code: Role code (company_admin, company_user)
        first_name: User first name
        last_name: User last name
        password: User password
        is_active: Whether user is active
        email_verified: Whether email is verified
        onboarding_complete: Whether onboarding is complete
        is_primary_company: Whether this is user's primary company
        
    Returns:
        Created User object
    """
    # Get active status
    active_status = db.query(UserStatus).filter(
        UserStatus.StatusName == "Active" if is_active else "Inactive"
    ).first()
    
    # Create user
    user = User(
        Email=email,
        PasswordHash=hash_password(password),
        FirstName=first_name,
        LastName=last_name,
        EmailVerified=email_verified,
        IsActive=is_active,
        UserStatusID=active_status.UserStatusID if active_status else None,
        OnboardingComplete=onboarding_complete,
        OnboardingStep=3 if onboarding_complete else 1,
        CreatedDate=datetime.utcnow(),
        UpdatedDate=datetime.utcnow(),
        IsDeleted=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create UserCompany relationship if company_id provided
    if company_id:
        # Get role
        role = db.query(UserCompanyRole).filter(
            UserCompanyRole.RoleCode == role_code
        ).first()
        
        # Get active status
        uc_active_status = db.query(UserCompanyStatus).filter(
            UserCompanyStatus.StatusCode == "active"
        ).first()
        
        # Get joined_via
        joined_via = db.query(JoinedVia).filter(
            JoinedVia.MethodCode == "signup"
        ).first()
        
        # Create UserCompany
        user_company = UserCompany(
            UserID=user.UserID,
            CompanyID=company_id,
            UserCompanyRoleID=role.UserCompanyRoleID if role else None,
            StatusID=uc_active_status.UserCompanyStatusID if uc_active_status else None,
            IsPrimaryCompany=is_primary_company,
            JoinedDate=datetime.utcnow(),
            JoinedViaID=joined_via.JoinedViaID if joined_via else None,
            CreatedBy=user.UserID,
            CreatedDate=datetime.utcnow(),
            UpdatedBy=user.UserID,
            UpdatedDate=datetime.utcnow(),
            IsDeleted=False
        )
        db.add(user_company)
        db.commit()
    
    return user


def create_test_token(
    user_id: int,
    email: str,
    role: Optional[str] = None,
    company_id: Optional[int] = None
) -> str:
    """
    Create a test JWT token for a user.
    
    Args:
        user_id: User ID
        email: User email
        role: Optional role code
        company_id: Optional company ID
        
    Returns:
        JWT access token string
    """
    return create_access_token(
        user_id=user_id,
        email=email,
        role=role,
        company_id=company_id
    )


def create_test_invitation(
    db: Session,
    company_id: int,
    invited_by: int,
    email: str,
    role_code: str = "company_user",
    expires_in_days: int = 7,
    status_code: str = "pending"
) -> UserInvitation:
    """
    Create a test invitation.
    
    Args:
        db: Database session
        company_id: Company ID
        invited_by: User ID of inviter
        email: Email address to invite
        role_code: Role code for invitation
        expires_in_days: Days until invitation expires
        status_code: Invitation status
        
    Returns:
        Created UserInvitation object
    """
    # Get role
    role = db.query(UserCompanyRole).filter(
        UserCompanyRole.RoleCode == role_code
    ).first()
    
    # Get status
    inv_status = db.query(UserInvitationStatus).filter(
        UserInvitationStatus.StatusCode == status_code
    ).first()
    
    # Generate token
    invitation_token = secrets.token_urlsafe(32)
    
    invitation = UserInvitation(
        CompanyID=company_id,
        Email=email,
        UserCompanyRoleID=role.UserCompanyRoleID if role else None,
        InvitedBy=invited_by,
        InvitedAt=datetime.utcnow(),
        ExpiresAt=datetime.utcnow() + timedelta(days=expires_in_days),
        InvitationToken=invitation_token,
        StatusID=inv_status.UserInvitationStatusID if inv_status else None,
        CreatedDate=datetime.utcnow(),
        CreatedBy=invited_by,
        UpdatedDate=datetime.utcnow(),
        UpdatedBy=invited_by,
        IsDeleted=False
    )
    db.add(invitation)
    db.commit()
    db.refresh(invitation)
    return invitation


class MultiTenantTestScenario:
    """
    Helper class for creating multi-tenant test scenarios.
    
    Creates two companies with different users and data,
    making it easy to test data isolation.
    """
    
    def __init__(self, db: Session):
        self.db = db
        
        # Company A
        self.company_a = create_test_company(db, "Company A Pty Ltd", "53004085616")
        self.admin_a = create_test_user(
            db,
            "admin_a@company-a.com",
            self.company_a.CompanyID,
            role_code="company_admin",
            first_name="Admin",
            last_name="A",
            onboarding_complete=True
        )
        self.user_a = create_test_user(
            db,
            "user_a@company-a.com",
            self.company_a.CompanyID,
            role_code="company_user",
            first_name="User",
            last_name="A",
            onboarding_complete=True
        )
        self.token_admin_a = create_test_token(
            int(self.admin_a.UserID),  # type: ignore
            str(self.admin_a.Email),  # type: ignore
            "company_admin",
            int(self.company_a.CompanyID)  # type: ignore
        )
        self.token_user_a = create_test_token(
            int(self.user_a.UserID),  # type: ignore
            str(self.user_a.Email),  # type: ignore
            "company_user",
            int(self.company_a.CompanyID)  # type: ignore
        )
        
        # Company B
        self.company_b = create_test_company(db, "Company B Pty Ltd", "51824753556")
        self.admin_b = create_test_user(
            db,
            "admin_b@company-b.com",
            self.company_b.CompanyID,
            role_code="company_admin",
            first_name="Admin",
            last_name="B",
            onboarding_complete=True
        )
        self.user_b = create_test_user(
            db,
            "user_b@company-b.com",
            self.company_b.CompanyID,
            role_code="company_user",
            first_name="User",
            last_name="B",
            onboarding_complete=True
        )
        self.token_admin_b = create_test_token(
            int(self.admin_b.UserID),  # type: ignore
            str(self.admin_b.Email),  # type: ignore
            "company_admin",
            int(self.company_b.CompanyID)  # type: ignore
        )
        self.token_user_b = create_test_token(
            int(self.user_b.UserID),  # type: ignore
            str(self.user_b.Email),  # type: ignore
            "company_user",
            int(self.company_b.CompanyID)  # type: ignore
        )
    
    def cleanup(self):
        """Clean up test data"""
        # Note: In practice, tests should run in transactions that rollback
        # But this is here for completeness
        pass


def get_auth_headers(token: str) -> dict:
    """
    Get authorization headers for test requests.
    
    Args:
        token: JWT access token
        
    Returns:
        Dict with Authorization header
    """
    return {"Authorization": f"Bearer {token}"}
