# Story 2.1 UAT Test Guide
**User Profile Enhancement - Bio, Theme, Layout, Font Size, and Industries**

Date: January 15, 2025

---

## ✅ **Migration Complete**

Database migration `013` successfully applied:
- ✅ 4 new reference tables created (ThemePreference, LayoutDensity, FontSize, UserIndustry)
- ✅ User table enhanced with 4 new fields (Bio, ThemePreferenceID, LayoutDensityID, FontSizeID)
- ✅ All seed data inserted with proper CSS classes and metadata
- ✅ Full audit trail logging implemented

---

## 🧪 **UAT Test Scenarios**

### **Prerequisites**

Before testing, ensure you have:
1. ✅ Backend server running on `http://localhost:8000`
2. ✅ Authenticated user account (or create a test account)
3. ✅ Postman or similar API tool, OR frontend UI with profile page
4. ✅ Database access (optional) to verify data

---

### **Test 1: Bio Field Validation (AC-2.1.1)**

**API Endpoint:** `PUT /api/users/me/profile/enhancements`

**Steps:**
1. Login and get your access token
2. Try updating bio with 501 characters (over limit)
3. Try updating bio with valid text under 500 characters
4. Try leaving bio empty (should be allowed)

**Expected Results:**
- ✅ Bio with 501 characters returns 422 validation error
- ✅ Bio with ≤500 characters saves successfully
- ✅ Empty bio saves as NULL (optional field)
- ✅ Database stores correct value in `User.Bio` field

**API Request Example:**
```json
PUT /api/users/me/profile/enhancements
Headers: { "Authorization": "Bearer <token>" }
Body: {
  "bio": "Seasoned event manager with 10+ years experience in corporate conferences..."
}
```

**Success Response:**
```json
{
  "success": true,
  "user_id": 123,
  "message": "Profile updated successfully"
}
```

---

### **Test 2: Theme Preferences (AC-2.1.2, AC-2.1.6)**

**API Endpoints:** 
- `GET /api/users/reference/themes` (list available themes)
- `PUT /api/users/me/profile/enhancements` (update preference)

**Steps:**
1. Get list of available themes
2. Update profile to use "dark" theme
3. Get your enhanced profile to verify theme was saved
4. Switch to "high-contrast" theme
5. Try an invalid theme ID (should fail)

**Expected Results:**
- ✅ List returns 4 themes: light, dark, high-contrast, system
- ✅ Each theme has: id, code, name, description, css_class
- ✅ Dark theme (ID 2) saves correctly
- ✅ Enhanced profile returns theme preference data
- ✅ Invalid theme ID returns 400 error
- ✅ Database stores correct `User.ThemePreferenceID`

**API Request Example:**
```json
GET /api/users/reference/themes
Response: [
  {
    "id": 1,
    "code": "light",
    "name": "Light Theme",
    "description": "Clean, bright interface",
    "css_class": "theme-light"
  },
  { ... dark ... },
  { ... high-contrast ... },
  { ... system ... }
]

PUT /api/users/me/profile/enhancements
Body: {
  "theme_preference_id": 2  // dark theme
}
```

---

### **Test 3: Layout Density (AC-2.1.2, AC-2.1.7)**

**API Endpoints:**
- `GET /api/users/reference/layout-densities` (list options)
- `PUT /api/users/me/profile/enhancements` (update preference)

**Steps:**
1. Get list of layout density options
2. Update profile to "compact" layout
3. Switch to "spacious" layout
4. Verify change saved in database

**Expected Results:**
- ✅ List returns 3 options: compact, comfortable, spacious
- ✅ Each option has proper CSS class for UI styling
- ✅ Layout preference saves and retrieves correctly
- ✅ Database stores correct `User.LayoutDensityID`

**API Request Example:**
```json
GET /api/users/reference/layout-densities
Response: [
  {
    "id": 1,
    "code": "compact",
    "name": "Compact",
    "description": "Tight spacing for power users",
    "css_class": "layout-compact"
  },
  { ... comfortable ... },
  { ... spacious ... }
]
```

---

### **Test 4: Font Size (AC-2.1.2, AC-2.1.8)**

**API Endpoints:**
- `GET /api/users/reference/font-sizes` (list options)
- `PUT /api/users/me/profile/enhancements` (update preference)

**Steps:**
1. Get list of font size options
2. Update to "large" font size
3. Switch to "medium" size
4. Verify font size preference

