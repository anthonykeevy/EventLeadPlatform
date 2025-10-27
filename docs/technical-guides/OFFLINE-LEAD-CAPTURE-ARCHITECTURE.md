## Offline Lead Capture Architecture - Event Field Collection

**Created:** 2025-10-26  
**Context:** Story 1.16 Enhanced - Multi-Tab Auth + Offline Support  
**Priority:** Critical for hero feature (lead capture at events)

---

## 🎯 **Business Requirement**

Event staff use tablets/laptops at events to collect leads via public forms. Events often have:
- ❌ **Unreliable WiFi** (conference centers, outdoor venues)
- ❌ **Spotty cellular** (basement venues, crowded networks)
- ❌ **Network congestion** (hundreds of attendees on same network)

**Problem:** Lost internet = lost leads = angry customers = lost business

**Solution:** **Offline-first architecture** that queues leads locally and uploads when connection restores.

---

## 🏗️ **Architecture Overview**

```
┌──────────────────────────────────────────────────────────────┐
│                    PUBLIC LEAD FORM                          │
│                  (No Authentication Required)                │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
              ┌──────────────┐
              │  Submit Lead  │
              └──────┬───────┘
                     │
           ┌─────────▼──────────┐
           │  Network Available? │
           └─────────┬──────────┘
                     │
        ┌────────────┼────────────┐
        │ YES                     │ NO
        ▼                         ▼
┌───────────────┐         ┌──────────────────┐
│  Upload Now   │         │ Queue in IndexedDB│
│  to Backend   │         │ (Offline Storage) │
└───────┬───────┘         └────────┬─────────┘
        │                          │
        ▼                          │
  ┌─────────┐                      │
  │ Success │                      │
  └─────────┘                      │
                                   │
                     ┌─────────────▼──────────────┐
                     │  Background Sync Service   │
                     │  (Service Worker)          │
                     └─────────────┬──────────────┘
                                   │
                        ┌──────────▼───────────┐
                        │  Network Restored?   │
                        └──────────┬───────────┘
                                   │
                                   ▼
                         ┌──────────────────┐
                         │ Upload Queued    │
                         │ Leads to Backend │
                         └──────┬───────────┘
                                │
                                ▼
                          ┌──────────┐
                          │ Success! │
                          └──────────┘
```

---

## 💾 **Storage Strategy**

### **Why IndexedDB (not localStorage)?**

| Feature | localStorage | IndexedDB |
|---------|--------------|-----------|
| Storage Limit | ~5-10 MB | ~50 MB - 1 GB+ |
| Data Structure | String key-value | Complex objects, indexes |
| Query Performance | Slow (full scan) | Fast (indexes) |
| Async | No (blocking) | Yes (non-blocking) |
| Transaction Support | No | Yes |
| **Best For** | Small config data | Large datasets (leads!) |

**Example:** Event with 500 attendees:
- localStorage: Can store ~50-100 leads (might run out)
- IndexedDB: Can store 5,000+ leads (no problem)

---

## 🔄 **Data Flow**

### **Scenario 1: Online (Normal Operation)**
```typescript
// Lead form component
const handleSubmit = async (leadData) => {
  try {
    // Try immediate upload
    await submitLead(leadData)
    
    // Success! Show confirmation
    showSuccess('Lead captured!')
  } catch (error) {
    // Network error - queue for later
    await offlineQueue.enqueue('lead_submission', leadData)
    
    // Show offline message
    showInfo('Lead saved offline. Will upload when online.')
  }
}
```

### **Scenario 2: Offline (Queue Builds Up)**
```typescript
// All leads go to IndexedDB
await offlineQueue.enqueue('lead_submission', {
  formId: 123,
  eventId: 456,
  responses: {...},
  timestamp: Date.now(),
  deviceId: getDeviceFingerprint()
})

// Queue stats updated
// UI shows: "3 leads pending upload"
```

### **Scenario 3: Connection Restored**
```typescript
// Browser fires 'online' event
window.addEventListener('online', async () => {
  console.log('🌐 Connection restored')
  
  // Automatically process queue
  await offlineQueue.processQueue()
  
  // Show success notification
  showSuccess('3 leads uploaded successfully!')
})
```

---

## 🛡️ **Integration with Auth System**

