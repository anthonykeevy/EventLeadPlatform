# UAT Instructions: Story 1.13 - Configuration Service

**Story:** Configuration Service Implementation  
**Status:** Ready for UAT  
**Date:** October 17, 2025  
**Tester Profile:** Business Admin Users + End Users  
**Duration:** 90 minutes (60 min admin + 30 min end user)  
**Environment:** Staging (with admin access enabled)

---

## Pre-Requisites

### For UAT Testers:
- [ ] Admin user account with `system_admin` role
- [ ] Regular user account for end-user testing
- [ ] Access to staging environment
- [ ] Chrome/Edge browser (latest version)
- [ ] Database connection credentials (for verification queries)

### For UAT Facilitator:
- [ ] Backend services running (`.\scripts\start-services-clean.ps1`)
- [ ] MailHog running for email verification
- [ ] Database seeded with configuration data
- [ ] Admin panel accessible
- [ ] Monitoring dashboard open

---

## Test Environment Setup

### 1. Start Services
```powershell
# From project root directory (C:\Users\tonyk\OneDrive\Projects\EventLeadPlatform)
.\scripts\start-services-clean.ps1

# Then start backend (in same or new terminal)
cd backend
.\venv\Scripts\activate
python -m uvicorn main:app --reload

# Then start frontend (in new terminal)
cd frontend
npm run dev
```

### 2. Verify Services
```powershell
.\scripts\simple-monitor.ps1
```

**Expected:** All services show "Running" status

### 3. Verify Database Configuration
Open SQL Server Management Studio and run:
```sql
-- Should return 12 settings
SELECT SettingKey, SettingValue, SettingType, IsActive
FROM config.AppSetting
WHERE IsDeleted = 0
ORDER BY SortOrder;
```

**Expected:** 12 rows returned with authentication, security, validation, invitation, and email settings

---

## UAT Test Scenarios

## **SCENARIO 1: Admin Changes JWT Token Expiry** (Critical)

**Goal:** Verify admins can change JWT expiry without code deployment

### Steps:

1. **Login as Admin**
   - Navigate to: `http://localhost:8000/admin/settings`
   - Login with admin credentials
   - **Expected:** Admin settings page loads

2. **View Current Settings**
   - Locate "JWT Access Token Expiry" setting
   - Note current value (should be "15" minutes)
   - **Expected:** Setting displays with description and current value

3. **Update JWT Expiry**
   - Click "Edit" on JWT Access Token Expiry setting
   - Change value from "15" to "30"
   - Click "Save"
   - **Expected:** 
     - Success message displayed
     - Value updates immediately
     - No page refresh required

4. **Force Cache Reload** (5-minute cache test)
   - Click "Reload Configuration Cache" button
   - **Expected:** Success message "Configuration reloaded"

5. **Verify Change Takes Effect**
   - Open new browser window (incognito)
   - Login as regular user
   - Check JWT token expiry in browser developer tools:
     ```javascript
     // In Console:
     const token = localStorage.getItem('access_token');
     const payload = JSON.parse(atob(token.split('.')[1]));
     console.log('Token expires in:', (payload.exp - payload.iat) / 60, 'minutes');
     ```
   - **Expected:** Shows "30 minutes" (not 15)

6. **Verify Database Audit Trail**
   ```sql
   SELECT TOP 1 
       SettingKey, 
       SettingValue, 
       UpdatedBy, 
       UpdatedDate 
   FROM config.AppSetting 
   WHERE SettingKey = 'ACCESS_TOKEN_EXPIRY_MINUTES'
   ORDER BY UpdatedDate DESC;
   ```
   - **Expected:** Shows updated value with admin UserID and timestamp

### Success Criteria:
- [ ] Admin can update setting without developer help
- [ ] Change takes effect within 5 minutes (or immediately with cache reload)
- [ ] New logins receive 30-minute tokens
- [ ] Old tokens remain valid until their original expiry
- [ ] Audit trail shows who/when/what changed

---

## **SCENARIO 2: Admin Changes Password Minimum Length** (Critical)

**Goal:** Verify password validation uses database-configured rules

### Steps:

1. **Update Password Minimum Length**
   - Navigate to admin settings
   - Find "Password Minimum Length" setting
   - Change from "8" to "10"
   - Save changes
   - Reload configuration cache

