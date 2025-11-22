# Form Ownership Transfer - Bulk Transfer Procedure

## Overview

This document defines the stored procedure for bulk ownership transfer of forms when a user is off-boarded from a company. This allows Company Admins to cleanly reassign form ownership without per-form micromanagement.

---

## 1. Ownership Model

### 1.1 Ownership Principles

**Strong but Not Absolute:**
- Form creator gets MANAGE access by default (Resource Ownership - Layer 5)
- Ownership can be reassigned by:
  - **Company Admin** (for their own company)
  - **System Admin** (global override)
- Regular users cannot revoke creator access

**No Per-Form Ownership UI:**
- We will **NOT** manage ownership transfer at individual form level in the UI
- Instead, we support **bulk transfer** at company level via stored procedure

---

## 2. Stored Procedure: `sp_TransferFormOwnership`

### 2.1 Procedure Signature

```sql
CREATE PROCEDURE [dbo].[sp_TransferFormOwnership]
    @FromUserID BIGINT,
    @ToUserID BIGINT,
    @CompanyID BIGINT,
    @PerformedBy BIGINT,
    @Reason NVARCHAR(500) = NULL
AS
```

### 2.2 Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `@FromUserID` | BIGINT | User ID to transfer ownership FROM (off-boarding user) |
| `@ToUserID` | BIGINT | User ID to transfer ownership TO (new owner) |
| `@CompanyID` | BIGINT | Company ID (must match company of both users) |
| `@PerformedBy` | BIGINT | User ID performing the transfer (must be Company Admin or System Admin) |
| `@Reason` | NVARCHAR(500) | Optional reason for transfer (e.g., "Bulk ownership transfer on offboarding") |

### 2.3 Behavior

**1. Validation:**
- Verify `@PerformedBy` has Company Admin privileges for `@CompanyID` OR is System Admin
- Verify `@FromUserID` is a member of `@CompanyID`
- Verify `@ToUserID` is a member of `@CompanyID`
- Verify both users are active and not deleted
- Verify `@FromUserID != @ToUserID`

**2. Ownership Transfer:**
- Update `Form.CreatedBy` from `@FromUserID` to `@ToUserID` for all forms where:
  - `Form.CompanyID = @CompanyID`
  - `Form.CreatedBy = @FromUserID`
  - `Form.IsDeleted = 0`

**3. FormAccessControl Updates (Optional):**
- Update `FormAccessControl.UserID` from `@FromUserID` to `@ToUserID` for:
  - Forms where `Form.CompanyID = @CompanyID`
  - `FormAccessControl.UserID = @FromUserID`
  - `FormAccessControl.IsDeleted = 0`
- This ensures access grants are transferred along with ownership

**4. Audit Trail:**
- Insert records into `audit.ActivityLog` for each form transferred:
  - `Action = 'form.ownership.transferred'`
  - `EntityType = 'Form'`
  - `EntityID = FormID`
  - `OldValue = JSON with old owner details`
  - `NewValue = JSON with new owner details`
  - `ChangedBy = @PerformedBy`
  - `CompanyID = @CompanyID`

### 2.4 Complete Procedure Implementation

