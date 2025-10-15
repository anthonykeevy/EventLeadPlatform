# Story 1.8: Role Management Architecture & Implementation

**Status:** ReadyForImplementation - Schema Ready ✅

---

## Story

As a **platform architect**,
I want **a properly designed role management system that separates system-level and company-level roles**,
so that **system admins can manage the platform while company admins manage their teams without cross-contamination**.

---

## Architecture Summary

The platform uses a **dual-role architecture**:

### System-Level Roles (Platform-Wide)
- Stored in `UserRole` database table
- Assigned via `User.UserRoleID` foreign key
- **Example:** `system_admin` - can manage entire platform
- Not tied to any specific company

### Company-Level Roles (Company-Scoped)
- Stored in `UserCompanyRole` database table  
- Assigned via `UserCompany.UserCompanyRoleID` foreign key
- **Examples:** `company_admin`, `company_user`, `company_viewer`
- Scoped to specific company context

### Audit Trail
- All role changes automatically logged to `AuditRole` table
- Triggered by database triggers (tamper-proof)
- Cannot be bypassed by application code

---

## Acceptance Criteria

### AC-1.8.1: System and Company Role Separation ✅
**Given** the role management system is implemented  
**When** roles are assigned  
**Then** system roles (`system_admin`) and company roles (`company_admin`, `company_user`, `company_viewer`) are stored in separate tables

### AC-1.8.2: System Admin Not Tied to Company ✅
**Given** a user is assigned `system_admin` role  
**When** the role is stored  
**Then** the role is assigned via `User.UserRoleID` (not via `UserCompany`)

### AC-1.8.3: Company Roles Scoped to Company ✅
**Given** a user is assigned a company role  
**When** the role is stored  
**Then** the role is assigned via `UserCompany.UserCompanyRoleID` for that specific company

### AC-1.8.4: Role Hierarchy Enforced
**Given** roles have different privilege levels  
**When** a user attempts to assign a role  
**Then** users can only assign roles with lower privilege than their own (higher `RoleLevel` number)

### AC-1.8.5: Role Changes Audited
**Given** a user's role is changed  
**When** the database record is updated  
**Then** the change is automatically logged to `AuditRole` table with old role, new role, and who made the change

### AC-1.8.6: Role Assignment API
**Given** authorized users need to assign roles  
**When** API endpoints are called  
**Then** role assignment APIs work correctly and enforce hierarchy

### AC-1.8.7: Role Management UI
**Given** authorized users need to manage roles via UI  
**When** users access role management features  
**Then** UI displays only roles they have permission to assign

### AC-1.8.8: Comprehensive Testing
**Given** role management is critical to security  
**When** tests are run  
**Then** all role assignment, hierarchy, and audit functionality is covered by tests

### AC-1.8.9: Permission Abstraction Layer (Future-Proofing)
**Given** the platform may evolve to granular permission-based access control  
**When** code needs to check permissions  
**Then** all permission checks use `PermissionService` (backend) or `usePermissions` hook (frontend) to enable future migration without major refactoring

---

## Database Tables

**Note:** Database uses PascalCase naming (e.g., `UserRole`, `UserRoleID`). Backend Python code will use snake_case (e.g., `user_role`, `user_role_id`).

### UserRole (System-Level Roles Lookup)
```sql
UserRoleID BIGINT PRIMARY KEY
RoleCode NVARCHAR(50) UNIQUE          -- e.g., 'system_admin'
RoleName NVARCHAR(100)                -- e.g., 'System Administrator'
Description NVARCHAR(500)
RoleLevel INT                         -- 1 = highest privilege
CanManagePlatform BIT
CanManageAllCompanies BIT
CanViewAllData BIT
CanAssignSystemRoles BIT
IsActive BIT
SortOrder INT
CreatedDate, CreatedBy, UpdatedDate, UpdatedBy
```

**Seed Data:** 1 role (`system_admin`)

### UserCompanyRole (Company-Level Roles Lookup)
```sql
UserCompanyRoleID BIGINT PRIMARY KEY
RoleCode NVARCHAR(50) UNIQUE          -- e.g., 'company_admin', 'company_user'
RoleName NVARCHAR(100)                -- e.g., 'Company Administrator'
Description NVARCHAR(500)
RoleLevel INT                         -- 2 = company_admin, 3 = company_user, 4 = company_viewer
CanManageCompany BIT
CanManageUsers BIT
CanManageEvents BIT
CanManageForms BIT
CanExportData BIT
CanViewReports BIT
IsActive BIT
SortOrder INT
CreatedDate, CreatedBy, UpdatedDate, UpdatedBy
```

