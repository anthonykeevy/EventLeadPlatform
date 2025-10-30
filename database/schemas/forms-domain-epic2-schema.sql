-- =====================================================================
-- Forms Domain Epic 2 Schema - Complete Form Management System
-- =====================================================================
-- Author: Dimitri (Data Domain Architect)
-- Date: January 15, 2025
-- Version: 1.0.0 (INITIAL RELEASE)
-- =====================================================================
-- Purpose:
--   Complete form management system for EventLead Platform:
--   1. Form creation and management
--   2. Form field types and validation
--   3. Form deployment with approval workflow integration
--   4. Form-level access control for external relationships
--   5. Form response capture and storage
--   6. Form analytics and performance metrics
--   7. Integration with Company and Event domains
-- =====================================================================
-- Integration Points:
--   - Company Domain: Form ownership, access control, approval workflow
--   - Event Domain: Form context, urgency calculation
--   - User Domain: Form creators, submitters, access control
-- =====================================================================

USE [EventLeadPlatform];
GO

-- =====================================================================
-- PHASE 1: CREATE REFERENCE TABLES
-- =====================================================================

-- =====================================================================
-- 1. CREATE FormFieldType REFERENCE TABLE
-- =====================================================================
-- Purpose: Define available form field types with validation patterns
-- =====================================================================
CREATE TABLE [ref].[FormFieldType] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    FormFieldTypeID INT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Field Type Definition
    -- =====================================================================
    TypeCode NVARCHAR(50) NOT NULL UNIQUE,
    -- ^ Unique code for field type: 'TEXT', 'NUMBER', 'DATE', 'EMAIL', etc.
    -- Used for: Programmatic identification of field types
    
    TypeName NVARCHAR(100) NOT NULL,
    -- ^ Human-readable name: 'Text Input', 'Number Input', 'Date Picker', etc.
    -- Used for: UI display and user selection
    
    TypeDescription NVARCHAR(500) NULL,
    -- ^ Detailed description of field type and usage
    -- Example: "Single-line text input for short responses"
    
    ValidationPattern NVARCHAR(200) NULL,
    -- ^ Regex pattern for client-side validation
    -- Example: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$" for email
    
    -- =====================================================================
    -- Configuration
    -- =====================================================================
    IsActive BIT NOT NULL DEFAULT 1,
    -- ^ Is this field type available for use?
    -- Used for: Enabling/disabling field types
    
    SortOrder INT NOT NULL DEFAULT 0,
    -- ^ Display order in field type selector
    -- Used for: UI organization and user experience
    
    -- =====================================================================
    -- Audit Trail
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NOT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT FK_FormFieldType_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_FormFieldType_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [dbo].[User](UserID)
);
GO

-- Insert standard field types
INSERT INTO [ref].[FormFieldType] (TypeCode, TypeName, TypeDescription, ValidationPattern, IsActive, SortOrder) VALUES
('TEXT', 'Text Input', 'Single-line text input for short responses', NULL, 1, 10),
('TEXTAREA', 'Text Area', 'Multi-line text input for longer responses', NULL, 1, 20),
('NUMBER', 'Number Input', 'Numeric input with optional decimal places', '^-?\d+(\.\d+)?$', 1, 30),
('EMAIL', 'Email Address', 'Email input with built-in validation', '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', 1, 40),
('PHONE', 'Phone Number', 'Phone number input with formatting', '^[\+]?[1-9][\d]{0,15}$', 1, 50),
('DATE', 'Date Picker', 'Date selection with calendar widget', '^\d{4}-\d{2}-\d{2}$', 1, 60),
('DATETIME', 'Date & Time', 'Date and time selection', '^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', 1, 70),
('SELECT', 'Dropdown Select', 'Single selection from predefined options', NULL, 1, 80),
('RADIO', 'Radio Buttons', 'Single selection from radio button options', NULL, 1, 90),
('CHECKBOX', 'Checkboxes', 'Multiple selection from checkbox options', NULL, 1, 100),
('RATING', 'Rating Scale', 'Numeric rating scale (1-5, 1-10, etc.)', '^[1-9]\d*$', 1, 110),
('FILE', 'File Upload', 'File upload with type and size restrictions', NULL, 1, 120),
('SIGNATURE', 'Digital Signature', 'Digital signature capture', NULL, 1, 130);
GO

