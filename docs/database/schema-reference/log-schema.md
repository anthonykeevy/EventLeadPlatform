# `log` Schema - Technical Logging

**Schema Purpose:** Application logging for debugging, monitoring, and diagnostics  
**Table Count:** 4  
**Retention:** 90 days, then archive or delete  
**Backup Priority:** MEDIUM (can be rebuilt from application logs if needed)  
**Write Volume:** VERY HIGH (every API request logged)

---

## Schema Overview

The `log` schema provides technical logs for debugging, monitoring, and performance analysis. These logs are HIGH volume and SHORT retention (unlike `audit` tables which are compliance-focused with 7-year retention).

**Key Differences: `log` vs `audit`:**
- **`log`:** Technical/diagnostic (API requests, errors, auth attempts) - 90-day retention
- **`audit`:** Business/compliance (user actions, role changes) - 7-year retention

---

## Table Overview

| # | Table | Purpose | Write Volume | Retention |
|---|-------|---------|--------------|-----------|
| 1 | `ApiRequest` | HTTP request/response logging | VERY HIGH (every request) | 90 days |
| 2 | `AuthEvent` | Authentication events (login, logout) | MEDIUM | 90 days |
| 3 | `ApplicationError` | Application errors (exceptions, 500s) | LOW (errors only) | 90 days |
| 4 | `EmailDelivery` | Email delivery tracking | MEDIUM | 90 days |

---

## 1. `log.ApiRequest` - HTTP Request/Response Logging

**Purpose:** Log all HTTP API requests for debugging, monitoring, and performance analysis

**What Gets Logged:**
- Every API request (method, path, query params)
- Request headers (User-Agent, Authorization presence)
- Request body size (not full body for privacy)
- Response status code
- Response time (ms)
- User context (UserID, CompanyID)

**Primary Key:** `ApiRequestID` (BIGINT IDENTITY)

**Foreign Keys:**
- `UserID` → `dbo.User.UserID` (NULL for unauthenticated requests)
- `CompanyID` → `dbo.Company.CompanyID` (NULL for unauthenticated or system requests)

**Key Columns:**
- `RequestID` (NVARCHAR(100)) - Unique correlation ID (UUID)
- `Method` (NVARCHAR(10)) - HTTP method (GET, POST, PUT, DELETE)
- `Path` (NVARCHAR(500)) - API endpoint path
- `QueryParams` (NVARCHAR(MAX)) - Query string
- `RequestHeaders` (NVARCHAR(MAX)) - JSON (excluding sensitive headers)
- `RequestBodySize` (INT) - Size in bytes (for monitoring)
- `StatusCode` (INT) - HTTP response status code
- `ResponseBodySize` (INT) - Size in bytes
- `DurationMs` (INT) - Response time in milliseconds
- `UserID`, `CompanyID` - User context (NULL if unauthenticated)
- `IPAddress` (NVARCHAR(50)) - Hashed client IP
- `UserAgent` (NVARCHAR(500)) - Browser/device info
- `CreatedDate` (DATETIME2) - When request occurred

**Indexes:**
- `IX_ApiRequest_CreatedDate` (time-based queries, archiving)
- `IX_ApiRequest_UserID` (find all requests by user)
- `IX_ApiRequest_StatusCode` (filter by error codes)
- `IX_ApiRequest_Path` (find slow endpoints)

**Query Patterns:**
```sql
-- Find slow requests (performance monitoring)
SELECT Path, AVG(DurationMs) as AvgTime, COUNT(*) as RequestCount
FROM log.ApiRequest
WHERE CreatedDate >= DATEADD(DAY, -1, GETUTCDATE())
  AND DurationMs > 100  -- Slow threshold
GROUP BY Path
ORDER BY AvgTime DESC;

-- Error rate by endpoint (reliability monitoring)
SELECT Path, 
    COUNT(*) as TotalRequests,
    SUM(CASE WHEN StatusCode >= 500 THEN 1 ELSE 0 END) as ErrorCount
FROM log.ApiRequest
WHERE CreatedDate >= DATEADD(HOUR, -1, GETUTCDATE())
GROUP BY Path;

-- User's recent API activity (support)
SELECT TOP 100 * 
FROM log.ApiRequest 
WHERE UserID = @user_id 
ORDER BY CreatedDate DESC;
```

**Archiving Strategy:**
```sql
-- Archive logs older than 90 days (move to cold storage)
INSERT INTO log_archive.ApiRequest 
SELECT * FROM log.ApiRequest 
WHERE CreatedDate < DATEADD(DAY, -90, GETUTCDATE());

DELETE FROM log.ApiRequest 
WHERE CreatedDate < DATEADD(DAY, -90, GETUTCDATE());
```

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: log.ApiRequest)