**Seed Data:** 3 roles (`company_admin`, `company_user`, `company_viewer`)

### User Table Changes
```sql
ALTER TABLE [User]
ADD UserRoleID BIGINT NULL;           -- FK to UserRole table
```

**Logic:** `UserRoleID = NULL` means user is not a system admin

### UserCompany Table Changes
```sql
ALTER TABLE [UserCompany]
ADD UserCompanyRoleID BIGINT NULL;    -- FK to UserCompanyRole table
```

**Logic:** Every `UserCompany` record must have a `UserCompanyRoleID`

### AuditRole (Audit Trail - Auto-Populated)
```sql
AuditRoleID BIGINT PRIMARY KEY
TableName NVARCHAR(50)                -- 'User' or 'UserCompany'
RecordID BIGINT                       -- UserID or UserCompanyID
ColumnName NVARCHAR(50)               -- 'UserRoleID' or 'UserCompanyRoleID'
OldRoleID BIGINT NULL
NewRoleID BIGINT NULL
OldRoleName NVARCHAR(100) NULL
NewRoleName NVARCHAR(100) NULL
ChangedBy BIGINT                      -- FK to User
ChangedByEmail NVARCHAR(255)
ChangeReason NVARCHAR(500) NULL
IPAddress NVARCHAR(50) NULL
UserAgent NVARCHAR(500) NULL
CreatedDate DATETIME2
IsDeleted BIT
```

**Important:** This table is populated automatically by database triggers

---

## Role Hierarchy

**RoleLevel** determines privilege (lower number = higher privilege):
- `1` = System Admin (highest - platform-wide)
- `2` = Company Admin (company-wide)
- `3` = Company User (standard access)
- `4` = Company Viewer (read-only)

**Rule:** Users can only assign roles with **higher** `RoleLevel` number (lower privilege) than their own.

**Examples:**
- ✅ Company Admin (level 2) can assign Company User (level 3)
- ❌ Company Admin (level 2) cannot assign System Admin (level 1)
- ❌ Company User (level 3) cannot assign Company Admin (level 2)

---

## Security Rules

### 1. System Admin Protection
- **ONLY** System Admins can assign `system_admin` role
- Company Admins cannot see or assign system roles
- System Admin role is not tied to any company

### 2. Role Escalation Prevention
- Backend must validate role hierarchy before assignment
- Users cannot assign roles with equal or higher privilege
- System roles can only be assigned by system admins

### 3. Audit Trail (Automatic)
- All role changes automatically logged via database triggers
- Triggers fire on `UPDATE` of `UserRoleID` or `UserCompanyRoleID`
- Cannot be bypassed by application code
- Captures old role → new role transition

---

## Tasks / Subtasks

### Story Context (Before Development Begins)
- [ ] Create `docs/story-context-1.8.xml` (single source of truth for developer)

### Database Schema (Prerequisites - Execute Before Development)
- [x] Schema design approved by Solomon ✅
- [x] SQL file ready (`database/schemas/role-schema.sql`) ✅
- [ ] Execute schema on development database
- [ ] Verify seed data loaded (1 system role, 3 company roles)
- [ ] Verify triggers working correctly
- [ ] Bootstrap UserID=1 as `system_admin`

### Backend Implementation - Phase 1: Models
- [ ] Create `backend/models/user_role.py` (SQLAlchemy model for UserRole table)
- [ ] Create `backend/models/user_company_role.py` (SQLAlchemy model for UserCompanyRole table)
- [ ] Create `backend/models/audit_role.py` (SQLAlchemy model for AuditRole table)
- [ ] Update `backend/models/user.py` (add `user_role_id` field)
- [ ] Update `backend/models/user_company.py` (add `user_company_role_id` field)

### Backend Implementation - Phase 2: Service Layer
- [ ] Create `backend/modules/roles/service.py` with:
  - [ ] `get_available_roles(current_user, context)` - Returns roles user can assign
  - [ ] `assign_system_role(user_id, role_id, assigner_id)` - Assign system role with validation
  - [ ] `assign_company_role(user_company_id, role_id, assigner_id)` - Assign company role with validation
  - [ ] `validate_role_hierarchy(assigner_level, target_level)` - Enforce hierarchy
  - [ ] `get_user_permissions(user_id, company_id)` - Get effective permissions
  - [ ] `check_permission(user_id, company_id, permission)` - Permission check helper

### Backend Implementation - Phase 2.5: Permission Abstraction Layer (AC-1.8.9)
**Purpose:** Enable future migration to permission-based access control without major refactoring

