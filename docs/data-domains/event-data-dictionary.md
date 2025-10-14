# Event Domain - Data Dictionary

**Author:** Dimitri (Data Domain Architect) 🔍  
**Date:** October 13, 2025  
**Table:** `[Event]`

---

## Overview

The Event table stores information about events where users collect leads (trade shows, conferences) and informal scenarios (hair salon feedback). It supports a **hybrid strategy** - curated database + user-generated additions.

---

## Table: [Event]

### Primary Key

| Column | Type | Nullable | Description | Business Purpose |
|--------|------|----------|-------------|------------------|
| `EventID` | `BIGINT IDENTITY(1,1)` | NOT NULL | Unique identifier for each event record | System-generated ID for referencing events in forms, submissions, and dashboards |

---

### Foreign Keys

| Column | Type | Nullable | References | Description | Business Purpose |
|--------|------|----------|------------|-------------|------------------|
| `CompanyID` | `BIGINT` | NOT NULL | `[Company](CompanyID)` | Company that owns/created this event record | For user-generated events, tracks which company created the event. For curated events, could reference a "system company" |

---

### Core Event Fields

| Column | Type | Nullable | Default | Description | Business Purpose | Industry Source |
|--------|------|----------|---------|-------------|------------------|----------------|
| `Name` | `NVARCHAR(200)` | NOT NULL | - | Event name | User-facing event title (e.g., "CES 2025", "Hair Salon Feedback") | **Eventbrite, Meetup, Bizzabo** - all use similar field |
| `Description` | `NVARCHAR(MAX)` | NULL | - | Long-form event description | Supports multi-paragraph descriptions, markdown-safe. Used for event detail pages and search | **Eventbrite** - rich descriptions for discovery |
| `ShortDescription` | `NVARCHAR(500)` | NULL | - | Brief summary for list views | One-sentence summary for event cards, mobile views | **Eventbrite** - "summary" field for snippets |

---

### Date/Time Fields

| Column | Type | Nullable | Default | Description | Business Purpose | Industry Source |
|--------|------|----------|---------|-------------|------------------|----------------|
| `StartDateTime` | `DATETIME2` | NOT NULL | - | Event start date/time (UTC) | **MUST be UTC per Solomon's standards.** Used for filtering (upcoming events), sorting, and form activation windows | **All platforms** - core field |
| `EndDateTime` | `DATETIME2` | NULL | - | Event end date/time (UTC) | **Nullable to support ongoing/indefinite events** (e.g., hair salon feedback forms). Multi-day events store end date here | **Eventbrite, Meetup** - standard field |
| `TimezoneIdentifier` | `NVARCHAR(50)` | NULL | - | IANA timezone (e.g., "Australia/Sydney") | Backend stores UTC, frontend converts to local time for display. Needed because "9am in Sydney" is different from "9am in Perth" | **Eventbrite** - timezone handling |

---

### Location Fields (Flexible: Physical, Online, or Hybrid)

| Column | Type | Nullable | Default | Description | Business Purpose | Industry Source |
|--------|------|----------|---------|-------------|------------------|----------------|
| `EventFormat` | `NVARCHAR(20)` | NOT NULL | `'Physical'` | Format type: 'Physical', 'Online', 'Hybrid' | Determines which location fields are required. Post-COVID trend: 30% of events are hybrid | **Eventbrite, Bizzabo** - post-2020 standard |
| `VenueName` | `NVARCHAR(200)` | NULL | - | Venue name (e.g., "ICC Sydney", "Online") | User-facing venue display. Can be informal ("My Hair Salon") or formal ("ICC Sydney") | **Eventbrite** - "venue.name" |
| `VenueAddress` | `NVARCHAR(500)` | NULL | - | Full street address | **Optional for privacy/informal events.** Used for maps, directions, geocoding | **Eventbrite** - "venue.address" |
| `City` | `NVARCHAR(100)` | NULL | - | City name (e.g., "Sydney", "Melbourne") | **Primary location filter.** Users search "Events in Sydney" | **All platforms** - critical for discovery |
| `StateProvince` | `NVARCHAR(100)` | NULL | - | State/Province (e.g., "New South Wales") | Secondary location filter. Useful for regional events | **Eventbrite** - "venue.region" |
| `Country` | `NVARCHAR(100)` | NULL | `'Australia'` | Country name | Default "Australia" for MVP. International expansion ready | **Eventbrite** - "venue.country" |
| `PostalCode` | `NVARCHAR(20)` | NULL | - | Zip/Postal code | Optional. Used for precise geocoding | **Eventbrite** - "venue.postal_code" |
| `Latitude` | `DECIMAL(9,6)` | NULL | - | Geocoded latitude (-90 to 90) | **Optional.** Enables map display, distance calculations. Can be populated via Google Maps API | **Eventbrite** - "venue.latitude" |
| `Longitude` | `DECIMAL(9,6)` | NULL | - | Geocoded longitude (-180 to 180) | **Optional.** Enables map display | **Eventbrite** - "venue.longitude" |
| `OnlineEventUrl` | `NVARCHAR(500)` | NULL | - | URL for online/hybrid events (Zoom, Teams, etc.) | For online/hybrid events. Example: "https://zoom.us/j/1234567890" | **Meetup, Eventbrite** - post-COVID addition |

