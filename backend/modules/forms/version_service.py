"""
Form Version Service
Business logic for form versioning and publishing
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func, desc, update
from typing import List, Optional, Dict, Any
from datetime import datetime
import json

from models.form_version import FormVersion
from models.form import Form
from models.audit.activity_log import ActivityLog
from common.logger import get_logger
from modules.forms.access_guard import check_form_access_guard

logger = get_logger(__name__)

class FormVersionService:
    def __init__(self, db: Session):
        self.db = db

    async def get_versions(self, form_id: int, user_id: int) -> List[FormVersion]:
        """
        Get all versions for a form.
        """
        # Check VIEW access to the form
        await check_form_access_guard(self.db, form_id, user_id, "VIEW")

        stmt = select(FormVersion).where(
            FormVersion.FormID == form_id
        ).order_by(desc(FormVersion.VersionNumber))
        
        result = self.db.execute(stmt)
        return result.scalars().all()

    async def get_version(self, form_id: int, version_number: int, user_id: int) -> Optional[FormVersion]:
        """
        Get a specific version.
        """
        # Check VIEW access
        await check_form_access_guard(self.db, form_id, user_id, "VIEW")

        stmt = select(FormVersion).where(
            FormVersion.FormID == form_id,
            FormVersion.VersionNumber == version_number
        )
        return self.db.execute(stmt).scalar_one_or_none()

    async def create_version(self, form_id: int, user_id: int, definition: Dict[str, Any], comment: Optional[str] = None) -> FormVersion:
        """
        Create a new draft version.
        """
        # Check MANAGE/EDIT access
        await check_form_access_guard(self.db, form_id, user_id, "EDIT")

        # Get next version number
        last_ver = self.db.execute(
            select(func.max(FormVersion.VersionNumber))
            .where(FormVersion.FormID == form_id)
        ).scalar() or 0
        
        new_ver_num = last_ver + 1

        # Create new version
        new_version = FormVersion(
            FormID=form_id,
            VersionNumber=new_ver_num,
            DefinitionJSON=json.dumps(definition),
            VersionComment=comment,
            Status='DRAFT',
            IsActive=False,
            CreatedBy=user_id,
            CreatedDate=datetime.utcnow()
        )
        
        self.db.add(new_version)
        self.db.flush()
        
        logger.info(f"Created FormVersion {new_ver_num} for Form {form_id} by User {user_id}")
        return new_version

    async def update_version(self, form_id: int, version_number: int, user_id: int, definition: Dict[str, Any], comment: Optional[str] = None) -> FormVersion:
        """
        Update a DRAFT version.
        """
        # Check EDIT access
        await check_form_access_guard(self.db, form_id, user_id, "EDIT")

        stmt = select(FormVersion).where(
            FormVersion.FormID == form_id,
            FormVersion.VersionNumber == version_number
        )
        version = self.db.execute(stmt).scalar_one_or_none()
        
        if not version:
            raise ValueError(f"Version {version_number} not found")
            
        if version.Status != 'DRAFT':
            raise ValueError("Only DRAFT versions can be modified")
            
        version.DefinitionJSON = json.dumps(definition)
        if comment is not None:
            version.VersionComment = comment
            
        self.db.flush()
        
        logger.info(f"Updated FormVersion {version_number} for Form {form_id} by User {user_id}")
        return version

    async def publish_version(self, form_id: int, version_number: int, user_id: int) -> FormVersion:
        """
        Publish a specific version, making it the active one.
        """
        # Check MANAGE access (Publishing is a Manage action)
        await check_form_access_guard(self.db, form_id, user_id, "MANAGE")

        # Get the target version
        stmt = select(FormVersion).where(
            FormVersion.FormID == form_id,
            FormVersion.VersionNumber == version_number
        )
        target_version = self.db.execute(stmt).scalar_one_or_none()
        
        if not target_version:
            raise ValueError(f"Version {version_number} not found for Form {form_id}")

        # Deactivate all other versions
        self.db.execute(
            update(FormVersion)
            .where(FormVersion.FormID == form_id)
            .values(IsActive=False)
        )
        
        # Activate target version
        target_version.IsActive = True
        target_version.Status = 'PUBLISHED'
        target_version.PublishedDate = datetime.utcnow()
        target_version.PublishedBy = user_id
        
        self.db.flush()
        
        # Log activity
        self._log_activity(user_id, form_id, "form_version.published", 
                          f"Published version {version_number}", 
                          {"version": version_number})
        
        logger.info(f"Published FormVersion {version_number} for Form {form_id} by User {user_id}")
        return target_version

    async def get_active_version(self, form_id: int, user_id: int) -> Optional[FormVersion]:
        """
        Get the currently active (published) version.
        """
        # Check VIEW access
        await check_form_access_guard(self.db, form_id, user_id, "VIEW")

        stmt = select(FormVersion).where(
            FormVersion.FormID == form_id,
            FormVersion.IsActive == True
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def _log_activity(self, user_id: int, form_id: int, action: str, details: str, new_value: Dict[str, Any]):
        try:
            log = ActivityLog(
                UserID=user_id,
                CompanyID=0, # TBD: Fetch from form
                Action=action,
                EntityType="FormVersion",
                EntityID=form_id, # Logging against the Form
                NewValue=json.dumps(new_value),
                # Comments field does not exist in ActivityLog model, putting in NewValue JSON if needed
                # But here we just drop it as details is passed in NewValue already if we structure it right
                # Actually, details is passed as 'details' argument. Let's add it to NewValue.
                CreatedDate=datetime.utcnow()
            )
            
            # Update NewValue to include details
            current_val = json.loads(log.NewValue) if log.NewValue else {}
            current_val['details'] = details
            log.NewValue = json.dumps(current_val)
            # We need to get CompanyID from the Form for proper logging
            form = self.db.get(Form, form_id)
            if form:
                log.CompanyID = form.CompanyID
            
            self.db.add(log)
        except Exception as e:
            logger.error(f"Failed to log activity: {e}")