```sql
CREATE PROCEDURE [dbo].[sp_TransferFormOwnership]
    @FromUserID BIGINT,
    @ToUserID BIGINT,
    @CompanyID BIGINT,
    @PerformedBy BIGINT,
    @Reason NVARCHAR(500) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRANSACTION;
    
    BEGIN TRY
        -- =====================================================================
        -- VALIDATION
        -- =====================================================================
        
        -- Verify @PerformedBy has Company Admin privileges OR is System Admin
        DECLARE @IsSystemAdmin BIT = 0;
        DECLARE @IsCompanyAdmin BIT = 0;
        
        -- Check if System Admin
        SELECT @IsSystemAdmin = 1
        FROM dbo.User u
        INNER JOIN ref.UserRole ur ON u.UserRoleID = ur.UserRoleID
        WHERE u.UserID = @PerformedBy
          AND u.IsDeleted = 0
          AND ur.RoleCode = 'system_admin';
        
        -- Check if Company Admin
        IF @IsSystemAdmin = 0
        BEGIN
            SELECT @IsCompanyAdmin = 1
            FROM dbo.UserCompany uc
            INNER JOIN ref.UserCompanyRole ucr ON uc.UserCompanyRoleID = ucr.UserCompanyRoleID
            INNER JOIN ref.UserCompanyStatus ucs ON uc.StatusID = ucs.UserCompanyStatusID
            WHERE uc.UserID = @PerformedBy
              AND uc.CompanyID = @CompanyID
              AND uc.IsDeleted = 0
              AND ucs.StatusCode = 'active'
              AND ucr.RoleCode = 'company_admin';
        END
        
        IF @IsSystemAdmin = 0 AND @IsCompanyAdmin = 0
        BEGIN
            RAISERROR('User performing transfer must be Company Admin for the company or System Admin', 16, 1);
            RETURN;
        END
        
        -- Verify @FromUserID is a member of @CompanyID
        IF NOT EXISTS (
            SELECT 1
            FROM dbo.UserCompany uc
            INNER JOIN ref.UserCompanyStatus ucs ON uc.StatusID = ucs.UserCompanyStatusID
            WHERE uc.UserID = @FromUserID
              AND uc.CompanyID = @CompanyID
              AND uc.IsDeleted = 0
              AND ucs.StatusCode = 'active'
        )
        BEGIN
            RAISERROR('FromUserID must be an active member of the specified company', 16, 1);
            RETURN;
        END
        
        -- Verify @ToUserID is a member of @CompanyID
        IF NOT EXISTS (
            SELECT 1
            FROM dbo.UserCompany uc
            INNER JOIN ref.UserCompanyStatus ucs ON uc.StatusID = ucs.UserCompanyStatusID
            WHERE uc.UserID = @ToUserID
              AND uc.CompanyID = @CompanyID
              AND uc.IsDeleted = 0
              AND ucs.StatusCode = 'active'
        )
        BEGIN
            RAISERROR('ToUserID must be an active member of the specified company', 16, 1);
            RETURN;
        END
        
        -- Verify users are not the same
        IF @FromUserID = @ToUserID
        BEGIN
            RAISERROR('FromUserID and ToUserID cannot be the same', 16, 1);
            RETURN;
        END
        
        -- =====================================================================
        -- OWNERSHIP TRANSFER
        -- =====================================================================
        
        DECLARE @FormsTransferred INT = 0;
        DECLARE @AccessControlsTransferred INT = 0;
        
        -- Update Form.CreatedBy
        UPDATE f
        SET f.CreatedBy = @ToUserID,
            f.UpdatedBy = @PerformedBy,
            f.UpdatedDate = GETUTCDATE()
        FROM dbo.Form f
        WHERE f.CompanyID = @CompanyID
          AND f.CreatedBy = @FromUserID
          AND f.IsDeleted = 0;
        
        SET @FormsTransferred = @@ROWCOUNT;
        
        -- Update FormAccessControl.UserID (transfer access grants)
        UPDATE fac
        SET fac.UserID = @ToUserID,
            fac.UpdatedBy = @PerformedBy,
            fac.UpdatedDate = GETUTCDATE()
        FROM dbo.FormAccessControl fac
        INNER JOIN dbo.Form f ON fac.FormID = f.FormID
        WHERE f.CompanyID = @CompanyID
          AND fac.UserID = @FromUserID
          AND fac.IsDeleted = 0;
        
        SET @AccessControlsTransferred = @@ROWCOUNT;
        
        -- =====================================================================
        -- AUDIT TRAIL
        -- =====================================================================
        
        -- Get user details for audit
        DECLARE @FromUserEmail NVARCHAR(255);
        DECLARE @ToUserEmail NVARCHAR(255);
        DECLARE @PerformedByEmail NVARCHAR(255);
        
        SELECT @FromUserEmail = Email FROM dbo.User WHERE UserID = @FromUserID;
        SELECT @ToUserEmail = Email FROM dbo.User WHERE UserID = @ToUserID;
        SELECT @PerformedByEmail = Email FROM dbo.User WHERE UserID = @PerformedBy;
        
        -- Insert audit records for each transferred form
        INSERT INTO audit.ActivityLog (
            UserID,
            CompanyID,
            Action,
            EntityType,
            EntityID,
            OldValue,
            NewValue,
            ChangedBy,
            ChangedByEmail,
            CreatedDate
        )
        SELECT
            @FromUserID,
            @CompanyID,
            'form.ownership.transferred',
            'Form',
            f.FormID,
            JSON_OBJECT(
                'old_owner_id': @FromUserID,
                'old_owner_email': @FromUserEmail,
                'form_id': f.FormID,
                'form_name': f.FormName
            ),
            JSON_OBJECT(
                'new_owner_id': @ToUserID,
                'new_owner_email': @ToUserEmail,
                'form_id': f.FormID,
                'form_name': f.FormName,
                'transferred_by': @PerformedBy,
                'transferred_by_email': @PerformedByEmail,
                'reason': ISNULL(@Reason, 'Bulk ownership transfer on offboarding'),
                'transferred_at': GETUTCDATE()
            ),
            @PerformedBy,
            @PerformedByEmail,
            GETUTCDATE()
        FROM dbo.Form f
        WHERE f.CompanyID = @CompanyID
          AND f.CreatedBy = @ToUserID  -- Now owned by new user
          AND f.UpdatedBy = @PerformedBy  -- Just updated by this procedure
          AND f.UpdatedDate >= DATEADD(SECOND, -5, GETUTCDATE());  -- Within last 5 seconds
        
        -- =====================================================================
        -- SUCCESS
        -- =====================================================================
        
        COMMIT TRANSACTION;
        
        SELECT 
            @FormsTransferred AS FormsTransferred,
            @AccessControlsTransferred AS AccessControlsTransferred,
            'SUCCESS' AS Status,
            'Ownership transfer completed successfully' AS Message;
        
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
        
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        DECLARE @ErrorSeverity INT = ERROR_SEVERITY();
        DECLARE @ErrorState INT = ERROR_STATE();
        
        RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState);
    END CATCH
END;
GO
```

