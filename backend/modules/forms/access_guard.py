"""
Form Access Guard Utilities
Reusable access check functions for form operations
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status

from models.form import Form
from .access_control_service import check_user_access, get_user_access_level, get_user_form_access


async def check_form_access_guard(
    db: Session,
    form_id: int,
    user_id: int,
    required_access: str = "VIEW"
) -> Form:
    """
    Check if user has required access to form, return form if access granted.
    
    Uses centralized database function fn_GetUserFormAccess which implements
    6-priority access check logic including agency event-scoped access.
    
    Args:
        db: Database session
        form_id: Form ID
        user_id: User ID
        required_access: Required access type (VIEW, EDIT, MANAGE, SUBMIT, ANALYZE)
        
    Returns:
        Form object if access granted
        
    Raises:
        HTTPException: 403 Forbidden if access denied, 404 if form not found
    """
    # Get form
    form = db.query(Form).filter(
        Form.FormID == form_id,
        Form.IsDeleted == False
    ).first()
    
    if not form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Form not found: {form_id}"
        )
    
    # Use centralized database function for access check
    # This handles all access types including agency event-scoped access
    has_access = await check_user_access(db, form_id, user_id, required_access)
    
    if not has_access:
        # Get access info for better error message
        access_info = await get_user_form_access(db, form_id, user_id)
        if access_info:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: You have {access_info.get('EffectiveAccessTypeCode', 'no')} access, but {required_access} is required. {access_info.get('AccessReason', '')}"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: You do not have {required_access} access to this form"
            )
    
    return form


async def filter_accessible_forms(
    db: Session,
    forms: List[Form],
    user_id: int,
    company_id: int,
    required_access: str = "VIEW"
) -> List[Form]:
    """
    Filter forms based on user access.
    
    Uses centralized database function fn_GetUserFormAccess which handles:
    - System Admin override
    - Resource ownership
    - Explicit FormAccessControl entries
    - Agency event-scoped access
    - Company role defaults
    
    Args:
        db: Database session
        forms: List of forms to filter
        user_id: User ID
        company_id: Company ID (for context, but access is determined by database function)
        required_access: Required access type (VIEW, EDIT, MANAGE, SUBMIT, ANALYZE)
        
    Returns:
        List of forms user has access to
    """
    accessible_forms = []
    
    for form in forms:
        # Use centralized database function for access check
        # This handles all access scenarios including agency event-scoped access
        has_access = await check_user_access(db, form.FormID, user_id, required_access)
        if has_access:
            accessible_forms.append(form)
    
    return accessible_forms

