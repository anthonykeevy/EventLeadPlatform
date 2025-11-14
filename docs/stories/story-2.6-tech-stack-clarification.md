# Story 2.6: Tech Stack Clarification

**Date:** November 5, 2025  
**Topic:** TanStack Query vs TanStack Table, Foreign Key Handling, Tech Stack Architecture

---

## Question 1: TanStack Query vs TanStack Table - Do We Need to Upgrade?

### Answer: No upgrade needed - they are different products

**Key Point:** `@tanstack/react-query` and `@tanstack/react-table` are **separate products** from the TanStack ecosystem.

### Current State

**TanStack Query (Already Installed):**
- Package: `@tanstack/react-query`
- Version: `5.8.4` ✅ (Current and stable)
- Purpose: **Data fetching and caching** (API state management)
- Status: **NO UPGRADE NEEDED**

**TanStack Table (New Addition):**
- Package: `@tanstack/react-table`
- Version: `v8` (Latest stable)
- Purpose: **Table component library** (UI component for displaying data)
- Status: **NEW INSTALLATION** (separate package)

### Why They're Confused

Both products are from **TanStack** (formerly React Query team), but they serve different purposes:

| Product | Purpose | What It Does |
|---------|---------|--------------|
| **TanStack Query** | Data fetching | Manages API calls, caching, refetching, mutations |
| **TanStack Table** | UI component | Displays data in table format with sorting, filtering, pagination |

### How They Work Together

```typescript
// TanStack Query fetches data from API
const { data, isLoading } = useQuery({
  queryKey: ['admin-events'],
  queryFn: () => fetchAdminEvents()
})

// TanStack Table displays the data
const table = useReactTable({
  data: data ?? [],  // ← Data from TanStack Query
  columns: eventColumns,
  // ...
})
```

### Current Usage of TanStack Query

**Installed in:** `frontend/package.json`  
**Current Version:** `5.8.4` ✅  
**Status:** Stable, no upgrade needed

**Where It's Used:**
- Test utilities: `frontend/src/test/utils.tsx` (QueryClientProvider)
- Configuration hooks: `docs/EPIC-1-DATABASE-CONFIGURATION-REDESIGN.md` (useAppConfig, useValidationRules)
- Story documentation: References to using TanStack Query for caching
- **Note:** Currently not heavily used in production code yet (planned for future stories)

**What Currently Uses TanStack Query:**
1. **Test Setup** - QueryClientProvider for test environment
2. **Planned Usage** - Documented in stories for:
   - Dashboard data caching (Story 1.18)
   - Configuration data fetching
   - API state management (future implementation)

**Migration Impact: NONE**
- TanStack Query v5.8.4 is stable and current
- No breaking changes needed
- TanStack Table v8 is a **separate package** - no conflict

### Installation Command

```bash
# Install TanStack Table (new package)
npm install @tanstack/react-table

# TanStack Query stays as-is (already installed)
# No upgrade needed
```

---

## Question 2: Foreign Key Handling in Tables - Dropdowns for FK Values

### Answer: Yes, TanStack Table can handle foreign keys as dropdowns

**Key Point:** TanStack Table is **headless** (no default rendering), so you have full control over how foreign keys are displayed and edited.

### Current Pattern in Codebase

**Example: CountrySelector Component**
- Location: `frontend/src/features/validation/components/CountrySelector.tsx`
- Pattern: Dropdown select for foreign key relationships
- Uses: Native `<select>` element with options from API

### How to Handle Foreign Keys in TanStack Table

**Option 1: Display FK as Text (Read-Only)**
```typescript
// Column definition - show FK relationship name
{
  accessorKey: 'eventType',
  header: 'Event Type',
  cell: ({ row }) => {
    // Backend includes FK relationship data
    return row.original.eventType?.name || 'N/A'
  }
}
```

**Option 2: Inline Dropdown (Editable)**
```typescript
// Column definition - editable dropdown
{
  accessorKey: 'eventTypeId',
  header: 'Event Type',
  cell: ({ row, table }) => {
    const [isEditing, setIsEditing] = useState(false)
    const eventTypes = useEventTypes() // Fetch from API
    
    if (isEditing) {
      return (
        <select
          value={row.original.eventTypeId}
          onChange={(e) => {
            // Update row data
            table.options.meta?.updateData(row.index, 'eventTypeId', parseInt(e.target.value))
          }}
        >
          {eventTypes.map(type => (
            <option key={type.id} value={type.id}>
              {type.name}
            </option>
          ))}
        </select>
      )
    }
    
    return (
      <span onClick={() => setIsEditing(true)}>
        {row.original.eventType?.name || 'N/A'}
      </span>
    )
  }
}
```