---

## 2. `log.AuthEvent` - Authentication Events

**Purpose:** Log all authentication-related events (login, logout, token refresh)

**What Gets Logged:**
- Login attempts (success/failure)
- Logout events
- Token refresh requests
- Password reset requests
- Email verification attempts
- Account lockout events

**Primary Key:** `AuthEventID` (BIGINT IDENTITY)

**Foreign Keys:**
- `UserID` → `dbo.User.UserID` (NULL for failed logins with invalid email)

**Key Columns:**
- `EventType` (NVARCHAR(50)) - Type of auth event
  - `login.success`
  - `login.failed`
  - `logout`
  - `token.refresh`
  - `password.reset.requested`
  - `password.reset.completed`
  - `email.verification.sent`
  - `email.verification.completed`
  - `account.locked`
  - `account.unlocked`
- `UserID` - User involved (NULL for failed logins)
- `Email` (NVARCHAR(255)) - Email attempted (for failed logins)
- `Reason` (NVARCHAR(255)) - Reason for failure (e.g., "Invalid password", "Account locked")
- `IPAddress` (NVARCHAR(50)) - Hashed client IP
- `UserAgent` (NVARCHAR(500)) - Browser/device info
- `RequestID` (NVARCHAR(100)) - Correlation ID (link to log.ApiRequest)
- `CreatedDate` (DATETIME2) - When event occurred

**Indexes:**
- `IX_AuthEvent_UserID` (find all auth events for user)
- `IX_AuthEvent_Email` (failed login attempts by email)
- `IX_AuthEvent_EventType` (filter by event type)
- `IX_AuthEvent_CreatedDate` (time-based queries, archiving)

**Query Patterns:**
```sql
-- Failed login attempts (security monitoring)
SELECT Email, COUNT(*) as FailedAttempts
FROM log.AuthEvent
WHERE EventType = 'login.failed'
  AND CreatedDate >= DATEADD(HOUR, -1, GETUTCDATE())
GROUP BY Email
HAVING COUNT(*) >= 5;  -- Brute force detection

-- User's auth history (support)
SELECT * 
FROM log.AuthEvent 
WHERE UserID = @user_id 
ORDER BY CreatedDate DESC;

-- Recent account lockouts (security review)
SELECT * 
FROM log.AuthEvent 
WHERE EventType = 'account.locked'
  AND CreatedDate >= DATEADD(DAY, -7, GETUTCDATE())
ORDER BY CreatedDate DESC;
```

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: log.AuthEvent)

---

## 3. `log.ApplicationError` - Application Errors

**Purpose:** Log application exceptions and errors (500s, unhandled exceptions)

**What Gets Logged:**
- Unhandled exceptions
- Database errors
- External API errors (ABR, email delivery, payment processor)
- Validation errors (if deemed critical)

**Primary Key:** `ApplicationErrorID` (BIGINT IDENTITY)

**Foreign Keys:**
- `UserID` → `dbo.User.UserID` (user who triggered error, NULL if system error)
- `CompanyID` → `dbo.Company.CompanyID` (tenant context, NULL if system error)

**Key Columns:**
- `ErrorType` (NVARCHAR(100)) - Type of error (e.g., 'UnhandledException', 'DatabaseError', 'ExternalAPIError')
- `ErrorMessage` (NVARCHAR(MAX)) - Error message
- `StackTrace` (NVARCHAR(MAX)) - Full stack trace
- `Severity` (NVARCHAR(20)) - Severity level ('critical', 'error', 'warning')
- `RequestID` (NVARCHAR(100)) - Correlation ID (link to log.ApiRequest)
- `Path` (NVARCHAR(500)) - API endpoint where error occurred
- `Method` (NVARCHAR(10)) - HTTP method
- `UserID`, `CompanyID` - User/tenant context
- `IPAddress`, `UserAgent` - Client context
- `AdditionalData` (NVARCHAR(MAX)) - JSON with extra context
- `CreatedDate` (DATETIME2) - When error occurred

**Indexes:**
- `IX_ApplicationError_CreatedDate` (time-based queries)
- `IX_ApplicationError_ErrorType` (filter by error type)
- `IX_ApplicationError_Severity` (critical errors only)
- `IX_ApplicationError_Path` (errors by endpoint)

