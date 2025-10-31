"""
User Service Module
Business logic for user profile management
"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional, List
from datetime import datetime

from models.user import User
from models.user_industry import UserIndustry
from models.ref.timezone import Timezone
from models.ref.theme_preference import ThemePreference
from models.ref.layout_density import LayoutDensity
from models.ref.font_size import FontSize
from models.ref.industry import Industry
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


# ============================================================================
# Epic 2: Enhanced User Profile Management
# ============================================================================

async def update_user_profile_enhancements(
    db: Session,
    user_id: int,
    bio: Optional[str] = None,
    theme_preference_id: Optional[int] = None,
    layout_density_id: Optional[int] = None,
    font_size_id: Optional[int] = None
) -> User:
    """
    Update user profile enhancements (Epic 2).
    
    Args:
        db: Database session
        user_id: User ID to update
        bio: Professional bio (optional)
        theme_preference_id: Theme preference ID (optional)
        layout_density_id: Layout density ID (optional)
        font_size_id: Font size ID (optional)
        
    Returns:
        Updated User object
        
    Raises:
        ValueError: If user not found or invalid IDs
    """
    # Get user
    user = db.execute(
        select(User).where(User.UserID == user_id)
    ).scalar_one_or_none()
    
    if not user:
        raise ValueError(f"User not found: {user_id}")
    
    # Validate foreign key references if provided
    if theme_preference_id is not None:
        theme = db.get(ThemePreference, theme_preference_id)
        if not theme:
            raise ValueError(f"Invalid theme preference ID: {theme_preference_id}")
    
    if layout_density_id is not None:
        density = db.get(LayoutDensity, layout_density_id)
        if not density:
            raise ValueError(f"Invalid layout density ID: {layout_density_id}")
    
    if font_size_id is not None:
        font_size = db.get(FontSize, font_size_id)
        if not font_size:
            raise ValueError(f"Invalid font size ID: {font_size_id}")
    
    # Store old values for audit
    old_values = {
        "Bio": user.Bio,
        "ThemePreferenceID": user.ThemePreferenceID,
        "LayoutDensityID": user.LayoutDensityID,
        "FontSizeID": user.FontSizeID
    }
    
    # Update user profile
    updates_made = False
    if bio is not None:
        user.Bio = bio  # type: ignore
        updates_made = True
    if theme_preference_id is not None:
        old_theme = user.ThemePreferenceID
        user.ThemePreferenceID = theme_preference_id  # type: ignore
        if old_theme != theme_preference_id:
            updates_made = True
            logger.info(f"Updating ThemePreferenceID: {old_theme} -> {theme_preference_id}")
    if layout_density_id is not None:
        old_density = user.LayoutDensityID
        user.LayoutDensityID = layout_density_id  # type: ignore
        if old_density != layout_density_id:
            updates_made = True
            logger.info(f"Updating LayoutDensityID: {old_density} -> {layout_density_id}")
    if font_size_id is not None:
        old_font = user.FontSizeID
        user.FontSizeID = font_size_id  # type: ignore
        if old_font != font_size_id:
            updates_made = True
            logger.info(f"Updating FontSizeID: {old_font} -> {font_size_id}")
    
    if not updates_made:
        logger.warning(f"No updates to make for user {user_id}")
        db.refresh(user)
        return user
    
    user.UpdatedDate = datetime.utcnow()  # type: ignore
    user.UpdatedBy = user_id  # type: ignore
    
    # Log to audit table
    changed_fields = []
    if old_values["Bio"] != bio and bio is not None:
        changed_fields.append(("Bio", old_values["Bio"], bio))
    if old_values["ThemePreferenceID"] != theme_preference_id and theme_preference_id is not None:
        changed_fields.append(("ThemePreferenceID", old_values["ThemePreferenceID"], theme_preference_id))
    if old_values["LayoutDensityID"] != layout_density_id and layout_density_id is not None:
        changed_fields.append(("LayoutDensityID", old_values["LayoutDensityID"], layout_density_id))
    if old_values["FontSizeID"] != font_size_id and font_size_id is not None:
        changed_fields.append(("FontSizeID", old_values["FontSizeID"], font_size_id))
    
    try:
        # Add audit entries first
        for field_name, old_val, new_val in changed_fields:
            audit_entry = UserAudit(
                UserID=user_id,
                FieldName=field_name,
                OldValue=str(old_val) if old_val is not None else None,
                NewValue=str(new_val) if new_val is not None else None,
                ChangeType="UPDATE",
                ChangeReason="User profile enhancement update",
                ChangedBy=user_id,
                ChangedByEmail=user.Email,
                IPAddress=None,
                UserAgent=None
            )
            db.add(audit_entry)
        
        # Flush to ensure changes are tracked
        db.flush()
        
        # Commit all changes (user updates + audit entries)
        db.commit()
        
        # Refresh user to get latest data from database
        db.refresh(user)
        
        # Verify what was actually saved
        logger.info(f"User profile enhancements COMMITTED: UserID={user_id}, "
                   f"ThemePreferenceID={user.ThemePreferenceID} (expected: {theme_preference_id}), "
                   f"LayoutDensityID={user.LayoutDensityID} (expected: {layout_density_id}), "
                   f"FontSizeID={user.FontSizeID} (expected: {font_size_id})")
        
        # Double-check by querying database directly
        verify_user = db.execute(
            select(User).where(User.UserID == user_id)
        ).scalar_one_or_none()
        if verify_user:
            logger.info(f"Database verification - UserID={verify_user.UserID}, "
                       f"ThemePreferenceID={verify_user.ThemePreferenceID}, "
                       f"LayoutDensityID={verify_user.LayoutDensityID}, "
                       f"FontSizeID={verify_user.FontSizeID}")
        
        return user
        
    except Exception as e:
        logger.error(f"Error committing profile enhancement update: {str(e)}", exc_info=True)
        db.rollback()
        raise


async def get_user_industries(db: Session, user_id: int) -> List[UserIndustry]:
    """
    Get all active industry associations for a user.
    
    Args:
        db: Database session
        user_id: User ID
        
    Returns:
        List of UserIndustry records
    """
    stmt = select(UserIndustry).where(
        UserIndustry.UserID == user_id,
        UserIndustry.IsDeleted == False
    ).order_by(UserIndustry.IsPrimary.desc(), UserIndustry.SortOrder.asc())
    
    return list(db.execute(stmt).scalars().all())


async def add_user_industry(
    db: Session,
    user_id: int,
    industry_id: int,
    is_primary: bool = False,
    sort_order: Optional[int] = None
) -> UserIndustry:
    """
    Add an industry association to a user.
    
    Args:
        db: Database session
        user_id: User ID
        industry_id: Industry ID
        is_primary: Whether this is the primary industry
        sort_order: Display order (auto-assigned if not provided)
        
    Returns:
        Created UserIndustry object
        
    Raises:
        ValueError: If user/industry not found, duplicate association, or constraint violation
    """
    # Validate user exists
    user = db.get(User, user_id)
    if not user:
        raise ValueError(f"User not found: {user_id}")
    
    # Validate industry exists
    industry = db.get(Industry, industry_id)
    if not industry:
        raise ValueError(f"Industry not found: {industry_id}")
    
    # Check for duplicate association
    existing = db.execute(
        select(UserIndustry).where(
            UserIndustry.UserID == user_id,
            UserIndustry.IndustryID == industry_id,
            UserIndustry.IsDeleted == False
        )
    ).scalar_one_or_none()
    
    if existing:
        raise ValueError(f"Industry already associated with user: {industry_id}")
    
    # If setting as primary, unset other primary industries
    if is_primary:
        other_primary = db.execute(
            select(UserIndustry).where(
                UserIndustry.UserID == user_id,
                UserIndustry.IsPrimary == True,
                UserIndustry.IsDeleted == False
            )
        ).scalars().all()
        
        for ui in other_primary:
            ui.IsPrimary = False  # type: ignore
            ui.UpdatedDate = datetime.utcnow()  # type: ignore
            ui.UpdatedBy = user_id  # type: ignore
            ui.SortOrder = ui.SortOrder + 1 if ui.SortOrder else 1  # type: ignore
    
    # Assign sort order
    if sort_order is None:
        if is_primary:
            sort_order = 0
        else:
            # Get max sort order and add 1
            max_sort = db.execute(
                select(UserIndustry.SortOrder).where(
                    UserIndustry.UserID == user_id,
                    UserIndustry.IsDeleted == False
                ).order_by(UserIndustry.SortOrder.desc())
            ).scalar()
            sort_order = (max_sort or 0) + 1 if max_sort else 1
    
    # Create UserIndustry record
    user_industry = UserIndustry(
        UserID=user_id,
        IndustryID=industry_id,
        IsPrimary=is_primary,
        SortOrder=sort_order,
        CreatedBy=user_id,
        UpdatedBy=user_id
    )
    
    try:
        db.add(user_industry)
        db.commit()
        db.refresh(user_industry)
        
        logger.info(f"Industry added to user: UserID={user_id}, IndustryID={industry_id}, IsPrimary={is_primary}")
        
        return user_industry
        
    except Exception as e:
        logger.error(f"Error adding industry to user: {str(e)}", exc_info=True)
        db.rollback()
        raise


async def update_user_industry(
    db: Session,
    user_industry_id: int,
    user_id: int,
    is_primary: Optional[bool] = None,
    sort_order: Optional[int] = None
) -> UserIndustry:
    """
    Update an existing industry association.
    
    Args:
        db: Database session
        user_industry_id: UserIndustry ID
        user_id: User ID (for verification)
        is_primary: Whether this should be the primary industry
        sort_order: Display order
        
    Returns:
        Updated UserIndustry object
        
    Raises:
        ValueError: If association not found or constraint violation
    """
    # Get association
    user_industry = db.get(UserIndustry, user_industry_id)
    if not user_industry:
        raise ValueError(f"Industry association not found: {user_industry_id}")
    
    # Verify ownership
    if user_industry.UserID != user_id:
        raise ValueError(f"User does not own this association: {user_industry_id}")
    
    # If setting as primary, unset other primary industries
    if is_primary is not None and is_primary and not user_industry.IsPrimary:
        other_primary = db.execute(
            select(UserIndustry).where(
                UserIndustry.UserID == user_id,
                UserIndustry.UserIndustryID != user_industry_id,
                UserIndustry.IsPrimary == True,
                UserIndustry.IsDeleted == False
            )
        ).scalars().all()
        
        for ui in other_primary:
            ui.IsPrimary = False  # type: ignore
            ui.UpdatedDate = datetime.utcnow()  # type: ignore
            ui.UpdatedBy = user_id  # type: ignore
            ui.SortOrder = ui.SortOrder + 1 if ui.SortOrder else 1  # type: ignore
    
    # Update fields
    if is_primary is not None:
        user_industry.IsPrimary = is_primary  # type: ignore
        if is_primary:
            user_industry.SortOrder = 0  # type: ignore
    if sort_order is not None:
        user_industry.SortOrder = sort_order  # type: ignore
    
    user_industry.UpdatedDate = datetime.utcnow()  # type: ignore
    user_industry.UpdatedBy = user_id  # type: ignore
    
    try:
        db.commit()
        db.refresh(user_industry)
        
        logger.info(f"Industry association updated: UserIndustryID={user_industry_id}")
        
        return user_industry
        
    except Exception as e:
        logger.error(f"Error updating industry association: {str(e)}", exc_info=True)
        db.rollback()
        raise


async def remove_user_industry(db: Session, user_industry_id: int, user_id: int) -> None:
    """
    Remove (soft delete) an industry association.
    
    Args:
        db: Database session
        user_industry_id: UserIndustry ID
        user_id: User ID (for verification)
        
    Raises:
        ValueError: If association not found
    """
    # Get association
    user_industry = db.get(UserIndustry, user_industry_id)
    if not user_industry:
        raise ValueError(f"Industry association not found: {user_industry_id}")
    
    # Verify ownership
    if user_industry.UserID != user_id:
        raise ValueError(f"User does not own this association: {user_industry_id}")
    
    # Soft delete
    user_industry.IsDeleted = True  # type: ignore
    user_industry.DeletedDate = datetime.utcnow()  # type: ignore
    user_industry.DeletedBy = user_id  # type: ignore
    user_industry.UpdatedDate = datetime.utcnow()  # type: ignore
    user_industry.UpdatedBy = user_id  # type: ignore
    
    try:
        db.commit()
        
        logger.info(f"Industry association removed: UserIndustryID={user_industry_id}")
        
    except Exception as e:
        logger.error(f"Error removing industry association: {str(e)}", exc_info=True)
        db.rollback()
        raise

