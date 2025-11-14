# Event Data Flow: Database to Frontend

## Overview
This document traces the complete data flow from the SQL Server database table `dbo.Event` to the React frontend components.

## Data Flow Pipeline

### 1. Database Table (`dbo.Event`)
**Location:** SQL Server database table

**Key Fields:**
- `EventID` (BIGINT, Primary Key)
- `Name`, `Description`, `ShortDescription` (NVARCHAR)
- `CompanyID`, `CreatedBy` (BIGINT, Foreign Keys)
- `StartDateTime`, `EndDateTime` (DATETIME2)
- `VenueName`, `VenueAddress`, `City`, `State` (NVARCHAR)
- `Latitude`, `Longitude` (DECIMAL)
- `EventTypeID`, `IndustryID` (Foreign Keys)
- `Tags` (NVARCHAR(MAX))
- `IsPublic`, `IsRecurring` (BIT)
- `EventStatusID` (INT, Foreign Key)
- `OrganizerContactEmail`, `OrganizerWebsite` (NVARCHAR)
- `ExpectedAttendees`, `ActualAttendees` (INT)
- `FormsCreated`, `TotalSubmissions` (INT)
- Audit fields: `CreatedDate`, `UpdatedDate`, `UpdatedBy`, `IsDeleted`

**Related Tables (via Foreign Keys):**
- `ref.EventType` (via `EventTypeID`)
- `ref.EventStatus` (via `EventStatusID`)
- `ref.Industry` (via `IndustryID`)
- `dbo.Company` (via `CompanyID`)

---

### 2. SQLAlchemy Model (`backend/models/event.py`)
**Location:** `backend/models/event.py`

**Purpose:** Maps database columns to Python objects

**Key Mappings:**
```python
class Event(Base):
    EventID = Column(BigInteger, primary_key=True)
    Name = Column(String(200), nullable=False)
    Description = Column(String(None), nullable=True)
    # ... all other columns mapped with PascalCase names
```

**Relationships (lazy-loaded by default):**
```python
event_type = relationship("EventType", foreign_keys=[EventTypeID])
event_status = relationship("EventStatus", foreign_keys=[EventStatusID])
```

**⚠️ CRITICAL:** Relationships must be **eager loaded** using `joinedload()` or `selectinload()` to be included in API responses. Otherwise, they will be `None`.

---

### 3. Service Layer (`backend/modules/events/service.py`)
**Location:** `backend/modules/events/service.py`

**Function:** `get_events(db, company_id, filters) -> List[Event]`

**Eager Loading (REQUIRED):**
```python
from sqlalchemy.orm import joinedload

query = db.query(Event).options(
    joinedload(Event.event_type),      # ✅ Loads EventType relationship
    joinedload(Event.event_status)     # ✅ Loads EventStatus relationship
).filter(...)
```

**Returns:** List of `Event` SQLAlchemy model objects with relationships loaded.

---

### 4. Router/API Layer (`backend/modules/events/router.py`)
**Location:** `backend/modules/events/router.py`

**Function:** `_event_to_response(event: Event) -> EventResponse`

**Purpose:** Converts SQLAlchemy `Event` model to Pydantic `EventResponse` schema.

**Key Steps:**
1. Extracts relationship data (`event.event_type`, `event.event_status`)
2. Creates nested `EventTypeResponse` and `EventStatusResponse` objects
3. Constructs `EventResponse` with all fields

**Example:**
```python
event_type_response = None
if event.event_type:  # ✅ Must be eager loaded!
    event_type_response = EventTypeResponse(
        EventTypeID=event.event_type.EventTypeID,
        TypeCode=event.event_type.TypeCode,
        TypeName=event.event_type.TypeName,
        # ...
    )

return EventResponse(
    EventID=event.EventID,
    Name=event.Name,
    event_type=event_type_response,  # Nested object
    # ... all other fields
)
```

---

### 5. Pydantic Response Schema (`backend/modules/events/schemas.py`)
**Location:** `backend/modules/events/schemas.py`

**Schema:** `EventResponse(BaseModel)`

