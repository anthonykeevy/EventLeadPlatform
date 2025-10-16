# Backend Database Abstraction Layer - Naming Convention Isolation

**Date:** October 16, 2025  
**Author:** Solomon 📜 (Database Migration Validator)  
**Question:** How do we prevent database naming conventions (PascalCase) from leaking to the frontend?

---

## 🎯 **SHORT ANSWER**

**YES** - You should absolutely create an abstraction layer that transforms database naming conventions before they reach the frontend.

**Architecture:**
```
Database (SQL)          Backend (Python)           Frontend (TypeScript)
PascalCase          →   snake_case            →    camelCase
UserID              →   user_id               →    userId
CompanyName         →   company_name          →    companyName
```

This is achieved through **3 layers**:
1. **SQLAlchemy Models** (map database columns to Python properties)
2. **Pydantic Schemas** (define API contracts with camelCase)
3. **Response Transformers** (auto-convert naming conventions)

---

## 📊 **THE PROBLEM**

### **Without Abstraction Layer:**

**Database Schema (SQL Server):**
```sql
CREATE TABLE [dbo].[User] (
    UserID BIGINT PRIMARY KEY,
    FirstName NVARCHAR(100),
    LastName NVARCHAR(100),
    EmailAddress NVARCHAR(255)
);
```

**Backend API Response (BAD - exposes database names):**
```json
{
  "UserID": 123,
  "FirstName": "John",
  "LastName": "Doe",
  "EmailAddress": "john@example.com"
}
```

**Frontend Code (BAD - tightly coupled to database):**
```typescript
// Frontend is now coupled to SQL naming conventions
const userName = user.FirstName + " " + user.LastName;
const email = user.EmailAddress;

// If you rename database column, frontend breaks! 🚨
```

**Problems:**
- ❌ Frontend tightly coupled to database schema
- ❌ Database refactoring breaks frontend
- ❌ Inconsistent naming conventions across layers
- ❌ Violates separation of concerns
- ❌ Poor developer experience (mixing conventions)

---

## ✅ **THE SOLUTION: 3-LAYER ABSTRACTION**

### **Layer 1: SQLAlchemy Models (Database → Python)**

**Purpose:** Map SQL Server columns (PascalCase) to Python properties (snake_case)

**File:** `backend/models/user.py`

```python
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    """
    SQLAlchemy model - Maps SQL Server columns to Python properties
    Database uses PascalCase, Python uses snake_case
    """
    __tablename__ = 'User'
    __table_args__ = {'schema': 'dbo'}
    
    # =====================================================================
    # Map SQL Server columns (PascalCase) to Python properties (snake_case)
    # =====================================================================
    
    # Primary Key
    user_id = Column('UserID', BigInteger, primary_key=True, autoincrement=True)
    
    # Authentication
    email = Column('Email', String(255), nullable=False, unique=True)
    password_hash = Column('PasswordHash', String(500), nullable=False)
    
    # Profile
    first_name = Column('FirstName', String(100), nullable=False)
    last_name = Column('LastName', String(100), nullable=False)
    phone = Column('Phone', String(20), nullable=True)
    role_title = Column('RoleTitle', String(100), nullable=True)
    profile_picture_url = Column('ProfilePictureUrl', String(500), nullable=True)
    timezone_identifier = Column('TimezoneIdentifier', String(50), nullable=False, default='Australia/Sydney')
    
    # Status & Account State
    status_id = Column('StatusID', BigInteger, nullable=False)
    is_email_verified = Column('IsEmailVerified', Boolean, nullable=False, default=False)
    email_verified_at = Column('EmailVerifiedAt', DateTime, nullable=True)
    is_locked = Column('IsLocked', Boolean, nullable=False, default=False)
    locked_until = Column('LockedUntil', DateTime, nullable=True)
    failed_login_attempts = Column('FailedLoginAttempts', Integer, nullable=False, default=0)
    last_login_date = Column('LastLoginDate', DateTime, nullable=True)
    last_password_change = Column('LastPasswordChange', DateTime, nullable=True)
    
    # Session Management
    session_token = Column('SessionToken', String(255), nullable=True)
    access_token_version = Column('AccessTokenVersion', Integer, nullable=False, default=1)
    refresh_token_version = Column('RefreshTokenVersion', Integer, nullable=False, default=1)
    
    # Onboarding
    onboarding_complete = Column('OnboardingComplete', Boolean, nullable=False, default=False)
    onboarding_step = Column('OnboardingStep', Integer, nullable=False, default=1)
    
    # Foreign Keys
    country_id = Column('CountryID', BigInteger, nullable=True)
    preferred_language_id = Column('PreferredLanguageID', BigInteger, nullable=True)
    user_role_id = Column('UserRoleID', BigInteger, nullable=True)
    
    # Audit Trail
    created_date = Column('CreatedDate', DateTime, nullable=False, default=datetime.utcnow)
    created_by = Column('CreatedBy', BigInteger, nullable=True)
    updated_date = Column('UpdatedDate', DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column('UpdatedBy', BigInteger, nullable=True)
    is_deleted = Column('IsDeleted', Boolean, nullable=False, default=False)
    deleted_date = Column('DeletedDate', DateTime, nullable=True)
    deleted_by = Column('DeletedBy', BigInteger, nullable=True)
    
    def __repr__(self):
        return f"<User(user_id={self.user_id}, email='{self.email}', first_name='{self.first_name}')>"
```