### 2.5 Usage Example

```sql
-- Company Admin off-boarding a user and transferring all their forms to another user
EXEC [dbo].[sp_TransferFormOwnership]
    @FromUserID = 123,           -- User being off-boarded
    @ToUserID = 456,             -- New owner
    @CompanyID = 789,            -- Company ID
    @PerformedBy = 100,          -- Company Admin performing transfer
    @Reason = 'Bulk ownership transfer on offboarding - user leaving company';
```

### 2.6 Guardrails

**Security Checks:**
- ✅ Only Company Admin (for the company) or System Admin can execute
- ✅ Both users must be active members of the same company
- ✅ Users cannot be the same
- ✅ Only non-deleted forms are transferred

**Data Integrity:**
- ✅ Transaction ensures atomicity (all or nothing)
- ✅ Audit trail captures all changes
- ✅ FormAccessControl entries are transferred along with ownership
- ✅ Updated timestamps track when transfer occurred

**Error Handling:**
- ✅ Comprehensive validation before any changes
- ✅ Transaction rollback on error
- ✅ Clear error messages for debugging

---

## 3. Backend Integration

### 3.1 Service Method

**File:** `backend/modules/forms/ownership_service.py`

```python
"""
Form Ownership Transfer Service
"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict, Any
from common.logger import get_logger

logger = get_logger(__name__)


async def transfer_form_ownership(
    db: Session,
    from_user_id: int,
    to_user_id: int,
    company_id: int,
    performed_by: int,
    reason: str = None
) -> Dict[str, Any]:
    """
    Transfer form ownership from one user to another (bulk transfer).
    
    Args:
        db: Database session
        from_user_id: User ID to transfer ownership FROM
        to_user_id: User ID to transfer ownership TO
        company_id: Company ID (both users must belong to this company)
        performed_by: User ID performing the transfer (must be Company Admin or System Admin)
        reason: Optional reason for transfer
        
    Returns:
        Dict with transfer results:
        - forms_transferred: Number of forms transferred
        - access_controls_transferred: Number of access control entries transferred
        - status: 'SUCCESS' or 'ERROR'
        - message: Status message
        
    Raises:
        ValueError: If validation fails
        Exception: If stored procedure fails
    """
    try:
        # Call stored procedure
        result = db.execute(
            text("""
                EXEC [dbo].[sp_TransferFormOwnership]
                    @FromUserID = :from_user_id,
                    @ToUserID = :to_user_id,
                    @CompanyID = :company_id,
                    @PerformedBy = :performed_by,
                    @Reason = :reason
            """),
            {
                'from_user_id': from_user_id,
                'to_user_id': to_user_id,
                'company_id': company_id,
                'performed_by': performed_by,
                'reason': reason or 'Bulk ownership transfer on offboarding'
            }
        ).fetchone()
        
        db.commit()
        
        logger.info(
            f"Form ownership transferred: FromUserID={from_user_id}, "
            f"ToUserID={to_user_id}, CompanyID={company_id}, "
            f"FormsTransferred={result.FormsTransferred}, "
            f"AccessControlsTransferred={result.AccessControlsTransferred}"
        )
        
        return {
            'forms_transferred': result.FormsTransferred,
            'access_controls_transferred': result.AccessControlsTransferred,
            'status': result.Status,
            'message': result.Message
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Form ownership transfer failed: {str(e)}", exc_info=True)
        raise
```

