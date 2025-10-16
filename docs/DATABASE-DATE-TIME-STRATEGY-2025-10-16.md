# Database Date/Time Management Strategy

**Date:** October 16, 2025  
**Author:** Solomon 📜 (Database Migration Validator)  
**Purpose:** Comprehensive assessment of date/time storage and handling

---

## 🎯 **CURRENT APPROACH IN REBUILD PLAN**

```sql
-- All audit trail timestamps
CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
DeletedDate DATETIME2 NULL,

-- Event/business timestamps
EventStartDate DATETIME2 NOT NULL,
EventEndDate DATETIME2 NOT NULL,
```

**Current Standards:**
- ✅ `DATETIME2` (not DATETIME) - 0.1 microsecond precision, larger date range
- ✅ `GETUTCDATE()` for defaults - UTC timestamps
- ✅ All timestamps stored in UTC

---

## 🌍 **THE TIMEZONE PROBLEM**

### **Scenario: Event Platform**
```
Event: "Sydney Tech Conference"
Location: ICC Sydney, Australia (AEDT timezone)
Event Starts: 2025-12-15 09:00:00 AEDT (Sydney local time)
```

**❌ WRONG APPROACH (storing local time):**
```sql
EventStartDate = '2025-12-15 09:00:00'  -- What timezone is this?
-- Database has NO IDEA this is AEDT
-- If user is in London, they see "Event starts at 9:00 AM" (WRONG!)
```

**✅ CORRECT APPROACH (storing UTC + timezone):**
```sql
-- Database (UTC)
EventStartDate = '2025-12-14 22:00:00'  -- UTC time
EventTimezone = 'Australia/Sydney'      -- IANA timezone

-- Display logic (application layer)
-- User in Sydney sees: "Dec 15, 9:00 AM AEDT" ✅
-- User in London sees: "Dec 14, 10:00 PM GMT" ✅
-- User in New York sees: "Dec 14, 5:00 PM EST" ✅
```

---

## 📐 **INDUSTRY BEST PRACTICES**

### **1. ALWAYS Store UTC in Database**

**Why UTC?**
- ✅ No ambiguity (no DST confusion)
- ✅ Sortable chronologically
- ✅ Math works correctly (`EventEnd - EventStart = Duration`)
- ✅ No timezone conversion on database side

**Research from Industry Leaders:**

| **Company** | **Approach** | **Source** |
|------------|-------------|-----------|
| **Stripe** | All timestamps in UTC, store `timezone` separately | Engineering Blog |
| **Airbnb** | UTC in database, display in user's timezone | Tech Blog |
| **Eventbrite** | Event times in UTC + event timezone | API Docs |
| **Google Calendar** | UTC storage, IANA timezone for events | API Reference |
| **AWS** | All API timestamps in ISO 8601 UTC | Documentation |

---

## 🏗️ **RECOMMENDED DATABASE ARCHITECTURE**

### **Option A: Separate Timezone Columns (Recommended for EventLead)**

```sql
CREATE TABLE [dbo].[Event] (
    EventID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- Event timing (ALWAYS UTC)
    EventStartDateUTC DATETIME2 NOT NULL,
    EventEndDateUTC DATETIME2 NOT NULL,
    
    -- Timezone information
    EventTimezone NVARCHAR(50) NOT NULL,     -- IANA: 'Australia/Sydney', 'America/New_York'
    
    -- Display-friendly (computed or stored)
    EventStartDateLocal AS (
        -- SQL Server 2022+ has AT TIME ZONE
        EventStartDateUTC AT TIME ZONE 'UTC' AT TIME ZONE EventTimezone
    ) PERSISTED,
    
    -- Registration windows (also UTC)
    RegistrationOpensUTC DATETIME2 NOT NULL,
    RegistrationClosesUTC DATETIME2 NOT NULL,
    
    -- Audit trail (UTC)
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    ...
);
```

**Benefits:**
- ✅ Crystal clear: UTC vs Local time explicit in column names
- ✅ All sorting, filtering, comparisons work correctly
- ✅ Can calculate duration: `EventEndDateUTC - EventStartDateUTC`
- ✅ Frontend can convert UTC → User's timezone
- ✅ Event timezone stored for display ("Event starts 9:00 AM AEDT")

---

### **Option B: UTC Only + Application Timezone (Simpler)**