PRINT 'FormFieldType reference table created successfully!';
GO

-- =====================================================================
-- PHASE 2: CREATE CORE FORM TABLES
-- =====================================================================

-- =====================================================================
-- 2. CREATE Form TABLE
-- =====================================================================
-- Purpose: Main form management and metadata
-- =====================================================================
CREATE TABLE [dbo].[Form] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    FormID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Form Identity
    -- =====================================================================
    FormName NVARCHAR(200) NOT NULL,
    -- ^ Form title/name
    -- Example: "Customer Feedback Survey"
    -- Required: Users need to identify forms
    
    FormDescription NVARCHAR(MAX) NULL,
    -- ^ Detailed description of form purpose
    -- Example: "Collect feedback from customers after event attendance"
    -- Optional: Provides context for form users
    
    -- =====================================================================
    -- Ownership and Context
    -- =====================================================================
    CompanyID BIGINT NOT NULL,
    -- ^ Owner company (foreign key to Company)
    -- Used for: Form ownership and access control
    
    EventID BIGINT NULL,
    -- ^ Associated event (foreign key to Event)
    -- Used for: Event-specific forms and context
    -- NULL = General form not tied to specific event
    
    -- =====================================================================
    -- Form Status and Configuration
    -- =====================================================================
    FormStatus NVARCHAR(20) NOT NULL DEFAULT 'Draft',
    -- ^ Form status: 'Draft', 'Published', 'Archived'
    -- Draft = Being created/edited
    -- Published = Live and accepting responses
    -- Archived = No longer accepting responses
    
    IsPublic BIT NOT NULL DEFAULT 0,
    -- ^ Can form be accessed without authentication?
    -- 0 = Requires authentication
    -- 1 = Public access (no login required)
    
    RequiresApproval BIT NOT NULL DEFAULT 0,
    -- ^ Does form deployment require approval?
    -- 0 = Auto-publish when ready
    -- 1 = Requires head office approval (Epic 2 integration)
    
    -- =====================================================================
    -- Deployment and Limits
    -- =====================================================================
    DeploymentCost DECIMAL(10,2) NULL,
    -- ^ Cost for form deployment (for approval workflow)
    -- Example: $500.00 for complex form deployment
    -- Used for: Company domain approval workflow
    
    MaxResponses INT NULL,
    -- ^ Maximum number of responses allowed
    -- NULL = No limit
    -- Used for: Response management and capacity planning
    
    ResponseDeadline DATETIME2 NULL,
    -- ^ When form stops accepting responses
    -- NULL = No deadline
    -- Used for: Time-limited forms and event forms
    
    -- =====================================================================
    -- Form Settings
    -- =====================================================================
    AllowMultipleSubmissions BIT NOT NULL DEFAULT 0,
    -- ^ Can same user submit multiple times?
    -- 0 = One submission per user
    -- 1 = Multiple submissions allowed
    
    RequireAuthentication BIT NOT NULL DEFAULT 0,
    -- ^ Must user be logged in to submit?
    -- 0 = Anonymous submissions allowed
    -- 1 = Must be authenticated user
    
    ShowProgressBar BIT NOT NULL DEFAULT 1,
    -- ^ Show progress bar during form completion?
    -- 0 = No progress indicator
    -- 1 = Show completion progress
    
    RandomizeQuestions BIT NOT NULL DEFAULT 0,
    -- ^ Randomize field order for each submission?
    -- 0 = Fixed field order
    -- 1 = Randomize field order
    
    -- =====================================================================
    -- Audit Trail
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NOT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    IsDeleted BIT NOT NULL DEFAULT 0,
    DeletedDate DATETIME2 NULL,
    DeletedBy BIGINT NULL,
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT FK_Form_Company FOREIGN KEY (CompanyID) 
        REFERENCES [dbo].[Company](CompanyID),
    CONSTRAINT FK_Form_Event FOREIGN KEY (EventID) 
        REFERENCES [dbo].[Event](EventID),
    CONSTRAINT FK_Form_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_Form_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_Form_DeletedBy FOREIGN KEY (DeletedBy) 
        REFERENCES [dbo].[User](UserID),
    
    -- Validate FormStatus values
    CONSTRAINT CK_Form_Status CHECK (
        FormStatus IN ('Draft', 'Published', 'Archived')
    ),
    
    -- Validate DeploymentCost is positive
    CONSTRAINT CK_Form_DeploymentCost CHECK (
        DeploymentCost IS NULL OR DeploymentCost >= 0
    ),
    
    -- Validate MaxResponses is positive
    CONSTRAINT CK_Form_MaxResponses CHECK (
        MaxResponses IS NULL OR MaxResponses > 0
    )
);
GO