**Query Patterns:**
```sql
-- Critical errors in last hour (alerting)
SELECT * 
FROM log.ApplicationError 
WHERE Severity = 'critical'
  AND CreatedDate >= DATEADD(HOUR, -1, GETUTCDATE())
ORDER BY CreatedDate DESC;

-- Error frequency by endpoint (reliability)
SELECT Path, ErrorType, COUNT(*) as ErrorCount
FROM log.ApplicationError
WHERE CreatedDate >= DATEADD(DAY, -7, GETUTCDATE())
GROUP BY Path, ErrorType
ORDER BY ErrorCount DESC;

-- User's error history (support)
SELECT * 
FROM log.ApplicationError 
WHERE UserID = @user_id 
ORDER BY CreatedDate DESC;
```

**Alerting:**
```python
# Send alert if critical error
if severity == 'critical':
    send_slack_alert(
        channel='#production-alerts',
        message=f"🚨 Critical Error: {error_message}",
        error_id=error_id
    )
```

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: log.ApplicationError)

---

## 4. `log.EmailDelivery` - Email Delivery Tracking

**Purpose:** Track email delivery status (sent, delivered, bounced, opened)

**What Gets Logged:**
- Email verification links sent
- Password reset emails
- Team invitations
- Notifications
- Marketing emails (future)

**Primary Key:** `EmailDeliveryID` (BIGINT IDENTITY)

**Foreign Keys:**
- `UserID` → `dbo.User.UserID` (recipient, NULL for invitations to non-users)
- `CompanyID` → `dbo.Company.CompanyID` (tenant context, NULL for system emails)

**Key Columns:**
- `EmailType` (NVARCHAR(50)) - Type of email
  - `verification`
  - `password_reset`
  - `invitation`
  - `notification`
- `RecipientEmail` (NVARCHAR(255)) - Email address (hashed or encrypted for privacy)
- `Subject` (NVARCHAR(255)) - Email subject line
- `TemplateID` (NVARCHAR(100)) - Email template identifier
- `Status` (NVARCHAR(50)) - Delivery status
  - `pending` - Queued for sending
  - `sent` - Sent to email provider
  - `delivered` - Provider confirmed delivery
  - `bounced` - Bounced (invalid email)
  - `opened` - Recipient opened email (tracking pixel)
  - `clicked` - Recipient clicked link
  - `failed` - Failed to send (provider error)
- `ProviderMessageID` (NVARCHAR(255)) - External provider's message ID (for tracking)
- `ErrorMessage` (NVARCHAR(MAX)) - Error message (if failed/bounced)
- `SentAt` (DATETIME2) - When sent to provider
- `DeliveredAt` (DATETIME2) - When provider confirmed delivery
- `OpenedAt` (DATETIME2) - When recipient opened (if tracked)
- `ClickedAt` (DATETIME2) - When recipient clicked link
- `UserID`, `CompanyID` - User/tenant context
- `CreatedDate` (DATETIME2) - When email was queued

**Indexes:**
- `IX_EmailDelivery_RecipientEmail` (find emails sent to address)
- `IX_EmailDelivery_Status` (filter by delivery status)
- `IX_EmailDelivery_EmailType` (filter by email type)
- `IX_EmailDelivery_CreatedDate` (time-based queries, archiving)

**Query Patterns:**
```sql
-- Bounced emails (invalid addresses)
SELECT RecipientEmail, COUNT(*) as BounceCount
FROM log.EmailDelivery
WHERE Status = 'bounced'
  AND CreatedDate >= DATEADD(DAY, -30, GETUTCDATE())
GROUP BY RecipientEmail
ORDER BY BounceCount DESC;

-- Email delivery rate (reliability)
SELECT 
    EmailType,
    COUNT(*) as TotalSent,
    SUM(CASE WHEN Status = 'delivered' THEN 1 ELSE 0 END) as Delivered,
    SUM(CASE WHEN Status = 'bounced' THEN 1 ELSE 0 END) as Bounced,
    SUM(CASE WHEN Status = 'failed' THEN 1 ELSE 0 END) as Failed
FROM log.EmailDelivery
WHERE CreatedDate >= DATEADD(DAY, -7, GETUTCDATE())
GROUP BY EmailType;

-- User's email history (support)
SELECT * 
FROM log.EmailDelivery 
WHERE RecipientEmail = @email 
ORDER BY CreatedDate DESC;
```

**Full SQL Definition:** See `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` (Section: log.EmailDelivery)

---

## Common Patterns

### **Request ID (Correlation)**

Every log entry should include a `RequestID` to correlate logs across tables:

```python
# Generate unique request ID
request_id = str(uuid.uuid4())

# Log API request
log_api_request(request_id=request_id, ...)

# If error occurs
log_application_error(request_id=request_id, ...)

# If auth event
log_auth_event(request_id=request_id, ...)
```

