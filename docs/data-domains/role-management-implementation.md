# Role Management Implementation Guide

**Document Purpose:** Developer implementation reference for Story 1.8  
**Status:** Ready for Implementation  
**SQL File:** `database/schemas/role-schema.sql`

---

## Important: Database vs Backend Naming

- **Database:** Uses **PascalCase** (e.g., `UserRole`, `UserRoleID`, `RoleLevel`)
- **Backend (Python):** Uses **snake_case** (e.g., `user_role`, `user_role_id`, `role_level`)

This guide shows database schema in SQL (PascalCase) and backend logic in Python (snake_case).

---

## Architecture Overview

The EventLead Platform uses a **dual-role architecture** that separates system-level roles (platform administration) from company-level roles (team management).

### Key Principles

1. **Complete Separation**: System roles and company roles are in separate tables with no cross-contamination
2. **Single Role Per Context**: Users have one system role (or none) and one company role per company
3. **Automatic Auditing**: All role changes are captured via database triggers (tamper-proof)
4. **Security First**: Role hierarchy enforced at database level with `RoleLevel` column

---

## Database Tables

### 1. UserRole Table (System-Level Roles)

**Purpose:** Defines platform-wide system roles (e.g., `system_admin`)

```sql
CREATE TABLE [UserRole] (
    UserRoleID BIGINT IDENTITY(1,1) PRIMARY KEY,
    RoleCode NVARCHAR(50) NOT NULL,
    RoleName NVARCHAR(100) NOT NULL,
    Description NVARCHAR(500) NOT NULL,
    RoleLevel INT NOT NULL,  -- 1 = highest privilege
    CanManagePlatform BIT NOT NULL DEFAULT 0,
    CanManageAllCompanies BIT NOT NULL DEFAULT 0,
    CanViewAllData BIT NOT NULL DEFAULT 0,
    CanAssignSystemRoles BIT NOT NULL DEFAULT 0,
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 0,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    CONSTRAINT UX_UserRole_RoleCode UNIQUE (RoleCode)
);
```

**Seed Data:** 1 role
- `system_admin` (RoleLevel 1) - Platform-wide administrator

### 2. UserCompanyRole Table (Company-Level Roles)

**Purpose:** Defines company-scoped roles (e.g., `company_admin`, `company_user`)

```sql
CREATE TABLE [UserCompanyRole] (
    UserCompanyRoleID BIGINT IDENTITY(1,1) PRIMARY KEY,
    RoleCode NVARCHAR(50) NOT NULL,
    RoleName NVARCHAR(100) NOT NULL,
    Description NVARCHAR(500) NOT NULL,
    RoleLevel INT NOT NULL,  -- 2 = company_admin, 3 = company_user, 4 = company_viewer
    CanManageCompany BIT NOT NULL DEFAULT 0,
    CanManageUsers BIT NOT NULL DEFAULT 0,
    CanManageEvents BIT NOT NULL DEFAULT 0,
    CanManageForms BIT NOT NULL DEFAULT 0,
    CanExportData BIT NOT NULL DEFAULT 0,
    CanViewReports BIT NOT NULL DEFAULT 0,
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 0,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    CONSTRAINT UX_UserCompanyRole_RoleCode UNIQUE (RoleCode)
);
```

**Seed Data:** 3 roles
- `company_admin` (RoleLevel 2) - Full company access
- `company_user` (RoleLevel 3) - Standard user access
- `company_viewer` (RoleLevel 4) - Read-only access

### 3. User Table Changes

**Add column:**
```sql
ALTER TABLE [User]
ADD UserRoleID BIGINT NULL;  -- FK to UserRole

ALTER TABLE [User]
ADD CONSTRAINT FK_User_UserRole 
    FOREIGN KEY (UserRoleID) REFERENCES [UserRole](UserRoleID);
```

**Logic:**
- `UserRoleID = NULL` → User is an application user (not a system admin)
- `UserRoleID = 1` → User is a system admin

### 4. UserCompany Table Changes

**Add column:**
```sql
ALTER TABLE [UserCompany]
ADD UserCompanyRoleID BIGINT NULL;  -- FK to UserCompanyRole

ALTER TABLE [UserCompany]
ADD CONSTRAINT FK_UserCompany_UserCompanyRole 
    FOREIGN KEY (UserCompanyRoleID) REFERENCES [UserCompanyRole](UserCompanyRoleID);
```

**Logic:**
- Every `UserCompany` record MUST have a `UserCompanyRoleID`
- Determines what the user can do within that specific company

### 5. AuditRole Table (Audit Trail)

**Purpose:** Automatic audit log for all role changes (populated via triggers)

