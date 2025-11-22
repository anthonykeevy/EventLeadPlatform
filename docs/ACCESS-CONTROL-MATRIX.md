# Access Control Matrix - Multi-Layer Permissions

## Overview

This document provides a comprehensive matrix showing how access controls cascade across different layers of the EventLead Platform. Understanding these layers is critical for implementing proper form access control.

---

## Access Control Layers

The platform uses **5 layers of access control** that cascade from platform-wide to resource-specific:

1. **System Role** (`ref.UserRole`) - Platform-level permissions
2. **Company Role** (`ref.UserCompanyRole`) - Company-level permissions
3. **Event Company Role** (`ref.EventCompanyRole`) - Event-specific company permissions
4. **Form Access Control** (`dbo.FormAccessControl` + `ref.FormAccessControlAccessType`) - Form-specific permissions
5. **Resource Ownership** - Creator-based implicit permissions

---

## Layer 1: System Role (Platform-Level)

**Table:** `ref.UserRole`  
**Applies To:** Entire platform (all companies, all resources)  
**Assigned To:** `dbo.User.UserRoleID`

| System Role | Role Level | CanManagePlatform | CanManageAllCompanies | CanViewAllData | CanAssignSystemRoles | Scope |
|-------------|------------|-------------------|----------------------|----------------|---------------------|-------|
| `system_admin` | 100 | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | Platform-wide override |
| `company_user` | 10 | ❌ No | ❌ No | ❌ No | ❌ No | Standard user (default) |

**Key Rules:**
- **System Admin** can access ALL companies and ALL resources (bypasses all other layers)
- **Company User** has no system-level permissions (subject to all other layers)
- System role is assigned at user account creation

---

## Layer 2: Company Role (Company-Level)

**Table:** `ref.UserCompanyRole`  
**Applies To:** All resources within a specific company  
**Assigned To:** `dbo.UserCompany.UserCompanyRoleID` (junction table)

| Company Role | Role Level | CanManageCompany | CanManageUsers | CanManageEvents | CanManageForms | CanExportData | CanViewReports | Default Form Access |
|--------------|------------|------------------|----------------|-----------------|----------------|---------------|----------------|-------------------|
| `company_admin` | 100 | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | **MANAGE** |
| `company_user` | 50 | ❌ No | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | **VIEW** |
| `company_viewer` | 10 | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No | ✅ Yes | **VIEW** |

**Key Rules:**
- Company Admin can manage company settings, users, events, and forms
- Company User can create/edit own events and forms, export data, view reports
- Company Viewer has read-only access (view events, forms, reports only)
- **Default Form Access:** Company role determines baseline form access (can be overridden by Layer 4)
- A user can have different company roles in different companies

---

## Layer 3: Event Company Role (Event-Specific)

**Table:** `ref.EventCompanyRole`  
**Applies To:** Event management AND event-scoped form access (for agency roles)  
**Assigned To:** `dbo.EventCompany.EventCompanyRoleID` (junction table)

| Event Role | Role Level | HasEditEvent | HasDeleteEvent | HasManageParticipants | HasViewEvent | HasViewAllFormsForEvent | HasEditAllFormsForEvent | Form Access Impact |
|------------|------------|--------------|----------------|----------------------|--------------|------------------------|------------------------|-------------------|
| `event_owner` | 100 | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No | ❌ No | **None** (uses company role default) |
| `event_organizer` | 50 | ✅ Yes | ❌ No | ❌ No | ✅ Yes | ❌ No | ❌ No | **None** (uses company role default) |
| `event_participant` | 10 | ❌ No | ❌ No | ❌ No | ✅ Yes | ❌ No | ❌ No | **None** (uses company role default) |
| `agency_form_builder` | 25 | ❌ No | ❌ No | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes | **VIEW/EDIT all forms for event** (event-scoped access) |