**Option 3: Expandable Row Form (Recommended for Admin)**
```typescript
// When row is expanded, show form below with dropdowns
{
  id: 'expander',
  cell: ({ row }) => (
    <button onClick={() => row.toggleExpanded()}>
      {row.getIsExpanded() ? '▼' : '▶'}
    </button>
  )
}

// Expanded row content
{row.getIsExpanded() && (
  <tr>
    <td colSpan={columns.length}>
      <EventEditForm 
        event={row.original}
        eventTypes={eventTypes}  // Dropdown options
        eventStatuses={eventStatuses}
        companies={companies}
        onSave={(updatedEvent) => {
          // Update via API
          updateEvent(row.original.id, updatedEvent)
        }}
      />
    </td>
  </tr>
)}
```

### Event Table Foreign Keys

**Event Table Foreign Keys (from schema):**
1. **EventTypeID** → `ref.EventType` (Trade Show, Conference, Expo, etc.)
2. **EventStatusID** → `ref.EventStatus` (Draft, Published, Completed, etc.)
3. **IndustryID** → `Industry` (optional - industry classification)
4. **CountryID** → `Country` (optional - country classification)
5. **CompanyID** → `Company` (event owner)
6. **OrganizerCompanyID** → `Company` (optional - organizer company)
7. **CreatedBy** → `User` (event creator)
8. **UpdatedBy** → `User` (last updater)
9. **PublicReviewBy** → `User` (admin reviewer)

### Recommended Pattern for Admin Event Management

**For Admin Event Management Table:**

1. **Display FK as Text** (default view)
   - Show relationship name (e.g., "Trade Show" instead of "1")
   - Backend includes FK relationship data in response

2. **Inline Editing** (quick edits)
   - Click cell → dropdown appears
   - Select new value → save immediately
   - Good for: EventType, EventStatus, Industry

3. **Expandable Row Form** (complex edits)
   - Click expand button → form appears below
   - Full form with all dropdowns
   - Good for: Company, Organizer, Country

### Implementation Example

```typescript
// Event Management Tab with FK Dropdowns
const EventManagementTab = () => {
  // Fetch reference data for dropdowns
  const { data: eventTypes } = useQuery({
    queryKey: ['event-types'],
    queryFn: () => fetchEventTypes()
  })
  
  const { data: eventStatuses } = useQuery({
    queryKey: ['event-statuses'],
    queryFn: () => fetchEventStatuses()
  })
  
  const { data: companies } = useQuery({
    queryKey: ['admin-companies'],
    queryFn: () => fetchAdminCompanies()
  })
  
  // Column definitions with FK dropdowns
  const columns: ColumnDef<Event>[] = [
    {
      accessorKey: 'name',
      header: 'Event Name'
    },
    {
      accessorKey: 'eventTypeId',
      header: 'Event Type',
      cell: ({ row }) => {
        const eventType = eventTypes?.find(t => t.id === row.original.eventTypeId)
        return eventType?.name || 'N/A'
      },
      // Inline editing dropdown
      enableEditing: true,
      editCell: ({ row, table }) => (
        <select
          value={row.original.eventTypeId}
          onChange={(e) => {
            table.options.meta?.updateData(
              row.index, 
              'eventTypeId', 
              parseInt(e.target.value)
            )
          }}
        >
          {eventTypes?.map(type => (
            <option key={type.id} value={type.id}>
              {type.name}
            </option>
          ))}
        </select>
      )
    },
    // ... more columns
  ]
  
  return <DataTable data={events} columns={columns} />
}
```

---

## Question 3: How TanStack Query Works with SQLAlchemy - Tech Stack Architecture

### Answer: They work together through the API layer

**Key Point:** TanStack Query (frontend) and SQLAlchemy (backend) are **separated by the API layer** - they don't directly interact.

### Tech Stack Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                      │
├─────────────────────────────────────────────────────────┤
│ TanStack Query (v5.8.4)                                 │
│   ↓ Fetches data via HTTP                               │
│   ↓ Manages caching & state                             │
│ Axios (HTTP Client)                                     │
│   ↓ Makes HTTP requests                                 │
│   ↓ Handles authentication                               │
└─────────────────────────────────────────────────────────┘
                      ↓ HTTP/REST API
┌─────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                     │
├─────────────────────────────────────────────────────────┤
│ FastAPI (REST API)                                      │
│   ↓ Receives HTTP requests                              │
│   ↓ Validates with Pydantic                             │
│ SQLAlchemy (ORM)                                        │
│   ↓ Queries database                                    │
│   ↓ Maps database rows to Python objects                │
└─────────────────────────────────────────────────────────┘
                      ↓ SQL Queries