-- Create indexes for Form table
CREATE INDEX IX_Form_Company ON [dbo].[Form](CompanyID, IsDeleted)
    WHERE IsDeleted = 0;
GO

CREATE INDEX IX_Form_Event ON [dbo].[Form](EventID, IsDeleted)
    WHERE IsDeleted = 0 AND EventID IS NOT NULL;
GO

CREATE INDEX IX_Form_Status ON [dbo].[Form](FormStatus, IsDeleted)
    WHERE IsDeleted = 0;
GO

CREATE INDEX IX_Form_Public ON [dbo].[Form](IsPublic, FormStatus, IsDeleted)
    WHERE IsDeleted = 0;
GO

PRINT 'Form table created successfully!';
GO

-- =====================================================================
-- 3. CREATE FormField TABLE
-- =====================================================================
-- Purpose: Form field configuration and validation
-- =====================================================================
CREATE TABLE [dbo].[FormField] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    FormFieldID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Form Reference
    -- =====================================================================
    FormID BIGINT NOT NULL,
    -- ^ Parent form (foreign key to Form)
    -- Used for: Linking fields to forms
    
    -- =====================================================================
    -- Field Identity
    -- =====================================================================
    FieldName NVARCHAR(200) NOT NULL,
    -- ^ Internal field name (programmatic identifier)
    -- Example: "customer_email", "event_rating"
    -- Used for: Data processing and API access
    
    FieldLabel NVARCHAR(200) NOT NULL,
    -- ^ Display label for field
    -- Example: "Email Address", "Rate Your Experience"
    -- Used for: UI display and user experience
    
    -- =====================================================================
    -- Field Configuration
    -- =====================================================================
    FieldType NVARCHAR(50) NOT NULL,
    -- ^ Field type (references FormFieldType.TypeCode)
    -- Example: 'TEXT', 'EMAIL', 'RATING'
    -- Used for: Field rendering and validation
    
    FieldOrder INT NOT NULL,
    -- ^ Display order within form
    -- Used for: Field sequencing and layout
    
    IsRequired BIT NOT NULL DEFAULT 0,
    -- ^ Is field required for form submission?
    -- 0 = Optional field
    -- 1 = Required field
    
    IsVisible BIT NOT NULL DEFAULT 1,
    -- ^ Is field visible to users?
    -- 0 = Hidden field
    -- 1 = Visible field
    -- Used for: Conditional logic and hidden fields
    
    -- =====================================================================
    -- Field Content
    -- =====================================================================
    HelpText NVARCHAR(500) NULL,
    -- ^ Help text displayed below field
    -- Example: "Enter your email address for confirmation"
    -- Used for: User guidance and field explanation
    
    PlaceholderText NVARCHAR(200) NULL,
    -- ^ Placeholder text shown in empty field
    -- Example: "Enter your name here"
    -- Used: User experience and field hints
    
    DefaultValue NVARCHAR(MAX) NULL,
    -- ^ Default value for field
    -- Example: "Yes" for checkbox, "5" for rating
    -- Used: Pre-populating fields
    
    -- =====================================================================
    -- Field Configuration (JSON)
    -- =====================================================================
    ValidationRules NVARCHAR(MAX) NULL,
    -- ^ JSON validation rules
    -- Example: {"minLength": 5, "maxLength": 100, "pattern": "^[A-Za-z ]+$"}
    -- Used: Client and server-side validation
    
    FieldOptions NVARCHAR(MAX) NULL,
    -- ^ JSON options for select/radio/checkbox fields
    -- Example: [{"value": "option1", "label": "Option 1"}, {"value": "option2", "label": "Option 2"}]
    -- Used: Dynamic option generation
    
    ConditionalLogic NVARCHAR(MAX) NULL,
    -- ^ JSON conditional display rules
    -- Example: {"showIf": {"field": "age", "operator": ">=", "value": 18}}
    -- Used: Dynamic form behavior
    
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
    CONSTRAINT FK_FormField_Form FOREIGN KEY (FormID) 
        REFERENCES [dbo].[Form](FormID),
    CONSTRAINT FK_FormField_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_FormField_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [dbo].[User](UserID),
    
    -- Validate FieldType values
    CONSTRAINT CK_FormField_Type CHECK (
        FieldType IN ('TEXT', 'TEXTAREA', 'NUMBER', 'EMAIL', 'PHONE', 'DATE', 'DATETIME', 
                     'SELECT', 'RADIO', 'CHECKBOX', 'RATING', 'FILE', 'SIGNATURE')
    ),
    
    -- Validate FieldOrder is positive
    CONSTRAINT CK_FormField_Order CHECK (FieldOrder > 0)
);
GO

