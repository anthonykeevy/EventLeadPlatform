# Agency / Outsourced Event-Form Access Model

## Overview

This document defines the access control model for agency/outsourced form-building scenarios, where external agencies work on forms for specific events while maintaining tight access scoping at the database layer.

---

## 1. Agency Event Company Role

### 1.1 New Role: `agency_form_builder`

**Purpose:** Allow external agency companies to work on forms for a specific event with tightly scoped access to that event only.

**Role Configuration:**

| Field | Value | Description |
|-------|-------|-------------|
| `RoleCode` | `agency_form_builder` | Unique role identifier |
| `RoleName` | `Agency Form Builder` | Display name |
| `RoleLevel` | `25` | Between `event_participant` (10) and `event_organizer` (50) |
| `HasEditEvent` | `0` | Cannot edit event details |
| `HasDeleteEvent` | `0` | Cannot delete event |
| `HasManageParticipants` | `0` | Cannot manage event participants |
| `HasViewEvent` | `1` | Can view event details (read-only) |
| `HasViewAllFormsForEvent` | `1` | **NEW** - Can view all forms for this event |
| `HasEditAllFormsForEvent` | `1` | **NEW** - Can edit all forms for this event |

**Database Schema Changes:**

```sql
-- Add new columns to ref.EventCompanyRole
ALTER TABLE [ref].[EventCompanyRole]
ADD HasViewAllFormsForEvent BIT NOT NULL DEFAULT 0,
    HasEditAllFormsForEvent BIT NOT NULL DEFAULT 0;

-- Create index for performance
CREATE INDEX IX_EventCompanyRole_FormAccess 
ON [ref].[EventCompanyRole](HasViewAllFormsForEvent, HasEditAllFormsForEvent)
WHERE HasViewAllFormsForEvent = 1 OR HasEditAllFormsForEvent = 1;
```

**Seed Data:**

```sql
INSERT INTO [ref].[EventCompanyRole] (
    RoleCode, 
    RoleName, 
    Description, 
    RoleLevel,
    HasEditEvent,
    HasDeleteEvent,
    HasManageParticipants,
    HasViewEvent,
    HasViewAllFormsForEvent,
    HasEditAllFormsForEvent,
    IsActive,
    SortOrder,
    CreatedBy
) VALUES (
    'agency_form_builder',
    'Agency Form Builder',
    'External agency company working on forms for a specific event. Read-only event access, but can view and edit all forms associated with the event. Forms remain owned by host company.',
    25,
    0,  -- Cannot edit event
    0,  -- Cannot delete event
    0,  -- Cannot manage participants
    1,  -- Can view event
    1,  -- Can view all forms for event
    1,  -- Can edit all forms for event
    1,  -- Active
    4,  -- Sort order (after event_participant)
    1   -- CreatedBy (system)
);
```

---

## 2. Agency Visibility & Form Access Behavior

### 2.1 Form Ownership Model

**Key Principle:** Forms remain owned by the host company, even when created by agency users.

**Database Structure:**
- `Form.CompanyID = HostCompanyID` (form belongs to host company)
- `Form.EventID = EventID` (form is associated with the event)
- `Form.CreatedBy = AgencyUserID` (agency user can create forms)

**Behavior:**
- Agency users can **create forms** for the event
- Forms are logically owned by the **host company** (based on `CompanyID`)
- Agency users have **event-scoped access** to all forms for that event
- Agency users **cannot see** the full host company (limited visibility)

### 2.2 Agency Form Access Rules

**When computing access for agency users:**

1. **Check EventCompany relationship:**
   ```sql
   IF EXISTS (
       SELECT 1 
       FROM dbo.EventCompany ec
       INNER JOIN ref.EventCompanyRole ecr ON ec.EventCompanyRoleID = ecr.EventCompanyRoleID
       WHERE ec.EventID = @FormEventID
         AND ec.CompanyID = @AgencyCompanyID
         AND ec.IsDeleted = 0
         AND ec.IsActive = 1
         AND ecr.HasViewAllFormsForEvent = 1
   )
   ```

2. **Determine access level:**
   - If `HasViewAllFormsForEvent = 1` → **VIEW** access to all forms for that event
   - If `HasEditAllFormsForEvent = 1` → **EDIT** access to all forms for that event
   - Access is **event-scoped only** - agency sees forms for that event, not all host company forms

3. **Per-form overrides:**
   - `FormAccessControl` entries can still override agency access
   - More restrictive ACLs take precedence (e.g., if agency has EDIT but ACL grants VIEW, use VIEW)
   - More permissive ACLs take precedence (e.g., if agency has VIEW but ACL grants MANAGE, use MANAGE)

### 2.3 Agency Visibility Restrictions

**What Agency Users CAN See:**
- ✅ Event details (read-only)
- ✅ All forms associated with the event
- ✅ Form submissions for event forms (if granted ANALYZE access)
- ✅ Their own created forms (via Resource Ownership)

