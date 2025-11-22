# Form Access Control - Relationship Types Guide

## Company Role Dimension

### Overview

Every user is assigned a **Company Role** when they join a company. Company roles define the user's permissions within that company and can be used to simplify form access control.

### Company Roles (ref.UserCompanyRole)

| Role Code | Role Name | Role Level | CanManageCompany | CanManageUsers | CanManageEvents | CanManageForms | CanExportData | CanViewReports |
|-----------|-----------|------------|------------------|----------------|-----------------|----------------|---------------|----------------|
| `company_admin` | Company Administrator | 100 | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| `company_user` | Company User | 50 | ❌ No | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| `company_viewer` | Company Viewer | 10 | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No | ✅ Yes |

**Role Permissions:**
- **Company Admin**: Full access to manage company, users, events, forms, and reports
- **Company User**: Can create/edit own content (events, forms), export data, view reports, but cannot manage company settings or users
- **Company Viewer**: Read-only access - can view events, forms, and reports only

### Company Role to Form Access Type Mapping

**Simplified Model:** Use company role as **default form access** and allow `FormAccessControl` to override/upgrade access.

| Company Role | Default Form Access Type | Rationale |
|--------------|-------------------------|-----------|
| **Company Admin** | **MANAGE** | Admin has full company access, so default to full form access |
| **Company User** | **VIEW** | Standard user should start with view-only, can be upgraded if needed |
| **Company Viewer** | **VIEW** | Viewer role is read-only, so default to view-only |

**Access Upgrade Flow:**
1. User joins company with company role → gets **default form access** based on role
2. Form owner can **upgrade access** via `FormAccessControl` if needed (e.g., Company User → EDIT or SUBMIT)
3. Form owner can **downgrade access** via `FormAccessControl` if needed (e.g., Company Admin → VIEW for specific sensitive form)

**Benefits of This Model:**
- ✅ **Simpler**: Default access based on role, no need to grant access for every form
- ✅ **Secure**: Company Viewer always gets minimal access, Company Admin gets full access
- ✅ **Flexible**: Can override defaults via `FormAccessControl` for specific forms
- ✅ **Auditable**: Still track explicit access grants via `FormAccessControl` table
- ✅ **Intuitive**: User's company role determines their baseline form access

### Form Access Control Logic (Simplified)

**Access Check Priority:**
1. **Explicit `FormAccessControl` entry exists** → Use specified access type (overrides default)
2. **No explicit entry** → Use default based on company role:
   - Company Admin → MANAGE
   - Company User → VIEW
   - Company Viewer → VIEW
3. **User is form owner** → Always has MANAGE access (implicit, no entry needed)
4. **User is in form's company** → Gets default access based on role (implicit, no entry needed)
5. **External user (different company)** → Requires explicit `FormAccessControl` entry

**Implementation:**
```python
def get_user_form_access(user_id: int, form_id: int, company_role: str):
    # 1. Check explicit FormAccessControl entry
    explicit_access = db.query(FormAccessControl).filter(
        FormAccessControl.FormID == form_id,
        FormAccessControl.UserID == user_id,
        FormAccessControl.IsDeleted == False
    ).first()
    
    if explicit_access:
        return explicit_access.FormAccessControlAccessTypeID  # Use explicit access
    
    # 2. Check if user is form owner
    form = db.query(Form).filter(Form.FormID == form_id).first()
    if form.CreatedBy == user_id:
        return MANAGE_ACCESS_TYPE_ID  # Form owner always has MANAGE
    
    # 3. Check if user is in form's company
    user_company = db.query(UserCompany).filter(
        UserCompany.UserID == user_id,
        UserCompany.CompanyID == form.CompanyID,
        UserCompany.IsDeleted == False,
        UserCompany.StatusID == ACTIVE_STATUS_ID
    ).first()
    
    if user_company:
        # Use default based on company role
        if company_role == "company_admin":
            return MANAGE_ACCESS_TYPE_ID
        elif company_role == "company_user":
            return VIEW_ACCESS_TYPE_ID
        elif company_role == "company_viewer":
            return VIEW_ACCESS_TYPE_ID
    
    # 4. External user - no default access
    return None  # No access
```

