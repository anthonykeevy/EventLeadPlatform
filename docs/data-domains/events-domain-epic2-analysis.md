# Events Domain Epic 2 Analysis - Complete Event Management System

**Author:** Dimitri 🔍 (Data Domain Architect)  
**Date:** January 15, 2025  
**Status:** Epic 2 Ready - Consolidated Analysis  
**Epic:** Epic 2 - Events Management & Multi-Tenant Support

---

## 🎯 **Epic 2 Requirements Summary**

### **Core Business Need**
- Event management for lead capture platform
- Multi-tenant event access (company-scoped events)
- Event selection and form creation workflow
- Integration with Company and User domains
- Support for both curated and user-generated events

### **Key Success Criteria**
- ✅ Event creation and management interface
- ✅ Multi-tenant event filtering (company-scoped)
- ✅ Event selection for form creation
- ✅ Integration with Company domain for ownership
- ✅ Integration with User domain for creators
- ✅ Foundation for future form builder integration

---

## 🔍 **Industry Research Findings**

### **Event Management Platform Patterns**

**1. Eventbrite Event Structure**
- **Event Identity**: Name, description, short description
- **Date/Time**: Start/end dates with timezone support
- **Location**: Venue name, address, coordinates
- **Classification**: Event type, industry, tags
- **Visibility**: Public vs private events
- **Organizer**: Company/organization information

**2. Bizzabo Enterprise Events**
- **Multi-tenant**: Company-scoped event access
- **Rich Metadata**: Industry classification, event types
- **Location Services**: Venue details with coordinates
- **Status Management**: Draft, published, completed, cancelled
- **Audit Trail**: Complete tracking of event changes

**3. Meetup.com Event Patterns**
- **Community Events**: User-generated content
- **Location-based**: City, venue, coordinates
- **Category System**: Technology, Business, Social
- **Recurring Events**: Support for series
- **Private Groups**: Member-only events

### **Key Industry Insights**
- **Hybrid Strategy**: 70% curated events, 30% user-generated
- **Location Services**: 90% of events have venue information
- **Industry Classification**: Essential for event recommendations
- **Timezone Support**: Critical for global platforms
- **Status Workflow**: Draft → Published → Completed → Archived

---

## 🏗️ **Epic 2 Events Domain Schema Design**

### **Core Event Table**

**1. Event (Main Event Table)**
```sql
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
    -- Note: FK naming follows convention - OrganizerCompanyID in Event table
    
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
```

### **Reference Tables**

**2. EventType (Event Type Reference)**
```sql
CREATE TABLE [ref].[EventType] (
    EventTypeID INT IDENTITY(1,1) PRIMARY KEY,
    TypeCode NVARCHAR(20) NOT NULL UNIQUE,
    TypeName NVARCHAR(50) NOT NULL,
    TypeDescription NVARCHAR(200) NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 0,
    -- Audit trail
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
```

**3. EventStatus (Event Status Reference)**
```sql
CREATE TABLE [ref].[EventStatus] (
    EventStatusID INT IDENTITY(1,1) PRIMARY KEY,
    StatusCode NVARCHAR(20) NOT NULL UNIQUE,
    StatusName NVARCHAR(50) NOT NULL,
    StatusDescription NVARCHAR(200) NULL,
    StatusColor NVARCHAR(7) NULL,                 -- Hex color for dashboard
    StatusIcon NVARCHAR(50) NULL,                 -- Icon name for dashboard
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 0,
    -- Audit trail
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
```

**4. RecurrencePattern (Recurrence Pattern Reference)**
```sql
CREATE TABLE [ref].[RecurrencePattern] (
    RecurrencePatternID INT IDENTITY(1,1) PRIMARY KEY,
    PatternCode NVARCHAR(20) NOT NULL UNIQUE,
    PatternName NVARCHAR(50) NOT NULL,
    PatternDescription NVARCHAR(200) NULL,
    PatternFormula NVARCHAR(100) NULL,            -- Formula for calculating next occurrence
    IsActive BIT NOT NULL DEFAULT 1,
    SortOrder INT NOT NULL DEFAULT 0,
    -- Audit trail
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
```

---

