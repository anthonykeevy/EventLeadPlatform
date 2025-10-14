# Event Schema Updates - Version 1.1

**Date:** October 13, 2025  
**Author:** Dimitri (Data Domain Architect) + Anthony Keevy  
**Version:** 1.1.0 (Schema refinements based on client feedback)

---

## Summary of Changes

Based on Anthony's strategic feedback, we've made the following schema improvements:

### **1. ✅ Public vs Private Events - Confirmed Core Field**
- `IsPublic BIT NOT NULL DEFAULT 1`
- **Use Case:** Capricorn members-only event (IsPublic = 0)
- **Filtering:** Exclude private events from public event list

### **2. ✅ Industry Table - Shared Classification**
- **NEW TABLE:** `[Industry]` (shared between Company and Event)
- **Change:** `Event.Industry NVARCHAR(100)` → `Event.IndustryID INT`
- **Benefits:**
  - Consistent classification across Company and Event
  - Dropdown options (no free-text)
  - Industry-based event recommendations ("Your company is in Technology → here are Technology events")

### **3. ✅ EventType - Fixed Dropdown**
- Keep as `NVARCHAR(50)` with CHECK constraint (for MVP)
- **Phase 2:** Consider EventType lookup table for admin-managed additions
- **Who can add:** System Admin only (prevent pollution)

### **4. ✅ Tags - Flexible with Auto-Suggest**
- Keep as `NVARCHAR(MAX)` (comma-separated)
- Frontend: Auto-suggest popular tags
- **Who can add:** Customers (any tag they want)

### **5. ✅ Organizer Links to Company Table**
- **Change:** `OrganizerName NVARCHAR(200)` → `OrganizerCompanyID BIGINT`
- **Benefits:**
  - Track all events by organizer (e.g., "All events by Reed Exhibitions")
  - Link to organizer company profile (website, contact info)
  - Consistent company data (no duplicate "Reed Exhibitions" vs "Reed")

### **6. ✅ Dashboard Recommendation - Industry-Based Events**
- **Replace:** Event stats/KPIs (vanity metrics)
- **With:** "Recommended Events for Your Industry" widget
- **Query:** Show events where Company.IndustryID = Event.IndustryID
- **UX:** Actionable "Create Form" button on each recommended event

---

## Updated Schema Highlights

### **Foreign Keys (New/Updated)**

```sql
-- Core ownership
CompanyID BIGINT NOT NULL,  -- Company that created event (user-generated)
CONSTRAINT FK_Event_Company FOREIGN KEY (CompanyID) REFERENCES [Company](CompanyID),

-- Industry classification (SHARED with Company table)
IndustryID INT NULL,
CONSTRAINT FK_Event_Industry FOREIGN KEY (IndustryID) REFERENCES [Industry](IndustryID),

-- Organizer (links to Company table)
OrganizerCompanyID BIGINT NULL,
CONSTRAINT FK_Event_OrganizerCompany FOREIGN KEY (OrganizerCompanyID) REFERENCES [Company](CompanyID),
```

### **New Table: Industry**

```sql
CREATE TABLE [Industry] (
    IndustryID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(100) NOT NULL UNIQUE,  -- "Technology", "Healthcare", etc.
    Description NVARCHAR(500) NULL,
    DisplayOrder INT NOT NULL DEFAULT 999,
    IsActive BIT NOT NULL DEFAULT 1,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE()
);

-- Seed data: 21 industries (Technology, Healthcare, Manufacturing, ...)
-- See: database/schemas/industry-schema.sql
```

---

## Questions Addressed

### **Q1: Was there a flag for public vs private events?**

**A: YES!** ✅

```sql
IsPublic BIT NOT NULL DEFAULT 1,
-- ^ 1 = Public (discoverable in event list)
-- ^ 0 = Private (only visible to creator)
```

**Use Case:** Capricorn members-only event
```sql
INSERT INTO [Event] (Name, IsPublic, ...)
VALUES ('Capricorn Members Networking', 0, ...);
-- Won't appear in public event list
```

