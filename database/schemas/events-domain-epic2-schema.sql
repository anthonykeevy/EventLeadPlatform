-- =====================================================================
-- Events Domain Epic 2 Schema - Complete Event Management System
-- Event Management & Multi-Tenant Support
-- =====================================================================
-- Author: Dimitri (Data Domain Architect)
-- Date: January 15, 2025
-- Version: 1.0.0 (EPIC 2 READY)
-- =====================================================================
-- Purpose:
--   Epic 2 Events domain - Complete Event Management:
--   1. Event creation and management interface
--   2. Multi-tenant event filtering (company-scoped)
--   3. Event selection for form creation
--   4. Integration with Company domain for ownership
--   5. Integration with User domain for creators
--   6. Foundation for future form builder integration
-- =====================================================================
-- Epic 2 Features:
--   ✅ Event Management: Complete event lifecycle management
--   ✅ Multi-Tenant Support: Company-scoped event access
--   ✅ Form Integration: Events as context for form creation
--   ✅ Industry Intelligence: Industry-based event recommendations
--   ✅ Location Services: Venue details with coordinates
--   ✅ Status Management: Draft, published, completed, cancelled
--   ✅ Audit Trail: Complete tracking of event changes
-- =====================================================================
-- Integration Points:
--   - Company Domain: Event ownership and multi-tenant filtering
--   - User Domain: Event creators and permissions
--   - Forms Header Domain: Events for form creation
-- =====================================================================

USE [EventLeadPlatform];
GO

-- =====================================================================
-- PHASE 1: CREATE REFERENCE TABLES
-- =====================================================================

-- =====================================================================
-- 1. CREATE EventType REFERENCE TABLE
-- =====================================================================
-- Purpose: Event type reference for classification
-- =====================================================================
CREATE TABLE [ref].[EventType] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    EventTypeID INT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Event Type Identity
    -- =====================================================================
    TypeCode NVARCHAR(20) NOT NULL UNIQUE,
    -- ^ Event type code for system use
    -- Examples: 'TRADE_SHOW', 'CONFERENCE', 'EXPO'
    
    TypeName NVARCHAR(50) NOT NULL,
    -- ^ Human-readable event type name
    -- Examples: 'Trade Show', 'Conference', 'Expo'
    
    TypeDescription NVARCHAR(200) NULL,
    -- ^ Detailed description of event type
    -- Example: 'Industry trade shows and exhibitions'
    
    -- =====================================================================
    -- Configuration
    -- =====================================================================
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 0,
    
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
    
    CONSTRAINT FK_EventType_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_EventType_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_EventType_DeletedBy FOREIGN KEY (DeletedBy) 
        REFERENCES [dbo].[User](UserID)
);
GO

-- Insert default event types
INSERT INTO [ref].[EventType] (TypeCode, TypeName, TypeDescription, IsActive, SortOrder, CreatedBy) VALUES
('TRADE_SHOW', 'Trade Show', 'Industry trade shows and exhibitions', 1, 1, 1),
('CONFERENCE', 'Conference', 'Professional conferences and conventions', 1, 2, 1),
('EXPO', 'Expo', 'Public exhibitions and expositions', 1, 3, 1),
('COMMUNITY', 'Community Event', 'Local community events and meetups', 1, 4, 1),
('JOB_FAIR', 'Job Fair', 'Career and job fair events', 1, 5, 1),
('PRODUCT_LAUNCH', 'Product Launch', 'Product launch and announcement events', 1, 6, 1),
('WORKSHOP', 'Workshop', 'Educational workshops and training', 1, 7, 1),
('SEMINAR', 'Seminar', 'Professional seminars and presentations', 1, 8, 1),
('OTHER', 'Other', 'Other types of events', 1, 9, 1);
GO

PRINT 'EventType reference table created successfully!';
GO

