# ADR-002: Backend Abstraction Layer Design

**Status:** Accepted  
**Date:** 2025-10-16  
**Deciders:** Anthony Keevy (Product Owner), Winston (Architect)  
**Context:** Epic 1 - Authentication & Onboarding

---

## Context and Problem Statement

EventLeadPlatform uses SQL Server with PascalCase naming conventions (Anthony's standards), Python backend with snake_case conventions (PEP 8), and TypeScript frontend with camelCase conventions (JavaScript standards). 

**Key Problem:** Without proper abstraction, database naming conventions leak into API responses, tightly coupling frontend to database schema. This makes refactoring dangerous and violates separation of concerns.

**Key Questions:**
- How do we isolate database naming conventions from frontend code?
- Should we transform naming conventions at the API boundary?
- What's the best approach for maintaining type safety across layers?
- How do we prevent database schema changes from breaking frontend?

**Constraints:**
- Must maintain Anthony's database standards (PascalCase, self-documenting foreign keys)
- Must follow Python PEP 8 (snake_case for variables/functions)
- Must follow JavaScript conventions (camelCase for JSON APIs)
- Must be type-safe (TypeScript on frontend, Pydantic on backend)
- Must not require manual mapping for every field (too error-prone)

---

## Decision Drivers

1. **Separation of Concerns:** Database, backend, and frontend should be independently evolvable
2. **Developer Experience:** Developers should use native conventions for their layer (no cognitive load of switching)
3. **Type Safety:** Compile-time errors for mismatched field names (prevent runtime bugs)
4. **Maintainability:** Database refactoring shouldn't require frontend changes
5. **Standards Compliance:** Each layer follows its own industry best practices
6. **Performance:** Transformation overhead must be negligible

---

## Considered Options

### **Option A: No Abstraction (Direct Database Naming in API)**

```python
# Backend
@router.get("/api/users/{id}")
def get_user(id: int):
    user = db.query(User).filter(User.UserID == id).first()
    return {
        "UserID": user.UserID,           # PascalCase in JSON
        "FirstName": user.FirstName,
        "EmailAddress": user.Email
    }
```

```typescript
// Frontend
const userName = user.FirstName + " " + user.LastName;  // SQL naming in JavaScript
```

**Pros:**
- ✅ Simplest approach (no mapping needed)
- ✅ No transformation overhead

**Cons:**
- ❌ Frontend tightly coupled to database schema
- ❌ Database column rename breaks frontend
- ❌ Violates JavaScript naming conventions (confusing for frontend devs)
- ❌ Mixing naming conventions in same codebase (poor developer experience)
- ❌ No clear boundaries between layers

---

### **Option B: Manual Mapping in Each Endpoint**

```python
@router.get("/api/users/{id}")
def get_user(id: int):
    user = db.query(User).filter(User.UserID == id).first()
    return {
        "userId": user.UserID,           # Manual camelCase conversion
        "firstName": user.FirstName,
        "lastName": user.LastName,
        "email": user.Email
    }
```

**Pros:**
- ✅ Frontend gets camelCase (JavaScript convention)
- ✅ Explicit mapping (clear what's exposed)

**Cons:**
- ❌ Extremely error-prone (easy to forget fields)
- ❌ High maintenance burden (update every endpoint when schema changes)
- ❌ No type safety (typos not caught until runtime)
- ❌ Verbose and repetitive code
- ❌ Inconsistent (developers will forget or do it differently)

---

### **Option C: 3-Layer Abstraction with Automatic Transformation** ⭐ **CHOSEN**

```python
# Layer 1: SQLAlchemy Model (Database → Python)
class User(Base):
    __tablename__ = 'User'
    __table_args__ = {'schema': 'dbo'}
    
    # Column mapping: python_property = Column('SQLColumnName', ...)
    user_id = Column('UserID', BigInteger, primary_key=True)
    first_name = Column('FirstName', String(100), nullable=False)
    email = Column('Email', String(255), nullable=False)


# Layer 2: Pydantic Schema (Python → JSON with camelCase)
def to_camel_case(string: str) -> str:
    components = string.split('_')
    return components[0] + ''.join(x.capitalize() for x in components[1:])

class UserResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel_case)
    
    user_id: int          # API outputs: "userId"
    first_name: str       # API outputs: "firstName"
    email: EmailStr       # API outputs: "email"


# Layer 3: Service Layer (Clean Python code)
class UserService:
    @staticmethod
    def get_user(db: Session, user_id: int) -> UserResponse:
        user = db.query(User).filter(User.user_id == user_id).first()
        return UserResponse.model_validate(user)  # Auto-converts to camelCase


# Layer 4: API Router
@router.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return UserService.get_user(db, user_id)
```

```typescript
// Frontend (receives clean camelCase)
interface User {
  userId: number;
  firstName: string;
  email: string;
}

const user: User = await api.get<User>('/api/users/123');
console.log(user.firstName);  // Clean JavaScript code
```

**Pros:**
- ✅ Each layer uses its native convention (PascalCase → snake_case → camelCase)
- ✅ Automatic transformation (Pydantic `alias_generator` + SQLAlchemy column mapping)
- ✅ Type-safe at every layer (compile-time errors for field mismatches)
- ✅ Database refactoring doesn't break frontend (only update SQLAlchemy model)
- ✅ Clean, idiomatic code in every layer (no mixed conventions)
- ✅ DRY principle (transformation rules defined once, applied everywhere)
- ✅ Testable (each layer can be unit tested independently)

**Cons:**
- ⚠️ Requires column name mapping in SQLAlchemy models (one-time setup per table)
- ⚠️ Requires Pydantic schema definitions (but needed anyway for validation)
- ⚠️ Slight learning curve for developers unfamiliar with SQLAlchemy column mapping

---

## Decision Outcome

**Chosen Option:** Option C - 3-Layer Abstraction with Automatic Transformation

**Rationale:**
- EventLeadPlatform will grow to 100+ tables across 8 epics - manual mapping not scalable
- Type safety is critical for preventing runtime bugs
- Each layer should follow its own standards (database team uses SQL conventions, frontend team uses JavaScript conventions)
- Database refactoring must not break frontend (independence of evolution)
- Automatic transformation eliminates human error and inconsistency

---

## Implementation Strategy

### **Layer 1: SQLAlchemy Models (Database → Python)**

**Purpose:** Map SQL Server columns (PascalCase) to Python properties (snake_case)

**Pattern:**
```python
# backend/models/user.py
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, Integer
from backend.common.database import Base

class User(Base):
    """
    SQLAlchemy model - Maps SQL Server columns to Python properties
    
    Column naming pattern:
      python_property = Column('SQLServerColumnName', type, constraints)
    
    Example:
      user_id = Column('UserID', BigInteger, primary_key=True)
      - Python code uses: user.user_id
      - Database stores in: UserID column
    """
    __tablename__ = 'User'
    __table_args__ = {'schema': 'dbo'}
    
    # Primary Key
    user_id = Column('UserID', BigInteger, primary_key=True, autoincrement=True)
    
    # Authentication
    email = Column('Email', String(255), nullable=False, unique=True)
    password_hash = Column('PasswordHash', String(500), nullable=False)
    
    # Profile
    first_name = Column('FirstName', String(100), nullable=False)
    last_name = Column('LastName', String(100), nullable=False)
    phone = Column('Phone', String(20), nullable=True)
    
    # Booleans (Is/Has prefix in database)
    is_email_verified = Column('IsEmailVerified', Boolean, nullable=False, default=False)
    is_locked = Column('IsLocked', Boolean, nullable=False, default=False)
    
    # Foreign Keys
    status_id = Column('StatusID', BigInteger, nullable=False)
    country_id = Column('CountryID', BigInteger, nullable=True)
    
    # Audit Trail
    created_date = Column('CreatedDate', DateTime, nullable=False, default=datetime.utcnow)
    created_by = Column('CreatedBy', BigInteger, nullable=True)
    updated_date = Column('UpdatedDate', DateTime, nullable=False, default=datetime.utcnow)
    updated_by = Column('UpdatedBy', BigInteger, nullable=True)
    is_deleted = Column('IsDeleted', Boolean, nullable=False, default=False)
```

**Benefits:**
- Python code uses Pythonic snake_case (`user.user_id`, `user.first_name`)
- Database stores PascalCase (complies with Anthony's standards)
- SQLAlchemy handles translation automatically (zero runtime overhead)

---

### **Layer 2: Pydantic Schemas (Python → JSON API)**

**Purpose:** Auto-convert Python properties (snake_case) to JSON fields (camelCase)

**Reusable Config:**
```python
# backend/common/schemas.py
from pydantic import ConfigDict

def to_camel_case(string: str) -> str:
    """
    Convert snake_case to camelCase
    
    Examples:
        user_id → userId
        first_name → firstName
        is_email_verified → isEmailVerified
    """
    components = string.split('_')
    return components[0] + ''.join(x.capitalize() for x in components[1:])

# Reusable config for all Pydantic schemas
CamelCaseConfig = ConfigDict(
    alias_generator=to_camel_case,
    populate_by_name=True,  # Allow both camelCase and snake_case (flexibility)
    from_attributes=True    # Allow ORM model conversion
)
```

**Schema Pattern:**
```python
# backend/modules/auth/schemas.py
from backend.common.schemas import CamelCaseConfig
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserResponse(BaseModel):
    """API Response Schema - Outputs camelCase for frontend"""
    model_config = CamelCaseConfig
    
    # Define fields in Python snake_case
    # Pydantic automatically outputs camelCase in JSON
    user_id: int = Field(..., description="Unique user identifier")
    email: EmailStr = Field(..., description="User email address")
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    
    is_email_verified: bool
    is_locked: bool
    
    created_date: datetime
    last_login_date: Optional[datetime] = None


class UserCreateRequest(BaseModel):
    """API Request Schema - Accepts camelCase from frontend"""
    model_config = CamelCaseConfig
    
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    first_name: str
    last_name: str
    phone: Optional[str] = None
```

**JSON Output:**
```json
{
  "userId": 123,
  "email": "john@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "isEmailVerified": true,
  "createdDate": "2025-10-16T10:30:00Z"
}
```

---

### **Layer 3: Service Layer (Business Logic)**

**Purpose:** Clean Python code with snake_case throughout

**Pattern:**
```python
# backend/modules/auth/service.py
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.modules.auth.schemas import UserResponse, UserCreateRequest
from backend.common.security import hash_password
from datetime import datetime
from typing import Optional

class UserService:
    """Service layer - Business logic with Pythonic naming"""
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreateRequest) -> UserResponse:
        """Create new user - Notice clean Python naming throughout"""
        # All code uses snake_case (PEP 8 compliant)
        new_user = User(
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone=user_data.phone,
            status_id=2,  # 'pending' status
            is_email_verified=False,
            created_date=datetime.utcnow()
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Pydantic converts to camelCase automatically
        return UserResponse.model_validate(new_user)
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[UserResponse]:
        """Get user by ID - Python naming in queries"""
        user = db.query(User).filter(User.user_id == user_id).first()
        
        if user:
            return UserResponse.model_validate(user)
        return None
```

---

### **Layer 4: API Router (HTTP Endpoints)**

**Purpose:** Define API contracts with proper response models

**Pattern:**
```python
# backend/modules/auth/router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.common.database import get_db
from backend.modules.auth.schemas import UserResponse, UserCreateRequest
from backend.modules.auth.service import UserService

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreateRequest, db: Session = Depends(get_db)):
    """
    Create new user
    
    Request body (camelCase from frontend):
    {
      "email": "john@example.com",
      "password": "SecurePass123!",
      "firstName": "John",
      "lastName": "Doe"
    }
    
    Response (camelCase to frontend):
    {
      "userId": 123,
      "firstName": "John",
      "isEmailVerified": false
    }
    """
    return UserService.create_user(db, user_data)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

---

## Data Flow Summary

```
┌─────────────────────────────────────────────────────────────┐
│               DATA TRANSFORMATION FLOW                       │
└─────────────────────────────────────────────────────────────┘

Database (SQL Server):
  Column: UserID (PascalCase)
      ↓
SQLAlchemy Model (Python):
  Property: user_id (snake_case)
  Code: user = db.query(User).filter(User.user_id == 123).first()
      ↓
Service Layer (Python):
  Variable: user.user_id (snake_case)
  Code: new_user = User(first_name=data.first_name, ...)
      ↓
Pydantic Schema (JSON API):
  Field: userId (camelCase)
  Transformation: alias_generator converts automatically
      ↓
Frontend (TypeScript):
  Property: user.userId (camelCase)
  Code: console.log(user.userId, user.firstName)
```

---

## Consequences

### **Positive:**

1. **Each layer uses native conventions:**
   - Database: PascalCase (SQL Server standards)
   - Python: snake_case (PEP 8)
   - JSON API: camelCase (JavaScript standards)

2. **Database refactoring independence:**
   ```python
   # Database column renamed: FirstName → GivenName
   
   # Only SQLAlchemy model changes:
   first_name = Column('GivenName', String(100))  # Update mapping
   
   # Python code unchanged (still uses first_name)
   # Frontend unchanged (still receives firstName)
   # API contract preserved ✅
   ```

3. **Type safety at every layer:**
   - SQLAlchemy: Column types enforced
   - Pydantic: Request/response validation
   - TypeScript: Compile-time type checking
   - Typos caught before runtime

4. **Automatic transformation:**
   - No manual field mapping needed
   - Consistent across all endpoints
   - Eliminates human error

5. **Testable layers:**
   ```python
   # Test service layer independently
   def test_create_user():
       user_data = UserCreateRequest(
           email="test@example.com",
           first_name="Test",
           ...
       )
       result = UserService.create_user(db, user_data)
       assert result.first_name == "Test"
   ```

### **Negative:**

1. **Column mapping required:**
   - Every SQLAlchemy model needs explicit column mapping
   - **Mitigation:** Template available, copy-paste pattern for new models

2. **Pydantic schemas required:**
   - Must define Request/Response schemas for every endpoint
   - **Mitigation:** Needed anyway for validation, documentation (not extra work)

3. **Learning curve:**
   - Developers must understand SQLAlchemy column mapping
   - **Mitigation:** This ADR + quick-reference guide + code examples

---

## Compliance with Standards

**BMAD v6 Alignment:**
- ✅ Separation of concerns (each layer independently evolvable)
- ✅ Type safety (prevents runtime bugs)
- ✅ Documented architecture decision (ADR)

**Anthony's Database Standards:**
- ✅ Database uses PascalCase (UserID, FirstName, IsActive)
- ✅ Self-documenting foreign keys (CompanyID, UserRoleID)
- ✅ Is/Has prefix for booleans (IsEmailVerified, IsLocked)

**Python PEP 8:**
- ✅ snake_case for variables/functions (user_id, first_name)
- ✅ Clean, Pythonic code

**JavaScript/TypeScript Standards:**
- ✅ camelCase for JSON APIs (userId, firstName)
- ✅ Industry standard (Airbnb style guide)

---

## References

- Solution Architecture: `docs/solution-architecture.md` (Backend Abstraction Layer Architecture section)
- Backend Abstraction Layer Guide: `docs/technical-guides/backend-database-abstraction-layer.md`
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html
- Pydantic Documentation: https://docs.pydantic.dev/latest/concepts/alias/
- PEP 8 (Python Style Guide): https://peps.python.org/pep-0008/

---

## Approval

**Approved by:** Anthony Keevy  
**Date:** 2025-10-16  
**Status:** Accepted - To be implemented in Epic 1 Story 1.1-1.3

---

**Winston** 🏗️  
*"Build walls between layers. Let each layer speak its own language."*

