"""
Company Service Module
Business logic for company creation and management
"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional, Tuple
from datetime import datetime

from models.company import Company
from models.user_company import UserCompany
from models.user import User
from models.ref.user_company_role import UserCompanyRole
from models.ref.user_company_status import UserCompanyStatus
from models.ref.joined_via import JoinedVia
from models.ref.country import Country
from models.ref.industry import Industry
from models.audit.company_audit import CompanyAudit
from common.validators import validate_australian_business_number
from common.logger import get_logger

logger = get_logger(__name__)


async def check_user_has_company(db: Session, user_id: int) -> bool:
    """
    Check if user already has an active company.
    
    Args:
        db: Database session
        user_id: User ID
        
    Returns:
        True if user has active company, False otherwise
    """
    # Check for active UserCompany relationship
    user_company = db.execute(
        select(UserCompany)
        .join(UserCompanyStatus)
        .where(
            UserCompany.UserID == user_id,
            UserCompany.IsDeleted == False,
            UserCompanyStatus.StatusCode == "active"
        )
    ).scalar_one_or_none()
    
    return user_company is not None


async def create_company(
    db: Session,
    user_id: int,
    company_name: str,
    abn: Optional[str],
    acn: Optional[str],
    phone: Optional[str],
    email: Optional[str],
    website: Optional[str],
    country_id: int,
    industry_id: Optional[int]
) -> Tuple[Company, UserCompany]:
    """
    Create a new company and assign user as company_admin.
    
    Args:
        db: Database session
        user_id: User ID creating the company
        company_name: Company name
        abn: ABN (optional, validated if provided)
        acn: ACN (optional, validated if provided)
        phone: Company phone
        email: Company email
        website: Company website
        country_id: Country ID
        industry_id: Industry ID (optional)
        
    Returns:
        Tuple of (Company, UserCompany)
        
    Raises:
        ValueError: If validation fails or user already has company
    """
    # Check user doesn't already have a company (AC-1.5.8)
    if await check_user_has_company(db, user_id):
        raise ValueError("User already has an active company")
    
    # Validate ABN/ACN if provided (AC-1.5.9)
    is_valid, error_msg = validate_australian_business_number(abn=abn, acn=acn)
    if not is_valid:
        raise ValueError(error_msg)
    
    # Validate country exists
    country = db.execute(
        select(Country).where(Country.CountryID == country_id)
    ).scalar_one_or_none()
    
    if not country:
        raise ValueError(f"Invalid country ID: {country_id}")
    
    # Validate industry if provided
    if industry_id:
        industry = db.execute(
            select(Industry).where(Industry.IndustryID == industry_id)
        ).scalar_one_or_none()
        
        if not industry:
            raise ValueError(f"Invalid industry ID: {industry_id}")
    
    # Create company (AC-1.5.4)
    company = Company(
        CompanyName=company_name,
        ABN=abn,
        ACN=acn,
        Phone=phone,
        Email=email,
        Website=website,
        CountryID=country_id,
        IndustryID=industry_id,
        DisplayNameSource="User",
        IsActive=True,
        CreatedBy=user_id,
        CreatedDate=datetime.utcnow(),
        UpdatedBy=user_id,
        UpdatedDate=datetime.utcnow(),
        IsDeleted=False
    )
    db.add(company)
    db.flush()  # Get CompanyID
    
    # Log company creation to audit (AC-1.5.7)
    # Log company creation to audit table (field-level tracking)
    # Create audit entries for each field being set during company creation
    user = db.get(User, user_id)
    company_fields = {
        "CompanyName": company_name,
        "ABN": abn,
        "ACN": acn,
        "CountryID": country_id,
        "IndustryID": industry_id
    }
    
    for field_name, field_value in company_fields.items():
        if field_value is not None:  # Only log fields that have values
            audit_entry = CompanyAudit(
                CompanyID=company.CompanyID,
                FieldName=field_name,
                OldValue=None,  # No old value for creation
                NewValue=str(field_value),
                ChangeType="INSERT",
                ChangeReason="Company created during onboarding",
                ChangedBy=user_id,
                ChangedByEmail=user.Email if user else None,
                IPAddress=None,  # TODO: Get from request context
                UserAgent=None   # TODO: Get from request context
            )
            db.add(audit_entry)
    
    # Get company_admin role
    admin_role = db.execute(
        select(UserCompanyRole).where(UserCompanyRole.RoleCode == "company_admin")
    ).scalar_one_or_none()
    
    if not admin_role:
        raise ValueError("company_admin role not found in database")
    
    # Get active status
    active_status = db.execute(
        select(UserCompanyStatus).where(UserCompanyStatus.StatusCode == "active")
    ).scalar_one_or_none()
    
    if not active_status:
        raise ValueError("active status not found in database")
    
    # Get signup joined_via
    signup_via = db.execute(
        select(JoinedVia).where(JoinedVia.MethodCode == "signup")
    ).scalar_one_or_none()
    
    if not signup_via:
        raise ValueError("signup joined_via not found in database")
    
    # Create UserCompany relationship (AC-1.5.5)
    user_company = UserCompany(
        UserID=user_id,
        CompanyID=company.CompanyID,
        UserCompanyRoleID=admin_role.UserCompanyRoleID,
        StatusID=active_status.UserCompanyStatusID,
        IsPrimaryCompany=True,  # First company is primary
        JoinedDate=datetime.utcnow(),
        JoinedViaID=signup_via.JoinedViaID,
        CreatedBy=user_id,
        CreatedDate=datetime.utcnow(),
        UpdatedBy=user_id,
        UpdatedDate=datetime.utcnow(),
        IsDeleted=False
    )
    db.add(user_company)
    
    # Update user onboarding status
    user = db.execute(
        select(User).where(User.UserID == user_id)
    ).scalar_one_or_none()
    
    if user:
        user.OnboardingComplete = True  # type: ignore
        user.OnboardingStep = 5  # type: ignore # Completed
        user.UpdatedDate = datetime.utcnow()  # type: ignore
        user.UpdatedBy = user_id  # type: ignore
    
    # DON'T COMMIT YET - let the router commit after JWT creation succeeds
    # This ensures if JWT creation fails, we can rollback the whole transaction
    db.flush()  # Flush to get IDs, but don't commit
    
    logger.info(
        f"Company prepared (not committed yet): CompanyID={company.CompanyID}, UserID={user_id}, "
        f"Role=company_admin, ABN={abn}, ACN={acn}"
    )
    
    return company, user_company