**Key Rules:**
- **Standard Event Roles** (owner, organizer, participant) affect EVENT MANAGEMENT ONLY, not form access
- **Agency Event Role** (`agency_form_builder`) provides event-scoped form access:
  - `HasViewAllFormsForEvent = 1` → Agency users can **VIEW all forms** associated with that event
  - `HasEditAllFormsForEvent = 1` → Agency users can **EDIT all forms** associated with that event
  - Forms remain owned by host company (`Form.CompanyID = HostCompanyID`)
  - Agency users see only event-scoped forms, not full host company access
- Event Owner can edit/delete event and manage participants
- Event Organizer can edit extended event fields but not delete event
- Event Participant can view event details but cannot edit event
- **Event Participant can still create/manage their own forms** associated with the event (via Resource Ownership)
- Event owners can see participant count to understand impact of event changes on all participants
- **Agency form access is checked AFTER explicit FormAccessControl but BEFORE company role default** (see Access Check Priority)

---

## Layer 4: Form Access Control (Form-Specific)

**Table:** `dbo.FormAccessControl` + `ref.FormAccessControlAccessType`  
**Applies To:** Specific form  
**Assigned To:** `dbo.FormAccessControl` (junction table with User, Company, Form)

| Form Access Type | Access Level | Form Fields (Read) | Form Fields (Write) | Operations | Use Case |
|-----------------|--------------|-------------------|-------------------|------------|----------|
| **MANAGE** | 100 | All fields | All fields | Full management, delete, grant access | Form owner/admin |
| **EDIT** | 75 | All fields | FormName, FormDescription, FormStatusID, FormThumbnailURL, FormPreviewURL, EventID, IsPublic, Form content | Edit form content, change status | Content editor |
| **ANALYZE** | 50 | All fields + Submissions data, Analytics | None (read-only) | View analytics, export data | Data analyst |
| **SUBMIT** | 25 | All fields | Form submissions (create) | Submit responses | Form respondent |
| **VIEW** | 10 | All metadata fields (read-only) | None | View form, view status | Read-only access |

**Key Rules:**
- Explicit `FormAccessControl` entry **overrides** default access from company role (Layer 2)
- Form owner (creator) always has MANAGE access (implicit, Layer 5)
- External users (different company) **must** have explicit `FormAccessControl` entry
- Access types are hierarchical (higher levels include lower level permissions)

---

## Layer 5: Resource Ownership (Implicit)

**Applies To:** Resource creators  
**No Table:** Implicit based on `CreatedBy` field

| Resource Type | Ownership Permission | Implicit Access |
|--------------|---------------------|----------------|
| **Company** | Creator | Company Admin role (Layer 2) |
| **Event** | Creator | Event Owner role (Layer 3) + Full event control |
| **Form** | Creator | MANAGE access (Layer 4) + Cannot be revoked |

**Key Rules:**
- Resource creator always has full access to their resource
- Ownership cannot be transferred or revoked
- Ownership overrides all other access control layers

---

## Access Check Priority (Cascading Logic)

When checking if a user can access a form, the system evaluates in this order:

### Priority 1: System Admin Override
```
IF user.system_role == 'system_admin':
    RETURN MANAGE (full access, bypasses all other checks)
```

### Priority 2: Resource Ownership
```
IF user.user_id == form.created_by:
    RETURN MANAGE (form owner always has full access)
    
    NOTE: Ownership can be reassigned by:
    - Company Admin (for their own company) via bulk transfer procedure
    - System Admin (global override)
```

### Priority 3: Explicit Form Access Control
```
IF FormAccessControl entry exists (user_id, form_id, is_deleted=False):
    RETURN FormAccessControl.FormAccessControlAccessTypeID (use explicit access)
    
    NOTE: Per-form overrides remain valid and take precedence over agency access
```