**Key Points:**
- ✅ Column name mapping: `user_id = Column('UserID', ...)`
- ✅ Python code uses `user.user_id` (snake_case)
- ✅ Database stores in `UserID` column (PascalCase)
- ✅ SQLAlchemy handles the translation automatically

---

### **Layer 2: Pydantic Schemas (Python → JSON/Frontend)**

**Purpose:** Define API contracts with camelCase for frontend consumption

**File:** `backend/modules/auth/schemas.py`

```python
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional

class UserResponse(BaseModel):
    """
    API Response Schema - Uses camelCase for frontend
    """
    model_config = ConfigDict(
        # Automatically convert snake_case to camelCase
        alias_generator=lambda field_name: ''.join(
            word.capitalize() if i > 0 else word 
            for i, word in enumerate(field_name.split('_'))
        ),
        populate_by_name=True  # Allow both camelCase and snake_case
    )
    
    # Primary Key
    user_id: int = Field(..., description="Unique user identifier")
    
    # Profile
    email: EmailStr = Field(..., description="User email address")
    first_name: str = Field(..., min_length=1, max_length=100, description="First name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    role_title: Optional[str] = Field(None, max_length=100, description="Job title")
    profile_picture_url: Optional[str] = Field(None, max_length=500, description="Avatar URL")
    timezone_identifier: str = Field(default='Australia/Sydney', description="IANA timezone")
    
    # Status
    is_email_verified: bool = Field(..., description="Email verification status")
    email_verified_at: Optional[datetime] = Field(None, description="When email was verified")
    is_locked: bool = Field(..., description="Account lock status")
    locked_until: Optional[datetime] = Field(None, description="Lock expiry time")
    
    # Onboarding
    onboarding_complete: bool = Field(..., description="Onboarding completion status")
    onboarding_step: int = Field(..., ge=1, description="Current onboarding step")
    
    # Audit
    created_date: datetime = Field(..., description="Account creation timestamp")
    last_login_date: Optional[datetime] = Field(None, description="Last successful login")
    
    # Relationships (optional - expand as needed)
    country_id: Optional[int] = None
    preferred_language_id: Optional[int] = None
    user_role_id: Optional[int] = None


class UserCreateRequest(BaseModel):
    """
    API Request Schema - Accepts camelCase from frontend
    """
    model_config = ConfigDict(
        alias_generator=lambda field_name: ''.join(
            word.capitalize() if i > 0 else word 
            for i, word in enumerate(field_name.split('_'))
        ),
        populate_by_name=True
    )
    
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    timezone_identifier: str = Field(default='Australia/Sydney')


class UserUpdateRequest(BaseModel):
    """
    API Update Schema - Partial updates with camelCase
    """
    model_config = ConfigDict(
        alias_generator=lambda field_name: ''.join(
            word.capitalize() if i > 0 else word 
            for i, word in enumerate(field_name.split('_'))
        ),
        populate_by_name=True
    )
    
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    role_title: Optional[str] = Field(None, max_length=100)
    profile_picture_url: Optional[str] = Field(None, max_length=500)
    timezone_identifier: Optional[str] = None
```