- [ ] **Permission Service Creation:**
  - [ ] Create `backend/modules/permissions/service.py`
  - [ ] Define `Permission` enum with all platform permissions:
    - [ ] Company permissions: `company:settings:view`, `company:settings:edit`, `company:billing:view`, `company:billing:edit`
    - [ ] User permissions: `users:view`, `users:invite`, `users:edit`, `users:delete`, `users:assign_roles`
    - [ ] Event permissions: `events:view`, `events:create`, `events:edit`, `events:delete`, `events:publish`
    - [ ] Form permissions: `forms:view`, `forms:create`, `forms:edit`, `forms:delete`
    - [ ] Data permissions: `data:export`, `reports:view`, `reports:create`, `analytics:view`
  - [ ] Implement `PermissionService` class with stable public API:
    - [ ] `has_permission(user_id, permission, company_id)` - Check if user has permission
    - [ ] `get_user_permissions(user_id, company_id)` - Get all user permissions as list
  - [ ] Implement private method `_check_role_flags()` that maps Permission enum to role flags
  - [ ] Implement private method `_derive_permissions_from_role()` that converts role flags to permission list
  - [ ] Add comprehensive docstrings explaining future migration path
  - [ ] Document permission-to-role mapping in code comments

- [ ] **Documentation:**
  - [ ] Create `docs/architecture/permission-abstraction-layer.md` explaining:
    - [ ] Why abstraction layer exists (future PBAC migration)
    - [ ] How to use PermissionService in backend code
    - [ ] Migration path from role flags to Permission table (Year 2-3)

### Backend Implementation - Phase 3: API Endpoints
- [ ] `GET /api/admin/roles` - List all available roles (filtered by user context)
- [ ] `GET /api/admin/roles/system` - List system roles (system admins only)
- [ ] `GET /api/admin/roles/company` - List company roles
- [ ] `POST /api/admin/users/{user_id}/system-role` - Assign system role
- [ ] `POST /api/admin/users/{user_id}/company-role` - Assign company role
- [ ] `DELETE /api/admin/users/{user_id}/system-role` - Revoke system role
- [ ] `DELETE /api/admin/users/{user_id}/company-role` - Revoke company role
- [ ] `GET /api/admin/audit/roles` - View role change audit trail

### Backend Implementation - Phase 4: Authorization Middleware
- [ ] Create role-based authorization decorator
- [ ] Implement permission checking middleware
- [ ] Apply to protected endpoints
- [ ] Test with different role combinations

### Frontend Implementation - Phase 5: Permission Abstraction Layer (AC-1.8.9)
**Purpose:** Enable future migration to permission-based access control without major refactoring

- [ ] **Permission Hook Creation:**
  - [ ] Create `frontend/src/hooks/usePermissions.ts`
  - [ ] Define `Permission` type matching backend enum (TypeScript union type)
  - [ ] Implement `usePermissions()` hook with stable public API:
    - [ ] `hasPermission(permission)` - Check if current user has permission
    - [ ] `hasAnyPermission(permissions)` - Check if user has any of the permissions
    - [ ] `hasAllPermissions(permissions)` - Check if user has all permissions
    - [ ] `permissions` - Array of all user permissions (for debugging)
  - [ ] Implement private method `_derivePermissionsFromRole()` that maps role flags to permissions
  - [ ] Add comprehensive JSDoc comments explaining future migration path

- [ ] **Permission Gate Component:**
  - [ ] Create `frontend/src/components/PermissionGate.tsx`
  - [ ] Implement component that shows children only if user has permission
  - [ ] Add `fallback` prop for unauthorized state
  - [ ] Add TypeScript types and documentation

- [ ] **Documentation:**
  - [ ] Add JSDoc to `usePermissions` explaining:
    - [ ] How to use hook in components
    - [ ] How permission system will evolve (Year 2-3)
    - [ ] Migration path (no component changes required)

