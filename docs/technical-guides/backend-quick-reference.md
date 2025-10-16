# Backend Implementation Quick Reference

**Purpose:** 1-page cheat sheet for backend development patterns  
**Target Audience:** Backend developers implementing Epic 1 stories  
**Status:** ✅ APPROVED - Use as template for all implementations

---

## 🗂️ Project Structure

```
backend/
├── common/                    # Shared utilities
│   ├── database.py            # SQLAlchemy setup, get_db()
│   ├── security.py            # JWT, password hashing
│   └── schemas.py             # CamelCaseConfig (reusable)
├── models/                    # SQLAlchemy models (one file per table)
│   ├── user.py
│   ├── company.py
│   └── __init__.py            # Import all models
├── modules/                   # Feature modules
│   ├── auth/
│   │   ├── router.py          # API endpoints
│   │   ├── service.py         # Business logic
│   │   ├── schemas.py         # Pydantic models
│   │   └── dependencies.py    # Custom dependencies
│   └── companies/
│       ├── router.py
│       ├── service.py
│       └── schemas.py
├── migrations/                # Alembic migrations
│   └── versions/
├── main.py                    # FastAPI app entry point
└── requirements.txt
```

---

## 🏗️ 3-Layer Architecture

### **Layer 1: SQLAlchemy Model (Database → Python)**

```python
# backend/models/user.py
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime
from backend.common.database import Base

class User(Base):
    __tablename__ = 'User'
    __table_args__ = {'schema': 'dbo'}
    
    # Column mapping: python_property = Column('SQLColumnName', type)
    user_id = Column('UserID', BigInteger, primary_key=True)
    email = Column('Email', String(255), nullable=False, unique=True)
    password_hash = Column('PasswordHash', String(500), nullable=False)
    first_name = Column('FirstName', String(100), nullable=False)
    last_name = Column('LastName', String(100), nullable=False)
    status_id = Column('StatusID', BigInteger, nullable=False)
    is_email_verified = Column('IsEmailVerified', Boolean, default=False)
    created_date = Column('CreatedDate', DateTime, default=datetime.utcnow)
```

### **Layer 2: Pydantic Schema (Python → JSON API)**

```python
# backend/modules/auth/schemas.py
from pydantic import BaseModel, EmailStr, Field
from backend.common.schemas import CamelCaseConfig

class UserResponse(BaseModel):
    model_config = CamelCaseConfig  # Auto-converts to camelCase
    
    user_id: int
    email: EmailStr
    first_name: str
    last_name: str
    is_email_verified: bool

class UserCreateRequest(BaseModel):
    model_config = CamelCaseConfig
    
    email: EmailStr
    password: str = Field(min_length=8)
    first_name: str
    last_name: str
```

### **Layer 3: Service Layer (Business Logic)**

```python
# backend/modules/auth/service.py
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.modules.auth.schemas import UserResponse, UserCreateRequest
from backend.common.security import hash_password

class UserService:
    @staticmethod
    def create_user(db: Session, user_data: UserCreateRequest) -> UserResponse:
        new_user = User(
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            status_id=2  # 'pending'
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return UserResponse.model_validate(new_user)
```

### **Layer 4: API Router (HTTP Endpoints)**

```python
# backend/modules/auth/router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.common.database import get_db
from backend.modules.auth.schemas import UserResponse, UserCreateRequest
from backend.modules.auth.service import UserService

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user_data: UserCreateRequest, db: Session = Depends(get_db)):
    return UserService.create_user(db, user_data)
```

---

## 📦 Reusable Config (Copy-Paste)

```python
# backend/common/schemas.py
from pydantic import ConfigDict

def to_camel_case(string: str) -> str:
    """Convert snake_case → camelCase"""
    components = string.split('_')
    return components[0] + ''.join(x.capitalize() for x in components[1:])

CamelCaseConfig = ConfigDict(
    alias_generator=to_camel_case,
    populate_by_name=True,
    from_attributes=True
)
```

---

## 🔒 Common Dependencies

