# Centralized Form Access Logic - Database Function

## Overview

This document defines the table-valued function that centralizes all form access logic in the database. This ensures consistent access checks across all backend services and prevents logic duplication or divergence.

---

## 1. Function: `fn_GetUserFormAccess`

### 1.1 Function Signature

```sql
CREATE FUNCTION [dbo].[fn_GetUserFormAccess]
(
    @UserID BIGINT,
    @FormID BIGINT
)
RETURNS TABLE
AS
RETURN
(
    -- Returns single row with effective access information
    SELECT
        @UserID AS UserID,
        @FormID AS FormID,
        EffectiveAccessTypeID INT,
        EffectiveAccessTypeCode VARCHAR(20),
        CanView BIT,
        CanSubmit BIT,
        CanAnalyze BIT,
        CanEdit BIT,
        CanManage BIT,
        AccessSource VARCHAR(50),  -- 'system_admin', 'ownership', 'explicit_acl', 'agency_event', 'company_role', 'none'
        AccessReason NVARCHAR(500)  -- Human-readable explanation
)
```

### 1.2 Return Columns

| Column | Type | Description |
|--------|------|-------------|
| `UserID` | BIGINT | User ID (input parameter) |
| `FormID` | BIGINT | Form ID (input parameter) |
| `EffectiveAccessTypeID` | INT | Effective access type ID (from ref.FormAccessControlAccessType) |
| `EffectiveAccessTypeCode` | VARCHAR(20) | Effective access type code ('MANAGE', 'EDIT', 'ANALYZE', 'SUBMIT', 'VIEW', or NULL) |
| `CanView` | BIT | Can user view the form? |
| `CanSubmit` | BIT | Can user submit responses? |
| `CanAnalyze` | BIT | Can user view analytics? |
| `CanEdit` | BIT | Can user edit the form? |
| `CanManage` | BIT | Can user manage the form (delete, grant access)? |
| `AccessSource` | VARCHAR(50) | Source of access ('system_admin', 'ownership', 'explicit_acl', 'agency_event', 'company_role', 'none') |
| `AccessReason` | NVARCHAR(500) | Human-readable explanation of access source |

### 1.3 Access Check Priority

The function implements the following priority order:

1. **System Admin Override** → MANAGE (all forms, all companies)
2. **Resource Ownership** → MANAGE (form creator)
3. **Explicit FormAccessControl** → Use specified access type
4. **Agency Event-Scoped Access** → VIEW/EDIT all forms for event (if `agency_form_builder` role)
5. **Company Role Default** → Default based on company role
6. **No Access** → NULL (requires explicit FormAccessControl entry)

---

## 2. Complete Function Implementation