```sql
CREATE TABLE [dbo].[Event] (
    EventID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    -- All times in UTC (no suffix needed when UTC is standard)
    EventStartDate DATETIME2 NOT NULL,
    EventEndDate DATETIME2 NOT NULL,
    EventTimezone NVARCHAR(50) NOT NULL,     -- IANA timezone
    
    RegistrationOpens DATETIME2 NOT NULL,
    RegistrationCloses DATETIME2 NOT NULL,
    
    -- Audit trail (UTC)
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    ...
);
```

**Benefits:**
- ✅ Cleaner column names (UTC is implied)
- ✅ Industry standard (Stripe, Airbnb, Eventbrite all do this)
- ✅ All conversion logic in application layer (easier to test)

**When to Display Timezone:**
```typescript
// Frontend (React/TypeScript)
import { formatInTimeZone } from 'date-fns-tz';

// Event from API
const event = {
  eventStartDate: '2025-12-14T22:00:00Z',  // UTC from database
  eventTimezone: 'Australia/Sydney'
};

// Display to user
const displayTime = formatInTimeZone(
  event.eventStartDate, 
  event.eventTimezone, 
  'PPPp z'  // "December 15, 2025, 9:00 AM AEDT"
);
```

---

## 👤 **USER TIMEZONE vs EVENT TIMEZONE**

### **Critical Distinction:**

1. **User Timezone** (stored in User table)
   - User's personal timezone preference
   - Used for: Dashboard timestamps, email notifications, activity logs
   - Example: User in Sydney sees all timestamps in AEDT

2. **Event Timezone** (stored in Event table)
   - Event's physical location timezone
   - Used for: Event start/end times, registration deadlines
   - Example: Sydney event shows "9:00 AM AEDT" even to London user

```sql
-- User table
CREATE TABLE [dbo].[User] (
    UserID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    TimezoneIdentifier NVARCHAR(50) NOT NULL DEFAULT 'Australia/Sydney',
    -- ^ User's personal timezone for UI display
    -- Used for: "You created this form 2 hours ago" (in user's local time)
    
    LastLoginDate DATETIME2 NULL,          -- UTC
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),  -- UTC
    ...
);

-- Event table
CREATE TABLE [dbo].[Event] (
    EventID BIGINT IDENTITY(1,1) PRIMARY KEY,
    
    EventStartDate DATETIME2 NOT NULL,     -- UTC
    EventTimezone NVARCHAR(50) NOT NULL,   -- Event location timezone
    -- ^ Event's timezone for display
    -- Used for: "Event starts Dec 15, 9:00 AM AEDT" (always shows event local time)
    ...
);
```

---

## 📊 **IANA TIMEZONE DATABASE**

**Standard:** Use IANA timezone identifiers (not Windows timezone names)

**Examples:**
```
✅ CORRECT (IANA):
'Australia/Sydney'      → Handles AEDT/AEST automatically
'America/New_York'      → Handles EDT/EST automatically
'Europe/London'         → Handles BST/GMT automatically
'Asia/Tokyo'            → No DST (always JST)

❌ WRONG (Windows):
'AUS Eastern Standard Time'    → Not portable
'Eastern Standard Time'        → Ambiguous
'GMT Standard Time'            → Confusing
```

**Why IANA?**
- ✅ Cross-platform (JavaScript, Python, Java all use IANA)
- ✅ Handles DST automatically
- ✅ Historical accuracy (knows when DST rules changed)
- ✅ Future-proof (updated when countries change DST rules)

**SQL Server Support:**
```sql
-- SQL Server 2022+ supports IANA timezones
SELECT '2025-12-14T22:00:00' AT TIME ZONE 'UTC' 
       AT TIME ZONE 'Australia/Sydney';
-- Returns: '2025-12-15 09:00:00 +11:00' (AEDT)
```

---

## 🎯 **RECOMMENDED APPROACH FOR EVENTLEAD**

### **Hybrid Strategy (Best of Both Worlds)**

```sql
-- 1. ALL timestamps stored in UTC (database layer)
CREATE TABLE [dbo].[Event] (
    EventStartDate DATETIME2 NOT NULL,         -- UTC
    EventEndDate DATETIME2 NOT NULL,           -- UTC
    EventTimezone NVARCHAR(50) NOT NULL,       -- IANA: 'Australia/Sydney'
);

-- 2. User timezone for UI personalization
CREATE TABLE [dbo].[User] (
    TimezoneIdentifier NVARCHAR(50) NOT NULL DEFAULT 'Australia/Sydney',
);

-- 3. Application layer handles ALL timezone conversion
-- Backend API returns:
{
  "eventStartDate": "2025-12-14T22:00:00Z",    // UTC (ISO 8601)
  "eventTimezone": "Australia/Sydney",          // IANA
  "eventStartDateLocal": "2025-12-15T09:00:00+11:00"  // Pre-computed for convenience
}

-- 4. Frontend displays based on context:
// Event page: Show event timezone
"Event starts: December 15, 9:00 AM AEDT"

// User dashboard: Show user timezone
"You created this event 3 hours ago"
"Last login: Today at 2:30 PM" (in user's timezone)
```