**Filtering:**
```sql
-- Public event list
WHERE IsPublic = 1 AND IsDeleted = 0

-- Company's own events (include private)
WHERE (CompanyID = @CompanyID OR IsPublic = 1) AND IsDeleted = 0
```

---

### **Q2: Classification deep dive - Dropdowns vs free-text?**

**A: Hybrid Approach** 🎯

| Field | Type | Who Can Add? | Implementation |
|-------|------|--------------|----------------|
| **EventType** | Fixed dropdown | System Admin only | `NVARCHAR(50)` with CHECK constraint |
| **Industry** | Shared table | System Admin only | `IndustryID INT` → `[Industry]` table |
| **Tags** | Free-text + auto-suggest | Customers | `NVARCHAR(MAX)` (comma-separated) |

**Why This Approach?**

- **EventType:** Fixed list prevents pollution ("Conference" vs "Conf" vs "Conference 2025")
- **Industry:** Shared with Company table → consistent classification
- **Tags:** Flexible (users know domain-specific terms: "GovTech", "PropTech", "FinTech")

**Dropdowns:**
```typescript
// Frontend: Industry dropdown
GET /api/industries?active=true
// Returns: [{ id: 1, name: "Technology" }, { id: 2, name: "Healthcare" }, ...]

// EventType dropdown (hardcoded in frontend)
const eventTypes = [
  "Trade Show", "Conference", "Expo", "Community Event",
  "Job Fair", "Product Launch", "Networking", "Workshop", "Private", "Other"
];

// Tags auto-suggest (popular tags)
GET /api/events/popular-tags?limit=20
// Returns: ["B2B", "Lead Capture", "Networking", "Tech", ...]
```

---

### **Q3: Common Industry table for Companies and Events?**

**A: YES! Great idea!** ✅

**Schema:**
```sql
-- Shared Industry table
CREATE TABLE [Industry] (
    IndustryID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(100) NOT NULL UNIQUE
);

-- Company uses Industry
ALTER TABLE [Company] ADD IndustryID INT NULL;
ALTER TABLE [Company] ADD CONSTRAINT FK_Company_Industry 
    FOREIGN KEY (IndustryID) REFERENCES [Industry](IndustryID);

-- Event uses same Industry
ALTER TABLE [Event] ADD IndustryID INT NULL;
ALTER TABLE [Event] ADD CONSTRAINT FK_Event_Industry 
    FOREIGN KEY (IndustryID) REFERENCES [Industry](IndustryID);
```

**Benefits:**

1. **Consistent Classification**
   - No duplicates: "Technology" vs "Tech" vs "IT"
   - Controlled vocabulary

2. **Industry-Based Recommendations**
   ```sql
   -- Show company events in their industry
   SELECT e.* FROM [Event] e
   INNER JOIN [Company] c ON c.IndustryID = e.IndustryID
   WHERE c.CompanyID = @CompanyID
     AND e.IsPublic = 1
     AND e.StartDateTime >= GETUTCDATE();
   ```

3. **Better Filtering**
   - Users filter by industry: "Show me all Healthcare events"
   - Analytics: "Which industries use our platform most?"

4. **Dropdown Reuse**
   - Same dropdown for Company registration AND Event creation
   - One place to manage industry list

**Implementation:**
- ✅ Created: `database/schemas/industry-schema.sql`
- ✅ Seeded: 21 industries (Technology, Healthcare, Manufacturing, ...)
- ✅ Updated Event schema to use `IndustryID`

---

### **Q4: Dashboard - Event stats vs Industry recommendations?**

**A: Industry recommendations are better!** 🎯

**REMOVE (Vanity Metrics):**
- Total events in database
- Most popular events
- Event counts by type

**ADD (Actionable Recommendations):**

**Widget: "Recommended Events for Your Industry"**

