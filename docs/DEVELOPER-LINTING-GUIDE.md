# EventLead Platform - Custom Linting Rules
# Developer Experience Enhancement

## SQLAlchemy Type Suppressions
# These are common patterns in SQLAlchemy where Column types need to be converted
# to Python types for function calls. We suppress these specific warnings.

# Pattern 1: Column[int] -> int conversion
# Pattern 2: Column[str] -> str conversion  
# Pattern 3: Column[datetime] -> datetime conversion
# Pattern 4: Optional attribute access on SQLAlchemy models

## Custom Linting Rules for Epic 1

### Backend Rules:
- ✅ Suppress SQLAlchemy Column type conversion warnings
- ✅ Allow Optional attribute access on SQLAlchemy models
- ✅ Focus on actual logic errors, not type annotation issues
- ✅ Maintain type safety for business logic

### Frontend Rules:
- ✅ TypeScript strict mode enabled
- ✅ React component prop validation
- ✅ Hook dependency validation
- ✅ Accessibility attribute validation

### Database Rules:
- ✅ Migration file validation
- ✅ Schema naming consistency
- ✅ Foreign key constraint validation

## Epic 1 Specific Suppressions

### Files with SQLAlchemy type issues (acceptable):
- `backend/modules/auth/router.py` - JWT token generation with Column types
- `backend/modules/companies/router.py` - Company relationship queries
- `backend/modules/invitations/router.py` - Invitation token handling

### Rationale:
These files contain SQLAlchemy ORM queries where Column types are converted to Python types.
The type checker flags these as errors, but they're actually correct runtime behavior.
Suppressing these allows focus on actual logic errors.

## Developer Experience Improvements

### Added Tools:
1. **Diagnostic Log Tool** - `backend/diagnostic_logs.py`
2. **Audit Logging** - Comprehensive logging system
3. **Type-Safe API Patterns** - Consistent error handling
4. **Component Library** - Reusable UX components

### Custom Linting Benefits:
- Focus on actual bugs, not type annotation noise
- Faster development cycle
- Better developer experience
- Maintains code quality standards