---

## ⚠️ **COMMON PITFALLS TO AVOID**

### **1. Don't Store Local Time Without Timezone**
```sql
❌ BAD:
EventStartDate = '2025-12-15 09:00:00'  -- What timezone?!

✅ GOOD:
EventStartDate = '2025-12-14 22:00:00'  -- UTC
EventTimezone = 'Australia/Sydney'       -- Context
```

### **2. Don't Use DATETIME (Use DATETIME2)**
```sql
❌ BAD:
CreatedDate DATETIME  -- Limited precision, smaller range

✅ GOOD:
CreatedDate DATETIME2  -- 0.1μs precision, larger range (0001-9999)
```

### **3. Don't Use GETDATE() (Use GETUTCDATE())**
```sql
❌ BAD:
CreatedDate DATETIME2 DEFAULT GETDATE()  -- Server's local time (ambiguous!)

✅ GOOD:
CreatedDate DATETIME2 DEFAULT GETUTCDATE()  -- UTC (unambiguous)
```

### **4. Don't Convert Timezones in SQL (Do It in Application)**
```sql
❌ BAD:
SELECT EventStartDate AT TIME ZONE 'UTC' AT TIME ZONE @UserTimezone
-- SQL Server has limited timezone support, hard to test, slow

✅ GOOD:
-- Return UTC from database, convert in Python/JavaScript
SELECT EventStartDate, EventTimezone FROM Event
-- Let date-fns-tz, moment-timezone, or Python's zoneinfo handle conversion
```

### **5. Don't Forget Daylight Saving Time**
```sql
-- Event: "Sydney Summer Festival"
EventStartDate = '2025-01-15T09:00:00'  -- UTC
EventTimezone = 'Australia/Sydney'       -- AEDT (DST active, UTC+11)

-- Event: "Sydney Winter Festival"  
EventStartDate = '2025-07-15T09:00:00'  -- UTC
EventTimezone = 'Australia/Sydney'       -- AEST (DST inactive, UTC+10)

-- IANA timezone handles DST automatically! ✅
```

---

## 📦 **IMPLEMENTATION FOR EVENTLEAD**

### **1. Database Layer (SQL Server)**
```sql
-- Store UTC, store timezone
CREATE TABLE [dbo].[Event] (
    EventStartDate DATETIME2 NOT NULL,     -- UTC
    EventTimezone NVARCHAR(50) NOT NULL    -- IANA
);

CREATE TABLE [dbo].[User] (
    TimezoneIdentifier NVARCHAR(50) NOT NULL DEFAULT 'Australia/Sydney'
);
```

### **2. Backend Layer (Python FastAPI)**
```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

# Reading from database (always UTC)
event = db.query(Event).first()
event_start_utc = event.EventStartDate  # datetime in UTC

# Convert to event timezone for display
event_tz = ZoneInfo(event.EventTimezone)
event_start_local = event_start_utc.astimezone(event_tz)

# API response
return {
    "eventStartDate": event_start_utc.isoformat(),     # "2025-12-14T22:00:00Z"
    "eventTimezone": event.EventTimezone,               # "Australia/Sydney"
    "eventStartDateLocal": event_start_local.isoformat() # "2025-12-15T09:00:00+11:00"
}

# Writing to database (convert to UTC)
user_input = "2025-12-15 09:00 AM"  # User enters in event timezone
event_tz = ZoneInfo("Australia/Sydney")
local_dt = datetime.strptime(user_input, "%Y-%m-%d %I:%M %p").replace(tzinfo=event_tz)
utc_dt = local_dt.astimezone(timezone.utc)

# Save UTC to database
event.EventStartDate = utc_dt  # Stored as UTC
```