### Priority 4: Agency Event-Scoped Access (NEW)
```
IF form.event_id IS NOT NULL:
    IF EventCompany entry exists (event_id = form.event_id, company_id = user_company_id, is_deleted=False, is_active=True):
        IF EventCompanyRole.HasViewAllFormsForEvent = 1:
            IF EventCompanyRole.HasEditAllFormsForEvent = 1:
                RETURN EDIT (agency can edit all forms for event)
            ELSE:
                RETURN VIEW (agency can view all forms for event)
    
    NOTE: Agency access is event-scoped only - they see forms for that event, not full company access
```

### Priority 5: Company Role Default
```
IF UserCompany entry exists (user_id, form.company_id, is_deleted=False, status='active'):
    RETURN default based on UserCompanyRole:
        - company_admin → MANAGE
        - company_user → VIEW
        - company_viewer → VIEW
```

### Priority 6: External User (No Access)
```
ELSE:
    RETURN None (no access - requires explicit FormAccessControl entry)
```

**Notes:**
- **Agency Event Role** (`agency_form_builder`) is checked at Priority 4, providing event-scoped form access
- Standard Event Roles (owner, organizer, participant) do NOT affect form access - only event management
- Agency users see only event-scoped forms, not full host company access
- Forms remain owned by host company (`Form.CompanyID = HostCompanyID`)

---

## Complete Access Matrix

### Scenario 1: System Admin

| User Type | System Role | Company Role | Event Role | Explicit Form Access | **Final Form Access** |
|-----------|-------------|--------------|------------|---------------------|---------------------|
| System Admin | system_admin | N/A | N/A | N/A | **MANAGE** (all forms, all companies) |

**Notes:**
- System Admin bypasses ALL other layers
- Has full access to every form in the platform
- Can manage all companies and resources

---

### Scenario 2: Company Creator (Internal User)

| User Type | System Role | Company Role | Event Role | Explicit Form Access | **Final Form Access** |
|-----------|-------------|--------------|------------|---------------------|---------------------|
| Company Creator | company_user | company_admin | N/A | N/A | **MANAGE** (all company forms) |
| Company Creator | company_user | company_admin | event_owner | N/A | **MANAGE** (all company forms + event forms) |

**Notes:**
- Company creator automatically gets `company_admin` role (Layer 5)
- Has MANAGE access to all forms in their company (Layer 2 default)
- If they create an event, they get `event_owner` role (Layer 3)

---

### Scenario 3: Company Admin (Internal User)

| User Type | System Role | Company Role | Event Role | Explicit Form Access | **Final Form Access** |
|-----------|-------------|--------------|------------|---------------------|---------------------|
| Company Admin | company_user | company_admin | N/A | N/A | **MANAGE** (all company forms) |
| Company Admin | company_user | company_admin | event_owner | N/A | **MANAGE** (all company forms, including event forms) |
| Company Admin | company_user | company_admin | event_organizer | N/A | **MANAGE** (all company forms, including event forms) |
| Company Admin | company_user | company_admin | event_participant | N/A | **MANAGE** (all company forms, including event forms they create) |
| Company Admin | company_user | company_admin | N/A | VIEW (specific form) | **VIEW** (specific form), **MANAGE** (other forms) |

**Notes:**
- Default MANAGE access from `company_admin` role (Layer 2)
- **Event role does NOT affect form access** - Company Admin has MANAGE access to all forms regardless of event role
- Event role only affects **event management** (can edit event, delete event, manage participants)
- Even as `event_participant`, Company Admin can create/manage forms associated with the event
- Explicit FormAccessControl can downgrade access for specific sensitive forms

---

### Scenario 4: Company User (Internal User)

| User Type | System Role | Company Role | Explicit Form Access | **Final Form Access** |
|-----------|-------------|--------------|---------------------|---------------------|
| Company User | company_user | company_user | N/A | **VIEW** (all company forms) |
| Company User | company_user | company_user | EDIT (specific form) | **EDIT** (specific form), **VIEW** (other forms) |
| Company User | company_user | company_user | MANAGE (specific form) | **MANAGE** (specific form), **VIEW** (other forms) |