```sql
-- Query: Show events in company's industry
SELECT e.EventID, e.Name, e.StartDateTime, e.VenueName, e.City, 
       e.EventType, e.ExpectedAttendees
FROM [Event] e
INNER JOIN [Company] c ON c.IndustryID = e.IndustryID
WHERE c.CompanyID = @CompanyID
  AND e.IsPublic = 1
  AND e.Status = 'Published'
  AND e.StartDateTime >= GETUTCDATE()
  AND e.IsDeleted = 0
ORDER BY e.StartDateTime ASC
LIMIT 10;
```

**Dashboard Mockup:**
```
┌───────────────────────────────────────────────────────────────┐
│  🎯 Recommended Events for Your Industry (Technology)          │
│                                                                │
│  📅 May 15-17, 2025  │  CeBIT Australia 2025                  │
│  📍 ICC Sydney       │  Trade Show • 12,000 attendees         │
│                      │                      [Create Form] →   │
│                                                                │
│  📅 Jul 22-23, 2025  │  IoT Tech Expo Australia              │
│  📍 ICC Sydney       │  Conference • 5,000 attendees          │
│                      │                      [Create Form] →   │
│                                                                │
│  📅 Aug 13, 2025     │  Salesforce World Tour Sydney         │
│  📍 ICC Sydney       │  Hybrid • 5,000 attendees              │
│                      │                      [Create Form] →   │
└───────────────────────────────────────────────────────────────┘
```