**Key Points:**
- ✅ `alias_generator`: Auto-converts snake_case to camelCase
- ✅ Frontend receives: `{ "userId": 123, "firstName": "John" }`
- ✅ Python code uses: `user.user_id`, `user.first_name`
- ✅ Type safety with Pydantic validation

---

### **Layer 3: Service Layer (Business Logic)**

**Purpose:** Orchestrate database operations with clean Python code

**File:** `backend/modules/auth/service.py`

```python
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.modules.auth.schemas import UserResponse, UserCreateRequest, UserUpdateRequest
from backend.common.security import hash_password
from datetime import datetime
from typing import Optional

class UserService:
    """
    Service layer - Business logic with Python naming conventions
    """
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreateRequest) -> UserResponse:
        """
        Create new user - Notice clean Python naming throughout
        """
        # Hash password
        password_hash = hash_password(user_data.password)
        
        # Create SQLAlchemy model (Python snake_case)
        new_user = User(
            email=user_data.email,
            password_hash=password_hash,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone=user_data.phone,
            timezone_identifier=user_data.timezone_identifier,
            status_id=2,  # 'pending' status (email not verified yet)
            is_email_verified=False,
            onboarding_complete=False,
            onboarding_step=1,
            created_date=datetime.utcnow()
        )
        
        # Save to database (SQLAlchemy maps to PascalCase columns)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Return Pydantic schema (converts to camelCase for API)
        return UserResponse.model_validate(new_user)
    
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[UserResponse]:
        """
        Get user by ID - Notice Python naming in code
        """
        user = db.query(User).filter(User.user_id == user_id).first()
        
        if user:
            return UserResponse.model_validate(user)
        return None
    
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdateRequest) -> Optional[UserResponse]:
        """
        Update user - Notice Python naming throughout
        """
        user = db.query(User).filter(User.user_id == user_id).first()
        
        if not user:
            return None
        
        # Update fields (Python snake_case)
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        # Audit trail
        user.updated_date = datetime.utcnow()
        
        db.commit()
        db.refresh(user)
        
        return UserResponse.model_validate(user)
    
    
    @staticmethod
    def verify_email(db: Session, user_id: int) -> Optional[UserResponse]:
        """
        Mark email as verified - Notice clean Python naming
        """
        user = db.query(User).filter(User.user_id == user_id).first()
        
        if not user:
            return None
        
        # Update verification status
        user.is_email_verified = True
        user.email_verified_at = datetime.utcnow()
        user.status_id = 1  # 'active' status
        user.updated_date = datetime.utcnow()
        
        db.commit()
        db.refresh(user)
        
        return UserResponse.model_validate(user)
```

**Key Points:**
- ✅ All Python code uses snake_case
- ✅ No SQL naming conventions visible
- ✅ Clean, Pythonic code
- ✅ Database mapping handled by SQLAlchemy

---

### **Layer 4: API Router (HTTP Endpoints)**

**File:** `backend/modules/auth/router.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.common.database import get_db
from backend.modules.auth.schemas import UserResponse, UserCreateRequest, UserUpdateRequest
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
      "lastName": "Doe",
      "phone": "+61412345678",
      "timezoneIdentifier": "Australia/Sydney"
    }
    
    Response (camelCase to frontend):
    {
      "userId": 123,
      "email": "john@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "isEmailVerified": false,
      "onboardingComplete": false,
      "createdDate": "2025-10-16T10:30:00Z"
    }
    """
    return UserService.create_user(db, user_data)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get user by ID
    
    Response (camelCase to frontend):
    {
      "userId": 123,
      "firstName": "John",
      "lastName": "Doe",
      "email": "john@example.com"
    }
    """
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdateRequest, db: Session = Depends(get_db)):
    """
    Update user profile
    
    Request body (camelCase from frontend):
    {
      "firstName": "Jane",
      "roleTitle": "Senior Marketing Manager"
    }
    """
    user = UserService.update_user(db, user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
```

---

## 🌐 **FRONTEND CONSUMPTION**

### **TypeScript Interface (Auto-generated from Pydantic)**

**File:** `frontend/src/types/user.ts`