```python
# backend/common/dependencies.py
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from backend.common.database import get_db
from backend.models.user import User

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    """Get current user from JWT token"""
    user_id = decode_jwt_token(token)
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

async def get_current_company(current_user: User = Depends(get_current_user)) -> int:
    """Get current user's company ID (multi-tenant filtering)"""
    return current_user.company_id

def require_role(role: str):
    """Require specific role for endpoint"""
    async def dependency(current_user: User = Depends(get_current_user)):
        if current_user.role != role and current_user.role != "system_admin":
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return dependency
```

---

## 🛡️ Multi-Tenant Isolation

**EVERY query MUST filter by CompanyID:**

```python
# ✅ CORRECT: Multi-tenant safe
@router.get("/api/forms")
async def list_forms(
    company_id: int = Depends(get_current_company),
    db: Session = Depends(get_db)
):
    forms = db.query(Form).filter(Form.company_id == company_id).all()
    return forms

# ❌ WRONG: No company filter (security breach!)
@router.get("/api/forms")
async def list_forms(db: Session = Depends(get_db)):
    forms = db.query(Form).all()  # ❌ Returns ALL companies' forms
    return forms
```

---

## 🧪 Testing Patterns

```python
# backend/tests/test_user_service.py
import pytest
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.modules.auth.service import UserService
from backend.modules.auth.schemas import UserCreateRequest

def test_create_user(db: Session):
    user_data = UserCreateRequest(
        email="test@example.com",
        password="SecurePass123!",
        first_name="Test",
        last_name="User"
    )
    
    result = UserService.create_user(db, user_data)
    
    assert result.email == "test@example.com"
    assert result.first_name == "Test"
    assert result.is_email_verified == False
```

---

## 📝 Naming Convention Reference

| Layer | Convention | Example |
|-------|-----------|---------|
| **Database** | PascalCase | `UserID`, `FirstName`, `IsActive` |
| **Python (models)** | snake_case | `user_id`, `first_name`, `is_active` |
| **Python (classes)** | PascalCase | `User`, `UserService`, `AuthMiddleware` |
| **JSON API** | camelCase | `userId`, `firstName`, `isActive` |
| **Files** | snake_case | `user_service.py`, `auth_middleware.py` |

---

## ⚡ Common Patterns

### **Lookup Reference Table**

```python
status = db.query(UserStatus).filter(UserStatus.status_code == 'active').first()
user.status_id = status.user_status_id
```

### **Validate Foreign Key Exists**

```python
country = db.query(Country).filter(Country.country_id == country_id).first()
if not country:
    raise HTTPException(status_code=400, detail="Invalid country ID")
```

### **Soft Delete (Never Hard Delete)**

```python
user.is_deleted = True
user.deleted_date = datetime.utcnow()
user.deleted_by = current_user.user_id
db.commit()
```

### **Log to Audit Table**

```python
audit_log = ActivityLog(
    user_id=current_user.user_id,
    company_id=current_user.company_id,
    action='user.profile.updated',
    entity_type='User',
    entity_id=user_id,
    old_value=json.dumps({'first_name': old_name}),
    new_value=json.dumps({'first_name': new_name}),
    created_date=datetime.utcnow()
)
db.add(audit_log)
db.commit()
```

---

## 🚨 Security Checklist

**Every Endpoint MUST:**
- [ ] Require authentication (JWT token)
- [ ] Enforce authorization (role check)
- [ ] Filter by `CompanyID` (multi-tenant)
- [ ] Validate input (Pydantic schema)
- [ ] Use parameterized queries (SQLAlchemy ORM)
- [ ] Log security events (audit table)
- [ ] Return appropriate HTTP status (401, 403, 404)

---

## 📚 Related Documentation

- **Full Guide:** `docs/technical-guides/backend-database-abstraction-layer.md`
- **Solution Architecture:** `docs/solution-architecture.md`
- **ADR-002:** Backend Abstraction Layer Design
- **ADR-003:** Naming Convention Strategy

---

**Winston** 🏗️  
*"Consistency beats cleverness. Use these patterns everywhere."*