-- Create indexes for FormField table
CREATE INDEX IX_FormField_Form ON [dbo].[FormField](FormID, FieldOrder, IsDeleted)
    WHERE IsDeleted = 0;
GO

CREATE INDEX IX_FormField_Type ON [dbo].[FormField](FieldType, IsDeleted)
    WHERE IsDeleted = 0;
GO

PRINT 'FormField table created successfully!';
GO

-- =====================================================================
-- 4. CREATE FormSubmission TABLE
-- =====================================================================
-- Purpose: Form response capture and submission tracking
-- =====================================================================
CREATE TABLE [dbo].[FormSubmission] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    FormSubmissionID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Form Reference
    -- =====================================================================
    FormID BIGINT NOT NULL,
    -- ^ Submitted form (foreign key to Form)
    -- Used: Linking submissions to forms
    
    -- =====================================================================
    -- Submitter Information
    -- =====================================================================
    SubmittedBy BIGINT NULL,
    -- ^ User who submitted (foreign key to User)
    -- NULL = Anonymous submission
    -- Used: Authentication and user tracking
    
    SubmitterEmail NVARCHAR(100) NULL,
    -- ^ Email address of submitter
    -- Used: Contact information and duplicate detection
    
    SubmitterName NVARCHAR(200) NULL,
    -- ^ Name of submitter
    -- Used: Personalization and identification
    
    -- =====================================================================
    -- Submission Details
    -- =====================================================================
    SubmissionDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    -- ^ When form was submitted (UTC)
    -- Used: Timeline tracking and analytics
    
    IPAddress NVARCHAR(45) NULL,
    -- ^ IP address of submitter (IPv4 or IPv6)
    -- Used: Security and duplicate detection
    
    UserAgent NVARCHAR(500) NULL,
    -- ^ Browser information
    -- Used: Analytics and debugging
    
    -- =====================================================================
    -- Submission Status
    -- =====================================================================
    SubmissionStatus NVARCHAR(20) NOT NULL DEFAULT 'Complete',
    -- ^ Submission status: 'Complete', 'Partial', 'Abandoned'
    -- Complete = All required fields filled and submitted
    -- Partial = Some fields filled but not submitted
    -- Abandoned = User started but didn't complete
    
    CompletionTime INT NULL,
    -- ^ Time to complete form in seconds
    -- Used: Analytics and user experience optimization
    
    -- =====================================================================
    -- Audit Trail
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NOT NULL,
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT FK_FormSubmission_Form FOREIGN KEY (FormID) 
        REFERENCES [dbo].[Form](FormID),
    CONSTRAINT FK_FormSubmission_SubmittedBy FOREIGN KEY (SubmittedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_FormSubmission_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [dbo].[User](UserID),
    
    -- Validate SubmissionStatus values
    CONSTRAINT CK_FormSubmission_Status CHECK (
        SubmissionStatus IN ('Complete', 'Partial', 'Abandoned')
    ),
    
    -- Validate CompletionTime is positive
    CONSTRAINT CK_FormSubmission_CompletionTime CHECK (
        CompletionTime IS NULL OR CompletionTime >= 0
    )
);
GO

