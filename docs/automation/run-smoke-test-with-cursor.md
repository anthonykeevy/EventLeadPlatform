# Quick Start: Running Smoke Test with Cursor Browser Tools

## 🚀 **Quick Start**

Simply ask Cursor to run the smoke test:

```
"Can you help me run the Event Creation Smoke Test? 
Navigate to http://localhost:5173, login if needed, 
and walk through the smoke test steps in 
docs/SMOKE-TEST-EVENT-CREATION.md"
```

Or be more specific:

```
"Navigate to http://localhost:5173/dashboard and 
start the smoke test. First, click the Create Event 
button and verify the progressive disclosure works."
```

---

## 📋 **Step-by-Step Commands**

### 1. Navigate and Login

```
"Navigate to http://localhost:5173 and take a snapshot. 
Then login with [email] and [password]"
```

### 2. Test Progressive Disclosure

```
"Navigate to the dashboard, click the Create Event button, 
and verify that only the Event visibility options are shown. 
Then select Private and verify the tabs appear."
```

### 3. Test Form Validation

```
"In the Create Event modal, verify the Create Event button 
is disabled. Then fill in the event name field with 'Test Event' 
and verify the button is still disabled."
```

### 4. Test Tab Navigation

```
"Click Tab 2: Enhanced Details, verify it loads, then click 
Tab 3: Advanced, and finally return to Tab 1."
```

### 5. Test Event Creation

```
"Fill in all required fields for a new event (name: 'Smoke Test Event', 
date, time, event type) and click Create Event. Verify the success 
message appears and the event shows on the dashboard."
```

### 6. Test Role-Based Access

```
"Click on an event where I'm a participant. Verify all fields are 
disabled and the Update Event button is disabled. Then click on 
an event where I'm the owner and verify all fields are enabled."
```

---

## 💡 **Tips**

1. **Use Snapshots:** Ask Cursor to take snapshots at key points:
   ```
   "Take a snapshot of the current page"
   ```

2. **Wait for Elements:** If elements aren't loading:
   ```
   "Wait for the Create Event button to appear"
   ```

3. **Check for Errors:**
   ```
   "Check the console for any errors"
   "Check the network requests for failed API calls"
   ```

4. **Save Results:**
   ```
   "Take a screenshot and save it as test-results-[date].png"
   ```

---

## 🔄 **Full Test Run**

For a complete automated test run, ask:

```
"Run the complete Event Creation Smoke Test from 
docs/SMOKE-TEST-EVENT-CREATION.md. Navigate to 
http://localhost:5173, login if needed, and execute 
all test steps. Report results for each test."
```

---

## 📝 **Saving Test Results**

After running tests, ask Cursor to save the results:

```
"Create a test results document with the following format:
- Test 1: [Result]
- Test 2: [Result]
- Issues found: [List]
Save it as docs/test-results-[date].md"
```

---

**Quick Reference:** Just copy and paste the commands above into Cursor chat!

