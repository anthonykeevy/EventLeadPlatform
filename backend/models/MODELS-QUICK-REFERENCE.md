# SQLAlchemy Models Quick Reference

## Overview

This document provides quick reference for using SQLAlchemy models in the EventLead Platform.

**Total Models: 33 across 6 schemas**

- **ref** (13 models): Reference/lookup tables
- **dbo** (9 models): Core business entities
- **config** (2 models): Configuration tables
- **audit** (4 models): Audit trail tables
- **log** (4 models): Technical logging tables
- **cache** (1 model): API cache tables

## Importing Models

```python
# Import all models from main module
from backend.models import (
    User, Company, UserCompany,
    Country, UserStatus, UserCompanyRole,
    AppSetting, ActivityLog, ApiRequest, ABRSearch
)

# Or import from specific schemas
from backend.models.ref import Country, Language, Industry
from backend.models.config import AppSetting, ValidationRule
```

## Database Session Management

### Using FastAPI Dependency Injection

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from backend.common.database import get_db
from backend.models import User

@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    return user
```

### Direct Session Usage

```python
from backend.common.database import SessionLocal
from backend.models import User

# Create session
db = SessionLocal()

try:
    # Use session
    user = db.get(User, 1)
    print(user.Email)
finally:
    # Always close session
    db.close()
```

## Common Query Patterns

### Basic Queries

```python
from sqlalchemy import select
from backend.models import User, Company

# Get by primary key
user = db.get(User, user_id)

# Query with filter
stmt = select(User).where(User.Email == "user@example.com")
user = db.execute(stmt).scalar_one_or_none()

# Query all with filter
stmt = select(Company).where(Company.IsActive == True)
companies = db.execute(stmt).scalars().all()

# Count records
stmt = select(func.count()).select_from(User).where(User.IsDeleted == False)
count = db.execute(stmt).scalar()
```

### Pagination

```python
from backend.models import User

page = 1
page_size = 20
offset = (page - 1) * page_size

stmt = (
    select(User)
    .where(User.IsDeleted == False)
    .order_by(User.CreatedDate.desc())
    .limit(page_size)
    .offset(offset)
)
users = db.execute(stmt).scalars().all()
```

### Joins and Relationships

```python
from backend.models import User, UserCompany, Company

# Query with explicit join
stmt = (
    select(User, Company)
    .join(UserCompany, User.UserID == UserCompany.UserID)
    .join(Company, UserCompany.CompanyID == Company.CompanyID)
    .where(User.Email == "user@example.com")
)
result = db.execute(stmt).first()

# Using relationship navigation (lazy loading)
user = db.get(User, user_id)
for user_company in user.companies:
    print(f"Company: {user_company.company.CompanyName}")
    print(f"Role: {user_company.role.RoleName}")
```

### Eager Loading

```python
from sqlalchemy.orm import joinedload

# Load user with relationships
stmt = (
    select(User)
    .options(joinedload(User.companies).joinedload(UserCompany.company))
    .where(User.UserID == user_id)
)
user = db.execute(stmt).scalar_one()
```

## Creating Records

### Create User

```python
from backend.models import User
from backend.common.security import hash_password
from datetime import datetime

user = User(
    Email="newuser@example.com",
    PasswordHash=hash_password("SecurePassword123!"),
    FirstName="John",
    LastName="Doe",
    StatusID=1,  # Active
    TimezoneIdentifier="Australia/Sydney",
    CreatedDate=datetime.utcnow(),
    IsDeleted=False
)

db.add(user)
db.commit()
db.refresh(user)  # Get auto-generated ID

print(f"Created user with ID: {user.UserID}")
```

### Create Company

```python
from backend.models import Company

company = Company(
    CompanyName="Acme Corp",
    ABN="51824753556",
    CountryID=1,  # Australia
    DisplayNameSource="User",
    IsActive=True
)

db.add(company)
db.commit()
```

### Create User-Company Relationship

```python
from backend.models import UserCompany
from datetime import datetime

user_company = UserCompany(
    UserID=user.UserID,
    CompanyID=company.CompanyID,
    UserCompanyRoleID=1,  # Owner
    StatusID=1,  # Active
    IsPrimaryCompany=True,
    JoinedViaID=1,  # Signup
    JoinedDate=datetime.utcnow()
)

db.add(user_company)
db.commit()
```

## Updating Records

```python
from backend.models import User
from datetime import datetime

user = db.get(User, user_id)
user.FirstName = "Jane"
user.UpdatedDate = datetime.utcnow()
user.UpdatedBy = current_user_id

db.commit()
```

## Soft Deletes

```python
from backend.models import User
from datetime import datetime

user = db.get(User, user_id)
user.IsDeleted = True
user.DeletedDate = datetime.utcnow()
user.DeletedBy = current_user_id

db.commit()
```

## Security Utilities

### Password Hashing

```python
from backend.common.security import hash_password, verify_password

# Hash password (bcrypt, cost factor 12)
hashed = hash_password("MySecurePassword123!")
# Returns: "$2b$12$..."

