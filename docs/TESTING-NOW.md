# Testing Multi-Tab Auth - RIGHT NOW

**If you got the "Cannot read properties of undefined" error, do this:**

---

## 🔄 **Step 1: Refresh Browser**

The utilities need to be loaded by React. **Refresh your browser** (F5 or Ctrl+R)

---

## 🧪 **Step 2: Verify Utilities Are Available**

Open browser console and type:

```javascript
// Check if utilities are available
console.log(window.unsavedWorkTracker)
console.log(window.offlineQueue)
```

**Expected:** Should see objects (not undefined)

**If still undefined:**
- Wait 2-3 seconds for React to initialize
- Or refresh browser again
- Check console for errors

---

## ✅ **Step 3: Run Quick Test**

Once utilities are available:

```javascript
// Create fake unsaved work
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

// Verify it was registered
console.log('Has unsaved work:', window.unsavedWorkTracker.hasUnsavedWork())
console.log('Unsaved count:', window.unsavedWorkTracker.getUnsavedCount())
console.log('Summary:', window.unsavedWorkTracker.getSummary())
```

**Expected output:**
```
Has unsaved work: true
Unsaved count: 1
Summary: My Test Form
```

---

## 🎯 **Step 4: Test Multi-Tab Logout**

1. **Open another tab** to http://localhost:3000/dashboard
2. **In the new tab, click "Logout"**
3. **Switch back to first tab**
4. ✅ **Expected:** You should see a **YELLOW BANNER** at the top saying:
   - "You've been logged out in another tab"
   - "1 unsaved item: My Test Form"
   - "Save & Continue" button

5. **Click "Save & Continue"**
6. ✅ **Expected:** Console shows:
   - "💾 Saving test form..."
   - "✅ Test form saved!"
7. ✅ **Expected:** Tab navigates to /login

**SUCCESS!** Multi-tab auth with unsaved work protection is working! 🎉

---

## 🔍 **If Banner Doesn't Appear**

### **Check BroadcastChannel:**
```javascript
console.log('BroadcastChannel supported:', 'BroadcastChannel' in window)
```

### **Check storage events:**
```javascript
// Add listener
window.addEventListener('storage', (e) => {
  console.log('Storage event:', e.key, e.newValue ? 'SET' : 'CLEARED')
})

// Now logout in another tab
// Should see: "Storage event: eventlead_access_token CLEARED"
```

### **Check auth context:**
```javascript
// Look for these logs in console:
// "✅ BroadcastChannel initialized" (if supported)
// "🔄 Logout detected in another tab" (when you logout)
```

---

## 📦 **Test Offline Queue**

```javascript
// Check queue is ready
await window.offlineQueue.initialize()

// Add test item
await window.offlineQueue.enqueue('lead_submission', {
  formId: 123,
  name: 'Test Lead',
  email: 'test@example.com'
})

// Check stats
await window.offlineQueue.getStats()
// Should show: { totalQueued: 1, pending: 1, ... }

// Get all items
await window.offlineQueue.getAll()
// Should show array with 1 item
```

---

## ⚡ **Alternative: Manual Test Without Console**

If console commands don't work, you can still test by:

1. **Open Form Builder Example page** (when we build it)
2. **Make changes to form** (triggers unsaved work automatically)
3. **Open another tab and logout**
4. **First tab should show banner**

For now, the console test is the quickest way to verify!

---

**After refresh, utilities should be available!** Try again. 🚀


