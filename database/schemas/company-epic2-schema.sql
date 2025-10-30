-- =====================================================================
-- Company Domain Epic 2 Schema - Enhanced Billing Relationships & Approval Workflows
-- =====================================================================
-- Author: Dimitri (Data Domain Architect)
-- Date: January 15, 2025
-- Version: 2.0.0
-- =====================================================================
-- Purpose:
--   Epic 2 enhancements to Company domain:
--   1. Branch → Head Office approval workflows for form deployment costs
--   2. Company-to-company billing relationships with approval process
--   3. Complete audit trail for all approval decisions
--   4. Maintains Epic 1 schema integrity (no breaking changes)
-- 
-- Strategy:
--   Additive approach - new tables only, no modifications to existing Epic 1 tables
--   Foreign key relationships to existing Company table
--   Follows Solomon's standards: PascalCase, NVARCHAR, UTC timestamps
-- =====================================================================
-- Industry Research:
--   - Salesforce: Parent-child account hierarchies with centralized billing
--   - Microsoft Azure: Cost center-based approval workflows with escalation
--   - Enterprise SaaS: Threshold-based routing ($0-1K auto, $1K-5K manager, $5K+ exec)
--   - Audit Requirements: Complete trail for SOX compliance
-- =====================================================================

USE [EventLeadPlatform];
GO

-- =====================================================================
-- TABLE 1: CompanyApprovalWorkflow (Core Approval Requests)
-- =====================================================================
-- Purpose: Tracks approval requests from branches to head office
-- Key Insight: Supports multiple workflow types (FormDeployment, BillingChange, etc.)
-- =====================================================================
CREATE TABLE [CompanyApprovalWorkflow] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    WorkflowID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Company Relationships (Branch → Head Office)
    -- =====================================================================
    CompanyID BIGINT NOT NULL,
    -- ^ Branch company requesting approval (foreign key to Company)
    -- Example: "Acme Events Melbourne" (branch) requesting form deployment
    
    ParentCompanyID BIGINT NOT NULL,
    -- ^ Head office company that approves requests (foreign key to Company)
    -- Example: "Acme Holdings" (parent) approves branch requests
    
    -- =====================================================================
    -- Workflow Details
    -- =====================================================================
    WorkflowType NVARCHAR(50) NOT NULL,
    -- ^ Type of approval request: 'FormDeployment', 'BillingChange', 'BudgetIncrease'
    -- Extensible: Can add new types without schema changes
    -- Business rule: Different types may have different approval rules
    
    Status NVARCHAR(20) NOT NULL DEFAULT 'Pending',
    -- ^ Current status: 'Pending', 'Approved', 'Rejected', 'Escalated'
    -- Pending = Awaiting approval
    -- Approved = Request approved, can proceed
    -- Rejected = Request denied, cannot proceed
    -- Escalated = Moved to higher authority
    
    RequestedAmount DECIMAL(10,2) NULL,
    -- ^ Cost amount for this request (NULL if not applicable)
    -- Example: $500.00 for form deployment costs
    -- Used for: Budget validation, approval thresholds
    
    RequestDescription NVARCHAR(MAX) NOT NULL,
    -- ^ Detailed description of what's being requested
    -- Example: "Deploy customer feedback form for Q1 survey campaign"
    -- Required: Approvers need context to make decisions
    
    -- =====================================================================
    -- Submission Details
    -- =====================================================================
    SubmittedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    -- ^ When request was submitted (UTC)
    -- Used for: SLA tracking, escalation timers
    
    SubmittedBy BIGINT NOT NULL,
    -- ^ User who submitted the request (foreign key to User)
    -- Used for: Notifications, audit trail, follow-up questions
    
    -- =====================================================================
    -- Approval Details
    -- =====================================================================
    ApprovedDate DATETIME2 NULL,
    -- ^ When request was approved/rejected (UTC)
    -- NULL = Still pending approval
    
    ApprovedBy BIGINT NULL,
    -- ^ User who approved/rejected the request (foreign key to User)
    -- NULL = Not yet approved/rejected
    
    RejectionReason NVARCHAR(MAX) NULL,
    -- ^ Why request was rejected (if applicable)
    -- Example: "Exceeds quarterly budget limit"
    -- Helps branches understand and improve future requests
    
    -- =====================================================================
    -- Audit Trail (Standard for ALL tables - Solomon's requirement)
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NOT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT FK_CompanyApprovalWorkflow_Company FOREIGN KEY (CompanyID) 
        REFERENCES [Company](CompanyID),
    
    CONSTRAINT FK_CompanyApprovalWorkflow_ParentCompany FOREIGN KEY (ParentCompanyID) 
        REFERENCES [Company](CompanyID),
    
    CONSTRAINT FK_CompanyApprovalWorkflow_SubmittedBy FOREIGN KEY (SubmittedBy) 
        REFERENCES [User](UserID),
    
    CONSTRAINT FK_CompanyApprovalWorkflow_ApprovedBy FOREIGN KEY (ApprovedBy) 
        REFERENCES [User](UserID),
    
    CONSTRAINT FK_CompanyApprovalWorkflow_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [User](UserID),
    
    CONSTRAINT FK_CompanyApprovalWorkflow_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [User](UserID),
    
    -- Validate WorkflowType values
    CONSTRAINT CK_CompanyApprovalWorkflow_Type CHECK (
        WorkflowType IN ('FormDeployment', 'BillingChange', 'BudgetIncrease', 'ContractRenewal')
    ),
    
    -- Validate Status values
    CONSTRAINT CK_CompanyApprovalWorkflow_Status CHECK (
        Status IN ('Pending', 'Approved', 'Rejected', 'Escalated')
    ),
    
    -- Ensure ApprovedDate is set when ApprovedBy is set
    CONSTRAINT CK_CompanyApprovalWorkflow_ApprovalIntegrity CHECK (
        (ApprovedBy IS NULL AND ApprovedDate IS NULL) OR
        (ApprovedBy IS NOT NULL AND ApprovedDate IS NOT NULL)
    ),
    
    -- Prevent company from being its own parent
    CONSTRAINT CK_CompanyApprovalWorkflow_NoSelfParent CHECK (CompanyID != ParentCompanyID)
);
GO