**Notes:**
- Default VIEW access from `company_user` role (Layer 2)
- Can **create forms** (because `CanManageForms=True`) - Forms are always created for an Event
- When creating a form, user becomes form owner and has MANAGE access to their own forms (via Resource Ownership - Layer 5)
- Can **edit existing forms** if granted EDIT access via explicit FormAccessControl
- Can **VIEW all forms** within their company/companies
- Event role is NOT considered for form access - only affects event management operations
- Explicit FormAccessControl can upgrade access to specific forms (Layer 4)

---

### Scenario 5: Company Viewer (Internal User)

| User Type | System Role | Company Role | Explicit Form Access | **Final Form Access** |
|-----------|-------------|--------------|---------------------|---------------------|
| Company Viewer | company_user | company_viewer | N/A | **VIEW** (all company forms for events they can see) |
| Company Viewer | company_user | company_viewer | EDIT (specific form) | **EDIT** (specific form), **VIEW** (other forms they can see) |
| Company Viewer | company_user | company_viewer | MANAGE (specific form) | **MANAGE** (specific form), **VIEW** (other forms they can see) |

**Notes:**
- Default VIEW access from `company_viewer` role (Layer 2)
- **Cannot create forms** on their own (because `CanManageForms=False`)
- **Can only create/edit forms if explicitly invited** and granted EDIT or MANAGE access via FormAccessControl
- When invited to create a form for an Event, can create and manage that specific form (via Resource Ownership - Layer 5)
- Can **VIEW other forms** that the company has for events they have access to
- **Cannot see the Company or Event** they've been invited to create a form for (limited visibility)
- **Cannot see all associated Companies or Events** (restricted view scope)
- Event role is NOT considered for form access - only affects event management operations
- Explicit FormAccessControl is required to grant create/edit permissions (Layer 4)

---

### Scenario 6: User Belonging to Multiple Companies

| User Type | System Role | Company Role (Company A) | Company Role (Company B) | Explicit Form Access (Company A Forms) | **Final Form Access (Company A)** |
|-----------|-------------|-------------------------|-------------------------|----------------------------------------|----------------------------------|
| Multi-Company User | company_user | company_admin | company_user | N/A | **MANAGE** (all Company A forms) |
| Multi-Company User | company_user | company_user | company_viewer | N/A | **VIEW** (all Company A forms) |
| Multi-Company User | company_user | company_admin | company_viewer | EDIT (specific form in Company A) | **EDIT** (specific form), **MANAGE** (other forms) |

**Notes:**
- **Users can only see companies they belong to** (via `dbo.UserCompany` entries)
- **Every company a user belongs to has a Company Role** assigned (company_admin, company_user, or company_viewer)
- Each company membership has independent form access based on that company's role
- Form access is determined separately for each company based on the user's role in that company
- No default access from other companies - each company's access is independent
- Event role is NOT considered for form access - only affects event management operations
- **External user scenario is not applicable** - if a user doesn't belong to a company, they cannot see that company at all (UI restriction)

---

### Scenario 7: Agency Form Builder (Event-Scoped Access)

| User Type | System Role | Company Role (Agency) | Event Role | Explicit Form Access | **Final Form Access** |
|-----------|-------------|----------------------|------------|---------------------|---------------------|
| Agency User | company_user | company_user (Agency Company) | agency_form_builder | N/A | **EDIT** (all forms for event) |
| Agency User | company_user | company_user (Agency Company) | agency_form_builder | VIEW (specific form) | **VIEW** (specific form), **EDIT** (other event forms) |
| Agency User | company_user | company_user (Agency Company) | agency_form_builder | MANAGE (specific form) | **MANAGE** (specific form), **EDIT** (other event forms) |

