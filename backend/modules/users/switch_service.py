"""
Service for handling company switching logic.
"""
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from typing import Optional

from models.user import User
from models.company import Company
from models.user_company import UserCompany
from models.ref.user_company_role import UserCompanyRole
from models.ref.user_company_status import UserCompanyStatus
from modules.auth.jwt_service import create_access_token, create_refresh_token
from common.logger import get_logger

logger = get_logger(__name__)

class CompanySwitchService:
    def __init__(self, db: Session):
        self.db = db

    def switch_company(self, user_id: int, target_company_id: int, current_role: Optional[str] = None) -> dict:
        """
        Switches the user's active company context.
        
        1. Validates user has access to the target company (unless System Admin).
        2. Generates new JWTs with the updated company_id and role.
        3. Returns new tokens and company details.
        
        Note: This does NOT change the default company (IsPrimaryCompany). 
        The default company is only changed when explicitly set via set_default_company().
        
        System Admins: Can switch to any company without needing a UserCompany record.
        """
        # Get user to check if they're a System Admin
        user = self.db.get(User, user_id)
        if not user:
            raise ValueError("User not found.") # Should not happen
        
        # Check if user is a System Admin (via UserRoleID)
        is_system_admin = False
        role_code = None
        
        if user.UserRoleID is not None:
            from models.ref.user_role import UserRole
            user_role = self.db.get(UserRole, user.UserRoleID)
            if user_role and user_role.RoleCode == "system_admin":
                is_system_admin = True
                role_code = "system_admin"
        
        # If not System Admin, validate company membership
        if not is_system_admin:
            # Get the target UserCompany record
            target_uc_stmt = select(UserCompany).where(
                UserCompany.UserID == user_id,
                UserCompany.CompanyID == target_company_id
            )
            target_user_company = self.db.execute(target_uc_stmt).scalars().first()

            # Validation: User must belong to the target company
            if not target_user_company:
                raise ValueError("User does not have access to the target company.")
            
            # Validation: User's status in the company must be active
            user_company_status = self.db.get(UserCompanyStatus, target_user_company.StatusID)
            if not user_company_status or user_company_status.StatusCode != "active":
                raise ValueError("User is not active in the target company.")

            # Get role from UserCompany
            role = self.db.get(UserCompanyRole, target_user_company.UserCompanyRoleID)
            if not role:
                raise ValueError("User role not found.") # Should not happen
            role_code = role.RoleCode
        else:
            # System Admin: Use system_admin role, no UserCompany record needed
            # Verify company exists
            company = self.db.get(Company, target_company_id)
            if not company or company.IsDeleted:
                raise ValueError("Company not found or has been deleted.")

        # Step 3: Generate new JWTs
        new_access_token = create_access_token(
            db=self.db,
            user_id=user.UserID,
            email=user.Email,
            role=role_code,  # "system_admin" for System Admins, company role for others
            company_id=target_company_id
        )
        
        new_refresh_token = create_refresh_token(
            user_id=user.UserID,
            db=self.db
        )

        # Step 4: Log the switch event (implementation pending audit service)
        # For now, we just log to standard logger.
        logger.info(f"User {user_id} ({'System Admin' if is_system_admin else 'Regular User'}) switched company context to CompanyID={target_company_id}")
        
        self.db.commit()

        # Step 5: Return tokens and company details
        company = self.db.get(Company, target_company_id)
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "company": {
                "company_id": company.CompanyID,
                "company_name": company.CompanyName,
                "role": role_code
            }
        }
    
    def set_default_company(self, user_id: int, target_company_id: int) -> dict:
        """
        Sets a company as the user's default (primary) company without switching context.
        
        1. Validates user has access to the target company.
        2. Sets all of the user's other companies to IsPrimaryCompany=False.
        3. Sets the target company to IsPrimaryCompany=True.
        4. Returns company details (does NOT generate new tokens).
        """
        # Get the target UserCompany record
        target_uc_stmt = select(UserCompany).where(
            UserCompany.UserID == user_id,
            UserCompany.CompanyID == target_company_id
        )
        target_user_company = self.db.execute(target_uc_stmt).scalars().first()

        # Validation: User must belong to the target company
        if not target_user_company:
            raise ValueError("User does not have access to the target company.")
        
        # Validation: User's status in the company must be active
        user_company_status = self.db.get(UserCompanyStatus, target_user_company.StatusID)
        if not user_company_status or user_company_status.StatusCode != "active":
            raise ValueError("User is not active in the target company.")

        # Step 1: Set all user's companies to IsPrimaryCompany = False
        update_stmt = update(UserCompany).where(
            UserCompany.UserID == user_id
        ).values(IsPrimaryCompany=False)
        self.db.execute(update_stmt)

        # Step 2: Set the target company to IsPrimaryCompany = True
        target_user_company.IsPrimaryCompany = True
        self.db.add(target_user_company)

        # Step 3: Log the default company change
        logger.info(f"User {user_id} set CompanyID={target_company_id} as default company")
        
        self.db.commit()

        # Step 4: Return company details (no new tokens - user doesn't switch context)
        company = self.db.get(Company, target_company_id)
        role = self.db.get(UserCompanyRole, target_user_company.UserCompanyRoleID)
        
        return {
            "company": {
                "company_id": company.CompanyID,
                "company_name": company.CompanyName,
                "role": role.RoleCode if role else None
            }
        }