2. **Test on Signup Form (End User)**
   - Open signup page: `http://localhost:8000/signup`
   - Attempt to signup with 8-character password: `Test1234`
   - **Expected:** Error message "Password must be at least 10 characters long"

3. **Test with Valid Password**
   - Attempt signup with 10-character password: `Test123456`
   - Complete signup form
   - **Expected:** Signup successful, validation passes

4. **Verify Frontend Displays Updated Requirement**
   - Check password field placeholder text
   - **Expected:** Shows "Password (min 10 characters)"

5. **Verify Existing Users Not Affected**
   - Login as existing user with 8-character password
   - **Expected:** Login successful (no retroactive enforcement)

### Success Criteria:
- [ ] Password validation uses new minimum (10 characters)
- [ ] Frontend displays correct requirement
- [ ] Error messages are clear and helpful
- [ ] Existing users with shorter passwords can still login
- [ ] Change took effect within 5 minutes

---

## **SCENARIO 3: Configuration Fallback on Database Unavailable** (Resilience)

**Goal:** Verify system continues with code defaults if database fails

### Steps:

1. **Record Current Settings**
   - Note current JWT expiry, password min length
   - Record from admin panel

2. **Simulate Database Unavailability**
   - Stop backend service
   - Rename database connection string in `.env`:
     ```
     DATABASE_URL=invalid_connection_string
     ```
   - Restart backend service

3. **Attempt to Use Application**
   - Open signup page
   - Attempt to signup with 8-character password
   - **Expected:** 
     - Application continues to function
     - Uses code defaults (8-character minimum)
     - No crashes or 500 errors

4. **Check Application Logs**
   ```sql
   SELECT TOP 10 * 
   FROM log.ApplicationError 
   ORDER BY CreatedDate DESC;
   ```
   - **Expected:** Warning logs about fallback, but no errors

5. **Restore Database Connection**
   - Fix `.env` connection string
   - Restart backend
   - **Expected:** Application resumes using database configuration

### Success Criteria:
- [ ] Application doesn't crash when database unavailable
- [ ] Falls back to sensible code defaults
- [ ] Warning logged (not error)
- [ ] Seamlessly resumes database config when restored
- [ ] No data loss or corruption

---

## **SCENARIO 4: Configuration Changes Are Audited** (Compliance)

**Goal:** Verify all configuration changes are tracked for compliance

### Steps:

1. **Make Multiple Configuration Changes**
   - As Admin User 1: Change JWT expiry to 45 minutes
   - As Admin User 2: Change password min length to 12
   - As Admin User 1: Change invitation expiry to 14 days

2. **Query Audit Trail**
   ```sql
   SELECT 
       s.SettingKey,
       s.SettingValue,
       u.Email AS ChangedBy,
       s.UpdatedDate,
       s.SettingValue AS NewValue
   FROM config.AppSetting s
   LEFT JOIN dbo.[User] u ON s.UpdatedBy = u.UserID
   WHERE s.UpdatedDate > DATEADD(HOUR, -1, GETUTCDATE())
   ORDER BY s.UpdatedDate DESC;
   ```

3. **Verify Audit Completeness**
   - **Expected Results:**
     - All 3 changes logged
     - Each shows who made the change (email address)
     - Each shows when (timestamp)
     - Each shows what changed (new value)

4. **Test Cannot Change Without Audit**
   - Attempt to bypass API and update database directly
   - Verify application detects and logs this
   - **Expected:** Direct database changes detected in next audit report

### Success Criteria:
- [ ] 100% of changes audited
- [ ] Audit shows who, what, when
- [ ] Cannot change configuration without audit record
- [ ] Audit trail immutable (no deletion)
- [ ] Compliance report can be generated

---

## **SCENARIO 5: Frontend Receives Configuration Updates** (User Experience)

**Goal:** Verify frontend adapts to configuration changes automatically

### Steps:

1. **Open Signup Page**
   - Navigate to: `http://localhost:8000/signup`
   - Note current password requirement in placeholder

2. **Admin Changes Password Requirement**
   - In separate browser window, login as admin
   - Change password min length from 8 to 12
   - Reload configuration cache

3. **Wait for Frontend Cache Expiry**
   - Wait 5 minutes (React Query cache duration)
   - OR refresh the signup page
   - **Expected:** Placeholder text updates to "Password (min 12 characters)"

4. **Test Password Validation**
   - Enter 10-character password
   - **Expected:** Validation error "Password must be at least 12 characters long"
   - Enter 12-character password
   - **Expected:** Validation passes