**Benefits:**
- ✅ Actionable (users can create forms immediately)
- ✅ Personalized (based on their company's industry)
- ✅ Drives engagement (reminds them of upcoming events)
- ✅ Increases form creation rate

**Alternative Recommendations (Phase 2):**
- Events in their city (geolocation)
- Events similar to past events (collaborative filtering)
- Popular events (most forms created)

---

### **Q5: Marketing to online events?**

**A: Valid concern - De-prioritize for MVP** ⚠️

**Our Value Prop:** Booth lead capture at physical events

**Where Online Events Fit:**

| Event Type | Value Prop | Priority |
|------------|-----------|----------|
| **Physical Trade Shows** | iPad lead capture at booth | 🔥 **PRIMARY** (MVP focus) |
| **Hybrid Events** | Physical booth + virtual form | 🎯 **SECONDARY** (MVP supports, Phase 2 marketing) |
| **Virtual Exhibitor Halls** | Virtual booth visitors fill form | ⚠️ **TERTIARY** (Phase 3) |
| **Pure Webinars** | Post-webinar lead capture | ❌ **LOW VALUE** (weak fit) |

**Marketing Strategy:**
- ✅ **MVP Focus:** Physical events (trade shows, conferences, expos)
- ✅ **Schema Supports:** Hybrid events (EventFormat = 'Hybrid', OnlineEventUrl)
- ⏰ **Future:** Virtual exhibitor halls (specific online conferences like Salesforce Dreamforce Virtual)

**Why De-prioritize Pure Online Events?**
- Weak value prop (no booth context)
- Competitive disadvantage (Zoom has built-in polls/forms)
- Different buyer persona (webinar hosts vs booth exhibitors)

**Recommendation:** 🎯 Focus marketing on physical trade shows. Mention hybrid support as a feature, but don't lead with it.

---

### **Q6: 6 devices hosting same form - Different design approach?**

**A: No schema changes needed!** ✅

**This is an application architecture question, not a data model question.**

**Schema Already Supports This:**
```sql
-- Each iPad inserts submissions independently
INSERT INTO [Submission] (FormID, LeadData, SubmittedDate)
VALUES (@FormID, @LeadData, GETUTCDATE());
-- SQL Server handles concurrent writes natively (no conflicts)
```

**Application Requirements:**

#### **Option A: Online-Only (Simpler)**
- 6 iPads → all connected to internet
- POST submission to API immediately
- Backend handles concurrent writes (SQL Server ACID properties)

**Pros:**
- ✅ Simple (no sync logic)
- ✅ Real-time analytics

**Cons:**
- ❌ Requires internet (trade show WiFi notoriously bad)

#### **Option B: Offline-First (Recommended)** 🎯
- 6 iPads → store submissions locally (IndexedDB, SQLite)
- Periodic sync to backend (every 30 seconds or when online)
- Visual indicator: "Syncing... 3 submissions pending"

**Pros:**
- ✅ Works offline (critical for trade shows)
- ✅ Fast submission (no network latency)
- ✅ No data loss (queued locally)

**Cons:**
- ⚠️ More complex frontend code

**Frontend Stack:**
- React + IndexedDB (local storage)
- Background sync worker (Service Worker API)
- Conflict resolution: Last-write-wins (submissions are append-only, no conflicts)

**Backend Requirements:**
- Idempotent submission API (prevent duplicates if retry)
- `SubmissionID UUID` (generated on device, not IDENTITY)

**Recommendation:** 🎯 **Option B (Offline-First)** - Trade shows have terrible WiFi. Offline support is critical.

---

### **Q7: Duplicate detection complexity?**

**A: Moderate - Manageable with phased approach** ✅

**See detailed analysis:** `docs/data-domains/duplicate-detection-analysis.md`

**TLDR:**

| Approach | Dev Time | Accuracy | Recommendation |
|----------|----------|----------|----------------|
| **Exact String Matching** | 2 hours | ⭐ Low | ✅ MVP |
| **Fuzzy (Levenshtein)** | 2-3 days | ⭐⭐⭐ Medium | ✅ Phase 2 |
| **ML/Vector Embeddings** | 1-2 weeks | ⭐⭐⭐⭐⭐ High | ⏰ Phase 3 (if needed) |

**MVP Implementation (2 hours):**
```sql
-- Check exact duplicates (name + date + city)
SELECT EventID, Name FROM [Event]
WHERE Name = @NewEventName
  AND CAST(StartDateTime AS DATE) = CAST(@NewEventStartDateTime AS DATE)
  AND City = @NewEventCity
  AND IsDeleted = 0;
```

**Phase 2 (2-3 days):**
```sql
-- Pre-filter + fuzzy match (Levenshtein distance)
SELECT EventID, Name, dbo.LevenshteinDistance(@NewEventName, Name) AS Distance
FROM [Event]
WHERE City = @NewEventCity
  AND ABS(DATEDIFF(day, StartDateTime, @NewEventStartDateTime)) <= 3
HAVING Distance <= 5
ORDER BY Distance ASC;
```

**UX Flow:**
```
User adds: "CeBIT Australia 2025"
System finds: "CeBIT Australia 2025" (curated)

┌─────────────────────────────────────────────────────┐
│  ⚠️ Possible Duplicate Event Found                   │
│  We found an existing event:                        │
│                                                      │
│  ✅ CeBIT Australia 2025                             │
│     May 15-17, 2025 | ICC Sydney                    │
│     [Source: ICC Sydney Events]                     │
│                                                      │
│              [Use This Event]  [Add Anyway]         │
└─────────────────────────────────────────────────────┘
```

**Complexity:** ✅ **Low-to-Moderate** - Well-understood algorithms, manageable for MVP.

---

### **Q8: Organizers should link to Company table?**

**A: Absolutely! Updated schema** ✅

**Old Schema:**
```sql
OrganizerName NVARCHAR(200) NULL,  -- Free-text (inconsistent)
OrganizerWebsite NVARCHAR(500) NULL,
OrganizerContactEmail NVARCHAR(100) NULL,
```

**New Schema:**
```sql
OrganizerCompanyID BIGINT NULL,  -- Links to Company table
CONSTRAINT FK_Event_OrganizerCompany FOREIGN KEY (OrganizerCompanyID) 
    REFERENCES [Company](CompanyID),

OrganizerContactEmail NVARCHAR(100) NULL,  -- Event-specific contact
-- Note: General organizer info (name, website) comes from Company table
```

**Benefits:**

1. **Consistent Company Data**
   - No duplicates: "Reed Exhibitions" vs "Reed" vs "Reed Exhibitions Australia"
   - Single source of truth for organizer info

2. **Track All Events by Organizer**
   ```sql
   -- Show all events by Reed Exhibitions
   SELECT * FROM [Event]
   WHERE OrganizerCompanyID = @ReedExhibitionsCompanyID;
   ```

3. **Link to Organizer Profile**
   - Click organizer name → view company profile
   - See organizer's website, contact info, all events

4. **Organizer Dashboard (Future)**
   - Organizers can claim their events
   - Manage their event listings
   - See lead capture stats across their events

**Implementation:**
- ✅ Updated Event schema
- ✅ Added FK constraint
- 📋 TODO: Seed organizer companies (Reed Exhibitions, ICC Sydney, Hannover Fairs, etc.)

**Example:**
```sql
-- Create organizer company
INSERT INTO [Company] (Name, IsOrganizer, Website)
VALUES ('Reed Exhibitions', 1, 'https://www.reed.com.au');

-- Link event to organizer
INSERT INTO [Event] (..., OrganizerCompanyID, ...)
VALUES (..., @ReedExhibitionsCompanyID, ...);
```

---

## Updated Files

| File | Status | Changes |
|------|--------|---------|
| `database/schemas/event-schema.sql` | ✅ Updated | IndustryID (INT), OrganizerCompanyID (BIGINT) |
| `database/schemas/industry-schema.sql` | ✅ Created | New shared Industry table with 21 seed industries |
| `docs/data-domains/duplicate-detection-analysis.md` | ✅ Created | Complexity analysis (Exact → Fuzzy → ML) |
| `docs/data-domains/event-schema-updates-v1.1.md` | ✅ Created | This document (summary of changes) |

---

## Next Steps

### **Immediate (This Week):**

1. **Review Updated Schema**
   - ✅ Event.IndustryID (INT) instead of NVARCHAR
   - ✅ Event.OrganizerCompanyID (BIGINT) instead of OrganizerName
   - ✅ Event.IsPublic (BIT) - confirmed core field

2. **Create Industry Table Migration**
   - Run: `database/schemas/industry-schema.sql`
   - Verify 21 industries seeded

3. **Update Company Table**
   - Add: `Company.IndustryID INT NULL`
   - Add: `Company.IsOrganizer BIT NOT NULL DEFAULT 0`
   - Seed organizer companies (Reed Exhibitions, ICC Sydney, etc.)

### **Phase 2 (Post-MVP):**

4. **Industry-Based Event Recommendations**
   - Dashboard widget: "Recommended Events for Your Industry"
   - Query: Company.IndustryID = Event.IndustryID
   - UX: "Create Form" button on each recommended event

5. **Duplicate Detection (Fuzzy Matching)**
   - Implement Levenshtein distance function
   - Pre-filter by city + date (within ±3 days)
   - UX modal: "Did you mean this existing event?"

6. **Offline-First Form Submission**
   - IndexedDB for local storage
   - Background sync worker
   - Visual sync indicator

---

## Summary - Key Decisions

| Decision | Rationale | Status |
|----------|-----------|--------|
| **IsPublic flag is core** | Handles Capricorn members-only scenario | ✅ Confirmed |
| **Industry table (shared)** | Consistent classification, industry recommendations | ✅ Implemented |
| **EventType dropdown** | Fixed list (admin-managed) prevents pollution | ✅ Confirmed |
| **Tags free-text** | Flexible, auto-suggest popular tags | ✅ Confirmed |
| **Organizers → Company table** | Consistent data, track events by organizer | ✅ Implemented |
| **Dashboard: Industry recommendations** | Actionable (not vanity metrics) | ✅ Agreed |
| **De-prioritize online events** | Weak value prop for pure webinars | ✅ Agreed |
| **Offline-first forms** | Critical for trade show WiFi | ✅ Recommended |
| **Duplicate detection: Phased** | MVP = exact, Phase 2 = fuzzy | ✅ Agreed |

---

**Schema Version 1.1 Ready for Implementation! 🎉**

*Dimitri - Data Domain Architect* 🔍  
*With strategic input from Anthony Keevy*

