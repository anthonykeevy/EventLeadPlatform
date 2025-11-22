# Story 2.9: Remaining Work - Access Control Matrix Implementation

## Executive Summary

Story 2.9 has **basic form access control implemented**, but **does NOT yet implement** the enhanced access control model defined in the Access Control Matrix and related documents. The database migrations (024, 025, 026) have been created and run, but the backend code has not been updated to use the new database objects.

---

## ✅ What's Complete

### Database Layer
- ✅ **Migration 024**: `agency_form_builder` role added to `ref.EventCompanyRole` with `HasViewAllFormsForEvent` and `HasEditAllFormsForEvent` columns
- ✅ **Migration 025**: `sp_TransferFormOwnership` stored procedure created
- ✅ **Migration 026**: `fn_GetUserFormAccess` table-valued function created
- ✅ **Database Schema**: Updated documentation reflects new objects

### Basic Access Control (Story 2.9 Original Scope)
- ✅ FormAccessControl CRUD operations
- ✅ Access grant/revoke functionality
- ✅ Basic access checks (ownership, explicit ACL)
- ✅ Access control UI components
- ✅ Reference data endpoints

---

## ❌ What's Missing (From Access Control Matrix)

### 1. Backend Model Updates

#### 1.1 EventCompanyRole Model
**File:** `backend/models/ref/event_company_role.py`

**Status:** ❌ **NOT UPDATED**

**Missing:**
```python
HasViewAllFormsForEvent = Column(Boolean, nullable=False, default=False)
HasEditAllFormsForEvent = Column(Boolean, nullable=False, default=False)
```

**Impact:** Backend cannot access the new agency role columns, even though they exist in the database.

---

### 2. Access Control Service Updates

#### 2.1 Use Centralized Database Function
**File:** `backend/modules/forms/access_control_service.py`

**Status:** ❌ **NOT UPDATED**

**Current Implementation:**
- Uses custom Python logic for access checks
- Checks ownership, explicit ACL, company admin separately
- Does NOT use `fn_GetUserFormAccess` database function

**Required Changes:**
- Replace `check_user_access()` method to call `fn_GetUserFormAccess(@UserID, @FormID)`
- Use function return values: `EffectiveAccessTypeCode`, `CanView`, `CanEdit`, `CanManage`, etc.
- Use `AccessSource` and `AccessReason` for logging

**Example:**
```python
# Current (custom logic):
access_level = await check_user_access(db, form_id, user_id, "MANAGE")

# Required (use database function):
result = db.execute(
    text("SELECT * FROM [dbo].[fn_GetUserFormAccess](:user_id, :form_id)"),
    {"user_id": user_id, "form_id": form_id}
).fetchone()
access_level = result.EffectiveAccessTypeCode
can_manage = result.CanManage
```

**Impact:** Access checks are inconsistent and don't follow the 6-priority access check logic defined in the matrix.

---

#### 2.2 Agency Access Support
**File:** `backend/modules/forms/access_control_service.py`

**Status:** ❌ **NOT IMPLEMENTED**

**Missing:**
- Check for `agency_form_builder` role in `EventCompany` table
- Check `HasViewAllFormsForEvent` and `HasEditAllFormsForEvent` flags
- Grant VIEW/EDIT access to all forms for the event (Priority 4 in access check)

**Required Logic:**
```python
# Check if user's company has agency_form_builder role for event
# If yes, check HasViewAllFormsForEvent and HasEditAllFormsForEvent
# Grant appropriate access to all forms for that event
```

**Impact:** Agency/outsourced form-building scenario is not supported.

---

### 3. Access Guard Updates

#### 3.1 Use Database Function
**File:** `backend/modules/forms/access_guard.py`

**Status:** ❌ **NOT UPDATED**

**Required Changes:**
- Update `check_form_access()` to use `fn_GetUserFormAccess`
- Update `filter_accessible_forms()` to use database function in WHERE clause
- Remove duplicate access check logic

**Impact:** Access guards are inconsistent with centralized logic.

---

### 4. Ownership Transfer Service

#### 4.1 Ownership Service
**File:** `backend/modules/forms/ownership_service.py`

**Status:** ❌ **NOT CREATED**

**Required:**
- Create new service file
- Implement `transfer_form_ownership()` method
- Call `sp_TransferFormOwnership` stored procedure
- Handle errors and validation
- Log to audit trail

**See:** `docs/ACCESS-CONTROL-OWNERSHIP-TRANSFER.md` for implementation details.

**Impact:** Form ownership transfer (for user off-boarding) is not available.

---

#### 4.2 Ownership Router
**File:** `backend/modules/forms/ownership_router.py`

**Status:** ❌ **NOT CREATED**

**Required:**
- Create new router file
- Implement `POST /api/forms/ownership/transfer` endpoint
- Require Company Admin privileges
- Validate inputs (FromUserID, ToUserID, CompanyID)
- Call ownership service
- Return transfer results

**See:** `docs/ACCESS-CONTROL-OWNERSHIP-TRANSFER.md` for implementation details.

**Impact:** No API endpoint for ownership transfer.

---

### 5. Integration Updates

#### 5.1 Form Service Updates
**File:** `backend/modules/forms/service.py`

**Status:** ⚠️ **PARTIALLY UPDATED**