### Frontend Implementation - Phase 6: Components
- [ ] Create `RoleSelector` component (dropdown with hierarchy-aware filtering)
- [ ] Update `UserInvitation` form (show appropriate roles based on inviter's role)
- [ ] Create `RoleManagement` admin page (view/edit user roles)
- [ ] Create `AuditTrail` component (view role change history)
- [ ] Add role-based UI element visibility using `usePermissions` hook and `PermissionGate` component

### Testing - Phase 7: Comprehensive Coverage
- [ ] **Unit Tests:**
  - [ ] Role hierarchy validation logic
  - [ ] Role assignment validation
  - [ ] Permission checking functions
  - [ ] `PermissionService.has_permission()` returns correct results
  - [ ] `PermissionService.get_user_permissions()` returns complete permission list
  - [ ] `usePermissions()` hook derives correct permissions from role flags
- [ ] **Integration Tests:**
  - [ ] Role assignment/revocation flows
  - [ ] Database trigger functionality
  - [ ] Audit trail capture
  - [ ] Permission checks work across service layer
- [ ] **Security Tests:**
  - [ ] Role escalation prevention
  - [ ] System admin protection
  - [ ] Company admin cannot assign system_admin
  - [ ] Permission abstraction layer enforces same security as direct role checks
- [ ] **E2E Tests:**
  - [ ] System Admin can assign all roles
  - [ ] Company Admin role assignment limited to company roles
  - [ ] Audit trail visible in UI
  - [ ] UI elements hidden/shown based on permissions using `PermissionGate`

---

## Dev Notes

### Role Assignment Logic (Backend Code)

```python
# Backend uses snake_case naming
from models.user import User
from models.user_role import UserRole
from models.user_company_role import UserCompanyRole

# Assign system_admin role
user.user_role_id = 1  # system_admin

# Check if user is system admin
is_system_admin = user.user_role_id == 1

# Get user's company role
user_company = db.query(UserCompany).filter(
    UserCompany.user_id == user_id,
    UserCompany.company_id == company_id
).first()

is_company_admin = user_company.user_company_role_id == 1  # company_admin
```

### Common Database Queries

**Get all system admins:**
```sql
SELECT u.UserID, u.Email, ur.RoleName
FROM [User] u
INNER JOIN [UserRole] ur ON u.UserRoleID = ur.UserRoleID
WHERE u.UserRoleID IS NOT NULL;
```

**Get user's role within a company:**
```sql
SELECT u.UserID, u.Email, c.CompanyName, ucr.RoleName
FROM [User] u
INNER JOIN [UserCompany] uc ON u.UserID = uc.UserID
INNER JOIN [Company] c ON uc.CompanyID = c.CompanyID
INNER JOIN [UserCompanyRole] ucr ON uc.UserCompanyRoleID = ucr.UserCompanyRoleID
WHERE u.UserID = @UserID AND c.CompanyID = @CompanyID AND uc.IsActive = 1;
```

**View role change audit trail:**
```sql
SELECT 
    ar.CreatedDate AS ChangeDate,
    ar.TableName,
    ar.RecordID,
    ar.OldRoleName,
    ar.NewRoleName,
    ar.ChangedByEmail,
    ar.ChangeReason
FROM [AuditRole] ar
WHERE ar.IsDeleted = 0
ORDER BY ar.CreatedDate DESC;
```

### Architecture Patterns and Constraints
- **Zero Trust:** Role hierarchy enforced at database and API level
- **Audit Trail:** All role changes fully logged (automatic, tamper-proof)
- **Multi-tenancy:** System Admin sees all, Company Admin sees only their company
- **Future-Ready:** Design supports evolution to many-to-many roles if needed (Year 2-3)

### Testing Standards
- **Security Tests:** Role escalation attack prevention is critical
- **Unit Tests:** Role hierarchy validation logic
- **Integration Tests:** Full role assignment/revocation flow
- **E2E Tests:** UI role selector shows only appropriate options

---

## References

- **SQL Schema:** `database/schemas/role-schema.sql` (production-ready, Solomon approved)
- **Implementation Guide:** `docs/data-domains/role-management-implementation.md` (comprehensive developer reference)
- **User Schema:** `database/schemas/user-schema-v2.sql` (existing User/UserCompany tables)

---

## Type
Architecture + Feature (Epic 1)

## Priority
High - Blocks Epic 2 (Company Management)

## Estimated Effort
**5 weeks** (includes permission abstraction layer)
- Week 1: Database Schema Execution & Backend Models
- Week 2: Backend Service Layer & Permission Abstraction Layer (PermissionService)
- Week 3: API Endpoints & Authorization Middleware
- Week 4: Frontend Permission Abstraction (usePermissions hook) & Components
- Week 5: Comprehensive Testing & Security Validation

**Note:** Permission abstraction layer adds ~6 hours (included in Week 2 & 4 estimates)

## Dependencies
- Story 1.1 (User Signup) - Complete ✅
- Database schema ready - Complete ✅

---

## Dev Agent Record

### Context Reference
- `docs/story-context-1.8.xml` (to be created after story approval, before development begins)

### Agent Model Used
{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

---

**🚀 Ready for Implementation - Schema approved and ready to execute!**