**Notes:**
- Agency users belong to **Agency Company** (different from host company)
- Agency is linked to event via `EventCompany` with `agency_form_builder` role
- `HasViewAllFormsForEvent = 1` → VIEW all forms for event
- `HasEditAllFormsForEvent = 1` → EDIT all forms for event
- Forms remain owned by **host company** (`Form.CompanyID = HostCompanyID`)
- Agency users see **only event-scoped forms**, not full host company access
- Agency users **cannot see** host company details, other events, or company settings
- Explicit FormAccessControl can override agency access (more restrictive or permissive)
- Agency users can **create forms** for the event (forms owned by host company)

---

### Scenario 8: Form Owner (Creator)

| User Type | System Role | Company Role | Event Role | Explicit Form Access | **Final Form Access** |
|-----------|-------------|--------------|------------|---------------------|---------------------|
| Form Owner | company_user | company_admin | N/A | N/A | **MANAGE** (own form) |
| Form Owner | company_user | company_user | N/A | N/A | **MANAGE** (own form) |
| Form Owner | company_user | company_viewer | N/A | N/A | **MANAGE** (own form) |
| Form Owner | company_user | company_user (other company) | N/A | VIEW | **MANAGE** (ownership overrides explicit entry) |

**Notes:**
- Form owner always has MANAGE access (Layer 5 - Resource Ownership)
- Ownership overrides all other layers, including explicit FormAccessControl
- Ownership can be transferred by Company Admin or System Admin via bulk transfer procedure
- Cannot revoke access from form owner (except via ownership transfer)

---

## Access Type Capabilities Matrix

### What Each Access Type Can Do (Form Operations)

| Operation | VIEW | SUBMIT | ANALYZE | EDIT | MANAGE | **Elaboration** |
|-----------|------|--------|---------|------|--------|----------------|
| **View form metadata** | ✅ | ✅ | ✅ | ✅ | ✅ | See form name, description, status, creation date, owner, associated event |
| **View form content** | ✅ | ✅ | ✅ | ✅ | ✅ | See form structure, fields, questions, validation rules, layout |
| **View form status** | ✅ | ✅ | ✅ | ✅ | ✅ | See current form status (Draft, Active, Archived, etc.) and approval status |
| **Submit form responses** | ❌ | ✅ | ❌ | ❌ | ✅ | Submit data through the form (create new submission records) |
| **View own submissions** | ❌ | ✅ | ✅ | ❌ | ✅ | See submissions that the current user created (own response history) |
| **View all submissions** | ❌ | ❌ | ✅ | ❌ | ✅ | See ALL submissions from ALL users (aggregate data view) |
| **View analytics/reports** | ❌ | ❌ | ✅ | ❌ | ✅ | Access charts, graphs, statistics, submission trends, completion rates |
| **Export form data** | ❌ | ❌ | ✅ | ❌ | ✅ | Download submissions as CSV, Excel, PDF, or other export formats |
| **Edit form name** | ❌ | ❌ | ❌ | ✅ | ✅ | Change the form's display name |
| **Edit form description** | ❌ | ❌ | ❌ | ✅ | ✅ | Modify the form's description text |
| **Edit form content** | ❌ | ❌ | ❌ | ✅ | ✅ | Modify form structure: add/remove/edit fields, questions, validation rules, layout |
| **Change form status** | ❌ | ❌ | ❌ | ✅ | ✅ | Update form lifecycle status (Draft → Active, Active → Archived, etc.) |
| **Associate with event** | ❌ | ❌ | ❌ | ✅ | ✅ | Link form to an event or change which event the form is associated with (Note: Forms are always created for an Event) |
| **Set deployment cost** | ❌ | ❌ | ❌ | ❌ | ✅ | Set financial cost/pricing for form deployment (billing/financial control) |
| **Change approval status** | ❌ | ❌ | ❌ | ❌ | ✅ | Approve/reject forms (approval workflow for forms requiring review) |
| **Delete form** | ❌ | ❌ | ❌ | ❌ | ✅ | Soft delete form (marks as deleted, may be recoverable) |
| **Grant form access** | ❌ | ❌ | ❌ | ❌ | ✅ | Give other users/companies access to this form (create FormAccessControl entries) |
| **Revoke form access** | ❌ | ❌ | ❌ | ❌ | ✅ | Remove access from users/companies (delete/revoke FormAccessControl entries) |
| **Manage access control** | ❌ | ❌ | ❌ | ❌ | ✅ | Full management of form access control list (view, grant, revoke, modify access types) |