**Required:**
- Update all form CRUD methods to use `fn_GetUserFormAccess` via access guard
- Ensure agency access is checked (Priority 4)
- Ensure company role defaults are used (Priority 5)

**Impact:** Form operations may not respect all access control layers.

---

#### 5.2 Router Registration
**File:** `backend/main.py`

**Status:** ❌ **NOT UPDATED**

**Required:**
- Register `ownership_router` if created
- Ensure access control router uses updated services

**Impact:** Ownership transfer endpoint not available.

---

## 📋 Implementation Checklist

### Phase 1: Model Updates (High Priority)
- [ ] Update `EventCompanyRole` model with new columns
- [ ] Test model can read/write new columns
- [ ] Verify model relationships still work

### Phase 2: Access Control Service (High Priority)
- [ ] Update `check_user_access()` to use `fn_GetUserFormAccess`
- [ ] Update `get_user_accessible_forms()` to use database function
- [ ] Add agency access check logic (Priority 4)
- [ ] Remove duplicate access check code
- [ ] Test all access scenarios

### Phase 3: Access Guard Updates (High Priority)
- [ ] Update `check_form_access()` to use database function
- [ ] Update `filter_accessible_forms()` to use database function
- [ ] Test access guards with all scenarios

### Phase 4: Ownership Transfer (Medium Priority)
- [ ] Create `ownership_service.py`
- [ ] Implement `transfer_form_ownership()` method
- [ ] Create `ownership_router.py`
- [ ] Implement transfer endpoint
- [ ] Register router in `main.py`
- [ ] Test ownership transfer scenarios

### Phase 5: Integration (High Priority)
- [ ] Update form service to use new access checking
- [ ] Update form router to use new access checking
- [ ] Test all form CRUD operations
- [ ] Verify agency access works end-to-end

### Phase 6: Testing (High Priority)
- [ ] Unit tests for database function usage
- [ ] Integration tests for agency access
- [ ] Integration tests for ownership transfer
- [ ] End-to-end tests for complete workflows
- [ ] Performance tests for access checks

### Phase 7: Documentation (Medium Priority)
- [ ] Update `story-2.9.md` with new requirements
- [ ] Document agency access workflow
- [ ] Document ownership transfer workflow
- [ ] Update UAT test guide with new scenarios

---

## 🎯 Priority Order

### **Critical (Must Complete)**
1. **Update EventCompanyRole model** - Blocks all agency access functionality
2. **Update access control service to use database function** - Ensures consistent access logic
3. **Add agency access support** - Required for agency/outsourced form-building scenario
4. **Update access guards** - Ensures all form operations use centralized logic

### **Important (Should Complete)**
5. **Create ownership transfer service and router** - Required for user off-boarding scenario
6. **Update form service integration** - Ensures all form operations respect new access model
7. **Comprehensive testing** - Validates all scenarios work correctly

### **Nice to Have**
8. **Documentation updates** - Improves maintainability

---

## 📊 Gap Analysis

| Component | Database | Backend Model | Backend Service | API Endpoint | Status |
|-----------|----------|---------------|-----------------|--------------|--------|
| Agency Role | ✅ | ❌ | ❌ | ❌ | **25% Complete** |
| Access Function | ✅ | N/A | ❌ | ❌ | **33% Complete** |
| Ownership Transfer | ✅ | N/A | ❌ | ❌ | **33% Complete** |
| Basic Access Control | ✅ | ✅ | ✅ | ✅ | **100% Complete** |

---

## 🔗 Related Documents

- **Access Control Matrix**: `docs/ACCESS-CONTROL-MATRIX.md` - Complete access control model
- **Agency Model**: `docs/ACCESS-CONTROL-AGENCY-MODEL.md` - Agency role implementation
- **Ownership Transfer**: `docs/ACCESS-CONTROL-OWNERSHIP-TRANSFER.md` - Ownership transfer implementation
- **Database Function**: `docs/ACCESS-CONTROL-DATABASE-FUNCTION.md` - Centralized access logic
- **Implementation Plan**: `docs/ACCESS-CONTROL-IMPLEMENTATION-PLAN.md` - Complete implementation roadmap

---

## 💡 Recommendations

1. **Start with Model Updates**: Update `EventCompanyRole` model first - this unblocks agency access functionality.

2. **Migrate to Database Function**: Update access control service to use `fn_GetUserFormAccess` - this ensures all access checks follow the same 6-priority logic.

3. **Add Agency Support**: Implement agency access checks - this enables the agency/outsourced form-building scenario.

4. **Create Ownership Transfer**: Implement ownership transfer service and router - this enables user off-boarding workflows.

5. **Comprehensive Testing**: Test all scenarios from the Access Control Matrix to ensure everything works correctly.

---

## 📝 Notes

- The database migrations are complete and tested - no database changes needed.
- The basic access control from Story 2.9 is working - this is about enhancing it to match the Access Control Matrix.
- The Access Control Matrix defines a more sophisticated model with 6 priority levels - the current implementation only handles 3 (ownership, explicit ACL, company admin).
- Agency access and ownership transfer are new features not in the original Story 2.9 scope.

---

*Last Updated: 2025-01-XX*  
*Status: Database ready, backend code needs updates*