### **Key Design Decision: Public Forms Are Auth-Free**

```typescript
// ✅ GOOD: Public form (no auth)
<Route path="/forms/:formId" element={<PublicFormView />} />

// Component
export function PublicFormView() {
  // NO useAuth() hook
  // NO authentication required
  // Works even if user is logged out
  
  const handleSubmit = async (data) => {
    // Try to submit
    if (navigator.onLine) {
      try {
        await fetch('/api/public/forms/submit', {
          method: 'POST',
          // NO Authorization header
          body: JSON.stringify(data)
        })
      } catch (error) {
        // Queue offline
        await offlineQueue.enqueue('lead_submission', data)
      }
    } else {
      // Offline - queue immediately
      await offlineQueue.enqueue('lead_submission', data)
    }
  }
}
```

**Why this works:**
- ✅ Public forms don't require login
- ✅ No auth tokens needed
- ✅ No multi-tab auth issues
- ✅ Can queue and upload without authentication
- ✅ Works even if auth session expires

---

## 🔐 **Form Builder vs. Public Forms**

### **Form Builder (Authenticated)**
```typescript
// Requires login
<ProtectedRoute path="/forms/builder/:formId" element={<FormBuilder />} />

export function FormBuilder() {
  const { user } = useAuth() // Requires auth
  
  // Register with unsaved work tracker
  useUnsavedWork('form_builder', 'form_builder', 'Form design changes', async () => {
    await saveFormDraft()
  })
  
  // Auto-save every 10 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      if (isDirty) {
        saveFormDraft()
      }
    }, 10000)
    
    return () => clearInterval(interval)
  }, [isDirty])
}
```

### **Public Forms (No Auth)**
```typescript
// NO authentication required
<Route path="/f/:shortCode" element={<PublicFormView />} />

export function PublicFormView() {
  // NO useAuth() - works for everyone
  
  // Still uses offline queue for reliability
  const handleSubmit = async (data) => {
    if (!navigator.onLine) {
      await offlineQueue.enqueue('lead_submission', data)
      showOfflineMessage()
      return
    }
    
    try {
      await submitLead(data)
      showSuccess()
    } catch (error) {
      await offlineQueue.enqueue('lead_submission', data)
      showQueuedMessage()
    }
  }
}
```

---

## 📊 **Complete Lead Capture Flow**

### **At the Event (Day 1)**

```
09:00 - Event starts, WiFi is working
├─ Lead 1: Submitted online ✅ (uploaded immediately)
├─ Lead 2: Submitted online ✅ (uploaded immediately)
│
10:30 - WiFi drops (too many attendees)
├─ Lead 3: Queued in IndexedDB 📦 (shows "Saved offline" message)
├─ Lead 4: Queued in IndexedDB 📦
├─ Lead 5: Queued in IndexedDB 📦
│   └─ UI shows: "3 leads pending upload"
│
12:00 - Lunch break, WiFi restores
├─ Browser detects: navigator.onLine = true
├─ Offline queue processes automatically
├─ Leads 3, 4, 5 upload in background
├─ UI shows: "✅ 3 leads uploaded!"
│
14:00 - WiFi drops again
├─ Lead 6: Queued 📦
├─ Lead 7: Queued 📦
│
17:00 - Event ends, team packs up
├─ Still offline
├─ 2 leads in queue
├─ Team drives back to office
│
17:30 - Team arrives at office, connects to office WiFi
├─ Browser: Online event fires
├─ Queue processes automatically
├─ Leads 6, 7 upload ✅
├─ UI shows: "All leads uploaded!"
│
✅ ZERO LEADS LOST!
```

---

## 🔧 **Implementation Guide**

### **Step 1: Public Form Component**

