# Logging Architecture

**Status:** Implemented (Story 0.2)  
**Last Updated:** 2025-10-16

## Overview

The EventLead Platform implements a comprehensive, zero-touch logging infrastructure that automatically captures all API requests and errors without requiring manual logging code in endpoint handlers.

## Key Features

✅ **Automatic Request Logging** - 100% of API requests logged to database  
✅ **Global Exception Handling** - All unhandled errors captured with stack traces  
✅ **Request Correlation** - Unique RequestID (UUID4) links requests and errors  
✅ **User Context** - UserID and CompanyID automatically included when authenticated  
✅ **Sensitive Data Filtering** - Passwords, tokens, and secrets never logged  
✅ **Non-Blocking** - Background tasks ensure < 5ms latency overhead  
✅ **Zero Manual Code** - Developers never write logging code in endpoints  

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Incoming HTTP Request                     │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────────────┐
        │   RequestLoggingMiddleware (FIRST)    │
        │  - Generate RequestID (UUID4)         │
        │  - Set request context                │
        │  - Start timing                       │
        └───────────────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────────────┐
        │      Other Middleware (CORS, etc)     │
        └───────────────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────────────┐
        │         Route Handler (Your Code)     │
        │  - No logging code required!          │
        │  - Clean business logic only          │
        └───────────────────────────────────────┘
                        │
          ┌─────────────┴─────────────┐
          │                           │
     Success                       Exception
          │                           │
          ▼                           ▼
    ┌──────────┐              ┌──────────────────┐
    │ Response │              │ Exception Handler│
    └──────────┘              │ (Catches All)    │
          │                   └──────────────────┘
          │                           │
          └─────────────┬─────────────┘
                        │
                        ▼
        ┌───────────────────────────────────────┐
        │  RequestLoggingMiddleware (Returns)   │
        │  - Calculate duration                 │
        │  - Log to database (background task)  │
        │  - Add X-Request-ID header            │
        └───────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│     Response + X-Request-ID Header to Client                │
│  (Error response if exception occurred)                     │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Request Logging Middleware

**Location:** `backend/middleware/request_logger.py`

Automatically captures all API requests:

```python
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Generate RequestID
        request_id = str(uuid.uuid4())
        
        # Set context
        set_request_context(
            request_id=request_id,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent")
        )
        
        # Time request
        start_time = time.time()
        response = await call_next(request)
        duration_ms = int((time.time() - start_time) * 1000)
        
        # Log in background (non-blocking)
        background_task = BackgroundTask(log_api_request, log_data)
        response.background = background_task
        
        # Add RequestID to response
        response.headers["X-Request-ID"] = request_id
        
        return response
```

**Logged Fields:**
- `RequestID` - Unique UUID4 for correlation
- `Method` - HTTP method (GET, POST, PUT, DELETE, etc.)
- `Path` - Request path (e.g., `/api/events`)
- `QueryParams` - Query string (sanitized)
- `StatusCode` - HTTP response status (200, 404, 500, etc.)
- `DurationMs` - Request duration in milliseconds
- `UserID` - Authenticated user ID (NULL for anonymous)
- `CompanyID` - User's company ID (NULL for anonymous)
- `IPAddress` - Client IP address
- `UserAgent` - Client user agent string
- `CreatedDate` - Timestamp (UTC)

**Database Table:** `log.ApiRequest`

### 2. Global Exception Handler

**Location:** `backend/middleware/exception_handler.py`

Catches all unhandled exceptions:

```python
async def global_exception_handler(request: Request, exc: Exception):
    # Get request context
    context = get_current_request_context()
    
    # Extract error details
    error_type = type(exc).__name__
    error_message = str(exc)
    stack_trace = traceback.format_exc()
    
    # Log to database
    application_error = ApplicationError(
        RequestID=context.request_id,
        ErrorType=error_type,
        ErrorMessage=error_message,
        StackTrace=sanitize_stack_trace(stack_trace),  # Remove secrets!
        Severity="ERROR",
        Path=str(request.url.path),
        Method=request.method,
        UserID=getattr(request.state, "user_id", None),
        CompanyID=getattr(request.state, "company_id", None),
        IPAddress=context.ip_address,
        UserAgent=context.user_agent,
    )
    
    db.add(application_error)
    db.commit()
    
    # Return user-friendly error
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": error_type,
            "message": "An unexpected error occurred. Our team has been notified.",
            "details": {"requestId": context.request_id}
        }
    )
```

