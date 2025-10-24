# UAT Quick Start Guide - Story 1.9

**Ready to test in 5 minutes!** 🚀

---

## 📦 What You Got

Three documents to run comprehensive UAT:

1. **UAT-TEST-ACCOUNTS-STORY-1.9.md** - Test credentials for 3 testers
2. **UAT-GUIDE-STORY-1.9.md** - Complete testing methodology (850 lines)
3. **UAT-RESULTS-FORM-STORY-1.9.html** - Interactive form to capture results

---

## ⚡ Quick Setup (5 minutes)

### Step 1: Start Services

```powershell
# Terminal 1: Backend
cd backend
python main.py
# Wait for: "Application startup complete"

# Terminal 2: Frontend  
cd frontend
npm run dev
# Wait for: "Local: http://localhost:5173"

# Terminal 3: MailHog (if not running)
# Already running or start via Docker
```

### Step 2: Verify Services

- Backend: http://localhost:8000/api/health → Should show `{"status":"healthy"}`
- Frontend: http://localhost:5173 → Should load home page
- MailHog: http://localhost:8025 → Should show inbox

### Step 3: Open Tools for Each Tester

Each tester needs 3 windows open:

**Window 1: Browser**
- http://localhost:5173 (frontend to test)

**Window 2: UAT Results Form**
- Open: `docs/stories/UAT-RESULTS-FORM-STORY-1.9.html` in browser
- This guides through tests and captures results

**Window 3: SQL Server Management Studio (SSMS)**
- Connect to EventLeadDB
- Ready to run verification queries

---

## 👥 Tester Assignment

| Tester | Email | Password | Focus | Time |
|--------|-------|----------|-------|------|
| **Tester 1** | tester1.newuser@eventlead-uat.com | Tester1Pass!2025 | Happy Paths | 15-20min |
| **Tester 2** | tester2.errors@eventlead-uat.com | Tester2Pass!2025 | Error Handling | 20-25min |
| **Tester 3** | tester3.mobile@eventlead-uat.com | Tester3Pass!2025 | Mobile/A11y | 20-25min |