```sql
CREATE FUNCTION [dbo].[fn_GetUserFormAccess]
(
    @UserID BIGINT,
    @FormID BIGINT
)
RETURNS TABLE
AS
RETURN
(
    WITH AccessCheck AS (
        SELECT
            @UserID AS UserID,
            @FormID AS FormID,
            -- Get form details
            f.CompanyID AS FormCompanyID,
            f.EventID AS FormEventID,
            f.CreatedBy AS FormCreatedBy,
            -- Get user system role
            ur.RoleCode AS UserSystemRole,
            -- Get user company role for form's company
            ucr.RoleCode AS UserCompanyRole,
            ucr.CanManageForms AS UserCanManageForms,
            ucr.CanViewReports AS UserCanViewReports,
            -- Check explicit FormAccessControl
            fac.FormAccessControlAccessTypeID AS ExplicitAccessTypeID,
            facat.AccessTypeCode AS ExplicitAccessTypeCode,
            -- Check agency event-scoped access
            ecr.HasViewAllFormsForEvent AS AgencyHasViewAllForms,
            ecr.HasEditAllFormsForEvent AS AgencyHasEditAllForms,
            -- Agency company ID (if applicable)
            ec.CompanyID AS AgencyCompanyID
        FROM dbo.Form f
        -- Get user system role
        LEFT JOIN dbo.User u ON u.UserID = @UserID AND u.IsDeleted = 0
        LEFT JOIN ref.UserRole ur ON u.UserRoleID = ur.UserRoleID
        -- Get user company role for form's company
        LEFT JOIN dbo.UserCompany uc ON uc.UserID = @UserID 
            AND uc.CompanyID = f.CompanyID 
            AND uc.IsDeleted = 0
        LEFT JOIN ref.UserCompanyStatus ucs ON uc.StatusID = ucs.UserCompanyStatusID 
            AND ucs.StatusCode = 'active'
        LEFT JOIN ref.UserCompanyRole ucr ON uc.UserCompanyRoleID = ucr.UserCompanyRoleID
        -- Check explicit FormAccessControl
        LEFT JOIN dbo.FormAccessControl fac ON fac.FormID = f.FormID 
            AND fac.UserID = @UserID 
            AND fac.IsDeleted = 0
        LEFT JOIN ref.FormAccessControlAccessType facat ON fac.FormAccessControlAccessTypeID = facat.FormAccessControlAccessTypeID
        -- Check agency event-scoped access
        LEFT JOIN dbo.UserCompany uc_agency ON uc_agency.UserID = @UserID 
            AND uc_agency.IsDeleted = 0
        LEFT JOIN ref.UserCompanyStatus ucs_agency ON uc_agency.StatusID = ucs_agency.UserCompanyStatusID 
            AND ucs_agency.StatusCode = 'active'
        LEFT JOIN dbo.EventCompany ec ON ec.EventID = f.EventID 
            AND ec.CompanyID = uc_agency.CompanyID 
            AND ec.IsDeleted = 0 
            AND ec.IsActive = 1
        LEFT JOIN ref.EventCompanyRole ecr ON ec.EventCompanyRoleID = ecr.EventCompanyRoleID
        WHERE f.FormID = @FormID 
          AND f.IsDeleted = 0
    )
    SELECT
        UserID,
        FormID,
        -- Determine effective access type
        CASE
            -- Priority 1: System Admin Override
            WHEN UserSystemRole = 'system_admin' THEN
                (SELECT FormAccessControlAccessTypeID FROM ref.FormAccessControlAccessType WHERE AccessTypeCode = 'MANAGE')
            
            -- Priority 2: Resource Ownership
            WHEN FormCreatedBy = UserID THEN
                (SELECT FormAccessControlAccessTypeID FROM ref.FormAccessControlAccessType WHERE AccessTypeCode = 'MANAGE')
            
            -- Priority 3: Explicit FormAccessControl
            WHEN ExplicitAccessTypeID IS NOT NULL THEN
                ExplicitAccessTypeID
            
            -- Priority 4: Agency Event-Scoped Access
            WHEN AgencyHasEditAllForms = 1 THEN
                (SELECT FormAccessControlAccessTypeID FROM ref.FormAccessControlAccessType WHERE AccessTypeCode = 'EDIT')
            WHEN AgencyHasViewAllForms = 1 THEN
                (SELECT FormAccessControlAccessTypeID FROM ref.FormAccessControlAccessType WHERE AccessTypeCode = 'VIEW')
            
            -- Priority 5: Company Role Default
            WHEN UserCompanyRole = 'company_admin' THEN
                (SELECT FormAccessControlAccessTypeID FROM ref.FormAccessControlAccessType WHERE AccessTypeCode = 'MANAGE')
            WHEN UserCompanyRole = 'company_user' THEN
                (SELECT FormAccessControlAccessTypeID FROM ref.FormAccessControlAccessType WHERE AccessTypeCode = 'VIEW')
            WHEN UserCompanyRole = 'company_viewer' THEN
                (SELECT FormAccessControlAccessTypeID FROM ref.FormAccessControlAccessType WHERE AccessTypeCode = 'VIEW')
            
            -- Priority 6: No Access
            ELSE NULL
        END AS EffectiveAccessTypeID,
        
        CASE
            WHEN UserSystemRole = 'system_admin' THEN 'MANAGE'
            WHEN FormCreatedBy = UserID THEN 'MANAGE'
            WHEN ExplicitAccessTypeCode IS NOT NULL THEN ExplicitAccessTypeCode
            WHEN AgencyHasEditAllForms = 1 THEN 'EDIT'
            WHEN AgencyHasViewAllForms = 1 THEN 'VIEW'
            WHEN UserCompanyRole = 'company_admin' THEN 'MANAGE'
            WHEN UserCompanyRole = 'company_user' THEN 'VIEW'
            WHEN UserCompanyRole = 'company_viewer' THEN 'VIEW'
            ELSE NULL
        END AS EffectiveAccessTypeCode,
        
        -- Permission flags (based on effective access type)
        CASE
            WHEN UserSystemRole = 'system_admin' THEN 1
            WHEN FormCreatedBy = UserID THEN 1
            WHEN ExplicitAccessTypeCode IS NOT NULL THEN 
                CASE WHEN ExplicitAccessTypeCode IN ('VIEW', 'SUBMIT', 'ANALYZE', 'EDIT', 'MANAGE') THEN 1 ELSE 0 END
            WHEN AgencyHasEditAllForms = 1 THEN 1
            WHEN AgencyHasViewAllForms = 1 THEN 1
            WHEN UserCompanyRole = 'company_admin' THEN 1
            WHEN UserCompanyRole = 'company_user' THEN 1
            WHEN UserCompanyRole = 'company_viewer' THEN 1
            ELSE 0
        END AS CanView,
        
        CASE
            WHEN UserSystemRole = 'system_admin' THEN 1
            WHEN FormCreatedBy = UserID THEN 1
            WHEN ExplicitAccessTypeCode IN ('SUBMIT', 'MANAGE') THEN 1
            WHEN UserCompanyRole = 'company_admin' THEN 1
            ELSE 0
        END AS CanSubmit,
        
        CASE
            WHEN UserSystemRole = 'system_admin' THEN 1
            WHEN FormCreatedBy = UserID THEN 1
            WHEN ExplicitAccessTypeCode IN ('ANALYZE', 'MANAGE') AND UserCanViewReports = 1 THEN 1
            WHEN UserCompanyRole = 'company_admin' AND UserCanViewReports = 1 THEN 1
            WHEN UserCompanyRole = 'company_user' AND UserCanViewReports = 1 THEN 1
            ELSE 0
        END AS CanAnalyze,
        
        CASE
            WHEN UserSystemRole = 'system_admin' THEN 1
            WHEN FormCreatedBy = UserID THEN 1
            WHEN ExplicitAccessTypeCode IN ('EDIT', 'MANAGE') AND UserCanManageForms = 1 THEN 1
            WHEN AgencyHasEditAllForms = 1 THEN 1
            WHEN UserCompanyRole = 'company_admin' AND UserCanManageForms = 1 THEN 1
            ELSE 0
        END AS CanEdit,
        
        CASE
            WHEN UserSystemRole = 'system_admin' THEN 1
            WHEN FormCreatedBy = UserID THEN 1
            WHEN ExplicitAccessTypeCode = 'MANAGE' AND UserCanManageForms = 1 THEN 1
            WHEN UserCompanyRole = 'company_admin' AND UserCanManageForms = 1 THEN 1
            ELSE 0
        END AS CanManage,
        
        -- Access source
        CASE
            WHEN UserSystemRole = 'system_admin' THEN 'system_admin'
            WHEN FormCreatedBy = UserID THEN 'ownership'
            WHEN ExplicitAccessTypeCode IS NOT NULL THEN 'explicit_acl'
            WHEN AgencyHasEditAllForms = 1 OR AgencyHasViewAllForms = 1 THEN 'agency_event'
            WHEN UserCompanyRole IS NOT NULL THEN 'company_role'
            ELSE 'none'
        END AS AccessSource,
        
        -- Access reason
        CASE
            WHEN UserSystemRole = 'system_admin' THEN 'System Administrator - full platform access'
            WHEN FormCreatedBy = UserID THEN 'Form owner (creator) - full access to own forms'
            WHEN ExplicitAccessTypeCode IS NOT NULL THEN 
                'Explicit access control entry: ' + ExplicitAccessTypeCode
            WHEN AgencyHasEditAllForms = 1 THEN 
                'Agency event-scoped access: EDIT all forms for event (agency_form_builder role)'
            WHEN AgencyHasViewAllForms = 1 THEN 
                'Agency event-scoped access: VIEW all forms for event (agency_form_builder role)'
            WHEN UserCompanyRole = 'company_admin' THEN 
                'Company Administrator - default MANAGE access to all company forms'
            WHEN UserCompanyRole = 'company_user' THEN 
                'Company User - default VIEW access to all company forms'
            WHEN UserCompanyRole = 'company_viewer' THEN 
                'Company Viewer - default VIEW access to all company forms'
            ELSE 'No access - user is not a member of the form''s company and has no explicit access grant'
        END AS AccessReason
        
    FROM AccessCheck
);
GO
```