```typescript
export function PublicLeadForm({ formId }: { formId: string }) {
  const [isOnline, setIsOnline] = useState(navigator.onLine)
  const [queueStats, setQueueStats] = useState({ pending: 0 })
  
  // Listen for online/offline
  useEffect(() => {
    const handleOnline = () => setIsOnline(true)
    const handleOffline = () => setIsOnline(false)
    
    window.addEventListener('online', handleOnline)
    window.addEventListener('offline', handleOffline)
    
    return () => {
      window.removeEventListener('online', handleOnline)
      window.removeEventListener('offline', handleOffline)
    }
  }, [])
  
  // Subscribe to queue stats
  useEffect(() => {
    return offlineQueue.subscribe(setQueueStats)
  }, [])
  
  const handleSubmit = async (leadData: any) => {
    if (!navigator.onLine) {
      // Offline - queue immediately
      await offlineQueue.enqueue('lead_submission', {
        formId,
        ...leadData,
        capturedAt: new Date().toISOString()
      })
      
      showNotification('📦 Lead saved offline. Will upload when online.')
      return
    }
    
    try {
      // Try immediate upload
      const response = await fetch(`/api/public/forms/${formId}/submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(leadData)
      })
      
      if (!response.ok) throw new Error('Upload failed')
      
      showNotification('✅ Lead captured successfully!')
    } catch (error) {
      // Network error - queue for later
      await offlineQueue.enqueue('lead_submission', {
        formId,
        ...leadData,
        capturedAt: new Date().toISOString()
      })
      
      showNotification('📦 Lead queued. Will retry automatically.')
    }
  }
  
  return (
    <div>
      {/* Offline indicator */}
      {!isOnline && (
        <div className="bg-yellow-50 border border-yellow-400 p-3 rounded mb-4">
          <p className="text-yellow-800 text-sm">
            📡 Working offline. Leads will upload when connection restores.
          </p>
        </div>
      )}
      
      {/* Queue status */}
      {queueStats.pending > 0 && (
        <div className="bg-blue-50 border border-blue-400 p-3 rounded mb-4">
          <p className="text-blue-800 text-sm">
            📤 {queueStats.pending} lead(s) waiting to upload
          </p>
        </div>
      )}
      
      {/* Form fields */}
      <form onSubmit={handleSubmit}>
        {/* ... form fields ... */}
      </form>
    </div>
  )
}
```

### **Step 2: Service Worker (Background Sync)**

```javascript
// public/service-worker.js

// Register background sync
self.addEventListener('sync', async (event) => {
  if (event.tag === 'upload-leads') {
    event.waitUntil(uploadQueuedLeads())
  }
})

async function uploadQueuedLeads() {
  // Open IndexedDB
  const db = await openDB('eventlead_offline')
  const pending = await db.getAll('queue')
  
  // Upload each item
  for (const item of pending) {
    try {
      const response = await fetch('/api/public/forms/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(item.data)
      })
      
      if (response.ok) {
        // Remove from queue
        await db.delete('queue', item.id)
      }
    } catch (error) {
      // Will retry on next sync
      console.error('Background upload failed:', item.id)
    }
  }
}

// Register service worker
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/service-worker.js')
}
```

---

## 🚀 **How It Prevents Data Loss**

### **Scenario: Event Manager with 4 Forms Open**

```
CURRENT STATE:
Tab 1: Form Builder - VIP Form (unsaved changes)
Tab 2: Form Builder - General Form (unsaved changes)
Tab 3: Public form view (testing)
Tab 4: Dashboard

WHAT HAPPENS WHEN SOMEONE LOGS OUT IN TAB 4:

❌ OLD (Before Upgrade):
  → ALL tabs reload immediately
  → Tabs 1, 2 lose unsaved work
  → DISASTER!

✅ NEW (After Upgrade):
  → Tab 4 logs out normally
  → Tabs 1, 2 show BANNER: "Logged out in another tab"
  → Banner: "2 items with unsaved changes"
  → User clicks "Save & Continue"
  → Auto-save triggered
  → Forms saved to localStorage + backend
  → Auth syncs AFTER save completes
  → NO DATA LOSS! ✨
```

### **Scenario: Lost WiFi During Lead Capture**

```
EVENT VENUE:
10 tablets capturing leads (public forms, no auth)

11:00 AM - WiFi working
├─ Tablet 1: Lead captured → Upload success ✅
├─ Tablet 2: Lead captured → Upload success ✅

11:30 AM - WiFi dies (venue network overload)
├─ Tablet 1: Lead captured → Queued to IndexedDB 📦
├─ Tablet 2: Lead captured → Queued to IndexedDB 📦
├─ Tablet 3: Lead captured → Queued to IndexedDB 📦
├─ ...
├─ 50 leads queued across 10 tablets
├─ Users see: "📦 Saved offline - will upload automatically"