```sql
CREATE TABLE [AuditRole] (
    AuditRoleID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- What was changed?
    TableName NVARCHAR(50) NOT NULL,  -- 'User' or 'UserCompany'
    RecordID BIGINT NOT NULL,  -- UserID or UserCompanyID
    ColumnName NVARCHAR(50) NOT NULL,  -- 'UserRoleID' or 'UserCompanyRoleID'
    
    -- Role change details
    OldRoleID BIGINT NULL,  -- Previous role (NULL if first assignment)
    NewRoleID BIGINT NULL,  -- New role (NULL if removed)
    OldRoleName NVARCHAR(100) NULL,
    NewRoleName NVARCHAR(100) NULL,
    
    -- Who made the change?
    ChangedBy BIGINT NULL,
    ChangedByEmail NVARCHAR(255) NULL,
    
    -- Context
    ChangeReason NVARCHAR(500) NULL,
    IPAddress NVARCHAR(50) NULL,
    UserAgent NVARCHAR(500) NULL,
    
    -- Metadata
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    IsDeleted BIT NOT NULL DEFAULT 0,
    
    CONSTRAINT FK_AuditRole_ChangedBy FOREIGN KEY (ChangedBy) REFERENCES [User](UserID)
);
```

**Important:** This table is populated automatically by database triggers (see Schema File)

---

## Role Assignment Logic (Backend - Python)

**Important:** Backend code uses snake_case naming (e.g., `user_role_id`), not PascalCase

### System Role Assignment

```python
# Assign system_admin role
user.user_role_id = 1  # system_admin

# Check if user is system admin
is_system_admin = user.user_role_id == 1

# Remove system role
user.user_role_id = None
```

### Company Role Assignment

```python
# Assign company_admin role
user_company.user_company_role_id = 1  # company_admin

# Check if user is company admin for specific company
is_company_admin = user_company.user_company_role_id == 1

# Get user's role for a company
role = db.query(UserCompanyRole).join(UserCompany).filter(
    UserCompany.user_id == user_id,
    UserCompany.company_id == company_id
).first()
```

### Role Hierarchy

**RoleLevel determines hierarchy:**
- `1` = System Admin (highest - platform-wide)
- `2` = Company Admin (company-wide)
- `3` = Company User (standard access)
- `4` = Company Viewer (read-only)

**Rule:** Lower number = higher privilege

**Enforcement:**
```python
def can_assign_role(assigner_role_level: int, target_role_level: int) -> bool:
    """User can only assign roles with higher level number (lower privilege)"""
    return target_role_level > assigner_role_level

# Example:
# Company Admin (level 2) can assign Company User (level 3) ✅
# Company Admin (level 2) cannot assign System Admin (level 1) ❌
# Company User (level 3) cannot assign Company Admin (level 2) ❌
```

---

## Security Rules

### 1. System Admin Protection

- **ONLY** System Admins can assign `system_admin` role
- Company Admins **CANNOT** see or assign system roles
- System Admin role is **NOT** tied to any company

### 2. Company Admin Protection

- Company Admins can only assign roles within their company
- Company Admins can assign `company_user` and `company_viewer` roles
- Company Admins **CANNOT** assign `company_admin` to themselves

### 3. Role Escalation Prevention

```python
# Backend validation example
def validate_role_assignment(
    current_user: User,
    target_user: User,
    new_role_level: int
) -> bool:
    # Get assigner's highest role level
    assigner_level = get_highest_role_level(current_user)
    
    # Cannot assign role with equal or higher privilege
    if new_role_level <= assigner_level:
        raise PermissionError("Cannot assign role with equal or higher privilege")
    
    # System roles can only be assigned by system admins
    if new_role_level == 1 and current_user.UserRoleID != 1:
        raise PermissionError("Only system admins can assign system_admin role")
    
    return True
```

### 4. Audit Trail (Automatic)

All role changes are **automatically** logged to `AuditRole` table via database triggers. You don't need to manually insert into `AuditRole` - the triggers handle it.

**Trigger behavior:**
- Fires **AFTER UPDATE** on `User.UserRoleID` or `UserCompany.UserCompanyRoleID`
- Captures old role → new role transition
- Records who made the change and when
- **Cannot be bypassed** (database-level enforcement)

---

## Implementation Checklist

### Prerequisites: Database Schema (Execute Before Development Begins)
- [ ] Execute `database/schemas/role-schema.sql` on development database
- [ ] Verify all tables created (`UserRole`, `UserCompanyRole`, `AuditRole`)
- [ ] Verify seed data loaded (1 system role, 3 company roles)
- [ ] Verify triggers created (2 triggers for automatic auditing)
- [ ] Verify `User.UserRoleID` column added
- [ ] Verify `UserCompany.UserCompanyRoleID` column added
- [ ] Verify bootstrap: UserID=1 assigned `system_admin` role

### Phase 1: Backend Models
- [ ] Create `backend/models/user_role.py`
- [ ] Create `backend/models/user_company_role.py`
- [ ] Create `backend/models/audit_role.py`
- [ ] Update `backend/models/user.py` (add `user_role_id` field)
- [ ] Update `backend/models/user_company.py` (add `user_company_role_id` field)

