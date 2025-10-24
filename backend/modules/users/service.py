"""
User Service Module
Business logic for user profile management
"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional, List
from datetime import datetime

from models.user import User
from models.ref.timezone import Timezone
from models.audit.user_audit import UserAudit
from models.user_company import UserCompany
from models.ref.user_company_status import UserCompanyStatus
from models.company_relationship import CompanyRelationship
from common.logger import get_logger

logger = get_logger(__name__)


async def get_user_companies_with_relationship_context(db: Session, user_id: int) -> List[dict]:
    """
    Get all active companies a user belongs to, enriched with relationship context.
    AC-1.11.1, AC-1.11.3, AC-1.11.8
    """
    # Get all active UserCompany associations
    uc_stmt = select(UserCompany).join(UserCompanyStatus).where(
        UserCompany.UserID == user_id,
        UserCompany.IsDeleted == False,
        UserCompanyStatus.StatusCode == "active"
    ).order_by(UserCompany.IsPrimaryCompany.desc(), UserCompany.JoinedDate.asc())
    user_companies = db.execute(uc_stmt).scalars().all()

    company_ids = [uc.CompanyID for uc in user_companies]
    if not company_ids:
        return []

    # Get all relationships involving any of the user's companies
    rel_stmt = select(CompanyRelationship).where(
        (CompanyRelationship.ParentCompanyID.in_(company_ids)) |
        (CompanyRelationship.ChildCompanyID.in_(company_ids)),
        CompanyRelationship.IsDeleted == False,
        CompanyRelationship.Status == 'active'
    )
    relationships = db.execute(rel_stmt).scalars().all()
    
    # Organize relationships for quick lookup
    rel_map = {}
    for rel in relationships:
        rel_map.setdefault(rel.ParentCompanyID, []).append(rel)
        rel_map.setdefault(rel.ChildCompanyID, []).append(rel)

    results = []
    for uc in user_companies:
        company_details = {
            "user_company": uc,
            "relationship": None
        }

        # Determine relationship context from the perspective of the *current* company (uc.CompanyID)
        if uc.CompanyID in rel_map:
            for rel in rel_map[uc.CompanyID]:
                # This logic finds the first relationship, assuming one company won't be
                # a branch and a partner of the same other company simultaneously.
                # More complex logic may be needed if multiple relationship types can coexist.
                
                # If the user's company is the PARENT in the relationship
                if rel.ParentCompanyID == uc.CompanyID:
                    if rel.relationship_type.TypeName == 'branch':
                        display_name = 'Head Office'
                    else: # subsidiary, partner
                        display_name = 'Parent'
                    
                    company_details['relationship'] = {
                        "type": "parent",
                        "display_name": display_name,
                        "related_company_id": rel.ChildCompanyID
                    }
                    break

                # If the user's company is the CHILD in the relationship
                elif rel.ChildCompanyID == uc.CompanyID:
                    if rel.relationship_type.TypeName == 'branch':
                        display_name = 'Branch'
                    elif rel.relationship_type.TypeName == 'subsidiary':
                        display_name = 'Subsidiary'
                    else: # partner
                         display_name = 'Partner'

                    company_details['relationship'] = {
                        "type": "child",
                        "display_name": display_name,
                        "related_company_id": rel.ParentCompanyID
                    }
                    break
        
        results.append(company_details)

    return results


async def update_user_details(
    db: Session,
    user_id: int,
    phone: Optional[str],
    timezone_identifier: str,
    role_title: Optional[str]
) -> User:
    """
    Update user profile details.
    
    Args:
        db: Database session
        user_id: User ID to update
        phone: Phone number (optional)
        timezone_identifier: IANA timezone identifier
        role_title: Job title (optional)
        
    Returns:
        Updated User object
        
    Raises:
        ValueError: If timezone is invalid or user not found
    """
    # Validate timezone exists (skip if ref.Timezone table not created yet - Epic 1 MVP)
    try:
        timezone = db.execute(
            select(Timezone).where(Timezone.TimezoneIdentifier == timezone_identifier)
        ).scalar_one_or_none()
        
        if not timezone:
            # For Epic 1: Accept any timezone if table doesn't exist
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Timezone validation skipped - ref.Timezone table may not exist: {timezone_identifier}")
    except Exception as e:
        # Table doesn't exist yet - skip validation for Epic 1
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Timezone validation skipped (table not found): {str(e)}")
    
    # Get user
    user = db.execute(
        select(User).where(User.UserID == user_id)
    ).scalar_one_or_none()
    
    if not user:
        raise ValueError(f"User not found: {user_id}")
    
    # Store old values for audit
    old_values = {
        "Phone": user.Phone,
        "TimezoneIdentifier": user.TimezoneIdentifier,
        "RoleTitle": user.RoleTitle
    }
    
    # Update user details
    user.Phone = phone  # type: ignore
    user.TimezoneIdentifier = timezone_identifier  # type: ignore
    user.RoleTitle = role_title  # type: ignore
    user.UpdatedDate = datetime.utcnow()  # type: ignore
    user.UpdatedBy = user_id  # type: ignore
    
    # Log to audit table (Story 1.5: AC-1.5.7)
    # UserAudit is field-level tracking - create one entry per changed field
    changed_fields = []
    if old_values["Phone"] != phone:
        changed_fields.append(("Phone", old_values["Phone"], phone))
    if old_values["TimezoneIdentifier"] != timezone_identifier:
        changed_fields.append(("TimezoneIdentifier", old_values["TimezoneIdentifier"], timezone_identifier))
    if old_values["RoleTitle"] != role_title:
        changed_fields.append(("RoleTitle", old_values["RoleTitle"], role_title))
    
    # Create audit entry for each changed field
    try:
        for field_name, old_val, new_val in changed_fields:
            audit_entry = UserAudit(
                UserID=user_id,
                FieldName=field_name,
                OldValue=str(old_val) if old_val is not None else None,
                NewValue=str(new_val) if new_val is not None else None,
                ChangeType="UPDATE",
                ChangeReason="User profile update during onboarding",
                ChangedBy=user_id,
                ChangedByEmail=user.Email,
                IPAddress=None,  # TODO: Get from request context
                UserAgent=None   # TODO: Get from request context
            )
            db.add(audit_entry)
        
        db.commit()
        db.refresh(user)
        
        logger.info(f"User details updated: UserID={user_id}, Timezone={timezone_identifier}")
        
        return user
        
    except Exception as e:
        logger.error(f"Error committing user details update: {str(e)}", exc_info=True)
        db.rollback()  # Explicit rollback on error
        raise


async def get_user_profile(db: Session, user_id: int) -> Optional[User]:
    """
    Get user profile by ID.
    
    Args:
        db: Database session
        user_id: User ID
        
    Returns:
        User object or None if not found
    """
    return db.execute(
        select(User).where(User.UserID == user_id)
    ).scalar_one_or_none()