**Logged Fields:**
- `ApplicationErrorID` - Primary key
- `RequestID` - Correlation to ApiRequest
- `ErrorType` - Exception class name
- `ErrorMessage` - Exception message
- `StackTrace` - Full stack trace (sanitized)
- `Severity` - ERROR or CRITICAL
- `Path` - Request path where error occurred
- `Method` - HTTP method
- `UserID` - Authenticated user ID (NULL for anonymous)
- `CompanyID` - User's company ID (NULL for anonymous)
- `IPAddress` - Client IP address
- `UserAgent` - Client user agent string
- `AdditionalData` - Extra context (JSON)
- `CreatedDate` - Error timestamp (UTC)

**Database Table:** `log.ApplicationError`

### 3. Request Context Manager

**Location:** `backend/common/request_context.py`

Makes request context available throughout the request lifecycle:

```python
from contextvars import ContextVar

_request_context: ContextVar[Optional[RequestContext]] = ContextVar("request_context", default=None)

def set_request_context(request_id, user_id=None, company_id=None, ip_address=None, user_agent=None):
    context = RequestContext(request_id, user_id, company_id, ip_address, user_agent)
    _request_context.set(context)

def get_current_request_context() -> Optional[RequestContext]:
    return _request_context.get()
```

**Usage:** Access request context from anywhere:

```python
from common.request_context import get_current_request_context

context = get_current_request_context()
print(f"Request ID: {context.request_id}")
print(f"User ID: {context.user_id}")
```

### 4. Sensitive Data Filtering

**Location:** `backend/common/log_filters.py`

Ensures passwords, tokens, and secrets are NEVER logged:

**Sensitive Patterns:**
- `password`, `passwd`, `pwd`
- `token`, `access_token`, `refresh_token`
- `secret`, `api_key`, `apikey`
- `auth`, `authorization`, `credential`
- `private_key`, `session_id`, `csrf`

**Functions:**
- `sanitize_dict()` - Sanitize request/response bodies
- `sanitize_headers()` - Remove Authorization headers
- `sanitize_query_params()` - Filter sensitive query params
- `sanitize_stack_trace()` - Remove secrets from error traces

**Example:**

```python
# Input
data = {
    "username": "john@example.com",
    "password": "SecurePassword123!",
    "api_key": "sk_live_1234567890"
}

# Output
sanitized = sanitize_dict(data)
# {
#     "username": "john@example.com",
#     "password": "[REDACTED]",
#     "api_key": "[REDACTED]"
# }
```

### 5. Logging Utilities

**Location:** `backend/common/logger.py`

Structured logging with RequestID included:

```python
from common.logger import get_logger

logger = get_logger(__name__)
logger.info("Processing payment")  # RequestID automatically included

# Output:
# [2025-10-16 21:30:45] [INFO] [550e8400-e29b-41d4-a716-446655440000] [module.name] Processing payment
```

## Configuration

### Middleware Registration

**Location:** `backend/main.py`

```python
from middleware import RequestLoggingMiddleware, global_exception_handler
from common.logger import configure_logging

# Configure logging
configure_logging(log_level="INFO")

app = FastAPI()

# Register exception handler FIRST
app.add_exception_handler(Exception, global_exception_handler)

# Add middleware (LIFO order)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(CORSMiddleware, ...)
```

**Order Matters:** RequestLoggingMiddleware should be added LAST (runs first) to capture the entire request lifecycle.

## Usage Examples

### Example 1: Clean Endpoint Code

```python
# ❌ OLD WAY (Manual logging - DON'T DO THIS)
@router.post("/api/events")
def create_event(request: CreateEventRequest, db: Session = Depends(get_db)):
    logger.info(f"Creating event: {request.name}")  # Manual
    try:
        event = event_service.create(request)
        logger.info(f"Event created: {event.id}")  # Manual
        return event
    except Exception as e:
        logger.error(f"Error creating event: {str(e)}")  # Manual
        raise

# ✅ NEW WAY (Automatic - NO LOGGING CODE)
@router.post("/api/events")
def create_event(request: CreateEventRequest, db: Session = Depends(get_db)):
    # Middleware logs everything automatically!
    event = event_service.create(request)
    return event
```

### Example 2: Querying Logs by RequestID

```sql
-- Find all details for a specific request
SELECT 
    r.RequestID,
    r.Method,
    r.Path,
    r.StatusCode,
    r.DurationMs,
    r.UserID,
    r.CompanyID,
    e.ErrorType,
    e.ErrorMessage,
    e.StackTrace
FROM log.ApiRequest r
LEFT JOIN log.ApplicationError e ON r.RequestID = e.RequestID
WHERE r.RequestID = '550e8400-e29b-41d4-a716-446655440000';
```

