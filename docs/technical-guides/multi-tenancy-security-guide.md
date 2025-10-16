**# Multi-Tenant Data Isolation & Security Guide (Story 1.8)

## Overview

This guide documents the multi-tenant data isolation architecture, security patterns, and testing strategies for the EventLead platform. All company-scoped data is isolated using JWT-based company filtering.

## Architecture

### Multi-Tenancy Model

EventLead uses a **shared database, shared schema** multi-tenancy model with **row-level isolation**:

- **Single Database**: All companies share the same database
- **Shared Schema**: All companies use the same table structure
- **Row-Level Isolation**: `CompanyID` column filters data per company
- **JWT-Based Context**: Company ID stored in JWT, not request body

### Key Principles

1. **JWT is Source of Truth**: Company ID always comes from JWT, never from user input
2. **Filter Every Query**: All company-scoped queries MUST filter by `company_id`
3. **Verify Company Match**: Path parameters with `company_id` must match JWT `company_id`
4. **Role-Based Access**: Combine company filtering with role checks (`company_admin`, `company_user`)
5. **Audit Cross-Company Attempts**: Log all denied cross-company access attempts

## Implementation Patterns

### Pattern 1: Basic Company Filtering

```python
from common.multi_tenant import filter_by_company

@router.get("/events")
async def get_events(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Apply company filter
    query = db.query(Event)
    query = filter_by_company(query, current_user.company_id)
    events = query.all()
    return events
```

### Pattern 2: Verify Company Access for Specific Resource

```python
from common.multi_tenant import verify_company_access

@router.get("/events/{event_id}")
async def get_event(
    event_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get event
    event = db.query(Event).filter(Event.EventID == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Verify company access
    verify_company_access(
        resource_company_id=event.CompanyID,
        user_company_id=current_user.company_id,
        resource_type="Event"
    )
    
    return event
```

### Pattern 3: Verify Path Company Matches User

```python
from common.multi_tenant import verify_path_company_matches_user

@router.post("/companies/{company_id}/events")
async def create_event(
    company_id: int,
    event_data: CreateEventRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify company_id in path matches user's company
    verify_path_company_matches_user(company_id, current_user.company_id)
    
    # Create event
    event = Event(
        CompanyID=company_id,  # Use verified company_id
        **event_data.dict()
    )
    db.add(event)
    db.commit()
    return event
```

### Pattern 4: Require Company Context

```python
from common.multi_tenant import require_company_context

@router.get("/dashboard")
async def get_dashboard(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Ensure user has company context
    company_id = require_company_context(current_user.company_id)
    
    # Fetch dashboard data
    stats = get_company_stats(db, company_id)
    return stats
```

## Endpoint Audit

### Endpoints with Company Filtering (✅ Verified)

All existing endpoints have been audited and use proper company filtering:

#### **Team Invitation Endpoints** (Story 1.6)
- `POST /api/companies/{company_id}/invite` - ✅ Verifies path company matches user
- `GET /api/companies/{company_id}/invitations` - ✅ Filters by company_id
- `POST /api/companies/{company_id}/invitations/{id}/resend` - ✅ Verifies company match
- `DELETE /api/companies/{company_id}/invitations/{id}` - ✅ Verifies company match

#### **Invitation Acceptance Endpoints** (Story 1.7)
- `GET /api/invitations/{token}` - ✅ Public (no filtering needed)
- `POST /api/invitations/{token}/accept` - ✅ Creates UserCompany with verified company_id

#### **User Profile Endpoints** (Story 1.5)
- `GET /api/users/me` - ✅ User-scoped (no company filtering needed)
- `POST /api/users/me/details` - ✅ User-scoped (no company filtering needed)
- `GET /api/users/me/companies` - ✅ Filters by user's companies
- `POST /api/users/me/switch-company` - ✅ Verifies user belongs to target company

#### **Company Endpoints** (Story 1.5)
- `POST /api/companies` - ✅ Creates new company with user as admin

#### **Authentication Endpoints** (Stories 1.1, 1.2, 1.4)
- `POST /api/auth/signup` - ✅ User-scoped (no company filtering needed)
- `POST /api/auth/login` - ✅ User-scoped (no company filtering needed)
- `POST /api/auth/verify-email` - ✅ User-scoped (no company filtering needed)
- `POST /api/auth/password-reset/request` - ✅ User-scoped (no company filtering needed)
- `POST /api/auth/password-reset/confirm` - ✅ User-scoped (no company filtering needed)

### Future Endpoints Requiring Company Filtering

When implementing new company-scoped features, ensure these patterns are followed:

