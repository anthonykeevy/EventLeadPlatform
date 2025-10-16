# RBAC Middleware & Authorization Guide

## Overview

This guide explains how to use the JWT authentication middleware and role-based access control (RBAC) system implemented in Story 1.3.

## Components

### 1. JWT Authentication Middleware

**Location:** `backend/middleware/auth.py`

The `JWTAuthMiddleware` automatically validates JWT tokens on protected endpoints and injects the current user into the request state.

**How it works:**
1. Extracts Authorization header (`Bearer <token>`)
2. Validates JWT signature and expiration
3. Verifies token type is "access" (not "refresh")
4. Extracts user claims (user_id, email, role, company_id)
5. Stores `CurrentUser` in `request.state.user`
6. Updates request context for logging

**Public endpoints** (skip authentication):
- `/api/auth/*` - Authentication endpoints
- `/docs`, `/redoc`, `/openapi.json` - API documentation
- `/api/health` - Health check
- `/` - Root endpoint

**Error responses:**
- `401 Unauthorized` - Missing, invalid, or expired token
- `403 Forbidden` - Valid token but insufficient permissions

### 2. Current User Model

**Location:** `backend/modules/auth/models.py`

```python
from modules.auth.models import CurrentUser

user = CurrentUser(
    user_id=123,
    email="john@example.com",
    role="company_admin",
    company_id=456
)
```

**Fields:**
- `user_id` (int): Unique user identifier
- `email` (str): User email address
- `role` (Optional[str]): User role (company_admin, company_user, etc.)
- `company_id` (Optional[int]): Active company ID for multi-tenant isolation

**Note:** The model is immutable (`frozen=True`)

### 3. Dependency Injection

**Location:** `backend/modules/auth/dependencies.py`

#### Required Authentication

```python
from fastapi import Depends
from modules.auth.dependencies import get_current_user
from modules.auth.models import CurrentUser

@router.get("/api/users/me")
async def get_profile(
    current_user: CurrentUser = Depends(get_current_user)
):
    return {
        "user_id": current_user.user_id,
        "email": current_user.email
    }
```

#### Optional Authentication

```python
from modules.auth.dependencies import get_current_user_optional

@router.get("/api/public-content")
async def get_content(
    current_user: CurrentUser | None = Depends(get_current_user_optional)
):
    if current_user:
        return {"content": "personalized", "user": current_user.user_id}
    return {"content": "public"}
```

### 4. Role-Based Authorization

**Location:** `backend/common/rbac.py`

#### @require_role Decorator

Restricts endpoint access to specific roles.

**Single role:**
```python
from fastapi import Request
from common.rbac import require_role
from modules.auth.dependencies import get_current_user

@router.post("/api/companies/{company_id}/invite")
@require_role("company_admin")
async def invite_team_member(
    request: Request,
    company_id: int,
    current_user: CurrentUser = Depends(get_current_user)
):
    # Only company admins can access this
    return {"message": "Invitation sent"}
```

**Multiple roles:**
```python
@router.get("/api/dashboard")
@require_role(["company_admin", "company_user"])
async def get_dashboard(
    request: Request,
    current_user: CurrentUser = Depends(get_current_user)
):
    # Either company_admin or company_user can access
    return {"data": "..."}
```

**Important:** The endpoint must accept `request: Request` parameter for the decorator to work.

#### Helper Functions

```python
from common.rbac import (
    has_role,
    is_company_admin,
    belongs_to_company,
    require_company_access
)

# Check if user has specific role
if has_role(current_user, "company_admin"):
    # Grant admin privileges
    pass

# Check if user is company admin
if is_company_admin(current_user):
    # Admin-only logic
    pass

# Check if user belongs to company
if belongs_to_company(current_user, company_id):
    # User can access this company's data
    pass

# Require company access (raises 403 if fails)
require_company_access(current_user, company_id)
```

### 5. Multi-Tenant Data Isolation

The middleware automatically extracts `company_id` from the JWT and stores it in `request.state.user.company_id`.

**Best practice for company-specific endpoints:**

```python
@router.get("/companies/{company_id}/data")
async def get_company_data(
    company_id: int,
    current_user: CurrentUser = Depends(get_current_user)
):
    # Verify user belongs to the requested company
    if current_user.company_id != company_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied. You do not belong to this company."
        )
    
    # Fetch company data
    # ...
```

Or use the helper function:

```python
from common.rbac import require_company_access

@router.get("/companies/{company_id}/data")
async def get_company_data(
    company_id: int,
    current_user: CurrentUser = Depends(get_current_user)
):
    require_company_access(current_user, company_id)
    # Fetch company data
    # ...
```

## Common Patterns

### Pattern 1: Public Endpoint
```python
@router.get("/api/public")
async def public_endpoint():
    return {"message": "public"}
```