-- Index for pending approvals (head office dashboard queries)
CREATE INDEX IX_CompanyApprovalWorkflow_Pending ON [CompanyApprovalWorkflow](ParentCompanyID, Status, SubmittedDate)
    WHERE Status = 'Pending' AND IsDeleted = 0;
GO

-- Index for branch request history
CREATE INDEX IX_CompanyApprovalWorkflow_BranchHistory ON [CompanyApprovalWorkflow](CompanyID, SubmittedDate)
    WHERE IsDeleted = 0;
GO

PRINT 'CompanyApprovalWorkflow table created successfully!';
GO

-- =====================================================================
-- TABLE 2: CompanyBillingRelationship (Company-to-Company Billing)
-- =====================================================================
-- Purpose: Manages billing relationships between companies
-- Key Insight: Supports parent-child, partnership, and vendor relationships
-- =====================================================================
CREATE TABLE [CompanyBillingRelationship] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    RelationshipID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Company Relationships (Payer ↔ Payee)
    -- =====================================================================
    PayerCompanyID BIGINT NOT NULL,
    -- ^ Company that pays invoices (foreign key to Company)
    -- Example: "Acme Holdings" pays for "Acme Events Melbourne" invoices
    
    PayeeCompanyID BIGINT NOT NULL,
    -- ^ Company that receives invoices (foreign key to Company)
    -- Example: "EventLead Platform" receives payment from "Acme Holdings"
    
    -- =====================================================================
    -- Relationship Details
    -- =====================================================================
    RelationshipType NVARCHAR(50) NOT NULL,
    -- ^ Type of billing relationship: 'ParentChild', 'Partnership', 'Vendor'
    -- ParentChild = Subsidiary bills parent company
    -- Partnership = Equal partnership billing
    -- Vendor = Service provider billing
    
    BillingTerms NVARCHAR(MAX) NULL,
    -- ^ JSON object containing billing terms and conditions
    -- Example: {"paymentTerms": "Net 30", "currency": "AUD", "discount": "2%"}
    -- Flexible: Can store any billing configuration
    
    ApprovalRequired BIT NOT NULL DEFAULT 1,
    -- ^ Does this relationship require approval for invoices?
    -- 1 = All invoices require approval
    -- 0 = Auto-approve all invoices (trusted relationship)
    
    MaxApprovalAmount DECIMAL(10,2) NULL,
    -- ^ Auto-approve invoices under this amount (NULL = no auto-approval)
    -- Example: $1000.00 - invoices under $1K auto-approved
    -- Used for: Reducing approval overhead for small amounts
    
    -- =====================================================================
    -- Relationship Lifecycle
    -- =====================================================================
    StartDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    -- ^ When billing relationship became active (UTC)
    
    EndDate DATETIME2 NULL,
    -- ^ When billing relationship ends (NULL = ongoing)
    -- Used for: Contract renewals, relationship termination
    
    Status NVARCHAR(20) NOT NULL DEFAULT 'Active',
    -- ^ Relationship status: 'Active', 'Suspended', 'Terminated'
    -- Active = Normal billing operations
    -- Suspended = Temporary pause (e.g., payment issues)
    -- Terminated = Relationship ended
    
    -- =====================================================================
    -- Audit Trail
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NOT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT FK_CompanyBillingRelationship_Payer FOREIGN KEY (PayerCompanyID) 
        REFERENCES [Company](CompanyID),
    
    CONSTRAINT FK_CompanyBillingRelationship_Payee FOREIGN KEY (PayeeCompanyID) 
        REFERENCES [Company](CompanyID),
    
    CONSTRAINT FK_CompanyBillingRelationship_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [User](UserID),
    
    CONSTRAINT FK_CompanyBillingRelationship_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [User](UserID),
    
    -- Validate RelationshipType values
    CONSTRAINT CK_CompanyBillingRelationship_Type CHECK (
        RelationshipType IN ('ParentChild', 'Partnership', 'Vendor', 'Affiliate')
    ),
    
    -- Validate Status values
    CONSTRAINT CK_CompanyBillingRelationship_Status CHECK (
        Status IN ('Active', 'Suspended', 'Terminated')
    ),
    
    -- Prevent company from billing itself
    CONSTRAINT CK_CompanyBillingRelationship_NoSelfBilling CHECK (PayerCompanyID != PayeeCompanyID),
    
    -- Ensure EndDate is after StartDate
    CONSTRAINT CK_CompanyBillingRelationship_DateOrder CHECK (
        EndDate IS NULL OR EndDate > StartDate
    )
);
GO

