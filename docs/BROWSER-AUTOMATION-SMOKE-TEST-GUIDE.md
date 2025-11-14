# Browser Automation Guide - Event Creation Smoke Test

**Date:** November 4, 2025  
**Story:** 2.4 - Event Management CRUD  
**Purpose:** Automate smoke test using Cursor's browser tools for regression testing

---

## 🎯 **Overview**

This guide shows you how to use Cursor's built-in browser automation tools to automate the Event Creation Smoke Test. The browser tools allow you to:
- Navigate to pages
- Take snapshots of the page
- Click elements
- Type text
- Wait for elements to appear
- Capture screenshots

**Note:** These browser tools are accessible via Cursor's MCP (Model Context Protocol) integration. You can use them directly in chat or save the steps for later execution.

---

## 📋 **Prerequisites**

1. **Application Running:**
   - Backend API running on `http://localhost:8000`
   - Frontend running on `http://localhost:5173` (or your configured port)
   - Database accessible

2. **User Account:**
   - Have a test user account ready
   - User should have at least one company
   - For role-based testing, have access to events with different roles (owner, participant)

3. **Browser Tools Available:**
   - Cursor's browser extension must be enabled
   - MCP server for browser tools should be running

---

## 🔧 **How to Use Browser Tools in Cursor**

### Basic Commands

The browser tools available in Cursor include:

1. **Navigate:** `browser_navigate(url)` - Navigate to a URL
2. **Snapshot:** `browser_snapshot()` - Capture accessibility snapshot (better than screenshot)
3. **Click:** `browser_click(element, ref)` - Click on an element
4. **Type:** `browser_type(element, ref, text)` - Type text into a field
5. **Wait:** `browser_wait_for(text, time)` - Wait for text to appear
6. **Screenshot:** `browser_take_screenshot()` - Capture screenshot

### Using the Tools

You can use these tools in two ways:

#### Method 1: Direct Chat Commands
Ask Cursor to perform actions:
```
"Navigate to http://localhost:5173 and take a snapshot"
"Click the Create Event button"
"Type 'Test Event' in the event name field"
```

#### Method 2: Saved Test Script
Save the test steps in a document (like this one) and reference it for regression testing.

---

## 📝 **Automated Smoke Test Steps**

### **Setup Phase**

```markdown
1. Navigate to application: http://localhost:5173
2. Take snapshot to verify page loaded
3. Login if not already logged in
4. Navigate to Dashboard
5. Wait for dashboard to load
```

### **Test 1: Event Creation Modal - Progressive Disclosure**

```markdown
STEP 1: Navigate to Dashboard
- Action: Navigate to http://localhost:5173/dashboard
- Wait: Wait for "Dashboard" text to appear
- Verify: Dashboard loaded with company list

STEP 2: Click Create Event Button
- Action: Click button with text "Create Event" or "Add Event"
- Wait: Wait for modal to appear
- Verify: Modal shows only "Event" label with "Private" and "Public" radio buttons
- Verify: No tabs visible yet

STEP 3: Select Private Visibility
- Action: Click radio button or label "Private"
- Wait: Wait for tabs to appear
- Verify: Tabs appear (Tab 1: Essentials, Tab 2: Enhanced Details, Tab 3: Advanced)
- Verify: Tab 1 is automatically selected and visible
```

### **Test 2: Form Validation & Button States**

```markdown
STEP 4: Verify Create Event Button Disabled
- Action: Take snapshot of modal
- Verify: "Create Event" button is DISABLED (grayed out)
- Action: Hover over disabled button (if possible)
- Verify: Tooltip appears listing incomplete required fields

STEP 5: Fill Event Name
- Action: Type "Test Event" in event name field
- Verify: "Create Event" button still disabled (other fields incomplete)

STEP 6: Fill Required Fields
- Action: Fill in Start Date
- Action: Fill in Start Time
- Action: Select Event Type from dropdown
- Verify: "Create Event" button becomes ENABLED
```

### **Test 3: Tab Navigation**

```markdown
STEP 7: Navigate to Tab 2
- Action: Click "Tab 2: Enhanced Details"
- Verify: Tab 2 content appears
- Verify: Tab 2 button is highlighted/active

STEP 8: Navigate to Tab 3
- Action: Click "Tab 3: Advanced"
- Verify: Tab 3 content appears

STEP 9: Return to Tab 1
- Action: Click "← Back to Tab 1: Essentials" button
- Verify: Returns to Tab 1
```

### **Test 4: Smart Field Inference**

```markdown
STEP 10: Check Timezone Pre-fill
- Action: Navigate to Tab 1: Essentials
- Verify: Timezone field is pre-filled with browser timezone
- Verify: Visual indicator (🔍) shows source

STEP 11: Check Country Auto-detection
- Verify: Country field may auto-fill from timezone
- Verify: Visual indicator shows source

STEP 12: Check City Pre-fill
- Verify: City field may pre-fill from recent events
- Verify: Visual indicator shows "🔍 From your recent events" if pre-filled
```

### **Test 5: Create Event**

```markdown
STEP 13: Fill All Required Fields
- Action: Ensure Event Name is filled: "Smoke Test Event"
- Action: Set Start Date: Today
- Action: Set Start Time: Current time + 1 hour
- Action: Select Event Type

STEP 14: Create Event
- Action: Click "Create Event" button
- Wait: Wait for success notification
- Verify: Button shows loading state ("Creating...")
- Verify: Success notification appears
- Verify: Modal closes
- Verify: Event appears in event list/dashboard
```