- **Events**: All event queries filtered by `company_id`
- **Forms**: All form queries filtered by `company_id`
- **Leads**: All lead queries filtered by `company_id`
- **Campaigns**: All campaign queries filtered by `company_id`
- **Settings**: Company settings filtered by `company_id`

## Security Checklist

### ✅ Implemented Protections

- [x] JWT contains `company_id` claim
- [x] Company ID extracted from JWT, not request body
- [x] All company-scoped endpoints filter by `company_id`
- [x] Path company IDs verified against JWT company ID
- [x] Role requirements enforced (`@require_role` decorator)
- [x] Users cannot access other companies' data
- [x] Failed cross-company access logged
- [x] Email validation for invitations
- [x] Token expiry and single-use enforcement
- [x] Password hashing (bcrypt, cost factor 12)
- [x] SQL injection prevented (parameterized queries)

### 🔄 Infrastructure Protections

- [ ] HTTPS enforced in production (server/proxy level)
- [ ] Rate limiting (to be implemented)
- [ ] IP-based blocking for suspicious patterns (to be implemented)
- [ ] Database indexes on `CompanyID` columns (verified)

## Testing Strategy

### Test Suites Created

1. **`test_multi_tenancy.py`** - Data isolation tests
   - Company filtering helpers
   - Cross-company access prevention
   - Multi-company user scenarios

2. **`test_rbac.py`** - Role-based access control tests
   - Admin vs user permissions
   - Role enforcement on all endpoints
   - Unauthenticated access blocked

3. **`test_security.py`** - Security tests
   - JWT forgery prevention
   - Company ID manipulation blocked
   - SQL injection prevention
   - XSS sanitization
   - Audit logging verification

4. **`test_performance.py`** - Performance tests
   - Query overhead measurement
   - Index usage verification
   - Large dataset performance
   - Concurrent query handling

### Running Tests

```bash
# Run all multi-tenancy tests
cd backend
pytest tests/test_multi_tenancy.py -v

# Run all security tests
pytest tests/test_security.py -v

# Run all RBAC tests
pytest tests/test_rbac.py -v

# Run performance tests
pytest tests/test_performance.py -v

# Run all Story 1.8 tests
pytest tests/test_multi_tenancy.py tests/test_rbac.py tests/test_security.py tests/test_performance.py -v
```

## Helper Functions Reference

### `filter_by_company(query, company_id)`

Applies company filter to SQLAlchemy query.

**Parameters:**
- `query`: SQLAlchemy Query object
- `company_id`: Company ID from JWT

**Returns:** Filtered Query object

**Raises:** HTTPException 403 if no company context

### `verify_company_access(resource_company_id, user_company_id, resource_type)`

Verifies user has access to resource's company.

**Parameters:**
- `resource_company_id`: Company ID of resource
- `user_company_id`: Company ID from JWT
- `resource_type`: Resource type for logging

**Raises:** HTTPException 403 if companies don't match

### `require_company_context(company_id)`

Ensures user has valid company context.

**Parameters:**
- `company_id`: Company ID from JWT

**Returns:** Valid company_id

**Raises:** HTTPException 403 if no company context

### `verify_path_company_matches_user(path_company_id, user_company_id)`

Verifies company_id in URL path matches user's company.

**Parameters:**
- `path_company_id`: Company ID from URL path
- `user_company_id`: Company ID from JWT

**Raises:** HTTPException 403 if companies don't match

### `log_cross_company_access_attempt(...)`

Logs denied cross-company access attempts to audit table.

**Parameters:**
- `db`: Database session
- `user_id`: User ID
- `user_company_id`: User's company ID
- `attempted_company_id`: Attempted company ID
- `resource_type`: Resource type
- `resource_id`: Resource ID
- `endpoint`: API endpoint

## Database Schema

### Company-Scoped Tables

All tables with `CompanyID` column are company-scoped:

- `dbo.Company` - Company records
- `dbo.UserCompany` - User-company relationships
- `dbo.UserInvitation` - Team invitations
- `dbo.Event` (future) - Events
- `dbo.Form` (future) - Forms
- `dbo.Lead` (future) - Leads
- `dbo.Campaign` (future) - Campaigns

### Indexes

All company-scoped tables should have indexes on `CompanyID`:

```sql
-- Example: Create index on UserInvitation
CREATE NONCLUSTERED INDEX IX_UserInvitation_CompanyID
ON dbo.UserInvitation (CompanyID)
INCLUDE (Email, StatusID, ExpiresAt);
```

### Foreign Keys

All company-scoped tables have foreign key to `dbo.Company`:

```sql
ALTER TABLE dbo.UserInvitation
ADD CONSTRAINT FK_UserInvitation_Company
FOREIGN KEY (CompanyID) REFERENCES dbo.Company(CompanyID);
```