-- Index for active billing relationships
CREATE INDEX IX_CompanyBillingRelationship_Active ON [CompanyBillingRelationship](PayerCompanyID, Status)
    WHERE Status = 'Active' AND IsDeleted = 0;
GO

-- Index for payee relationships
CREATE INDEX IX_CompanyBillingRelationship_Payee ON [CompanyBillingRelationship](PayeeCompanyID, Status)
    WHERE Status = 'Active' AND IsDeleted = 0;
GO

PRINT 'CompanyBillingRelationship table created successfully!';
GO

-- =====================================================================
-- TABLE 3: ApprovalAuditTrail (Complete Audit Trail)
-- =====================================================================
-- Purpose: Tracks every action in approval workflows for compliance
-- Key Insight: Immutable audit log - never updated, only inserted
-- =====================================================================
CREATE TABLE [ApprovalAuditTrail] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    AuditID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Workflow Reference
    -- =====================================================================
    WorkflowID BIGINT NOT NULL,
    -- ^ Link to CompanyApprovalWorkflow record
    -- Used for: Tracking all actions on a specific approval request
    
    -- =====================================================================
    -- Action Details
    -- =====================================================================
    Action NVARCHAR(50) NOT NULL,
    -- ^ Action performed: 'Submitted', 'Approved', 'Rejected', 'Escalated', 'Commented'
    -- Submitted = Request was created
    -- Approved = Request was approved
    -- Rejected = Request was rejected
    -- Escalated = Request moved to higher authority
    -- Commented = Additional comments added
    
    ActionDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    -- ^ When action was performed (UTC)
    -- Used for: Timeline reconstruction, SLA tracking
    
    PerformedBy BIGINT NOT NULL,
    -- ^ User who performed the action (foreign key to User)
    -- Used for: Accountability, compliance reporting
    
    Comments NVARCHAR(MAX) NULL,
    -- ^ Additional comments or notes about this action
    -- Example: "Approved - within budget limits"
    -- Optional: Provides context for audit reviewers
    
    -- =====================================================================
    -- Status Tracking
    -- =====================================================================
    PreviousStatus NVARCHAR(20) NULL,
    -- ^ Status before this action (for state transitions)
    -- Example: 'Pending' → 'Approved'
    
    NewStatus NVARCHAR(20) NULL,
    -- ^ Status after this action (for state transitions)
    -- Example: 'Pending' → 'Approved'
    
    -- =====================================================================
    -- Audit Trail (Immutable - Never Updated)
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NOT NULL,
    -- Note: No UpdatedDate/UpdatedBy - audit trail is immutable
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT FK_ApprovalAuditTrail_Workflow FOREIGN KEY (WorkflowID) 
        REFERENCES [CompanyApprovalWorkflow](WorkflowID),
    
    CONSTRAINT FK_ApprovalAuditTrail_PerformedBy FOREIGN KEY (PerformedBy) 
        REFERENCES [User](UserID),
    
    CONSTRAINT FK_ApprovalAuditTrail_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [User](UserID),
    
    -- Validate Action values
    CONSTRAINT CK_ApprovalAuditTrail_Action CHECK (
        Action IN ('Submitted', 'Approved', 'Rejected', 'Escalated', 'Commented', 'Viewed')
    ),
    
    -- Validate Status values
    CONSTRAINT CK_ApprovalAuditTrail_Status CHECK (
        (PreviousStatus IS NULL OR PreviousStatus IN ('Pending', 'Approved', 'Rejected', 'Escalated')) AND
        (NewStatus IS NULL OR NewStatus IN ('Pending', 'Approved', 'Rejected', 'Escalated'))
    )
);
GO

