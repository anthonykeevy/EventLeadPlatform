# UAT Test Accounts - Story 1.9

**Story:** 1.9 - Frontend Authentication - Signup & Login  
**Number of Testers:** 3  
**Test Environment:** Local Development (http://localhost:5173)

---

## Test Account Assignments

### Tester 1 - New User Signup & Happy Paths

**Primary Focus:** Test successful signup and login flows

**Test Email:** `tester1.newuser@eventlead-uat.com`  
**Test Password:** `Tester1Pass!2025`  
**First Name:** `Sarah`  
**Last Name:** `Johnson`  
**Role:** Event Organizer (non-technical user)

**Assigned Scenarios:**
1. New User Signup (Happy Path)
3. Login with Valid Credentials (Happy Path)
6. Password Visibility Toggle
8. Forgot Password Link
9. Navigation Between Auth Pages

**Why this assignment:**
- Tests core functionality first
- Represents typical new user experience
- Validates happy paths work before error testing

---

### Tester 2 - Error Paths & Edge Cases

**Primary Focus:** Test error handling and validation

**Test Email (Primary):** `tester2.errors@eventlead-uat.com`  
**Test Email (Duplicate Test):** `tester1.newuser@eventlead-uat.com` (reuse Tester 1's email)  
**Test Email (Invalid Format):** `invalid-email-format`  
**Test Password:** `Tester2Pass!2025`  
**Wrong Password (for testing):** `WrongPassword123!`  
**First Name:** `Michael`  
**Last Name:** `Chen`  
**Role:** IT Manager (technical user)

**Assigned Scenarios:**
2. Signup with Duplicate Email (Error Path)
4. Login with Invalid Credentials (Error Path)
5. Login with Unverified Email (Error Path) - *Manual setup required*
7. Remember Me Checkbox

**Why this assignment:**
- Tests all error scenarios
- Validates error messages are clear
- Ensures system handles failures gracefully
- Technical user can verify error details

---

### Tester 3 - Mobile, Accessibility & UX

**Primary Focus:** Test mobile responsiveness, accessibility, UX polish

**Test Email:** `tester3.mobile@eventlead-uat.com`  
**Test Password:** `Tester3Pass!2025`  
**First Name:** `Lisa`  
**Last Name:** `Martinez`  
**Role:** Marketing Professional (non-technical, mobile user)

**Assigned Scenarios:**
10. Redirect Authenticated Users
11. Mobile Responsiveness (Primary)
12. Accessibility Testing (Keyboard & Screen Reader)
Plus: Quick smoke test of Scenario 1 (Signup) on mobile

**Why this assignment:**
- Tests mobile experience thoroughly
- Validates accessibility compliance
- Provides non-technical user perspective on UX
- Tests edge cases (redirect logic)

---

## Pre-Test Setup Instructions

### Database Preparation

**Option A: Clean Database (Recommended for first UAT run)**
```sql
-- Run this in SSMS BEFORE starting UAT
USE EventLeadDB;
GO

-- Clear test data from previous runs (if any)
DELETE FROM dbo.UserRefreshToken WHERE UserID IN (
    SELECT UserID FROM dbo.[User] WHERE Email LIKE '%@eventlead-uat.com'
);
DELETE FROM dbo.UserEmailVerificationToken WHERE UserID IN (
    SELECT UserID FROM dbo.[User] WHERE Email LIKE '%@eventlead-uat.com'
);
DELETE FROM dbo.[User] WHERE Email LIKE '%@eventlead-uat.com';
GO

-- Verify cleanup
SELECT COUNT(*) AS TestUsersRemaining 
FROM dbo.[User] 
WHERE Email LIKE '%@eventlead-uat.com';
-- Should return 0
```

**Option B: Pre-create Tester 1 Account (For Tester 2 duplicate email test)**

If you want Tester 2 to immediately test duplicate email error:
```sql
-- This will be created by Tester 1 during their test
-- Only run this if skipping Tester 1's signup scenario
-- (Not recommended - better to let Tester 1 create it naturally)
```

---

### Environment Checklist

Each tester should verify BEFORE starting:

**Backend API:**
```powershell
# Check API is running
curl http://localhost:8000/api/health
# Expected: {"status":"healthy"}
```

**Frontend:**
```powershell
# Check frontend is running
# Open browser: http://localhost:5173
# Expected: EventLead home page loads
```

**MailHog:**
```powershell
# Check email service
# Open browser: http://localhost:8025
# Expected: MailHog inbox interface
```

**Database:**
```sql
-- Test database connection in SSMS
USE EventLeadDB;
SELECT @@VERSION;
-- Should return SQL Server version info
```

---

## Test Execution Order

**Important:** Testers should run in this order to avoid conflicts:

### Phase 1: Tester 1 (15-20 minutes)
- Tester 1 completes their scenarios FIRST
- This creates the user account needed for Tester 2's duplicate email test
- Tester 1 should NOT delete their account

### Phase 2: Tester 2 & Tester 3 (Parallel - 20-25 minutes each)
- After Tester 1 completes, Tester 2 and Tester 3 can run in parallel
- Tester 2 will use Tester 1's email for duplicate test
- Tester 3 will test mobile and accessibility independently

---

## Tester 1 - Detailed Test Data

### Scenario 1: New User Signup

**Form Data to Enter:**
```
First Name: Sarah
Last Name: Johnson
Email: tester1.newuser@eventlead-uat.com
Password: Tester1Pass!2025
```

**Password Requirements Validation:**
- ✅ At least 8 characters (14 characters)
- ✅ Contains uppercase letter (T, P)
- ✅ Contains lowercase letter (ester, ass)
- ✅ Contains number (1, 2025)
- ✅ Contains special character (!)

**Expected Database Record:**
```sql
-- Run after signup to verify
SELECT UserID, Email, FirstName, LastName, EmailVerified, IsActive, CreatedDate
FROM dbo.[User]
WHERE Email = 'tester1.newuser@eventlead-uat.com';
```

**Expected Results:**
- EmailVerified = 0 (not verified yet)
- IsActive = 1 (active)
- FirstName = 'Sarah'
- LastName = 'Johnson'

---

### Scenario 3: Login with Valid Credentials

**Prerequisites:**
- Must complete Scenario 1 first
- Must manually verify email in database (for MVP):
  ```sql
  -- Run this to allow login (simulates clicking verification email)
  UPDATE dbo.[User] 
  SET EmailVerified = 1 
  WHERE Email = 'tester1.newuser@eventlead-uat.com';
  ```

**Login Credentials:**
```
Email: tester1.newuser@eventlead-uat.com
Password: Tester1Pass!2025
```

**Expected Database Changes:**
```sql
-- Verify refresh token created
SELECT RefreshTokenID, UserID, ExpiresAt, RevokedAt, CreatedDate
FROM dbo.UserRefreshToken
WHERE UserID = (SELECT UserID FROM dbo.[User] WHERE Email = 'tester1.newuser@eventlead-uat.com')
ORDER BY CreatedDate DESC;
```

---

## Tester 2 - Detailed Test Data

### Scenario 2: Signup with Duplicate Email

**Prerequisites:**
- Tester 1 MUST complete Scenario 1 first
- Verify Tester 1's account exists in database

**Form Data to Enter:**
```
First Name: Michael
Last Name: Chen
Email: tester1.newuser@eventlead-uat.com  ← SAME as Tester 1 (intentional)
Password: Tester2Pass!2025
```

**Expected Error:**
```
"This email is already registered. Try logging in."
```

**Database Verification:**
```sql
-- Verify NO new user created
SELECT COUNT(*) AS UserCount
FROM dbo.[User]
WHERE Email = 'tester1.newuser@eventlead-uat.com';
-- Should return 1 (only Tester 1's account)
```

---

### Scenario 4: Login with Invalid Credentials

**First, create Tester 2's own account:**
```
First Name: Michael
Last Name: Chen
Email: tester2.errors@eventlead-uat.com
Password: Tester2Pass!2025
```

**Then manually verify:**
```sql
UPDATE dbo.[User] 
SET EmailVerified = 1 
WHERE Email = 'tester2.errors@eventlead-uat.com';
```

**Then test with WRONG password:**
```
Email: tester2.errors@eventlead-uat.com
Password: WrongPassword123!  ← Intentionally wrong
```

**Expected Error:**
```
"Email or password is incorrect."
```

---

### Scenario 5: Login with Unverified Email

**Manual Setup Required:**

1. Create a new test user in database (unverified):
```sql
-- Run this in SSMS to create unverified test account
INSERT INTO dbo.[User] (
    Email, PasswordHash, FirstName, LastName, 
    EmailVerified, IsActive, OnboardingComplete, 
    CreatedDate, UpdatedDate
)
VALUES (
    'unverified@eventlead-uat.com',
    '$2b$12$LhVgXJ5gX5xK9qZ5yZ5yZ5yZ5yZ5yZ5yZ5yZ5yZ5yZ5yZ5yZ5yZ5', -- Hash of "Unverified1!"
    'Unverified',
    'User',
    0,  -- EmailVerified = FALSE
    1,  -- IsActive = TRUE
    0,  -- OnboardingComplete = FALSE
    GETDATE(),
    GETDATE()
);
GO
```

**Login Attempt:**
```
Email: unverified@eventlead-uat.com
Password: Unverified1!
```

**Expected Error:**
```
"Please verify your email before logging in."
```

**Note:** This test requires backend to check EmailVerified flag. If error doesn't appear, verify backend validation exists.

---

## Tester 3 - Detailed Test Data

### Scenario 11: Mobile Responsiveness

**Test Email:** `tester3.mobile@eventlead-uat.com`  
**Test Password:** `Tester3Pass!2025`  
**First Name:** `Lisa`  
**Last Name:** `Martinez`

**Mobile Devices to Test:**

**Option 1: Real Mobile Device (Preferred)**
- Access http://[your-computer-ip]:5173
- Example: http://192.168.1.100:5173
- Make sure phone is on same WiFi network

**Option 2: Browser DevTools Mobile Emulation**
1. Open Chrome DevTools (F12)
2. Click "Toggle Device Toolbar" (Ctrl+Shift+M)
3. Select device:
   - iPhone 12 Pro (390 x 844)
   - Samsung Galaxy S20 (360 x 800)

**What to Test:**
- Tap targets easy to touch (44px minimum)
- Virtual keyboard doesn't cover form fields
- Text readable without zooming
- Password strength indicator displays correctly
- All buttons work with tap (not just click)

---

### Scenario 12: Accessibility Testing

**Prerequisites:**
- Download NVDA screen reader (free): https://www.nvaccess.org/download/
- Or use built-in Windows Narrator (Win + Ctrl + Enter)

**Keyboard Navigation Test:**

Use ONLY keyboard (no mouse):
- Tab: Move to next field
- Shift+Tab: Move to previous field
- Enter: Submit form
- Space: Toggle checkboxes

**Expected Behavior:**
- Tab order is logical (First Name → Last Name → Email → Password → Submit)
- Focus indicator visible (blue outline or similar)
- Enter key submits form when on submit button

**Screen Reader Test:**

Turn on NVDA and navigate signup form:
- Each field should announce its label
- Required fields should announce "required"
- Error messages should be announced immediately
- Success messages should be announced

---

## Quick Reference: SQL Verification Queries

Copy these into SSMS for quick database checks during testing:

```sql
-- CHECK 1: View all test users
SELECT UserID, Email, FirstName, LastName, EmailVerified, IsActive, CreatedDate
FROM dbo.[User]
WHERE Email LIKE '%@eventlead-uat.com'
ORDER BY CreatedDate DESC;

-- CHECK 2: Verify password is hashed (security check)
SELECT Email, LEFT(PasswordHash, 10) + '...' AS HashPreview, LEN(PasswordHash) AS HashLength
FROM dbo.[User]
WHERE Email LIKE '%@eventlead-uat.com';
-- HashLength should be 60+ characters

-- CHECK 3: View verification tokens
SELECT u.Email, t.Token, t.ExpiresAt, t.UsedAt, t.CreatedDate
FROM dbo.UserEmailVerificationToken t
JOIN dbo.[User] u ON t.UserID = u.UserID
WHERE u.Email LIKE '%@eventlead-uat.com'
ORDER BY t.CreatedDate DESC;

-- CHECK 4: View refresh tokens (after login)
SELECT u.Email, t.Token, t.ExpiresAt, t.RevokedAt, t.CreatedDate
FROM dbo.UserRefreshToken t
JOIN dbo.[User] u ON t.UserID = u.UserID
WHERE u.Email LIKE '%@eventlead-uat.com'
ORDER BY t.CreatedDate DESC;

-- CHECK 5: View recent API requests
SELECT TOP 20 
    RequestID, Method, Path, StatusCode, DurationMs, 
    UserID, CreatedDate
FROM log.ApiRequest
WHERE Path LIKE '%/api/auth/%'
ORDER BY CreatedDate DESC;

-- CHECK 6: Check for errors
SELECT TOP 10 
    ErrorID, ErrorType, ErrorMessage, Severity, Path, CreatedDate
FROM log.ApplicationError
WHERE CreatedDate > DATEADD(MINUTE, -30, GETDATE())
ORDER BY CreatedDate DESC;

-- CLEANUP: Remove all test data after UAT (run at end)
DELETE FROM dbo.UserRefreshToken WHERE UserID IN (
    SELECT UserID FROM dbo.[User] WHERE Email LIKE '%@eventlead-uat.com'
);
DELETE FROM dbo.UserEmailVerificationToken WHERE UserID IN (
    SELECT UserID FROM dbo.[User] WHERE Email LIKE '%@eventlead-uat.com'
);
DELETE FROM dbo.[User] WHERE Email LIKE '%@eventlead-uat.com';
```

---

## Summary Table

| Tester | Email | Password | Focus Area | Scenarios | Time |
|--------|-------|----------|------------|-----------|------|
| Tester 1 | tester1.newuser@eventlead-uat.com | Tester1Pass!2025 | Happy Paths | 1,3,6,8,9 | 15-20min |
| Tester 2 | tester2.errors@eventlead-uat.com | Tester2Pass!2025 | Error Paths | 2,4,5,7 | 20-25min |
| Tester 3 | tester3.mobile@eventlead-uat.com | Tester3Pass!2025 | Mobile/A11y | 10,11,12 | 20-25min |

**Total UAT Time:** ~60 minutes with all 3 testers

---

**End of Test Accounts Document**

