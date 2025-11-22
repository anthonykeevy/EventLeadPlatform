# Access Control Implementation Plan

## Overview

This document provides the implementation plan for the updated access control model, including agency/outsourced form-building, ownership transfer, and centralized database access logic.

---

## 1. Database Schema Changes

### 1.1 Add Agency Form Builder Role

**Migration:** `backend/migrations/versions/024_add_agency_form_builder_role.py`

**Changes:**
1. Add `HasViewAllFormsForEvent` column to `ref.EventCompanyRole`
2. Add `HasEditAllFormsForEvent` column to `ref.EventCompanyRole`
3. Insert `agency_form_builder` role seed data
4. Update existing roles to set new columns to `0`
5. Create index for performance

**SQL:**
```sql
-- Add columns
ALTER TABLE [ref].[EventCompanyRole]
ADD HasViewAllFormsForEvent BIT NOT NULL DEFAULT 0,
    HasEditAllFormsForEvent BIT NOT NULL DEFAULT 0;

-- Create index
CREATE INDEX IX_EventCompanyRole_FormAccess 
ON [ref].[EventCompanyRole](HasViewAllFormsForEvent, HasEditAllFormsForEvent)
WHERE HasViewAllFormsForEvent = 1 OR HasEditAllFormsForEvent = 1;

-- Insert agency role
INSERT INTO [ref].[EventCompanyRole] (
    RoleCode, RoleName, Description, RoleLevel,
    HasEditEvent, HasDeleteEvent, HasManageParticipants, HasViewEvent,
    HasViewAllFormsForEvent, HasEditAllFormsForEvent,
    IsActive, SortOrder, CreatedBy
) VALUES (
    'agency_form_builder',
    'Agency Form Builder',
    'External agency company working on forms for a specific event. Read-only event access, but can view and edit all forms associated with the event. Forms remain owned by host company.',
    25,
    0, 0, 0, 1,  -- Event management: read-only
    1, 1,        -- Form access: view and edit all forms for event
    1, 4, 1
);
```

---

### 1.2 Create Ownership Transfer Stored Procedure

**Migration:** `backend/migrations/versions/025_add_form_ownership_transfer_procedure.py`

**Changes:**
1. Create `sp_TransferFormOwnership` stored procedure
2. Grant execute permissions to appropriate roles

**See:** `docs/ACCESS-CONTROL-OWNERSHIP-TRANSFER.md` for complete procedure implementation.

---

### 1.3 Create Centralized Access Function

**Migration:** `backend/migrations/versions/026_add_form_access_function.py`

**Changes:**
1. Create `fn_GetUserFormAccess` table-valued function
2. Create recommended indexes for performance
3. Grant execute permissions

**See:** `docs/ACCESS-CONTROL-DATABASE-FUNCTION.md` for complete function implementation.

---

## 2. Backend Model Updates

### 2.1 EventCompanyRole Model

**File:** `backend/models/ref/event_company_role.py`

**Changes:**
```python
# Add new columns
HasViewAllFormsForEvent = Column(Boolean, nullable=False, default=False)
HasEditAllFormsForEvent = Column(Boolean, nullable=False, default=False)
```

### 2.2 Access Control Service

**File:** `backend/modules/forms/access_control_service.py`

**Changes:**
1. Update `get_user_form_access` to use `[dbo].[fn_GetUserFormAccess]` function
2. Remove duplicate access check logic (now in database)
3. Add agency access check support

**See:** `docs/ACCESS-CONTROL-DATABASE-FUNCTION.md` for implementation.

### 2.3 Ownership Service

**File:** `backend/modules/forms/ownership_service.py` (NEW)

**Changes:**
1. Create service for form ownership transfer
2. Call `sp_TransferFormOwnership` stored procedure
3. Handle errors and logging

**See:** `docs/ACCESS-CONTROL-OWNERSHIP-TRANSFER.md` for implementation.

### 2.4 Ownership Router

**File:** `backend/modules/forms/ownership_router.py` (NEW)

**Changes:**
1. Create API endpoint for ownership transfer
2. Require Company Admin privileges
3. Validate inputs

**See:** `docs/ACCESS-CONTROL-OWNERSHIP-TRANSFER.md` for implementation.

---

## 3. Implementation Order

### Phase 1: Database Foundation
1. ✅ Create migration for `agency_form_builder` role
2. ✅ Create migration for ownership transfer procedure
3. ✅ Create migration for access function
4. ✅ Run migrations and verify

### Phase 2: Backend Updates
1. ✅ Update `EventCompanyRole` model
2. ✅ Update access control service to use database function
3. ✅ Create ownership service and router
4. ✅ Update all form endpoints to use new access checking
5. ✅ Add agency access support

### Phase 3: Testing
1. ✅ Unit tests for access function
2. ✅ Integration tests for agency access
3. ✅ Integration tests for ownership transfer
4. ✅ End-to-end tests for complete workflows

### Phase 4: Documentation
1. ✅ Update Access Control Matrix
2. ✅ Create Agency Model documentation
3. ✅ Create Ownership Transfer documentation
4. ✅ Create Database Function documentation

---

## 4. Testing Checklist

### 4.1 Agency Access Tests