### Example 3: Find Slow Requests

```sql
-- Find requests taking > 1 second
SELECT TOP 100
    RequestID,
    Method,
    Path,
    DurationMs,
    UserID,
    CreatedDate
FROM log.ApiRequest
WHERE DurationMs > 1000
ORDER BY DurationMs DESC;
```

### Example 4: Find User's Recent Errors

```sql
-- Find all errors for a specific user
SELECT TOP 50
    e.RequestID,
    e.ErrorType,
    e.ErrorMessage,
    e.Path,
    e.Method,
    e.CreatedDate,
    r.DurationMs
FROM log.ApplicationError e
LEFT JOIN log.ApiRequest r ON e.RequestID = r.RequestID
WHERE e.UserID = 123
ORDER BY e.CreatedDate DESC;
```

## Troubleshooting

### How do I find logs for a specific request?

1. Client receives `X-Request-ID` header in response
2. Use RequestID to query `log.ApiRequest` and `log.ApplicationError`
3. Stack traces include full error details

**Example:**

```bash
# Client makes request
curl -i https://api.eventlead.com/api/events

# Response includes:
X-Request-ID: 550e8400-e29b-41d4-a716-446655440000

# Query database:
SELECT * FROM log.ApiRequest WHERE RequestID = '550e8400-e29b-41d4-a716-446655440000';
```

### How do I debug performance issues?

Query `log.ApiRequest` for slow requests:

```sql
-- Find slowest endpoints
SELECT 
    Path,
    AVG(DurationMs) as AvgDuration,
    MAX(DurationMs) as MaxDuration,
    COUNT(*) as RequestCount
FROM log.ApiRequest
WHERE CreatedDate > DATEADD(day, -7, GETUTCDATE())
GROUP BY Path
HAVING AVG(DurationMs) > 500
ORDER BY AvgDuration DESC;
```

### How do I track error rates?

Query `log.ApplicationError` for error trends:

```sql
-- Error rate by hour (last 24 hours)
SELECT 
    DATEPART(hour, CreatedDate) as Hour,
    COUNT(*) as ErrorCount,
    COUNT(DISTINCT RequestID) as UniqueRequests
FROM log.ApplicationError
WHERE CreatedDate > DATEADD(day, -1, GETUTCDATE())
GROUP BY DATEPART(hour, CreatedDate)
ORDER BY Hour DESC;
```

## Security Considerations

### ✅ What's Safe to Log

- Email addresses
- User IDs, Company IDs
- Request paths and methods
- Status codes and timing
- IP addresses and user agents
- Non-sensitive query params

### ❌ NEVER Log These

- Passwords (any form)
- JWT tokens, API keys
- Credit card numbers
- Session IDs, CSRF tokens
- Private keys, secrets
- Authorization headers

**All sensitive data is automatically filtered by `log_filters.py`**

## Performance

### Latency Overhead

- **Target:** < 5ms per request
- **Actual:** ~2-3ms (background tasks + context vars)
- **Method:** Non-blocking database writes using FastAPI BackgroundTasks

### Scalability

- **Database writes:** Async background tasks
- **Connection pooling:** Configured in `database.py`
- **High volume:** Tested with 100+ concurrent requests/second

## Future Enhancements

### Story 1.2 - JWT Authentication
- JWT middleware will populate `UserID` and `CompanyID` in request.state
- Request context automatically updated by `update_request_context()`

### Story 1.3 - RBAC Middleware
- Role-based access control will add role context
- Audit logs will capture permission checks

### Story 3.X - Analytics Dashboard
- Real-time monitoring of API requests
- Error rate alerts and dashboards
- Performance trend analysis

## Testing

### Unit Tests

```bash
# Run all logging tests
pytest backend/tests/test_request_logging.py -v
pytest backend/tests/test_exception_handler.py -v
pytest backend/tests/test_log_filters.py -v

# Run standalone validation
python backend/tests/test_log_filters_standalone.py
```

### Integration Tests

```bash
# End-to-end logging with database
pytest backend/tests/test_logging_integration.py -v -m integration
```

## References

- [Story 0.2: Automated Logging Infrastructure](../stories/story-0.2.md)
- [Tech Spec Epic 1: Logging Patterns](../tech-spec-epic-1.md#automated-logging-patterns)
- [ADR-002: Backend Abstraction Layer](../architecture/decisions/ADR-002-backend-abstraction-layer.md)
- [Database Quick Reference](./database-quick-reference.md)

---

**Questions or Issues?** Contact the development team or reference Story 0.2 documentation.