-- Create indexes for FormSubmission table
CREATE INDEX IX_FormSubmission_Form ON [dbo].[FormSubmission](FormID, SubmissionDate);
GO

CREATE INDEX IX_FormSubmission_SubmittedBy ON [dbo].[FormSubmission](SubmittedBy, SubmissionDate)
    WHERE SubmittedBy IS NOT NULL;
GO

CREATE INDEX IX_FormSubmission_Email ON [dbo].[FormSubmission](SubmitterEmail, SubmissionDate)
    WHERE SubmitterEmail IS NOT NULL;
GO

CREATE INDEX IX_FormSubmission_Status ON [dbo].[FormSubmission](SubmissionStatus, SubmissionDate);
GO

PRINT 'FormSubmission table created successfully!';
GO

-- =====================================================================
-- 5. CREATE FormResponse TABLE
-- =====================================================================
-- Purpose: Individual field responses within submissions
-- =====================================================================
CREATE TABLE [dbo].[FormResponse] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    FormResponseID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Submission Reference
    -- =====================================================================
    FormSubmissionID BIGINT NOT NULL,
    -- ^ Parent submission (foreign key to FormSubmission)
    -- Used: Linking responses to submissions
    
    FormFieldID BIGINT NOT NULL,
    -- ^ Field being responded to (foreign key to FormField)
    -- Used: Linking responses to form fields
    
    -- =====================================================================
    -- Response Data
    -- =====================================================================
    ResponseValue NVARCHAR(MAX) NULL,
    -- ^ Raw response value as stored
    -- Example: "john@example.com", "5", "2024-01-15"
    -- Used: Data processing and analysis
    
    ResponseText NVARCHAR(MAX) NULL,
    -- ^ Formatted response for display
    -- Example: "John Smith (john@example.com)", "5 stars", "January 15, 2024"
    -- Used: UI display and reporting
    
    ResponseDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    -- ^ When response was captured
    -- Used: Timeline tracking and analytics
    
    -- =====================================================================
    -- Audit Trail
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NOT NULL,
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT FK_FormResponse_Submission FOREIGN KEY (FormSubmissionID) 
        REFERENCES [dbo].[FormSubmission](FormSubmissionID),
    CONSTRAINT FK_FormResponse_Field FOREIGN KEY (FormFieldID) 
        REFERENCES [dbo].[FormField](FormFieldID),
    CONSTRAINT FK_FormResponse_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [dbo].[User](UserID)
);
GO

-- Create indexes for FormResponse table
CREATE INDEX IX_FormResponse_Submission ON [dbo].[FormResponse](FormSubmissionID, FormFieldID);
GO

CREATE INDEX IX_FormResponse_Field ON [dbo].[FormResponse](FormFieldID, ResponseDate);
GO

-- Unique constraint to prevent duplicate responses
CREATE UNIQUE INDEX UX_FormResponse_SubmissionField ON [dbo].[FormResponse](FormSubmissionID, FormFieldID);
GO

PRINT 'FormResponse table created successfully!';
GO

