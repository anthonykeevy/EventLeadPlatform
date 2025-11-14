# Platform Offline-First Capability Proposal

## Problem Statement

During UAT testing, the following issues were identified:
1. **No visual offline indicator** - Users don't know they're offline
2. **Form data loss** - Page redirects to login when offline, losing unsaved work
3. **No auto-save** - Form data not persisted when offline
4. **No auto-retry** - When connection restored, queued work doesn't automatically sync

## Security Considerations

### ✅ Safe to Store Offline
- Form draft data (event details, lead forms)
- User preferences
- UI state (active tabs, filters)
- Queue metadata (timestamps, retry counts)

### ❌ Never Store Offline
- Access tokens (already handled by tokenStorage)
- Refresh tokens (already handled by tokenStorage)
- Passwords or sensitive PII
- Payment information

### Security Measures
1. **Token Validation on Reconnect**: When back online, validate token before retrying requests
2. **Data Validation**: Validate all queued data before sending to backend
3. **Expiry Handling**: If token expired while offline, refresh before retrying
4. **Rate Limiting**: Prevent queue flooding with exponential backoff
5. **Local Storage Encryption**: Consider encrypting sensitive form data (future enhancement)

## Solution Architecture

### 1. Offline Status Indicator Component

**Location**: `frontend/src/features/ux/components/OfflineIndicator.tsx`

**Features**:
- Visual banner/icon in top-right corner
- Shows "Offline" status with warning icon
- Shows "Syncing..." when processing queue
- Shows "X items pending" count
- Auto-hides when online and queue empty

**Implementation**:
```typescript
- Subscribe to navigator.onLine events
- Subscribe to offlineQueue stats
- Display persistent indicator when offline
- Show sync progress when processing queue
```

### 2. Enhanced Offline Queue

**Extend**: `frontend/src/utils/offlineQueue.ts`

**New Queue Types**:
- `event_draft` - Event creation/editing drafts
- `event_create` - Event creation requests (queued when offline)
- `event_update` - Event update requests (queued when offline)
- `form_draft` - Lead form drafts (existing)

**New Features**:
- Form state persistence (auto-save every 30 seconds)
- Request queuing (queue API calls when offline)
- Smart retry (exponential backoff, max 5 retries)
- Conflict resolution (handle concurrent edits)

### 3. Form Auto-Save Service

**New File**: `frontend/src/utils/formAutoSave.ts`

**Features**:
- Auto-save form state to IndexedDB every 30 seconds
- Restore form state on page reload
- Clear saved state after successful submission
- Handle multiple forms (event creation, event edit, lead forms)

**Storage Key Format**: `form_draft_{formType}_{formId}_{userId}`

### 4. Network-Aware Axios Interceptor

**Modify**: All axios clients (eventsApi, authApi, etc.)

**Behavior**:
- Detect offline state before making requests
- Queue requests instead of failing immediately
- Prevent login redirect when offline (401 errors)
- Auto-retry queued requests when back online

**Implementation**:
```typescript
// Pseudo-code
if (!navigator.onLine) {
  // Queue request instead of failing
  await offlineQueue.enqueue('api_request', {
    method: config.method,
    url: config.url,
    data: config.data,
    headers: config.headers
  })
  // Return a pending promise that resolves when queued
  return Promise.resolve({ status: 'queued', data: null })
}

// If 401 and offline, don't clear tokens - queue refresh
if (error.response?.status === 401 && !navigator.onLine) {
  await offlineQueue.enqueue('token_refresh', {})
  return Promise.resolve({ status: 'queued', data: null })
}
```

### 5. Offline-Aware Event Creation

**Modify**: `frontend/src/features/events/components/CreateEventModal.tsx`

**Features**:
- Auto-save form state every 30 seconds
- Show "Draft saved" notification
- Restore form state on page reload
- Queue create request when offline
- Show "Will sync when online" message

**Implementation**:
```typescript
// Auto-save hook
useEffect(() => {
  const interval = setInterval(() => {
    if (formData.name || formData.startDatetime) {
      formAutoSave.save('event_create', formData)
    }
  }, 30000) // 30 seconds
  
  return () => clearInterval(interval)
}, [formData])

// Restore on mount
useEffect(() => {
  const draft = formAutoSave.restore('event_create')
  if (draft) {
    setFormData(draft)
    toast.info('Draft restored', 'Your previous work has been restored')
  }
}, [])

// Handle submit when offline
const handleSubmit = async () => {
  if (!navigator.onLine) {
    await offlineQueue.enqueue('event_create', formData)
    toast.success('Event queued', 'Will be created when connection is restored')
    onClose()
    return
  }
  // Normal submit flow...
}
```

### 6. Token Refresh Queue Handler

**New**: Token refresh queuing in offlineQueue

**Behavior**:
- When offline and token expires, queue refresh request
- When back online, refresh token first, then process other queue items
- If refresh fails, show "Please log in again" message

## Implementation Plan

### Phase 1: Core Infrastructure (Week 1)
1. ✅ Create `OfflineIndicator` component
2. ✅ Extend `offlineQueue` with new queue types
3. ✅ Create `formAutoSave` service
4. ✅ Add offline detection to axios interceptors

### Phase 2: Event Forms (Week 1)
5. ✅ Integrate auto-save into `CreateEventModal`
6. ✅ Integrate auto-save into `EditEventModal`
7. ✅ Queue event create/update requests when offline
8. ✅ Handle queue processing on reconnect