┌─────────────────────────────────────────────────────────┐
│                    DATABASE (SQL Server)                 │
├─────────────────────────────────────────────────────────┤
│ MS SQL Server 2022                                      │
│   ↓ Stores data                                         │
│   ↓ Enforces constraints                                │
└─────────────────────────────────────────────────────────┘
```

### How They Work Together

**1. Frontend: TanStack Query**
```typescript
// Frontend: Fetch events from API
const { data, isLoading } = useQuery({
  queryKey: ['admin-events'],
  queryFn: async () => {
    // Axios makes HTTP request to backend
    const response = await axios.get('/api/admin/events')
    return response.data  // JSON data from backend
  }
})
```

**2. Backend: FastAPI + SQLAlchemy**
```python
# Backend: FastAPI endpoint
@router.get("/api/admin/events")
async def get_admin_events(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    # SQLAlchemy queries database
    events = db.query(Event).all()
    
    # Convert SQLAlchemy models to Pydantic schemas (JSON)
    return [EventResponse.from_orm(event) for event in events]
```

**3. Data Flow:**
```
Frontend (React) 
  → TanStack Query (caching)
  → Axios (HTTP request)
  → Backend API (FastAPI)
  → SQLAlchemy (database query)
  → SQL Server (data storage)
  → SQLAlchemy (Python objects)
  → Pydantic (JSON serialization)
  → HTTP Response (JSON)
  → Axios (HTTP response)
  → TanStack Query (cache & state)
  → React Component (render)
```

### Tech Stack Components

**Frontend Stack:**
- **React 18.2.0** - UI framework
- **TypeScript 5.2.2** - Type safety
- **TanStack Query 5.8.4** - Data fetching & caching
- **TanStack Table v8** - Table component (NEW)
- **Axios 1.6.2** - HTTP client
- **Tailwind CSS 3.3.5** - Styling

**Backend Stack:**
- **FastAPI 0.104.1** - REST API framework
- **Python 3.11.6** - Backend language
- **SQLAlchemy 2.0.23** - ORM (database abstraction)
- **Pydantic 2.5.0** - Data validation & serialization
- **Alembic 1.12.1** - Database migrations

**Database:**
- **MS SQL Server 2022** - Data storage

### Key Points

1. **TanStack Query ≠ SQLAlchemy**
   - TanStack Query: Frontend data fetching (React)
   - SQLAlchemy: Backend database access (Python)
   - They communicate via HTTP/REST API

2. **Data Flow**
   - Frontend requests data → Backend queries database → Returns JSON → Frontend caches & displays

3. **No Direct Connection**
   - TanStack Query doesn't directly access SQLAlchemy
   - SQLAlchemy doesn't directly access TanStack Query
   - They're separated by the API layer (FastAPI)

4. **Benefits of This Architecture**
   - **Separation of Concerns:** Frontend and backend are independent
   - **Scalability:** Can scale frontend and backend separately
   - **Technology Independence:** Can change frontend or backend without affecting the other
   - **Security:** Database is not directly exposed to frontend

### Example: Event Management Flow

**1. Admin clicks "Event Management" tab**
```typescript
// Frontend: TanStack Query fetches events
const { data: events } = useQuery({
  queryKey: ['admin-events'],
  queryFn: () => adminApi.getEvents()
})
```

**2. Axios makes HTTP request**
```typescript
// frontend/src/features/admin/api/adminApi.ts
export const getEvents = async () => {
  const response = await axios.get('/api/admin/events')
  return response.data
}
```

**3. FastAPI receives request**
```python
# backend/modules/admin/dashboard_router.py
@router.get("/api/admin/events")
async def get_admin_events(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    # Verify admin role
    if current_user.role != "system_admin":
        raise HTTPException(403, "Admin access required")
    
    # SQLAlchemy queries database
    events = db.query(Event).all()
    
    # Convert to JSON via Pydantic
    return [EventResponse.from_orm(event) for event in events]
```

**4. SQLAlchemy queries database**
```python
# SQLAlchemy generates SQL:
# SELECT * FROM [dbo].[Event] WHERE IsDeleted = 0

# Returns Python objects:
# [Event(id=1, name="Trade Show 2025", ...), ...]
```

**5. Pydantic serializes to JSON**
```python
# Pydantic converts SQLAlchemy models to JSON:
# {
#   "id": 1,
#   "name": "Trade Show 2025",
#   "eventTypeId": 1,
#   "eventType": {"id": 1, "name": "Trade Show"},
#   ...
# }
```

**6. TanStack Query caches & displays**
```typescript
// TanStack Query caches the response
// TanStack Table displays the data
const table = useReactTable({
  data: events,  // ← Cached data from TanStack Query
  columns: eventColumns,
  // ...
})
```

---

## Summary

### Question 1: TanStack Query Upgrade?
**Answer:** ❌ **NO UPGRADE NEEDED**
- TanStack Query v5.8.4 is current and stable
- TanStack Table v8 is a **separate package** (new installation)
- No conflict - they work together

### Question 2: Foreign Key Dropdowns?
**Answer:** ✅ **YES, FULLY SUPPORTED**
- TanStack Table is headless (full control)
- Can display FK as text (read-only)
- Can use inline dropdowns (editable cells)
- Can use expandable row forms (complex edits)
- Pattern matches existing codebase (CountrySelector example)

### Question 3: TanStack Query + SQLAlchemy?
**Answer:** ✅ **THEY WORK TOGETHER THROUGH API LAYER**
- TanStack Query: Frontend data fetching (React)
- SQLAlchemy: Backend database access (Python)
- Communication: HTTP/REST API (FastAPI)
- Data flow: Frontend → API → Backend → Database → Backend → API → Frontend

---

**Prepared By:** Product Manager (John)  
**Date:** November 5, 2025