### **3. Frontend Layer (React TypeScript)**
```typescript
import { formatInTimeZone } from 'date-fns-tz';
import { formatDistanceToNow } from 'date-fns';

// Event page: Show event timezone
<div>
  Event starts: {formatInTimeZone(
    event.eventStartDate,
    event.eventTimezone,
    'PPPp z'  // "December 15, 2025, 9:00 AM AEDT"
  )}
</div>

// Dashboard: Show user timezone (relative time)
<div>
  Created {formatDistanceToNow(
    new Date(form.createdDate),
    { addSuffix: true }
  )}  // "3 hours ago" (in user's browser timezone)
</div>

// User settings: Show absolute time in user's timezone
<div>
  Last login: {new Date(user.lastLoginDate).toLocaleString(
    'en-AU',
    { timeZone: user.timezoneIdentifier }
  )}  // "16/10/2025, 2:30 PM" (AEDT)
</div>
```

---

## 🎯 **RECOMMENDATIONS FOR REBUILD PLAN**

### **1. Keep Current UTC Approach ✅**
```sql
-- Current approach is CORRECT
CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),  -- ✅ UTC
EventStartDate DATETIME2 NOT NULL,                     -- ✅ UTC
```

### **2. Add User Timezone (Dimitri's Design) ⭐**
```sql
-- Add to User table
TimezoneIdentifier NVARCHAR(50) NOT NULL DEFAULT 'Australia/Sydney',
```

### **3. Add Event Timezone (Future - Epic 2) ⭐**
```sql
-- Add to Event table (Epic 2)
EventTimezone NVARCHAR(50) NOT NULL,  -- IANA: 'Australia/Sydney'
```

### **4. Document Conventions 📋**
```sql
-- Naming convention (add to standards):
-- 1. All DATETIME2 fields store UTC (no conversion in database)
-- 2. Use GETUTCDATE() for defaults (never GETDATE())
-- 3. Store timezone separately (EventTimezone, User.TimezoneIdentifier)
-- 4. Application layer handles timezone conversion (not SQL)
-- 5. Use IANA timezone identifiers (not Windows timezones)
```

---

## 📊 **COMPARISON OF APPROACHES**

| **Approach** | **Pros** | **Cons** | **Recommendation** |
|-------------|----------|----------|-------------------|
| **UTC Only (No Timezone)** | ✅ Simple<br>✅ Fast queries | ❌ Can't display local time<br>❌ DST issues | ❌ Not suitable for event platform |
| **Local Time Only** | ✅ Matches user input | ❌ DST ambiguity<br>❌ Can't sort globally<br>❌ Math breaks | ❌ Never use |
| **UTC + Timezone String** | ✅ Best practice<br>✅ Handles DST<br>✅ Portable | ✅ Requires app logic | ⭐ **RECOMMENDED** |
| **DATETIMEOFFSET** | ✅ Built-in offset | ❌ Larger storage<br>❌ Offset != Timezone<br>❌ Can't handle DST | ⚠️ Not recommended |

---

## 🏆 **FINAL RECOMMENDATION**

**For EventLead Platform:**

```sql
-- 1. ALL database timestamps in UTC (current approach ✅)
CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE()

-- 2. Add User timezone for personalization
User.TimezoneIdentifier NVARCHAR(50) NOT NULL DEFAULT 'Australia/Sydney'

-- 3. Add Event timezone (Epic 2)
Event.EventTimezone NVARCHAR(50) NOT NULL

-- 4. Application handles conversion (Python zoneinfo, JavaScript date-fns-tz)
-- 5. API returns both UTC and pre-computed local time
{
  "eventStartDate": "2025-12-14T22:00:00Z",
  "eventTimezone": "Australia/Sydney",
  "eventStartDateLocal": "2025-12-15T09:00:00+11:00"
}
```

**Benefits:**
- ✅ Industry best practice (Stripe, Airbnb, Eventbrite all do this)
- ✅ Handles DST automatically (IANA timezone database)
- ✅ Works for international expansion
- ✅ Fast database queries (UTC sorting)
- ✅ Great UX (users see their local time)

---

**Solomon** 📜  
*"Store UTC, convert late. This is the way."*

---

## 📚 **REFERENCES**

1. [W3C Date and Time Formats](https://www.w3.org/TR/NOTE-datetime) - ISO 8601 standard
2. [IANA Timezone Database](https://www.iana.org/time-zones) - Authoritative timezone source
3. [Stripe API Design](https://stripe.com/docs/api) - All timestamps in UTC
4. [Eventbrite API](https://www.eventbrite.com/platform/api) - Event timezone handling
5. [PostgreSQL DateTime Best Practices](https://wiki.postgresql.org/wiki/Don%27t_Do_This#Date.2FTime_storage) - Store UTC
6. SQL Server `AT TIME ZONE` [Documentation](https://learn.microsoft.com/en-us/sql/t-sql/queries/at-time-zone-transact-sql)

