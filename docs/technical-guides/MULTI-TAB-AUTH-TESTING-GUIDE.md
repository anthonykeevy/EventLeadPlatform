# Multi-Tab Authentication Testing Guide

**Feature:** Graceful Multi-Tab Auth Sync + Offline Lead Capture  
**Story:** 1.16 Enhanced  
**Date:** 2025-10-26

---

## 🎯 **What Was Implemented**

1. ✅ **Graceful auth sync** - No forced reloads
2. ✅ **Unsaved work detection** - Protects user data
3. ✅ **Auth change banner** - Non-blocking warnings
4. ✅ **BroadcastChannel + fallback** - Modern + compatible
5. ✅ **Offline queue** - IndexedDB for lead capture
6. ✅ **Multi-tab coordination** - All tabs stay in sync

---

## 🧪 **Test Scenarios**

### **Test 1: Basic Multi-Tab Logout Sync** ⏱️ 2 minutes

**Setup:**
1. Open browser to http://localhost:3000
2. Login as `admin@test.com`
3. Open 2 more tabs to /dashboard
4. All 3 tabs should show dashboard

**Test:**
1. In Tab 1, click "Logout"
2. ✅ **Expected:** Tab 1 navigates to /login (no reload)
3. ✅ **Expected:** Tabs 2 & 3 show banner: "You've been logged out in another tab"
4. Click "Continue" in banner
5. ✅ **Expected:** Tabs 2 & 3 navigate to /login

**Pass Criteria:**
- No page reloads (check browser refresh indicator)
- Banner appears in other tabs
- All tabs end up on /login
- No console errors

---

### **Test 2: Multi-Tab Login Sync** ⏱️ 2 minutes

**Setup:**
1. Open 3 browser tabs to /login (not logged in)

**Test:**
1. In Tab 1, login as `admin@test.com`
2. ✅ **Expected:** Tab 1 navigates to /dashboard
3. ✅ **Expected:** Tabs 2 & 3 show banner: "Logged in as admin@test.com in another tab"
4. Click "Continue" in banner
5. ✅ **Expected:** Tabs 2 & 3 navigate to /dashboard

**Pass Criteria:**
- No page reloads
- Banner appears in other tabs
- All tabs show same user's dashboard
- No console errors

---

### **Test 3: Unsaved Work Protection** ⏱️ 5 minutes

**Setup:**
1. Login as `admin@test.com`
2. Open developer console in Tab 1
3. Simulate unsaved work by running:
```javascript
// In browser console
window.unsavedWorkTracker.register({
  id: 'test_form_1',
  type: 'form_builder',
  description: 'Test Form Design',
  isDirty: true,
  autoSaveEnabled: true,
  onSave: async () => {
    console.log('Saving test form...')
    await new Promise(resolve => setTimeout(resolve, 1000))
    console.log('Test form saved!')
  }
})
```

**Test:**
1. Open Tab 2 to /dashboard
2. In Tab 2, click "Logout"
3. Tab 2 logs out normally
4. ✅ **Expected:** Tab 1 shows banner: "You've been logged out in another tab"
5. ✅ **Expected:** Banner shows: "1 unsaved item: Test Form Design"
6. Click "Save & Continue"
7. ✅ **Expected:** Console shows "Saving test form..."
8. ✅ **Expected:** Console shows "Test form saved!"
9. ✅ **Expected:** Tab 1 logs out after save completes

**Pass Criteria:**
- Banner appears with unsaved work warning
- Save function is called
- Logout happens AFTER save completes
- No data loss

---

### **Test 4: Offline Lead Capture** ⏱️ 10 minutes

**Setup:**
1. Open browser to a public form (will build in Epic 2)
2. Open DevTools → Network tab

**Test:**
1. In Network tab, select "Offline" mode
2. Fill out form and submit
3. ✅ **Expected:** See message: "📦 Lead saved offline"
4. Check browser console:
```javascript
// Check queue
const stats = await window.offlineQueue.getStats()
console.log(stats) // Should show 1 pending item
```
5. In Network tab, select "Online" mode
6. Wait 2-3 seconds
7. ✅ **Expected:** See message: "✅ Lead uploaded!"
8. Check console again:
```javascript
const stats = await window.offlineQueue.getStats()
console.log(stats) // Should show 0 pending, 1 success
```

**Pass Criteria:**
- Lead queued when offline
- Lead uploaded when online
- User sees appropriate messages
- No errors in console

---

### **Test 5: Form Builder Multi-Tab (Simulated)** ⏱️ 5 minutes

**Setup:**
1. Login as `admin@test.com`
2. Open 4 tabs to /dashboard
3. In each tab, simulate unsaved work:

**Tab 1:**
```javascript
window.unsavedWorkTracker.register({
  id: 'form_1',
  type: 'form_builder',
  description: 'VIP Registration Form',
  isDirty: true,
  autoSaveEnabled: true,
  onSave: async () => {
    console.log('Saving VIP form...')
    await new Promise(resolve => setTimeout(resolve, 1000))
  }
})
```