**What Agency Users CANNOT See:**
- ❌ Full host company details
- ❌ Host company's other events (not associated with agency)
- ❌ Host company's forms for other events
- ❌ Host company's users or team structure
- ❌ Host company's settings or configuration

**UI Implications:**
- Agency users see a **limited dashboard** showing only:
  - The event they're working on
  - Forms associated with that event
  - Their own user profile
- Agency users do NOT see company switcher or company-level navigation

---

## 3. Access Check Priority (Updated)

The access check priority includes agency event-scoped access:

### Priority Order:

1. **System Admin Override** → MANAGE (all forms, all companies)
2. **Resource Ownership** → MANAGE (form creator)
3. **Explicit FormAccessControl** → Use specified access type (overrides agency access)
4. **Agency Event-Scoped Access** → VIEW/EDIT all forms for event (if `agency_form_builder` role)
5. **Company Role Default** → Default based on company role
6. **No Access** → Requires explicit FormAccessControl entry

**Key Points:**
- Agency access is checked **AFTER** explicit FormAccessControl (allows per-form overrides)
- Agency access is checked **BEFORE** company role default (agency access takes precedence)
- Agency access is **event-scoped only** - does not grant company-wide access

---

## 4. Implementation Example

### 4.1 Linking Agency to Event

```sql
-- Host company links agency company to event
INSERT INTO dbo.EventCompany (
    EventID,
    CompanyID,  -- Agency Company ID
    EventCompanyRoleID,  -- agency_form_builder role ID
    IsActive,
    CreatedBy,
    CreatedDate,
    IsDeleted
)
SELECT 
    @EventID,
    @AgencyCompanyID,
    (SELECT EventCompanyRoleID FROM ref.EventCompanyRole WHERE RoleCode = 'agency_form_builder'),
    1,
    @HostCompanyAdminUserID,
    GETUTCDATE(),
    0;
```

### 4.2 Agency User Creating Form

```sql
-- Agency user creates form for event
INSERT INTO dbo.Form (
    FormName,
    FormDescription,
    CompanyID,  -- Host Company ID (form ownership)
    EventID,    -- Event ID (form association)
    FormStatusID,
    FormApprovalStatusID,
    CreatedBy,  -- Agency User ID (form creator)
    CreatedDate,
    IsDeleted
)
VALUES (
    @FormName,
    @FormDescription,
    @HostCompanyID,  -- Form owned by host company
    @EventID,
    @FormStatusID,
    @FormApprovalStatusID,
    @AgencyUserID,   -- Created by agency user
    GETUTCDATE(),
    0
);
```

### 4.3 Access Check for Agency User

```sql
-- Check if agency user has access to form
DECLARE @AgencyUserID BIGINT = 123;
DECLARE @FormID BIGINT = 456;

-- Get form details
DECLARE @FormEventID BIGINT;
DECLARE @FormCompanyID BIGINT;

SELECT @FormEventID = EventID, @FormCompanyID = CompanyID
FROM dbo.Form
WHERE FormID = @FormID AND IsDeleted = 0;

-- Check agency event-scoped access
IF EXISTS (
    SELECT 1
    FROM dbo.UserCompany uc
    INNER JOIN dbo.EventCompany ec ON uc.CompanyID = ec.CompanyID
    INNER JOIN ref.EventCompanyRole ecr ON ec.EventCompanyRoleID = ecr.EventCompanyRoleID
    WHERE uc.UserID = @AgencyUserID
      AND uc.IsDeleted = 0
      AND uc.StatusID = (SELECT UserCompanyStatusID FROM ref.UserCompanyStatus WHERE StatusCode = 'active')
      AND ec.EventID = @FormEventID
      AND ec.IsDeleted = 0
      AND ec.IsActive = 1
      AND ecr.HasViewAllFormsForEvent = 1
)
BEGIN
    -- Agency has access - determine level
    IF EXISTS (
        SELECT 1
        FROM dbo.UserCompany uc
        INNER JOIN dbo.EventCompany ec ON uc.CompanyID = ec.CompanyID
        INNER JOIN ref.EventCompanyRole ecr ON ec.EventCompanyRoleID = ecr.EventCompanyRoleID
        WHERE uc.UserID = @AgencyUserID
          AND uc.IsDeleted = 0
          AND uc.StatusID = (SELECT UserCompanyStatusID FROM ref.UserCompanyStatus WHERE StatusCode = 'active')
          AND ec.EventID = @FormEventID
          AND ec.IsDeleted = 0
          AND ec.IsActive = 1
          AND ecr.HasEditAllFormsForEvent = 1
    )
    BEGIN
        -- Agency has EDIT access to all forms for event
        SELECT 'EDIT' AS AccessLevel;
    END
    ELSE
    BEGIN
        -- Agency has VIEW access to all forms for event
        SELECT 'VIEW' AS AccessLevel;
    END
END
ELSE
BEGIN
    -- No agency access - check other layers (ownership, explicit ACL, company role)
    -- ... (continue with standard access check logic)
END
```

---

## 5. Workflow Integration

### 5.1 Agency Onboarding