---

### Event Classification (Discovery & Filtering)

| Column | Type | Nullable | Default | Description | Business Purpose | Industry Source |
|--------|------|----------|---------|-------------|------------------|----------------|
| `EventType` | `NVARCHAR(50)` | NOT NULL | `'Other'` | Event category: 'Trade Show', 'Conference', 'Expo', 'Community Event', 'Job Fair', 'Product Launch', 'Networking', 'Workshop', 'Private', 'Other' | **Primary filter for event discovery.** Matches solution-architecture.md requirements | **Eventbrite** - "category", **Bizzabo** - event types |
| `Industry` | `NVARCHAR(100)` | NULL | - | Industry focus (e.g., "Technology", "Healthcare", "Retail") | **Useful for event discovery and lead quality.** Example: "Show me all Technology events" | **Bizzabo** - industry tagging for B2B events |
| `Tags` | `NVARCHAR(MAX)` | NULL | - | Comma-separated tags (e.g., "B2B, Lead Capture, Tech") | **Flexible categorization.** Consider JSON column in future for structured tagging | **Meetup** - interest-based tags |

---

### Event Source & Quality Flags (Hybrid Strategy)

| Column | Type | Nullable | Default | Description | Business Purpose | Industry Source |
|--------|------|----------|---------|-------------|------------------|----------------|
| `EventSource` | `NVARCHAR(20)` | NOT NULL | `'UserGenerated'` | Data quality flag: 'Curated', 'UserGenerated', 'Verified' | **Critical for hybrid strategy.** 'Curated' = from venue websites (high quality), 'UserGenerated' = user-submitted (variable quality), 'Verified' = user-generated but admin/community approved | **Dimitri's design** - unique hybrid approach |
| `SourceUrl` | `NVARCHAR(500)` | NULL | - | Source URL (for curated events) | Attribution for curated events. Example: "https://iccsydney.com/events/boat-show" | **Data governance** - transparency |
| `SourceAttribution` | `NVARCHAR(200)` | NULL | - | Credit source (e.g., "ICC Sydney Events Calendar") | **Production seed data governance.** Example: "Sourced from Tourism NSW" | **Data governance** - credit original sources |
| `IsPublic` | `BIT` | NOT NULL | `1` | Public (1) vs Private (0) visibility | **1 = Public** (discoverable in event list). **0 = Private** (only visible to creator). Critical for hair salon scenario | **Eventbrite** - private events feature |

---

### Event Lifecycle Status