### Phase 3: Testing & Refinement (Week 2)
9. ✅ Test offline scenarios
10. ✅ Test token expiry during offline
11. ✅ Test concurrent edits (conflict resolution)
12. ✅ Performance testing (large forms, many queued items)

### Phase 4: Platform-Wide Rollout (Week 2)
13. ✅ Apply to lead forms
14. ✅ Apply to other forms (invitations, etc.)
15. ✅ Documentation
16. ✅ User training materials

## User Experience Flow

### Scenario: User Creates Event While Offline

1. **User starts creating event** → Form opens normally
2. **User goes offline** → Offline indicator appears in top-right
3. **User fills form** → Auto-saves every 30 seconds (silent)
4. **User submits** → Shows "Event queued - will sync when online"
5. **User closes browser** → Form state saved to IndexedDB
6. **User reopens browser** → Form state restored, "Draft restored" notification
7. **Connection restored** → Queue processes automatically
8. **Event created** → Success notification, draft cleared

### Scenario: Token Expires While Offline

1. **User offline, token expires** → No immediate action
2. **User submits form** → Queued with "token_refresh" flag
3. **Connection restored** → Token refresh attempted first
4. **If refresh succeeds** → Process queued requests
5. **If refresh fails** → Show "Please log in again" message, preserve draft

## Technical Details

### Storage Strategy

**IndexedDB** (via offlineQueue):
- Queued API requests
- Form drafts (large data)
- Queue metadata

**localStorage** (via formAutoSave):
- Form state (small, fast access)
- Last save timestamp
- Form version (for conflict detection)

### Queue Processing Order

1. Token refresh requests (if any)
2. Create requests (before updates)
3. Update requests
4. Delete requests
5. Other requests

### Conflict Resolution

**Strategy**: Last-write-wins with user notification
- When processing queued update, check if event was modified
- If modified, show conflict resolution dialog
- User chooses: Keep local changes, Keep server changes, or Merge

## Security Checklist

- [x] No tokens stored in offline queue
- [x] Form data validated before queuing
- [x] Token validated before processing queue
- [x] Rate limiting on queue processing
- [x] Queue size limits (prevent DoS)
- [x] Auto-cleanup of old queue items
- [x] No sensitive PII in localStorage
- [x] HTTPS-only in production (enforced by browser)

## Testing Scenarios

### Test Case 1: Basic Offline Form Creation
1. Go offline
2. Create event form
3. Fill form
4. Submit form
5. Verify queued
6. Go online
7. Verify event created

### Test Case 2: Token Expiry During Offline
1. Login
2. Go offline
3. Wait for token expiry
4. Fill and submit form
5. Go online
6. Verify token refresh
7. Verify event created

### Test Case 3: Page Reload During Offline
1. Go offline
2. Fill form
3. Reload page
4. Verify form restored
5. Complete and submit
6. Go online
7. Verify event created

### Test Case 4: Multiple Forms Offline
1. Go offline
2. Create 3 events
3. Edit 2 events
4. Go online
5. Verify all 5 requests processed
6. Verify correct order (creates before updates)

### Test Case 5: Conflict Resolution
1. User A edits event (online)
2. User B edits same event (offline)
3. User B goes online
4. Verify conflict dialog shown
5. User B chooses "Keep local changes"
6. Verify User B's changes applied

## Success Metrics

- **Form completion rate**: Increase by 15% (fewer abandoned forms)
- **User satisfaction**: Reduce "lost work" complaints by 80%
- **Queue success rate**: >95% of queued requests succeed
- **Performance**: <100ms form restore time
- **Storage**: <10MB offline data per user

## Future Enhancements

1. **Service Worker**: True offline-first with background sync
2. **Conflict Resolution UI**: Visual diff tool for conflicts
3. **Offline Analytics**: Track offline usage patterns
4. **Progressive Web App**: Installable app with offline support
5. **Encrypted Storage**: Encrypt sensitive form data
6. **Multi-device Sync**: Sync drafts across devices

## Configuration Decisions

1. **Queue Size Limit**: **100 items** (confirmed)
   - **Clarification**: 1 item = 1 API operation (e.g., 1 event creation, 1 event update, 1 form submission)
   - A complete form submission = 1 queue item (not individual fields)
   - 100 items covers 100 complete operations (e.g., 100 event creations, or mix of creates/updates/deletes)
   - **Storage**: Each item stores the complete request payload, so 100 items is sufficient for most use cases
   - **Configurable**: Will be stored in app settings, customers can see their queue status when offline

2. **Queue Contents**: **Only unprocessed items** (pending/failed status)
   - Processed items (success status) are auto-cleaned after 1 hour
   - Failed items remain until manually retried or auto-retried on reconnect
   - **Customer Visibility**: Queue status shown in offline indicator (e.g., "3 items pending")
   - **App Setting**: Queue limit configurable per customer (default: 100)

3. **Queue Age Limit**: **7 days** (confirmed)
   - Auto-delete items older than 7 days
   - Prevents stale data accumulation
   - Configurable in app settings

4. **Notification Frequency**: **Silent after first save** (confirmed)
   - Show "Draft saved" notification only on first auto-save
   - Subsequent saves are silent (no notification spam)
   - User can see save status in UI if needed

5. **Search Offline Handling**: **Show message in results area** (NEW)
   - When offline, show message in search results: "Search unavailable while offline. Please reconnect to search for events."
   - Not noisy - just replaces empty results with helpful message
   - Applies to: Public Event Search, Company Network Search, Admin Event Search