12:30 PM - Lunch break, WiFi restores
├─ ALL tablets detect: online event
├─ Background sync triggers
├─ 50 leads upload in parallel
├─ Users see: "✅ All leads uploaded!"

✅ ZERO LEADS LOST despite 1 hour of no WiFi!
```

---

## 🛠️ **Technical Implementation**

### **1. IndexedDB Schema**

```typescript
// Database: eventlead_offline
// Store: queue

interface QueuedLead {
  id: string                    // "lead_1698765432_abc123"
  type: 'lead_submission'       // Item type
  data: {
    formId: number
    eventId: number
    responses: Record<string, any>
    capturedAt: string          // ISO timestamp
    deviceId: string            // Device fingerprint
    metadata: {
      userAgent: string
      screenResolution: string
      location?: { lat: number, lng: number }
    }
  }
  timestamp: number             // Queue time
  retryCount: number            // Upload attempts
  lastRetry?: number            // Last attempt time
  error?: string                // Last error message
  status: 'pending' | 'uploading' | 'failed' | 'success'
}
```

### **2. Upload Strategy**

```typescript
// Exponential backoff for retries
const getRetryDelay = (retryCount: number) => {
  // 1st retry: 5 seconds
  // 2nd retry: 10 seconds
  // 3rd retry: 20 seconds
  // Max: 2 minutes
  return Math.min(5000 * Math.pow(2, retryCount), 120000)
}

// Process queue with retry logic
async function processQueue() {
  const pending = await offlineQueue.getPending()
  
  for (const item of pending) {
    try {
      await uploadWithRetry(item)
    } catch (error) {
      // Schedule retry
      const delay = getRetryDelay(item.retryCount)
      setTimeout(() => processQueue(), delay)
    }
  }
}
```

### **3. Conflict Resolution**

```typescript
// What if same lead submitted twice?
// (User clicks submit, queues offline, then WiFi restores and they submit again)

// Solution: Dedupe by unique ID
const createLeadId = (formId: number, timestamp: number, deviceId: string) => {
  return `lead_${formId}_${timestamp}_${deviceId}`
}

// Backend checks for duplicates
// POST /api/public/forms/{formId}/submit
{
  "leadId": "lead_123_1698765432_abc123",  // Client-generated ID
  "responses": {...}
}

// Backend:
// 1. Check if leadId already exists
// 2. If exists: Return 200 (idempotent)
// 3. If new: Insert and return 201
```

---

## 🎨 **User Experience**

### **Offline Indicator (Always Visible)**

```tsx
<div className="fixed top-0 left-0 right-0 z-50">
  {!isOnline && (
    <div className="bg-yellow-50 border-b-2 border-yellow-400 p-2 text-center">
      <p className="text-sm text-yellow-800 flex items-center justify-center gap-2">
        <WifiOff className="w-4 h-4" />
        Working offline • {queueStats.pending} leads queued
      </p>
    </div>
  )}
  
  {isOnline && queueStats.pending > 0 && (
    <div className="bg-blue-50 border-b-2 border-blue-400 p-2 text-center">
      <p className="text-sm text-blue-800 flex items-center justify-center gap-2">
        <Upload className="w-4 h-4 animate-bounce" />
        Uploading {queueStats.pending} queued leads...
      </p>
    </div>
  )}
</div>
```

### **Success States**

```tsx
// Immediate upload (online)
showToast({
  type: 'success',
  message: '✅ Lead captured!',
  duration: 2000
})

// Queued (offline)
showToast({
  type: 'info',
  message: '📦 Lead saved offline',
  description: 'Will upload when connection restores',
  duration: 4000
})

