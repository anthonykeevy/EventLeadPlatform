# Story 1.15 Context - Lessons from Stories 1.14 & 1.18 UAT

**Date:** 2025-10-22  
**For:** Story 1.15 (Frontend Password Reset)  
**Purpose:** Apply lessons learned to prevent common UAT bugs

---

## 🎯 Key Lessons from UAT (Stories 1.14 & 1.18)

### **Pattern #1: snake_case ↔ camelCase Conversions**

**What Happened:**
- Backend returns: `company_name`, `is_primary`, `user_id`
- Frontend expects: `companyName`, `isPrimaryCompany`, `userId`
- Result: Data existed but didn't display

**For Story 1.15:**
✅ **Add transformation in API client immediately:**
```typescript
// In password reset API client
export async function requestPasswordReset(email: string) {
  const response = await apiClient.post('/api/auth/password-reset/request', { email })
  // Backend returns snake_case, transform to camelCase
  return {
    success: response.data.success,
    message: response.data.message,
    userId: response.data.user_id  // ← Transform here
  }
}
```

---

### **Pattern #2: Missing Model Imports**

**What Happened:**
- Code used `User` model but forgot `from models.user import User`
- Result: NameError crashes

**For Story 1.15:**
✅ **Verify imports at start of implementation:**
- Check all model imports in router files
- Run `grep "from models" backend/modules/auth/router.py` to verify

---

### **Pattern #3: Wrong Relationship Names**

**What Happened:**
- Used `user_company.user_company_role` instead of `user_company.role`
- Result: AttributeError

**For Story 1.15:**
✅ **Check SQLAlchemy relationship names:**
- Before using relationships, check model definition
- Use `relationship_name` as defined in model, not assumed name

---

### **Pattern #4: Transaction Management**

**What Happened:**
- Committed to database before all operations complete
- If later operation failed, data was orphaned

**For Story 1.15:**
✅ **Transaction best practices:**
```python
try:
    # All database operations
    # ...
    db.commit()  # ← Only at the end
    return success_response
except Exception as e:
    db.rollback()  # ← Always rollback on error
    raise HTTPException(...)
```

---

### **Pattern #5: Token Storage**

**What Happened:**
- Used wrong localStorage key: `access_token` instead of `eventlead_access_token`

**For Story 1.15:**
✅ **Always use utility functions:**
```typescript
import { getAccessToken, storeTokens, clearTokens } from '../utils/tokenStorage'
// Never directly access localStorage for tokens
```

---

## 🚀 Story 1.15 Quick Start Checklist

**Before Implementation:**
- [ ] Review backend endpoints in Story 1.4 (already complete)
- [ ] Note all response field names (snake_case)
- [ ] Plan camelCase transformations for frontend

**During Implementation:**
- [ ] Import tokenStorage utilities (don't use localStorage directly)
- [ ] Add snake_case → camelCase transformation in API client
- [ ] Verify all model imports
- [ ] Use try/catch with explicit rollback (if backend changes needed)

**During UAT:**
- [ ] Test with valid email (should receive reset link)
- [ ] Test with invalid/non-existent email
- [ ] Test expired token scenario
- [ ] Test token already used scenario

---

## 💡 PM Strategic Input

**Story 1.15 Risk Assessment:** 🟢 LOW

**Why Low Risk:**
1. Backend already complete and tested (Story 1.4)
2. Similar patterns to login/signup (Stories 1.9)
3. Isolated feature (doesn't affect other flows)
4. You now have UAT experience

**Recommended Approach:**
- Implement using proven patterns from Stories 1.9, 1.14
- Apply lessons learned (transformations, imports, utilities)
- Keep UAT testing lightweight (30-45 minutes)
- Focus on user flow: Request → Email → Confirm → Success

**Estimated Timeline:**
- Implementation: 2-3 hours
- UAT: 30-45 minutes
- Bug fixes (if any): 30 minutes
- **Total: 3-4 hours**

**Value Delivered:**
- Completes authentication flow
- Users can recover lost access
- Professional user experience

---

**Ready to start Story 1.15?**