**Tab 2:**
```javascript
window.unsavedWorkTracker.register({
  id: 'form_2',
  type: 'form_builder',
  description: 'General Admission Form',
  isDirty: true,
  autoSaveEnabled: true,
  onSave: async () => {
    console.log('Saving General form...')
    await new Promise(resolve => setTimeout(resolve, 1000))
  }
})
```

**Tab 3:**
```javascript
window.unsavedWorkTracker.register({
  id: 'form_3',
  type: 'form_builder',
  description: 'Vendor Registration Form',
  isDirty: true,
  autoSaveEnabled: true,
  onSave: async () => {
    console.log('Saving Vendor form...')
    await new Promise(resolve => setTimeout(resolve, 1000))
  }
})
```

**Tab 4:** (Leave clean - no unsaved work)

**Test:**
1. In Tab 4, click "Logout"
2. ✅ **Expected:** Tab 4 logs out immediately (no unsaved work)
3. ✅ **Expected:** Tabs 1, 2, 3 show banner with unsaved work warning
4. In Tab 1, click "Save & Continue"
5. ✅ **Expected:** Console shows "Saving VIP form..."
6. ✅ **Expected:** Tab 1 logs out after save
7. In Tab 2, click "X" (dismiss banner)
8. ✅ **Expected:** Banner closes, user can keep working
9. In Tab 3, click "Save & Continue"
10. ✅ **Expected:** Console shows "Saving Vendor form..."
11. ✅ **Expected:** Tab 3 logs out after save

**Pass Criteria:**
- Each tab handles logout independently
- Save functions are called
- User can choose to continue working
- No forced reloads
- No data loss

---

### **Test 6: Browser Refresh with Unsaved Work** ⏱️ 2 minutes

**Setup:**
1. Login as `admin@test.com`
2. Open DevTools console
3. Create unsaved work:
```javascript
window.unsavedWorkTracker.register({
  id: 'test_draft',
  type: 'form_builder',
  description: 'Important Form Draft',
  isDirty: true,
  autoSaveEnabled: false
})
```

**Test:**
1. Try to refresh page (F5 or Ctrl+R)
2. ✅ **Expected:** Browser shows confirmation dialog:
   "You have unsaved changes. Are you sure you want to leave?"
3. Click "Cancel"
4. ✅ **Expected:** Page doesn't reload
5. Click refresh again
6. Click "Leave"
7. ✅ **Expected:** Page reloads

**Pass Criteria:**
- beforeunload warning appears
- User can cancel refresh
- Unsaved work is protected

---

### **Test 7: Queue Persistence Across Browser Restarts** ⏱️ 3 minutes

**Setup:**
1. Open browser to public form
2. Go offline (DevTools → Network → Offline)
3. Submit 3 leads
4. Check queue:
```javascript
const stats = await window.offlineQueue.getStats()
console.log(stats) // Should show 3 pending
```

**Test:**
1. **Close browser completely** (Ctrl+W or close window)
2. **Reopen browser** to same public form
3. Check queue again:
```javascript
const stats = await window.offlineQueue.getStats()
console.log(stats) // Should STILL show 3 pending
```
4. Go online (DevTools → Network → Online)
5. Wait 3-5 seconds
6. ✅ **Expected:** All 3 leads upload automatically
7. Check queue:
```javascript
const stats = await window.offlineQueue.getStats()
console.log(stats) // Should show 0 pending, 3 success
```

**Pass Criteria:**
- Queue persists across browser restarts (IndexedDB)
- Leads upload automatically when back online
- No data loss

---

### **Test 8: Concurrent Logout in Multiple Tabs** ⏱️ 3 minutes

**Setup:**
1. Login as `admin@test.com`
2. Open 3 tabs to /dashboard
3. In Tab 1 console, create unsaved work:
```javascript
window.unsavedWorkTracker.register({
  id: 'tab1_work',
  type: 'form_builder',
  description: 'Tab 1 unsaved work',
  isDirty: true,
  autoSaveEnabled: false
})
```

**Test:**
1. In Tab 2, click "Logout" (Tab 2 has no unsaved work)
2. Tab 2 logs out immediately
3. Tab 1 shows banner (has unsaved work)
4. Tab 3 shows banner (no unsaved work, but waiting)
5. In Tab 3, click "Continue"
6. ✅ **Expected:** Tab 3 logs out
7. In Tab 1, click "X" to dismiss banner
8. ✅ **Expected:** Tab 1 continues working (still logged in locally)
9. Try to call an API endpoint in Tab 1
10. ✅ **Expected:** Gets 401 Unauthorized (tokens are cleared)
11. Shows error: "Session expired. Please log in again."

**Pass Criteria:**
- Each tab handles logout independently
- Tabs with unsaved work can continue working locally
- API calls fail gracefully when tokens are cleared
- User is guided to log in again

---

### **Test 9: Real-World Event Scenario** ⏱️ 15 minutes

**Setup:**
1. Simulate event with tablet
2. Open public form on tablet
3. Prepare test leads (10 sample submissions)

**Test:**
1. Submit 3 leads while **online**
   - ✅ All upload immediately
   - ✅ See success messages