-- Index for workflow audit history
CREATE INDEX IX_ApprovalAuditTrail_Workflow ON [ApprovalAuditTrail](WorkflowID, ActionDate);
GO

-- Index for user action history
CREATE INDEX IX_ApprovalAuditTrail_User ON [ApprovalAuditTrail](PerformedBy, ActionDate);
GO

PRINT 'ApprovalAuditTrail table created successfully!';
GO

-- =====================================================================
-- SUMMARY
-- =====================================================================
PRINT '========================================';
PRINT 'Company Domain Epic 2 Schema Complete!';
PRINT '========================================';
PRINT 'New Tables Created:';
PRINT '  1. CompanyApprovalWorkflow (approval requests - 15 fields)';
PRINT '  2. CompanyBillingRelationship (billing relationships - 12 fields)';
PRINT '  3. ApprovalAuditTrail (audit trail - 10 fields)';
PRINT '';
PRINT 'Key Features:';
PRINT '  ✅ Branch → Head Office approval workflows';
PRINT '  ✅ Company-to-company billing relationships';
PRINT '  ✅ Complete audit trail for compliance';
PRINT '  ✅ Backward compatible with Epic 1';
PRINT '  ✅ Industry-standard approval patterns';
PRINT '';
PRINT 'Next Steps:';
PRINT '  1. Sally UX review (approval interface design)';
PRINT '  2. Solomon schema validation (Database Migration Validator)';
PRINT '  3. Developer implementation planning';
PRINT '  4. Epic 2 testing strategy';
PRINT '========================================';
GO
