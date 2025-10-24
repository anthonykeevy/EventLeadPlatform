# EventLead Platform - Troubleshooting Guide

## Diagnostic Tool: `diagnostic_logs.py` ✅ WORKING

**Purpose:** Extract recent log entries from all log tables for troubleshooting authentication and application errors.

**Usage:**
```powershell
cd backend
python diagnostic_logs.py [limit]
```

**Parameters:**
- `limit` (optional): Number of recent entries to show (default: 10)

**Example:**
```powershell
python diagnostic_logs.py 5  # Show last 5 entries from each log table
```

**Output:**
The tool displays:
1. **Recent Auth Events** - Authentication attempts (login, signup, password reset, etc.)
2. **Recent Application Errors** - All application errors captured by global exception handler
3. **Recent API Requests** - All API requests with status codes and duration
4. **Correlation View** - Links related logs by RequestID for failed requests

**Note:** Backend services must be running for the tool to connect to the database.

**Fix Applied (Oct 21, 2025):**
- Updated to use backend's database connection instead of building connection string manually
- Now imports `engine` from `common.database` for consistency with API

---

## Story 1.9 UAT Issues - Resolution Log

### Issue 1: Missing `AuthEvent` Logs ✅ FIXED

**Problem:**  
- `log.AuthEvent` entries were not being created during signup/login attempts
- Only `log.ApplicationError` and `log.ApiRequest` were populated