- [ ] Agency user can view all forms for event
- [ ] Agency user can edit all forms for event
- [ ] Agency user cannot see host company details
- [ ] Agency user cannot see other events
- [ ] Agency user can create forms (owned by host company)
- [ ] Per-form ACL overrides agency access correctly
- [ ] Agency access revoked when EventCompany.IsActive = 0

### 4.2 Ownership Transfer Tests

- [ ] Company Admin can transfer ownership
- [ ] System Admin can transfer ownership
- [ ] Regular user cannot transfer ownership
- [ ] All forms transferred correctly
- [ ] FormAccessControl entries transferred
- [ ] Audit trail created
- [ ] Validation errors handled correctly

### 4.3 Access Function Tests

- [ ] System Admin returns MANAGE
- [ ] Form owner returns MANAGE
- [ ] Explicit ACL returns specified type
- [ ] Agency access returns VIEW/EDIT
- [ ] Company role returns default
- [ ] No access returns NULL
- [ ] Company permission constraints enforced

---

## 5. Migration Checklist

### Pre-Migration
- [ ] Backup database
- [ ] Review migration scripts
- [ ] Test migrations on staging environment

### Migration Execution
- [ ] Run migration 024 (agency role)
- [ ] Run migration 025 (ownership transfer)
- [ ] Run migration 026 (access function)
- [ ] Verify all objects created successfully

### Post-Migration
- [ ] Verify agency role exists
- [ ] Test ownership transfer procedure
- [ ] Test access function with various scenarios
- [ ] Update backend code to use new function
- [ ] Deploy backend updates

---

## 6. Rollback Plan

### If Issues Arise

1. **Database Rollback:**
   - Run migration downgrade scripts in reverse order
   - Restore from backup if needed

2. **Backend Rollback:**
   - Revert to previous access control service implementation
   - Keep database changes (non-breaking) or rollback if critical

3. **Feature Flags:**
   - Consider feature flags for agency access and ownership transfer
   - Allow gradual rollout

---

## 7. Key Files to Update

### Database Migrations
- `backend/migrations/versions/024_add_agency_form_builder_role.py` (NEW)
- `backend/migrations/versions/025_add_form_ownership_transfer_procedure.py` (NEW)
- `backend/migrations/versions/026_add_form_access_function.py` (NEW)

### Backend Models
- `backend/models/ref/event_company_role.py` (UPDATE)

### Backend Services
- `backend/modules/forms/access_control_service.py` (UPDATE)
- `backend/modules/forms/ownership_service.py` (NEW)
- `backend/modules/forms/access_guard.py` (UPDATE)

### Backend Routers
- `backend/modules/forms/ownership_router.py` (NEW)
- `backend/main.py` (UPDATE - register new router)

### Documentation
- `docs/ACCESS-CONTROL-MATRIX.md` (UPDATE)
- `docs/ACCESS-CONTROL-AGENCY-MODEL.md` (NEW)
- `docs/ACCESS-CONTROL-OWNERSHIP-TRANSFER.md` (NEW)
- `docs/ACCESS-CONTROL-DATABASE-FUNCTION.md` (NEW)
- `docs/ACCESS-CONTROL-IMPLEMENTATION-PLAN.md` (NEW - this file)

---

## 8. Success Criteria

### Agency Model
- ✅ Agency users can view/edit all forms for specific event
- ✅ Forms remain owned by host company
- ✅ Agency users have limited visibility (event-scoped only)
- ✅ Per-form ACLs can override agency access

### Ownership Transfer
- ✅ Company Admin can bulk transfer form ownership
- ✅ All forms and access control entries transferred
- ✅ Complete audit trail created
- ✅ Validation and security checks enforced

### Centralized Access Logic
- ✅ All access checks use database function
- ✅ Consistent access logic across all services
- ✅ Performance optimized with proper indexes
- ✅ Access source and reason tracked

---

## 9. Next Steps

1. **Review and Approve:**
   - Review all documentation
   - Approve design decisions
   - Confirm migration approach

2. **Create Migrations:**
   - Generate migration files
   - Test migrations on staging
   - Prepare rollback scripts

3. **Update Backend:**
   - Update models
   - Update services
   - Create new services/routers
   - Update existing endpoints

4. **Testing:**
   - Unit tests
   - Integration tests
   - End-to-end tests
   - Performance tests

5. **Deployment:**
   - Deploy database migrations
   - Deploy backend updates
   - Monitor for issues
   - Verify functionality

---

## 10. Questions for Clarification

Before implementation, please confirm:

1. **Agency Role Naming:**
   - Is `agency_form_builder` the preferred role code?
   - Should we use `agency_form_builder` or `agency_form_editor`?

2. **Agency Permissions:**
   - Should agencies be able to delete forms they create?
   - Should agencies be able to grant access to other users?
   - Should agencies have ANALYZE access by default?

3. **Ownership Transfer:**
   - Should we transfer FormAccessControl entries automatically?
   - Should we allow partial transfers (specific forms only)?
   - Should we require a reason for transfer?

4. **Access Function:**
   - Should we cache access results?
   - What cache TTL is appropriate?
   - Should we log all access checks?

5. **Backward Compatibility:**
   - Do we need to support existing access patterns?
   - Are there any breaking changes to consider?

---

This implementation plan provides a roadmap for implementing the updated access control model with agency support, ownership transfer, and centralized database logic.