2. **Disconnect WiFi** on tablet (turn off WiFi or enable airplane mode)
3. Submit 4 more leads while **offline**
   - ✅ All queue in IndexedDB
   - ✅ See "Saved offline" messages
   - ✅ Offline indicator appears at top
4. **Reconnect WiFi**
5. Wait 5-10 seconds
   - ✅ Queued leads upload automatically
   - ✅ See "All leads uploaded!" message
   - ✅ Offline indicator disappears
6. Check backend database
   - ✅ All 7 leads present
   - ✅ No duplicates
   - ✅ Timestamps correct

**Pass Criteria:**
- All leads captured (0% loss rate)
- Automatic retry works
- User experience is smooth
- No technical knowledge required

---

## 🔍 **Developer Console Commands**

### **Check Auth State**
```javascript
// Get current unsaved work
window.unsavedWorkTracker.getUnsavedSources()

// Get summary
window.unsavedWorkTracker.getSummary()

// Check if has unsaved work
window.unsavedWorkTracker.hasUnsavedWork()

// Get count
window.unsavedWorkTracker.getUnsavedCount()
```

### **Check Queue State**
```javascript
// Get queue stats
await window.offlineQueue.getStats()

// Get all queued items
await window.offlineQueue.getAll()

// Get pending only
await window.offlineQueue.getPending()

// Manually process queue
await window.offlineQueue.processQueue()

// Retry all failed items
await window.offlineQueue.retryFailed()

// Clear successful items
await window.offlineQueue.clearSuccessful()
```

### **Simulate Offline/Online**
```javascript
// Simulate going offline
window.dispatchEvent(new Event('offline'))

// Simulate going online
window.dispatchEvent(new Event('online'))

// Check current status
console.log(navigator.onLine)
```

### **Test BroadcastChannel**
```javascript
// In Tab 1 console
const channel = new BroadcastChannel('eventlead_auth')
channel.postMessage({ type: 'TEST', message: 'Hello from Tab 1' })

// In Tab 2 console
const channel = new BroadcastChannel('eventlead_auth')
channel.onmessage = (e) => console.log('Received:', e.data)
```

---

## ✅ **Success Criteria**

All tests must pass with these criteria:

1. **No page reloads** (except initial login)
2. **No data loss** (unsaved work protected)
3. **Tabs stay synchronized** (auth state consistent)
4. **Works offline** (leads queue properly)
5. **Automatic retry** (queued items upload when online)
6. **No console errors** (clean execution)
7. **Good UX** (helpful messages, clear feedback)
8. **Cross-browser** (Chrome, Firefox, Safari, Edge)

---

## 🐛 **Common Issues & Solutions**

### **Issue: Banner doesn't appear in other tabs**
**Cause:** BroadcastChannel not supported and storage event not firing  
**Check:**
```javascript
// Check if BroadcastChannel is available
console.log('BroadcastChannel supported:', 'BroadcastChannel' in window)

// Check storage events manually
window.addEventListener('storage', (e) => {
  console.log('Storage event:', e.key, e.newValue)
})
```

### **Issue: Queue doesn't persist**
**Cause:** IndexedDB not initialized  
**Check:**
```javascript
// Check IndexedDB
await window.offlineQueue.initialize()
const stats = await window.offlineQueue.getStats()
console.log(stats)
```

### **Issue: beforeunload warning doesn't show**
**Cause:** Unsaved work not registered  
**Check:**
```javascript
console.log('Has unsaved work:', window.unsavedWorkTracker.hasUnsavedWork())
console.log('Unsaved sources:', window.unsavedWorkTracker.getUnsavedSources())
```

---

## 📊 **Test Report Template**

```markdown
## Multi-Tab Auth Test Report

**Date:** [Date]
**Tester:** [Name]
**Browser:** [Chrome/Firefox/Safari/Edge] [Version]
**OS:** [Windows/Mac/Linux]

### Test Results

| Test | Status | Notes |
|------|--------|-------|
| Basic Multi-Tab Logout | ✅/❌ | |
| Multi-Tab Login | ✅/❌ | |
| Unsaved Work Protection | ✅/❌ | |
| Offline Lead Capture | ✅/❌ | |
| Form Builder Multi-Tab | ✅/❌ | |
| Browser Refresh Warning | ✅/❌ | |
| Queue Persistence | ✅/❌ | |
| Concurrent Logout | ✅/❌ | |
| Real-World Event Scenario | ✅/❌ | |

### Issues Found

1. [Description]
2. [Description]

### Overall Status
✅ PASS / ❌ FAIL

### Recommendations

[Any improvements or concerns]
```

---

## 🚀 **Performance Benchmarks**

| Operation | Target | Measurement |
|-----------|--------|-------------|
| Queue item (IndexedDB write) | <50ms | `console.time('enqueue')` |
| Process queue (100 items) | <5s | `console.time('processQueue')` |
| Auth sync (cross-tab) | <100ms | Time from event to banner |
| Save all unsaved work | <3s | Time from click to complete |
| Page load with queue | <2s | Time to interactive |

---

**All tests should pass before shipping Form Builder to production!** ✅


