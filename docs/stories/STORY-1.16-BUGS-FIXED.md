# Story 1.16: Bugs Fixed During Testing

**Date:** 2025-10-25  
**Testing Session:** UAT by Anthony Keevy

---

## 🐛 **Bug #1: camelCase/snake_case Mismatch** 

**Severity:** Critical (422 Error - Unprocessable Entity)  
**Found:** During first invitation attempt  
**Status:** ✅ Fixed

### **Problem:**
Frontend was sending camelCase field names (`firstName`, `lastName`) but backend expects snake_case (`first_name`, `last_name`). This caused a 422 validation error and blank screen.

### **Error Message:**
```
Failed to load resource: the server responded with a status of 422 (Unprocessable Content)
```

### **Root Cause:**
Missing data transformation at the API boundary. Pattern was applied in Story 1.19 but not consistently applied to Story 1.16.

### **Fix Applied:**
**File:** `frontend/src/features/dashboard/api/teamApi.ts`

Added transformation in `inviteUser()` function:
```typescript
// Transform camelCase to snake_case for backend
const backendData = {
  email: data.email,
  first_name: data.firstName,
  last_name: data.lastName,
  role: data.role
}
```

Added transformation in `editUserRole()` function:
```typescript
// Transform camelCase to snake_case for backend
const backendData = {
  role_code: data.roleCode
}
```

---

## 🐛 **Bug #2: React Rendering Error (Objects as React Children)**

**Severity:** Critical (Blank Page)  
**Found:** During first invitation attempt  
**Status:** ✅ Fixed

### **Problem:**
Pydantic validation errors from backend return as arrays/objects, not strings. This caused "Objects are not valid as React child" error when trying to display the error message.

### **Error Message:**
```
Uncaught Error: Objects are not valid as a React child (found: object with keys {type, loc, msg, input})
```

### **Root Cause:**
Error handling only expected string error messages but Pydantic returns structured validation errors.

### **Fix Applied:**
**Files:** 
- `frontend/src/features/dashboard/components/InviteUserModal.tsx`
- `frontend/src/features/dashboard/components/EditRoleModal.tsx`

Added proper error type checking:
```typescript
if (error.response?.data?.detail) {
  const detail = error.response.data.detail
  if (typeof detail === 'string') {
    setSubmitError(detail)
  } else if (Array.isArray(detail)) {
    // Pydantic validation errors are arrays
    const errorMessages = detail.map((err: any) => err.msg).join(', ')
    setSubmitError(`Validation error: ${errorMessages}`)
  } else if (typeof detail === 'object') {
    setSubmitError(JSON.stringify(detail))
  } else {
    setSubmitError('Validation error occurred')
  }
}
```

Also added 422 status code handling for better UX.

---

## 🐛 **Bug #3: Missing Invitation Acceptance Page**

**Severity:** Critical (Broken Feature)  
**Found:** When clicking invitation link in email  
**Status:** ✅ Fixed

### **Problem:**
No frontend route for `/invitations/accept`. Clicking invitation link resulted in blank page with error: "No routes matched location /invitations/accept?token=..."

### **Root Cause:**
Story 1.7 backend was implemented but frontend acceptance page was never created.

### **Fix Applied:**

**Created Files:**
1. `frontend/src/features/invitations/pages/InvitationAcceptancePage.tsx` (~250 lines)
   - Public page to view invitation details
   - Accept invitation button (if logged in)
   - Log in / Sign up buttons (if not logged in)
   - Beautiful UI with invitation details display

2. `frontend/src/features/invitations/api/invitationApi.ts`
   - `viewInvitation()` - View invitation details
   - `acceptInvitation()` - Accept invitation

3. `frontend/src/features/invitations/types/invitation.types.ts`
   - `InvitationDetails` type
   - `AcceptInvitationResponse` type

4. `frontend/src/features/invitations/index.ts`
   - Export all invitation components

**Modified Files:**
- `frontend/src/App.tsx` - Added route: `/invitations/accept`

### **Features Implemented:**
- ✅ View invitation details (company, role, inviter, expiry)
- ✅ Accept invitation if logged in
- ✅ Redirect to login/signup if not logged in
- ✅ Show expired status if invitation expired
- ✅ Show success message and redirect to dashboard
- ✅ Update JWT tokens after acceptance
- ✅ Mobile responsive design

---

## 📋 **Additional Notes**

### **Pending Invitations Display**
Pending invitations appear in the **"Invitations" tab** of the team management panel, not in the main "Members" tab. This is by design:
- Click the user icon (👥) in company header
- Click the **"Invitations"** tab
- Pending invitations will appear there

### **Future Enhancement Ideas**
1. Add badge count to "Invitations" tab showing number of pending invitations
2. Show recent invitations in the Members tab as "Pending" status
3. Add toast notifications instead of browser alerts
4. Add ability to view invitation history (accepted, expired, cancelled)

---

## ✅ **Testing Checklist After Fixes**

- [x] Bug #1 Fixed: camelCase/snake_case transformation working
- [x] Bug #2 Fixed: Error handling improved
- [x] Bug #3 Fixed: Invitation acceptance page working
- [ ] **Ready for Re-Test:** All bugs fixed, ready for full UAT

---

## 🧪 **Re-Test Instructions**

1. **Refresh browser** (Ctrl+R or F5)
2. **Test Invitation Flow:**
   ```
   a. Login as Company Admin
   b. Click user icon (👥) in company header
   c. Click "Invite User" button
   d. Fill form and submit ✅ Should work now!
   e. Click "Invitations" tab ✅ Should see pending invitation
   f. Go to MailHog (localhost:8025) ✅ Should see email
   g. Click invitation link ✅ Should see beautiful acceptance page
   h. Click "Accept Invitation" (if logged in) ✅ Should redirect to dashboard
   ```

3. **Test Role Editing:**
   ```
   a. In Members tab, click "Edit" on user
   b. Change role and submit ✅ Should work!
   ```

---

**All Critical Bugs Fixed!** 🎉