---

## Company Restrictions Impact

### Company-Level Permissions (Layer 2) Influence Form Access

| Company Role | CanManageForms | CanViewReports | CanExportData | Impact on Form Access |
|--------------|----------------|----------------|---------------|---------------------|
| **company_admin** | ✅ Yes | ✅ Yes | ✅ Yes | **Full form management** - Can create, edit, delete, manage access |
| **company_user** | ✅ Yes | ✅ Yes | ✅ Yes | **Can create/edit own forms** - Default VIEW for others, can be upgraded |
| **company_viewer** | ❌ No | ✅ Yes | ❌ No | **Read-only** - Cannot create forms, VIEW only for existing forms |

**Key Rules:**
- `CanManageForms=False` → User **cannot create** new forms (but can view/edit if granted)
- `CanViewReports=False` → User **cannot access** ANALYZE access type
- `CanExportData=False` → User **cannot export** form data (even with ANALYZE access)

**Form Access Must Respect Company Permissions:**
- If `CanManageForms=False`, user cannot be granted EDIT or MANAGE access (even via explicit FormAccessControl)
- If `CanViewReports=False`, user cannot be granted ANALYZE access
- Company-level permissions are **hard constraints** that cannot be overridden by form-level access

---

## Event Access Impact on Forms

### ⚠️ **IMPORTANT: Event Role Does NOT Affect Form Access**

**Event roles affect EVENT MANAGEMENT ONLY, not form access.**

| Event Role | Event Permissions | Form Access Impact | Notes |
|------------|------------------|-------------------|-------|
| **event_owner** | Full event control (edit, delete, manage participants) | **None** | Can create/manage own forms for event (via Resource Ownership) |
| **event_organizer** | Edit extended event fields (cannot delete) | **None** | Can create/manage own forms for event (via Resource Ownership) |
| **event_participant** | View event details (cannot edit event) | **None** | Can create/manage own forms for event (via Resource Ownership) |

**Key Rules:**
- **Event role does NOT cascade to form access** - Form access is determined by Company Role (Layer 2) and Form Access Control (Layer 4)
- Event role determines what you can do with the **event itself** (edit event, delete event, manage participants)
- Event participants can still **create and manage their own forms** associated with the event (via Resource Ownership - Layer 5)
- Event owners can see **participant count** to understand impact of event changes on all participants
- If a form is associated with an event (`Form.EventID`), any participant can create forms for that event, regardless of their event role

**Example:**
- Company Admin (as `event_participant`) → Cannot edit event, but has **MANAGE** access to forms they create for the event
- Company User (as `event_participant`) → Cannot edit event, but has **MANAGE** access to forms they create for the event
- Event ownership or participant status has no bearing on form access - only Resource Ownership (who created the form) matters

---

## Access Control Decision Flow

