# UAT Guide: Story 1.9 - Frontend Authentication (Signup & Login)

**Story:** 1.9 - Frontend Authentication - Signup & Login Pages  
**UAT Date:** TBD  
**UAT Lead:** Anthony Keevy  
**Environment:** Staging/Local Development  
**Estimated Duration:** 45-60 minutes per tester  

---

## Table of Contents

1. [UAT Overview & Objectives](#uat-overview--objectives)
2. [Pre-Test Setup](#pre-test-setup)
3. [UAT Test Scenarios](#uat-test-scenarios)
4. [Database Verification Guide](#database-verification-guide)
5. [UAT Best Practices for Your Team](#uat-best-practices-for-your-team)
6. [Results Template](#results-template)

---

## UAT Overview & Objectives

### What is UAT?

**User Acceptance Testing (UAT)** is the final testing phase before releasing a feature to production. Unlike technical testing (unit tests, integration tests), UAT focuses on:

- **Real user workflows** - Does it work the way users expect?
- **Business requirements** - Does it meet all acceptance criteria?
- **User experience** - Is it intuitive and pleasant to use?
- **Edge cases** - What happens when users do unexpected things?

### Why This Story Matters

Story 1.9 implements the **first interaction** users have with the EventLead Platform. If signup/login is confusing or broken, users will never reach the rest of your application. This makes UAT critical.

### Success Criteria

This UAT passes if:
- ✅ All 10 acceptance criteria are validated
- ✅ 90%+ of testers complete signup without assistance
- ✅ Average time to complete signup < 2 minutes
- ✅ All error messages are clear and actionable
- ✅ Mobile experience rated ≥4/5 by mobile testers
- ✅ Database changes match expected behavior

---

## Pre-Test Setup

### Environment Requirements

**Backend Services:**
```powershell
# Start backend API
cd backend
python main.py
# Expected: Server running at http://localhost:8000

# Verify health endpoint
# Open browser: http://localhost:8000/api/health
# Expected: {"status": "healthy", "service": "EventLead API", "environment": "development"}
```

**Frontend Application:**
```powershell
# Start frontend dev server
cd frontend
npm run dev
# Expected: Server running at http://localhost:5173
```

**MailHog Email Testing:**
```powershell
# Access MailHog UI
# Open browser: http://localhost:8025
# Expected: MailHog inbox interface (for viewing verification emails)
```

**Database Access:**
```powershell
# SQL Server Management Studio (SSMS)
# Server: localhost
# Database: EventLeadDB
# Authentication: Windows Authentication (or SQL Server auth)
```

### Pre-Test Checklist

Before starting UAT, verify:

- [ ] Backend API is running and health check passes
- [ ] Frontend dev server is running
- [ ] MailHog is accessible
- [ ] Database connection works
- [ ] Browser cache is cleared (Ctrl+Shift+Delete)
- [ ] Browser console is open (F12) to catch any JavaScript errors
- [ ] Test data is prepared (see below)

### Test Data Preparation

Create a test data sheet for each tester:

| Tester Name | Test Email | Test Password | Notes |
|-------------|-----------|---------------|-------|
| Tester 1 | john.doe@testmail.com | Test1234! | New user |
| Tester 2 | jane.smith@testmail.com | SecurePass1! | New user |
| Tester 3 | existing@testmail.com | Password123! | Will test "email exists" error |

**Password Requirements:**
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 number
- At least 1 special character

---

## UAT Test Scenarios

### Scenario 1: New User Signup (Happy Path)

**Objective:** Verify a new user can successfully create an account.

**Acceptance Criteria Tested:** AC-1.9.1, AC-1.9.4, AC-1.9.5, AC-1.9.6, AC-1.9.8, AC-1.9.9

**Steps:**

1. **Navigate to Application**
   ```
   Action: Open browser and go to http://localhost:5173
   Expected: Home page loads with "Sign Up" button visible
   ```

2. **Access Signup Page**
   ```
   Action: Click "Sign Up" button
   Expected: 
   - Browser navigates to /signup
   - Signup form displays with 4 fields:
     * First Name
     * Last Name
     * Email Address
     * Password
   - "Sign Up" button is DISABLED (form is empty)
   - Link to "Log In" is visible at bottom
   ```

3. **Test Form Validation - First Name**
   ```
   Action: Click in "First Name" field, type "J", then click outside field
   Expected: 
   - Error message appears: "First name must be at least 2 characters"
   - Error message is RED and appears below the field
   - Submit button remains DISABLED
   
   Action: Clear field and type "John"
   Expected:
   - Error message disappears
   - Field border turns GREEN (validation success)
   ```

4. **Test Form Validation - Email**
   ```
   Action: Type "invalid-email" in Email field
   Expected:
   - Error message: "Please enter a valid email address"
   - Submit button remains DISABLED
   
   Action: Clear and type "john.doe@testmail.com"
   Expected:
   - Error message disappears
   - Field border turns GREEN
   ```

5. **Test Password Strength Indicator**
   ```
   Action: Type "weak" in Password field
   Expected:
   - Password strength bar appears
   - Bar is RED and shows "Weak"
   - Requirements checklist shows:
     ❌ At least 8 characters
     ❌ Contains uppercase letter
     ✅ Contains lowercase letter
     ❌ Contains number
     ❌ Contains special character
   
   Action: Clear and type "Test1234!"
   Expected:
   - Bar turns GREEN and shows "Very Strong"
   - All 5 requirements show green checkmarks ✅
   - Submit button becomes ENABLED
   ```

6. **Test Password Visibility Toggle**
   ```
   Action: Click eye icon next to password field
   Expected:
   - Password changes from dots (••••) to visible text
   - Icon changes to "eye with slash"
   
   Action: Click icon again
   Expected:
   - Password returns to hidden (dots)
   ```

7. **Complete Signup Form**
   ```
   Action: Fill all fields with valid data:
   - First Name: John
   - Last Name: Doe
   - Email: john.doe@testmail.com
   - Password: Test1234!
   
   Expected:
   - All fields show green borders
   - Submit button is ENABLED and teal colored
   ```

8. **Submit Signup Form**
   ```
   Action: Click "Sign Up" button
   Expected:
   - Button changes to show spinner and "Creating Account..."
   - Button becomes DISABLED during submission
   - Form fields are DISABLED during submission
   ```

9. **Verify Success Message**
   ```
   Expected (after 1-2 seconds):
   - Form disappears
   - Success screen appears with:
     * Green checkmark icon ✅
     * Heading: "Account Created Successfully!"
     * Message: "We've sent a verification email to john.doe@testmail.com"
     * Instructions: "Please click the link in the email to verify your account"
     * "Go to Login →" link
   ```

10. **Verify Email Sent**
    ```
    Action: Open MailHog (http://localhost:8025)
    Expected:
    - New email visible in inbox
    - Subject: "Verify Your EventLead Account" (or similar)
    - To: john.doe@testmail.com
    - Body contains verification link
    ```

11. **Check Database Changes**
    ```
    See "Database Verification - New User Signup" section below
    ```

**Success Criteria:**
- [ ] Form validation works in real-time
- [ ] Password strength indicator updates correctly
- [ ] Submit button states change appropriately
- [ ] Success message displays correctly
- [ ] Verification email sent to MailHog
- [ ] User record created in database

**Time to Complete:** Should be < 2 minutes

---

### Scenario 2: Signup with Duplicate Email (Error Path)

**Objective:** Verify error handling when user tries to sign up with existing email.

**Acceptance Criteria Tested:** AC-1.9.5 (Error Handling)

**Prerequisite:** Run Scenario 1 first, or ensure john.doe@testmail.com already exists in database.

**Steps:**

1. **Navigate to Signup Page**
   ```
   Action: Go to http://localhost:5173/signup
   ```

2. **Fill Form with Existing Email**
   ```
   Action: Fill form with:
   - First Name: Jane
   - Last Name: Smith
   - Email: john.doe@testmail.com (SAME as Scenario 1)
   - Password: Test1234!
   
   Action: Click "Sign Up"
   ```

3. **Verify Error Message**
   ```
   Expected:
   - Red error box appears at top of form
   - Message: "This email is already registered. Try logging in."
   - Form remains visible (not replaced with success screen)
   - All fields remain enabled
   - User can correct email and try again
   ```

4. **Verify Error is User-Friendly**
   ```
   Check that error message:
   - Does NOT show technical details (no stack traces, error codes)
   - Tells user WHAT went wrong ("email already registered")
   - Tells user HOW to fix it ("try logging in")
   - Is clearly visible (red background, alert icon)
   ```

**Success Criteria:**
- [ ] Backend rejects duplicate email
- [ ] Frontend displays user-friendly error
- [ ] User can retry with different email
- [ ] No database record created

---

### Scenario 3: Login with Valid Credentials (Happy Path)

**Objective:** Verify existing user can log in successfully.

**Acceptance Criteria Tested:** AC-1.9.2, AC-1.9.3, AC-1.9.7

**Prerequisite:** User must exist and have verified email (use user from Scenario 1, manually set EmailVerified=1 in database if needed).

**Steps:**

1. **Navigate to Login Page**
   ```
   Action: Go to http://localhost:5173/login
   Expected: Login form displays with:
   - Email field
   - Password field
   - "Remember me" checkbox
   - "Forgot password?" link
   - "Log In" button (DISABLED initially)
   - "Don't have an account? Sign Up" link
   ```

2. **Test Email Validation**
   ```
   Action: Type "invalid" in email field
   Expected: Error message "Please enter a valid email address"
   
   Action: Type valid email "john.doe@testmail.com"
   Expected: Error disappears
   ```

3. **Enter Valid Credentials**
   ```
   Action: Fill form:
   - Email: john.doe@testmail.com
   - Password: Test1234!
   
   Expected:
   - Submit button becomes ENABLED
   ```

4. **Submit Login Form**
   ```
   Action: Click "Log In" button
   Expected:
   - Button shows spinner and "Logging In..."
   - Form disabled during submission
   ```

5. **Verify Successful Login**
   ```
   Expected (after 1-2 seconds):
   - User redirected to /dashboard (or /onboarding if onboarding incomplete)
   - JWT tokens stored in browser (check localStorage in DevTools)
   - User remains logged in after page refresh
   ```

6. **Verify Token Storage**
   ```
   Action: Open browser DevTools (F12) → Application tab → Local Storage
   Expected to see:
   - eventlead_access_token: [long JWT string]
   - eventlead_refresh_token: [long JWT string]
   - eventlead_token_expiry: [Unix timestamp]
   ```

7. **Test Session Persistence**
   ```
   Action: Refresh page (F5)
   Expected:
   - User remains logged in
   - No redirect to /login
   - User data still available
   ```

8. **Check Database Changes**
   ```
   See "Database Verification - User Login" section below
   ```

**Success Criteria:**
- [ ] Valid credentials accepted
- [ ] JWT tokens stored correctly
- [ ] User redirected appropriately
- [ ] Session persists after refresh
- [ ] Database logs login activity

**Time to Complete:** Should be < 30 seconds

---

### Scenario 4: Login with Invalid Credentials (Error Path)

**Objective:** Verify proper error handling for wrong password.

**Acceptance Criteria Tested:** AC-1.9.5 (Error Handling)

**Steps:**

1. **Navigate to Login Page**
   ```
   Action: Go to http://localhost:5173/login
   ```

2. **Enter Wrong Password**
   ```
   Action: Fill form:
   - Email: john.doe@testmail.com
   - Password: WrongPassword123!
   
   Action: Click "Log In"
   ```

3. **Verify Error Message**
   ```
   Expected:
   - Red error box appears
   - Message: "Email or password is incorrect."
   - NO indication of which field is wrong (security best practice)
   - Form remains enabled for retry
   - NO redirect
   ```

4. **Test Multiple Failed Attempts**
   ```
   Action: Try 2 more times with wrong password
   Expected:
   - Same error message each time
   - No account lockout (for MVP)
   - No indication of how many attempts remaining
   ```

**Success Criteria:**
- [ ] Invalid credentials rejected
- [ ] Error message is secure (doesn't reveal if email exists)
- [ ] User can retry immediately
- [ ] No database changes

---

### Scenario 5: Login with Unverified Email (Error Path)

**Objective:** Verify users must verify email before logging in.

**Acceptance Criteria Tested:** AC-1.9.5 (Error Handling)

**Prerequisite:** Create user in database with EmailVerified=0.

**Steps:**

1. **Attempt Login with Unverified Account**
   ```
   Action: Try to log in with unverified user
   Expected:
   - Red error box appears
   - Message: "Please verify your email before logging in."
   - Link to "Resend verification email" (if implemented)
   ```

2. **Verify No Token Issued**
   ```
   Action: Check localStorage in DevTools
   Expected: No tokens stored
   ```

**Success Criteria:**
- [ ] Backend blocks unverified users
- [ ] Error message is clear
- [ ] No tokens issued

---

### Scenario 6: Password Visibility Toggle

**Objective:** Test password show/hide functionality.

**Acceptance Criteria Tested:** AC-1.9.8 (Security - Password visibility toggle)

**Steps:**

1. **On Signup Page**
   ```
   Action: Type password "Test1234!" in password field
   Expected: Password shows as dots: ••••••••••
   
   Action: Click eye icon
   Expected: 
   - Password reveals as text: Test1234!
   - Icon changes to eye-with-slash
   
   Action: Click icon again
   Expected: Password hides again as dots
   ```

2. **On Login Page**
   ```
   Repeat same test on login page
   Expected: Same toggle behavior
   ```

**Success Criteria:**
- [ ] Toggle works on both forms
- [ ] Icons change appropriately
- [ ] Password is hidden by default

---

### Scenario 7: Remember Me Checkbox

**Objective:** Test "Remember me" functionality (if implemented).

**Acceptance Criteria Tested:** AC-1.9.2 (Remember me checkbox)

**Steps:**

1. **Login with Remember Me Unchecked**
   ```
   Action: Log in WITHOUT checking "Remember me"
   Expected: 
   - Token stored in localStorage (not sessionStorage for MVP)
   - Session persists (MVP behavior - remember me is optional UI element)
   ```

2. **Login with Remember Me Checked**
   ```
   Action: Log in WITH "Remember me" checked
   Expected: Same behavior as above (MVP stores all tokens in localStorage)
   ```

**Note:** Full "Remember me" implementation (sessionStorage vs localStorage) is planned for Phase 2.

---

### Scenario 8: Forgot Password Link

**Objective:** Verify forgot password link is present and navigates correctly.

**Acceptance Criteria Tested:** AC-1.9.2 (Forgot password link)

**Steps:**

1. **On Login Page**
   ```
   Action: Look for "Forgot password?" link
   Expected: Link visible below password field
   
   Action: Click link
   Expected: Navigate to /forgot-password (or show "Coming Soon" if not implemented)
   ```

**Success Criteria:**
- [ ] Link is visible and accessible
- [ ] Link navigates to correct page

---

### Scenario 9: Navigation Between Auth Pages

**Objective:** Test links between signup and login pages.

**Acceptance Criteria Tested:** AC-1.9.7 (Routing & Navigation)

**Steps:**

1. **From Home to Signup**
   ```
   Action: Click "Sign Up" on home page
   Expected: Navigate to /signup
   ```

2. **From Signup to Login**
   ```
   Action: Click "Log In" link at bottom of signup form
   Expected: Navigate to /login
   ```

3. **From Login to Signup**
   ```
   Action: Click "Sign Up" link at bottom of login form
   Expected: Navigate to /signup
   ```

4. **From Success Screen to Login**
   ```
   Action: After successful signup, click "Go to Login →"
   Expected: Navigate to /login
   ```

**Success Criteria:**
- [ ] All navigation links work
- [ ] URLs update correctly
- [ ] Back button works

---

### Scenario 10: Redirect Authenticated Users

**Objective:** Verify logged-in users can't access auth pages.

**Acceptance Criteria Tested:** AC-1.9.7 (Redirect authenticated users)

**Prerequisite:** User must be logged in.

**Steps:**

1. **Try to Access Signup While Logged In**
   ```
   Action: Log in, then manually navigate to /signup
   Expected: Automatic redirect to /dashboard (or /onboarding)
   ```

2. **Try to Access Login While Logged In**
   ```
   Action: While logged in, navigate to /login
   Expected: Automatic redirect to /dashboard (or /onboarding)
   ```

**Success Criteria:**
- [ ] Authenticated users cannot access /signup
- [ ] Authenticated users cannot access /login
- [ ] Redirect happens instantly

---

### Scenario 11: Mobile Responsiveness (Mobile Devices)

**Objective:** Test signup/login on mobile devices.

**Acceptance Criteria Tested:** AC-1.9.9 (Mobile responsiveness)

**Devices to Test:**
- iOS (iPhone Safari)
- Android (Chrome)
- Browser DevTools mobile emulation (as backup)

**Steps:**

1. **Access Signup on Mobile**
   ```
   Action: Open http://[your-ip]:5173/signup on mobile device
   Expected:
   - Form renders correctly (no horizontal scroll)
   - Text is readable without zooming
   - Input fields are at least 44px tall (easy to tap)
   - Buttons are easy to tap
   ```

2. **Test Virtual Keyboard**
   ```
   Action: Tap email field
   Expected: Email keyboard appears (with @ symbol)
   
   Action: Tap password field
   Expected: Standard keyboard appears
   ```

3. **Complete Signup on Mobile**
   ```
   Action: Fill out entire signup form on mobile
   Expected:
   - All fields are easy to interact with
   - Validation messages are readable
   - Password strength indicator displays correctly
   - Submit button is easy to tap
   - Success screen is readable
   ```

4. **Test Login on Mobile**
   ```
   Action: Complete login flow on mobile
   Expected: Same ease of use as desktop
   ```

5. **Rate Mobile Experience**
   ```
   Ask tester to rate 1-5 on:
   - Ease of use: ___/5
   - Visual design: ___/5
   - Speed/performance: ___/5
   - Overall satisfaction: ___/5
   ```

**Success Criteria:**
- [ ] All elements render correctly
- [ ] No horizontal scrolling
- [ ] Touch targets are adequate
- [ ] Virtual keyboard is appropriate
- [ ] Average rating ≥4/5

---

### Scenario 12: Accessibility Testing

**Objective:** Verify screen reader compatibility and keyboard navigation.

**Acceptance Criteria Tested:** AC-1.9.4 (Accessibility)

**Tools Needed:**
- Screen reader (NVDA for Windows, JAWS, or VoiceOver for Mac)
- Keyboard only (no mouse)

**Steps:**

1. **Keyboard Navigation on Signup**
   ```
   Action: Use ONLY Tab key to navigate through signup form
   Expected:
   - Tab moves focus to: First Name → Last Name → Email → Password → Submit button
   - Focus indicator is clearly visible (outline/border)
   - Enter key on submit button submits form
   ```

2. **Screen Reader Testing**
   ```
   Action: Turn on screen reader and navigate signup form
   Expected:
   - Each field is announced with its label
   - Required fields are announced as "required"
   - Error messages are announced immediately
   - Success messages are announced
   ```

3. **ARIA Labels Verification**
   ```
   Action: Inspect form elements in DevTools
   Expected: Each field has:
   - aria-label or label element
   - aria-required="true"
   - aria-invalid="true" when invalid
   - aria-describedby linking to error message
   ```

**Success Criteria:**
- [ ] All fields accessible via keyboard
- [ ] Screen reader announces all content
- [ ] ARIA labels present
- [ ] Focus indicators visible

---

## Database Verification Guide

### Overview

This section teaches you how to verify that frontend actions correctly update the database. This is critical for UAT because the UI might "look" correct but fail to save data properly.

### Tools Required

- SQL Server Management Studio (SSMS)
- Or Azure Data Studio
- Or any SQL client that can query SQL Server

### How to Verify Database Changes

**Step 1: Open Query Window**
```sql
-- Connect to EventLeadDB database
USE EventLeadDB;
GO
```

**Step 2: Run verification queries (see below)**

---

### Verification 1: New User Signup

**When to Check:** After completing Scenario 1 (New User Signup)

**What to Verify:**
1. User record created in `dbo.User` table
2. Verification token created in `dbo.UserEmailVerificationToken` table
3. No login records yet (user hasn't logged in)

**Query 1: Check User Record**
```sql
-- Find the user you just created
SELECT 
    UserID,
    Email,
    FirstName,
    LastName,
    EmailVerified,
    IsActive,
    OnboardingComplete,
    CreatedDate,
    UpdatedDate
FROM dbo.[User]
WHERE Email = 'john.doe@testmail.com';
```

**Expected Results:**
```
UserID: [Auto-generated, e.g., 123]
Email: john.doe@testmail.com
FirstName: John
LastName: Doe
EmailVerified: 0 (FALSE - not verified yet)
IsActive: 1 (TRUE)
OnboardingComplete: 0 (FALSE - not completed yet)
CreatedDate: [Current timestamp]
UpdatedDate: [Current timestamp]
```

**✅ Success Check:**
- [ ] User record exists
- [ ] Email matches what you entered
- [ ] EmailVerified = 0 (not verified yet)
- [ ] IsActive = 1 (account is active)
- [ ] CreatedDate is recent (within last 5 minutes)

**❌ Failure Indicators:**
- No record found → Signup didn't save to database
- EmailVerified = 1 → Should be 0 until email verified
- IsActive = 0 → Account should be active by default

**Query 2: Check Verification Token**
```sql
-- Find the verification token for this user
SELECT 
    TokenID,
    UserID,
    Token,
    ExpiresAt,
    UsedAt,
    CreatedDate
FROM dbo.UserEmailVerificationToken
WHERE UserID = [UserID from Query 1];
```

**Expected Results:**
```
TokenID: [Auto-generated]
UserID: [Matches user from Query 1]
Token: [Random string, e.g., "a1b2c3d4e5f6..."]
ExpiresAt: [24 hours from now]
UsedAt: NULL (not used yet)
CreatedDate: [Current timestamp]
```

**✅ Success Check:**
- [ ] Token record exists
- [ ] Token is not NULL
- [ ] ExpiresAt is 24 hours in future
- [ ] UsedAt is NULL

**Query 3: Check Password Hash**
```sql
-- Verify password is hashed (not plain text)
SELECT 
    UserID,
    Email,
    PasswordHash,
    LEN(PasswordHash) AS HashLength
FROM dbo.[User]
WHERE Email = 'john.doe@testmail.com';
```

**Expected Results:**
```
PasswordHash: [Long hashed string, e.g., "$2b$12$xyz..."]
HashLength: 60 (for bcrypt) or similar
```

**⚠️ CRITICAL Security Check:**
- [ ] PasswordHash is NOT "Test1234!" (plain text)
- [ ] PasswordHash is a long string (60+ characters)
- [ ] PasswordHash starts with "$2b$" or similar (bcrypt format)

**❌ MAJOR FAILURE if:**
- PasswordHash contains plain text password
- This is a critical security vulnerability

---

### Verification 2: User Login

**When to Check:** After completing Scenario 3 (Login with Valid Credentials)

**What to Verify:**
1. Refresh token created in `dbo.UserRefreshToken` table
2. API request logged in `log.ApiRequest` table
3. No application errors in `log.ApplicationError` table

**Query 1: Check Refresh Token**
```sql
-- Find refresh tokens for this user
SELECT 
    RefreshTokenID,
    UserID,
    Token,
    ExpiresAt,
    RevokedAt,
    CreatedDate
FROM dbo.UserRefreshToken
WHERE UserID = [UserID from previous query]
ORDER BY CreatedDate DESC;
```

**Expected Results:**
```
RefreshTokenID: [Auto-generated]
UserID: [Your user's ID]
Token: [Long random string]
ExpiresAt: [7 days from now, or configured expiry]
RevokedAt: NULL (token is active)
CreatedDate: [Just now]
```

**✅ Success Check:**
- [ ] New refresh token created
- [ ] Token is NOT NULL
- [ ] ExpiresAt is in the future
- [ ] RevokedAt is NULL (token is valid)

**Query 2: Check API Request Logs**
```sql
-- Find recent login API requests
SELECT TOP 10
    ApiRequestID,
    RequestID,
    Method,
    Path,
    StatusCode,
    DurationMs,
    UserID,
    IPAddress,
    CreatedDate
FROM log.ApiRequest
WHERE Path LIKE '%/api/auth/login%'
ORDER BY CreatedDate DESC;
```

**Expected Results:**
```
Method: POST
Path: /api/auth/login
StatusCode: 200 (success)
DurationMs: [Usually < 500ms]
UserID: [Your user's ID after login]
IPAddress: [Your IP or ::1 for localhost]
```

**✅ Success Check:**
- [ ] Login request logged
- [ ] StatusCode = 200 (success)
- [ ] DurationMs < 1000 (reasonable performance)
- [ ] UserID matches your user

**Query 3: Check for Errors**
```sql
-- Look for any errors in the last 5 minutes
SELECT TOP 10
    ErrorID,
    ErrorType,
    ErrorMessage,
    Severity,
    Path,
    StackTrace,
    CreatedDate
FROM log.ApplicationError
WHERE CreatedDate > DATEADD(MINUTE, -5, GETDATE())
ORDER BY CreatedDate DESC;
```

**Expected Results:**
```
[No rows returned] ← This is GOOD!
```

**✅ Success Check:**
- [ ] No errors logged during UAT session
- [ ] If errors exist, they are unrelated to auth flow

**❌ Failure Indicators:**
- Errors with Path = '/api/auth/login' or '/api/auth/signup'
- Severity = 'ERROR' or 'CRITICAL'

---

### Verification 3: Failed Login Attempt

**When to Check:** After completing Scenario 4 (Login with Invalid Credentials)

**What to Verify:**
1. NO refresh token created (login failed)
2. API request logged with status 401 Unauthorized
3. No changes to User table (failed login doesn't modify user)

**Query 1: Check API Logs for Failed Login**
```sql
-- Find failed login attempts
SELECT TOP 10
    ApiRequestID,
    Method,
    Path,
    StatusCode,
    DurationMs,
    IPAddress,
    CreatedDate
FROM log.ApiRequest
WHERE Path LIKE '%/api/auth/login%'
  AND StatusCode != 200
ORDER BY CreatedDate DESC;
```

**Expected Results:**
```
StatusCode: 401 (Unauthorized)
Path: /api/auth/login
Method: POST
```

**✅ Success Check:**
- [ ] Failed login logged
- [ ] StatusCode = 401 (Unauthorized)
- [ ] No refresh token created for this attempt

**Query 2: Verify No Refresh Token**
```sql
-- Count refresh tokens (should not increase after failed login)
SELECT COUNT(*) AS TokenCount
FROM dbo.UserRefreshToken
WHERE UserID = [Your UserID]
  AND CreatedDate > DATEADD(MINUTE, -5, GETDATE());
```

**Expected Results:**
```
TokenCount: 0 (no new tokens from failed login)
```

---

### Verification 4: Email Verification Token Used

**When to Check:** After user clicks verification link in email (Story 1.10)

**Note:** This is for future reference when email verification is implemented.

**Query:**
```sql
-- Check if verification token was used
SELECT 
    TokenID,
    UserID,
    Token,
    ExpiresAt,
    UsedAt,
    CreatedDate
FROM dbo.UserEmailVerificationToken
WHERE UserID = [Your UserID];
```

**Expected Results After Verification:**
```
UsedAt: [Timestamp when user clicked verification link]
ExpiresAt: [Future timestamp]
```

**Query 2: Check User Email Verified**
```sql
-- Verify user's email is now verified
SELECT 
    UserID,
    Email,
    EmailVerified,
    UpdatedDate
FROM dbo.[User]
WHERE UserID = [Your UserID];
```

**Expected Results:**
```
EmailVerified: 1 (TRUE - email now verified)
UpdatedDate: [Updated timestamp]
```

---

### Common Database Troubleshooting

**Problem:** No user record after signup

**Possible Causes:**
1. Backend API not running
2. Database connection failed
3. Frontend not calling correct API endpoint
4. Validation failed on backend

**How to Debug:**
1. Check backend logs for errors
2. Verify database connection string
3. Check browser Network tab (F12) for API calls
4. Look in `log.ApplicationError` table for errors

**Query to Debug:**
```sql
-- Look for recent signup API calls
SELECT TOP 10 *
FROM log.ApiRequest
WHERE Path LIKE '%/api/auth/signup%'
ORDER BY CreatedDate DESC;

-- Look for errors
SELECT TOP 10 *
FROM log.ApplicationError
WHERE Path LIKE '%/api/auth/signup%'
ORDER BY CreatedDate DESC;
```

---

**Problem:** Password appears in logs or database

**THIS IS CRITICAL SECURITY ISSUE!**

**What to Check:**
```sql
-- Check if password is hashed
SELECT Email, PasswordHash
FROM dbo.[User]
WHERE Email = 'test@example.com';
-- PasswordHash should be long hashed string, NOT plain text

-- Check API request logs (passwords should NOT appear here)
SELECT TOP 10 RequestBody
FROM log.ApiRequest
WHERE Path LIKE '%/api/auth/%';
-- Look for passwords in RequestBody - should be [REDACTED]
```

**If passwords are visible:**
1. STOP UAT immediately
2. Notify development team
3. This is a P0 security bug
4. Do NOT proceed to production

---

## UAT Best Practices for Your Team

### How to Run Effective UAT Sessions

This section teaches you and your team the methodology behind UAT, so you can apply it to future stories.

---

### 1. The Think-Aloud Protocol

**What is it?**
Ask testers to verbalize their thoughts while testing.

**Why it works:**
You discover:
- What confuses users
- What they expect to happen
- Where they get stuck
- What delights them

**How to do it:**
```
UAT Lead: "Please talk through what you're thinking as you use the application."

Tester: "Okay, I see a signup form. I'm going to fill in my name... 
         Oh, the first name field is glowing red. I wonder what I did wrong?
         Ah, I see the error message - it needs at least 2 characters. That makes sense."
```

**✅ Good UAT Facilitation:**
- Let tester explore naturally
- Don't give hints or help (unless completely stuck)
- Take notes on confusion points
- Ask "What are you thinking?" if they go silent

**❌ Bad UAT Facilitation:**
- "Click the blue button on the right"
- "No, you need to enter your email first"
- Helping too quickly (defeats purpose of testing)

---

### 2. The 5-Second Rule

**What is it?**
If a user is confused for more than 5 seconds, there's a UX problem.

**How to apply:**
- Time how long users take to complete tasks
- If they pause and look confused → UX issue
- If they click wrong button → UI is unclear

**Example:**
```
Task: "Sign up for an account"
Tester: [Stares at form for 8 seconds]
Tester: "I'm not sure what to do with this password..."

Issue Found: Password requirements not visible until typing
Fix: Show requirements before user types
```

---

### 3. Mobile-First Testing

**Why mobile matters:**
- 60%+ of users access web apps on mobile
- Touch targets are different from mouse clicks
- Virtual keyboards change the experience

**How to test mobile:**
1. **Real devices > Emulators**
   - Chrome DevTools mobile mode is okay for layout
   - Real devices catch touch issues, keyboard issues, performance

2. **Test minimum viable tap targets**
   - Buttons should be at least 44x44 pixels
   - Form fields should be at least 44px tall

3. **Test virtual keyboard interactions**
   - Email field should show email keyboard (@, .com)
   - Password field should allow paste (for password managers)
   - Form shouldn't resize weirdly when keyboard appears

**Mobile Testing Checklist:**
- [ ] All text readable without zooming
- [ ] No horizontal scrolling required
- [ ] Buttons easy to tap (no mis-taps)
- [ ] Virtual keyboard doesn't cover important content
- [ ] Performance feels smooth (no lag)

---

### 4. Error Path Testing is Critical

**Common mistake:**
Only testing the "happy path" (everything works perfectly)

**Reality:**
Users make mistakes, networks fail, servers hiccup

**What to test:**
- Wrong password
- Invalid email format
- Network disconnected (turn off wifi mid-signup)
- Server down (stop backend API)
- Duplicate data
- Edge cases (emoji in name field? 🤔)

**Error Message Quality Checklist:**
- [ ] Tells user WHAT went wrong
- [ ] Tells user HOW to fix it
- [ ] Uses plain language (no "Error 422: Unprocessable Entity")
- [ ] Appears in expected location
- [ ] Visible color contrast (red on red is bad)

**Example - Bad Error:**
```
"Error: VALIDATION_FAILED"
```

**Example - Good Error:**
```
"This email is already registered. Try logging in or use a different email address."
```

---

### 5. Database Verification is Essential

**Why check the database?**
- UI might show success but fail to save data
- Data might be saved incorrectly
- Security issues (passwords in plain text)

**When to check:**
- After every Create operation (signup)
- After every Update operation (login)
- After error paths (failed login shouldn't create records)

**What to verify:**
1. **Data Existence:** Record was created
2. **Data Accuracy:** Values match what user entered
3. **Data Security:** Sensitive data is hashed/encrypted
4. **Data Relationships:** Foreign keys link correctly
5. **Audit Trail:** CreatedDate, UpdatedDate populated

**Teaching Your Team:**
Create a "Database Verification Cheat Sheet" with common queries for each story.

---

### 6. Accessibility is Non-Negotiable

**Why it matters:**
- Legal requirement (ADA, WCAG 2.1)
- 15% of population has some disability
- Good accessibility = better UX for everyone

**Basic Accessibility Tests:**

1. **Keyboard Navigation**
   ```
   Test: Can you complete entire task using only Tab and Enter keys?
   Success: Yes, without touching mouse
   ```

2. **Screen Reader**
   ```
   Test: Turn on NVDA/VoiceOver and navigate form
   Success: All content is announced clearly
   ```

3. **Color Contrast**
   ```
   Test: Use browser DevTools to check contrast ratios
   Success: 4.5:1 minimum for text, 3:1 for large text
   ```

4. **Focus Indicators**
   ```
   Test: Tab through form - can you see where focus is?
   Success: Clear outline or border on focused element
   ```

**Accessibility Testing Tools:**
- WAVE browser extension (free)
- axe DevTools (free)
- Lighthouse (built into Chrome DevTools)

---

### 7. Performance Matters

**What to measure:**
- Time to complete signup: < 2 minutes
- Time from click to response: < 3 seconds
- Page load time: < 2 seconds
- API response time: < 500ms

**How to measure:**
```
Browser DevTools → Network tab → Watch timing
- Signup API call should be < 500ms
- Login API call should be < 300ms
```

**If performance is slow:**
1. Check database query performance (use SQL Profiler)
2. Check network latency (WiFi vs wired)
3. Check backend logs for slow operations

---

### 8. Security Testing Basics

**What to check:**

1. **Passwords Never Visible in Logs**
   ```sql
   -- Passwords should be [REDACTED] in API logs
   SELECT RequestBody FROM log.ApiRequest WHERE Path LIKE '%auth%';
   ```

2. **Passwords Hashed in Database**
   ```sql
   -- Should see long hash, not plain text
   SELECT PasswordHash FROM dbo.[User];
   ```

3. **JWT Tokens Not in URL**
   ```
   Check browser URL bar - should NOT see ?token=xyz...
   Tokens should be in localStorage or headers only
   ```

4. **No Sensitive Data in Browser Console**
   ```
   Open F12 → Console
   Should NOT see: console.log("Password: Test1234!")
   ```

---

## Results Template

Use this template to record UAT results for each tester.

---

### UAT Session: Story 1.9 - Authentication

**Tester Information:**
- Name: ___________________________
- Role: ___________________________ (e.g., Event Organizer, Developer, QA)
- Device: _________________________ (Desktop, Mobile - specify)
- Browser: ________________________ (Chrome, Safari, etc.)
- Date: ___________________________
- Duration: _______________________ minutes

---

**Scenario Results:**

| Scenario | Pass/Fail | Time (sec) | Notes |
|----------|-----------|------------|-------|
| 1. New User Signup | ☐ Pass ☐ Fail | _____ | |
| 2. Duplicate Email Error | ☐ Pass ☐ Fail | _____ | |
| 3. Valid Login | ☐ Pass ☐ Fail | _____ | |
| 4. Invalid Login | ☐ Pass ☐ Fail | _____ | |
| 5. Unverified Email Block | ☐ Pass ☐ Fail | _____ | |
| 6. Password Visibility Toggle | ☐ Pass ☐ Fail | _____ | |
| 7. Remember Me | ☐ Pass ☐ Fail | _____ | |
| 8. Forgot Password Link | ☐ Pass ☐ Fail | _____ | |
| 9. Navigation Links | ☐ Pass ☐ Fail | _____ | |
| 10. Redirect Authenticated | ☐ Pass ☐ Fail | _____ | |
| 11. Mobile Responsiveness | ☐ Pass ☐ Fail | _____ | |
| 12. Accessibility | ☐ Pass ☐ Fail | _____ | |

**Overall Time to Complete Signup:** _______ minutes (Target: < 2 minutes)

---

**Database Verification:**

| Check | Pass/Fail | Notes |
|-------|-----------|-------|
| User record created | ☐ Pass ☐ Fail | |
| Password hashed correctly | ☐ Pass ☐ Fail | |
| Verification token created | ☐ Pass ☐ Fail | |
| Refresh token on login | ☐ Pass ☐ Fail | |
| API requests logged | ☐ Pass ☐ Fail | |
| No errors in error log | ☐ Pass ☐ Fail | |

---

**User Experience Ratings (1-5 scale, 5 = best):**

- Ease of use: ☐ 1 ☐ 2 ☐ 3 ☐ 4 ☐ 5
- Visual design: ☐ 1 ☐ 2 ☐ 3 ☐ 4 ☐ 5
- Error message clarity: ☐ 1 ☐ 2 ☐ 3 ☐ 4 ☐ 5
- Speed/performance: ☐ 1 ☐ 2 ☐ 3 ☐ 4 ☐ 5
- Mobile experience: ☐ 1 ☐ 2 ☐ 3 ☐ 4 ☐ 5 ☐ N/A

**Overall satisfaction:** ☐ 1 ☐ 2 ☐ 3 ☐ 4 ☐ 5

---

**Issues Found:**

| Issue # | Severity | Description | Steps to Reproduce |
|---------|----------|-------------|-------------------|
| 1 | ☐ Critical ☐ High ☐ Medium ☐ Low | | |
| 2 | ☐ Critical ☐ High ☐ Medium ☐ Low | | |
| 3 | ☐ Critical ☐ High ☐ Medium ☐ Low | | |

**Severity Definitions:**
- **Critical:** Blocks usage (e.g., can't signup at all)
- **High:** Major issue (e.g., confusing error message)
- **Medium:** Annoying but not blocking (e.g., button color)
- **Low:** Nice to have (e.g., typo)

---

**Positive Observations:**

What worked well?
- ___________________________________________
- ___________________________________________
- ___________________________________________

---

**Improvement Suggestions:**

What could be better?
- ___________________________________________
- ___________________________________________
- ___________________________________________

---

**Tester Comments:**

[Free-form feedback]

_______________________________________________
_______________________________________________
_______________________________________________

---

**UAT Lead Sign-Off:**

- Lead: ________________________
- Date: ________________________
- Decision: ☐ **PASS - Ready for Production** ☐ **CONDITIONAL PASS - Fix minor issues** ☐ **FAIL - Requires fixes and retest**

---

## Summary & Next Steps

### UAT Success Criteria

Story 1.9 UAT is considered **PASSED** if:

- ✅ 90%+ completion rate (9/10 testers successfully complete signup)
- ✅ Average signup time < 2 minutes
- ✅ All critical acceptance criteria validated
- ✅ Error messages understood by 100% of testers
- ✅ Mobile rating ≥ 4/5 average
- ✅ No critical or high-severity bugs found
- ✅ Database verification passes for all scenarios
- ✅ Accessibility tests pass (keyboard nav, screen reader)

### Post-UAT Actions

**If UAT Passes:**
1. Document test results
2. Archive test data
3. Schedule production deployment
4. Prepare rollback plan
5. Monitor production logs after deployment

**If UAT Fails:**
1. Prioritize issues (Critical → High → Medium → Low)
2. Create bug tickets for each issue
3. Fix issues
4. Retest affected scenarios
5. Schedule follow-up UAT session

### Training Your Team

**Checklist for Teaching UAT:**
- [ ] Share this guide with team
- [ ] Run practice UAT session on completed feature
- [ ] Record UAT session (video) for training
- [ ] Create story-specific UAT checklists
- [ ] Establish UAT schedule (every sprint)
- [ ] Define roles (UAT Lead, Testers, Note-taker)

---

## Appendix: Quick Reference

### Essential SQL Queries

```sql
-- Find user by email
SELECT * FROM dbo.[User] WHERE Email = 'test@example.com';

-- Check recent signups (last 24 hours)
SELECT * FROM dbo.[User] WHERE CreatedDate > DATEADD(DAY, -1, GETDATE());

-- Count refresh tokens per user
SELECT UserID, COUNT(*) AS TokenCount 
FROM dbo.UserRefreshToken 
GROUP BY UserID;

-- Recent API requests
SELECT TOP 20 * FROM log.ApiRequest ORDER BY CreatedDate DESC;

-- Recent errors
SELECT TOP 20 * FROM log.ApplicationError ORDER BY CreatedDate DESC;

-- Check password hashing
SELECT Email, LEFT(PasswordHash, 10) + '...' AS HashPreview, LEN(PasswordHash) AS HashLength
FROM dbo.[User];
```

### Browser DevTools Shortcuts

- **F12** - Open DevTools
- **Ctrl+Shift+Delete** - Clear cache
- **Ctrl+Shift+C** - Inspect element
- **Ctrl+Shift+M** - Toggle mobile view

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Form doesn't submit | Check browser console (F12) for JavaScript errors |
| API call fails | Check backend is running, check Network tab in DevTools |
| User not created in DB | Check backend logs, check `log.ApplicationError` table |
| Slow performance | Check Network tab for slow API calls, check database query plans |
| Mobile layout broken | Test in real device, not just DevTools emulation |

---

**End of UAT Guide**

**Questions?** Contact UAT Lead: Anthony Keevy

**Document Version:** 1.0  
**Last Updated:** 2025-01-19  
**Story:** 1.9 - Frontend Authentication