-- =====================================================================
-- 6. CREATE FormAccessControl TABLE
-- =====================================================================
-- Purpose: Form-level access control for external relationships
-- =====================================================================
CREATE TABLE [dbo].[FormAccessControl] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    FormAccessControlID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Form and User References
    -- =====================================================================
    FormID BIGINT NOT NULL,
    -- ^ Form being accessed (foreign key to Form)
    -- Used: Linking access control to forms
    
    UserID BIGINT NOT NULL,
    -- ^ User with access (foreign key to User)
    -- Used: Identifying who has access
    
    CompanyID BIGINT NOT NULL,
    -- ^ Company granting access (foreign key to Company)
    -- Used: Tracking which company granted access
    
    -- =====================================================================
    -- Access Control Details
    -- =====================================================================
    AccessType NVARCHAR(20) NOT NULL,
    -- ^ Type of access: 'View', 'Edit', 'Manage', 'Submit'
    -- View = Can view form and responses
    -- Edit = Can edit form content
    -- Manage = Can manage form settings and access
    -- Submit = Can submit responses to form
    
    RelationshipTypeID INT NOT NULL,
    -- ^ Relationship type (foreign key to CompanyRelationshipType)
    -- Used: Tracking relationship type (Partner, Vendor, Client, Affiliate)
    
    -- =====================================================================
    -- Access Management
    -- =====================================================================
    GrantedBy BIGINT NOT NULL,
    -- ^ User who granted access (foreign key to User)
    -- Used: Audit trail and access management
    
    GrantedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    -- ^ When access was granted (UTC)
    -- Used: Access timeline tracking
    
    ExpiryDate DATETIME2 NULL,
    -- ^ When access expires (NULL = no expiry)
    -- Used: Temporary access grants
    
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
    CONSTRAINT FK_FormAccessControl_Form FOREIGN KEY (FormID) 
        REFERENCES [dbo].[Form](FormID),
    CONSTRAINT FK_FormAccessControl_User FOREIGN KEY (UserID) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_FormAccessControl_Company FOREIGN KEY (CompanyID) 
        REFERENCES [dbo].[Company](CompanyID),
    CONSTRAINT FK_FormAccessControl_RelationshipType FOREIGN KEY (RelationshipTypeID) 
        REFERENCES [ref].[CompanyRelationshipType](CompanyRelationshipTypeID),
    CONSTRAINT FK_FormAccessControl_GrantedBy FOREIGN KEY (GrantedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_FormAccessControl_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_FormAccessControl_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [dbo].[User](UserID),
    
    -- Validate AccessType values
    CONSTRAINT CK_FormAccessControl_AccessType CHECK (
        AccessType IN ('View', 'Edit', 'Manage', 'Submit')
    ),
    
    -- Ensure ExpiryDate is after GrantedDate
    CONSTRAINT CK_FormAccessControl_ExpiryDate CHECK (
        ExpiryDate IS NULL OR ExpiryDate > GrantedDate
    )
);
GO

-- Create indexes for FormAccessControl table
CREATE INDEX IX_FormAccessControl_Form ON [dbo].[FormAccessControl](FormID, IsDeleted)
    WHERE IsDeleted = 0;
GO

CREATE INDEX IX_FormAccessControl_User ON [dbo].[FormAccessControl](UserID, IsDeleted)
    WHERE IsDeleted = 0;
GO

CREATE INDEX IX_FormAccessControl_Company ON [dbo].[FormAccessControl](CompanyID, IsDeleted)
    WHERE IsDeleted = 0;
GO

-- Unique constraint to prevent duplicate access grants
CREATE UNIQUE INDEX UX_FormAccessControl_Unique ON [dbo].[FormAccessControl](FormID, UserID, CompanyID)
    WHERE IsDeleted = 0;
GO

PRINT 'FormAccessControl table created successfully!';
GO