---

## 3. Usage Examples

### 3.1 Basic Usage

```sql
-- Get user's access to a specific form
SELECT * FROM [dbo].[fn_GetUserFormAccess](@UserID, @FormID);
```

### 3.2 Check Specific Permission

```sql
-- Check if user can edit a form
SELECT CanEdit 
FROM [dbo].[fn_GetUserFormAccess](@UserID, @FormID);
```

### 3.3 Get Access for Multiple Forms

```sql
-- Get access for all forms in an event
SELECT 
    f.FormID,
    f.FormName,
    a.*
FROM dbo.Form f
CROSS APPLY [dbo].[fn_GetUserFormAccess](@UserID, f.FormID) a
WHERE f.EventID = @EventID
  AND f.IsDeleted = 0;
```

### 3.4 Filter Forms by Access Level

```sql
-- Get all forms user can edit
SELECT 
    f.FormID,
    f.FormName,
    a.EffectiveAccessTypeCode,
    a.AccessSource
FROM dbo.Form f
CROSS APPLY [dbo].[fn_GetUserFormAccess](@UserID, f.FormID) a
WHERE a.CanEdit = 1
  AND f.IsDeleted = 0;
```

---

## 4. Backend Integration

### 4.1 Service Method

**File:** `backend/modules/forms/access_control_service.py`