### 3.2 API Endpoint

**File:** `backend/modules/forms/ownership_router.py`

```python
"""
Form Ownership Transfer Router
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional

from common.database import get_db
from modules.auth.dependencies import get_current_user
from modules.auth.models import CurrentUser
from common.rbac import require_company_admin_for_company
from .ownership_service import transfer_form_ownership
from common.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/forms", tags=["forms"])


class TransferOwnershipRequest(BaseModel):
    """Request schema for form ownership transfer"""
    from_user_id: int = Field(..., description="User ID to transfer ownership FROM")
    to_user_id: int = Field(..., description="User ID to transfer ownership TO")
    company_id: int = Field(..., description="Company ID (both users must belong to this company)")
    reason: Optional[str] = Field(None, description="Optional reason for transfer")


@router.post(
    "/transfer-ownership",
    status_code=status.HTTP_200_OK,
    summary="Transfer form ownership (bulk)",
    description="Transfer ownership of all forms from one user to another (Company Admin only)"
)
async def transfer_form_ownership_endpoint(
    request: TransferOwnershipRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Transfer form ownership from one user to another (bulk transfer).
    
    Requires Company Admin privileges for the specified company.
    """
    try:
        # Verify user is Company Admin for the company (or System Admin)
        require_company_admin_for_company(current_user, request.company_id)
        
        # Transfer ownership
        result = await transfer_form_ownership(
            db=db,
            from_user_id=request.from_user_id,
            to_user_id=request.to_user_id,
            company_id=request.company_id,
            performed_by=current_user.user_id,
            reason=request.reason
        )
        
        return result
        
    except ValueError as e:
        logger.warning(f"Form ownership transfer validation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Form ownership transfer failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to transfer form ownership"
        )
```

---

## 4. Testing Scenarios

### 4.1 Successful Transfer

**Scenario:** Company Admin transfers all forms from User A to User B

**Steps:**
1. User A has 5 forms in Company X
2. Company Admin calls transfer procedure
3. All 5 forms now have `CreatedBy = User B`
4. FormAccessControl entries for User A are transferred to User B
5. Audit records created for each form

**Expected Result:**
- ✅ All forms transferred
- ✅ Access control entries transferred
- ✅ Audit trail complete
- ✅ User B now has MANAGE access to all transferred forms

### 4.2 Validation Failures

**Scenario 1:** Non-admin user tries to transfer
- **Expected:** Error - "User performing transfer must be Company Admin"

**Scenario 2:** Users from different companies
- **Expected:** Error - "ToUserID must be an active member of the specified company"

**Scenario 3:** Same user for from/to
- **Expected:** Error - "FromUserID and ToUserID cannot be the same"

### 4.3 Partial Transfer

**Scenario:** User A has forms in Company X and Company Y
- Transfer only for Company X
- **Expected:** Only Company X forms transferred, Company Y forms unchanged

---

## 5. Migration Requirements

### 5.1 Database Migration

**File:** `backend/migrations/versions/025_add_form_ownership_transfer_procedure.py`

**Changes:**
1. Create `sp_TransferFormOwnership` stored procedure
2. Add appropriate indexes for performance
3. Grant execute permissions to appropriate roles

### 5.2 Backend Implementation

**Files:**
1. `backend/modules/forms/ownership_service.py` - Service layer
2. `backend/modules/forms/ownership_router.py` - API endpoints
3. Update `backend/main.py` to register router

---

## 6. Summary

### Key Features

1. **Bulk Transfer:** Transfer all forms from one user to another in a single operation
2. **Access Control Transfer:** FormAccessControl entries are transferred along with ownership
3. **Audit Trail:** Complete audit log of all ownership transfers
4. **Security:** Only Company Admin or System Admin can perform transfers
5. **Validation:** Comprehensive validation before any changes
6. **Transaction Safety:** Atomic operation (all or nothing)

### Benefits

- ✅ **Clean Off-boarding:** Easy to transfer ownership when users leave
- ✅ **No Per-Form Management:** Bulk operation, no UI needed
- ✅ **Auditable:** Complete audit trail for compliance
- ✅ **Secure:** Database-enforced permissions
- ✅ **Flexible:** Can be called from API or directly from database

This procedure provides a clean, secure way to handle form ownership transfer during user off-boarding.