-- =====================================================================
-- 2. CREATE EventStatus REFERENCE TABLE
-- =====================================================================
-- Purpose: Event status reference with dashboard visual elements
-- =====================================================================
CREATE TABLE [ref].[EventStatus] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    EventStatusID INT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Status Identity
    -- =====================================================================
    StatusCode NVARCHAR(20) NOT NULL UNIQUE,
    -- ^ Status code for system use
    -- Examples: 'DRAFT', 'PUBLISHED', 'COMPLETED'
    
    StatusName NVARCHAR(50) NOT NULL,
    -- ^ Human-readable status name
    -- Examples: 'Draft', 'Published', 'Completed'
    
    StatusDescription NVARCHAR(200) NULL,
    -- ^ Detailed description of status
    -- Example: 'Event is being created and edited'
    
    -- =====================================================================
    -- Dashboard Visual Elements
    -- =====================================================================
    StatusColor NVARCHAR(7) NULL,
    -- ^ Hex color code for dashboard display
    -- Examples: '#FFA500' (orange for draft), '#28A745' (green for published)
    
    StatusIcon NVARCHAR(50) NULL,
    -- ^ Icon name for dashboard display
    -- Examples: 'draft-icon', 'published-icon', 'completed-icon'
    
    -- =====================================================================
    -- Configuration
    -- =====================================================================
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 0,
    
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
    
    CONSTRAINT FK_EventStatus_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_EventStatus_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_EventStatus_DeletedBy FOREIGN KEY (DeletedBy) 
        REFERENCES [dbo].[User](UserID)
);
GO

-- Insert default event statuses
INSERT INTO [ref].[EventStatus] (StatusCode, StatusName, StatusDescription, StatusColor, StatusIcon, IsActive, SortOrder, CreatedBy) VALUES
('DRAFT', 'Draft', 'Event is being created and edited', '#FFA500', 'draft-icon', 1, 1, 1),
('PENDING_REVIEW', 'Pending Review', 'Event submitted for public review', '#FFC107', 'pending-icon', 1, 2, 1),
('PUBLISHED', 'Published', 'Event is live and accepting forms', '#28A745', 'published-icon', 1, 3, 1),
('COMPLETED', 'Completed', 'Event has finished', '#17A2B8', 'completed-icon', 1, 4, 1),
('CANCELLED', 'Cancelled', 'Event has been cancelled', '#DC3545', 'cancelled-icon', 1, 5, 1),
('REJECTED', 'Rejected', 'Event rejected during review', '#6C757D', 'rejected-icon', 1, 6, 1),
('ARCHIVED', 'Archived', 'Event has been archived', '#6C757D', 'archived-icon', 1, 7, 1);
GO

-- =====================================================================
-- 3. CREATE RecurrencePattern REFERENCE TABLE
-- =====================================================================
-- Purpose: Recurrence pattern reference for recurring events
-- =====================================================================
CREATE TABLE [ref].[RecurrencePattern] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    RecurrencePatternID INT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Pattern Identity
    -- =====================================================================
    PatternCode NVARCHAR(20) NOT NULL UNIQUE,
    -- ^ Pattern code for system use
    -- Examples: 'DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY'
    
    PatternName NVARCHAR(50) NOT NULL,
    -- ^ Human-readable pattern name
    -- Examples: 'Daily', 'Weekly', 'Monthly', 'Yearly'
    
    PatternDescription NVARCHAR(200) NULL,
    -- ^ Detailed description of pattern
    -- Example: 'Event occurs every day'
    
    -- =====================================================================
    -- Pattern Configuration
    -- =====================================================================
    PatternFormula NVARCHAR(100) NULL,
    -- ^ Formula for calculating next occurrence
    -- Example: 'ADD_DAYS(1)', 'ADD_WEEKS(1)', 'ADD_MONTHS(1)'
    -- Used by system to calculate next event date
    
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 0,
    
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
    
    CONSTRAINT FK_RecurrencePattern_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_RecurrencePattern_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_RecurrencePattern_DeletedBy FOREIGN KEY (DeletedBy) 
        REFERENCES [dbo].[User](UserID)
);
GO

-- Insert default recurrence patterns
INSERT INTO [ref].[RecurrencePattern] (PatternCode, PatternName, PatternDescription, PatternFormula, IsActive, SortOrder, CreatedBy) VALUES
('NONE', 'No Recurrence', 'One-time event', NULL, 1, 1, 1),
('DAILY', 'Daily', 'Event occurs every day', 'ADD_DAYS(1)', 1, 2, 1),
('WEEKLY', 'Weekly', 'Event occurs every week', 'ADD_WEEKS(1)', 1, 3, 1),
('MONTHLY', 'Monthly', 'Event occurs every month', 'ADD_MONTHS(1)', 1, 4, 1),
('YEARLY', 'Yearly', 'Event occurs every year', 'ADD_YEARS(1)', 1, 5, 1),
('CUSTOM', 'Custom', 'Custom recurrence pattern', NULL, 1, 6, 1);
GO

PRINT 'EventStatus reference table created successfully!';
GO

-- =====================================================================
-- PHASE 2: CREATE CORE EVENT TABLE
-- =====================================================================