**Expected Results:**
- ✅ List returns 3 options: small (14px), medium (16px), large (18px)
- ✅ Each option includes BaseFontSize for accessibility
- ✅ Font preference saves correctly
- ✅ Database stores correct `User.FontSizeID`

**API Request Example:**
```json
GET /api/users/reference/font-sizes
Response: [
  {
    "id": 1,
    "code": "small",
    "name": "Small",
    "description": "Smaller text (14px)",
    "css_class": "font-small",
    "base_font_size": "14px"
  },
  { ... medium (16px) ... },
  { ... large (18px) ... }
]
```

---

### **Test 5: Industry Associations - Add (AC-2.1.4)**

**API Endpoints:**
- `GET /api/users/reference/industries` (list available industries)
- `POST /api/users/me/industries` (add industry)
- `GET /api/users/me/industries` (list user's industries)

**Steps:**
1. Get list of available industries
2. Add your first industry as primary
3. Add a second industry as secondary
4. List your industries to verify both were added
5. Try adding the same industry twice (should fail)

**Expected Results:**
- ✅ Industries list returns available options
- ✅ First industry added with `is_primary: true`
- ✅ Second industry added with `is_primary: false`
- ✅ List endpoint returns both with correct primary status
- ✅ Duplicate attempt returns 400 error
- ✅ Database stores both in `UserIndustry` table

**API Request Example:**
```json
POST /api/users/me/industries
Body: {
  "industry_id": 1,
  "is_primary": true
}

Response: {
  "user_industry_id": 45,
  "industry_id": 1,
  "industry_name": "Technology",
  "is_primary": true,
  "sort_order": 0
}
```

---

### **Test 6: Industry Associations - Update Primary (AC-2.1.5)**

**API Endpoint:** `PUT /api/users/me/industries/{user_industry_id}`

**Steps:**
1. Have at least 2 industries (one primary, one secondary)
2. Update secondary industry to become primary
3. Verify previous primary becomes secondary
4. Get industries list to confirm changes

**Expected Results:**
- ✅ Only one industry can be primary at a time
- ✅ Setting one as primary automatically sets others to secondary
- ✅ Update endpoint returns success with updated data
- ✅ Database constraint ensures single primary industry

**API Request Example:**
```json
PUT /api/users/me/industries/45
Body: {
  "is_primary": true
}

Response: {
  "user_industry_id": 45,
  "industry_id": 1,
  "is_primary": true,
  "sort_order": 0
}
```

---

### **Test 7: Industry Associations - Remove (Soft Delete)**

**API Endpoint:** `DELETE /api/users/me/industries/{user_industry_id}`

**Steps:**
1. Have at least one industry association
2. Get your industries and note the user_industry_id
3. Delete one industry
4. List industries again to verify it's gone
5. Check database to verify it's soft-deleted (IsDeleted=1)

**Expected Results:**
- ✅ Delete returns 204 No Content
- ✅ Industry removed from list endpoint
- ✅ Database marks record as deleted (soft delete)
- ✅ Cannot delete with invalid ID (404 error)

**API Request Example:**
```json
DELETE /api/users/me/industries/45
Response: 204 No Content
```

---

### **Test 8: Complete Profile Update (All Fields)**

**API Endpoint:** `PUT /api/users/me/profile/enhancements`

**Steps:**
1. Update profile with all new fields in one request:
   - Bio
   - Theme preference
   - Layout density
   - Font size
2. Get enhanced profile to verify all changes
3. Update only some fields (partial update)

**Expected Results:**
- ✅ All fields update successfully in single request
- ✅ Enhanced profile endpoint returns all new fields
- ✅ Partial updates work correctly (only specified fields change)
- ✅ NULL fields remain unchanged in database

**API Request Example:**
```json
PUT /api/users/me/profile/enhancements
Body: {
  "bio": "Full-stack developer specializing in event management platforms",
  "theme_preference_id": 2,  // dark
  "layout_density_id": 1,    // compact
  "font_size_id": 3          // large
}

GET /api/users/me/profile/enhanced
Response: {
  "user_id": 123,
  "email": "user@example.com",
  "bio": "Full-stack developer specializing in event management platforms",
  "theme_preference": {
    "id": 2,
    "code": "dark",
    "name": "Dark Theme",
    "css_class": "theme-dark"
  },
  "layout_density": {
    "id": 1,
    "code": "compact",
    "name": "Compact",
    "css_class": "layout-compact"
  },
  "font_size": {
    "id": 3,
    "code": "large",
    "name": "Large",
    "base_font_size": "18px",
    "css_class": "font-large"
  }
}
```

---

### **Test 9: Audit Trail (AC-2.1.13)**

**Database Verification**

**Steps:**
1. Make any profile update
2. Query audit.UserAudit table to find the log entry
3. Verify all audit fields are populated correctly

**Expected Results:**
- ✅ Audit entry created for every profile update
- ✅ CreatedBy, CreatedDate populated correctly
- ✅ UpdatedBy, UpdatedDate populated on changes
- ✅ User context preserved in audit log

**SQL Query:**
```sql
SELECT TOP 5 *
FROM audit.UserAudit
WHERE UserID = <your_user_id>
ORDER BY CreatedDate DESC
```

---

### **Test 10: Authentication & Authorization**

**API Endpoints:** All profile endpoints

**Steps:**
1. Try accessing profile endpoints without token (401)
2. Try accessing profile endpoints with invalid token (401)
3. Verify only your own profile can be updated
4. Verify you cannot access other users' industries

**Expected Results:**
- ✅ All endpoints require valid JWT token
- ✅ Missing token returns 401 Unauthorized
- ✅ Invalid token returns 401 with error message
- ✅ Users cannot modify other users' profiles

**API Request Example:**
```json
PUT /api/users/me/profile/enhancements
Headers: {}  // No Authorization header

Response: 401 Unauthorized
{
  "detail": "Not authenticated"
}
```

---

## 📊 **Success Criteria**

### Must Pass (Critical)
- ✅ Bio field validates max 500 characters
- ✅ All 4 theme preferences available and functional
- ✅ All 3 layout densities available and functional
- ✅ All 3 font sizes available with correct base sizes
- ✅ Industry associations: add, update, remove all work
- ✅ Only one primary industry allowed
- ✅ Duplicate industry association prevented
- ✅ Authentication required for all endpoints
- ✅ Audit trail created for all changes

### Should Pass (Important)
- ✅ Partial updates work correctly (update only some fields)
- ✅ Reference data returns consistent format
- ✅ Error messages are clear and actionable
- ✅ API responses include proper status codes

### Nice to Have
- ✅ Frontend UI matches backend functionality
- ✅ CSS classes applied to UI elements
- ✅ Profile preferences persist across sessions

---

## 🐛 **Troubleshooting**

### Issue: "Cannot connect to database"
- Check SQL Server is running
- Verify connection string in `.env` file
- Check firewall rules for port 1433

### Issue: "404 Not Found" on endpoints
- Verify backend server is running: `python -m uvicorn main:app --reload`
- Check endpoint paths match exactly
- Ensure user router is registered in main.py

### Issue: "401 Unauthorized"
- Verify JWT token is valid and not expired
- Check token format: `Bearer <token>`
- Ensure user account exists and is active

### Issue: "Validation Error" on valid data
- Check API request JSON format
- Verify field names are camelCase (not PascalCase)
- Review Pydantic schema validation rules

---

## 📝 **Test Results Template**

```
Test Date: ___________
Tester Name: ___________
Environment: Staging / Production

Test 1: Bio Field Validation
[ ] Pass [ ] Fail - Notes: _______________________

Test 2: Theme Preferences
[ ] Pass [ ] Fail - Notes: _______________________

Test 3: Layout Density
[ ] Pass [ ] Fail - Notes: _______________________

Test 4: Font Size
[ ] Pass [ ] Fail - Notes: _______________________

Test 5: Industry Associations - Add
[ ] Pass [ ] Fail - Notes: _______________________

Test 6: Industry Associations - Update
[ ] Pass [ ] Fail - Notes: _______________________

Test 7: Industry Associations - Remove
[ ] Pass [ ] Fail - Notes: _______________________

Test 8: Complete Profile Update
[ ] Pass [ ] Fail - Notes: _______________________

Test 9: Audit Trail
[ ] Pass [ ] Fail - Notes: _______________________

Test 10: Authentication & Authorization
[ ] Pass [ ] Fail - Notes: _______________________

Overall Result: [ ] Pass [ ] Fail
Blocking Issues: _______________________________
```

---

## 📚 **Reference**

- **Story File:** `docs/stories/story-2.1.md`
- **API Endpoints:** `backend/modules/users/router.py`
- **Database Migration:** `backend/migrations/versions/013_enhanced_user_profile.py`
- **Test Suite:** `backend/tests/test_story_2_1_profile_enhancement.py`

---

**Questions or Issues?**
Contact the development team or refer to the story file for detailed acceptance criteria.