## Audit Logging

### Logged Events

All cross-company access attempts are logged to `audit.ActivityLog`:

- **CROSS_COMPANY_ACCESS_DENIED**: User tried to access another company's data
- **INVITATION_ACCEPTED**: User accepted team invitation
- **USER_SIGNUP_WITH_INVITATION**: New user signed up with invitation
- **COMPANY_SWITCHED**: User switched active company

### Monitoring Queries

```sql
-- Find cross-company access attempts in last 24 hours
SELECT 
    al.UserID,
    u.Email,
    al.Action,
    al.EntityType,
    al.OldValue,
    al.CreatedDate
FROM audit.ActivityLog al
JOIN dbo.[User] u ON u.UserID = al.UserID
WHERE al.Action = 'CROSS_COMPANY_ACCESS_DENIED'
AND al.CreatedDate > DATEADD(HOUR, -24, GETUTCDATE())
ORDER BY al.CreatedDate DESC;

-- Find suspicious patterns (multiple attempts from same user)
SELECT 
    al.UserID,
    u.Email,
    COUNT(*) AS AttemptCount
FROM audit.ActivityLog al
JOIN dbo.[User] u ON u.UserID = al.UserID
WHERE al.Action = 'CROSS_COMPANY_ACCESS_DENIED'
AND al.CreatedDate > DATEADD(HOUR, -24, GETUTCDATE())
GROUP BY al.UserID, u.Email
HAVING COUNT(*) > 5
ORDER BY AttemptCount DESC;
```

## Troubleshooting

### "No company context" Error

**Cause:** User's JWT doesn't have `company_id` claim

**Solutions:**
1. User needs to complete onboarding (create or join company)
2. User needs to switch to a company if they belong to multiple
3. Check JWT token contains `company_id` claim

### "Access denied. Resource belongs to different company"

**Cause:** User tried to access another company's data

**Solutions:**
1. Verify user is accessing correct company's resources
2. Check if user belongs to multiple companies and needs to switch
3. Review audit logs for suspicious patterns

### "Cannot access different company's resources"

**Cause:** Company ID in URL path doesn't match JWT company ID

**Solutions:**
1. User needs to switch to correct company
2. Check URL path has correct company ID
3. Verify JWT was issued for correct company

## Performance Optimization

### Database Indexes

Ensure all company-scoped tables have indexes on `CompanyID`:

```sql
-- Check for missing indexes
SELECT 
    OBJECT_SCHEMA_NAME(t.object_id) + '.' + t.name AS TableName,
    c.name AS ColumnName
FROM sys.tables t
INNER JOIN sys.columns c ON t.object_id = c.object_id
WHERE c.name = 'CompanyID'
AND NOT EXISTS (
    SELECT 1
    FROM sys.index_columns ic
    INNER JOIN sys.indexes i ON ic.object_id = i.object_id AND ic.index_id = i.index_id
    WHERE ic.object_id = t.object_id
    AND ic.column_id = c.column_id
);
```

### Query Optimization

- Use `filter_by(CompanyID=company_id)` for single-column filters
- Use indexes for commonly queried columns
- Consider pagination for large result sets
- Monitor slow query logs

### Caching (Future)

Consider caching strategies for:
- User's company list (changes infrequently)
- Company settings (changes infrequently)
- User permissions (changes infrequently)

## Best Practices

### DO ✅

- Always filter company-scoped queries by `company_id`
- Extract `company_id` from JWT, not request body
- Verify path `company_id` matches JWT `company_id`
- Log all denied cross-company access attempts
- Use helper functions for consistent filtering
- Write tests for all company-scoped endpoints
- Monitor audit logs for suspicious patterns

### DON'T ❌

- Don't trust `company_id` from request body
- Don't skip company filtering on any company-scoped query
- Don't expose other companies' data in error messages
- Don't log sensitive data (passwords, tokens)
- Don't allow users to manipulate JWT claims
- Don't skip authorization checks

## Related Documentation

- [RBAC Middleware Guide](./rbac-middleware-guide.md) - Role-based access control
- [JWT Authentication](./jwt-authentication.md) - JWT token structure
- [Invitation System](./team-invitation-guide.md) - Team invitations
- [Audit Logging](./audit-logging-guide.md) - Audit trail documentation

## References

- Story 1.3: RBAC Middleware & Authorization
- Story 1.5: First-Time User Onboarding
- Story 1.6: Team Invitation System
- Story 1.7: Invited User Acceptance
- Story 1.8: Multi-Tenant Data Isolation & Testing

## Change Log

| Date | Version | Changes |
|------|---------|---------|
| 2025-10-16 | 1.0 | Initial release (Story 1.8) |