5. **Verify Multiple Settings Update Together**
   - Admin changes:
     - JWT expiry to 60 minutes
     - Email verification expiry to 48 hours
     - Company name min length to 3
   - Reload frontend
   - **Expected:** All settings reflect new values

### Success Criteria:
- [ ] Frontend receives configuration updates within 5 minutes
- [ ] UI adapts to new requirements automatically
- [ ] Users see updated validation requirements
- [ ] No manual refresh required (after cache expiry)
- [ ] Multiple setting changes applied together

---

## **SCENARIO 6: Multiple Configuration Changes** (Stress Test)

**Goal:** Verify system handles rapid configuration changes

### Steps:

1. **Rapid Fire Configuration Changes**
   - Change JWT expiry: 15 → 30 → 45 → 60 minutes
   - Change password min: 8 → 10 → 12 → 8 characters
   - Change invitation expiry: 7 → 14 → 7 days
   - All within 2 minutes

2. **Verify System Stability**
   - **Expected:**
     - All changes accepted
     - No conflicts or errors
     - Latest value always wins
     - Cache invalidates correctly

3. **Test Concurrent Changes**
   - Admin User 1 changes JWT expiry
   - Admin User 2 changes password minimum
   - Both at the same time
   - **Expected:** Both changes succeed independently

4. **Verify Final State**
   ```sql
   SELECT SettingKey, SettingValue, UpdatedDate, UpdatedBy
   FROM config.AppSetting
   WHERE SettingKey IN (
       'ACCESS_TOKEN_EXPIRY_MINUTES',
       'PASSWORD_MIN_LENGTH',
       'INVITATION_EXPIRY_DAYS'
   )
   ORDER BY SettingKey;
   ```
   - **Expected:** Latest values from each admin persisted

### Success Criteria:
- [ ] System handles rapid changes without errors
- [ ] No race conditions or data corruption
- [ ] Concurrent changes by different admins work
- [ ] Cache invalidates correctly for all changes
- [ ] Audit trail accurate for all changes

---

## **SCENARIO 7: Invalid Configuration Rejected** (Data Integrity)

**Goal:** Verify system prevents invalid configuration values

### Steps:

1. **Attempt Invalid Integer**
   - Try to set password min length to "abc"
   - **Expected:** Error "Invalid value for setting type 'integer'"

2. **Attempt Invalid Boolean**
   - Try to set welcome_email_enabled to "maybe"
   - **Expected:** Error "Invalid value for setting type 'boolean'"

3. **Attempt Negative Value**
   - Try to set password min length to "-5"
   - **Expected:** Error "Value must be positive"

4. **Attempt Zero or Empty**
   - Try to set JWT expiry to "0"
   - **Expected:** Error "Value must be greater than 0"

5. **Attempt SQL Injection**
   - Try to set value to: `'; DROP TABLE AppSetting; --`
   - **Expected:** 
     - Value rejected or safely escaped
     - No SQL injection vulnerability
     - System remains stable

6. **Verify Fallback to Default**
   - Corrupt a setting value in database directly
   - Restart application
   - **Expected:** Application uses DefaultValue from database or code default

### Success Criteria:
- [ ] Invalid values rejected with clear error messages
- [ ] Type validation enforced (integer, boolean, etc.)
- [ ] Range validation enforced (no negatives, zeros)
- [ ] No SQL injection vulnerabilities
- [ ] System falls back to safe defaults on corruption

---

## UAT Sign-Off Checklist

### Functional Requirements
- [ ] Admin can change JWT expiry without code deployment
- [ ] Admin can change password rules without code deployment  
- [ ] Changes take effect in ≤5 minutes (or immediately with cache reload)
- [ ] Frontend receives and displays updated configuration
- [ ] Existing users not affected by retroactive validation
- [ ] System functions with code defaults if database unavailable

### Non-Functional Requirements
- [ ] Configuration changes cause 0 seconds of downtime
- [ ] All configuration changes audited (who, what, when)
- [ ] Invalid configuration values rejected
- [ ] No crashes or 500 errors during testing
- [ ] Multiple concurrent changes handled correctly
- [ ] Cache invalidates correctly on changes

### Usability
- [ ] Admin can change settings without developer assistance
- [ ] Error messages are clear and actionable
- [ ] UI shows updated requirements to users
- [ ] Admin interface is intuitive
- [ ] No technical knowledge required to change settings