### **Test 6a: Role-Based Access Control**

```markdown
STEP 15: Open Participant Event
- Action: Navigate to Dashboard
- Action: Find event where you are a participant (not owner)
- Action: Click on event card
- Verify: Edit Event modal opens

STEP 16: Verify Participant Restrictions
- Verify: Modal header shows "Your role: Participant (View Only)"
- Verify: All form fields are greyed out and disabled
- Verify: "Update Event" button is disabled
- Action: Hover over disabled "Update Event" button
- Verify: Tooltip explains why button is disabled

STEP 17: Open Owner Event
- Action: Close modal
- Action: Find event where you are the owner
- Action: Click on event card
- Verify: Edit Event modal opens
- Verify: All fields are enabled and editable
- Verify: "Update Event" button is enabled
- Verify: Modal header shows "Your role: Owner"
```

### **Test 6b: Organizer Company Field (Public Events)**

```markdown
STEP 18: Open Create Event for Public
- Action: Click "Create Event" button
- Action: Select "Public" visibility
- Action: Navigate to Tab 1: Essentials

STEP 19: Verify Organizer Company Field
- Verify: "Organizer Company" dropdown field appears
- Verify: Field is marked as required
- Verify: Dropdown is populated with your companies
- Action: Select a company from dropdown
- Verify: Company is selected

STEP 20: Verify Field Hidden for Private
- Action: Select "Private" visibility
- Verify: "Organizer Company" field is hidden
```

---

## 💾 **Saving Test Steps for Regression Testing**

### Option 1: Markdown Test Script (Recommended)

Save this document and update it with:
- Test results (✅ Pass / ❌ Fail)
- Screenshots of failures
- Notes on any issues

### Option 2: Create a Test Script File

Create a file like `smoke-test-steps.json`:

```json
{
  "testName": "Event Creation Smoke Test",
  "version": "1.0",
  "date": "2025-11-04",
  "steps": [
    {
      "step": 1,
      "action": "navigate",
      "url": "http://localhost:5173/dashboard",
      "waitFor": "Dashboard"
    },
    {
      "step": 2,
      "action": "click",
      "element": "Create Event button",
      "waitFor": "Modal"
    }
  ]
}
```

### Option 3: Use Cursor Chat History

Save the chat conversation where you run the tests. Cursor maintains chat history that you can reference later.

---

## 🔄 **Running Regression Tests**

### Quick Regression Test

1. **Open this document in Cursor**
2. **Ask Cursor to run the tests:**
   ```
   "Can you walk through the smoke test steps in BROWSER-AUTOMATION-SMOKE-TEST-GUIDE.md?"
   ```

3. **Cursor will:**
   - Navigate to the application
   - Execute each step
   - Report results
   - Take snapshots/screenshots at key points

### Full Regression Test

1. **Start fresh:**
   - Clear browser cache
   - Ensure clean database state (if needed)

2. **Run all tests in sequence:**
   - Follow the steps in order
   - Document any failures
   - Take screenshots of issues

3. **Save results:**
   - Update test results in this document
   - Create a new file: `smoke-test-results-YYYY-MM-DD.md`

---

## 📊 **Test Results Template**

Create a results file for each test run:

```markdown
# Smoke Test Results - [Date]

## Test Environment
- Date: [Date]
- Tester: [Name]
- Browser: [Browser/Version]
- Application URL: [URL]
- Build Version: [Version]

## Test Results

### Test 1: Event Creation Modal - Progressive Disclosure
- Status: ✅ Pass / ❌ Fail
- Notes: [Any issues or observations]

### Test 2: Form Validation & Button States
- Status: ✅ Pass / ❌ Fail
- Notes: [Any issues or observations]

[... Continue for all tests ...]

## Summary
- Total Tests: [Number]
- Passed: [Number]
- Failed: [Number]
- Issues Found: [List of issues]
```

---

## 🛠️ **Troubleshooting**

### Browser Tools Not Working

1. **Check MCP Server:**
   - Ensure browser extension MCP server is running
   - Check Cursor settings for MCP configuration

2. **Verify Application:**
   - Ensure frontend is running
   - Check backend API is accessible

3. **Element Not Found:**
   - Use `browser_snapshot()` to see current page state
   - Check element selectors/references
   - Wait for elements to load before interacting

### Test Failures

1. **Take Screenshot:**
   - Use `browser_take_screenshot()` to capture current state

2. **Check Console:**
   - Use `browser_console_messages()` to see errors

3. **Check Network:**
   - Use `browser_network_requests()` to see API calls

---

## 📚 **Additional Resources**

- [Cursor Browser Tools Documentation](#) - Link to Cursor docs
- [SMOKE-TEST-EVENT-CREATION.md](./SMOKE-TEST-EVENT-CREATION.md) - Original smoke test manual steps
- [Event Creation Workflow Documentation](#) - Feature documentation

---

## 🎯 **Next Steps**

1. **Initial Run:**
   - Run through all tests manually using browser tools
   - Document any issues or improvements needed

2. **Create Test Script:**
   - Save test steps in a reusable format
   - Add to your test suite

3. **Automate:**
   - Consider integrating with Playwright/Cypress for CI/CD
   - Use these browser tools for quick manual/assisted testing

---

**Last Updated:** November 4, 2025  
**Maintained By:** Development Team