| Column | Type | Nullable | Default | Description | Business Purpose | Industry Source |
|--------|------|----------|---------|-------------|------------------|----------------|
| `Status` | `NVARCHAR(20)` | NOT NULL | `'Draft'` | Lifecycle status: 'Draft', 'Published', 'Live', 'Completed', 'Cancelled' | **Draft** = Not visible to other users yet. **Published** = Visible in event list, before start date. **Live** = Event is currently happening. **Completed** = Past event (historical). **Cancelled** = Event cancelled (retain data, don't show in active lists) | **Eventbrite** - status field, **Bizzabo** - event states |

---

### Capacity & RSVP (Optional - Future Feature)

| Column | Type | Nullable | Default | Description | Business Purpose | Industry Source |
|--------|------|----------|---------|-------------|------------------|----------------|
| `ExpectedAttendees` | `INT` | NULL | - | Expected attendance (e.g., 5000) | **Useful for trade shows.** Helps users prioritize: "CES has 175,000 attendees" vs "Local meetup has 25". Future: Use for lead projections | **Bizzabo** - attendee counts, **Eventbrite** - ticket capacity |

---

### Organizer Information (Optional)

| Column | Type | Nullable | Default | Description | Business Purpose | Industry Source |
|--------|------|----------|---------|-------------|------------------|----------------|
| `OrganizerName` | `NVARCHAR(200)` | NULL | - | Event organizer (e.g., "Reed Exhibitions") | **Trust signal.** Example: "Organized by Reed Exhibitions" (reputable) | **Eventbrite** - "organizer.name" |
| `OrganizerWebsite` | `NVARCHAR(500)` | NULL | - | Organizer website URL | **Additional context.** Users can verify event legitimacy | **Eventbrite** - "organizer.url" |
| `OrganizerContactEmail` | `NVARCHAR(100)` | NULL | - | Organizer email (optional, for questions) | **Future feature:** Users can contact organizer for booth info | **Eventbrite** - contact information |

---

### Media Assets (Optional - Future Feature)

| Column | Type | Nullable | Default | Description | Business Purpose | Industry Source |
|--------|------|----------|---------|-------------|------------------|----------------|
| `LogoUrl` | `NVARCHAR(500)` | NULL | - | Event logo URL (S3/Azure Blob storage) | **Visual appeal.** Event cards look professional with logos. Example: CES logo, Vivid Sydney logo | **Eventbrite** - "logo.url" |
| `CoverImageUrl` | `NVARCHAR(500)` | NULL | - | Cover banner image URL | **Event detail page.** Large hero image for marketing | **Eventbrite** - cover images |

---

### Audit Trail (Standard for ALL Tables - Solomon's Requirement)

| Column | Type | Nullable | Default | Description | Business Purpose | Industry Source |
|--------|------|----------|---------|-------------|------------------|----------------|
| `CreatedDate` | `DATETIME2` | NOT NULL | `GETUTCDATE()` | Record creation timestamp (UTC) | **Audit trail.** Track when event was added to database | **Solomon's standard** - all tables |
| `CreatedBy` | `BIGINT` | NOT NULL | - | UserID who created this record | **Audit trail.** Track who added this event (user or system admin for curated events) | **Solomon's standard** |
| `UpdatedDate` | `DATETIME2` | NULL | - | Last update timestamp (UTC) | **Audit trail.** Track when event details were last modified | **Solomon's standard** |
| `UpdatedBy` | `BIGINT` | NULL | - | UserID who last updated this record | **Audit trail.** Track who modified event details | **Solomon's standard** |
| `IsDeleted` | `BIT` | NOT NULL | `0` | Soft delete flag (0 = active, 1 = deleted) | **Soft delete pattern.** Retain historical data, don't show in active queries. Critical for cancelled events (retain for reporting) | **Solomon's standard** |
| `DeletedDate` | `DATETIME2` | NULL | - | Deletion timestamp (UTC) | **Audit trail.** Track when event was soft-deleted | **Solomon's standard** |
| `DeletedBy` | `BIGINT` | NULL | - | UserID who soft-deleted this record | **Audit trail.** Track who deleted the event | **Solomon's standard** |

---

## Constraints

### Foreign Key Constraints

| Constraint | Description | Business Rule |
|------------|-------------|---------------|
| `FK_Event_Company` | Event belongs to a Company | Every event must be owned by a company (user-generated) or system company (curated) |
| `FK_Event_CreatedBy` | CreatedBy references User | Track who created the event record |
| `FK_Event_UpdatedBy` | UpdatedBy references User | Track who last modified the event |
| `FK_Event_DeletedBy` | DeletedBy references User | Track who soft-deleted the event |

### Check Constraints

| Constraint | Description | Business Rule |
|------------|-------------|---------------|
| `CK_Event_Dates` | `StartDateTime <= EndDateTime` | Event cannot end before it starts. NULL EndDateTime is allowed (ongoing events) |
| `CK_Event_Format` | `EventFormat IN ('Physical', 'Online', 'Hybrid')` | Enforce valid event format values |
| `CK_Event_Source` | `EventSource IN ('Curated', 'UserGenerated', 'Verified')` | Enforce valid event source values for hybrid strategy |
| `CK_Event_Status` | `Status IN ('Draft', 'Published', 'Live', 'Completed', 'Cancelled')` | Enforce valid lifecycle status values |
| `CK_Event_AuditDates` | `CreatedDate <= UpdatedDate <= DeletedDate` | Audit trail dates must be chronological |

---

## Indexes

### Performance-Critical Indexes

| Index | Columns | Purpose | Query Pattern |
|-------|---------|---------|---------------|
| `IX_Event_Discovery` | `IsPublic, Status, StartDateTime, IsDeleted` | **Public event list queries** | "Show me all upcoming public events" (event selection page) |
| `IX_Event_Company` | `CompanyID, IsDeleted` INCLUDE `(Name, StartDateTime, Status)` | **Company dashboard** | "Show me all events created by my company" |
| `IX_Event_Dates` | `StartDateTime, EndDateTime, IsDeleted` | **Date-based filtering** | "Show me events in November 2025" or "Show me past events" |
| `IX_Event_Location` | `City, StateProvince, Country, IsDeleted` | **Location filtering** | "Show me events in Sydney" or "Show me events in New South Wales" |
| `IX_Event_Type` | `EventType, IsDeleted` | **Event type filtering** | "Show me all Trade Shows" or "Show me all Conferences" |
| `IX_Event_Source` | `EventSource, IsDeleted` | **Source filtering** | "Show me curated events only" or "Show me user-generated events" |

---

## Sample Data Examples

### Example 1: Formal Event (Curated - Trade Show)

```sql
EventID = 1
CompanyID = 1 (System Company)
Name = 'Sydney International Boat Show 2025'
Description = 'Australia''s premier boat show featuring luxury yachts, fishing boats, marine equipment...'
ShortDescription = 'Premier boat show with 300+ exhibitors'
StartDateTime = '2025-08-01T00:00:00Z' -- UTC
EndDateTime = '2025-08-05T08:00:00Z' -- UTC
TimezoneIdentifier = 'Australia/Sydney'
EventFormat = 'Physical'
VenueName = 'ICC Sydney'
VenueAddress = '14 Darling Dr, Sydney NSW 2000'
City = 'Sydney'
StateProvince = 'New South Wales'
Country = 'Australia'
Latitude = -33.8688
Longitude = 151.2093
EventType = 'Expo'
Industry = 'Marine & Maritime'
Tags = 'Boats, Marine, B2B, Trade Show'
EventSource = 'Curated' -- HIGH QUALITY
SourceUrl = 'https://iccsydney.com/whats-on'
SourceAttribution = 'ICC Sydney Events Calendar'
IsPublic = 1 -- Discoverable
Status = 'Published'
ExpectedAttendees = 45000
OrganizerName = 'Australian Marine Industry Federation'
OrganizerWebsite = 'https://www.boatshow.com.au'
```

**Business Context:**  
This is a major Australian trade show where booth exhibitors would use our platform to collect leads. Curated from ICC Sydney's official calendar, this event has rich metadata, high quality, and is discoverable to all users.

---

### Example 2: Informal "Event" (User-Generated - Private)

```sql
EventID = 42
CompanyID = 5 (Hair Salon Company)
Name = 'Hair Salon Customer Feedback'
Description = 'Ongoing feedback collection for our hair salon customers after their appointments. Not a real event - just a feedback form.'
StartDateTime = '2025-01-01T00:00:00Z' -- Arbitrary start date
EndDateTime = NULL -- Ongoing/indefinite
TimezoneIdentifier = 'Australia/Sydney'
EventFormat = 'Physical'
VenueName = 'Bella Hair Studio'
City = 'Sydney'
StateProvince = 'New South Wales'
Country = 'Australia'
EventType = 'Private' -- Non-event scenario
EventSource = 'UserGenerated' -- User created
IsPublic = 0 -- Private (only visible to creator)
Status = 'Published'
-- All other fields: NULL (minimal metadata)
```

**Business Context:**  
This handles the "hair salon" edge case. It's not a real event - just a context for a feedback form. Private visibility means other users won't see it in the event list. Ongoing (NULL EndDateTime) means the form never expires.

---

### Example 3: Hybrid Event (Physical + Online)

```sql
EventID = 15
CompanyID = 1 (System Company)
Name = 'Australian Healthcare Innovation Summit 2025'
Description = 'Hybrid event combining in-person expo with virtual sessions...'
StartDateTime = '2025-10-05T08:30:00Z'
EndDateTime = '2025-10-06T17:00:00Z'
TimezoneIdentifier = 'Australia/Melbourne'
EventFormat = 'Hybrid' -- Physical + Online
VenueName = 'Melbourne Convention Centre'
VenueAddress = '1 Convention Centre Pl, South Wharf VIC 3006'
City = 'Melbourne'
StateProvince = 'Victoria'
Country = 'Australia'
OnlineEventUrl = 'https://teams.microsoft.com/meet/healthcare2025' -- Virtual component
EventType = 'Conference'
Industry = 'Healthcare'
EventSource = 'Curated'
IsPublic = 1
Status = 'Published'
ExpectedAttendees = 2500
```

**Business Context:**  
Post-COVID trend: Many events are hybrid (physical venue + virtual attendance). This example shows both physical location AND online URL populated.

---

### Example 4: Cancelled Event (Historical Data)

```sql
EventID = 99
Name = 'Tech Summit Australia 2025 (CANCELLED)'
Description = 'Major technology conference - CANCELLED due to venue issues. Retained for historical records.'
Status = 'Cancelled' -- Event cancelled
IsDeleted = 0 -- NOT soft-deleted (retain for reporting)
-- Other fields: Standard event metadata
```

**Business Context:**  
When events are cancelled, we retain the data (soft delete = 0) but mark Status = 'Cancelled'. This allows historical reporting ("How many forms did we create for that cancelled event?") without showing it in active event lists.

---

## Business Rules Summary

### 1. **Hybrid Strategy (Curated + User-Generated)**

- **Curated Events:** High-quality events from official sources (ICC Sydney, tourism boards)
  - `EventSource = 'Curated'`
  - `SourceUrl` and `SourceAttribution` populated
  - Full metadata (venue, geocoding, organizer)
  - Discoverable to all users (`IsPublic = 1`)

- **User-Generated Events:** Users add events not in curated database
  - `EventSource = 'UserGenerated'`
  - Minimal required fields (Name, Date, Location)
  - Can be private (`IsPublic = 0`) or public (`IsPublic = 1`)
  - Variable data quality

- **Verified Events:** User-generated events approved by admin/community
  - `EventSource = 'Verified'`
  - Upgraded after review process

### 2. **Formal vs Informal Scenarios**

- **Formal Events (Trade Shows, Conferences):**
  - Rich metadata (venue, industry, attendees, organizer)
  - Public visibility (`IsPublic = 1`)
  - Specific start/end dates
  - Example: Sydney International Boat Show

- **Informal "Events" (Hair Salon, Private Feedback):**
  - Minimal metadata (name, basic location)
  - Private visibility (`IsPublic = 0`)
  - Ongoing (NULL `EndDateTime`)
  - Example: Hair Salon Customer Feedback

### 3. **Event Lifecycle**

- **Draft:** User created but not yet published (not visible to other users)
- **Published:** Visible in event list, before start date
- **Live:** Event is currently happening (today's date within StartDateTime-EndDateTime)
- **Completed:** Past event (EndDateTime has passed)
- **Cancelled:** Event cancelled (retain data for reporting, don't show in active lists)

### 4. **Soft Deletes**

- `IsDeleted = 0`: Active event (show in queries)
- `IsDeleted = 1`: Soft-deleted event (exclude from queries, retain for audit trail)
- **Important:** Cancelled events use `Status = 'Cancelled'`, NOT `IsDeleted = 1`

### 5. **UTC Timestamps**

- **ALL date/time fields stored in UTC** (Solomon's standard)
- `TimezoneIdentifier` stores IANA timezone (e.g., "Australia/Sydney") for display
- Frontend converts UTC → local time for user display
- Example: Event starts at "2025-08-01T10:00:00+10:00" (Sydney) → stored as "2025-08-01T00:00:00Z" (UTC)

---

## Data Validation Rules

| Field | Validation Rule | Error Message |
|-------|----------------|---------------|
| `Name` | Required, 1-200 characters | "Event name is required and cannot exceed 200 characters" |
| `StartDateTime` | Required, cannot be in the past (for new events) | "Event start date must be in the future" |
| `EndDateTime` | Must be >= StartDateTime (if not NULL) | "Event end date cannot be before start date" |
| `EventFormat` | Must be 'Physical', 'Online', or 'Hybrid' | "Invalid event format" |
| `EventType` | Required, must be from predefined list | "Please select a valid event type" |
| `City` | Recommended (warn if NULL for public events) | "Adding a city helps users find your event" |
| `IsPublic` | Required (0 or 1) | "Please specify event visibility" |
| `Status` | Required, must be from predefined list | "Invalid event status" |

---

## Query Examples

### 1. **Event Discovery - Public Event List (Upcoming)**

```sql
SELECT EventID, Name, ShortDescription, StartDateTime, EndDateTime, 
       VenueName, City, EventType, EventSource, ExpectedAttendees
FROM [Event]
WHERE IsDeleted = 0
  AND IsPublic = 1
  AND Status = 'Published'
  AND StartDateTime >= GETUTCDATE()
ORDER BY StartDateTime ASC;
```

**Business Purpose:** Show users upcoming public events they can select when creating forms.

---

### 2. **Company Dashboard - "My Events"**

```sql
SELECT EventID, Name, StartDateTime, EndDateTime, Status, EventType
FROM [Event]
WHERE CompanyID = @CompanyID
  AND IsDeleted = 0
ORDER BY StartDateTime DESC;
```

**Business Purpose:** Show a company all events they've created (user-generated) or associated with.

---

### 3. **Filter by City - "Events in Sydney"**

```sql
SELECT EventID, Name, StartDateTime, VenueName, EventType
FROM [Event]
WHERE IsDeleted = 0
  AND IsPublic = 1
  AND City = 'Sydney'
  AND Status = 'Published'
  AND StartDateTime >= GETUTCDATE()
ORDER BY StartDateTime ASC;
```

**Business Purpose:** Location-based discovery (primary filter for users).

---

### 4. **Curated Events Only - "Verified Events"**

```sql
SELECT EventID, Name, StartDateTime, VenueName, EventSource, SourceAttribution
FROM [Event]
WHERE IsDeleted = 0
  AND IsPublic = 1
  AND EventSource = 'Curated'
  AND Status = 'Published'
ORDER BY StartDateTime ASC;
```

**Business Purpose:** Show high-quality curated events only (filter option for users who want verified data).

---

### 5. **Admin Review Queue - User-Generated Events**

```sql
SELECT EventID, Name, StartDateTime, City, EventType, CreatedDate, CreatedBy
FROM [Event]
WHERE EventSource = 'UserGenerated'
  AND Status = 'Draft'
  AND IsDeleted = 0
ORDER BY CreatedDate DESC;
```

**Business Purpose:** Admin dashboard showing user-added events pending review.

---

## Next Steps

1. **Validate with Solomon (Database Migration Validator)**
   - Confirm PascalCase naming
   - Confirm NVARCHAR usage (UTF-8 support)
   - Confirm UTC timestamps
   - Confirm soft delete pattern
   - Confirm audit trail completeness

2. **Create Alembic Migration**
   - Generate migration script from schema
   - Add indexes
   - Add constraints
   - Add comments

3. **Import Production Seed Data**
   - Run `database/seeds/production/event_production_seed.sql`
   - Verify 50 curated events loaded
   - Test event selection UI

4. **Share with UX Expert**
   - Event discovery page mockups
   - Event selection flow
   - Event card design (show: Name, Date, Venue, Badge)

5. **Share with Product Manager**
   - Review strategic recommendations (Hybrid approach)
   - Prioritize product enhancements
   - Plan roadmap (MVP → Phase 2 → Phase 3)

---

**Data Dictionary Complete! 📚**

*Dimitri - Data Domain Architect*