```
┌─────────────────────────────────────┐
│ User requests Form Access          │
└──────────────┬──────────────────────┘
               │
               ▼
    ┌──────────────────────┐
    │ System Admin?        │
    └──────────┬───────────┘
               │
         ┌─────┴─────┐
         │ Yes       │ No
         ▼           ▼
    ┌────────┐  ┌──────────────────┐
    │ MANAGE │  │ Form Owner?      │
    └────────┘  └────────┬─────────┘
                         │
                    ┌────┴────┐
                    │ Yes     │ No
                    ▼         ▼
               ┌────────┐  ┌────────────────────────┐
               │ MANAGE │  │ Explicit FormAccess?   │
               └────────┘  └────────┬───────────────┘
                                    │
                               ┌────┴────┐
                               │ Yes     │ No
                               ▼         ▼
                          ┌────────┐  ┌──────────────────┐
                          │ Use    │  │ Company Role?    │
                          │ Explicit│  └────────┬─────────┘
                          └────────┘            │
                                           ┌────┴────┐
                                           │ Yes     │ No
                                           ▼         ▼
                                      ┌────────┐  ┌────────┐
                                      │ Use    │  │ DENY   │
                                      │ Company│  │ Access │
                                      │ Default│  └────────┘
                                      └────────┘

NOTE: Event Role is NOT included - it only affects
      event management, not form access
```

---

## Practical Examples

### Example 1: Internal User with Upgraded Access

**User:** John (company_user in Acme Corp)  
**Scenario:** Needs to edit a specific form

