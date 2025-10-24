# UAT Sections for Stories 1.14-1.17

**Date:** 2025-10-16  
**Status:** Ready to be added to story files  
**Stories:** 1.14 (Frontend Onboarding), 1.15 (Password Reset), 1.16 (Team Management), 1.17 (UX Polish)

---

## Story 1.14: Frontend Onboarding Flow - UAT Section

### UAT Scenarios

1. **Complete Onboarding Journey (Happy Path):**
   - User logs in after email verification
   - User sees onboarding wizard (Step 1 of 2)
   - User completes user details (name, phone, role)
   - User clicks "Next"
   - User sees company setup (Step 2 of 2)
   - User searches for company using ABR search
   - Company details pre-fill automatically
   - User reviews and submits
   - User redirected to dashboard
   - Onboarding completed in <5 minutes

2. **Progress Indicator Clarity:**
   - User sees clear progress: "Step 1 of 2"
   - User understands current position in flow
   - User knows what's coming next
   - Progress bar/indicator is motivating, not overwhelming
   - User never asks "How many more steps?"

3. **Auto-Save Prevents Data Loss:**
   - User fills out Step 1 halfway
   - User accidentally refreshes page
   - Page reloads with form data intact
   - User sees "Form restored from auto-save" message
   - User completes onboarding without re-entering data

4. **Enhanced Company Search Integration:**
   - User searches for company by name
   - Search results appear quickly
   - User selects correct company
   - Company details pre-fill all fields
   - User verifies ABN, address, GST status correct
   - Pre-filled data saves significant time

5. **Validation and Error Handling:**
   - User leaves required field empty
   - User clicks "Next"
   - System shows inline error below field
   - Error message is clear and actionable
   - User fills field, error disappears
   - User proceeds successfully

6. **Back Navigation Works:**
   - User completes Step 1, proceeds to Step 2
   - User realizes they need to change something
   - User clicks "Back" button
   - Returns to Step 1 with data intact
   - User makes change
   - User proceeds to Step 2 again successfully

7. **Mobile Onboarding Experience:**
   - User completes onboarding on mobile device
   - All fields are easily tappable (44px targets)
   - Virtual keyboard doesn't obscure fields
   - Progress indicator clear on mobile
   - Scrolling works smoothly
   - Entire experience feels professional on mobile

### UAT Success Criteria

- [ ] **Completion Rate:** >85% of users complete onboarding without abandoning
- [ ] **Time to Value:** <5 minutes average time to complete onboarding
- [ ] **Abandonment Rate:** <10% of users abandon onboarding flow
- [ ] **Auto-Save Saves Users:** >80% of users who refresh mid-flow continue (not restart)
- [ ] **Company Search Success:** >90% find and select correct company
- [ ] **Progress Clarity:** >95% understand where they are in the flow
- [ ] **Mobile Experience:** Rated ≥4/5 by mobile testers
- [ ] **Zero Confusion:** <5% of users confused about what to do next

### UAT Test Plan