```typescript
/**
 * User type - camelCase (JavaScript convention)
 * Matches backend UserResponse schema
 */
export interface User {
  userId: number;
  email: string;
  firstName: string;
  lastName: string;
  phone: string | null;
  roleTitle: string | null;
  profilePictureUrl: string | null;
  timezoneIdentifier: string;
  isEmailVerified: boolean;
  emailVerifiedAt: string | null;
  isLocked: boolean;
  lockedUntil: string | null;
  onboardingComplete: boolean;
  onboardingStep: number;
  createdDate: string;
  lastLoginDate: string | null;
  countryId: number | null;
  preferredLanguageId: number | null;
  userRoleId: number | null;
}

export interface CreateUserRequest {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  phone?: string;
  timezoneIdentifier?: string;
}

export interface UpdateUserRequest {
  firstName?: string;
  lastName?: string;
  phone?: string;
  roleTitle?: string;
  profilePictureUrl?: string;
  timezoneIdentifier?: string;
}
```

---

### **React Component (Clean camelCase)**

**File:** `frontend/src/features/auth/UserProfile.tsx`

```typescript
import React, { useEffect, useState } from 'react';
import { User } from '@/types/user';
import { api } from '@/lib/api';

export const UserProfile: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  
  useEffect(() => {
    // Fetch user from API (receives camelCase)
    api.get<User>('/api/v1/users/123')
      .then(response => {
        setUser(response.data);
        
        // Notice: Clean JavaScript naming, no SQL conventions!
        console.log('User ID:', response.data.userId);
        console.log('Full Name:', `${response.data.firstName} ${response.data.lastName}`);
        console.log('Email Verified:', response.data.isEmailVerified);
      });
  }, []);
  
  if (!user) return <div>Loading...</div>;
  
  return (
    <div className="profile-card">
      <img src={user.profilePictureUrl || '/default-avatar.png'} alt="Profile" />
      
      <h2>{user.firstName} {user.lastName}</h2>
      
      {user.roleTitle && <p className="role-title">{user.roleTitle}</p>}
      
      <p className="email">{user.email}</p>
      
      {user.isEmailVerified ? (
        <span className="badge badge-success">✓ Email Verified</span>
      ) : (
        <span className="badge badge-warning">⚠ Email Not Verified</span>
      )}
      
      <div className="onboarding-progress">
        <p>Onboarding: Step {user.onboardingStep}</p>
        {user.onboardingComplete && <span>✅ Complete</span>}
      </div>
    </div>
  );
};
```

**Key Points:**
- ✅ Frontend uses camelCase (JavaScript convention)
- ✅ No SQL naming conventions visible
- ✅ Clean, idiomatic TypeScript code
- ✅ Type-safe with TypeScript interfaces

---

## 🔄 **DATA FLOW SUMMARY**

```
┌──────────────────────────────────────────────────────────────────┐
│                        DATA TRANSFORMATION FLOW                   │
└──────────────────────────────────────────────────────────────────┘

Database (SQL Server):
  Column: UserID (PascalCase)
      ↓
SQLAlchemy Model (Python):
  Property: user_id (snake_case)
  Mapping: user_id = Column('UserID', BigInteger)
      ↓
Service Layer (Python):
  Variable: user.user_id (snake_case)
  Code: user = db.query(User).filter(User.user_id == 123).first()
      ↓
Pydantic Schema (JSON API):
  Field: userId (camelCase)
  Alias: alias_generator converts snake_case → camelCase
      ↓
Frontend (TypeScript):
  Property: user.userId (camelCase)
  Code: console.log(user.userId, user.firstName)
```

---

## ✅ **BENEFITS OF THIS ARCHITECTURE**

### **1. Separation of Concerns**
- ✅ Database schema changes don't affect frontend
- ✅ Each layer uses its own naming convention
- ✅ Clear boundaries between layers

### **2. Flexibility**
- ✅ Rename database columns without breaking frontend
- ✅ Change API response format without database migration
- ✅ Support multiple API versions with different naming

### **3. Developer Experience**
- ✅ Backend devs use Pythonic snake_case
- ✅ Frontend devs use JavaScript camelCase
- ✅ Database follows SQL Server standards (PascalCase)
- ✅ No mixing of conventions in any layer