-- =====================================================================
-- 7. CREATE FormAnalytics TABLE
-- =====================================================================
-- Purpose: Form performance metrics and analytics
-- =====================================================================
CREATE TABLE [dbo].[FormAnalytics] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    FormAnalyticsID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Form Reference
    -- =====================================================================
    FormID BIGINT NOT NULL,
    -- ^ Form being analyzed (foreign key to Form)
    -- Used: Linking analytics to forms
    
    -- =====================================================================
    -- Analytics Period
    -- =====================================================================
    MetricDate DATE NOT NULL,
    -- ^ Date for which metrics are calculated
    -- Used: Daily analytics aggregation
    
    -- =====================================================================
    -- Performance Metrics
    -- =====================================================================
    TotalViews INT NOT NULL DEFAULT 0,
    -- ^ Total number of form views on this date
    -- Used: Form visibility and reach metrics
    
    TotalSubmissions INT NOT NULL DEFAULT 0,
    -- ^ Total number of form submissions on this date
    -- Used: Form engagement and conversion metrics
    
    CompletionRate DECIMAL(5,2) NULL,
    -- ^ Percentage of views that resulted in submissions
    -- Calculated: (TotalSubmissions / TotalViews) * 100
    -- Used: Form effectiveness measurement
    
    AverageCompletionTime INT NULL,
    -- ^ Average time to complete form in seconds
    -- Used: User experience optimization
    
    BounceRate DECIMAL(5,2) NULL,
    -- ^ Percentage of users who viewed but didn't submit
    -- Calculated: ((TotalViews - TotalSubmissions) / TotalViews) * 100
    -- Used: Form abandonment analysis
    
    -- =====================================================================
    -- Audit Trail
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy BIGINT NOT NULL,
    UpdatedDate DATETIME2 NULL,
    UpdatedBy BIGINT NULL,
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT FK_FormAnalytics_Form FOREIGN KEY (FormID) 
        REFERENCES [dbo].[Form](FormID),
    CONSTRAINT FK_FormAnalytics_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_FormAnalytics_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [dbo].[User](UserID),
    
    -- Validate metrics are non-negative
    CONSTRAINT CK_FormAnalytics_Views CHECK (TotalViews >= 0),
    CONSTRAINT CK_FormAnalytics_Submissions CHECK (TotalSubmissions >= 0),
    CONSTRAINT CK_FormAnalytics_CompletionRate CHECK (
        CompletionRate IS NULL OR (CompletionRate >= 0 AND CompletionRate <= 100)
    ),
    CONSTRAINT CK_FormAnalytics_CompletionTime CHECK (
        AverageCompletionTime IS NULL OR AverageCompletionTime >= 0
    ),
    CONSTRAINT CK_FormAnalytics_BounceRate CHECK (
        BounceRate IS NULL OR (BounceRate >= 0 AND BounceRate <= 100)
    )
);
GO

-- Create indexes for FormAnalytics table
CREATE INDEX IX_FormAnalytics_Form ON [dbo].[FormAnalytics](FormID, MetricDate);
GO

CREATE INDEX IX_FormAnalytics_Date ON [dbo].[FormAnalytics](MetricDate, FormID);
GO

-- Unique constraint to prevent duplicate daily metrics
CREATE UNIQUE INDEX UX_FormAnalytics_FormDate ON [dbo].[FormAnalytics](FormID, MetricDate);
GO

PRINT 'FormAnalytics table created successfully!';
GO

-- =====================================================================
-- PHASE 3: CREATE HELPER FUNCTIONS
-- =====================================================================

-- =====================================================================
-- 8. CREATE Form Completion Rate Function
-- =====================================================================
-- Purpose: Calculate form completion rate
-- =====================================================================
CREATE FUNCTION [dbo].[CalculateFormCompletionRate](@FormID BIGINT, @StartDate DATE, @EndDate DATE)
RETURNS DECIMAL(5,2)
AS
BEGIN
    DECLARE @CompletionRate DECIMAL(5,2);
    DECLARE @TotalViews INT;
    DECLARE @TotalSubmissions INT;
    
    -- Get total views for date range
    SELECT @TotalViews = ISNULL(SUM(TotalViews), 0)
    FROM [dbo].[FormAnalytics]
    WHERE FormID = @FormID 
        AND MetricDate >= @StartDate 
        AND MetricDate <= @EndDate;
    
    -- Get total submissions for date range
    SELECT @TotalSubmissions = ISNULL(SUM(TotalSubmissions), 0)
    FROM [dbo].[FormAnalytics]
    WHERE FormID = @FormID 
        AND MetricDate >= @StartDate 
        AND MetricDate <= @EndDate;
    
    -- Calculate completion rate
    IF @TotalViews > 0
        SET @CompletionRate = (@TotalSubmissions * 100.0) / @TotalViews;
    ELSE
        SET @CompletionRate = 0;
    
    RETURN @CompletionRate;
