# ADR-003: Cross-Layer Naming Convention Strategy

**Status:** Accepted  
**Date:** 2025-10-16  
**Deciders:** Anthony Keevy (Product Owner), Winston (Architect)  
**Context:** Epic 1 - Authentication & Onboarding

---

## Context and Problem Statement

EventLeadPlatform spans three technology layers: SQL Server database, Python FastAPI backend, and TypeScript React frontend. Each layer has its own industry-standard naming conventions.

**Key Problem:** Should we enforce a single naming convention across all layers, or allow each layer to use its native convention?

**Key Questions:**
- Should database PascalCase (UserID) propagate to frontend?
- Should Python snake_case (user_id) be used in JSON APIs?
- How do we prevent confusion when the same field has different names in different layers?
- What's the performance cost of name transformation?

**Constraints:**
- Must follow industry best practices for each technology
- Must maintain code readability and developer productivity
- Must support future refactoring without breaking changes
- Must be teachable to new developers joining the project

---

## Decision Drivers

1. **Developer Productivity:** Developers should use familiar conventions for their layer
2. **Code Readability:** Each layer's code should look idiomatic (not foreign)
3. **Industry Standards:** Follow established conventions (SQL Server, PEP 8, JavaScript)
4. **Maintainability:** Clear transformation rules prevent confusion
5. **Tooling Support:** Linters, formatters, and IDEs expect standard conventions
6. **Team Independence:** Database team, backend team, frontend team work independently

---

## Considered Options

### **Option A: Single Convention Across All Layers**

**Variant 1: PascalCase everywhere**
```sql
-- Database
SELECT UserID, FirstName FROM User;
```
```python
# Backend
user.UserID  # ❌ Violates PEP 8
```
```typescript
// Frontend
user.UserID  // ❌ Violates JavaScript conventions
```

**Variant 2: camelCase everywhere**
```sql
-- Database
SELECT userId, firstName FROM user;  -- ❌ Violates SQL Server conventions
```
```python
# Backend
user.userId  # ❌ Violates PEP 8
```
```typescript
// Frontend
user.userId  // ✅ Correct
```

**Variant 3: snake_case everywhere**
```sql
-- Database
SELECT user_id, first_name FROM user;  -- ❌ Violates Anthony's standards
```
```python
# Backend
user.user_id  # ✅ Correct (PEP 8)
```
```typescript
// Frontend
user.user_id  // ❌ Violates JavaScript conventions
```

**Pros:**
- ✅ Consistent naming across all layers
- ✅ No transformation needed

**Cons:**
- ❌ Violates industry best practices for at least 2 of 3 layers
- ❌ Code looks unidiomatic in non-matching layers
- ❌ Linters/formatters complain (or must be disabled)
- ❌ Confusing for developers experienced in those technologies
- ❌ Harder to hire developers (must unlearn conventions)

---

### **Option B: Native Conventions with Manual Mapping**

Each layer uses its own convention, but developers manually map at boundaries.

```python
# Backend manually converts for API
@router.get("/users/{id}")
def get_user(id: int):
    user = db.query(User).filter(User.UserID == id).first()
    return {
        "userId": user.UserID,        # Manual conversion
        "firstName": user.FirstName,
        "lastName": user.LastName
    }
```