**Root Cause:**  
The `log_auth_event()` function in `audit_service.py` was trying to use columns that don't exist in the `AuthEvent` model:
- ❌ `EventStatus` (doesn't exist)
- ❌ `Details` (doesn't exist)
- ✅ `EventType` (correct)
- ✅ `Reason` (correct)

**Fix Applied:**
Updated `backend/modules/auth/audit_service.py`:
```python
# OLD (incorrect):
auth_event = AuthEvent(
    EventType=event_type,
    EventStatus="SUCCESS" if success else "FAILURE",  # ❌ Column doesn't exist
    Details=json.dumps(details),  # ❌ Column doesn't exist
    ...
)

# NEW (correct):
auth_event = AuthEvent(
    EventType=event_type,  # Use event type like "LOGIN_FAILED"
    Reason=json.dumps(details),  # Store details in Reason field
    Email=details.get("email") if details else None,  # Extract email
    ...
)
```

**Files Changed:**
- `backend/modules/auth/audit_service.py`

---

### Issue 2: Password Validation TypeError ✅ FIXED

**Problem:**  
Signup was failing with:
```
TypeError: validate_password_strength() missing 1 required positional argument: 'password'
```

**Root Cause:**  
Story 1.13 updated `validate_password_strength()` to require a `db` session parameter (for reading configurable password rules from the database), but the auth router was still calling it with only the password.

**Function Signature:**
```python
# Story 1.13 signature:
def validate_password_strength(db: Session, password: str) -> List[str]:
    """Validate password using configurable rules from database"""
```

**Fix Applied:**
Updated all 3 occurrences in `backend/modules/auth/router.py`:
```python
# OLD (incorrect):
password_errors = validate_password_strength(request_data.password)

# NEW (correct):
password_errors = validate_password_strength(db, request_data.password)
```

**Locations Fixed:**
1. Signup endpoint (invitation-based) - Line 133
2. Signup endpoint (regular) - Line 196
3. Password reset endpoint - Line 779

**Files Changed:**
- `backend/modules/auth/router.py`

---

## Testing After Fixes

1. **Start Backend Services:**
   ```powershell
   .\scripts\start-services-clean.ps1
   ```

2. **Test Signup:**
   - Navigate to `http://localhost:5173/signup`
   - Enter test email and password
   - Submit form

3. **Verify Logs:**
   ```powershell
   cd backend
   python diagnostic_logs.py 3
   ```

4. **Expected Results:**
   - ✅ `log.AuthEvent` entry with `EventType = "SIGNUP"` or `"SIGNUP_FAILED"`
   - ✅ `log.ApplicationError` entry (if signup failed)
   - ✅ `log.ApiRequest` entry with status code and duration
   - ✅ All three logs linked by same `RequestID`

---

### Issue 3: Column Name Mismatches in User Model ✅ FIXED

**Problem:**  
Multiple TypeError exceptions during signup due to using incorrect column names when creating/updating User records.

**Errors Found:**
1. `'EmailVerified' is an invalid keyword argument for User` - Should be `IsEmailVerified`
2. `'IsActive' is an invalid keyword argument for User` - Should use `StatusID` (Foreign key to UserStatus table)
3. `generate_verification_token() got an unexpected keyword argument 'expiry_hours'` - Function reads expiry from database config

**Root Cause:**  
Code was using incorrect column names that didn't match the actual User model schema:
- User model has `IsEmailVerified`, not `EmailVerified`
- User model has `StatusID` (FK to UserStatus), not `IsActive`  
- Verification token expiry is configured in database (Story 1.13), not passed as parameter

**Fix Applied:**
Updated `backend/modules/auth/user_service.py`:
```python
# Fixed column names:
- EmailVerified → IsEmailVerified
- IsActive → StatusID
- UserStatusID → StatusID (correct column name)

# Fixed create_user():
user = User(
    IsEmailVerified=False,  # Not EmailVerified
    StatusID=pending_status.UserStatusID,  # Not IsActive or UserStatusID
    ...
)

# Fixed verify_email():
user.IsEmailVerified = True  # Not EmailVerified  
user.StatusID = active_status.UserStatusID  # Not IsActive
```

Updated `backend/modules/auth/router.py`:
```python
# Fixed token generation call:
token = generate_verification_token(db, user.UserID)  # Removed expiry_hours parameter

# Fixed status checks:
if user.status and user.status.StatusName not in ["Active"]:  # Not user.IsActive
```

**Files Changed:**
- `backend/modules/auth/user_service.py`
- `backend/modules/auth/router.py`
- `backend/modules/auth/audit_service.py`

---

### Issue 4: Response Format Mismatch (Backend/Frontend) ✅ FIXED

**Problem:**  
Frontend showing "Connection error" and "An error occurred" even though backend was returning HTTP 400 with specific error messages like "Email already registered".

**Root Cause:**  
The global exception handler was returning error messages in a custom format that didn't match what the frontend expected:

```python
# Backend was returning:
{
  "success": false,
  "error": "HTTPException",
  "message": "Email already registered...",  # ❌ Frontend doesn't read 'message'
  "details": { "requestId": "..." }
}

# Frontend was expecting FastAPI standard:
{
  "detail": "Email already registered..."  # ✅ Frontend reads 'detail'
}
```

The frontend's `authApi.ts` tries to access `axiosError.response?.data?.detail`, but the backend was using `message` instead, causing `detail` to be `undefined` and triggering generic error messages.

**Fix Applied:**
Updated `backend/middleware/exception_handler.py` to use FastAPI's standard `detail` field:
```python
# HTTPException responses:
return JSONResponse(
    status_code=exc.status_code,
    content={
        "detail": exc.detail,  # FastAPI standard field
        "requestId": request_id,
    },
)

# System error responses:
return JSONResponse(
    status_code=500,
    content={
        "detail": "An unexpected error occurred. Our team has been notified.",
        "requestId": request_id,
    },
)
```

**Files Changed:**
- `backend/middleware/exception_handler.py`

---

### Issue 5: Frontend Password Error Message Override ✅ FIXED

**Problem:**  
Frontend was displaying generic password requirement messages even when the backend provided specific, actionable error messages.

**Root Cause:**  
The `formatAuthError()` function in `frontend/src/features/auth/api/authApi.ts` was checking if the error detail contained "password requirements" and replacing the backend's detailed message with a generic frontend message.

**Example:**
```
Backend sends: "Password does not meet security requirements: Password must be at least 8 characters long"
Frontend showed: "Password must be at least 8 characters with uppercase, lowercase, number, and special character."
```

**Fix Applied:**
Updated `frontend/src/features/auth/api/authApi.ts` to pass through the backend's specific error message:
```typescript
// OLD (incorrect):
if (detail.includes('weak password') || detail.includes('password requirements')) {
  return new Error('Password must be at least 8 characters with uppercase, lowercase, number, and special character.')
}

// NEW (correct):
if (detail.includes('Password does not meet security requirements')) {
  return new Error(detail) // Use backend's detailed message
}
```

**Result:**
Users now see specific, actionable error messages that tell them exactly what's wrong with their password based on the configurable password rules from the database (Story 1.13).

**Files Changed:**
- `frontend/src/features/auth/api/authApi.ts`

---

### Issue 6: Transaction Boundary Violation (User created even if email fails) ✅ FIXED

**Problem:**  
Users were being committed to the database even when verification email failed to send, leaving users in an invalid state (registered but can't verify email).

**Example:**
- User submits signup form
- `create_user()` commits user to DB
- Email send fails (e.g., SMTP error, wrong parameters)
- User exists in DB but has no verification email
- User can't login (not verified) and can't get verification email

**Root Cause:**  
Transaction boundary was incorrectly placed. The signup flow was:
1. `create_user()` → commits immediately ✅
2. `generate_verification_token()` → commits immediately ✅  
3. Send email → if fails, user already committed ❌

This violated ACID principles - the entire signup should be atomic.

**Fix Applied:**
Refactored to use proper transaction management with rollback on failure:

**Updated `backend/modules/auth/user_service.py`:**
```python
def create_user(..., auto_commit: bool = True) -> User:
    db.add(user)
    if auto_commit:
        db.commit()
    else:
        db.flush()  # Get UserID without committing
    return user
```

**Updated `backend/modules/auth/token_service.py`:**
```python
def generate_verification_token(..., auto_commit: bool = True) -> str:
    db.add(token)
    if auto_commit:
        db.commit()
    else:
        db.flush()  # Generate TokenID without committing
    return token_value
```

**Updated `backend/modules/auth/router.py`:**
```python
# Create user (don't commit yet)
user = create_user(db, ..., auto_commit=False)

try:
    # Generate token (don't commit yet)
    token = generate_verification_token(db, user.UserID, auto_commit=False)
    
    # Send email (if fails, exception raised)
    await email_service.send_email(...)
    
    # Log audit
    log_user_creation(db, user.UserID, user.Email)
    
    # Everything succeeded - commit the transaction
    db.commit()
    
except Exception as error:
    # Email send failed - rollback everything
    db.rollback()
    raise HTTPException(500, "Failed to send verification email...")
```

**Result:**
- If email send fails, user is NOT created in database
- User can retry signup without "email already registered" error
- Maintains data integrity and ACID compliance

**Files Changed:**
- `backend/modules/auth/user_service.py`
- `backend/modules/auth/token_service.py`
- `backend/modules/auth/router.py`

---

### Issue 7: Email Service Parameter Mismatch ✅ FIXED

**Problem:**  
`EmailService.send_email()` being called with parameters `email_type` and `user_id` that don't exist in the function signature.

**Error:**
```
TypeError: EmailService.send_email() got an unexpected keyword argument 'email_type'
```

**Fix Applied:**
Removed the extra parameters from the signup endpoint. The email service doesn't need these for sending emails.

**Files Changed:**
- `backend/modules/auth/router.py`

---

## Related Documentation

- **Story 0.2:** Global Logging Infrastructure (`docs/stories/story-0.2.md`)
- **Story 1.9:** Frontend Authentication (`docs/stories/story-1.9.md`)
- **Story 1.13:** Password Configuration (`docs/stories/story-1.13.md`)
- **Service Management:** `docs/SERVICE-MANAGEMENT-GUIDE.md`

---

## Common Issues

### Issue: "Connection error" on frontend
**Cause:** Generic error message when backend validation fails  
**Resolution:** Check `log.ApplicationError` and `log.AuthEvent` for specific error details using `diagnostic_logs.py`

### Issue: No logs appearing
**Cause:** Backend services not running or database connection issue  
**Resolution:** 
1. Check services: `.\scripts\simple-monitor.ps1`
2. Check logs: `.\scripts\view-logs.ps1`
3. Verify database connection in `backend/.env`

### Issue: Password validation always fails
**Cause:** Missing or incorrect `db` parameter in `validate_password_strength()` call  
**Resolution:** Ensure all calls include `db` as first parameter: `validate_password_strength(db, password)`

---

*Last Updated: October 21, 2025*
*Story: 1.9 UAT - Signup & Login*

