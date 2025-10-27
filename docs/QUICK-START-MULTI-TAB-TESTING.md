# Quick Start: Testing Multi-Tab Auth & Offline Features

**For:** Story 1.16 Enhanced (Option B)  
**Time:** 10 minutes  
**Goal:** Verify multi-tab auth and offline queue work correctly

---

## 🚀 **Quick Test (10 Minutes)**

### **Step 1: Start Services**

```bash
# Terminal 1 - Backend
cd backend
.\venv\Scripts\activate
uvicorn main:app --reload

# Terminal 2 - Frontend  
cd frontend
npm run dev
```

---

### **Step 2: Test Multi-Tab Auth** ⏱️ 3 minutes

1. **Open browser** to http://localhost:3000
2. **Login** as `admin@test.com` (password: `Test123!@#`)
3. **Open 2 more tabs** to http://localhost:3000/dashboard
4. All 3 tabs should show dashboard ✅

5. **Open DevTools console in Tab 1**
6. **Create fake unsaved work:**
```javascript
window.unsavedWorkTracker.register({
  id: 'test_form',
  type: 'form_builder',
  description: 'My Test Form',
  isDirty: true,
  onSave: async () => {
    console.log('💾 Saving test form...')
    await new Promise(resolve => setTimeout(resolve, 1000))
    console.log('✅ Test form saved!')
  }
})
```

7. **In Tab 2, click "Logout"**
8. ✅ **Expected:** Tab 2 logs out immediately
9. ✅ **Expected:** Tab 1 shows **BANNER**: "You've been logged out in another tab"
10. ✅ **Expected:** Banner shows: "1 unsaved item"
11. ✅ **Expected:** Tab 3 shows banner (no unsaved work)

12. **In Tab 1, click "Save & Continue"** on banner
13. ✅ **Expected:** Console shows "💾 Saving test form..."
14. ✅ **Expected:** Console shows "✅ Test form saved!"
15. ✅ **Expected:** Tab 1 navigates to /login

**PASS:** No page reloads, banner appeared, save function called! ✅

---

### **Step 3: Test Offline Queue** ⏱️ 5 minutes

1. **Open browser console**
2. **Check queue is initialized:**
```javascript
// Should see object with methods
console.log(window.offlineQueue)

// Get initial stats
await window.offlineQueue.getStats()
// Should show: { totalQueued: 0, pending: 0, ... }
```

3. **Add test items to queue:**
```javascript
// Simulate 3 offline lead submissions
await window.offlineQueue.enqueue('lead_submission', {
  formId: 123,
  name: 'John Doe',
  email: 'john@test.com'
})

await window.offlineQueue.enqueue('lead_submission', {
  formId: 123,
  name: 'Jane Smith',
  email: 'jane@test.com'
})

await window.offlineQueue.enqueue('lead_submission', {
  formId: 123,
  name: 'Bob Johnson',
  email: 'bob@test.com'
})
```

4. **Check queue stats:**
```javascript
await window.offlineQueue.getStats()
// Should show: { totalQueued: 3, pending: 3, ... }
```

5. **Get all queued items:**
```javascript
await window.offlineQueue.getAll()
// Should show array with 3 items
```

6. **Close browser completely**
7. **Reopen browser** (http://localhost:3000)
8. **Open console again:**
```javascript
await window.offlineQueue.getStats()
// ✅ Should STILL show 3 items! (IndexedDB persists)
```

**PASS:** Queue persists across browser restarts! ✅

---

### **Step 4: Test Network Events** ⏱️ 2 minutes

1. **In browser console:**
```javascript
// Listen for network changes
window.addEventListener('online', () => console.log('🌐 ONLINE'))
window.addEventListener('offline', () => console.log('📡 OFFLINE'))

// Check current status
console.log('Currently:', navigator.onLine ? 'ONLINE' : 'OFFLINE')
```

2. **Open DevTools → Network tab**
3. **Select "Offline" mode**
4. ✅ **Expected:** Console shows "📡 OFFLINE"

5. **Select "Online" mode**
6. ✅ **Expected:** Console shows "🌐 ONLINE"

**PASS:** Network detection working! ✅

---

## ✅ **Success Checklist**

After running all tests, verify:

- [ ] ✅ Multi-tab auth works (no forced reloads)
- [ ] ✅ Banner appears when auth changes in other tabs
- [ ] ✅ Unsaved work is protected
- [ ] ✅ Save function is called before auth sync
- [ ] ✅ Offline queue initialized (window.offlineQueue exists)
- [ ] ✅ Queue persists across browser restarts
- [ ] ✅ Network events fire correctly
- [ ] ✅ No console errors

---

## 🐛 **If Something Doesn't Work**

### **Issue: window.unsavedWorkTracker is undefined**
```bash
# Check if utilities are exported
# Look in frontend/src/utils/index.ts

# Manually import in console:
import { unsavedWorkTracker } from './src/utils/unsavedWorkTracker'
window.unsavedWorkTracker = unsavedWorkTracker
```

### **Issue: window.offlineQueue is undefined**
```bash
# Manually import in console:
import { offlineQueue } from './src/utils/offlineQueue'
window.offlineQueue = offlineQueue

# Then initialize
await offlineQueue.initialize()
```

### **Issue: Banner doesn't appear**
```bash
# Check browser support
console.log('BroadcastChannel:', 'BroadcastChannel' in window)
console.log('Storage events:', 'onstorage' in window)

# Check if auth context is mounted
# Should see console logs when logging out
```

---

## 📊 **Expected Results Summary**

| Test | Expected Result | Status |
|------|----------------|--------|
| Multi-tab logout | Banner appears, no reload | ⬜ |
| Unsaved work protection | Save function called | ⬜ |
| Offline queue | Items persist | ⬜ |
| Network detection | Events fire correctly | ⬜ |
| BroadcastChannel | Works in modern browsers | ⬜ |
| localStorage fallback | Works in all browsers | ⬜ |

---

## 🚀 **Next: Test Real Invitation Flow**

After confirming the infrastructure works:

1. **Close all tabs**
2. **Open fresh browser**
3. **Login as admin@test.com**
4. **Click user icon (👥)** in SUTTONS & CO
5. **Click "Invitations" tab**
6. **Check if usertest@test.com invitation is there**
7. **Try resending the invitation**
8. **Check MailHog** (localhost:8025)
9. **Click invitation link**
10. **Should see beautiful acceptance page** ✅

---

**Total Test Time: 10 minutes**  
**If all tests pass: Story 1.16 is production-ready!** 🎉


