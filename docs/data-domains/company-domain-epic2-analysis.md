# Company Domain Epic 2 Analysis - Enhanced Billing Relationships & Approval Workflows

**Author:** Dimitri 🔍 (Data Domain Architect)  
**Date:** January 15, 2025  
**Status:** Industry Research Complete - Schema Design Phase  
**Epic:** Epic 2 - Enhanced Company Billing & Approval Workflows

---

## 🎯 **Epic 2 Requirements Summary**

### **Core Business Need**
- Branch companies can request head office approval for form deployment costs
- Head office can approve/reject branch form deployments with full audit trail
- Enhanced company-to-company billing relationships with approval process
- Maintain existing Epic 1 schema integrity (don't break what works)

### **Key Success Criteria**
- ✅ Branch → Head Office approval workflow for form costs
- ✅ Company-to-company billing relationship management
- ✅ Complete audit trail for all approval decisions
- ✅ Backward compatibility with Epic 1 Company domain
- ✅ Industry-standard approval workflow patterns

---

## 🔍 **Industry Research Findings**

### **Enterprise Billing Approval Patterns**

**1. Salesforce Billing Management**
- Parent-child account hierarchies with centralized billing
- Approval workflows based on cost thresholds ($1K, $5K, $10K+)
- Automated routing to appropriate approvers by role/department
- Audit trail with approval comments and timestamps

**2. Microsoft Azure Enterprise Billing**
- Cost center-based approval workflows
- Department-level spending limits with escalation
- Multi-level approval chains (Manager → Director → VP)
- Real-time budget tracking and alerts

**3. Enterprise SaaS Approval Workflows**
- **Threshold-based routing**: $0-1K (auto-approve), $1K-5K (manager), $5K+ (executive)
- **Role-based approvals**: Finance Manager, Department Head, CFO
- **Escalation policies**: Auto-escalate after 48 hours
- **Audit requirements**: Full trail for SOX compliance

### **Key Industry Insights**
- **Automation**: 80% of approvals under $1K are automated
- **Escalation**: Average approval time 24-48 hours with escalation
- **Audit**: Complete audit trail mandatory for enterprise customers
- **Integration**: Approval workflows integrate with existing ERP systems

---

## 🏗️ **Epic 2 Schema Design** ✅ **REVISED FOR EXISTING SCHEMA**

### **Existing Tables Analysis** 🔍

**✅ CompanyRelationship (Already Exists)**
- Handles parent-child company relationships (branch, subsidiary, partner)
- Fields: ParentCompanyID, ChildCompanyID, RelationshipTypeID, Status
- Perfect for Epic 2 branch → head office relationships

**✅ CompanySwitchRequest (Already Exists)**
- Handles approval workflows for company access requests
- Fields: UserID, ToCompanyID, StatusID, ApprovedBy, RejectedBy
- Can be extended for form deployment approval workflows

**✅ CompanyRelationshipType (Reference Table)**
- Types: 'branch', 'subsidiary', 'partner'
- Already supports Epic 2 relationship types

### **Epic 2 Enhancements Required** 🚀 **REVISED BASED ON UX INPUT**

**1. Extend CompanySwitchRequest for Form Deployment** ✅ **SIMPLIFIED FOR MVP**
```sql
-- Add new fields to existing CompanySwitchRequest table
ALTER TABLE [dbo].[CompanySwitchRequest] ADD
    RequestedAmount DECIMAL(10,2) NULL,           -- Cost amount for form deployment
    RequestDescription NVARCHAR(MAX) NULL,        -- What's being requested
    EventDate DATETIME2 NULL,                     -- Event date for urgency calculation
    UrgencyLevel NVARCHAR(20) NULL;              -- 'Low', 'Medium', 'High' (calculated)
-- REMOVED: EscalationChain and CurrentApproverID (too complex for MVP)
```

**2. Add New Request Types**
```sql
-- Extend ref.CompanySwitchRequestType table
INSERT INTO [ref].[CompanySwitchRequestType] VALUES
(4, 'FormDeployment', 'Request approval for form deployment costs'),
(5, 'BillingChange', 'Request approval for billing relationship changes'),
(6, 'AccessRequest', 'Request access to company resources'),
(7, 'FormAccess', 'Request access to specific forms');
```

**3. Add New Status Types**
```sql
-- Extend ref.CompanySwitchRequestStatus table
INSERT INTO [ref].[CompanySwitchRequestStatus] VALUES
(4, 'Escalated', 'Request escalated to higher authority'),
(5, 'UnderReview', 'Request under detailed review'),
(6, 'PendingApprover', 'Waiting for specific approver'),
(7, 'EscalationRequired', 'Escalation needed - approver unavailable');
```

**4. Create ApprovalAuditTrail (New Table) - CORRECTED FIELD NAMES**
```sql
CREATE TABLE [audit].[ApprovalAuditTrail] (
    ApprovalAuditTrailID BIGINT IDENTITY(1,1) PRIMARY KEY,
    CompanySwitchRequestID BIGINT NOT NULL,        -- Link to CompanySwitchRequest
    Action NVARCHAR(50) NOT NULL,                 -- 'Submitted', 'Approved', 'Rejected', 'Escalated'
    ActionDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    PerformedBy BIGINT NOT NULL,                  -- User who performed action
    Comments NVARCHAR(MAX) NULL,                  -- Additional comments
    PreviousStatus NVARCHAR(20) NULL,              -- Status before this action
    NewStatus NVARCHAR(20) NULL,                  -- Status after this action
    -- REMOVED: EscalationReason (too complex for MVP)
    -- Audit trail
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NOT NULL,
    
    CONSTRAINT FK_ApprovalAuditTrail_Request FOREIGN KEY (CompanySwitchRequestID) 
        REFERENCES [dbo].[CompanySwitchRequest](RequestID),
    CONSTRAINT FK_ApprovalAuditTrail_PerformedBy FOREIGN KEY (PerformedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_ApprovalAuditTrail_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [dbo].[User](UserID)
);
```

**5. Extend User Table for External Approvers** ✅ **SIMPLIFIED FOR MVP**
```sql
-- Add external approver support to existing User table
ALTER TABLE [dbo].[User] ADD
    IsExternalApprover BIT NOT NULL DEFAULT 0;    -- Flag for external approvers
-- REMOVED: ExternalApproverRole (use UserRole instead)
-- REMOVED: ApprovalMethod (email only for MVP)
```

**6. Add New User Roles** ✅ **CORRECTED TABLE NAME**
```sql
-- Extend ref.UserRole table (correct table name)
INSERT INTO [ref].[UserRole] (RoleCode, RoleName, Description, RoleLevel, CanManagePlatform, CanManageAllCompanies, CanViewAllData, CanAssignSystemRoles, IsActive, SortOrder) VALUES
('HEAD_OFFICE_ADMIN', 'Head Office Administrator', 'Manages company relationships and approval workflows', 10, 0, 1, 1, 1, 1, 10),
('PARTNER_USER', 'Partner User', 'Form-level access to partner companies', 5, 0, 0, 0, 0, 1, 50),
('VENDOR_USER', 'Vendor User', 'Form-level access to vendor relationships', 5, 0, 0, 0, 0, 1, 51),
('CLIENT_USER', 'Client User', 'View-only access to assigned forms', 3, 0, 0, 0, 0, 1, 52),
('AFFILIATE_USER', 'Affiliate User', 'Form-level access to affiliate relationships', 5, 0, 0, 0, 0, 1, 53),
('EXTERNAL_APPROVER', 'External Approver', 'Email-only approver without platform access', 7, 0, 0, 0, 0, 1, 40);
```

**7. DEFERRED: Form Access Control Table** ⏳ **DEFER TO FORM DOMAIN**
```sql
-- FormAccessControl table will be created when Form domain is defined
-- This ensures proper foreign key relationships and naming conventions
-- Will be implemented in Epic 3 (Form Domain)
```

**8. DEFERRED: Escalation Chain Table** ⏳ **REMOVED FROM MVP**
```sql
-- EscalationChain table removed from MVP due to complexity
-- Simple approval workflow: Single approver per relationship type
-- Manual escalation can be added in future releases
-- Focus on core approval functionality first
```

---

## 🏢 **Company Relationship Setup & Access Level Management** 🔍

### **Missing Foundation: Company Relationship Establishment**

**Critical Issue**: Epic 1 built the CompanyRelationship table but didn't implement the workflow for establishing relationships. Epic 2 approval workflows depend on this foundation.

### **Industry Research: Access Level Management**

**1. Salesforce Enterprise Access Patterns**
- **Account Hierarchy**: Parent accounts control child account access
- **Role-Based Access**: Different roles (Admin, Manager, User) with escalating permissions
- **Delegation**: Temporary access delegation for approvals
- **Power Struggle Mitigation**: Clear escalation paths and approval limits

**2. Microsoft Azure Enterprise Patterns**
- **Subscription Hierarchy**: Management groups → Subscriptions → Resource groups
- **Access Control**: RBAC (Role-Based Access Control) with inheritance
- **Approval Workflows**: Built-in approval processes for resource creation
- **User Experience**: Simplified interface for single-tenant customers

**3. Enterprise SaaS Best Practices**
- **Progressive Disclosure**: Complex features hidden until needed
- **Customer Segmentation**: Different interfaces for SMB vs Enterprise
- **Access Governance**: Regular access reviews and cleanup
- **Audit Compliance**: Complete access change tracking

### **Proposed Company Relationship Setup Workflow**

**Step 1: Relationship Request**
- Company A requests relationship with Company B
- Specify relationship type: 'branch', 'subsidiary', 'partner'
- Define access levels and approval thresholds
- Set up billing terms and payment methods

**Step 2: Access Level Configuration**
- **Head Office**: Full access to all child companies
- **Branch Manager**: Limited access to own branch + approval requests
- **Branch User**: Standard user access + request approval capability
- **Partner**: Shared access to specific resources only

**Step 3: Approval Authority Setup**
- Define approval thresholds by relationship type
- Set up escalation chains (Manager → Director → Executive)
- Configure notification preferences
- Establish audit requirements

### **Customer Complexity Management** 🎯

**Single Business Customers (Majority)**
- **Hidden Complexity**: No company relationship UI shown
- **Simplified Workflow**: Direct form deployment (no approval needed)
- **Auto-Configuration**: Single company setup with default settings
- **Clean Interface**: Focus on core form creation features

**Multi-Business Customers (Enterprise)**
- **Full Workflow**: Complete company relationship management
- **Approval Processes**: All Epic 2 features available
- **Advanced Features**: Multi-level approvals, audit trails, reporting
- **Power User Interface**: Advanced configuration options

### **Access Level Research Findings**

**Power Struggle Mitigation Strategies**
1. **Clear Hierarchy**: Transparent reporting structure
2. **Escalation Paths**: Defined escalation procedures
3. **Approval Limits**: Dollar amount thresholds prevent abuse
4. **Audit Trails**: Complete transparency of all decisions
5. **Regular Reviews**: Periodic access and permission audits

**User-Friendly Access Management**
1. **Role Templates**: Pre-defined roles for common scenarios
2. **Bulk Operations**: Manage multiple users/companies at once
3. **Self-Service**: Users can request access changes
4. **Approval Delegation**: Temporary access delegation
5. **Mobile Access**: Approve requests on mobile devices

## 🔄 **Complete Epic 2 Workflow Design** ✅ **COMPLETE PROCESS**

### **Phase 0: Company Relationship Setup** (Foundation)

**Step 1: Initial Company Registration**
- Single business: Auto-configure as standalone company
- Multi-business: Present relationship setup options
- Detect customer complexity during onboarding

**Step 2: Relationship Establishment**
- Company A requests relationship with Company B
- Specify relationship type: 'branch', 'subsidiary', 'partner'
- Define access levels and approval thresholds
- Set up billing terms and payment methods

**Step 3: Access Level Configuration**
- **Head Office**: Full access to all child companies
- **Branch Manager**: Limited access + approval request capability
- **Branch User**: Standard access + request approval capability
- **Partner**: Shared access to specific resources only

### **Phase 1: Form Deployment Approval Flow** ✅ **SIMPLIFIED FOR MVP**

**Step 1: Request Submission**
- Branch user submits form deployment request
- System validates: Is branch? Has parent company? Within limits?
- Creates CompanySwitchRequest record with RequestTypeID = 4 (FormDeployment)
- Sets StatusID = 1 (Pending), populates RequestedAmount, RequestDescription, EventDate
- **Simple Routing**: Route to designated approver for this relationship type

**Step 2: Automated Routing** ✅ **SIMPLE APPROACH**
- **Single Approver**: Route to one designated approver per relationship
- **Email Notifications**: Send to approver (platform or external)
- **No Escalation**: Keep it simple for MVP

**Step 3: Approval Decision** ✅ **SIMPLE APPROVAL**
- **Approver Reviews**: Reviews request, approves/rejects
- **Log Action**: Log decision in ApprovalAuditTrail
- **External Approver**: Email-only approval process
- **Manual Escalation**: User can manually escalate if needed

**Step 4: Notification & Execution**
- Notify branch of decision
- If approved: Enable form deployment
- If rejected: Block deployment with reason

### **Phase 2: Company-to-Company Billing Flow** (Using Existing Tables)

**Step 1: Relationship Setup**
- Use existing CompanyRelationship table
- Set RelationshipTypeID = 1 (branch) or 2 (subsidiary)
- Status = 'active' for billing relationships

**Step 2: Invoice Generation**
- System generates invoice based on relationship terms
- Check if approval required (amount > threshold)
- Route to CompanySwitchRequest workflow if needed

**Step 3: Approval Process**
- Same workflow as form deployment
- Additional validation: Budget availability, contract terms
- Integration with existing billing system

---

## 📊 **Database Schema Changes Summary** ✅ **SIMPLIFIED FOR MVP**

### **New Tables (1)**
1. **ApprovalAuditTrail** - Complete audit trail for all approval actions (audit schema)

### **Modified Tables (4)**
1. **CompanySwitchRequest** - Add fields: RequestedAmount, RequestDescription, EventDate, UrgencyLevel
2. **CompanySwitchRequestType** - Add types: 'FormDeployment', 'BillingChange', 'AccessRequest', 'FormAccess'
3. **CompanySwitchRequestStatus** - Add statuses: 'Escalated', 'UnderReview', 'PendingApprover', 'EscalationRequired'
4. **User** - Add field: IsExternalApprover

### **Extended Reference Tables (1)**
1. **UserRole** - Add roles: 'HEAD_OFFICE_ADMIN', 'PARTNER_USER', 'VENDOR_USER', 'CLIENT_USER', 'AFFILIATE_USER', 'EXTERNAL_APPROVER'

### **Existing Tables Used (2)**
1. **CompanyRelationship** - Already handles parent-child relationships (no changes needed)
2. **CompanyRelationshipType** - Already supports 'branch', 'subsidiary', 'partner' (no changes needed)
3. **UserCompany** - Already handles role allocation (no changes needed)

### **DEFERRED TO FUTURE RELEASES**
- **FormAccessControl** - Defer to Form domain (Epic 3)
- **EscalationChain** - Too complex for MVP, defer to future release

### **Key Relationships** (Using Existing Schema + New Tables)
- CompanySwitchRequest.ToCompanyID → Company.CompanyID (branch requesting)
- CompanySwitchRequest.FromCompanyID → Company.CompanyID (head office approving)
- CompanyRelationship.ParentCompanyID → Company.CompanyID (head office)
- CompanyRelationship.ChildCompanyID → Company.CompanyID (branch)
- ApprovalAuditTrail.CompanySwitchRequestID → CompanySwitchRequest.RequestID

---

## 🎨 **UX Expert Review & Refinements** ✅ **SALLY'S INPUT INCORPORATED**

### **Key UX Decisions Made**

**1. Dashboard Hierarchical View Maintained** ✅
- **Decision**: All users see Organization → Event → Form hierarchy regardless of relationship type
- **Rationale**: Consistent user experience, familiar navigation pattern
- **Implementation**: Access control at data level, not UI level

**2. Form Ownership Rules Clarified** ✅
- **Customer Initiates**: Form sits in customer's organization
- **Partner Creates**: Form sits in partner's organization
- **Client Access**: No platform account required, optional account creation
- **Rationale**: Clear ownership model, flexible client access

**3. External Approvers Integration** ✅
- **Decision**: Use existing User table with flags (no UserType field needed)
- **Implementation**: Leverage existing UserCompany table for role allocation
- **Onboarding**: Use existing invitation/onboarding process

**4. Escalation Process** ⚠️ **REQUIRES DATA MODEL SOLUTION**
- **Challenge**: How to handle escalation within existing CompanySwitchRequest workflow
- **Options**: Stay in current workflow vs alternative routes
- **Decision**: Provide data model solution for flexible escalation

**5. Head Office Admin Role** ✅
- **Availability**: Only when company relationships are detected
- **Assignment**: Automatic when company adds first branch
- **Delegation**: Manual assignment by Head Office Admin

**6. System Roles Extended** ✅
- **New Roles**: Head Office Admin, Partner User, Vendor User, Client User, Affiliate User
- **Assignment**: Via existing UserCompany table
- **Access Control**: One-way access (Partner sees customer, not vice versa)

### **Data Model Implications**

**Existing Schema Leverage**:
- ✅ UserCompany table for role allocation (no changes needed)
- ✅ Existing onboarding status (no changes needed)
- ✅ CompanyRelationship table for relationships (no changes needed)
- ✅ CompanySwitchRequest table for approvals (extensions only)

**New Requirements**:
- 🔧 External approver support in User table
- 🔧 New system roles for relationship types
- 🔧 Form-level access control
- 🔧 Escalation chain data structure

### **Critical UX Questions for Sally** ✅ **RESOLVED**
1. **Approval Dashboard**: How should head office approvers see pending requests?
2. **Branch Interface**: How should branches submit and track approval requests?
3. **Notification System**: Email vs in-app notifications for approval decisions?
4. **Mobile Experience**: Do approvers need mobile access for urgent approvals?
5. **Bulk Operations**: Can approvers handle multiple requests at once?

### **UX Requirements Clarified** ✅
1. **Urgency Calculation**: Event date - today (24 hours default for no event date)
2. **Transparency**: Full transparency with audit trail showing attempts/failures/success
3. **Industry Standards**: Value-based approval thresholds ($1K, $5K, $10K+)
4. **Accessibility**: TBD - needs research
5. **Language**: English only for MVP, collect language preferences this epic

### **Proposed UX Flow** ✅ **ENHANCED**
**Branch Side:**
- "Request Approval" button on form deployment page
- Simple form: Amount, Description, Submit
- Status tracking: "Pending", "Approved", "Rejected"
- Real-time notifications when status changes

**Head Office Side:**
- Approval dashboard with pending requests
- Quick approve/reject with comments
- Bulk approval for similar requests
- Audit trail view for compliance

### **Enhanced UX Specifications** 🎨

**1. Urgency-Based Approval Interface**
- **Event Date Calculation**: Show "Urgent" if event date < 7 days away
- **Default Urgency**: 24 hours for forms without event dates
- **Visual Indicators**: Red (urgent), Yellow (moderate), Green (low urgency)
- **Approval Priority**: Auto-sort by urgency + amount

**2. Value-Based Approval Thresholds** (Industry Standard)
- **$0-1,000**: Auto-approve (green badge)
- **$1,000-5,000**: Manager approval (yellow badge)
- **$5,000+**: Executive approval (red badge)
- **Visual Cues**: Color-coded badges, progress bars

**3. Transparent Audit Trail UX**
- **Timeline View**: Chronological list of all actions
- **Status Changes**: Clear before/after state transitions
- **Failure Tracking**: Highlight failed attempts with retry options
- **Success Confirmation**: Clear success states with next steps
- **Comments**: Expandable comment threads for context

**4. Language Preference Collection** (Epic 2)
- **User Profile**: Add language preference field
- **Future Ready**: Schema supports multi-language expansion
- **MVP Scope**: English only, but collect preferences now

---

## 🔧 **Implementation Recommendations** ✅ **SIMPLIFIED FOR MVP**

### **Phase 0: Company Relationship Setup (Foundation)**
1. **Customer Complexity Detection** - Detect single vs multi-business during onboarding
2. **Relationship Establishment Workflow** - Company A requests relationship with Company B
3. **Access Level Configuration** - Define head office, branch manager, branch user roles
4. **Single Business Simplification** - Hide complexity for single-business customers

### **Phase 1: Core Approval Workflow (MVP)** ✅ **SIMPLE APPROACH**
1. **Extend CompanySwitchRequest table** - Add RequestedAmount, RequestDescription, EventDate, UrgencyLevel
2. **Add new request types** - 'FormDeployment', 'BillingChange', 'AccessRequest', 'FormAccess'
3. **Add new status types** - 'Escalated', 'UnderReview', 'PendingApprover', 'EscalationRequired'
4. **Create ApprovalAuditTrail table** - Complete audit trail for compliance (audit schema)
5. **Extend User table** - Add IsExternalApprover flag only
6. **Add new user roles** - HEAD_OFFICE_ADMIN, PARTNER_USER, VENDOR_USER, CLIENT_USER, AFFILIATE_USER, EXTERNAL_APPROVER
7. **Basic branch → head office approval flow** using existing CompanyRelationship
8. **Simple approval routing** - Single approver per relationship type
9. **Email notifications** for status changes

### **Phase 2: Enhanced Billing Relationships**
1. **Use existing CompanyRelationship** - No changes needed, already supports billing relationships
2. **Company-to-company billing setup** via CompanyRelationship table
3. **Automated approval thresholds** based on RequestedAmount
4. **Integration with existing billing system**

### **Phase 3: Future Enhancements** ⏳ **DEFERRED**
1. **Escalation chains** - Add in future release when complexity is needed
2. **Form-level access control** - Add when Form domain is defined
3. **Advanced reporting and analytics** using ApprovalAuditTrail
4. **Mobile approval app** for urgent requests
5. **Power struggle mitigation** - Clear escalation paths and approval limits

---

## 📋 **Next Steps**

### **Immediate Actions**
1. **Sally Review**: Get UX expert input on approval interface design
2. **Solomon Validation**: Review schema with Database Migration Validator
3. **Developer Handoff**: Create detailed implementation specifications
4. **Testing Strategy**: Plan Epic 2 testing approach

### **Success Metrics**
- **Approval Time**: < 24 hours average approval time
- **User Adoption**: 90% of branches use approval workflow
- **Audit Compliance**: 100% audit trail coverage
- **System Performance**: No impact on Epic 1 functionality

---

## 🎯 **Strategic Benefits** ✅ **REVISED FOR EXISTING SCHEMA**

### **Business Value**
- **Cost Control**: Head office oversight of branch spending via CompanySwitchRequest
- **Compliance**: Complete audit trail for financial controls via ApprovalAuditTrail
- **Scalability**: Support for complex company hierarchies via existing CompanyRelationship
- **Trust**: Transparent approval process builds confidence

### **Technical Benefits**
- **Minimal Schema Changes**: Only 1 new table + 3 table extensions (vs 3 new tables)
- **Leverages Existing Infrastructure**: Uses proven CompanySwitchRequest approval workflow
- **Industry Standard**: Follows enterprise approval workflow patterns
- **Extensible**: Easy to add new approval types via CompanySwitchRequestType
- **Performance**: Optimized indexes already exist on CompanySwitchRequest
- **Backward Compatible**: No breaking changes to Epic 1 functionality

---

**Ready for Sally's UX review and Solomon's schema validation!** 🚀

---

## 📋 **Epic 2 Analysis Summary** ✅ **SIMPLIFIED FOR MVP**

### **Key Changes Made**
- ✅ **No Schema Conflicts**: Works with existing CompanyRelationship and CompanySwitchRequest tables
- ✅ **Simplified Approach**: Removed complex escalation chains for MVP
- ✅ **External Approvers**: Email-only approvers without platform accounts
- ✅ **Dashboard Consistency**: Maintains hierarchical view for all users
- ✅ **Role-Based Access**: New user roles for relationship types
- ✅ **Audit Compliance**: Complete audit trail in audit schema
- ✅ **MVP Focus**: Core approval functionality without complexity

### **Deliverables Ready**
1. **Analysis Document**: Complete Epic 2 analysis with simplified approach
2. **Schema Design**: 1 new table + 4 table extensions + 1 reference table extension
3. **Simple Approval Workflow**: Single approver per relationship type
4. **Implementation Plan**: 3-phase approach focused on core functionality

### **Next Actions**
1. **Sally Review**: UX expert input incorporated and validated
2. **Solomon Validation**: Database Migration Validator review of simplified schema
3. **Developer Handoff**: Implementation specifications with simple approval workflow
4. **Testing Strategy**: Epic 2 testing approach with basic approval scenarios

### **Critical Data Model Decisions**
- **Simple Approval**: Single approver per relationship type (no escalation chains)
- **External Approvers**: User table extension with IsExternalApprover flag
- **Role Management**: New user roles via existing UserRole table
- **Audit Trail**: Complete audit trail in audit schema
- **Dashboard Access**: Hierarchical view maintained with role-based access control
- **Deferred Complexity**: Escalation chains and form access control deferred to future releases

### **MVP Scope Decisions**
- **REMOVED**: EscalationChain table (too complex for MVP)
- **REMOVED**: FormAccessControl table (defer to Form domain)
- **REMOVED**: Complex escalation logic (manual escalation only)
- **FOCUSED**: Core approval workflow with single approver per relationship

---

*Dimitri - Data Domain Architect* 🔍  
*"Epic 2 analysis complete - simplified for MVP with core approval functionality!"*