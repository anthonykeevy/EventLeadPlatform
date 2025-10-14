-- =====================================================================
-- Event Table - Industry-Standard Event Management Schema
-- =====================================================================
-- Author: Dimitri (Data Domain Architect)
-- Date: October 13, 2025
-- Version: 1.0.0
-- =====================================================================
-- Purpose:
--   Supports lead capture platform with both formal events (trade shows,
--   conferences, expos) and informal scenarios (hair salon feedback, etc.)
-- 
-- Strategy:
--   Hybrid approach - curated database + user-generated additions
--
-- Standards:
--   - PascalCase naming (Solomon's requirement)
--   - NVARCHAR for text (UTF-8 support)
--   - DATETIME2 with UTC timestamps
--   - Soft deletes (IsDeleted flag)
--   - Full audit trail on all tables
-- =====================================================================
-- Industry Research:
--   - Eventbrite: Rich venue metadata, categorization
--   - Bizzabo/Swoogo: Exhibitor/booth focus, event hierarchy
--   - Meetup: Low-friction user-generated events
--   - Lead Capture Apps: Minimal event data, context for leads
-- =====================================================================

USE [EventLeadPlatform];
GO

-- =====================================================================
-- Event Table
-- =====================================================================
CREATE TABLE [Event] (
    -- =====================================================================
    -- Primary Key
    -- =====================================================================
    EventID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- =====================================================================
    -- Foreign Keys
    -- =====================================================================
    CompanyID BIGINT NOT NULL,
    -- ^ Company that owns this event entry (for user-generated events)
    -- For curated events, could reference a "system company" or be nullable
    
    -- =====================================================================
    -- Core Event Fields (Industry Standard - from Eventbrite/Bizzabo research)
    -- =====================================================================
    Name NVARCHAR(200) NOT NULL,
    -- ^ Event name (e.g., "CES 2025", "Hair Salon Feedback", "ICC Sydney Expo")
    
    Description NVARCHAR(MAX) NULL,
    -- ^ Long-form description (markdown-safe, supports multi-paragraph)
    
    ShortDescription NVARCHAR(500) NULL,
    -- ^ Brief summary for list views (optional)
    
    -- =====================================================================
    -- Date/Time Fields (UTC-based, supports multi-day events)
    -- =====================================================================
    StartDateTime DATETIME2 NOT NULL,
    -- ^ Event start (UTC) - MUST be UTC per Solomon's standards
    
    EndDateTime DATETIME2 NULL,
    -- ^ Event end (UTC) - nullable for ongoing/indefinite events (hair salon)
    
    TimezoneIdentifier NVARCHAR(50) NULL,
    -- ^ IANA timezone (e.g., "Australia/Sydney") for display purposes
    -- Backend stores UTC, frontend converts for user display
    
    -- =====================================================================
    -- Location Fields (Flexible: Physical, Online, or Hybrid)
    -- =====================================================================
    EventFormat NVARCHAR(20) NOT NULL DEFAULT 'Physical',
    -- ^ Options: 'Physical', 'Online', 'Hybrid'
    -- CHECK constraint enforced below
    
    VenueName NVARCHAR(200) NULL,
    -- ^ Venue name (e.g., "ICC Sydney", "My Hair Salon", "Online")
    
    VenueAddress NVARCHAR(500) NULL,
    -- ^ Full street address (optional for privacy/informal events)
    
    City NVARCHAR(100) NULL,
    -- ^ City name (used for filtering: "Sydney", "Melbourne")
    
    StateProvince NVARCHAR(100) NULL,
    -- ^ State/Province (e.g., "New South Wales", "Victoria")
    
    Country NVARCHAR(100) NULL DEFAULT 'Australia',
    -- ^ Country name (default Australia for MVP)
    
    PostalCode NVARCHAR(20) NULL,
    -- ^ Zip/Postal code (optional)
    
    Latitude DECIMAL(9,6) NULL,
    -- ^ Geocoded latitude (for map display, optional)
    
    Longitude DECIMAL(9,6) NULL,
    -- ^ Geocoded longitude (optional)
    
    OnlineEventUrl NVARCHAR(500) NULL,
    -- ^ URL for online/hybrid events (Zoom, Teams, etc.)
    
    -- =====================================================================
    -- Event Classification (Discovery & Filtering)
    -- =====================================================================
    EventType NVARCHAR(50) NOT NULL DEFAULT 'Other',
    -- ^ Options: 'Trade Show', 'Conference', 'Expo', 'Community Event', 
    --   'Job Fair', 'Product Launch', 'Networking', 'Workshop', 'Private', 'Other'
    -- Matches solution-architecture.md requirements
    
    IndustryID INT NULL,
    -- ^ Industry classification (links to shared Industry table)
    -- Useful for event discovery, filtering, and industry-based recommendations
    
    Tags NVARCHAR(MAX) NULL,
    -- ^ Comma-separated tags (e.g., "B2B, Lead Capture, Tech")
    -- Consider JSON column in future for structured tagging
    
    -- =====================================================================
    -- Event Source & Quality Flags (Hybrid Strategy)
    -- =====================================================================
    EventSource NVARCHAR(20) NOT NULL DEFAULT 'UserGenerated',
    -- ^ Options: 'Curated', 'UserGenerated', 'Verified'
    --   'Curated' = From venue websites/tourism boards (high quality)
    --   'UserGenerated' = User-submitted event (variable quality)
    --   'Verified' = User-generated but verified by admin/community
    
    SourceUrl NVARCHAR(500) NULL,
    -- ^ Source URL (for curated events: venue website, Eventbrite, etc.)
    
    SourceAttribution NVARCHAR(200) NULL,
    -- ^ Credit source (e.g., "ICC Sydney Events Calendar", "Tourism NSW")
    
    IsPublic BIT NOT NULL DEFAULT 1,
    -- ^ Public (discoverable in event list) vs Private (only visible to creator)
    --   Private = hair salon, internal company events, etc.
    
    -- =====================================================================
    -- Event Lifecycle Status
    -- =====================================================================
    Status NVARCHAR(20) NOT NULL DEFAULT 'Draft',
    -- ^ Options: 'Draft', 'Published', 'Live', 'Completed', 'Cancelled'
    --   Draft = Not visible to other users yet
    --   Published = Visible in event list, before start date
    --   Live = Event is currently happening
    --   Completed = Past event (historical)
    --   Cancelled = Event cancelled (retain data, don't show in active lists)
    
    -- =====================================================================
    -- Capacity & RSVP (Optional - future feature)
    -- =====================================================================
    ExpectedAttendees INT NULL,
    -- ^ Expected attendance (useful for trade shows: "5,000 attendees")
    --   Helps users prioritize which events to attend
    
    -- =====================================================================
    -- Organizer Information (Optional)
    -- =====================================================================
    OrganizerCompanyID BIGINT NULL,
    -- ^ Event organizer (links to Company table)
    -- Examples: Reed Exhibitions, ICC Sydney, Hannover Fairs Australia
    -- Benefits: Track all events by organizer, link organizer profile
    
    OrganizerContactEmail NVARCHAR(100) NULL,
    -- ^ Organizer contact email (optional, for event-specific questions)
    -- Note: General organizer info comes from Company table
    
    -- =====================================================================
    -- Media Assets (Optional - future feature)
    -- =====================================================================
    LogoUrl NVARCHAR(500) NULL,
    -- ^ Event logo URL (S3/Azure Blob storage)
    
    CoverImageUrl NVARCHAR(500) NULL,
    -- ^ Cover banner image URL
    
    -- =====================================================================
    -- Audit Trail (Standard for ALL tables - Solomon's requirement)
    -- =====================================================================
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    -- ^ Record creation timestamp (UTC)
    
    CreatedBy BIGINT NOT NULL,
    -- ^ UserID who created this record
    
    UpdatedDate DATETIME2 NULL,
    -- ^ Last update timestamp (UTC)
    
    UpdatedBy BIGINT NULL,
    -- ^ UserID who last updated this record
    
    IsDeleted BIT NOT NULL DEFAULT 0,
    -- ^ Soft delete flag (0 = active, 1 = deleted)
    
    DeletedDate DATETIME2 NULL,
    -- ^ Deletion timestamp (UTC)
    
    DeletedBy BIGINT NULL,
    -- ^ UserID who soft-deleted this record
    
    -- =====================================================================
    -- Constraints
    -- =====================================================================
    CONSTRAINT FK_Event_Company FOREIGN KEY (CompanyID) REFERENCES [Company](CompanyID),
    CONSTRAINT FK_Event_Industry FOREIGN KEY (IndustryID) REFERENCES [Industry](IndustryID),
    CONSTRAINT FK_Event_OrganizerCompany FOREIGN KEY (OrganizerCompanyID) REFERENCES [Company](CompanyID),
    CONSTRAINT FK_Event_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES [User](UserID),
    CONSTRAINT FK_Event_UpdatedBy FOREIGN KEY (UpdatedBy) REFERENCES [User](UserID),
    CONSTRAINT FK_Event_DeletedBy FOREIGN KEY (DeletedBy) REFERENCES [User](UserID),
    
    -- Date validation
    CONSTRAINT CK_Event_Dates CHECK (
        StartDateTime <= ISNULL(EndDateTime, '9999-12-31')
    ),
    
    -- Event format validation
    CONSTRAINT CK_Event_Format CHECK (
        EventFormat IN ('Physical', 'Online', 'Hybrid')
    ),
    
    -- Event source validation
    CONSTRAINT CK_Event_Source CHECK (
        EventSource IN ('Curated', 'UserGenerated', 'Verified')
    ),
    
    -- Status validation
    CONSTRAINT CK_Event_Status CHECK (
        Status IN ('Draft', 'Published', 'Live', 'Completed', 'Cancelled')
    ),
    
    -- Audit trail consistency
    CONSTRAINT CK_Event_AuditDates CHECK (
        CreatedDate <= ISNULL(UpdatedDate, '9999-12-31') AND
        CreatedDate <= ISNULL(DeletedDate, '9999-12-31')
    )
);
GO

-- =====================================================================
-- Indexes (Performance Optimization)
-- =====================================================================

-- Event discovery queries (public event list)
CREATE INDEX IX_Event_Discovery ON [Event](IsPublic, Status, StartDateTime, IsDeleted)
    WHERE IsDeleted = 0;
GO

-- Company's events (user dashboard)
CREATE INDEX IX_Event_Company ON [Event](CompanyID, IsDeleted)
    INCLUDE (Name, StartDateTime, Status)
    WHERE IsDeleted = 0;
GO

-- Date-based queries (upcoming events, past events)
CREATE INDEX IX_Event_Dates ON [Event](StartDateTime, EndDateTime, IsDeleted)
    WHERE IsDeleted = 0;
GO

-- Location-based queries (city/state filtering)
CREATE INDEX IX_Event_Location ON [Event](City, StateProvince, Country, IsDeleted)
    WHERE IsDeleted = 0;
GO

-- Event type filtering
CREATE INDEX IX_Event_Type ON [Event](EventType, IsDeleted)
    WHERE IsDeleted = 0;
GO

-- Curated vs user-generated filtering
CREATE INDEX IX_Event_Source ON [Event](EventSource, IsDeleted)
    WHERE IsDeleted = 0;
GO

-- Full-text search on Name and Description (future feature)
-- CREATE FULLTEXT INDEX ON [Event](Name, Description) KEY INDEX PK_Event;
-- GO

PRINT 'Event table created successfully!';
GO