**Field Definitions:**
```python
class EventResponse(BaseModel):
    event_id: int = Field(..., alias="EventID")           # Field name: event_id, Alias: EventID
    name: str = Field(..., alias="Name")
    venue_name: Optional[str] = Field(None, alias="VenueName")
    event_type: Optional[EventTypeResponse] = None         # Nested object (no alias)
    event_status: Optional[EventStatusResponse] = None     # Nested object (no alias)
    
    class Config:
        populate_by_name = True  # ✅ Allows both field name AND alias when reading
        from_attributes = True   # ✅ Allows from_orm() conversion
```

**⚠️ CRITICAL SERIALIZATION ISSUE:**
- **`populate_by_name=True`** affects **DESERIALIZATION** (reading JSON → Python object)
- **Serialization** (Python object → JSON) **ALWAYS uses field names** (snake_case), NOT aliases
- FastAPI JSON responses will use **snake_case** field names, not PascalCase aliases

**Example JSON Output:**
```json
{
  "event_id": 1,           // ✅ Field name (snake_case)
  "name": "My Event",      // ✅ Field name (snake_case)
  "venue_name": "...",     // ✅ Field name (snake_case)
  "event_type": {          // ✅ Nested object uses snake_case
    "event_type_id": 1,
    "type_name": "Trade Show"
  }
}
```

**NOT:**
```json
{
  "EventID": 1,            // ❌ Alias is NOT used in serialization
  "Name": "My Event",      // ❌ Alias is NOT used in serialization
}
```

---

### 6. FastAPI JSON Response
**Location:** FastAPI automatically serializes Pydantic models to JSON

**Process:**
1. Pydantic model (`EventResponse`) is serialized using `.model_dump()` or `.dict()`
2. Serialization uses **field names** (snake_case), not aliases
3. Nested objects are recursively serialized

**JSON Response:**
```json
{
  "events": [
    {
      "event_id": 1,
      "name": "Sydney Gift Fair 2026",
      "description": "...",
      "venue_name": "Sydney Convention Centre",
      "city": "Sydney",
      "state": "NSW",
      "tags": "retail, trade show",
      "expected_attendees": 5000,
      "event_type": {
        "event_type_id": 1,
        "type_name": "Trade Show"
      },
      "event_status": {
        "event_status_id": 2,
        "status_name": "Published",
        "status_color": "#28A745"
      }
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 20
}
```

---

### 7. Frontend API Client (`frontend/src/features/events/api/eventsApi.ts`)
**Location:** `frontend/src/features/events/api/eventsApi.ts`

**Function:** `transformEvent(backendEvent: any): Event`

**Purpose:** Converts backend snake_case JSON to frontend camelCase TypeScript types.

**Key Transformation:**
```typescript
function transformEvent(backendEvent: any): Event {
  return {
    eventId: backendEvent.event_id ?? backendEvent.EventID ?? 0,      // snake_case → camelCase
    name: backendEvent.name ?? backendEvent.Name ?? '',               // Both formats supported
    venueName: backendEvent.venue_name ?? backendEvent.VenueName,    // snake_case → camelCase
    tags: backendEvent.tags ?? backendEvent.Tags,                     // snake_case → camelCase
    expectedAttendees: backendEvent.expected_attendees ?? backendEvent.ExpectedAttendees,
    eventType: backendEvent.event_type ? transformEventType(backendEvent.event_type) : null,
    eventStatus: backendEvent.event_status ? transformEventStatus(backendEvent.event_status) : null,
    // ... all other fields
  }
}
```

**⚠️ CRITICAL:** The `transformEvent` function handles BOTH formats:
- `backendEvent.event_id` (snake_case from Pydantic field name)
- `backendEvent.EventID` (PascalCase from alias, if somehow used)

**This is defensive coding** - the backend should always send snake_case, but the frontend handles both.

---

### 8. Frontend TypeScript Types (`frontend/src/features/events/types/events.types.ts`)
**Location:** `frontend/src/features/events/types/events.types.ts`

**Type Definition:**
```typescript
export interface Event {
  eventId: number           // camelCase
  name: string
  venueName: string | null
  city: string | null
  state: string | null
  tags: string | null
  expectedAttendees: number | null
  eventType: EventType | null      // Nested object
  eventStatus: EventStatus | null   // Nested object
  // ... all other fields in camelCase
}
```

---

### 9. Frontend Components
**Location:** `frontend/src/features/dashboard/components/CompanyContainer.tsx`