1. **System Role:** `company_user` (no system override)
2. **Company Role:** `company_user` → Default VIEW access
3. **Event:** Form is associated with Event (all forms are created for an Event)
4. **Explicit FormAccessControl:** EDIT (granted by form owner)
5. **Form Ownership:** No (John didn't create the form)

**Result:** **EDIT** access (explicit entry overrides company default)

**Note:** All forms are created for an Event, so there's always an event relationship. Event role does not affect form access.

---

### Example 2: User Belonging to Multiple Companies

**User:** Sarah (company_admin in Beta Corp, company_user in Acme Corp)  
**Scenario:** Needs to submit responses to Acme Corp's form

1. **System Role:** `company_user` (no system override)
2. **Company Role in Acme Corp:** `company_user` → Default VIEW access
3. **Company Role in Beta Corp:** `company_admin` (different company, doesn't apply to Acme Corp forms)
4. **Event:** Form is associated with Event (all forms are created for an Event)
5. **Explicit FormAccessControl:** SUBMIT (granted by Acme Corp to upgrade from VIEW)
6. **Form Ownership:** No (Sarah didn't create the form)

**Result:** **SUBMIT** access (explicit entry upgrades from default VIEW access)

**Note:** Since Sarah belongs to Acme Corp, she has default VIEW access. The explicit SUBMIT entry upgrades her access for this specific form.

---

### Example 3: Company Viewer Invited to Create Form

**User:** Mike (company_viewer in Gamma Corp)  
**Scenario:** Invited to create a form for an Event (has explicit MANAGE access)

1. **System Role:** `company_user` (no system override)
2. **Company Role:** `company_viewer` → Default VIEW access (cannot create forms without explicit invitation)
3. **Event:** Form is created for an Event (all forms are created for an Event)
4. **Explicit FormAccessControl:** MANAGE (invited by Company Admin to create form for Event)
5. **Form Ownership:** **YES** (Mike created the form after being invited)

**Result:** **MANAGE** access (ownership + explicit invitation overrides company role)

**Notes:**
- Mike has `company_viewer` role which normally prevents form creation
- He was explicitly invited and granted MANAGE access via FormAccessControl
- Once he creates the form, he becomes the form owner (Resource Ownership - Layer 5)
- Mike can manage the form he created, but has VIEW access to other company forms
- Mike cannot see the full Company or Event details - only the forms he's been given access to

---

### Example 4: Event Participant Creating Own Form

**User:** Lisa (company_user in Delta Corp)  
**Scenario:** Using existing event (as participant) and creating own form for that event

1. **System Role:** `company_user` (no system override)
2. **Company Role:** `company_user` → Default VIEW access
3. **Event Role:** **event_participant** (Lisa is using existing event created by someone else)
4. **Explicit FormAccessControl:** None
5. **Form Ownership:** **YES** (Lisa creates the form)

**Result:** **MANAGE** access to her own form (Resource Ownership overrides company role default)

**Key Point:** Even though Lisa is only an `event_participant` (can't edit the event), she can still create and manage her own forms associated with that event.

---

### Example 5: System Admin Accessing Any Form

**User:** Admin (system_admin)  
**Scenario:** Needs to access any form in the platform

1. **System Role:** **system_admin** → Platform-wide override
2. **Company Role:** N/A (bypassed)
3. **Event Role:** N/A (bypassed)
4. **Explicit FormAccessControl:** N/A (bypassed)
5. **Form Ownership:** N/A (bypassed)

**Result:** **MANAGE** access (system admin bypasses all layers)

---

## Implementation Recommendations

### 1. Access Check Function (Using Database Function)

**Recommended Approach:** Use the centralized database function `[dbo].[fn_GetUserFormAccess]` for all access checks.

```python
async def get_user_form_access(
    db: Session,
    user_id: int,
    form_id: int
) -> Optional[Dict[str, Any]]:
    """
    Get user's effective access to a form using centralized database function.
    
    Returns: Dict with access information, or None if no access
    """
    from sqlalchemy import text
    
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
```

**Note:** The database function implements all access check priorities including:
- System Admin Override
- Resource Ownership
- Explicit FormAccessControl
- **Agency Event-Scoped Access** (NEW)
- Company Role Default
- No Access

See `docs/ACCESS-CONTROL-DATABASE-FUNCTION.md` for complete function implementation.

### 2. Access Enforcement

**Before allowing any form operation, check:**

1. **Does user have required access type?**
   - VIEW operations → Require VIEW or higher
   - SUBMIT operations → Require SUBMIT or higher
   - ANALYZE operations → Require ANALYZE or higher AND `CanViewReports=True`
   - EDIT operations → Require EDIT or higher AND `CanManageForms=True`
   - MANAGE operations → Require MANAGE AND `CanManageForms=True`

2. **Does user's company role permit the operation?**
   - `CanManageForms=False` → Cannot EDIT or MANAGE (hard constraint)
   - `CanViewReports=False` → Cannot ANALYZE (hard constraint)
   - `CanExportData=False` → Cannot export data (hard constraint)

3. **Is access expired?**
   - Check `FormAccessControl.ExpiryDate` if explicit entry exists

---

## Summary

### Key Takeaways

1. **4 Layers of Access Control for Forms:**
   - **System Role** → Platform-wide override
   - **Company Role** → Company-wide defaults
   - **Form Access Control** → Form-specific overrides
   - **Resource Ownership** → Creator privileges (always MANAGE)

   **Note:** Event Role is **NOT** a layer for form access - it only affects event management operations.

2. **Priority Order:**
   - System Admin > Ownership > Explicit > Company Role > No Access
   - **Event Role is NOT included** - it only affects event management

3. **Company Permissions are Hard Constraints:**
   - `CanManageForms=False` → Cannot EDIT/MANAGE forms
   - `CanViewReports=False` → Cannot ANALYZE forms
   - Cannot be overridden by form-level access

4. **Default Access Strategy:**
   - Company Admin → MANAGE (all company forms)
   - Company User → VIEW (all company forms, can be upgraded)
   - Company Viewer → VIEW (all company forms, can be upgraded)
   - External User → No access (requires explicit entry)

5. **Event Role Clarification:**
   - **Event role affects EVENT MANAGEMENT ONLY**, not form access
   - `event_participant` can still create/manage their own forms for the event
   - Event owners can see participant count to understand impact of event changes
   - Form access is determined by Company Role and Form Access Control, NOT by Event Role

6. **External Users Require Explicit Entry:**
   - Different company = No default access
   - Must create `FormAccessControl` entry for each form

7. **Resource Ownership Always Wins:**
   - Form creator always has MANAGE access (cannot be revoked)
   - Works even for `event_participant` users creating forms for existing events

This matrix provides the foundation for implementing comprehensive, multi-layer access control that respects both company-level permissions and form-specific requirements, with clear separation between event management and form access.