**IMPORTANT:** Tester 1 must go first! (Tester 2 needs Tester 1's account for duplicate email test)

---

## 🎯 How It Works

### For Each Tester:

1. **Open the Results Form** (`UAT-RESULTS-FORM-STORY-1.9.html`)
2. **Select your tester ID** from dropdown → Form shows your credentials
3. **Select a scenario** to test
4. **Click "Start Test"** → Form displays:
   - Step-by-step instructions
   - What to verify (checkboxes)
   - Expected results
5. **Perform the test** in your browser window (localhost:5173)
6. **Check the database** in SSMS (form shows SQL query to run)
7. **Fill out results** (pass/fail, ratings, feedback)
8. **Submit** → Form generates CSV file
9. **Repeat** for next scenario

### The Form Will Guide You Through:
- ✅ What credentials to use
- ✅ Step-by-step instructions
- ✅ What to verify at each step
- ✅ Database queries to run
- ✅ Results capture (checkbox, text, ratings)
- ✅ CSV export

---

## 📊 Example Flow: Tester 1, Scenario 1

**1. Open Results Form**
```
Select: "Tester 1 - Sarah Johnson"
→ Form shows: Email, Password, Scenarios
```

**2. Select Scenario**
```
Click: "Scenario 1: New User Signup"
→ Click "Start Test"
```

**3. Follow Instructions (Form shows these)**
```
Step 1: Navigate to http://localhost:5173
Step 2: Click "Sign Up"
Step 3: Fill form with your credentials
Step 4: Observe password strength indicator
Step 5: Click "Sign Up"
Step 6: Verify success message
Step 7: Check MailHog for email
```

**4. Check Items as You Go (Form has checkboxes)**
```
☑ Signup form rendered with all 4 fields
☑ Real-time validation works
☑ Password strength indicator displays correctly
☑ Submit button enables when form valid
☑ Success message displays "Check your email"
☑ Verification email received in MailHog
```

**5. Run Database Query (Form shows this)**
```sql
SELECT UserID, Email, FirstName, LastName, EmailVerified, IsActive
FROM dbo.[User]
WHERE Email = 'tester1.newuser@eventlead-uat.com';
-- Expected: EmailVerified = 0, IsActive = 1
```

**6. Fill Results Section**
```
Pass/Fail: ✅ PASS
Duration: 87 seconds (auto-calculated)
UX Rating: ⭐⭐⭐⭐⭐ (5/5)
Issues: None
Positive: Password strength indicator very clear
Suggestions: Could add "email sent" confirmation
```

**7. Database Verification**
```
Status: ✅ PASS - All database checks passed
Notes: User record created, EmailVerified=0 as expected, password hashed
```

**8. Submit**
```
Click "Submit Results"
→ Success! Download CSV
→ Test another scenario or finish
```

---

## 📁 CSV Output Format

The form generates CSV with normalized structure:

```csv
"timestamp","session_date","session_time","tester","device","browser","scenario","startTime","endTime","duration","pass_fail","ux_rating","issues_found","positive_feedback","suggestions","db_verification","db_notes","field_0","field_1",...
"2025-01-19T14:30:00.000Z","1/19/2025","2:30:00 PM","Tester 1","Desktop - Windows","Chrome","Scenario 1: New User Signup","2:30:15 PM","2:31:42 PM","87","PASS","5","None","Password indicator very clear","...","PASS","User created correctly","YES","YES",...
```

**CSV Includes:**
- Session metadata (date, time, duration)
- Tester info (ID, device, browser)
- Scenario name
- Pass/Fail status
- All checkbox results (YES/NO)
- All text feedback
- Database verification results
- UX ratings

---

## 🗄️ Database Verification Quick Reference

**Tester 1 needs to run this once:**
```sql
-- After Scenario 1 (Signup), run this to allow login:
UPDATE dbo.[User] 
SET EmailVerified = 1 
WHERE Email = 'tester1.newuser@eventlead-uat.com';
```

**Common verification queries** (form shows these automatically):

```sql
-- View test users
SELECT UserID, Email, FirstName, LastName, EmailVerified, IsActive
FROM dbo.[User]
WHERE Email LIKE '%@eventlead-uat.com';

-- Check password is hashed
SELECT Email, LEFT(PasswordHash, 10) + '...' AS HashPreview, LEN(PasswordHash)
FROM dbo.[User]
WHERE Email = 'YOUR_EMAIL';
-- Should be 60+ characters, NOT plain text

-- View recent API requests
SELECT TOP 10 RequestID, Method, Path, StatusCode, DurationMs
FROM log.ApiRequest
WHERE Path LIKE '%/api/auth/%'
ORDER BY CreatedDate DESC;
```

---

## ✅ Success Criteria Checklist

After all 3 testers complete their scenarios, verify:

- [ ] **90%+ scenarios passed** (at least 10/12 scenarios)
- [ ] **Average signup time < 2 minutes** (check CSV duration field)
- [ ] **Error messages clear** (check feedback from Tester 2)
- [ ] **Mobile rating ≥ 4/5** (check Tester 3's mobile rating)
- [ ] **No critical bugs found** (review "issues_found" in CSV)
- [ ] **Database verification passed** (all 3 testers report PASS)

---

## 🚨 Troubleshooting

### "Form shows my email but I can't login"
→ Run the SQL UPDATE to set EmailVerified=1 (email verification not implemented yet)

### "Database query returns no results"
→ Make sure you completed the signup first, check email is correct

### "Frontend won't load"
→ Check `npm run dev` is running, check port 5173 not in use

### "Backend API errors"
→ Check `python main.py` is running, check database connection

### "CSV won't download"
→ Make sure you clicked Submit first, check browser download settings

### "Tester 2 duplicate email test doesn't work"
→ Make sure Tester 1 completed Scenario 1 first

---

## 📞 Need Help?

**Reference Documents:**
- **Detailed Guide:** `UAT-GUIDE-STORY-1.9.md` (methodology & best practices)
- **Test Accounts:** `UAT-TEST-ACCOUNTS-STORY-1.9.md` (credentials & SQL queries)
- **Results Form:** `UAT-RESULTS-FORM-STORY-1.9.html` (interactive testing)

**Contact UAT Lead:** Anthony Keevy

---

## 🎬 After UAT

### 1. Collect CSVs from All Testers
```powershell
# Each tester downloads their CSV
# Save to: docs/uat-results/story-1.9/
```

### 2. Analyze Results
```powershell
# Open CSVs in Excel
# Check pass_fail column (should be mostly PASS)
# Check ux_rating column (should be 4-5)
# Read issues_found column for bugs
```

### 3. Create Issues for Bugs
```
Priority:
- Critical: Blocks usage (can't signup/login)
- High: Major UX issue (confusing error messages)
- Medium: Annoying but not blocking
- Low: Nice to have
```

### 4. Make Go/No-Go Decision
```
✅ GO: ≥90% pass, no critical bugs, mobile ≥4/5
❌ NO-GO: <90% pass or critical bugs found
⚠️ CONDITIONAL: Fix high-priority bugs, retest
```

---

## 📈 Next Steps

**If UAT Passes:**
1. ✅ Mark Story 1.9 as "Ready for Production"
2. 📝 Document lessons learned
3. 🚀 Schedule production deployment
4. 📊 Prepare monitoring plan

**If UAT Fails:**
1. 🐛 Create bug tickets
2. 🔧 Fix critical/high issues
3. 🔄 Schedule retest (Tester 2 format: just failed scenarios)
4. ✅ Confirm fixes with testers

---

**Ready? Let's test! 🚀**

**Estimated Total Time:** 60 minutes (all 3 testers in sequence)

---

*This guide is part of the BMAD Method - UAT Best Practices*

