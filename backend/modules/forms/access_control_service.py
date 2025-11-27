"""
Form Access Control Service
Business logic for form access control operations (grant, revoke, check access)
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, or_, and_, func, text
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone

from models.form_access_control import FormAccessControl
from models.form import Form
from models.user import User
from models.company import Company
from models.ref.form_access_control_access_type import FormAccessControlAccessType
from models.ref.company_relationship_type import CompanyRelationshipType
from models.audit.activity_log import ActivityLog
from common.logger import get_logger

logger = get_logger(__name__)


async def grant_access(
    db: Session,
    form_id: int,
    user_id: Optional[int],
    company_id: int,
    granted_by: int,
    access_type_id: int,
    relationship_type_id: int,
    expiry_date: Optional[datetime] = None,
    target_company_id: Optional[int] = None  # Company to grant access to (for company-wide access)
) -> FormAccessControl:
    """
    Grant access to a form for a user/company.
    
    Args:
        db: Database session
        form_id: Form ID
        user_id: User ID to grant access to (required for user access, None for company-wide)
        company_id: Company ID that owns the form (form owner's company)
        granted_by: User ID granting access (must have Manage access)
        access_type_id: FormAccessControlAccessType ID
        relationship_type_id: CompanyRelationshipType ID
        expiry_date: Optional expiry date (NULL = permanent access)
        target_company_id: Company ID to grant access to (for company-wide access when user_id is None)
        
    Returns:
        FormAccessControl entry (created or updated)
        
    Raises:
        ValueError: If validation fails
    """
    # Validate form exists
    form = db.execute(
        select(Form).where(
            Form.FormID == form_id,
            Form.IsDeleted == False
        )
    ).scalar_one_or_none()
    
    if not form:
        raise ValueError(f"Form not found: {form_id}")
    
    # Validate user has Manage access (or is form owner/company admin)
    # For now, check if user is form owner or company admin
    # TODO: Add proper company admin check
    if form.CompanyID != company_id:
        raise ValueError(f"Form does not belong to company: {company_id}")
    
    # For company-wide access, we need to grant access to each user in the target company
    # For now, if user_id is None, we'll use a placeholder approach
    # TODO: Implement proper company-wide access (grant to all users in target_company_id)
    if user_id is None:
        if not target_company_id:
            raise ValueError("Either user_id or target_company_id must be provided")
        # For now, raise an error - company-wide access needs to be implemented
        # by granting access to each user in the company
        raise ValueError("Company-wide access not yet implemented. Please grant access to specific users.")
    
    # Validate user exists
    user = db.execute(
        select(User).where(User.UserID == user_id)
    ).scalar_one_or_none()
    
    if not user:
        raise ValueError(f"User not found: {user_id}")
    
    # Validate access type exists
    access_type = db.execute(
        select(FormAccessControlAccessType).where(
            FormAccessControlAccessType.FormAccessControlAccessTypeID == access_type_id,
            FormAccessControlAccessType.IsDeleted == False,
            FormAccessControlAccessType.IsActive == True
        )
    ).scalar_one_or_none()
    
    if not access_type:
        raise ValueError(f"Invalid access type ID: {access_type_id}")
    
    # Validate relationship type exists
    relationship_type = db.execute(
        select(CompanyRelationshipType).where(
            CompanyRelationshipType.CompanyRelationshipTypeID == relationship_type_id,
            CompanyRelationshipType.IsDeleted == False,
            CompanyRelationshipType.IsActive == True
        )
    ).scalar_one_or_none()
    
    if not relationship_type:
        raise ValueError(f"Invalid relationship type ID: {relationship_type_id}")
    
    # Validate expiry date is after granted date (if provided)
    # Use timezone-aware UTC datetime to match timezone-aware expiry_date from frontend
    granted_date_utc = datetime.now(timezone.utc)
    if expiry_date:
        # Ensure both datetimes are timezone-aware for comparison
        expiry_date_aware = expiry_date
        if expiry_date.tzinfo is None:
            # If expiry_date is naive, assume it's UTC
            expiry_date_aware = expiry_date.replace(tzinfo=timezone.utc)
        # Compare timezone-aware datetimes
        if expiry_date_aware <= granted_date_utc:
            raise ValueError("Expiry date must be after granted date")
    
    # Convert to naive UTC for database storage (SQL Server DATETIME2 doesn't store timezone)
    granted_date_naive = granted_date_utc.replace(tzinfo=None)
    expiry_date_naive = expiry_date.replace(tzinfo=None) if expiry_date and expiry_date.tzinfo else expiry_date
    
    # Check for existing access (duplicate prevention)
    existing_access = db.execute(
        select(FormAccessControl).where(
            FormAccessControl.FormID == form_id,
            FormAccessControl.UserID == user_id,
            FormAccessControl.CompanyID == company_id,
            FormAccessControl.IsDeleted == False
        )
    ).scalar_one_or_none()
    
    if existing_access:
        # Update existing access
        existing_access.FormAccessControlAccessTypeID = access_type_id
        existing_access.CompanyRelationshipTypeID = relationship_type_id
        existing_access.GrantedBy = granted_by
        existing_access.GrantedDate = granted_date_naive
        existing_access.ExpiryDate = expiry_date_naive
        existing_access.UpdatedDate = datetime.now(timezone.utc).replace(tzinfo=None)  # Store as naive UTC
        existing_access.UpdatedBy = granted_by
        
        db.flush()
        
        # Log access update to audit trail
        try:
            # Get updater info
            updater = db.get(User, granted_by)
            updater_display = f"{updater.Email} ({updater.FirstName} {updater.LastName})" if updater else f"User {granted_by}"
            user_display = f"{user.Email} ({user.FirstName} {user.LastName})" if user else f"User {user_id}"
            
            import json
            activity_log = ActivityLog(
                UserID=granted_by,
                CompanyID=company_id,
                Action="form.access.updated",
                EntityType="Form",  # Associate with Form entity for compliance report
                EntityID=form_id,
                NewValue=json.dumps({
                    "details": f"Updated access for {user_display} to {access_type.AccessTypeName}",
                    "updated_for": user_display,
                    "access_type": access_type.AccessTypeName,
                    "updated_by": updater_display
                }),
                CreatedDate=datetime.now(timezone.utc).replace(tzinfo=None)  # Store as naive UTC
            )
            db.add(activity_log)
            db.flush()
        except Exception as e:
            logger.warning(f"Failed to log access update to audit trail: {str(e)}")
        
        logger.info(f"Form access updated: FormID={form_id}, UserID={user_id}, AccessType={access_type.AccessTypeCode}")
        return existing_access
    else:
        # Create new access
        # Use naive UTC datetimes already converted above
        access_control = FormAccessControl(
            FormID=form_id,
            UserID=user_id,
            CompanyID=company_id,
            FormAccessControlAccessTypeID=access_type_id,
            CompanyRelationshipTypeID=relationship_type_id,
            GrantedBy=granted_by,
            GrantedDate=granted_date_naive,
            ExpiryDate=expiry_date_naive,
            CreatedBy=granted_by,
            CreatedDate=datetime.now(timezone.utc).replace(tzinfo=None),  # Store as naive UTC
            IsDeleted=False
        )
        
        db.add(access_control)
        db.flush()
        
        # Log access grant to audit trail
        try:
            # Get granter info
            granter = db.get(User, granted_by)
            granter_display = f"{granter.Email} ({granter.FirstName} {granter.LastName})" if granter else f"User {granted_by}"
            user_display = f"{user.Email} ({user.FirstName} {user.LastName})" if user else f"User {user_id}"
            
            import json
            activity_log = ActivityLog(
                UserID=granted_by,
                CompanyID=company_id,
                Action="form.access.granted",
                EntityType="Form",  # Associate with Form entity for compliance report
                EntityID=form_id,
                NewValue=json.dumps({
                    "details": f"Granted {access_type.AccessTypeName} access to {user_display}",
                    "granted_to": user_display,
                    "access_type": access_type.AccessTypeName,
                    "granted_by": granter_display
                }),
                CreatedDate=datetime.now(timezone.utc).replace(tzinfo=None)  # Store as naive UTC
            )
            db.add(activity_log)
            db.flush()
        except Exception as e:
            logger.warning(f"Failed to log access grant to audit trail: {str(e)}")
        
        logger.info(f"Form access granted: FormID={form_id}, UserID={user_id}, AccessType={access_type.AccessTypeCode}")
        return access_control


async def revoke_access(
    db: Session,
    access_id: int,
    form_id: int,
    revoked_by: int,
    company_id: int
) -> None:
    """
    Revoke access to a form (soft delete).
    
    Args:
        db: Database session
        access_id: FormAccessControl ID
        form_id: Form ID (for validation)
        revoked_by: User ID revoking access (must have Manage access)
        company_id: Company ID (for validation)
        
    Raises:
        ValueError: If access not found or validation fails
    """
    # Get access control entry
    access_control = db.execute(
        select(FormAccessControl).where(
            FormAccessControl.FormAccessControlID == access_id,
            FormAccessControl.FormID == form_id,
            FormAccessControl.IsDeleted == False
        )
    ).scalar_one_or_none()
    
    if not access_control:
        raise ValueError(f"Access control entry not found: {access_id}")
    
    # Validate company ownership
    if access_control.CompanyID != company_id:
        raise ValueError(f"Access control entry does not belong to company: {company_id}")
    
    # Soft delete
    from datetime import timezone
    access_control.IsDeleted = True
    access_control.UpdatedDate = datetime.now(timezone.utc).replace(tzinfo=None)  # Store as naive UTC
    access_control.UpdatedBy = revoked_by
    
    db.flush()
    
    # Log revocation to audit trail
    try:
        import json
        
        # Get user info for better logging
        revoked_user = db.execute(
            select(User).where(User.UserID == access_control.UserID)
        ).scalar_one_or_none()
        revoked_user_display = f"{revoked_user.Email} ({revoked_user.FirstName} {revoked_user.LastName})" if revoked_user else f"User {access_control.UserID}"
        
        # Get revoker info
        revoker = db.get(User, revoked_by)
        revoker_display = f"{revoker.Email} ({revoker.FirstName} {revoker.LastName})" if revoker else f"User {revoked_by}"
        
        activity_log = ActivityLog(
            UserID=revoked_by,
            CompanyID=company_id,
            Action="form.access.revoked",
            EntityType="Form",  # Associate with Form entity for compliance report
            EntityID=form_id,
            NewValue=json.dumps({
                "details": f"Revoked access for {revoked_user_display}",
                "revoked_for": revoked_user_display,
                "revoked_by": revoker_display
            }),
            CreatedDate=datetime.now(timezone.utc).replace(tzinfo=None)  # Store as naive UTC
        )
        db.add(activity_log)
        db.flush()
    except Exception as e:
        logger.warning(f"Failed to log access revocation to audit trail: {str(e)}")
    
    logger.info(f"Form access revoked: FormID={form_id}, AccessID={access_id}")


async def get_form_access_list(
    db: Session,
    form_id: int,
    company_id: int,
    access_type_id: Optional[int] = None
) -> List[FormAccessControl]:
    """
    Get all access control entries for a form.
    
    Args:
        db: Database session
        form_id: Form ID
        company_id: Company ID (for validation)
        access_type_id: Optional filter by access type
        
    Returns:
        List of FormAccessControl entries (including expired for audit trail)
    """
    query = select(FormAccessControl).options(
        joinedload(FormAccessControl.user),
        joinedload(FormAccessControl.company),
        joinedload(FormAccessControl.access_type),
        joinedload(FormAccessControl.relationship_type),
        joinedload(FormAccessControl.granted_by_user)
    ).where(
        FormAccessControl.FormID == form_id,
        FormAccessControl.IsDeleted == False
    )
    
    # Filter by access type if provided
    if access_type_id:
        query = query.where(FormAccessControl.FormAccessControlAccessTypeID == access_type_id)
    
    access_list = db.execute(query).scalars().unique().all()
    
    logger.info(f"Retrieved {len(access_list)} access entries for FormID={form_id}")
    
    return access_list


async def get_user_form_access(
    db: Session,
    form_id: int,
    user_id: int
) -> Optional[Dict[str, Any]]:
    """
    Get user's effective access to a form using centralized database function.
    
    Uses fn_GetUserFormAccess which implements 6-priority access check logic:
    1. System Admin Override → MANAGE
    2. Resource Ownership → MANAGE (form creator)
    3. Explicit FormAccessControl → Use specified access type
    4. Agency Event-Scoped Access → VIEW/EDIT all forms for event
    5. Company Role Default → Default based on company role
    6. No Access → NULL
    
    Args:
        db: Database session
        form_id: Form ID
        user_id: User ID
        
    Returns:
        Dictionary with access information:
        - EffectiveAccessTypeCode: Access type code (MANAGE, EDIT, VIEW, SUBMIT, ANALYZE, or None)
        - CanView: bool
        - CanEdit: bool
        - CanManage: bool
        - CanSubmit: bool
        - CanAnalyze: bool
        - AccessSource: str (system_admin, ownership, explicit_acl, agency_event, company_role, none)
        - AccessReason: str (human-readable explanation)
        Or None if form not found
    """
    try:
        result = db.execute(
            text("""
                SELECT 
                    EffectiveAccessTypeCode,
                    CanView,
                    CanEdit,
                    CanManage,
                    CanSubmit,
                    CanAnalyze,
                    AccessSource,
                    AccessReason
                FROM [dbo].[fn_GetUserFormAccess](:user_id, :form_id)
            """),
            {"user_id": user_id, "form_id": form_id}
        ).fetchone()
        
        if result is None:
            logger.warning(f"Form not found or function returned no result: FormID={form_id}, UserID={user_id}")
            return None
        
        return {
            "EffectiveAccessTypeCode": result.EffectiveAccessTypeCode,
            "CanView": bool(result.CanView),
            "CanEdit": bool(result.CanEdit),
            "CanManage": bool(result.CanManage),
            "CanSubmit": bool(result.CanSubmit),
            "CanAnalyze": bool(result.CanAnalyze),
            "AccessSource": result.AccessSource,
            "AccessReason": result.AccessReason
        }
    except Exception as e:
        error_msg = str(e)
        # Check if function doesn't exist (migration not run)
        if "fn_GetUserFormAccess" in error_msg or "Invalid object name" in error_msg or "Could not find" in error_msg:
            logger.error(f"Database function fn_GetUserFormAccess not found. Migration may not have been run. Error: {error_msg}")
            raise Exception("Database function fn_GetUserFormAccess not found. Please run database migrations (alembic upgrade head).")
        logger.error(f"Error calling fn_GetUserFormAccess: {error_msg}")
        raise


async def check_user_access(
    db: Session,
    form_id: int,
    user_id: int,
    access_type_code: str
) -> bool:
    """
    Check if user has required access type to form.
    
    Uses centralized database function fn_GetUserFormAccess for consistent access checks.
    
    Args:
        db: Database session
        form_id: Form ID
        user_id: User ID
        access_type_code: Access type code (VIEW, EDIT, MANAGE, SUBMIT, ANALYZE)
        
    Returns:
        True if user has access, False otherwise
    """
    access_info = await get_user_form_access(db, form_id, user_id)
    
    if access_info is None:
        return False
    
    # Map access type code to permission flag
    access_type_map = {
        "VIEW": "CanView",
        "EDIT": "CanEdit",
        "MANAGE": "CanManage",
        "SUBMIT": "CanSubmit",
        "ANALYZE": "CanAnalyze"
    }
    
    permission_flag = access_type_map.get(access_type_code.upper())
    if permission_flag:
        return access_info.get(permission_flag, False)
    
    logger.warning(f"Unknown access type code: {access_type_code}")
    return False


async def get_user_access_level(
    db: Session,
    form_id: int,
    user_id: int
) -> Optional[str]:
    """
    Get user's access level to form.
    
    Uses centralized database function fn_GetUserFormAccess.
    Returns effective access type code from the function.
    
    Args:
        db: Database session
        form_id: Form ID
        user_id: User ID
        
    Returns:
        Access type code (MANAGE, EDIT, VIEW, SUBMIT, ANALYZE) or None
    """
    access_info = await get_user_form_access(db, form_id, user_id)
    
    if access_info is None:
        return None
    
    return access_info.get("EffectiveAccessTypeCode")


async def get_user_accessible_forms(
    db: Session,
    user_id: int,
    company_id: int,
    access_type_code: Optional[str] = None
) -> List[Form]:
    """
    Get all forms user has access to (company ownership OR granted access).
    
    Args:
        db: Database session
        user_id: User ID
        company_id: Company ID (for company-owned forms)
        access_type_code: Optional filter by access type
        
    Returns:
        List of Form objects user has access to
    """
    # Get company-owned forms (user has Manage access)
    company_forms_query = select(Form).where(
        Form.CompanyID == company_id,
        Form.IsDeleted == False
    )
    
    # Get forms with granted access
    granted_forms_query = select(Form).join(
        FormAccessControl, Form.FormID == FormAccessControl.FormID
    ).where(
        FormAccessControl.UserID == user_id,
        FormAccessControl.IsDeleted == False,
        or_(
            FormAccessControl.ExpiryDate.is_(None),
            FormAccessControl.ExpiryDate > func.getutcdate()
        ),
        Form.IsDeleted == False
    )
    
    # Filter by access type if provided
    if access_type_code:
        access_type = db.execute(
            select(FormAccessControlAccessType).where(
                FormAccessControlAccessType.AccessTypeCode == access_type_code,
                FormAccessControlAccessType.IsDeleted == False,
                FormAccessControlAccessType.IsActive == True
            )
        ).scalar_one_or_none()
        
        if access_type:
            granted_forms_query = granted_forms_query.where(
                FormAccessControl.FormAccessControlAccessTypeID == access_type.FormAccessControlAccessTypeID
            )
    
    # Combine queries (union)
    company_forms = db.execute(company_forms_query).scalars().all()
    granted_forms = db.execute(granted_forms_query).scalars().all()
    
    # Combine and deduplicate
    all_forms = {form.FormID: form for form in company_forms}
    for form in granted_forms:
        all_forms[form.FormID] = form
    
    forms_list = list(all_forms.values())
    
    logger.info(f"Retrieved {len(forms_list)} accessible forms for UserID={user_id}")
    
    return forms_list