```python
"""
Form Access Control Service - Updated to use database function
"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, Dict, Any
from common.logger import get_logger

logger = get_logger(__name__)


async def get_user_form_access(
    db: Session,
    user_id: int,
    form_id: int
) -> Optional[Dict[str, Any]]:
    """
    Get user's effective access to a form using centralized database function.
    
    Args:
        db: Database session
        user_id: User ID
        form_id: Form ID
        
    Returns:
        Dict with access information:
        - effective_access_type_id: Access type ID
        - effective_access_type_code: Access type code ('MANAGE', 'EDIT', etc.)
        - can_view: Can user view the form?
        - can_submit: Can user submit responses?
        - can_analyze: Can user view analytics?
        - can_edit: Can user edit the form?
        - can_manage: Can user manage the form?
        - access_source: Source of access ('system_admin', 'ownership', etc.)
        - access_reason: Human-readable explanation
        
    Returns None if form not found or user has no access.
    """
    try:
        result = db.execute(
            text("""
                SELECT 
                    EffectiveAccessTypeID,
                    EffectiveAccessTypeCode,
                    CanView,
                    CanSubmit,
                    CanAnalyze,
                    CanEdit,
                    CanManage,
                    AccessSource,
                    AccessReason
                FROM [dbo].[fn_GetUserFormAccess](:user_id, :form_id)
            """),
            {'user_id': user_id, 'form_id': form_id}
        ).fetchone()
        
        if not result or result.EffectiveAccessTypeCode is None:
            return None
        
        return {
            'effective_access_type_id': result.EffectiveAccessTypeID,
            'effective_access_type_code': result.EffectiveAccessTypeCode,
            'can_view': bool(result.CanView),
            'can_submit': bool(result.CanSubmit),
            'can_analyze': bool(result.CanAnalyze),
            'can_edit': bool(result.CanEdit),
            'can_manage': bool(result.CanManage),
            'access_source': result.AccessSource,
            'access_reason': result.AccessReason
        }
        
    except Exception as e:
        logger.error(f"Error getting user form access: {str(e)}", exc_info=True)
        raise


async def check_user_can_edit_form(
    db: Session,
    user_id: int,
    form_id: int
) -> bool:
    """
    Check if user can edit a form.
    
    Args:
        db: Database session
        user_id: User ID
        form_id: Form ID
        
    Returns:
        True if user can edit, False otherwise
    """
    access = await get_user_form_access(db, user_id, form_id)
    return access is not None and access.get('can_edit', False)


async def check_user_can_manage_form(
    db: Session,
    user_id: int,
    form_id: int
) -> bool:
    """
    Check if user can manage a form (delete, grant access).
    
    Args:
        db: Database session
        user_id: User ID
        form_id: Form ID
        
    Returns:
        True if user can manage, False otherwise
    """
    access = await get_user_form_access(db, user_id, form_id)
    return access is not None and access.get('can_manage', False)
```

### 4.2 Access Guard Decorator

**File:** `backend/modules/forms/access_guard.py`