**Pros:**
- ✅ Each layer uses native convention
- ✅ Explicit transformation (clear what's happening)

**Cons:**
- ❌ Extremely error-prone (easy to forget fields or make typos)
- ❌ High maintenance burden (update every endpoint when schema changes)
- ❌ No type safety (runtime errors only)
- ❌ Inconsistent (developers will do it differently)

---

### **Option C: Native Conventions with Automatic Transformation** ⭐ **CHOSEN**

Each layer uses its own native convention, with automatic transformation at boundaries.

```
┌──────────────────────────────────────────────────────────┐
│         TRANSFORMATION STRATEGY                           │
└──────────────────────────────────────────────────────────┘

Database Layer (SQL Server):
  Convention: PascalCase
  Example: UserID, FirstName, CompanyName, IsActive
  Reason: SQL Server standard, Anthony's requirement
  
    ↓ [SQLAlchemy Column Mapping]
    
Backend Layer (Python):
  Convention: snake_case
  Example: user_id, first_name, company_name, is_active
  Reason: PEP 8 standard (official Python style guide)
  
    ↓ [Pydantic alias_generator]
    
API Layer (JSON):
  Convention: camelCase
  Example: userId, firstName, companyName, isActive
  Reason: JavaScript/JSON standard (REST API best practice)
  
    ↓ [TypeScript interfaces]
    
Frontend Layer (TypeScript):
  Convention: camelCase
  Example: user.userId, user.firstName, user.isActive
  Reason: JavaScript/TypeScript standard (industry convention)
```

**Transformation Mechanisms:**
- **Database → Python:** SQLAlchemy column name mapping
- **Python → JSON:** Pydantic `alias_generator` function
- **JSON → TypeScript:** No transformation needed (both camelCase)

**Pros:**
- ✅ Each layer uses its native convention (idiomatic code everywhere)
- ✅ Automatic transformation (DRY principle, no manual mapping)
- ✅ Type-safe (compile-time errors for mismatches)
- ✅ Maintainable (transformation rules defined once)
- ✅ Standards-compliant (SQL Server, PEP 8, JavaScript all followed)
- ✅ Team independence (database changes don't ripple to frontend)

**Cons:**
- ⚠️ Requires understanding of transformation rules
- ⚠️ Same field has different names in different layers (but predictable)

---

## Decision Outcome

**Chosen Option:** Option C - Native Conventions with Automatic Transformation

**Rationale:**
- Developer productivity is highest when using familiar conventions
- Industry standards exist for a reason (tooling, libraries, team conventions)
- Automatic transformation eliminates error-prone manual mapping
- Clear, documented transformation rules prevent confusion
- Each team can work independently without crossing into other layers' conventions

---

## Naming Convention Rules

### **1. Database Layer (SQL Server)**

**Convention:** PascalCase  
**Standard Source:** Anthony's Database Standards + SQL Server Best Practices

| Pattern | Rule | Examples |
|---------|------|----------|
| **Tables** | Singular noun, PascalCase | `User`, `Company`, `Form`, `Event` |
| **Columns** | PascalCase | `UserID`, `FirstName`, `EmailAddress` |
| **Primary Keys** | `[TableName]ID` | `UserID`, `CompanyID`, `FormID` |
| **Foreign Keys** | `[ReferencedTableName]ID` | `CompanyID`, `UserRoleID`, `CountryID` |
| **Booleans** | `Is` or `Has` prefix | `IsActive`, `IsDeleted`, `HasAccess` |
| **Dates** | Descriptive suffix | `CreatedDate`, `UpdatedDate`, `ExpiresAt` |
| **Constraints** | `[Type]_[TableName]_[ColumnNames]` | `PK_User_UserID`, `FK_User_Country`, `UQ_User_Email` |
| **Indexes** | `IX_[TableName]_[ColumnNames]` | `IX_User_Email`, `IX_Form_CompanyID` |
| **Schemas** | Lowercase | `dbo`, `ref`, `config`, `log`, `audit`, `cache` |

**Examples:**
```sql
CREATE TABLE [dbo].[User] (
    UserID BIGINT IDENTITY(1,1) PRIMARY KEY,
    Email NVARCHAR(255) NOT NULL,
    FirstName NVARCHAR(100) NOT NULL,
    LastName NVARCHAR(100) NOT NULL,
    IsEmailVerified BIT NOT NULL DEFAULT 0,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CONSTRAINT FK_User_Country FOREIGN KEY (CountryID) REFERENCES [ref].[Country](CountryID),
    CONSTRAINT UQ_User_Email UNIQUE (Email)
);
```

---

### **2. Backend Layer (Python)**

**Convention:** snake_case  
**Standard Source:** PEP 8 (Python Enhancement Proposal 8 - official style guide)

| Pattern | Rule | Examples |
|---------|------|----------|
| **Variables** | snake_case | `user_id`, `first_name`, `is_active` |
| **Functions** | snake_case | `get_user_by_id()`, `create_company()`, `verify_password()` |
| **Classes** | PascalCase | `User`, `UserService`, `AuthMiddleware` |
| **Constants** | SCREAMING_SNAKE_CASE | `MAX_LOGIN_ATTEMPTS`, `TOKEN_EXPIRY_MINUTES` |
| **Private** | Leading underscore | `_validate_token()`, `_hash_password()` |
| **File names** | snake_case | `user_service.py`, `auth_middleware.py` |
| **Pydantic Models** | PascalCase class, snake_case fields | `UserResponse`, `CreateUserRequest` |

**Examples:**
```python
# SQLAlchemy Model
class User(Base):
    __tablename__ = 'User'
    user_id = Column('UserID', BigInteger, primary_key=True)
    first_name = Column('FirstName', String(100), nullable=False)
    is_email_verified = Column('IsEmailVerified', Boolean, default=False)


# Pydantic Schema
class UserResponse(BaseModel):
    model_config = CamelCaseConfig
    user_id: int
    first_name: str
    is_email_verified: bool


# Service Class
class UserService:
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[UserResponse]:
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            return UserResponse.model_validate(user)
        return None


# Constants
MAX_LOGIN_ATTEMPTS = 5
TOKEN_EXPIRY_MINUTES = 15
```

---

### **3. API Layer (JSON)**

**Convention:** camelCase  
**Standard Source:** JavaScript/JSON Community Standard (Google JSON Style Guide, Airbnb)

| Pattern | Rule | Examples |
|---------|------|----------|
| **Fields** | camelCase | `userId`, `firstName`, `isEmailVerified` |
| **Booleans** | `is` or `has` prefix | `isActive`, `hasAccess`, `isEmailVerified` |
| **Arrays** | Plural noun | `users`, `companies`, `forms` |
| **Objects** | Singular noun | `user`, `company`, `form` |
| **Dates** | ISO 8601 format | `"2025-10-16T10:30:00Z"` |

**Examples:**
```json
{
  "userId": 123,
  "email": "john@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "isEmailVerified": true,
  "isLocked": false,
  "createdDate": "2025-10-16T10:30:00Z",
  "companies": [
    {
      "companyId": 456,
      "companyName": "Acme Corp",
      "isActive": true
    }
  ]
}
```

---

### **4. Frontend Layer (TypeScript)**

**Convention:** camelCase  
**Standard Source:** Airbnb JavaScript Style Guide + TypeScript Best Practices

| Pattern | Rule | Examples |
|---------|------|----------|
| **Variables** | camelCase | `userId`, `firstName`, `isActive` |
| **Functions** | camelCase | `getUserById()`, `createCompany()`, `verifyEmail()` |
| **Classes** | PascalCase | `User`, `AuthService`, `FormBuilder` |
| **Interfaces** | PascalCase | `User`, `Company`, `ApiResponse<T>` |
| **Types** | PascalCase | `UserId`, `CompanyRole`, `AuthToken` |
| **Constants** | SCREAMING_SNAKE_CASE | `MAX_FILE_SIZE`, `API_BASE_URL` |
| **React Components** | PascalCase | `LoginForm`, `UserProfile`, `EventCard` |
| **File names** | PascalCase for components, camelCase for utils | `LoginForm.tsx`, `userService.ts` |

**Examples:**
```typescript
// Interface
export interface User {
  userId: number;
  email: string;
  firstName: string;
  lastName: string;
  isEmailVerified: boolean;
  createdDate: string;
}

// React Component
export const UserProfile: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  
  useEffect(() => {
    const fetchUser = async () => {
      const userData = await api.get<User>('/api/users/123');
      setUser(userData);
    };
    fetchUser();
  }, []);
  
  if (!user) return <div>Loading...</div>;
  
  return (
    <div className="user-profile">
      <h2>{user.firstName} {user.lastName}</h2>
      <p>{user.email}</p>
      {user.isEmailVerified && <Badge>Verified</Badge>}
    </div>
  );
};

// Service
export const userService = {
  getUserById: async (userId: number): Promise<User> => {
    return api.get<User>(`/api/users/${userId}`);
  }
};

// Constants
const MAX_UPLOAD_SIZE = 5 * 1024 * 1024;  // 5MB
const API_BASE_URL = 'https://api.eventlead.com';
```

---

## Transformation Examples

### **Example 1: User Entity**

```
Database:           UserID, FirstName, LastName, IsEmailVerified
Python Model:       user_id, first_name, last_name, is_email_verified
JSON API:           userId, firstName, lastName, isEmailVerified
TypeScript:         userId, firstName, lastName, isEmailVerified
```

### **Example 2: Company Relationship**

```
Database:           CompanyID, CompanyName, UserCompanyRoleID, IsActive
Python Model:       company_id, company_name, user_company_role_id, is_active
JSON API:           companyId, companyName, userCompanyRoleId, isActive
TypeScript:         companyId, companyName, userCompanyRoleId, isActive
```

### **Example 3: Timestamp Fields**

```
Database:           CreatedDate, UpdatedDate, LastLoginDate
Python Model:       created_date, updated_date, last_login_date
JSON API:           createdDate, updatedDate, lastLoginDate
TypeScript:         createdDate, updatedDate, lastLoginDate
```

---

## Special Cases

### **1. Abbreviations**

| Database | Python | JSON/TypeScript | Notes |
|----------|--------|-----------------|-------|
| `ABN` | `abn` | `abn` | Keep lowercase (not `aBN`) |
| `URL` | `url` | `url` | Keep lowercase (not `uRL`) |
| `ID` | `id` | `id` | Lowercase when standalone |
| `CompanyID` | `company_id` | `companyId` | Normal transformation |

### **2. JSON Fields in Database**

```sql
-- Database: Store JSON as NVARCHAR(MAX)
DesignJSON NVARCHAR(MAX)
IntegrationConfig NVARCHAR(MAX)

-- Python: Use JSON type or dict
design_json: dict
integration_config: dict | None

-- JSON API: Parse as object
designJson: object
integrationConfig: object | null

-- TypeScript: Define interface
designJson: FormDesign
integrationConfig: IntegrationConfig | null
```

### **3. Boolean Fields**

Always use `is_` or `has_` prefix for clarity:

```
Database:           IsActive, HasAccess, IsEmailVerified
Python Model:       is_active, has_access, is_email_verified
JSON API:           isActive, hasAccess, isEmailVerified
TypeScript:         isActive, hasAccess, isEmailVerified
```

---

## Performance Considerations

**Transformation Overhead:**
- SQLAlchemy column mapping: **Zero runtime overhead** (compiled once at startup)
- Pydantic alias generation: **Negligible** (<1ms per request, happens once per response)
- TypeScript: **Zero overhead** (compile-time only, removed in production build)

**Benchmarks (on typical API request):**
- Database query: 10-50ms
- SQLAlchemy model instantiation: <1ms
- Pydantic serialization + camelCase conversion: <1ms
- Network latency: 20-100ms

**Conclusion:** Transformation overhead is <1% of total request time.

---

## Consequences

### **Positive:**

1. **Idiomatic code in every layer:**
   - SQL queries look like standard SQL Server code
   - Python code passes PEP 8 linters
   - JavaScript code passes ESLint with Airbnb config

2. **Team independence:**
   - Database team uses familiar SQL conventions
   - Backend team uses familiar Python conventions
   - Frontend team uses familiar JavaScript conventions
   - No need to "context switch" mentally

3. **Tooling support:**
   - Linters work without custom rules
   - Auto-formatters work correctly
   - IDE autocomplete works as expected

4. **Easier hiring:**
   - New developers see familiar conventions
   - No need to "unlearn" industry standards
   - Faster onboarding

### **Negative:**

1. **Same field has different names:**
   - `UserID` (database) vs `user_id` (Python) vs `userId` (frontend)
   - **Mitigation:** Transformation is predictable and documented

2. **Learning curve for transformation:**
   - Developers must understand SQLAlchemy column mapping
   - Must understand Pydantic alias_generator
   - **Mitigation:** This ADR + code templates + examples

3. **Debugging across layers:**
   - Must mentally transform names when tracing bugs
   - **Mitigation:** Logging includes both Python names (in code) and camelCase (in API logs)

---

## Compliance with Standards

**Industry Standards Followed:**
- ✅ SQL Server Naming Conventions (Microsoft documentation)
- ✅ PEP 8 (Python official style guide)
- ✅ Google JSON Style Guide (camelCase for JSON)
- ✅ Airbnb JavaScript Style Guide (camelCase for variables)

**Anthony's Database Standards:**
- ✅ PascalCase for tables and columns
- ✅ Self-documenting foreign keys ([ReferencedTable]ID)
- ✅ Is/Has prefix for booleans
- ✅ Audit column naming (CreatedDate, UpdatedBy, etc.)

**BMAD v6 Alignment:**
- ✅ Clear architectural decision documented
- ✅ Standards-based approach (not arbitrary)
- ✅ Forward-looking (scales to 100+ tables)

---

## References

- Solution Architecture: `docs/solution-architecture.md` (Backend Abstraction Layer Architecture section)
- ADR-002: Backend Abstraction Layer Design
- PEP 8 Style Guide: https://peps.python.org/pep-0008/
- Google JSON Style Guide: https://google.github.io/styleguide/jsoncstyleguide.xml
- Airbnb JavaScript Style Guide: https://github.com/airbnb/javascript
- SQL Server Naming Conventions: https://learn.microsoft.com/en-us/sql/relational-databases/tables/specify-computed-columns-in-a-table

---

## Approval

**Approved by:** Anthony Keevy  
**Date:** 2025-10-16  
**Status:** Accepted - Implemented in Epic 1

---

**Winston** 🏗️  
*"Let each layer speak its mother tongue. Translation happens at the border."*