### **4. Maintainability**
- ✅ Each layer is independently testable
- ✅ Clear transformation rules
- ✅ Type safety at every layer

### **5. Compliance with Standards**
- ✅ Database: SQL Server naming standards (Anthony's rules)
- ✅ Python: PEP 8 naming conventions
- ✅ JavaScript/TypeScript: Airbnb style guide
- ✅ REST API: JSON convention (camelCase)

---

## 🛠️ **IMPLEMENTATION CHECKLIST**

### **For Each Database Table:**

- [ ] Create SQLAlchemy model with column name mapping
  ```python
  user_id = Column('UserID', BigInteger, primary_key=True)
  first_name = Column('FirstName', String(100), nullable=False)
  ```

- [ ] Create Pydantic response schema with camelCase alias
  ```python
  class UserResponse(BaseModel):
      model_config = ConfigDict(alias_generator=to_camel_case)
      user_id: int
      first_name: str
  ```

- [ ] Create Pydantic request schema for API input
  ```python
  class UserCreateRequest(BaseModel):
      model_config = ConfigDict(alias_generator=to_camel_case)
      email: EmailStr
      first_name: str
  ```

- [ ] Create service layer methods with Python naming
  ```python
  def create_user(db: Session, user_data: UserCreateRequest) -> UserResponse:
      new_user = User(first_name=user_data.first_name)
  ```

- [ ] Create API routes with proper response models
  ```python
  @router.post("/users", response_model=UserResponse)
  def create_user(user_data: UserCreateRequest):
  ```

- [ ] Generate TypeScript types from Pydantic schemas
  ```bash
  # Use pydantic2ts or similar tool
  pydantic2ts --module backend.modules.auth.schemas --output frontend/src/types/
  ```

---

## 🚀 **HELPER UTILITY**

**File:** `backend/common/schemas.py`

```python
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
    populate_by_name=True,  # Allow both camelCase and snake_case
    from_attributes=True    # Allow ORM model conversion
)
```

**Usage in schemas:**
```python
from backend.common.schemas import CamelCaseConfig

class UserResponse(BaseModel):
    model_config = CamelCaseConfig
    
    user_id: int
    first_name: str
    # API will output: {"userId": 123, "firstName": "John"}
```

---

## 📊 **NAMING CONVENTION REFERENCE**

| Layer | Convention | Example | When to Use |
|-------|-----------|---------|-------------|
| **SQL Server** | PascalCase | `UserID`, `FirstName`, `CompanyName` | Table/column definitions |
| **SQLAlchemy** | snake_case | `user_id`, `first_name`, `company_name` | Python model properties |
| **Pydantic** | snake_case | `user_id: int` | Schema field definitions |
| **JSON API** | camelCase | `{"userId": 123, "firstName": "John"}` | API request/response |
| **TypeScript** | camelCase | `user.userId`, `user.firstName` | Frontend code |
| **URL Params** | kebab-case | `/api/users/user-id` | REST API endpoints (optional) |

---

## 🎯 **FINAL ANSWER TO YOUR QUESTION**

### **"Can we prevent database naming conventions from leaking to frontend?"**

**YES!** Here's the solution:

1. **SQLAlchemy Models**: Map database columns (PascalCase) to Python properties (snake_case)
   ```python
   user_id = Column('UserID', BigInteger, primary_key=True)
   ```

2. **Pydantic Schemas**: Auto-convert Python properties (snake_case) to JSON fields (camelCase)
   ```python
   model_config = ConfigDict(alias_generator=to_camel_case)
   ```

3. **Service Layer**: Write clean Python code with snake_case
   ```python
   user = db.query(User).filter(User.user_id == 123).first()
   ```

4. **API Layer**: Return Pydantic schemas (auto-converted to camelCase)
   ```python
   @router.get("/users/{user_id}", response_model=UserResponse)
   ```

5. **Frontend**: Consume camelCase JSON with TypeScript types
   ```typescript
   console.log(user.userId, user.firstName);
   ```

**Result:** Each layer uses its own naming convention, with automatic translation between layers. Database refactoring never breaks frontend! ✅

---

**Solomon** 📜  
*"Build walls between layers. Let each layer speak its own language."*

