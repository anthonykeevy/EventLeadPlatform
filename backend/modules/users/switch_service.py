"""
Service for handling company switching logic.
"""
from sqlalchemy.orm import Session
from sqlalchemy import select, update

from models.user import User
from models.company import Company
from models.user_company import UserCompany
from models.ref.user_company_role import UserCompanyRole
from modules.auth.jwt_service import create_access_token, create_refresh_token
from common.logger import get_logger

logger = get_logger(__name__)

class CompanySwitchService:
    def __init__(self, db: Session):
        self.db = db

    def switch_company(self, user_id: int, target_company_id: int) -> dict:
        """
        Switches the user's active company context.
        
        1. Validates user has access to the target company.
        2. Sets all of the user's other companies to IsPrimaryCompany=False.
        3. Sets the target company to IsPrimaryCompany=True.
        4. Generates new JWTs with the updated company_id and role.
        5. Returns new tokens and company details.
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
        # Assuming StatusID 1 is 'active' based on common practice.
        # TODO: Replace magic number 1 with an enum or a lookup from ref.UserCompanyStatus
        if target_user_company.StatusID != 1:
            raise ValueError("User is not active in the target company.")

        # Step 1: Set all user's companies to IsPrimaryCompany = False
        update_stmt = update(UserCompany).where(
            UserCompany.UserID == user_id
        ).values(IsPrimaryCompany=False)
        self.db.execute(update_stmt)

        # Step 2: Set the target company to IsPrimaryCompany = True
        target_user_company.IsPrimaryCompany = True
        self.db.add(target_user_company)

        # Get user and role details for new token
        user = self.db.get(User, user_id)
        if not user:
            raise ValueError("User not found.") # Should not happen

        role = self.db.get(UserCompanyRole, target_user_company.UserCompanyRoleID)
        if not role:
            raise ValueError("User role not found.") # Should not happen

        # Step 3: Generate new JWTs
        new_access_token = create_access_token(
            db=self.db,
            user_id=user.UserID,
            email=user.Email,
            role=role.RoleCode,
            company_id=target_company_id
        )
        
        new_refresh_token = create_refresh_token(
            user_id=user.UserID,
            db=self.db
        )

        # Step 4: Log the switch event (implementation pending audit service)
        # For now, we just log to standard logger.
        logger.info(f"User {user_id} switched company context to CompanyID={target_company_id}")
        
        self.db.commit()

        # Step 5: Return tokens and company details
        company = self.db.get(Company, target_company_id)
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "company": {
                "company_id": company.CompanyID,
                "company_name": company.CompanyName,
                "role": role.RoleCode
            }
        }
