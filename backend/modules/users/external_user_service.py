"""
External User Service
Handles management of "Shadow Users" (External Approvers).
Story 2.12
"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from typing import Optional, Tuple
import secrets
import string

from models.user import User
from models.ref.user_status import UserStatus
from common.security import hash_password as get_password_hash
from common.logger import get_logger

logger = get_logger(__name__)

class ExternalUserService:
    
    def __init__(self, db: Session):
        self.db = db
        
    async def get_or_create_external_user(self, email: str, first_name: str = "External", last_name: str = "Approver") -> Tuple[User, bool]:
        """
        Find existing user by email, or create a new 'External' user.
        Returns (User, created_new)
        """
        # 1. Check for existing user
        user = self.db.execute(
            select(User).where(User.Email == email)
        ).scalar_one_or_none()
        
        if user:
            logger.info(f"Found existing user for external request: {email} (Status: {user.StatusID})")
            return user, False
            
        # 2. Create new "Shadow" User
        # Get 'EXTERNAL' status ID
        external_status = self.db.execute(
            select(UserStatus).where(UserStatus.StatusCode == 'EXTERNAL')
        ).scalar_one_or_none()
        
        if not external_status:
            raise ValueError("User Status 'EXTERNAL' not found in database. Please run migrations.")
            
        # Generate a random unusable password (they will set it on signup)
        # We still hash it to satisfy NOT NULL constraint and security best practices
        random_pw = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
        pw_hash = get_password_hash(random_pw)
        
        new_user = User(
            Email=email,
            FirstName=first_name,
            LastName=last_name,
            PasswordHash=pw_hash,
            StatusID=external_status.UserStatusID,
            IsEmailVerified=False, # They haven't verified via signup yet
            CreatedDate=datetime.utcnow(),
            IsLocked=False,
            FailedLoginAttempts=0,
            AccessTokenVersion=1,
            RefreshTokenVersion=1,
            OnboardingComplete=False
        )
        
        self.db.add(new_user)
        self.db.flush() # Get ID
        
        logger.info(f"Created new EXTERNAL user: {email} (ID: {new_user.UserID})")
        return new_user, True

    async def upgrade_external_user(self, user_id: int, password_hash: str, first_name: str, last_name: str) -> User:
        """
        Upgrade an EXTERNAL user to ACTIVE/PENDING during signup.
        """
        user = self.db.get(User, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
            
        # Verify current status is EXTERNAL
        # We need to load the status relationship or query it
        status = self.db.get(UserStatus, user.StatusID)
        if status.StatusCode != 'EXTERNAL':
            # If already active, we shouldn't be here usually (Auth service handles login)
            # But if they are creating an account for an existing email...
            logger.warning(f"Attempting to upgrade user {user.Email} with status {status.StatusCode}")
            # Proceeding might be okay if we are just updating details?
            # But for now, let's assume this flow is specifically for External -> Full
            pass
            
        # Get ACTIVE or PENDING status
        # Usually we set to PENDING_VERIFICATION until they verify email
        # But since they are signing up now, they will verify email next
        target_status = self.db.execute(
            select(UserStatus).where(UserStatus.StatusCode == 'PENDING') # Pending verification
        ).scalar_one_or_none()
        
        if not target_status:
             # Fallback to Active if Pending not found (rare)
             target_status = self.db.execute(
                select(UserStatus).where(UserStatus.StatusCode == 'ACTIVE')
            ).scalar_one_or_none()
            
        user.StatusID = target_status.UserStatusID
        user.PasswordHash = password_hash
        user.FirstName = first_name
        user.LastName = last_name
        user.UpdatedDate = datetime.utcnow()
        
        self.db.flush()
        logger.info(f"Upgraded EXTERNAL user {user.Email} to {target_status.StatusCode}")
        
        return user