**Usage:**
```typescript
const event: Event = ... // From API

// Display fields
{event.eventType && (
  <div>{event.eventType.typeName}</div>  // ✅ Nested object access
)}

{event.tags && (
  <div>{event.tags}</div>               // ✅ Direct field access
)}

{event.expectedAttendees && (
  <div>Expected: {event.expectedAttendees}</div>  // ✅ Direct field access
)}
```

---

## Common Issues & Solutions

### Issue 1: Relationships are `null` in API response
**Symptom:** `event_type: null`, `event_status: null` in JSON response

**Root Cause:** Relationships not eager loaded in service layer

**Solution:**
```python
# In backend/modules/events/service.py
from sqlalchemy.orm import joinedload

query = db.query(Event).options(
    joinedload(Event.event_type),      # ✅ Add this
    joinedload(Event.event_status)     # ✅ Add this
).filter(...)
```

---

### Issue 2: Fields are missing in frontend
**Symptom:** `event.tags` is `null` even though database has value

**Root Cause:** 
1. Field not included in `_event_to_response()` conversion
2. Field not mapped in `transformEvent()` function

**Solution:**
1. Check `_event_to_response()` includes the field:
   ```python
   return EventResponse(
       Tags=event.Tags,  # ✅ Must be included
       # ...
   )
   ```

2. Check `transformEvent()` maps the field:
   ```typescript
   tags: backendEvent.tags ?? backendEvent.Tags ?? null,  // ✅ Must be mapped
   ```

---

### Issue 3: Backend sends PascalCase but frontend expects snake_case
**Symptom:** `EventID` in JSON but frontend looks for `event_id`

**Root Cause:** Misunderstanding of Pydantic serialization

**Solution:**
- Pydantic **ALWAYS serializes** using field names (snake_case), NOT aliases
- Frontend should expect snake_case
- Frontend `transformEvent()` handles both formats defensively

---

## Verification Checklist

✅ **Database:** All fields exist in `dbo.Event` table
✅ **SQLAlchemy Model:** All columns mapped in `Event` model
✅ **Relationships:** Eager loaded in `get_events()` and `get_event_by_id()`
✅ **Router:** `_event_to_response()` includes all fields
✅ **Pydantic Schema:** All fields defined in `EventResponse`
✅ **Frontend Transform:** `transformEvent()` maps all fields
✅ **Frontend Types:** TypeScript `Event` interface includes all fields
✅ **Frontend Components:** Display all required fields

---

## Debugging Steps

1. **Check Database:**
   ```sql
   SELECT EventID, Name, Tags, ExpectedAttendees, VenueName, City, State
   FROM dbo.Event
   WHERE EventID = 1
   ```

2. **Check Backend Service:**
   ```python
   events = await get_events(db, company_id)
   event = events[0]
   print(f"Tags: {event.Tags}")                    # Should have value
   print(f"EventType: {event.event_type}")          # Should not be None
   print(f"EventStatus: {event.event_status}")     # Should not be None
   ```

3. **Check API Response:**
   ```bash
   curl http://localhost:8000/api/events | jq '.events[0]'
   ```
   Verify all fields are present in JSON

4. **Check Frontend Transform:**
   ```typescript
   console.log('Raw backend event:', backendEvent)
   console.log('Transformed event:', transformEvent(backendEvent))
   ```

5. **Check Frontend Component:**
   ```typescript
   console.log('Event in component:', event)
   console.log('Event tags:', event.tags)
   console.log('Event type:', event.eventType)
   ```

---

## Summary

**Data Flow:**
```
Database (PascalCase) 
  → SQLAlchemy Model (PascalCase)
  → Service Layer (+ Eager Load Relationships)
  → Router (_event_to_response)
  → Pydantic Schema (snake_case field names, PascalCase aliases)
  → FastAPI JSON (snake_case) ← Serialization uses field names!
  → Frontend API Client (transformEvent)
  → TypeScript Types (camelCase)
  → React Components
```

**Key Takeaways:**
1. ✅ **Eager load relationships** in service layer
2. ✅ **Pydantic serializes using field names** (snake_case), not aliases
3. ✅ **Frontend transforms** snake_case → camelCase
4. ✅ **Verify each step** in the pipeline has all fields