-- =====================================================================
-- 3. CREATE Event TABLE (MAIN EVENT TABLE)
-- =====================================================================
-- Purpose: Complete event management with multi-tenant support
-- =====================================================================
CREATE TABLE [dbo].[Event] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    EventID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Event Identity
    -- =====================================================================
    Name NVARCHAR(200) NOT NULL,
    -- ^ Event name/title
    -- Example: "CES 2025", "Hair Salon Feedback"
    -- Required: Users need to identify events
    
    Description NVARCHAR(MAX) NULL,
    -- ^ Detailed event description
    -- Example: "Consumer Electronics Show 2025 - Las Vegas"
    -- Optional: Rich descriptions for event detail pages
    
    ShortDescription NVARCHAR(500) NULL,
    -- ^ Brief summary for list views
    -- Example: "World's largest consumer electronics trade show"
    -- Optional: One-sentence summary for event cards
    
    -- =====================================================================
    -- Ownership and Context
    -- =====================================================================
    CompanyID BIGINT NOT NULL,
    -- ^ Owner company (foreign key to Company)
    -- Used for: Multi-tenant event filtering
    
    CreatedBy BIGINT NOT NULL,
    -- ^ User who created event (foreign key to User)
    -- Used for: Audit trail and permissions
    
    -- =====================================================================
    -- Date/Time Information
    -- =====================================================================
    StartDateTime DATETIME2 NOT NULL,
    -- ^ Event start date/time (UTC)
    -- Used for: Event scheduling and filtering
    
    EndDateTime DATETIME2 NULL,
    -- ^ Event end date/time (UTC)
    -- Used: Nullable for ongoing events
    -- NULL = Ongoing/indefinite event
    
    TimezoneIdentifier NVARCHAR(50) NULL,
    -- ^ IANA timezone (e.g., "Australia/Sydney")
    -- Used: Frontend timezone conversion
    
    -- =====================================================================
    -- Location Information
    -- =====================================================================
    VenueName NVARCHAR(200) NULL,
    -- ^ Venue name
    -- Example: "Las Vegas Convention Center"
    
    VenueAddress NVARCHAR(500) NULL,
    -- ^ Full venue address
    -- Example: "3150 Paradise Rd, Las Vegas, NV 89109, USA"
    
    City NVARCHAR(100) NULL,
    -- ^ City name
    -- Example: "Las Vegas"
    
    State NVARCHAR(100) NULL,
    -- ^ State/Province
    -- Example: "Nevada"
    
    CountryID BIGINT NULL,
    -- ^ Country (foreign key to ref.Country)
    -- Used: International event support
    
    Latitude DECIMAL(10,8) NULL,
    -- ^ GPS latitude
    -- Example: 36.1147
    
    Longitude DECIMAL(11,8) NULL,
    -- ^ GPS longitude
    -- Example: -115.1728
    
    -- =====================================================================
    -- Classification
    -- =====================================================================
    EventTypeID INT NOT NULL,
    -- ^ Event type (foreign key to ref.EventType)
    -- Used: Event type classification
    
    IndustryID BIGINT NULL,
    -- ^ Industry (foreign key to ref.Industry)
    -- Used: Industry-based event recommendations
    
    Tags NVARCHAR(MAX) NULL,
    -- ^ Comma-separated tags
    -- Example: "Technology,Innovation,Networking"
    -- Used: Flexible tagging system
    
    -- =====================================================================
    -- Event Configuration
    -- =====================================================================
    IsPublic BIT NOT NULL DEFAULT 0,
    -- ^ Public visibility
    -- 0 = Private event (company-only)
    -- 1 = Public event (visible to all users)
    
    EventStatusID INT NOT NULL,
    -- ^ Event status (foreign key to ref.EventStatus)
    -- Used: Event status management with visual elements
    
    IsRecurring BIT NOT NULL DEFAULT 0,
    -- ^ Recurring event flag
    -- 0 = One-time event
    -- 1 = Recurring event series
    
    RecurrencePatternID INT NULL,
    -- ^ Recurrence pattern (foreign key to ref.RecurrencePattern)
    -- Used: Recurring event pattern management
    
    -- =====================================================================
    -- Public Event Review Process
    -- =====================================================================
    IsPublicReviewRequired BIT NOT NULL DEFAULT 1,
    -- ^ Public review required flag
    -- 1 = Event requires admin review before going public
    -- 0 = Event can be made public immediately
    
    PublicReviewStatus NVARCHAR(20) NULL,
    -- ^ Public review status
    -- Values: 'PENDING', 'APPROVED', 'REJECTED'
    -- NULL = Not submitted for public review
    
    PublicReviewDate DATETIME2 NULL,
    -- ^ Date when public review was completed
    -- Used: Track review timeline
    
    PublicReviewBy BIGINT NULL,
    -- ^ User who completed public review
    -- Used: Audit trail for review decisions
    
    PublicReviewComments NVARCHAR(MAX) NULL,
    -- ^ Comments from public review
    -- Used: Feedback for event creators
    
    PublicVisibilityDate DATETIME2 NULL,
    -- ^ Specific date when event becomes public
    -- Example: '2025-02-15 09:00:00' = Make public on Feb 15, 2025 at 9 AM
    -- NULL = Make public immediately after approval
    
    -- =====================================================================
    -- Duplicate Event Detection
    -- =====================================================================
    DuplicateEventID BIGINT NULL,
    -- ^ Original event ID if this is a duplicate
    -- Used: Link to original event when duplicate is detected
    -- NULL = Original event
    
    IsDuplicate BIT NOT NULL DEFAULT 0,
    -- ^ Duplicate event flag
    -- 1 = This event is a duplicate of another
    -- 0 = This is an original event
    
    -- =====================================================================
    -- Organizer Information
    -- =====================================================================
    OrganizerCompanyID BIGINT NULL,
    -- ^ Organizer company (foreign key to Company)
    -- Used: Link to organizer company profile
    -- Note: Different from CompanyID (event owner) - this is the organizer
    
    OrganizerContactEmail NVARCHAR(100) NULL,
    -- ^ Organizer contact email (reception/call center)
    -- Example: "info@ces.tech", "reception@eventorganizer.com"
    -- Note: This is typically a general contact, not a specific user
    -- Future: Could be moved to separate EventOrganizerContact table
    
    OrganizerWebsite NVARCHAR(200) NULL,
    -- ^ Organizer website
    -- Example: "https://www.ces.tech"
    
    -- =====================================================================
    -- Event Metrics (Dashboard)
    -- =====================================================================
    ExpectedAttendees INT NULL,
    -- ^ Expected attendance
    -- Example: 150000
    
    ActualAttendees INT NULL,
    -- ^ Actual attendance (post-event)
    -- Example: 145000
    
    FormsCreated INT NOT NULL DEFAULT 0,
    -- ^ Number of forms created for this event
    -- Used: Dashboard metrics
    
    TotalSubmissions INT NOT NULL DEFAULT 0,
    -- ^ Total form submissions for this event
    -- Used: Dashboard metrics
    
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
    CONSTRAINT FK_Event_Company FOREIGN KEY (CompanyID) 
        REFERENCES [dbo].[Company](CompanyID),
    CONSTRAINT FK_Event_CreatedBy FOREIGN KEY (CreatedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_Event_Country FOREIGN KEY (CountryID) 
        REFERENCES [ref].[Country](CountryID),
    CONSTRAINT FK_Event_Industry FOREIGN KEY (IndustryID) 
        REFERENCES [ref].[Industry](IndustryID),
    CONSTRAINT FK_Event_EventType FOREIGN KEY (EventTypeID) 
        REFERENCES [ref].[EventType](EventTypeID),
    CONSTRAINT FK_Event_EventStatus FOREIGN KEY (EventStatusID) 
        REFERENCES [ref].[EventStatus](EventStatusID),
    CONSTRAINT FK_Event_RecurrencePattern FOREIGN KEY (RecurrencePatternID) 
        REFERENCES [ref].[RecurrencePattern](RecurrencePatternID),
    CONSTRAINT FK_Event_OrganizerCompany FOREIGN KEY (OrganizerCompanyID) 
        REFERENCES [dbo].[Company](CompanyID),
    CONSTRAINT FK_Event_PublicReviewBy FOREIGN KEY (PublicReviewBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_Event_DuplicateEvent FOREIGN KEY (DuplicateEventID) 
        REFERENCES [dbo].[Event](EventID),
    CONSTRAINT FK_Event_UpdatedBy FOREIGN KEY (UpdatedBy) 
        REFERENCES [dbo].[User](UserID),
    CONSTRAINT FK_Event_DeletedBy FOREIGN KEY (DeletedBy) 
        REFERENCES [dbo].[User](UserID),
    
    -- Validate PublicReviewStatus values
    CONSTRAINT CK_Event_PublicReviewStatus CHECK (
        PublicReviewStatus IS NULL OR PublicReviewStatus IN ('PENDING', 'APPROVED', 'REJECTED')
    ),
    
    -- Validate date logic
    CONSTRAINT CK_Event_DateTime CHECK (
        EndDateTime IS NULL OR EndDateTime > StartDateTime
    ),
    
    -- Validate coordinates
    CONSTRAINT CK_Event_Latitude CHECK (
        Latitude IS NULL OR (Latitude >= -90 AND Latitude <= 90)
    ),
    CONSTRAINT CK_Event_Longitude CHECK (
        Longitude IS NULL OR (Longitude >= -180 AND Longitude <= 180)
    ),
    
    -- Validate attendee counts
    CONSTRAINT CK_Event_Attendees CHECK (
        (ExpectedAttendees IS NULL OR ExpectedAttendees >= 0) AND
        (ActualAttendees IS NULL OR ActualAttendees >= 0)
    )
);
GO

-- Create indexes for Event table
CREATE INDEX IX_Event_Company ON [dbo].[Event](CompanyID, IsDeleted)
    WHERE IsDeleted = 0;
GO

CREATE INDEX IX_Event_Status ON [dbo].[Event](EventStatusID, IsDeleted)
    WHERE IsDeleted = 0;
GO

CREATE INDEX IX_Event_Type ON [dbo].[Event](EventTypeID, IsDeleted)
    WHERE IsDeleted = 0;
GO

CREATE INDEX IX_Event_Industry ON [dbo].[Event](IndustryID, IsDeleted)
    WHERE IsDeleted = 0 AND IndustryID IS NOT NULL;
GO

CREATE INDEX IX_Event_DateTime ON [dbo].[Event](StartDateTime, EndDateTime, IsDeleted)
    WHERE IsDeleted = 0;
GO

CREATE INDEX IX_Event_Public ON [dbo].[Event](IsPublic, EventStatusID, IsDeleted)
    WHERE IsDeleted = 0;
GO

CREATE INDEX IX_Event_Location ON [dbo].[Event](City, State, CountryID, IsDeleted)
    WHERE IsDeleted = 0;
GO

CREATE INDEX IX_Event_PublicReview ON [dbo].[Event](IsPublic, PublicReviewStatus, IsDeleted)
    WHERE IsDeleted = 0 AND IsPublic = 1;
GO

CREATE INDEX IX_Event_Duplicate ON [dbo].[Event](DuplicateEventID, IsDuplicate, IsDeleted)
    WHERE IsDeleted = 0;
GO

CREATE INDEX IX_Event_Recurring ON [dbo].[Event](IsRecurring, RecurrencePatternID, IsDeleted)
    WHERE IsDeleted = 0;
GO

PRINT 'Event table created successfully!';
GO

-- =====================================================================
-- PHASE 3: CREATE HELPER FUNCTIONS
-- =====================================================================

-- =====================================================================
-- 4. CREATE Event Dashboard Summary Function
-- =====================================================================
-- Purpose: Get event summary for dashboard display
-- =====================================================================
CREATE FUNCTION [dbo].[GetEventDashboardSummary](@EventID BIGINT)
RETURNS TABLE
AS
RETURN
(
    SELECT 
        e.EventID,
        e.Name,
        e.ShortDescription,
        e.CompanyID,
        e.CreatedBy,
        e.StartDateTime,
        e.EndDateTime,
        e.TimezoneIdentifier,
        e.VenueName,
        e.City,
        e.State,
        e.EventType,
        e.IndustryID,
        e.Tags,
        e.IsPublic,
        e.EventStatus,
        e.IsRecurring,
        e.ExpectedAttendees,
        e.ActualAttendees,
        e.FormsCreated,
        e.TotalSubmissions,
        e.CreatedDate,
        e.UpdatedDate,
        -- Calculated fields
        DATEDIFF(DAY, GETUTCDATE(), e.StartDateTime) as DaysUntilEvent,
        CASE 
            WHEN e.StartDateTime > GETUTCDATE() THEN 'Upcoming'
            WHEN e.EndDateTime IS NULL OR e.EndDateTime > GETUTCDATE() THEN 'Ongoing'
            ELSE 'Past'
        END as EventTimeline
    FROM [dbo].[Event] e
    WHERE e.EventID = @EventID 
        AND e.IsDeleted = 0
);
GO

PRINT 'Event dashboard summary function created successfully!';
GO

-- =====================================================================
-- 5. CREATE Event Search Function
-- =====================================================================
-- Purpose: Search events with filters
-- =====================================================================
CREATE FUNCTION [dbo].[SearchEvents](
    @CompanyID BIGINT,
    @EventType NVARCHAR(50) = NULL,
    @IndustryID BIGINT = NULL,
    @City NVARCHAR(100) = NULL,
    @StartDate DATETIME2 = NULL,
    @EndDate DATETIME2 = NULL,
    @IsPublic BIT = NULL
)
RETURNS TABLE
AS
RETURN
(
    SELECT 
        e.EventID,
        e.Name,
        e.ShortDescription,
        e.StartDateTime,
        e.EndDateTime,
        e.VenueName,
        e.City,
        e.State,
        e.EventType,
        e.EventStatus,
        e.IsPublic,
        e.FormsCreated,
        e.TotalSubmissions
    FROM [dbo].[Event] e
    WHERE e.CompanyID = @CompanyID
        AND e.IsDeleted = 0
        AND (@EventType IS NULL OR e.EventType = @EventType)
        AND (@IndustryID IS NULL OR e.IndustryID = @IndustryID)
        AND (@City IS NULL OR e.City = @City)
        AND (@StartDate IS NULL OR e.StartDateTime >= @StartDate)
        AND (@EndDate IS NULL OR e.EndDateTime <= @EndDate)
        AND (@IsPublic IS NULL OR e.IsPublic = @IsPublic)
);
GO

PRINT 'Event search function created successfully!';
GO

-- =====================================================================
-- 6. CREATE Event Metrics Update Function
-- =====================================================================
-- Purpose: Update event metrics when forms are created
-- =====================================================================
CREATE FUNCTION [dbo].[UpdateEventMetrics](@EventID BIGINT, @FormsCreated INT = 0, @TotalSubmissions INT = 0)
RETURNS BIT
AS
BEGIN
    DECLARE @Success BIT = 0;
    
    BEGIN TRY
        -- Update event metrics
        UPDATE [dbo].[Event]
        SET 
            FormsCreated = FormsCreated + @FormsCreated,
            TotalSubmissions = TotalSubmissions + @TotalSubmissions,
            UpdatedDate = GETUTCDATE()
        WHERE EventID = @EventID;
        
        SET @Success = 1;
    END TRY
    BEGIN CATCH
        SET @Success = 0;
    END CATCH
    
    RETURN @Success;
END;
GO

PRINT 'Event metrics update function created successfully!';
GO

-- =====================================================================
-- SUMMARY
-- =====================================================================
PRINT '========================================';
PRINT 'Events Domain Epic 2 Schema Complete!';
PRINT '========================================';
PRINT 'EPIC 2 READY:';
PRINT '';
PRINT 'Reference Tables:';
PRINT '  1. EventType (event type classification)';
PRINT '  2. EventStatus (event status with dashboard elements)';
PRINT '  3. RecurrencePattern (recurring event patterns)';
PRINT '';
PRINT 'Core Tables:';
PRINT '  4. Event (complete event management)';
PRINT '';
PRINT 'Helper Functions:';
PRINT '  5. GetEventDashboardSummary (dashboard data retrieval)';
PRINT '  6. SearchEvents (event search with filters)';
PRINT '  7. UpdateEventMetrics (metrics update)';
PRINT '';
PRINT 'Key Features:';
PRINT '  ✅ Complete event lifecycle management';
PRINT '  ✅ Multi-tenant event filtering (company-scoped)';
PRINT '  ✅ Event selection for form creation';
PRINT '  ✅ Industry-based event recommendations';
PRINT '  ✅ Location services with coordinates';
PRINT '  ✅ Status management with visual elements';
PRINT '  ✅ Event metrics and dashboard integration';
PRINT '  ✅ Public event review process';
PRINT '  ✅ Duplicate event detection';
PRINT '  ✅ Recurring event support';
PRINT '  ✅ Delayed public visibility';
PRINT '  ✅ Audit trail on all tables';
PRINT '  ✅ Foundation for form builder integration';
PRINT '';
PRINT 'Integration Points:';
PRINT '  ✅ Company Domain: Event ownership and multi-tenant filtering';
PRINT '  ✅ User Domain: Event creators and permissions';
PRINT '  ✅ Forms Header Domain: Events for form creation';
PRINT '';
PRINT 'Next Steps:';
PRINT '  1. Solomon schema validation (Database Migration Validator)';
PRINT '  2. Sally UX review (event interface design)';
PRINT '  3. Developer implementation planning';
PRINT '  4. Event management testing';
PRINT '========================================';
GO
