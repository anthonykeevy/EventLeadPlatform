# UAT Checklist - Story 1.15: Frontend Password Reset Pages

**Date:** 2025-10-22  
**Tester:** Anthony Keevy  
**Status:** ✅ PASSED (Critical Tests Complete)

---

## **AC-1.15.1: Password Reset Request Page**

### Happy Path ✅
- [x] Navigate from login page via "Forgot password?" link
- [x] Enter valid email address
- [x] Submit form
- [x] Receive success message
- [x] Email arrives in MailHog with correct link

### Edge Cases ✅
- [x] **Test 1.1:** Enter **invalid email format** - PASS
  - ✓ Form validation prevents submission
  - ✓ Error: "Please enter a valid email address"

- [x] **Test 1.2:** Enter **non-existent email** - PASS
  - ✓ Same success message (security feature)
  - ✓ No email sent to MailHog

- [x] **Test 1.3:** Click "Back to Login" link - PASS
  - ✓ Returns to `/login` page

- [x] **Test 1.4:** "Try again" link after success - PASS (UX improved)
  - ✓ Returns to email input form
  - ✓ Changed from button to subtle help text

---

## **AC-1.15.2: Password Reset Confirmation Page**

### Happy Path ✅
- [x] Click valid token link from email
- [x] Token validated on page load
- [x] Enter new password (meeting requirements)
- [x] Enter matching confirmation password
- [x] Submit form
- [x] See success message
- [x] Redirect to login page
- [x] Login with new password

### Edge Cases ✅
- [x] **Test 2.1:** Access `/reset-password/confirm` **without token** - PASS
  - ✓ Error page shown immediately
  - ✓ "Request New Reset Link" button displayed

- [x] **Test 2.2:** Access with **invalid token** - PASS
  - ✓ "Validating Reset Link..." loading state shown
  - ✓ Error page displayed after validation
  - ✓ Password form NOT shown (security fix)

- [x] **Test 2.3:** Valid token workflow - PASS
  - ✓ Token validated successfully on page load
  - ✓ Password form displayed
  - ✓ Password reset successful
  - ✓ Login works with new password

- [x] **Test 2.4:** Reuse a **token that's already been used** (Optional)
  - **How to test:** Use the same email link twice
  - **Expected:** Second use shows error page

- [x] **Test 2.5:** Enter **passwords that don't match** (Optional - Already tested in unit tests)
  - **Expected:** Validation error: "Passwords do not match"

- [ ] **Test 2.6:** Click "Remember your password? Log In" link (Optional)
  - **Expected:** Navigate to `/login` page

---

## **AC-1.15.3: Password Strength Indicator**

- [x] **Test 3.1:** Enter **weak password** (e.g., "short")
  - **Expected:** Red bar, "Weak" label
  - **Expected:** Checklist shows: ❌ At least 8 characters

- [x] **Test 3.2:** Enter **medium password** (e.g., "password123")
  - **Expected:** Yellow/orange bar, "Medium" label
  - **Expected:** Some checklist items ✅, some ❌

- [x] **Test 3.3:** Enter **strong password** (e.g., "SecurePass123!")
  - **Expected:** Green bar, "Strong" label
  - **Expected:** All checklist items ✅:
    - ✅ At least 8 characters
    - ✅ Contains uppercase letter
    - ✅ Contains lowercase letter
    - ✅ Contains number
    - ✅ Contains special character

- [x] **Test 3.4:** Password strength updates **in real-time** as you type
  - **Expected:** Strength meter changes while typing, not just on blur

---

## **AC-1.15.4: Error Handling**

- [ ] **Test 4.1:** Submit request form while **backend is down**
  - **How to test:** Stop backend server, submit form
  - **Expected:** Error message: "Connection error. Please check your internet and try again."
  - **Expected:** Form remains editable, can retry

- [ ] **Test 4.2:** Submit confirmation form with **password less than 8 characters**
  - **Expected:** Frontend validation prevents submission
  - **Expected:** Error: "Password must be at least 8 characters"

- [ ] **Test 4.3:** Test **network timeout** scenario
  - **Expected:** Appropriate error message
  - **Expected:** Retry option available

---

## **AC-1.15.5: Mobile Responsive**

- [ ] **Test 5.1:** Open request page on **mobile viewport** (< 768px)
  - **Expected:** Single-column layout
  - **Expected:** Touch-friendly buttons (easy to tap)
  - **Expected:** Form fields stack vertically
  - **Expected:** No horizontal scrolling

- [ ] **Test 5.2:** Open confirmation page on **mobile viewport**
  - **Expected:** Password strength indicator visible and readable
  - **Expected:** Both password fields visible
  - **Expected:** Virtual keyboard doesn't obscure submit button

- [ ] **Test 5.3:** Test on **tablet viewport** (768px - 1024px)
  - **Expected:** Layout adapts appropriately
  - **Expected:** Modal not too wide or too narrow

---

## **Additional Testing (Nice to Have)**

### Accessibility
- [ ] **Test A.1:** Navigate forms using **keyboard only** (Tab, Enter)
  - **Expected:** Can complete entire flow without mouse
  - **Expected:** Focus indicators visible

- [ ] **Test A.2:** Test with **screen reader** (if available)
  - **Expected:** ARIA labels read correctly
  - **Expected:** Error messages announced

### UI/UX Polish
- [ ] **Test U.1:** Verify **loading states** show during API calls
  - **Expected:** Spinner/loading text visible
  - **Expected:** Buttons disabled during submission

- [ ] **Test U.2:** Verify **password visibility toggle** works
  - **Expected:** Eye icon toggles password visibility
  - **Expected:** Works for both password fields

- [ ] **Test U.3:** Check **autofocus** on page load
  - **Expected:** Email field focused on request page
  - **Expected:** New password field focused on confirm page

---

## **Bug Testing (Regression)**

- [ ] **Test B.1:** Verify email link goes to `/reset-password/confirm` (not `/reset-password`)
  - **This was Bug #2** - make sure it stays fixed

- [ ] **Test B.2:** Verify email actually arrives in MailHog
  - **This was Bug #1** - make sure it stays fixed

---

## **Summary**

**Tests Completed:** 5 / 33  
**Tests Remaining:** 28

**Critical Tests (Must Do):**
1. Invalid/expired/used token scenarios (2.1 - 2.4)
2. Password strength indicator (3.1 - 3.4)
3. Mobile responsiveness (5.1 - 5.2)
4. Non-existent email test (1.2)

**Optional Tests (Nice to Have):**
- Accessibility testing
- UI/UX polish verification

---

**Next Steps:**
1. Test invalid/expired tokens (most important edge cases)
2. Test password strength indicator
3. Test mobile responsiveness
4. Test error handling scenarios

