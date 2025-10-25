# Story 1.19 UAT Test Guide
**Frontend ABR Search UI with Email Domain Verification**

Date: 2025-10-25

---

## ✅ **Migration Complete**

Database migration `012` successfully applied:
- ✅ Unique constraint on `Company.ABN` (filtered for non-NULL)
- ✅ Allows multiple NULL ABNs (sole traders, manual entries)
- ✅ Email domain verification implemented
- ✅ Auto-join for verified employees

---

## 🧪 **UAT Test Scenarios**

### **Test 1: ABN Search (Basic Flow)**

**Steps:**
1. Login as fresh user: `test1@test.com`
2. Complete Step 1 (user details)
3. Step 2: Search by ABN: `53102443916`
4. Should auto-detect "ABN (11 digits)"
5. Click result → Auto-fills form
6. Add street address + suburb
7. Submit

**Expected Results:**
- ✅ Single result: "ATLASSIAN PTY LTD"
- ✅ Auto-fills: Company name, ABN, State (NSW), Postcode (2000)
- ✅ Database saves: LegalEntityName, ACN, ABNStatus, EntityType, GSTRegistered

---

### **Test 2: ACN Search**

**Steps:**
1. Fresh user
2. Search by ACN: `158929938`
3. Click result
4. Submit

**Expected Results:**
- ✅ Auto-detects "ACN (9 digits)"
- ✅ Returns: "CANVA PTY LTD"
- ✅ Database saves **both ABN and ACN:**
  - ABN: `80158929938` (from ABR)
  - ACN: `158929938` (from ASICNumber field)

---

### **Test 3: Name Search with Enrichment**

**Steps:**
1. Fresh user
2. Search by name: `Canva`
3. See multiple results
4. Click any result
5. **Watch for brief "Loading complete details..." message** (enrichment)
6. Submit

**Expected Results:**
- ✅ Multiple results displayed
- ✅ Enrichment happens automatically (ABN lookup)
- ✅ Database saves complete data:
  - EntityType: "Australian Private Company"
  - GSTRegistered: true/false
  - ABNStatus: "Active"

---

### **Test 4: Email Domain Verification (Auto-Join)**

**Setup:**
1. User A (`alice@atlassian.com`) creates "Atlassian Pty Ltd" (ABN 53102443916)

**Test:**
1. User B logs in as `bob@atlassian.com`
2. Search: "Atlassian" or ABN `53102443916`
3. Click result
4. Submit

**Expected Results:**
- ✅ **NO error!** (Even though company exists)
- ✅ User B **automatically joins** existing company
- ✅ Both users now company_admin for same company
- ✅ Log shows: "Auto-joining user to existing company via domain verification"

---

### **Test 5: Duplicate ABN Prevention (Generic Email)**

**Setup:**
1. Company "CANVA PTY LTD" (ABN 80158929938) already exists

**Test:**
1. New user logs in as `testuser@gmail.com`
2. Search: "Canva" or ABN `80158929938`
3. Click result
4. Submit

**Expected Results:**
- ❌ **Error displayed:** "A company with ABN 80158929938 already exists. Company name: CANVA PTY LTD. If you work for this company, please request access."
- ✅ User prevented from creating duplicate
- ✅ User guided to request access flow

---

### **Test 6: Squatter Attack Prevention**

**Setup:**
1. Competitor (`competitor@evilcorp.com`) tries to register "Atlassian Pty Ltd"

**Test:**
1. Search: ABN `53102443916` (Atlassian)
2. Click result
3. Submit

**Expected Results:**
- ❌ **Blocked!** Error shown
- ✅ Cannot create company (domain doesn't match)
- ✅ Must request access
- 🛡️ **Squatter attack prevented!**

---

### **Test 7: Multiple NULL ABNs (Sole Traders)**

**Test:**
1. User A creates company: "Anthony's Consulting" (no ABN, NULL)
2. User B creates company: "Sarah's Design" (no ABN, NULL)
3. User C creates company: "Mike's Photography" (no ABN, NULL)

**Expected Results:**
- ✅ All 3 companies created successfully
- ✅ No duplicate errors
- ✅ NULL ABNs allowed unlimited times

---

### **Test 8: Complete Data Capture Verification**

**Test:**
Search and create company with any ABN, then check database:

```sql
SELECT 
    CompanyName,
    LegalEntityName,
    ABN,
    ACN,
    ABNStatus,
    EntityType,
    GSTRegistered,
    CreatedBy
FROM dbo.Company
WHERE CompanyID = (SELECT MAX(CompanyID) FROM dbo.Company);
```

**Expected Results:**
- ✅ CompanyName: Populated
- ✅ LegalEntityName: Populated (from ABR)
- ✅ ABN: Populated
- ✅ ACN: Populated (if company, NULL if sole trader)
- ✅ ABNStatus: "Active" or "Cancelled"
- ✅ EntityType: "Australian Private Company" or similar
- ✅ GSTRegistered: true/false (from ABR)

---

## 🎯 **Test Results Checklist**

- [ ] Test 1: ABN search works
- [ ] Test 2: ACN search works
- [ ] Test 3: Name search with enrichment works
- [ ] Test 4: Email domain auto-join works (alice@atlassian.com)
- [ ] Test 5: Duplicate prevention works (generic email blocked)
- [ ] Test 6: Squatter attack prevented
- [ ] Test 7: Multiple NULL ABNs allowed
- [ ] Test 8: Complete data saved to database

---

## 📊 **Success Criteria**

**All 8 tests must pass for Story 1.19 UAT sign-off**

---

## 🐛 **Known Limitations (Not Bugs)**

1. **Street address required from user** (ABR doesn't store it)
2. **Suburb required from user** (ABR doesn't store it)
3. **Entity type NULL for name searches** (unless enrichment works)
4. **Generic email users must request access** (security feature, not bug)

---

## 📝 **Post-UAT Actions**

After all tests pass:
1. Remove debug logging from browser console
2. Update story status to "Complete - UAT Passed"
3. Document any edge cases found
4. Sign off Story 1.19 ✅

---

**Ready for comprehensive UAT testing!** 🚀