1. **Host company admin** links agency company to event:
   - Creates `EventCompany` entry with `agency_form_builder` role
   - Agency company is now associated with the event

2. **Agency users** (members of agency company):
   - Can see the event in their dashboard (limited view)
   - Can view all forms for that event
   - Can edit all forms for that event (if `HasEditAllFormsForEvent = 1`)
   - Can create new forms for that event

3. **Form creation by agency:**
   - Agency user creates form → `Form.CompanyID = HostCompanyID` (form owned by host)
   - Agency user becomes form creator → has MANAGE access (Resource Ownership)
   - Other agency users have EDIT access (via agency event role)
   - Host company users have access based on their company role

### 5.2 Form Approval/Publishing

**Note:** The workflow for agencies creating forms and host company approving/publishing is documented in another artifact. The access model supports this workflow by:
- Allowing agency users to create/edit forms
- Maintaining form ownership with host company
- Enabling host company admins to review/approve/publish forms
- Providing event-scoped access for agencies without full company access

---

## 6. Security Considerations

### 6.1 Access Scoping

- **Event-scoped only:** Agency access is limited to forms for the specific event
- **No company-wide access:** Agency users cannot see host company's other events or forms
- **No user management:** Agency users cannot manage host company users or settings
- **Audit trail:** All agency actions are logged with agency company context

### 6.2 Data Isolation

- Forms remain owned by host company (`Form.CompanyID = HostCompanyID`)
- Agency users can create/edit forms but cannot transfer ownership
- Host company maintains control over form lifecycle (approval, publishing, deletion)
- Agency access can be revoked by removing `EventCompany` entry

### 6.3 Guardrails

- Only `company_admin` users in host company can link agencies to events
- Agency role assignment requires validation (ensure agency company exists, event exists)
- Agency access is automatically revoked if `EventCompany.IsActive = 0` or `IsDeleted = 1`
- Per-form ACLs can restrict agency access further if needed

---

## 7. Migration Requirements

### 7.1 Database Migration

**File:** `backend/migrations/versions/024_add_agency_form_builder_role.py`

**Changes:**
1. Add `HasViewAllFormsForEvent` and `HasEditAllFormsForEvent` columns to `ref.EventCompanyRole`
2. Insert `agency_form_builder` role seed data
3. Create index for performance
4. Update existing roles to set new columns to `0` (no form access)

### 7.2 Backend Model Updates

**File:** `backend/models/ref/event_company_role.py`

**Changes:**
1. Add `HasViewAllFormsForEvent` column
2. Add `HasEditAllFormsForEvent` column
3. Update model documentation

### 7.3 Access Control Service Updates

**File:** `backend/modules/forms/access_control_service.py`

**Changes:**
1. Update `get_user_form_access` function to check agency event-scoped access
2. Add agency access check at Priority 4 (after explicit ACL, before company role)
3. Ensure agency access respects per-form ACL overrides

---

## 8. Testing Scenarios

### 8.1 Agency Access Scenarios

1. **Agency user viewing event forms:**
   - Agency user should see all forms for the event
   - Agency user should NOT see forms for other events
   - Agency user should NOT see host company's other forms

2. **Agency user editing event forms:**
   - Agency user should be able to edit all forms for the event
   - Agency user should NOT be able to edit forms for other events
   - Agency user should NOT be able to delete forms (requires MANAGE access)

3. **Agency user creating forms:**
   - Agency user can create forms for the event
   - Form ownership remains with host company
   - Agency user gets MANAGE access to their own created forms
   - Other agency users get EDIT access to agency-created forms

4. **Per-form ACL overrides:**
   - If agency has EDIT but ACL grants VIEW → use VIEW
   - If agency has VIEW but ACL grants MANAGE → use MANAGE
   - Explicit ACL always takes precedence over agency access

### 8.2 Host Company Scenarios

1. **Host company admin linking agency:**
   - Only `company_admin` can link agencies to events
   - Agency company must exist and be valid
   - Event must exist and belong to host company

2. **Host company revoking agency access:**
   - Setting `EventCompany.IsActive = 0` revokes agency access
   - Agency users lose access to event forms immediately
   - Forms remain owned by host company

---

## 9. Summary

### Key Principles

1. **Forms remain owned by host company** - `Form.CompanyID = HostCompanyID`
2. **Agency access is event-scoped** - Only forms for the specific event
3. **Agency access is checked at Priority 4** - After explicit ACL, before company role
4. **Per-form ACLs can override** - More restrictive or permissive ACLs take precedence
5. **Limited visibility** - Agency users see only event-scoped resources, not full company

### Benefits

- ✅ **Tight access scoping** - Agencies only see what they need
- ✅ **Database-enforced** - Access logic centralized in database function
- ✅ **Flexible** - Per-form ACLs allow fine-grained control
- ✅ **Auditable** - All agency actions logged with context
- ✅ **Reversible** - Agency access can be revoked easily

This model supports agency/outsourced form-building while maintaining security and data isolation at the database layer.

