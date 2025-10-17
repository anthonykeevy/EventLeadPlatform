# Import Path Issue - Resolution Plan

**Date:** October 18, 2025  
**Issue:** Backend fails to start due to circular import issues  
**Root Cause:** Mixed import styles causing SQLAlchemy model circular imports  
**Status:** Partial fix applied, systematic resolution needed  

---

## Problem Description

The codebase has **189 files** with inconsistent import styles:

### Import Style A (Absolute from project root):
```python
from backend.models.user import User
from backend.common.database import SessionLocal
```

### Import Style B (Relative from backend directory):
```python
from models.user import User
from common.database import SessionLocal
```

When these styles are mixed, it creates **circular imports** that cause SQLAlchemy to fail with:
```
sqlalchemy.exc.InvalidRequestError: Table 'dbo.User' is already defined for this MetaData instance
```

---

## Files Fixed (9 files)

✅ **Middleware** (3 files):
- `backend/middleware/request_logger.py`
- `backend/middleware/auth.py`
- `backend/middleware/exception_handler.py`

✅ **Model __init__.py files** (5 files):
- `backend/models/ref/__init__.py`
- `backend/models/config/__init__.py`
- `backend/models/cache/__init__.py`
- `backend/models/log/__init__.py`
- `backend/models/audit/__init__.py`

✅ **Common** (1 file):
- `backend/common/config_service.py`

---

## Remaining Files to Fix (~180 files)

Files still using `backend.` prefix that need conversion to relative imports:

### High Priority (blocks startup):
- `backend/modules/auth/router.py` (lines 13, 14, 29, etc.)
- `backend/modules/auth/user_service.py` (line 11)
- `backend/modules/auth/token_service.py` (line 12-15)
- `backend/modules/invitations/*.py`
- `backend/modules/companies/*.py`
- `backend/modules/users/*.py`

### Medium Priority (needed for runtime):
- `backend/services/email_service.py`
- `backend/common/validators.py`
- All `backend/modules/*/service.py` files

### Low Priority (tests can use backend. prefix):
- `backend/tests/*.py` (can keep `backend.` prefix as tests run from project root)

---

## Solution Strategy

### Option 1: Systematic Fix (Recommended)
**Run automated find-replace across all non-test Python files:**

```powershell
# Find all files with backend. imports (excluding tests)
Get-ChildItem -Path backend -Filter *.py -Recurse | 
    Where-Object { $_.FullName -notlike "*\tests\*" -and $_.FullName -notlike "*\venv\*" } |
    ForEach-Object {
        $content = Get-Content $_.FullName -Raw
        if ($content -match "from backend\.") {
            Write-Host "Found: $($_.FullName)"
        }
    }
```

**Conversion Rules:**
| Old Import | New Import |
|------------|-----------|
| `from backend.models.` | `from models.` |
| `from backend.common.` | `from common.` |
| `from backend.modules.` | `from modules.` |
| `from backend.services.` | `from services.` |
| `from backend.middleware.` | `from middleware.` |
| `from backend.config.` | `from config.` |

**DON'T change these:**
- Test files (`backend/tests/*.py`) - they need `backend.` prefix
- `backend/models/*` files that import `from backend.common.database import Base` - change to `from common.database import Base`

### Option 2: Quick Workaround (Temporary)
Add this at the top of `backend/main.py`:
```python
import sys
import os
# Ensure consistent import resolution
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
# Also add project root for backend.* imports
project_root = os.path.dirname(backend_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
```

**Note:** This is a workaround and may cause other issues. Option 1 is preferred.

---

## Testing After Fix

1. **Test import:**
   ```powershell
   cd C:\Users\tonyk\OneDrive\Projects\EventLeadPlatform
   python -c "import backend.main as main; print('✅ Success!')"
   ```

2. **Start backend:**
   ```powershell
   cd backend
   python -m uvicorn main:app --reload
   ```

3. **Test API:**
   ```powershell
   curl http://localhost:8000/health
   ```

4. **Run tests:**
   ```powershell
   cd backend
   python -m pytest tests/ -v
   ```

---

## Commit Message Template

```
Fix: Resolve circular import issues (partial - 9 files)

Fixed import paths in middleware and model __init__.py files
to use relative imports instead of backend. prefix.

Files fixed:
- backend/middleware/*.py (3 files)
- backend/models/*/__init__.py (5 files)  
- backend/common/config_service.py

Remaining: ~180 files in modules/, services/ still need fixing.
See docs/IMPORT-PATH-ISSUE-RESOLUTION.md for complete resolution plan.

Issue: Mixed import styles causing SQLAlchemy circular imports
Impact: Backend won't start until all files use consistent relative imports
```

---

## Prevention

### Going Forward:
1. **Always use relative imports** within the backend codebase:
   ```python
   # ✅ CORRECT
   from models.user import User
   from common.database import SessionLocal
   
   # ❌ WRONG (causes circular imports)
   from backend.models.user import User
   from backend.common.database import SessionLocal
   ```

2. **Tests are the exception** - they can use `backend.` prefix since they run from project root:
   ```python
   # In backend/tests/*.py - this is OK
   from backend.models.user import User
   ```

3. **Update linting rules** to catch this:
   ```yaml
   # In .pylintrc or similar
   [IMPORTS]
   preferred-modules=
       backend.models:models,
       backend.common:common,
       backend.modules:modules
   ```

---

## Related Issues

- Story 0.2: Originally reported middleware import issue
- Story 1.13: Config service added more imports, exposed the issue
- Conftest.py: Already fixed to add project root to sys.path for tests

---

## Contact

**Issue Discovered By:** Story 1.13 UAT Testing Attempt  
**Tracked In:** This document  
**Resolution Needed Before:** Backend can start for UAT