## 🔄 **Event Workflow Integration**

### **Event Creation Workflow**

**Step 1: Event Creation**
- User creates event in 'Draft' status
- System validates required fields (Name, StartDateTime, EventType)
- Event is company-scoped (CompanyID from user context)

**Step 2: Event Configuration**
- User adds location, description, classification
- System validates date logic and coordinates
- Event remains in 'Draft' until published

**Step 3: Event Publication**
- User publishes event (status changes to 'Published')
- Event becomes available for form creation
- Event appears in company event list

**Step 4: Event Management**
- Users can create forms for published events
- Event metrics updated as forms are created
- Event status updated based on dates

### **Multi-Tenant Event Access**

**Company-Scoped Events**:
- Users only see events from their company
- Event creation scoped to user's company
- Event sharing controlled by company relationships

**Event Filtering**:
- Dashboard shows company events only
- Search and filter within company scope
- Industry-based recommendations

---

## 📊 **Database Schema Summary**

### **New Tables (4)**
1. **Event** - Main event management table
2. **EventType** - Event type reference table
3. **EventStatus** - Event status reference table
4. **RecurrencePattern** - Recurrence pattern reference table

### **Integration Points**
- **Company Domain**: Event ownership and multi-tenant filtering
- **User Domain**: Event creators and permissions
- **Forms Header Domain**: Events for form creation

### **Key Relationships**
- Event.CompanyID → Company.CompanyID (event ownership)
- Event.CreatedBy → User.UserID (event creator)
- Event.EventTypeID → EventType.EventTypeID (event type classification)
- Event.EventStatusID → EventStatus.EventStatusID (event status management)
- Event.RecurrencePatternID → RecurrencePattern.RecurrencePatternID (recurrence patterns)
- Event.IndustryID → Industry.IndustryID (industry classification)
- Event.OrganizerCompanyID → Company.CompanyID (organizer company)
- Event.DuplicateEventID → Event.EventID (duplicate event linking)

---

## 🎯 **Strategic Benefits**

### **Business Value**
- **Event Management**: Complete event lifecycle management
- **Multi-Tenant Support**: Company-scoped event access
- **Form Integration**: Events as context for form creation
- **Industry Intelligence**: Industry-based event recommendations
- **Public Event Review**: Quality control for public events
- **Duplicate Prevention**: Avoid duplicate event creation
- **Recurring Events**: Support for event series
- **Delayed Visibility**: Control when events become public with specific date

### **Technical Benefits**
- **Normalized Design**: Efficient data storage and retrieval
- **Flexible Architecture**: Supports both curated and user-generated events
- **Audit Trail**: Complete tracking of event changes
- **Performance**: Optimized for event queries and filtering
- **Reference Tables**: Proper FK relationships for data integrity
- **Review Workflow**: Built-in approval process for public events
- **Duplicate Detection**: Automatic linking of duplicate events

---

## 📋 **Epic 2 Deliverables**

### **Analysis Document**
- **File**: `events-domain-epic2-analysis.md` (this document)
- **Content**: Complete event domain analysis and schema design
- **Status**: Ready for Epic 2 implementation

### **Schema File**
- **File**: `database/schemas/events-domain-epic2-schema.sql`
- **Content**: Complete SQL schema with 3 tables
- **Status**: Ready for Solomon validation

### **Integration Points**
- **Company Domain**: Event ownership and multi-tenant filtering
- **User Domain**: Event creators and permissions
- **Forms Header Domain**: Events for form creation

---

## 🚀 **Next Steps**

### **Immediate Actions**
1. **Solomon Validation**: Review schema with Database Migration Validator
2. **UX Expert Review**: Get Sally's input on event interface design
3. **Developer Handoff**: Create implementation specifications
4. **Testing Strategy**: Plan event management testing

### **Success Metrics**
- **Event Creation**: < 3 minutes to create basic event
- **Event Discovery**: < 2 seconds to load event list
- **Form Integration**: Seamless event selection for form creation
- **Multi-Tenant**: 100% accurate company-scoped filtering

---

*Dimitri - Data Domain Architect* 🔍  
*"Events domain consolidated and ready for Epic 2 - complete event management with multi-tenant support!"*