### Security & Compliance
- [ ] Cannot change configuration without authentication
- [ ] Cannot change configuration without `system_admin` role
- [ ] Audit trail is complete and immutable
- [ ] No SQL injection vulnerabilities
- [ ] Sensitive data not logged

---

## Issues and Observations

### Critical Issues (Blocker)
_Record any issues that prevent story completion_

| Issue ID | Description | Severity | Assigned To | Status |
|----------|-------------|----------|-------------|--------|
| | | | | |

### Major Issues (Must Fix Before Production)
_Record issues that should be fixed before production release_

| Issue ID | Description | Severity | Assigned To | Status |
|----------|-------------|----------|-------------|--------|
| | | | | |

### Minor Issues (Can Fix Later)
_Record nice-to-have improvements_

| Issue ID | Description | Severity | Assigned To | Status |
|----------|-------------|----------|-------------|--------|
| | | | | |

### Observations and Feedback
_General feedback from testers_

---

## UAT Sign-Off

### Tester Sign-Off

**Admin User Tester:**
- Name: _____________________
- Date: _____________________
- Signature: _____________________
- Result: [ ] Pass [ ] Pass with minor issues [ ] Fail

**End User Tester:**
- Name: _____________________
- Date: _____________________
- Signature: _____________________
- Result: [ ] Pass [ ] Pass with minor issues [ ] Fail

### Product Owner Sign-Off

**Product Owner:**
- Name: _____________________
- Date: _____________________
- Signature: _____________________
- Decision: [ ] Accept [ ] Accept with conditions [ ] Reject

**Conditions for Acceptance (if any):**
_____________________________________________________________________________________
_____________________________________________________________________________________

### Story Status After UAT

- [ ] **Accepted** - Ready for production deployment
- [ ] **Accepted with Minor Issues** - Deploy, fix issues in next sprint
- [ ] **Rejected** - Return to development team

---

## Appendix A: Test Data

### Admin User Credentials
```
Email: admin@eventlead.com
Password: Admin123!
Role: system_admin
```

### Regular User Credentials
```
Email: user@test.com
Password: User123!
Role: company_user
```

### Database Connection
```
Server: localhost
Database: EventLeadPlatform
Authentication: Windows Authentication (Trusted_Connection)
```

---

## Appendix B: Useful SQL Queries

### View Current Configuration
```sql
SELECT 
    s.SettingKey,
    s.SettingValue,
    sc.CategoryName,
    st.TypeName,
    s.Description,
    s.IsActive,
    s.UpdatedDate
FROM config.AppSetting s
LEFT JOIN ref.SettingCategory sc ON s.SettingCategoryID = sc.SettingCategoryID
LEFT JOIN ref.SettingType st ON s.SettingTypeID = st.SettingTypeID
WHERE s.IsDeleted = 0
ORDER BY s.SortOrder;
```

### View Configuration Change History
```sql
SELECT TOP 20
    s.SettingKey,
    s.SettingValue AS CurrentValue,
    u.Email AS ChangedBy,
    s.UpdatedDate
FROM config.AppSetting s
LEFT JOIN dbo.[User] u ON s.UpdatedBy = u.UserID
ORDER BY s.UpdatedDate DESC;
```

### View Recent Application Errors
```sql
SELECT TOP 20
    ErrorType,
    ErrorMessage,
    Path,
    Method,
    CreatedDate
FROM log.ApplicationError
ORDER BY CreatedDate DESC;
```

### Check API Request Performance
```sql
SELECT 
    Path,
    COUNT(*) AS RequestCount,
    AVG(DurationMs) AS AvgDurationMs,
    MAX(DurationMs) AS MaxDurationMs
FROM log.ApiRequest
WHERE CreatedDate > DATEADD(HOUR, -1, GETUTCDATE())
GROUP BY Path
ORDER BY AvgDurationMs DESC;
```

---

## Support Contacts

**Development Team Lead:**
- Name: [Developer Name]
- Email: dev@eventlead.com
- Phone: [Phone Number]

**Product Owner:**
- Name: Tony (User)
- Email: [Email]

**Technical Support:**
- Email: support@eventlead.com
- Slack: #eventlead-support

---

**Document Version:** 1.0  
**Last Updated:** October 17, 2025  
**Next Review:** After UAT completion