# Verify password
is_valid = verify_password("MySecurePassword123!", hashed)
# Returns: True

# Wrong password
is_valid = verify_password("WrongPassword", hashed)
# Returns: False
```

### Token Generation

```python
from backend.common.security import generate_secure_token

# Generate email verification token
token = generate_secure_token(32)  # 256-bit security
# Returns: URL-safe string ~43 characters

# Generate password reset token
reset_token = generate_secure_token(32)
```

## Common Patterns

### Get User by Email

```python
from sqlalchemy import select
from backend.models import User

stmt = select(User).where(User.Email == email, User.IsDeleted == False)
user = db.execute(stmt).scalar_one_or_none()
```

### Get User's Companies

```python
from sqlalchemy import select
from backend.models import User, UserCompany, Company

user = db.get(User, user_id)

# Via relationship
for uc in user.companies:
    if not uc.IsDeleted:
        print(f"{uc.company.CompanyName} - {uc.role.RoleName}")

# Via explicit query
stmt = (
    select(Company)
    .join(UserCompany)
    .where(
        UserCompany.UserID == user_id,
        UserCompany.IsDeleted == False,
        Company.IsDeleted == False
    )
)
companies = db.execute(stmt).scalars().all()
```

### Check User Permission

```python
from backend.models import UserCompany

stmt = (
    select(UserCompany)
    .where(
        UserCompany.UserID == user_id,
        UserCompany.CompanyID == company_id,
        UserCompany.IsDeleted == False
    )
)
user_company = db.execute(stmt).scalar_one_or_none()

if user_company:
    role = user_company.role
    if role.CanManageEvents:
        # User has permission
        pass
```

### Audit Logging

```python
from backend.models import ActivityLog
from datetime import datetime

log = ActivityLog(
    UserID=user_id,
    UserEmail=user.Email,
    Action="create_event",
    EntityType="Event",
    EntityID=event_id,
    CompanyID=company_id,
    NewValue=json.dumps({"name": "My Event"}),
    IPAddress=request_ip,
    UserAgent=request_user_agent,
    CreatedDate=datetime.utcnow()
)

db.add(log)
db.commit()
```

## Model Naming Conventions (Solomon Standards)

All models follow PascalCase naming:

- **Tables**: `User`, `Company`, `UserCompany`
- **Columns**: `UserID`, `FirstName`, `EmailVerified`
- **Primary Keys**: `[TableName]ID` (e.g., `UserID`, `CompanyID`)
- **Foreign Keys**: `[ReferencedTable]ID` (e.g., `StatusID` references `UserStatus`)
- **Indexes**: `IX_TableName_ColumnName`
- **Constraints**: `FK_`, `UQ_`, `CK_`, `DF_` prefixes

## Audit Columns

All business tables include:

- `CreatedDate` (DATETIME2, UTC)
- `CreatedBy` (BIGINT, FK to User)
- `UpdatedDate` (DATETIME2, UTC)
- `UpdatedBy` (BIGINT, FK to User)
- `IsDeleted` (BIT, soft delete flag)
- `DeletedDate` (DATETIME2, UTC)
- `DeletedBy` (BIGINT, FK to User)

## Best Practices

1. **Always use `get_db()` dependency** in FastAPI routes
2. **Always close sessions** in direct usage
3. **Use soft deletes** - set `IsDeleted=True` instead of DELETE
4. **Update audit columns** on every change
5. **Use UTC timestamps** - all datetime fields are UTC
6. **Filter by IsDeleted** in queries
7. **Use transactions** for multi-table updates
8. **Eager load relationships** when needed to avoid N+1 queries
9. **Use connection pooling** - already configured
10. **Test queries** before deploying

## Testing

```python
# Run all tests
pytest backend/tests/

# Run specific test file
pytest backend/tests/test_models_import.py

# Run with verbose output
pytest -v backend/tests/

# Run with coverage
pytest --cov=backend backend/tests/
```

## Troubleshooting

### Circular Import Errors

Always import from `backend.models`:
```python
# Good
from backend.models import User, Company

# Bad - may cause circular imports
from backend.models.user import User
```

### Relationship Not Loading

Use eager loading:
```python
from sqlalchemy.orm import joinedload

stmt = select(User).options(joinedload(User.companies))
user = db.execute(stmt).scalar_one()
```

### Session Closed Errors

Always access relationships before closing session:
```python
user = db.get(User, user_id)
companies = user.companies  # Load before closing
db.close()

# Now can access
for uc in companies:
    print(uc.company.CompanyName)
```

## See Also

- [Database Quick Reference](../../docs/technical-guides/database-quick-reference.md)
- [Backend Quick Reference](../../docs/technical-guides/backend-quick-reference.md)
- [Tech Spec Epic 1](../../docs/tech-spec-epic-1.md)
- [ADR-003: Naming Conventions](../../docs/architecture/decisions/ADR-003-naming-convention-strategy.md)