```python
"""
Form Access Guard - Enforces access control using database function
"""
from functools import wraps
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import Callable, List
from modules.forms.access_control_service import get_user_form_access
from common.logger import get_logger

logger = get_logger(__name__)


def require_form_access(
    required_permission: str,  # 'view', 'submit', 'analyze', 'edit', 'manage'
    form_id_param: str = 'form_id'  # Parameter name for form_id in route
):
    """
    Decorator to require specific form access permission.
    
    Usage:
        @router.get("/forms/{form_id}")
        @require_form_access('edit')
        async def edit_form(form_id: int, ...):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get form_id from kwargs
            form_id = kwargs.get(form_id_param)
            if not form_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Form ID parameter '{form_id_param}' not found"
                )
            
            # Get current_user and db from dependencies
            current_user = kwargs.get('current_user')
            db = kwargs.get('db')
            
            if not current_user or not db:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Missing current_user or db dependency"
                )
            
            # Get user's access to form
            access = await get_user_form_access(
                db=db,
                user_id=current_user.user_id,
                form_id=form_id
            )
            
            if not access:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have access to this form"
                )
            
            # Check required permission
            permission_map = {
                'view': 'can_view',
                'submit': 'can_submit',
                'analyze': 'can_analyze',
                'edit': 'can_edit',
                'manage': 'can_manage'
            }
            
            permission_flag = permission_map.get(required_permission.lower())
            if not permission_flag or not access.get(permission_flag, False):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"You do not have {required_permission.upper()} permission for this form. "
                           f"Current access: {access.get('effective_access_type_code', 'NONE')}"
                )
            
            # Add access info to kwargs for use in handler
            kwargs['form_access'] = access
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator
```

---

## 5. Performance Considerations

### 5.1 Indexing

**Recommended indexes for performance:**

```sql
-- Form table
CREATE INDEX IX_Form_CompanyID_IsDeleted ON dbo.Form(CompanyID, IsDeleted);
CREATE INDEX IX_Form_EventID_IsDeleted ON dbo.Form(EventID, IsDeleted);
CREATE INDEX IX_Form_CreatedBy_IsDeleted ON dbo.Form(CreatedBy, IsDeleted);

-- FormAccessControl table
CREATE INDEX IX_FormAccessControl_UserID_FormID_IsDeleted 
ON dbo.FormAccessControl(UserID, FormID, IsDeleted);

-- EventCompany table
CREATE INDEX IX_EventCompany_EventID_CompanyID_IsActive_IsDeleted 
ON dbo.EventCompany(EventID, CompanyID, IsActive, IsDeleted);

-- UserCompany table
CREATE INDEX IX_UserCompany_UserID_CompanyID_StatusID_IsDeleted 
ON dbo.UserCompany(UserID, CompanyID, StatusID, IsDeleted);
```

### 5.2 Caching Considerations

**Backend caching strategy:**
- Cache access results for short duration (e.g., 5 minutes)
- Invalidate cache on:
  - FormAccessControl changes
  - UserCompany role changes
  - EventCompany changes
  - Form ownership transfers

---

## 6. Testing

### 6.1 Unit Tests

**Test scenarios:**
1. System Admin access (should return MANAGE)
2. Form owner access (should return MANAGE)
3. Explicit ACL access (should return specified type)
4. Agency event-scoped access (should return VIEW/EDIT)
5. Company role default access (should return based on role)
6. No access (should return NULL)

### 6.2 Integration Tests

**Test scenarios:**
1. Access check for multiple forms
2. Access check with expired ACL entries
3. Access check with inactive EventCompany entries
4. Access check with company permission constraints

---

## 7. Migration Requirements

### 7.1 Database Migration

**File:** `backend/migrations/versions/026_add_form_access_function.py`

**Changes:**
1. Create `fn_GetUserFormAccess` function
2. Create recommended indexes
3. Grant execute permissions

### 7.2 Backend Updates

**Files:**
1. Update `backend/modules/forms/access_control_service.py` to use function
2. Update `backend/modules/forms/access_guard.py` to use function
3. Update all form endpoints to use new access checking

---

## 8. Summary

### Key Benefits

1. **Centralized Logic:** All access checks in one place (database function)
2. **Consistency:** Same logic used everywhere (backend services, API endpoints)
3. **Performance:** Database-level optimization with proper indexes
4. **Maintainability:** Single source of truth for access rules
5. **Auditability:** Access source and reason tracked for debugging

### Access Check Priority

1. System Admin → MANAGE
2. Resource Ownership → MANAGE
3. Explicit FormAccessControl → Specified type
4. Agency Event-Scoped Access → VIEW/EDIT (if applicable)
5. Company Role Default → Based on role
6. No Access → NULL

This function provides a single, authoritative source for form access logic that can be used consistently across all backend services.