END;
GO

PRINT 'Form completion rate function created successfully!';
GO

-- =====================================================================
-- 9. CREATE Form Response Count Function
-- =====================================================================
-- Purpose: Get total response count for a form
-- =====================================================================
CREATE FUNCTION [dbo].[GetFormResponseCount](@FormID BIGINT)
RETURNS INT
AS
BEGIN
    DECLARE @ResponseCount INT;
    
    SELECT @ResponseCount = COUNT(*)
    FROM [dbo].[FormSubmission]
    WHERE FormID = @FormID 
        AND SubmissionStatus = 'Complete';
    
    RETURN ISNULL(@ResponseCount, 0);
END;
GO

PRINT 'Form response count function created successfully!';
GO

-- =====================================================================
-- 10. CREATE Form Access Check Function
-- =====================================================================
-- Purpose: Check if user has access to form
-- =====================================================================
CREATE FUNCTION [dbo].[CheckFormAccess](@FormID BIGINT, @UserID BIGINT, @AccessType NVARCHAR(20))
RETURNS BIT
AS
BEGIN
    DECLARE @HasAccess BIT = 0;
    
    -- Check if user has the required access type
    IF EXISTS (
        SELECT 1
        FROM [dbo].[FormAccessControl]
        WHERE FormID = @FormID 
            AND UserID = @UserID 
            AND AccessType = @AccessType
            AND IsDeleted = 0
            AND (ExpiryDate IS NULL OR ExpiryDate > GETUTCDATE())
    )
        SET @HasAccess = 1;
    
    RETURN @HasAccess;
END;
GO

PRINT 'Form access check function created successfully!';
GO

-- =====================================================================
-- SUMMARY
-- =====================================================================
PRINT '========================================';
PRINT 'Forms Domain Epic 2 Schema Complete!';
PRINT '========================================';
PRINT 'COMPLETE FORM MANAGEMENT SYSTEM:';
PRINT '';
PRINT 'Reference Tables:';
PRINT '  1. FormFieldType (13 field types)';
PRINT '';
PRINT 'Core Tables:';
PRINT '  2. Form (main form management)';
PRINT '  3. FormField (field configuration)';
PRINT '  4. FormSubmission (response capture)';
PRINT '  5. FormResponse (individual responses)';
PRINT '  6. FormAccessControl (access control)';
PRINT '  7. FormAnalytics (performance metrics)';
PRINT '';
PRINT 'Helper Functions:';
PRINT '  8. CalculateFormCompletionRate (analytics)';
PRINT '  9. GetFormResponseCount (response counting)';
PRINT '  10. CheckFormAccess (access validation)';
PRINT '';
PRINT 'Key Features:';
PRINT '  ✅ Complete form lifecycle management';
PRINT '  ✅ 13 field types with validation';
PRINT '  ✅ Form deployment approval integration';
PRINT '  ✅ Form-level access control';
PRINT '  ✅ Response capture and storage';
PRINT '  ✅ Form analytics and metrics';
PRINT '  ✅ Company and Event domain integration';
PRINT '  ✅ Audit trail on all tables';
PRINT '';
PRINT 'Integration Points:';
PRINT '  ✅ Company Domain: Form ownership, access control, approval workflow';
PRINT '  ✅ Event Domain: Form context, urgency calculation';
PRINT '  ✅ User Domain: Form creators, submitters, access control';
PRINT '';
PRINT 'Next Steps:';
PRINT '  1. Solomon schema validation (Database Migration Validator)';
PRINT '  2. Sally UX review (form interface design)';
PRINT '  3. Developer implementation planning';
PRINT '  4. Form testing strategy';
PRINT '========================================';
GO