### Pattern 2: Authenticated Endpoint
```python
@router.get("/api/protected")
async def protected_endpoint(
    current_user: CurrentUser = Depends(get_current_user)
):
    return {"message": "authenticated", "user": current_user.user_id}
```

### Pattern 3: Role-Restricted Endpoint
```python
@router.post("/api/admin")
@require_role("company_admin")
async def admin_endpoint(
    request: Request,
    current_user: CurrentUser = Depends(get_current_user)
):
    return {"message": "admin access"}
```

### Pattern 4: Company-Specific Endpoint
```python
@router.get("/companies/{company_id}/settings")
async def get_settings(
    company_id: int,
    current_user: CurrentUser = Depends(get_current_user)
):
    require_company_access(current_user, company_id)
    # Fetch settings
    return {"settings": "..."}
```

### Pattern 5: Optional Authentication
```python
@router.get("/api/content")
async def get_content(
    current_user: CurrentUser | None = Depends(get_current_user_optional)
):
    if current_user:
        # Return personalized content
        pass
    # Return public content
    pass
```

## Logging Integration

The middleware integrates with Story 0.2 (Automated Logging) by updating the request context:

```python
from common.request_context import update_request_context

# Middleware automatically calls:
update_request_context(
    user_id=current_user.user_id,
    company_id=current_user.company_id
)
```

This ensures all log entries (log.ApiRequest) include `UserID` and `CompanyID` for authenticated requests.

## Testing

### Running Tests

**Prerequisites:**
```bash
cd backend
pip install -r requirements.txt
```

**Run all auth middleware tests:**
```bash
python -m pytest tests/test_auth_middleware.py -v
```

**Run RBAC unit tests:**
```bash
python -m pytest tests/test_rbac_unit.py -v
```

**Run validation script:**
```bash
python validate_story_1_3.py
```

### Test Coverage

The test suite covers all acceptance criteria:

- **AC-1.3.1**: JWT validation on protected endpoints
- **AC-1.3.2**: JWT payload extraction
- **AC-1.3.3**: CurrentUser injection into request state
- **AC-1.3.4**: Role-based authorization decorator
- **AC-1.3.5**: Company context and multi-tenant isolation
- **AC-1.3.6**: Error handling (missing, invalid, expired tokens)
- **AC-1.3.7**: 401/403 error responses
- **AC-1.3.8**: Request context logging integration
- **AC-1.3.9**: Dependency injection (get_current_user)
- **AC-1.3.10**: Protected endpoint logging

## Security Considerations

1. **JWT Secret**: Must be at least 32 characters. Set `JWT_SECRET_KEY` environment variable.

2. **Token Expiry**: Default 60 minutes for access tokens. Configure with `JWT_EXPIRATION_MINUTES`.

3. **Token Type Validation**: Middleware rejects refresh tokens on protected endpoints.

4. **Multi-Tenant Isolation**: Always verify `company_id` matches user's company.

5. **Role Validation**: Use `@require_role` decorator to enforce role requirements.

6. **Public Endpoints**: Add to `JWTAuthMiddleware.PUBLIC_PATHS` if needed.

## Troubleshooting

### 401 Unauthorized - Missing token
```json
{"detail": "Missing authorization header"}
```
**Solution:** Include `Authorization: Bearer <token>` header

### 401 Unauthorized - Invalid token
```json
{"detail": "Invalid token"}
```
**Solution:** Ensure token is valid and not corrupted

### 401 Unauthorized - Expired token
```json
{"detail": "Token has expired"}
```
**Solution:** Use refresh token to get new access token

### 401 Unauthorized - Wrong token type
```json
{"detail": "Invalid token type"}
```
**Solution:** Use access token (not refresh token) for API requests

### 403 Forbidden - Wrong role
```json
{"detail": "Insufficient permissions. Required role: company_admin"}
```
**Solution:** User doesn't have required role. Check user's role assignment.

### 403 Forbidden - Different company
```json
{"detail": "Access denied. You do not belong to this company."}
```
**Solution:** User trying to access data from different company. Check company_id.

## Migration Notes

To protect existing endpoints:

1. Add `@require_role` decorator if role restriction needed
2. Add `current_user: CurrentUser = Depends(get_current_user)` parameter
3. If company-specific, add `require_company_access(current_user, company_id)`

Example before:
```python
@router.get("/api/data")
async def get_data():
    return {"data": "..."}
```

Example after:
```python
@router.get("/api/data")
async def get_data(
    current_user: CurrentUser = Depends(get_current_user)
):
    # Now protected by JWT authentication
    return {"data": "..."}
```

## References

- [Story 1.2: Login & JWT Tokens](../stories/story-1.2.md)
- [Story 0.2: Automated Logging](../stories/story-0.2.md)
- [Tech Spec Epic 1: RBAC](../tech-spec-epic-1.md)