**Query across tables:**
```sql
-- Find all logs related to a request
SELECT 'ApiRequest' as LogType, * FROM log.ApiRequest WHERE RequestID = @request_id
UNION ALL
SELECT 'AuthEvent' as LogType, * FROM log.AuthEvent WHERE RequestID = @request_id
UNION ALL
SELECT 'ApplicationError' as LogType, * FROM log.ApplicationError WHERE RequestID = @request_id;
```

---

### **Archiving Strategy**

**Problem:** Log tables grow very fast (millions of rows per month)

**Solution:** Aggressive archiving

```sql
-- Archive logs older than 90 days
CREATE PROCEDURE sp_ArchiveLogs
AS
BEGIN
    -- Move to cold storage (S3, Azure Blob)
    INSERT INTO log_archive.ApiRequest SELECT * FROM log.ApiRequest WHERE CreatedDate < DATEADD(DAY, -90, GETUTCDATE());
    INSERT INTO log_archive.AuthEvent SELECT * FROM log.AuthEvent WHERE CreatedDate < DATEADD(DAY, -90, GETUTCDATE());
    INSERT INTO log_archive.ApplicationError SELECT * FROM log.ApplicationError WHERE CreatedDate < DATEADD(DAY, -90, GETUTCDATE());
    INSERT INTO log_archive.EmailDelivery SELECT * FROM log.EmailDelivery WHERE CreatedDate < DATEADD(DAY, -90, GETUTCDATE());
    
    -- Delete from active tables
    DELETE FROM log.ApiRequest WHERE CreatedDate < DATEADD(DAY, -90, GETUTCDATE());
    DELETE FROM log.AuthEvent WHERE CreatedDate < DATEADD(DAY, -90, GETUTCDATE());
    DELETE FROM log.ApplicationError WHERE CreatedDate < DATEADD(DAY, -90, GETUTCDATE());
    DELETE FROM log.EmailDelivery WHERE CreatedDate < DATEADD(DAY, -90, GETUTCDATE());
END;

-- Schedule: Run daily at 2 AM (low traffic)
```

---

### **Performance Optimization**

**Write Optimization:**
- Logging should NEVER slow down application requests
- Use async logging (queue + background worker)
- Batch inserts (insert 100 records at once)
- Minimize indexes (only essential ones)

```python
# Async logging pattern
from queue import Queue
import threading

log_queue = Queue()

def log_worker():
    """Background worker that batches log inserts"""
    batch = []
    while True:
        log_entry = log_queue.get()
        batch.append(log_entry)
        
        if len(batch) >= 100:  # Batch size
            # Bulk insert to database
            db.bulk_insert_mappings(ApiRequest, batch)
            db.commit()
            batch = []

# Start background worker
threading.Thread(target=log_worker, daemon=True).start()

# Application code (non-blocking)
log_queue.put({
    'request_id': request_id,
    'method': 'GET',
    'path': '/api/users/123',
    'status_code': 200,
    'duration_ms': 45
})
```

---

### **Privacy Considerations**

**Problem:** Logs may contain PII (email, IP address, user agent)

**Solutions:**
1. **Hash IP addresses** (cannot be reversed, but can detect duplicate IPs)
2. **Truncate sensitive fields** (store first 3 chars of email)
3. **Aggregate before archiving** (store only counts, not individual records)

```python
import hashlib

def hash_ip(ip_address: str) -> str:
    """Hash IP address for privacy"""
    return hashlib.sha256(ip_address.encode()).hexdigest()[:16]

def anonymize_email(email: str) -> str:
    """Partially redact email for privacy"""
    local, domain = email.split('@')
    return f"{local[:3]}***@{domain}"
```

---

## Alerting & Monitoring

### **Critical Alerts (Real-Time)**

- Error rate > 5% for any endpoint
- Critical error (severity = 'critical')
- API latency > 1 second (P95)
- Failed login attempts > 10 in 5 minutes (brute force)
- Email bounce rate > 10%

### **Daily Reports**

- Top 10 slowest endpoints
- Error summary by type
- Failed login summary by email
- Email delivery rates

---

## Related Documentation

**Architecture:**
- `docs/solution-architecture.md` - API Architecture section
- `docs/architecture/decisions/ADR-001-database-schema-organization.md`

**Database:**
- `docs/database/REBUILD-PLAN-SUMMARY.md`
- `docs/DATABASE-REBUILD-PLAN-EPIC-1-2025-10-16.md` - Full SQL definitions

---

**Winston** 🏗️  
*"Logs are breadcrumbs. They lead you to the bug."*