### Phase 2: Backend Role Service
- [ ] Create `backend/modules/roles/service.py`
  - [ ] `get_available_roles(current_user, context)` - Returns roles user can assign
  - [ ] `assign_system_role(user_id, role_id, assigner_id)` - Assign system role
  - [ ] `assign_company_role(user_company_id, role_id, assigner_id)` - Assign company role
  - [ ] `validate_role_hierarchy(assigner_level, target_level)` - Enforce hierarchy
  - [ ] `get_user_permissions(user_id, company_id)` - Get user's effective permissions

### Phase 3: Backend API Endpoints
- [ ] `GET /api/admin/roles` - List all available roles (filtered by user context)
- [ ] `GET /api/admin/roles/system` - List system roles (system admins only)
- [ ] `GET /api/admin/roles/company` - List company roles
- [ ] `POST /api/admin/users/{userId}/system-role` - Assign system role
- [ ] `POST /api/admin/users/{userId}/company-role` - Assign company role
- [ ] `DELETE /api/admin/users/{userId}/system-role` - Revoke system role
- [ ] `DELETE /api/admin/users/{userId}/company-role` - Revoke company role
- [ ] `GET /api/admin/audit/roles` - View role change audit trail

### Phase 4: Frontend Components
- [ ] Create `RoleSelector` component (dropdown with hierarchy-aware filtering)
- [ ] Update `UserInvitation` form (show appropriate roles based on inviter's role)
- [ ] Create `RoleManagement` admin page (view/edit user roles)
- [ ] Create `AuditTrail` component (view role change history)

### Phase 5: Testing
- [ ] Unit tests: Role hierarchy validation logic
- [ ] Unit tests: Role assignment validation
- [ ] Integration tests: Role assignment/revocation flows
- [ ] Security tests: Role escalation prevention
- [ ] Security tests: System admin protection
- [ ] E2E tests: Company Admin cannot assign system_admin
- [ ] E2E tests: System Admin can assign all roles
- [ ] E2E tests: Audit trail captures all changes

---

## Common Queries

### Get all system admins
```sql
SELECT u.UserID, u.Email, ur.RoleName
FROM [User] u
INNER JOIN [UserRole] ur ON u.UserRoleID = ur.UserRoleID
WHERE u.UserRoleID IS NOT NULL;
```

### Get user's role within a company
```sql
SELECT u.UserID, u.Email, c.CompanyName, ucr.RoleName
FROM [User] u
INNER JOIN [UserCompany] uc ON u.UserID = uc.UserID
INNER JOIN [Company] c ON uc.CompanyID = c.CompanyID
INNER JOIN [UserCompanyRole] ucr ON uc.UserCompanyRoleID = ucr.UserCompanyRoleID
WHERE u.UserID = @UserID AND c.CompanyID = @CompanyID AND uc.IsActive = 1;
```

### Get all companies where user is admin
```sql
SELECT c.CompanyID, c.CompanyName
FROM [Company] c
INNER JOIN [UserCompany] uc ON c.CompanyID = uc.CompanyID
WHERE uc.UserID = @UserID 
  AND uc.UserCompanyRoleID = 1  -- company_admin
  AND uc.IsActive = 1;
```

### View role change audit trail
```sql
SELECT 
    ar.CreatedDate,
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

---

## Future Evolution (Not for Story 1.8)

This architecture is designed for **simplicity first** (single role per context), but can easily evolve:

1. **Many-to-Many Roles** (Year 2-3 if needed)
   - Create junction tables for multiple roles per user
   - Keep existing `UserRole`/`UserCompanyRole` as lookup tables

2. **Permission-Based Access Control (PBAC)** (Year 3-5)
   - Create `Permission` table for granular permissions
   - Create `RolePermission` junction table
   - Move from role-based to permission-based checks

---

## Related Files

- **SQL Schema:** `database/schemas/role-schema.sql` (production-ready, Solomon approved)
- **User Schema:** `database/schemas/user-schema-v2.sql` (existing User/UserCompany tables)
- **Story:** `docs/stories/story-1.8.md` (implementation tracking)

---

## Standards Compliance

✅ **PascalCase:** All table and column names  
✅ **NVARCHAR:** All text columns  
✅ **Audit Columns:** CreatedDate, CreatedBy, UpdatedDate, UpdatedBy on all tables  
✅ **[TableName]ID:** Primary key naming (UserRoleID, UserCompanyRoleID, AuditRoleID)  
✅ **Foreign Keys:** Proper naming conventions (FK_Table_ReferencedTable)  
✅ **IDENTITY(1,1):** Auto-increment for all primary keys  
✅ **GETUTCDATE():** UTC timestamps  
✅ **Seed Data:** All lookup tables populated  

**Reviewed and approved by Solomon (SQL Standards Sage) ✅**

---

**Ready for implementation. Execute `role-schema.sql` on development database to begin.**