### When to Use Explicit FormAccessControl

**Explicit `FormAccessControl` entries needed when:**
1. **External user** (different company) needs access → Always require explicit entry
2. **Upgrade access** for Company User/Viewer → Grant EDIT, SUBMIT, ANALYZE, or MANAGE
3. **Downgrade access** for Company Admin → Restrict to VIEW or EDIT for sensitive forms
4. **Time-bound access** → Set `ExpiryDate` for temporary access
5. **Relationship-based access** → Track access grant via specific relationship type

**Explicit `FormAccessControl` NOT needed when:**
1. User is in form's company → Uses default based on company role
2. User is form owner → Always has MANAGE access (implicit)
3. Company Admin accessing company forms → Uses default MANAGE access

---

## Understanding Relationship Types

### Branch vs Subsidiary - Key Differences

**Branch:**
- **Same Legal Entity**: A branch is a location/office of the **same company** (same ABN, same legal identity)
- **Example**: "Acme Corp Head Office" and "Acme Corp Melbourne Branch" are the same company, just different locations
- **Use Case**: When you have multiple offices/locations of the same company
- **Access Pattern**: Head office typically manages all branches; branches may need access to head office resources

**Subsidiary:**
- **Separate Legal Entity**: A subsidiary is a **separate company** that is owned or controlled by another company
- **Example**: "Acme Holdings Pty Ltd" owns "Acme Marketing Pty Ltd" - they are separate companies with separate ABNs
- **Use Case**: When one company owns/controls another company (parent-child relationship)
- **Access Pattern**: Parent company may need access to subsidiary resources; subsidiaries may need access to parent resources

**Key Distinction:**
- **Branch** = Same company, different location (one ABN, one legal entity)
- **Subsidiary** = Different companies, ownership relationship (separate ABNs, separate legal entities)

---

## Least Friction Access Grant Strategy

### Goal: Provide Access with Minimal Friction

**Recommended Approach: Invitation-Based Access Grant**

When granting access to a user from a company **not currently on the platform**:

1. **Send Invitation** (Don't Auto-Create)
   - User receives invitation email with form access context
   - Invitation includes: Company name, Form name, Access type, Relationship type
   - User onboards normally through existing invitation flow

2. **User Onboarding**
   - User accepts invitation and creates account (if new) or logs in (if existing)
   - Standard onboarding process applies
   - Company is created automatically if it doesn't exist (via invitation system)

3. **Automatic Access Grant**
   - When user accepts invitation and joins company, form access is automatically granted
   - User sees the company and associated form in their dashboard
   - Access is active immediately upon invitation acceptance

4. **Dashboard Experience**
   - User sees an extra company in their company switcher (the company that granted access)
   - Associated event/form is visible in that company's context
   - User can switch to that company and access the shared form

**Benefits:**
- ✅ Maintains data quality (user controls their own account)
- ✅ Follows existing invitation pattern (no new workflows)
- ✅ User sees context (company/form) in dashboard after onboarding
- ✅ Less risk of creating duplicate accounts
- ✅ User understands why they have access (invitation context)

### Linking Invitations to Form Access Requirements

**Current Schema Analysis:**

The `dbo.UserInvitation` table (27 columns) **already includes**:
- `UserCompanyRoleID` (BIGINT, FK to ref.UserCompanyRole, NOT NULL) - Company role to assign
- When invitation is accepted, `UserCompany` is created with the specified role
- Company role determines **default form access** (see Company Role Dimension above)

**Simplified Approach: Extend UserInvitation Table**

Add optional fields to `UserInvitation` for form access context:
- `FormID` (BIGINT, FK to dbo.Form, nullable) - **Optional**: If set, invitation is form-specific
- `FormAccessControlAccessTypeID` (INT, FK to ref.FormAccessControlAccessType, nullable) - **Optional**: Override default access type
- `CompanyRelationshipTypeID` (INT, FK to ref.CompanyRelationshipType, nullable) - **Optional**: Track relationship context
- `FormAccessExpiryDate` (DATETIME2, nullable) - **Optional**: Time-bound access

**Simplified Implementation Flow:**

**Scenario 1: Invite User to Company (General Invitation)**
1. User invites someone to join their company
2. System creates `UserInvitation` with `UserCompanyRoleID` (Company Admin, Company User, or Company Viewer)
3. `FormID` is NULL (general company invitation)
4. Invitation email sent with company context
5. User accepts invitation → creates account/joins company with specified role
6. **Default form access granted** based on company role (no explicit `FormAccessControl` entry needed)
   - Company Admin → MANAGE access to all company forms
   - Company User → VIEW access to all company forms
   - Company Viewer → VIEW access to all company forms
7. User sees company and all forms in dashboard (with appropriate access levels)

**Scenario 2: Invite User for Form-Specific Access (Form Access Invitation)**
1. User grants form access to non-platform user
2. System creates `UserInvitation` with:
   - `UserCompanyRoleID` (default to "company_viewer" for external users, or "company_user" if they should have more)
   - `FormID` set to the form ID
   - `FormAccessControlAccessTypeID` set to desired access type (default: VIEW, can be upgraded)
   - `CompanyRelationshipTypeID` set to relationship type
   - `FormAccessExpiryDate` if time-bound access
3. Invitation email sent with form context ("You've been invited to access Form X")
4. User accepts invitation → creates account/joins company with specified role
5. On invitation acceptance:
   - `UserCompany` created with `UserCompanyRoleID` from invitation
   - If `FormID` is set, **explicit `FormAccessControl` entry created**:
     - `FormID` = `UserInvitation.FormID`
     - `UserID` = Accepted user's ID
     - `CompanyID` = Invitation company ID (form owner's company)
     - `FormAccessControlAccessTypeID` = `UserInvitation.FormAccessControlAccessTypeID` (or default to VIEW if NULL)
     - `CompanyRelationshipTypeID` = `UserInvitation.CompanyRelationshipTypeID`
     - `ExpiryDate` = `UserInvitation.FormAccessExpiryDate`
     - `GrantedBy` = `UserInvitation.InvitedBy`
     - `GrantedDate` = `UserInvitation.AcceptedAt`
6. User sees company and specific form in dashboard with granted access level

**Default Access Strategy:**
- **Default to VIEW** for form-specific invitations (as user requested)
- Allow **upgrade after invitation acceptance** if more access needed
- Company role provides baseline permissions, explicit `FormAccessControl` provides form-specific overrides

**Benefits:**
- ✅ **Simpler workflow**: Company role determines default access, explicit grants only needed for upgrades
- ✅ **Default to VIEW**: Safe default for new users (as requested)
- ✅ **Flexible**: Can upgrade access after invitation acceptance
- ✅ **Auditable**: All access grants tracked via `FormAccessControl` table
- ✅ **Existing pattern**: Leverages current invitation system with company role assignment

### Dashboard Hierarchy Display

**Company Container System:**

Based on the existing dashboard hierarchy component (`hierarchyUtils.ts`), companies are displayed in containers based on their parent-child relationships:

**Display Rules:**
1. **Head Office Container**: Shows as root company container
2. **Branch Companies**: Display **inside** the Head Office container (nested)
3. **Subsidiary Companies**: Display **inside** the Parent company container (nested)
4. **Independent Companies**: Display as separate root containers (not nested)
   - Partner, Vendor, Client, Affiliate relationships do NOT create parent-child hierarchy
   - These show as separate companies in the dashboard

**Hierarchy Logic:**
- Uses `Company.ParentCompanyID` to determine nesting
- Branch relationships: Set `ParentCompanyID` = Head Office, `ChildCompanyID` = Branch
- Subsidiary relationships: Set `ParentCompanyID` = Parent Company, `ChildCompanyID` = Subsidiary
- Partner/Vendor/Client/Affiliate: Do NOT set `ParentCompanyID` (remain independent)

**Dashboard Experience:**
- User sees Head Office container
- Clicking expands to show Branch companies nested inside
- Each company container shows its events and forms
- User can switch between companies using company switcher
- Forms shared via access control appear in the appropriate company container

---

## Branch vs Head Office Determination

### The Challenge

When a user selects **Branch** as the relationship type and grants access to a company, how do we know:
- Is the form owner's company the Head Office?
- Is the grantee company the Branch?

### Solution: Relationship Direction (Option A - Recommended)

The `CompanyRelationship` table has:
- `ParentCompanyID`: The parent/primary company (typically Head Office)
- `ChildCompanyID`: The child/related company (typically Branch)

**When Granting Access:**

1. **If Form Owner is Parent Company:**
   - Form owner = Head Office
   - Grantee company = Branch
   - Relationship: `ParentCompanyID = form_owner_company_id`, `ChildCompanyID = grantee_company_id`

2. **If Form Owner is Child Company:**
   - Form owner = Branch
   - Grantee company = Head Office
   - Relationship: `ParentCompanyID = grantee_company_id`, `ChildCompanyID = form_owner_company_id`

**UI/UX Approach:**

When user selects "Branch" relationship type, show a question:
- **"Is this company a branch of yours, or are you a branch of this company?"**
- Radio buttons:
  - "They are a branch of my company" → Form owner = Parent, Grantee = Child
  - "I am a branch of their company" → Form owner = Child, Grantee = Parent

This determines `ParentCompanyID` and `ChildCompanyID` when creating the `CompanyRelationship`.

**Display in Dashboard:**
- Parent company (Head Office) shows as container
- Child company (Branch) shows nested inside parent container
- User can expand/collapse to see nested companies

---

## Access Types by Relationship Type

### Should Access Types Vary by Relationship Type?

**Yes - Different relationship types should have different access type recommendations:**

### Recommended Access Type Matrix

| Relationship Type | Recommended Access Types | Rationale |
|------------------|-------------------------|------------|
| **Branch** | Manage, Edit, View, Submit, Analyze | Same company, full trust, bidirectional access |
| **Subsidiary** | Manage, Edit, View, Submit, Analyze | Parent-child relationship, full access |
| **Partner** | View, Submit, Edit (limited) | Collaborative, project-specific, limited trust |
| **Vendor** | View, Submit | Service provider, needs to submit deliverables |
| **Client** | View, Submit | Customer, needs to submit forms/responses |
| **Affiliate** | View, Edit, Submit | Shared resources, moderate trust |

### Access Type Field-Level Definitions

Based on the `dbo.Form` table schema (23 columns), here are the field-level access definitions:

#### **VIEW Access** (`AccessTypeCode: 'VIEW'`)
**Can Access:**
- ✅ `FormID` - View form identifier
- ✅ `FormName` - View form name
- ✅ `FormDescription` - View form description
- ✅ `CompanyID` - View owning company (read-only)
- ✅ `EventID` - View associated event (read-only)
- ✅ `FormStatusID` - View form status (read-only)
- ✅ `FormApprovalStatusID` - View approval status (read-only)
- ✅ `IsPublic` - View public visibility setting (read-only)
- ✅ `FormThumbnailURL` - View thumbnail image
- ✅ `FormPreviewURL` - View preview URL
- ✅ `TotalSubmissions` - View submission count (read-only)
- ✅ `DemoLeadsCollected` - View demo leads count (read-only)
- ✅ `ProductionLeadsCollected` - View production leads count (read-only)
- ✅ `LastSubmissionDate` - View last submission date (read-only)
- ✅ `LastActivityDate` - View last activity date (read-only)
- ✅ `CreatedDate`, `CreatedBy` - View creation metadata (read-only)
- ✅ `UpdatedDate`, `UpdatedBy` - View update metadata (read-only)

**Cannot Access:**
- ❌ `DeploymentCost` - Financial information (restricted)
- ❌ Form content/fields (form builder data - separate domain)
- ❌ Form submissions/responses (requires ANALYZE access)
- ❌ Edit any fields
- ❌ Delete form
- ❌ Manage access control

**Operations Allowed:**
- View form in list/detail view
- View form preview
- View form status and metadata
- Cannot submit responses (requires SUBMIT access)

---

#### **EDIT Access** (`AccessTypeCode: 'EDIT'`)
**Includes all VIEW permissions, plus:**

**Can Modify:**
- ✅ `FormName` - Edit form name
- ✅ `FormDescription` - Edit form description
- ✅ `FormStatusID` - Change form status (within allowed transitions)
- ✅ `FormThumbnailURL` - Update thumbnail image
- ✅ `FormPreviewURL` - Update preview URL
- ✅ `EventID` - Associate/disassociate with events (within company)
- ✅ `IsPublic` - Change public visibility setting
- ✅ Form content/fields (form builder - separate domain, but requires EDIT access)

**Cannot Modify:**
- ❌ `CompanyID` - Cannot transfer form to different company
- ❌ `FormApprovalStatusID` - Cannot change approval status (requires approval workflow)
- ❌ `DeploymentCost` - Financial information (restricted)
- ❌ `TotalSubmissions`, `DemoLeadsCollected`, `ProductionLeadsCollected` - System-managed counters
- ❌ `LastSubmissionDate`, `LastActivityDate` - System-managed timestamps
- ❌ `CreatedDate`, `CreatedBy` - Audit fields (read-only)
- ❌ Delete form (requires MANAGE access)
- ❌ Manage access control (requires MANAGE access)

**Operations Allowed:**
- Edit form name, description, status
- Edit form content/structure (form builder)
- Associate form with events
- Change public visibility
- Cannot delete form
- Cannot grant/revoke access

---

#### **MANAGE Access** (`AccessTypeCode: 'MANAGE'`)
**Includes all VIEW and EDIT permissions, plus:**

**Can Modify:**
- ✅ All fields that EDIT can modify
- ✅ `FormApprovalStatusID` - Change approval status (if user has approval authority)
- ✅ `DeploymentCost` - Set deployment cost (financial control)
- ✅ Delete form - Soft delete (`IsDeleted = True`, `DeletedDate`, `DeletedBy`)
- ✅ Grant/revoke form access - Create/delete `FormAccessControl` entries
- ✅ Manage access control settings

**Cannot Modify:**
- ❌ `CompanyID` - Cannot transfer form to different company (company-level operation)
- ❌ `TotalSubmissions`, `DemoLeadsCollected`, `ProductionLeadsCollected` - System-managed (updated by submission system)
- ❌ `LastSubmissionDate`, `LastActivityDate` - System-managed (updated by activity tracking)
- ❌ `CreatedDate`, `CreatedBy` - Audit fields (read-only)

**Operations Allowed:**
- All EDIT operations
- Delete form (soft delete)
- Grant access to users/companies
- Revoke access from users/companies
- Manage form access control list
- Set deployment cost
- Change approval status (if authorized)

---

#### **SUBMIT Access** (`AccessTypeCode: 'SUBMIT'`)
**Includes all VIEW permissions, plus:**

**Can Access:**
- ✅ Submit form responses - Create form submission records
- ✅ View own submissions - View submissions they created
- ✅ Form submission endpoint - POST to form submission API

**Cannot Access:**
- ❌ Edit form content/structure
- ❌ View other users' submissions (requires ANALYZE access)
- ❌ View form analytics (requires ANALYZE access)
- ❌ Manage form settings
- ❌ Delete form

**Operations Allowed:**
- View form (read-only)
- Submit responses to form
- View own submission history
- Cannot see aggregate analytics or other users' data

---

#### **ANALYZE Access** (`AccessTypeCode: 'ANALYZE'`)
**Includes all VIEW permissions, plus:**

**Can Access:**
- ✅ `TotalSubmissions` - View total submission count
- ✅ `DemoLeadsCollected` - View demo leads count
- ✅ `ProductionLeadsCollected` - View production leads count
- ✅ `LastSubmissionDate` - View last submission timestamp
- ✅ `LastActivityDate` - View last activity timestamp
- ✅ View all form submissions - All users' submissions (not just own)
- ✅ View form analytics - Charts, reports, aggregate data
- ✅ Export form data - Export submissions/responses
- ✅ Form analytics endpoints - GET analytics/reports APIs

**Cannot Access:**
- ❌ Edit form content/structure (requires EDIT access)
- ❌ Submit responses (requires SUBMIT access - separate permission)
- ❌ Manage form settings (requires MANAGE access)
- ❌ Delete form (requires MANAGE access)

**Operations Allowed:**
- View form (read-only)
- View all submissions and responses
- View analytics and reports
- Export form data
- Cannot modify form or manage access

---

### Access Type Summary Table

| Access Type | Form Fields (Read) | Form Fields (Write) | Operations | Use Case |
|------------|-------------------|-------------------|------------|----------|
| **VIEW** | All metadata fields (read-only) | None | View form, view status | Read-only access |
| **EDIT** | All VIEW fields | FormName, FormDescription, FormStatusID, FormThumbnailURL, FormPreviewURL, EventID, IsPublic, Form content | Edit form content, change status | Content editor |
| **MANAGE** | All EDIT fields | All EDIT fields + FormApprovalStatusID, DeploymentCost, Delete form, Access control | Full form management | Form owner/admin |
| **SUBMIT** | All VIEW fields | Form submissions (create) | Submit responses | Form respondent |
| **ANALYZE** | All VIEW fields + Submission data, Analytics | None (read-only) | View analytics, export data | Data analyst |

**Note:** Access types are **additive** - users with higher access levels can perform all operations of lower levels. For example:
- MANAGE includes EDIT, VIEW, SUBMIT, ANALYZE
- EDIT includes VIEW
- ANALYZE includes VIEW (but not SUBMIT - these are separate)

---

## Complete Relationship Type Matrix

| Relationship Type | Legal Entity | Ownership | Use Case | Access Pattern | Recommended Access Types |
|------------------|--------------|-----------|----------|----------------|-------------------------|
| **Branch** | Same | N/A (same company) | Multiple locations/offices | Bidirectional, full access | Manage, Edit, View, Submit, Analyze |
| **Subsidiary** | Different | Parent owns child | Corporate hierarchy | Parent → Child, Child → Parent | Manage, Edit, View, Submit, Analyze |
| **Partner** | Different | Independent | Collaboration, agencies | Limited, project-specific | View, Submit, Edit (limited) |
| **Vendor** | Different | Independent | Supplier relationship | Vendor provides services | View, Submit |
| **Client** | Different | Independent | Customer relationship | Client receives services | View, Submit |
| **Affiliate** | Different | Related but not owned | Franchise, network | Shared resources, branding | View, Edit, Submit |

---

## Recommended Relationship Types for Your Platform

### Current Types (✅ Already exists):
1. **Branch** - Head office ↔ Branch relationships
2. **Subsidiary** - Parent company ↔ Subsidiary company
3. **Partner** - Agency relationships, collaborative partnerships

### Additional Types (✅ To be added):
4. **Vendor** - Supplier relationships
5. **Client** - Customer relationships
6. **Affiliate** - Franchise, network relationships

---

## Your Scenarios - Relationship Type Mapping

### Scenario 1: Head Office → Branch
**Relationship Type**: **Branch**

**Example:**
- Head Office: "Acme Corp Sydney"
- Branch: "Acme Corp Melbourne Branch"
- **Same company**, different location

**Access Pattern:**
- Head office grants access to branch users
- Branch users can access head office forms/resources
- Typically bidirectional access
- **Recommended Access**: Manage, Edit, View, Submit, Analyze

**Direction Determination:**
- Form owner (Head Office) = ParentCompanyID
- Grantee company (Branch) = ChildCompanyID
- **UI Question**: "They are a branch of my company"

**Dashboard Display:**
- Head Office shows as container
- Branch shows nested inside Head Office container

---

### Scenario 2: Branch → Head Office
**Relationship Type**: **Branch** (same relationship, reversed direction)

**Example:**
- Branch: "Acme Corp Melbourne Branch"
- Head Office: "Acme Corp Sydney"
- **Same company**, different location

**Access Pattern:**
- Branch can grant access to head office users
- Head office users can access branch forms/resources
- Same relationship type, just from branch perspective
- **Recommended Access**: Manage, Edit, View, Submit, Analyze

**Direction Determination:**
- Form owner (Branch) = ChildCompanyID
- Grantee company (Head Office) = ParentCompanyID
- **UI Question**: "I am a branch of their company"

**Dashboard Display:**
- Head Office shows as container
- Branch shows nested inside Head Office container

---

### Scenario 3: Company → Agency/Partner
**Relationship Type**: **Partner**

**Example:**
- Your Company: "Acme Corp"
- Agency: "Creative Marketing Agency"
- **Different companies**, collaborative relationship

**Access Pattern:**
- Company grants access to partner agency
- Partner agency can access specific forms/resources
- Typically limited, project-specific access
- **Recommended Access**: View, Submit, Edit (limited)

**Dashboard Display:**
- Partner company shows as **separate** container (not nested)
- No parent-child relationship in dashboard hierarchy

---

## Implementation Recommendations

### 1. Invitation-Based Access Grant
- ✅ Extend `UserInvitation` table with form access context fields
- ✅ Add `FormID`, `FormAccessControlAccessTypeID`, `CompanyRelationshipTypeID` to `UserInvitation`
- ✅ Auto-grant access when invitation accepted
- ✅ Show form/company in user dashboard after onboarding

### 2. Branch Direction Determination
- ✅ Ask user: "Are they a branch of yours, or are you a branch of theirs?"
- ✅ Store direction in CompanyRelationship (ParentCompanyID/ChildCompanyID)
- ✅ Display direction in UI for clarity
- ✅ Use direction to determine dashboard nesting

### 3. Access Type Recommendations
- ✅ Pre-select recommended access types based on relationship type
- ✅ Show warnings for non-recommended access types
- ✅ Allow override (flexibility is important)
- ✅ Default to "View" for safety
- ✅ Implement field-level access checks in backend

### 4. Dashboard Hierarchy
- ✅ Use `Company.ParentCompanyID` to determine nesting
- ✅ Branch/Subsidiary companies show nested in parent container
- ✅ Partner/Vendor/Client/Affiliate show as separate containers
- ✅ Forms shared via access control appear in appropriate company container

### 5. Additional Relationship Types
- ✅ Add Vendor, Client, Affiliate to database
- ✅ Update reference data seed scripts
- ✅ Update UI dropdowns and documentation

---

## Database Schema Notes

### UserInvitation Table Extension (Recommended)

**Current Schema:**
- `dbo.UserInvitation` already has `UserCompanyRoleID` (BIGINT, FK, NOT NULL) - Company role to assign

**Add to `dbo.UserInvitation`:**
```sql
ALTER TABLE [dbo].[UserInvitation]
ADD FormID BIGINT NULL,
    FormAccessControlAccessTypeID INT NULL,
    CompanyRelationshipTypeID INT NULL,
    FormAccessExpiryDate DATETIME2 NULL;

-- Foreign keys
ALTER TABLE [dbo].[UserInvitation]
ADD CONSTRAINT FK_UserInvitation_Form 
    FOREIGN KEY (FormID) REFERENCES [dbo].[Form](FormID);

ALTER TABLE [dbo].[UserInvitation]
ADD CONSTRAINT FK_UserInvitation_FormAccessControlAccessType 
    FOREIGN KEY (FormAccessControlAccessTypeID) REFERENCES [ref].[FormAccessControlAccessType](FormAccessControlAccessTypeID);

ALTER TABLE [dbo].[UserInvitation]
ADD CONSTRAINT FK_UserInvitation_CompanyRelationshipType 
    FOREIGN KEY (CompanyRelationshipTypeID) REFERENCES [ref].[CompanyRelationshipType](CompanyRelationshipTypeID);
```

**When Invitation Accepted:**
1. Create `UserCompany` record with `UserCompanyRoleID` from invitation (existing flow)
2. **Default form access granted** based on company role (no explicit `FormAccessControl` entry needed for internal users):
   - Company Admin → MANAGE access to all company forms (implicit)
   - Company User → VIEW access to all company forms (implicit)
   - Company Viewer → VIEW access to all company forms (implicit)
3. **If `UserInvitation.FormID` is NOT NULL** (form-specific invitation):
   - Create explicit `FormAccessControl` entry:
     - `FormID` = `UserInvitation.FormID`
     - `UserID` = Accepted user's ID
     - `CompanyID` = Invitation company ID (form owner's company)
     - `FormAccessControlAccessTypeID` = `UserInvitation.FormAccessControlAccessTypeID` **OR default to VIEW if NULL**
     - `CompanyRelationshipTypeID` = `UserInvitation.CompanyRelationshipTypeID`
     - `ExpiryDate` = `UserInvitation.FormAccessExpiryDate`
     - `GrantedBy` = `UserInvitation.InvitedBy`
     - `GrantedDate` = `UserInvitation.AcceptedAt`
   - This explicit entry **overrides** the default role-based access for this specific form

### CompanyRelationship Table
```sql
CompanyRelationship
├── ParentCompanyID (FK to Company) - Typically Head Office/Parent
├── ChildCompanyID (FK to Company) - Typically Branch/Subsidiary
├── RelationshipTypeID (FK to CompanyRelationshipType)
└── Status ('active', 'suspended', 'terminated')
```

**Direction Logic:**
- For Branch: Parent = Head Office, Child = Branch
- For Subsidiary: Parent = Parent Company, Child = Subsidiary
- For Partner/Vendor/Client/Affiliate: Direction less critical, but Parent = Grantor, Child = Grantee
- **Dashboard Nesting**: Only Branch and Subsidiary create parent-child hierarchy (use `Company.ParentCompanyID`)

---

## Simplified Model Summary

### Key Simplifications

1. **Company Role as Default Form Access**
   - Company Admin → MANAGE (full access to all company forms)
   - Company User → VIEW (view-only access to all company forms, can be upgraded)
   - Company Viewer → VIEW (view-only access to all company forms)

2. **Explicit FormAccessControl Only When Needed**
   - External users (different company) → Always require explicit entry
   - Upgrading access for Company User/Viewer → Grant higher access type
   - Downgrading access for Company Admin → Restrict to VIEW/EDIT for sensitive forms
   - Time-bound access → Set expiry date
   - Relationship tracking → Track via relationship type

3. **Default to VIEW for New Invitations**
   - Form-specific invitations default to VIEW access type
   - Can upgrade after invitation acceptance if more access needed
   - Safe default for external users

4. **Invitation Includes Company Role**
   - `UserInvitation.UserCompanyRoleID` already exists (NOT NULL)
   - Company role assigned when invitation accepted
   - Role determines default form access

### Access Check Priority

1. **Explicit `FormAccessControl` entry** → Use specified access type (overrides default)
2. **User is form owner** → MANAGE access (implicit)
3. **User is in form's company** → Default based on company role (implicit)
4. **External user** → No default access (requires explicit entry)

---

## Next Steps

1. **Immediate Actions:**
   - ✅ Exclude current user from company members list (DONE)
   - ✅ Add Vendor, Client, Affiliate relationship types to database
   - ✅ Update relationship type descriptions in database
   - ✅ Extend `UserInvitation` table with form access context fields
   - ✅ Implement role-based default form access logic in backend
   - ✅ Update access check functions to use company role defaults

2. **Short-term Enhancements:**
   - Implement invitation-based access grant flow (form-specific invitations)
   - Add branch direction selection UI
   - Add access type recommendations based on relationship type
   - Implement field-level access checks in backend
   - Add UI for upgrading form access after invitation acceptance

3. **Long-term Considerations:**
   - Access type templates per relationship type
   - Bulk access grant capabilities
   - Access review and audit workflows
   - Dashboard hierarchy visualization enhancements
   - Company role change impact on form access (revoke/downgrade if role changes)