// Upload success (after queue processed)
showToast({
  type: 'success',
  message: '✅ All leads uploaded!',
  description: '3 leads synced to server',
  duration: 3000
})
```

---

## 🔍 **Impact on Form Builder**

### **Form Builder Auto-Save Strategy**

```typescript
export function FormBuilder() {
  const [formData, setFormData] = useState<FormData>()
  const [isDirty, setIsDirty] = useState(false)
  
  // Register with unsaved work tracker
  const { markDirty, markClean } = useUnsavedWork(
    'form_builder_main',
    'form_builder',
    'Form design changes',
    async () => {
      // Save callback
      await saveToBackend(formData)
      await saveToLocalStorage(formData) // Backup
    }
  )
  
  // Auto-save every 10 seconds
  useEffect(() => {
    if (!isDirty) return
    
    const autoSaveTimer = setInterval(async () => {
      try {
        // Try backend first
        await saveToBackend(formData)
        
        // Also save to localStorage (backup)
        saveToLocalStorage(formData)
        
        markClean()
        showToast({ type: 'success', message: 'Auto-saved' })
      } catch (error) {
        // Backend failed - at least we have localStorage
        saveToLocalStorage(formData)
        showToast({ type: 'warning', message: 'Saved locally (offline)' })
      }
    }, 10000)
    
    return () => clearInterval(autoSaveTimer)
  }, [formData, isDirty, markClean])
  
  // Restore draft on mount
  useEffect(() => {
    const draft = loadFromLocalStorage()
    if (draft) {
      if (confirm('Found unsaved changes. Restore?')) {
        setFormData(draft)
      }
    }
  }, [])
  
  // Handle form changes
  const handleChange = (field: string, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }))
    markDirty()
  }
  
  return (
    <div>
      {/* Auto-save indicator */}
      <div className="fixed top-4 right-4 text-sm text-gray-500">
        {isDirty ? '💾 Saving...' : '✅ All changes saved'}
      </div>
      
      {/* Form builder UI */}
      <FormCanvas data={formData} onChange={handleChange} />
    </div>
  )
}
```

---

## 📈 **Data Loss Prevention Summary**

| Scenario | Old Behavior | New Behavior |
|----------|--------------|--------------|
| **Logout in another tab** | ❌ All tabs reload → lose work | ✅ Show banner → save first → no data loss |
| **Login in another tab** | ❌ All tabs reload → lose work | ✅ Show banner → continue working |
| **Lost WiFi during lead capture** | ❌ Leads lost | ✅ Queue in IndexedDB → upload later |
| **Browser crash** | ❌ All work lost | ✅ Restore from localStorage on next load |
| **Tab accidentally closed** | ❌ Work lost if not saved | ✅ beforeunload warning + auto-save |
| **Multiple forms open** | ❌ All reload together | ✅ Each tab independent + auto-save |

---

## 🎯 **Recommended Implementation Timeline**

### **Week 1 (NOW - Foundation)**
✅ Upgrade auth to graceful sync
✅ Add unsaved work tracker
✅ Add offline queue (IndexedDB)
✅ Add network listeners

### **Week 2 (Form Builder)**
🔄 Implement form builder with auto-save
🔄 Integrate unsaved work tracker
🔄 Add localStorage backup
🔄 Test multi-tab scenarios

### **Week 3 (Public Forms)**
🔄 Build public form renderer
🔄 Integrate offline queue
🔄 Add Service Worker for background sync
🔄 Test offline scenarios at mock event

### **Week 4 (Testing & Polish)**
🔄 Load test with 1000+ queued leads
🔄 Test network interruption scenarios
🔄 Test multi-device sync
🔄 Add admin dashboard for queue monitoring

---

## 🔒 **Security Considerations**

### **Public Forms (No Auth)**
- ✅ Rate limiting (max 10 submissions per IP per hour)
- ✅ CAPTCHA for public forms (prevent spam)
- ✅ Form validation (backend always validates)
- ✅ Client-generated lead IDs (prevent duplicates)

### **Offline Queue**
- ✅ IndexedDB is origin-isolated (safe)
- ✅ No sensitive data in queue (just lead responses)
- ✅ Queue cleanup after successful upload
- ✅ Max queue age: 7 days (auto-cleanup)

---

## 📊 **Monitoring & Admin Dashboard**

```typescript
// Admin view: Queue status across all devices
GET /api/admin/offline-queue/stats

{
  "totalDevices": 15,
  "totalQueued": 127,
  "pending": 12,
  "failed": 3,
  "oldestItemAge": 7200000, // 2 hours
  "deviceStats": [
    {
      "deviceId": "abc123",
      "deviceName": "Tablet #1",
      "queuedCount": 8,
      "lastSeen": "2025-10-26T12:30:00Z"
    }
  ]
}
```

---

**This architecture ensures ZERO data loss for both form building AND lead capture!** ✅


