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
from common.company_verification import verify_email_domain_ownership
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
    ).first()  # Use first() instead of scalar_one_or_none() to handle multiple rows gracefully
    
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
    industry_id: Optional[int],
    legal_entity_name: Optional[str] = None,
    abn_status: Optional[str] = None,
    entity_type: Optional[str] = None,
    gst_registered: Optional[bool] = None
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
    
    # Check for duplicate ABN (Story 1.19)
    # Business Rule: Only one company per ABN, but allow multiple NULL ABNs
    if abn:
        existing_company_row = db.execute(
            select(Company).where(
                Company.ABN == abn,
                Company.IsDeleted == False
            )
        ).first()
        
        if existing_company_row:
            existing_company = existing_company_row[0]
            
            # Get user email for domain verification
            user = db.execute(
                select(User).where(User.UserID == user_id)
            ).scalar_one_or_none()
            
            if not user:
                raise ValueError("User not found")
            
            # Story 1.19: Email domain verification (prevents squatter attacks)
            # If user's email domain matches company → Auto-join instead of error
            user_email = str(user.Email) if user.Email else ""
            company_name = str(existing_company.CompanyName or existing_company.LegalEntityName or "")
            
            is_verified, verification_reason = verify_email_domain_ownership(
                user_email, 
                company_name
            )
            
            if is_verified:
                # Auto-join existing company (domain matches - likely legitimate employee)
                logger.info(
                    f"Auto-joining user to existing company: UserID={user_id}, "
                    f"CompanyID={existing_company.CompanyID}, ABN={abn}, "
                    f"Reason: {verification_reason}"
                )
                
                # Get company_admin role ID
                admin_role = db.execute(
                    select(UserCompanyRole).where(UserCompanyRole.RoleName == 'company_admin')
                ).scalar_one_or_none()
                
                if not admin_role:
                    raise ValueError("company_admin role not found in reference data")
                
                # Get active status ID
                active_status = db.execute(
                    select(UserCompanyStatus).where(UserCompanyStatus.StatusCode == 'active')
                ).scalar_one_or_none()
                
                if not active_status:
                    raise ValueError("active status not found in reference data")
                
                # Create UserCompany relationship (company already exists)
                user_company = UserCompany(
                    UserID=user_id,
                    CompanyID=existing_company.CompanyID,
                    UserCompanyRoleID=admin_role.UserCompanyRoleID,
                    StatusID=active_status.UserCompanyStatusID,
                    JoinedDate=datetime.utcnow(),
                    CreatedBy=user_id,
                    CreatedDate=datetime.utcnow(),
                    UpdatedBy=user_id,
                    UpdatedDate=datetime.utcnow(),
                    IsDeleted=False
                )
                db.add(user_company)
                db.flush()
                
                logger.info(
                    f"User auto-joined existing company via domain verification: "
                    f"UserID={user_id}, Email={user_email}, CompanyID={existing_company.CompanyID}, "
                    f"CompanyName={company_name}"
                )
                
                # Return existing company + new user-company relationship
                return existing_company, user_company
            else:
                # Domain doesn't match - prevent squatting
                logger.warning(
                    f"Duplicate ABN registration blocked: UserID={user_id}, Email={user_email}, "
                    f"ABN={abn}, ExistingCompany={company_name}, "
                    f"Reason: {verification_reason}"
                )
                
                # Get admin contact hints (privacy-safe)
                # Find all company_admin users for this company
                admin_hints = db.execute(
                    select(User.FirstName, User.LastName, User.Email)
                    .select_from(UserCompany)
                    .join(User, UserCompany.UserID == User.UserID)
                    .join(UserCompanyRole, UserCompany.UserCompanyRoleID == UserCompanyRole.UserCompanyRoleID)
                    .where(
                        UserCompany.CompanyID == existing_company.CompanyID,
                        UserCompany.IsDeleted == False,
                        UserCompanyRole.RoleName == 'company_admin'
                    )
                    .limit(3)  # Show up to 3 admins
                ).fetchall()
                
                logger.debug(f"Found {len(admin_hints)} admin(s) for company {existing_company.CompanyID}")
                
                # Build helpful contact message
                admin_count = len(admin_hints)
                contact_info = ""
                
                if admin_count > 0:
                    # Extract email domain from first admin
                    email_domain = admin_hints[0][2].split('@')[1] if '@' in admin_hints[0][2] else None
                    
                    # Create admin name hints (First name + Last initial)
                    admin_names = [
                        f"{admin[0]} {admin[1][0]}." if admin[1] else admin[0]
                        for admin in admin_hints
                    ]
                    
                    contact_info = f" This company has {admin_count} administrator{'s' if admin_count > 1 else ''}"
                    if email_domain:
                        contact_info += f" (contact at @{email_domain})"
                    if admin_names:
                        contact_info += f": {', '.join(admin_names[:3])}"
                    contact_info += "."
                
                raise ValueError(
                    f"A company with ABN {abn} already exists in the system. "
                    f"Company name: {existing_company.CompanyName}.{contact_info} "
                    f"Please request access from an existing administrator."
                )
    
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
        LegalEntityName=legal_entity_name,  # Story 1.19: ABR data
        ABNStatus=abn_status,  # Story 1.19: ABR data
        EntityType=entity_type,  # Story 1.19: ABR data
        GSTRegistered=gst_registered,  # Story 1.19: ABR data
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