**Participants:** 12 representative users:
- 8 first-time users (never seen platform before)
- 4 returning users (signed up but didn't complete onboarding)
- Mix of devices (6 desktop, 6 mobile)
- Mix of company sizes (small unlisted, medium, large)

**Duration:** 30-45 minutes per participant

**Environment:** 
- Staging environment with realistic data
- ABR search fully functional
- Auto-save enabled
- Analytics tracking onboarding metrics

**Facilitation:** 
- Product Owner observes
- Does not intervene unless user stuck for >3 minutes
- Uses think-aloud protocol
- Measures completion time precisely
- Notes abandonment points

**Process:**
1. **Pre-Test:** "You just verified your email. Complete your account setup."
2. **Task 1:** "Complete the onboarding process" (observe entire flow)
3. **Intervention (Mid-Flow):** "Refresh the page now" (test auto-save)
4. **Task 2:** "Continue completing onboarding" (verify auto-save worked)
5. **Post-Test Survey:**
   - Rate ease of onboarding (1-5)
   - Was progress indicator clear? (Yes/No)
   - Did auto-save help? (Yes/No, if tested)
   - Any confusion or difficulties? (Open feedback)
   - Would you abandon if not required? (Yes/No - honesty check)

**Data Collection:**
- Completion rate (completed vs abandoned)
- Time to complete (average, median, p95)
- Abandonment points (which step users quit)
- Auto-save restoration success
- Company search success rate
- Progress clarity rating
- User satisfaction ratings
- Qualitative feedback

**Success Threshold:** ≥80% of UAT scenarios pass with ≥80% of testers

**Deviations from Success Criteria:**
- If completion rate <85%: Identify friction points, simplify flow
- If time to value >5 minutes: Optimize steps or reduce required fields
- If abandonment >10%: Find drop-off points and improve
- If auto-save doesn't help: Improve auto-save UX or messaging
- If company search fails: Improve search UX or fallback
- If mobile experience <4/5: Iterate on mobile design

---

## Story 1.15: Frontend Password Reset Pages - UAT Section

### UAT Scenarios

1. **Complete Password Reset Flow:**
   - User clicks "Forgot password?" from login page
   - User enters email address
   - User submits request
   - User sees success message (always, even if email doesn't exist - security)
   - User checks email and clicks reset link
   - User enters new password with confirmation
   - User sees password strength indicator
   - User submits new password
   - User redirected to login page with success message
   - User logs in with new password successfully

2. **Password Strength Indicator Helpful:**
   - User enters weak password ("password123")
   - Strength indicator shows "Weak" in red
   - Requirements checklist shows what's missing
   - User improves password ("Password123!")
   - Strength indicator updates to "Strong" in green
   - User feels confident password is secure

3. **Token Expiry Handling:**
   - User requests password reset
   - User waits >1 hour (token expires)
   - User clicks reset link
   - System shows clear error: "This reset link has expired"
   - System provides "Request new reset link" button
   - User clicks button, receives new email
   - User completes reset with new link successfully

4. **Password Confirmation Validation:**
   - User enters new password
   - User enters different confirmation password
   - System shows error: "Passwords do not match"
   - User corrects confirmation password
   - Validation passes, user can submit

5. **Mobile Password Reset:**
   - User completes password reset on mobile device
   - Email field uses email keyboard
   - Password field has show/hide toggle (easy to tap)
   - All form fields are accessible
   - Experience feels smooth on mobile

6. **Security Message Understanding:**
   - User enters non-existent email
   - System shows: "If an account exists with this email, you'll receive reset instructions"
   - User understands system won't reveal if email exists (security)
   - User accepts this is for security reasons

7. **Network Error Recovery:**
   - User submits password reset
   - Network error occurs
   - System shows clear error message
   - System provides "Try again" button
   - User clicks retry, successfully submits
   - Request goes through on second attempt

### UAT Success Criteria

- [ ] **Completion Rate:** >95% successfully complete password reset
- [ ] **Time to Complete:** <2 minutes average (from request to login)
- [ ] **Password Strength Understanding:** >90% understand how to create strong password
- [ ] **Expiry Handling:** 100% of users successfully request new link when expired
- [ ] **Security Message Accepted:** >85% understand and accept security message
- [ ] **Mobile Experience:** Rated ≥4/5 by mobile testers
- [ ] **Error Recovery:** >90% successfully retry after network error
- [ ] **Zero Security Concerns:** 0 users raise security concerns

### UAT Test Plan

**Participants:** 8 representative users:
- 4 non-technical users
- 4 technical users (to assess security messaging)
- Mix of devices (4 desktop, 4 mobile)

**Duration:** 20-30 minutes per participant

**Environment:** 
- Staging environment with email testing
- Test accounts with known passwords
- Ability to simulate token expiry
- Ability to simulate network errors

**Facilitation:** 
- Product Owner observes
- Does not reveal if email exists or not
- Measures completion time
- Notes reactions to security messages

**Process:**
1. **Pre-Test:** "You forgot your password. Reset it."
2. **Task 1:** "Request password reset"
3. **Task 2:** "Check email and complete reset" (measure time)
4. **Task 3:** "Log in with new password" (verify success)
5. **Task 4 (Token Expiry):** "Try this expired reset link" (test expiry handling)
6. **Post-Test Survey:**
   - Rate ease of password reset (1-5)
   - Was password strength indicator helpful? (Yes/No)
   - Did you understand the security message? (Yes/No)
   - Any security concerns? (Yes/No - explain)
   - Open feedback

**Data Collection:**
- Completion rate
- Time to complete
- Password strength indicator helpfulness
- Token expiry recovery success
- Security message understanding
- Error recovery success rate
- User satisfaction ratings
- Security concerns raised

**Success Threshold:** ≥80% of UAT scenarios pass with ≥80% of testers

**Deviations from Success Criteria:**
- If completion rate <95%: Identify failure points and simplify
- If time to complete >2 minutes: Optimize flow or email delivery
- If password strength not understood: Improve indicator or messaging
- If expiry handling confuses: Improve error message and recovery flow
- If security message not accepted: Adjust messaging (but maintain security)
- If mobile experience <4/5: Iterate on mobile design
- If security concerns raised: Address concerns or improve explanation

---

## Story 1.16: Frontend Team Management UI - UAT Section

### UAT Scenarios

1. **Company Admin Invites Team Member:**
   - Admin logs into team management dashboard
   - Admin sees current team members and pending invitations
   - Admin clicks "Invite User" button
   - Admin enters: First Name, Last Name, Email, Role
   - Admin submits invitation
   - System shows success toast: "Invitation sent to [email]"
   - Invitation appears in "Pending Invitations" list
   - Invitee receives email (verified separately)

2. **View and Manage Pending Invitations:**
   - Admin opens team management page
   - Admin sees pending invitations list
   - Each invitation shows: Name, Email, Role, Sent Date, Status
   - Status badges are clear (Pending in yellow, Accepted in green)
   - Admin can see invitation details at a glance
   - List is organized and easy to scan

3. **Resend Expired Invitation:**
   - Admin sees expired invitation in list
   - Invitation shows "Expired" status badge (gray)
   - Admin clicks "Resend" button
   - System generates new invitation token
   - System sends new email to invitee
   - Status updates to "Pending"
   - Admin receives confirmation toast

4. **Cancel Pending Invitation:**
   - Admin decides not to invite someone
   - Admin finds invitation in pending list
   - Admin clicks "Cancel" button
   - System shows confirmation: "Cancel invitation to [name]?"
   - Admin confirms cancellation
   - Invitation status updates to "Cancelled"
   - Invitation link no longer works

5. **Invitee Accepts Invitation:**
   - Invitee clicks invitation link from email
   - Invitee sees invitation acceptance page
   - Page shows: Company name, Assigned role, Inviter name
   - Invitee enters password (name and email pre-filled)
   - Invitee submits acceptance
   - Invitee auto-logged in
   - Invitee redirected to simplified onboarding
   - Invitee completes profile (no company setup needed)
   - Invitee redirected to dashboard

6. **Role-Based Access Control (Company User Cannot Invite):**
   - Company user (not admin) logs in
   - Company user tries to access team management page
   - System shows "Access Denied" message
   - Message explains: "Only Company Admins can manage team members"
   - User understands they don't have permission
   - No confusion or security concerns

7. **Mobile Team Management:**
   - Admin manages team on mobile device
   - Team member list displays clearly (stacked layout)
   - Invitation list readable on mobile
   - "Invite User" modal works on mobile
   - Form fields easy to tap
   - Actions (Resend, Cancel) work correctly

### UAT Success Criteria

- [ ] **Invitation Success Rate:** >90% of admins successfully invite team member
- [ ] **Time to Invite:** <3 minutes from clicking "Invite" to invitation sent
- [ ] **Invitation List Clarity:** >95% understand invitation status at a glance
- [ ] **Resend Success:** 100% of resend attempts succeed
- [ ] **Cancellation Success:** 100% of cancellations prevent invitation acceptance
- [ ] **Acceptance Success:** >95% of invitees successfully accept and join
- [ ] **RBAC Enforcement:** 100% of non-admins blocked from team management
- [ ] **Mobile Experience:** Rated ≥4/5 by mobile testers

### UAT Test Plan

**Participants:** 8 admin users + 8 invitees:
- 8 company admin users (will send invitations)
- 8 invitee users (will accept invitations)
- 2 company user (non-admin) for RBAC testing
- Mix of devices (8 desktop, 8 mobile)

**Duration:** 45 minutes for admin testing, 30 minutes for invitee testing

**Environment:** 
- Staging environment with email testing
- Test companies with admin and non-admin users
- Sample team data for context

**Facilitation:** 
- Product Owner observes both admin and invitee experiences
- Measures time for invitation and acceptance flows
- Verifies RBAC enforcement
- Notes any role confusion

**Process:**

**Admin Testing:**
1. **Pre-Test:** "You need to add a team member to your company"
2. **Task 1:** "Invite [test user] to your team" (measure time)
3. **Task 2:** "View pending invitations"
4. **Task 3:** "Resend this expired invitation"
5. **Task 4:** "Cancel this pending invitation"
6. **Post-Test Survey:**
   - Rate ease of inviting team members (1-5)
   - Were invitation statuses clear? (Yes/No)
   - Any confusion? (Open feedback)

**Invitee Testing:**
1. **Pre-Test:** "You received an invitation. Accept it."
2. **Task 1:** "Accept the invitation" (measure time)
3. **Task 2:** "Complete your profile" (simplified onboarding)
4. **Post-Test Survey:**
   - Rate ease of accepting invitation (1-5)
   - Was it clear what company you were joining? (Yes/No)
   - Open feedback

**RBAC Testing:**
1. Log in as company_user (not admin)
2. Attempt to access team management page
3. Verify "Access Denied" message
4. Verify message is clear and helpful

**Data Collection:**
- Invitation success rate
- Time to send invitation
- Invitation list comprehension
- Resend/cancel success rates
- Acceptance success rate
- RBAC enforcement rate
- User satisfaction ratings
- Qualitative feedback

**Success Threshold:** ≥80% of UAT scenarios pass with ≥80% of testers

**Deviations from Success Criteria:**
- If invitation success <90%: Simplify invitation form or improve validation
- If time to invite >3 minutes: Optimize form or reduce required fields
- If invitation list not clear: Redesign status badges or layout
- If resend/cancel fails: Fix backend integration or error handling
- If acceptance success <95%: Improve invitation acceptance UX
- If RBAC not enforced: CRITICAL - Fix immediately
- If mobile experience <4/5: Iterate on mobile design

---

## Story 1.17: UX Enhancement & Polish - UAT Section

### UAT Scenarios

1. **Comprehensive Error Recovery:**
   - User encounters network error during form submission
   - System shows clear error message: "Connection lost. Check internet and try again."
   - System provides "Retry" button
   - User clicks retry, submission succeeds
   - User feels confident system handles errors gracefully
   - No data lost during error

2. **Loading States Prevent Confusion:**
   - User submits form
   - System shows loading spinner immediately
   - Button shows "Submitting..." text
   - Form fields are disabled
   - User sees clear visual feedback
   - No "blank screen" moment
   - User never wonders "Did it work?"

3. **Micro-Interactions Feel Professional:**
   - User hovers over button → button scales slightly
   - User focuses form field → border glows subtly
   - User successfully submits → checkmark animation appears
   - Toast notification slides in from top-right
   - All animations are smooth (60fps)
   - User perceives platform as "polished" and "modern"

4. **Accessibility Works (Keyboard Navigation):**
   - User navigates entire signup flow using only keyboard
   - Tab order is logical and predictable
   - Enter key submits forms
   - Escape key closes modals
   - Focus indicators always visible
   - User completes entire flow without mouse

5. **Screen Reader Experience:**
   - Screen reader user navigates signup page
   - All form fields have descriptive labels
   - Error messages are announced immediately
   - Loading states are announced ("Loading...")
   - Success messages are announced
   - User completes signup using screen reader alone

6. **Mobile Touch Targets Easy to Tap:**
   - User completes forms on mobile device
   - All buttons are easy to tap (44px minimum)
   - No accidental taps on wrong elements
   - Touch targets have adequate spacing
   - User never struggles to hit buttons

7. **Performance Feels Fast:**
   - User navigates between pages
   - Page transitions are instant (<100ms)
   - Form interactions feel responsive
   - No lag or stuttering
   - Lighthouse score >90
   - User perceives platform as "fast"

### UAT Success Criteria

- [ ] **Error Recovery:** 100% of errors provide clear recovery path
- [ ] **Loading Clarity:** 0% of users confused during loading states
- [ ] **Polish Rating:** >90% rate overall experience as "professional" or "polished"
- [ ] **Keyboard Navigation:** 100% of tasks completable via keyboard only
- [ ] **Screen Reader Success:** 100% of screen reader users complete core flows
- [ ] **WCAG 2.1 AA Compliance:** 100% compliance verified by accessibility audit
- [ ] **Touch Target Success:** >95% of mobile taps hit intended target
- [ ] **Performance Rating:** >90% rate platform as "fast"
- [ ] **Lighthouse Score:** >90 on all core pages

### UAT Test Plan

**Participants:** 12 diverse users:
- 8 general users (test error handling, loading states, polish)
- 2 keyboard-only users (test keyboard navigation)
- 2 screen reader users (test accessibility)
- Mix of devices (6 desktop, 6 mobile)
- Mix of technical proficiency

**Duration:** 60 minutes per participant

**Environment:** 
- Staging environment with full UX enhancements
- Ability to simulate errors (network, API)
- Performance monitoring enabled
- Accessibility testing tools available

**Facilitation:** 
- Product Owner observes carefully
- For accessibility testing: Certified accessibility specialist present
- Uses think-aloud protocol
- Notes every UX issue encountered

**Process:**

**General UX Testing:**
1. **Pre-Test:** "Complete signup, onboarding, and explore the platform"
2. **Task 1:** "Sign up for account" (observe error handling if errors occur)
3. **Task 2:** "Complete onboarding" (observe loading states, animations)
4. **Task 3:** "Navigate between pages" (observe performance)
5. **Task 4:** "Use platform on mobile" (test touch targets)
6. **Post-Test Survey:**
   - Rate overall polish/professionalism (1-5)
   - Rate performance/speed (1-5)
   - Did you understand what was happening during loading? (Yes/No)
   - Were error messages helpful? (Yes/No, if errors occurred)
   - Open feedback on UX

**Keyboard Navigation Testing:**
1. **Pre-Test:** "Complete entire signup flow using only keyboard (no mouse)"
2. **Task 1:** Navigate signup form using Tab
3. **Task 2:** Submit form using Enter
4. **Task 3:** Navigate onboarding using keyboard only
5. **Task 4:** Close any modals using Escape
6. **Verification:** User completes all tasks without mouse

**Screen Reader Testing:**
1. **Pre-Test:** "Complete signup using screen reader (NVDA or JAWS)"
2. **Task 1:** Navigate signup form
3. **Task 2:** Understand and fix form errors
4. **Task 3:** Complete form submission
5. **Verification:** Screen reader user completes signup independently

**Performance Testing:**
1. Run Lighthouse audits on all core pages
2. Measure page load times
3. Measure interaction latencies
4. Verify all metrics meet targets

**Accessibility Audit:**
1. Run automated accessibility tests (axe-core)
2. Manual WCAG 2.1 AA audit
3. Color contrast verification
4. Keyboard navigation verification
5. Screen reader verification

**Data Collection:**
- Error recovery success rate
- Loading state clarity
- Polish/professionalism ratings
- Keyboard navigation success rate
- Screen reader success rate
- WCAG compliance score
- Touch target success rate
- Performance metrics (Lighthouse, load times)
- User satisfaction ratings
- Qualitative UX feedback

**Success Threshold:** ≥80% of UAT scenarios pass with ≥80% of testers

**Critical Gates:**
- **WCAG 2.1 AA Compliance:** Must be 100% - no exceptions
- **Screen Reader Success:** Must be 100% - accessibility is not optional
- **Lighthouse Score:** Must be >90 - performance is critical

**Deviations from Success Criteria:**
- If error recovery fails: Improve error messages and recovery options
- If loading states confuse: Add progress indicators or better feedback
- If polish rating low: Identify rough edges and improve animations/transitions
- If keyboard navigation fails: Fix tab order and keyboard shortcuts
- If screen reader fails: CRITICAL - Fix immediately, retest completely
- If WCAG compliance fails: CRITICAL - Fix accessibility issues, audit again
- If touch targets problematic: Increase sizes and spacing
- If performance poor: Optimize code splitting, images, API calls

---

**Generated by:** Sarah (Product Owner Agent)  
**Date:** 2025-10-16  
**Status:** Ready to be added to story files 1.14-1.17

