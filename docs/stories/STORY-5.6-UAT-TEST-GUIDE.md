# Story 5.6 UAT Test Guide — Publish Request Workflow

**Story:** 5.6  
**Epic:** 5 - Form Builder Readiness + Review & Publishing  
**Status:** Refined — step-by-step with common pitfalls  
**Created:** 2026-02-16  
**Updated:** 2026-02-17  

---

## Critical: Correct Flow (Do Not Bypass)

**The Pending Publish Requests card only shows rows from the `FormPublishRequest` table.**

- FormPublishRequest rows are created **only** when a Company User clicks **Request Publish** and the API succeeds.
- **Do NOT** manually change Form Status to "Pending Admin Review" in Edit Form — that bypasses the flow and does **not** create a FormPublishRequest. The Admin queue will stay empty.
- Always use the **Request Publish** button (Builder or Form Detail) to create a publish request.

---

## Config Setup (CompanyFormTestConfig)

| Setting | Value | Effect |
|---------|-------|--------|
| TestThresholdEnabled | **1** | Enables demo test requirement; blocks publish/request until threshold met |
| TestThresholdValue | **3** | Requires 3 demo test runs (preview submissions + "Record test run") |
| RequirePublishApproval | **1** | Company Users see "Request Publish"; must request before Admin can publish |

**To test threshold blocking:** Use `TestThresholdEnabled = 1`. With `TestThresholdEnabled = 0`, the threshold is disabled and you will **not** be blocked regardless of test count.

**SQL to set config (CompanyID 1016):**
```sql
-- Enable all checks for testing (upsert: insert if no row exists)
IF NOT EXISTS (SELECT 1 FROM dbo.CompanyFormTestConfig WHERE CompanyID = 1016)
    INSERT INTO dbo.CompanyFormTestConfig (CompanyID, TestThresholdEnabled, TestThresholdValue, RequirePublishApproval)
    VALUES (1016, 1, 3, 1);
ELSE
    UPDATE dbo.CompanyFormTestConfig
    SET TestThresholdEnabled = 1, TestThresholdValue = 3, RequirePublishApproval = 1,
        UpdatedDate = GETUTCDATE(), UpdatedBy = 1
    WHERE CompanyID = 1016;
```

---

## Approval Status vs Publish Approval (Two Different Concepts)

| Field | Source | Meaning |
|-------|--------|---------|
| **Approval Status (high-cost)** | `form.formApprovalStatus` (ref.FormApprovalStatus) | Story 2.11: Forms with deployment cost > $100 may need high-cost approval. "No Approval Required" means cost is low or unknown. |
| **Publish approval (Story 5.6)** | `CompanyFormTestConfig.RequirePublishApproval` | When enabled: Company Users must click **Request Publish**; Admin approves. Shown as "Publish approval: Required" in Form Detail (Company User only). |

**Important:** "Approval Status: No Approval Required (high-cost)" does **not** mean RequirePublishApproval is off. Check the separate line "Publish approval (Story 5.6): Required" — that confirms RequirePublishApproval is enabled.

---

## UAT: Step-by-Step

### Phase A: Threshold Not Met (Blocking)

1. **Config:** Set `TestThresholdEnabled = 1`, `TestThresholdValue = 3`, `RequirePublishApproval = 1` for company 1016.
2. **Reset form:** Ensure test form (e.g. Form 56 or 57) is Draft. Clear FormPublishRequest if any exist for this form.
3. **Demo tests:** Complete **2** demo submissions (preview) or click "Record test run" twice — stay below 3.
4. **Login as Company User** (company 1016).
5. **Open Form 56** in Form Detail (eye icon) or Form Builder.
6. **Verify:** Readiness shows "1 more test run(s) needed" (or similar).
7. **Verify:** "Request Publish" button is **disabled** with tooltip (e.g. "1 more test run(s) needed").
8. **Verify:** Company Admin cannot publish from Edit Form — changing Form Status to Published should **fail** with backend error (e.g. "1 more test run(s) needed").

### Phase B: Threshold Met → Request Publish

1. **Add one more test:** Submit via preview again OR click "Record test run" in Form Detail.
2. **Verify:** Readiness shows "Ready to publish".
3. **As Company User:** Click **Request Publish** (Builder header or Form Detail footer).
4. **Modal:** Enter optional message → Submit.
5. **Verify:** Success; Form status becomes "Pending Admin Review".
6. **Verify DB:** `SELECT * FROM dbo.FormPublishRequest WHERE FormID = 56 AND Status = 'pending'` — 1 row.
7. **Logout;** login as **Company Admin** (same company).
8. **Open Dashboard** — the **Pending Publish Requests** card should appear **above** the Company List (between KPI and companies), with Form 56 listed.
9. **Click "Review & Publish"** — navigates to `/forms/56/review`.
10. **Form Review page:** "Open in preview" opens the form in a new tab for testing. After testing, use **Approve & Publish** (with optional comment) or **Reject** (with optional reason). Approve publishes the form; Reject returns it to Draft.

### Phase C: Duplicate Request (Idempotent)

1. As Company User, with form already in Pending Admin Review from Phase B.
2. Click **Request Publish** again.
3. **Verify:** No error; same existing request returned (no duplicate row in FormPublishRequest).

### Phase D: RequirePublishApproval Disabled

1. Set `RequirePublishApproval = 0` for company 1016.
2. As Company User, open a Draft form with readiness met.
3. **Verify:** CTA shows **"Publish"** (not "Request Publish"); User can publish directly (subject to threshold).

---

## Troubleshooting: Request Publish Button or "Publish approval: Required" Missing

If you don't see the Request Publish button or "Publish approval: Required" despite RequirePublishApproval=1 in DB:

1. **User role:** Request Publish and "Publish approval: Required" show **only for Company Users** (not Company Admins). Company Admins see Publish/Approve directly.
2. **Config API:** Open DevTools → Network; reload Form Detail. Check `GET /api/forms/company-test-config` — response should have `requirePublishApproval: true`. If it fails or returns false, the frontend never shows the button.
3. **Company scope:** The API uses `current_user.company_id`. Ensure your logged-in user is in company 1016.
4. **Row exists:** If `CompanyFormTestConfig` has no row for company 1016, the API returns defaults (requirePublishApproval: false). Use the upsert SQL above.

**422 on GET /api/forms/company-test-config:** Fixed by registering `forms_readiness_router` **before** `forms_router` in `main.py`. Previously the path was matched as `form_id="company-test-config"` and failed validation. Restart the backend after this fix.

**Request Publish button (Phase A Step 7):** The button is now shown **disabled** when threshold is not met, with a tooltip (e.g. "1 more test run(s) needed"). Previously it was hidden — if you don't see it after this fix, verify points 1–4 above.

**"Open in preview" vs "Record test run":** When you need more test runs, the link now says **"Open in preview"** (for users with Manage access) — it opens the form in a new tab so you can complete and submit a real test. Submitting the form in preview counts as a test run. "Record test run" (one-click, for Edit-only users) still adds a run without opening preview, but may cause **Demo Leads** to stay lower than the readiness count (readiness = preview submissions + explicit records).

---

## Common Pitfalls

| Mistake | Result | Fix |
|---------|--------|-----|
| Manually set Form Status to "Pending Admin Review" in Edit Form | No FormPublishRequest created; Admin card empty | Use **Request Publish** button |
| TestThresholdEnabled = 0 | Threshold disabled; never blocked | Set TestThresholdEnabled = 1 |
| Wrong company context | Admin sees different company's forms | Ensure Admin is in same company (1016) |
| Card not visible | Card returns null when 0 requests | PendingPublishRequestsCard now always shows; "No pending publish requests" when empty |
| Logged in as Company Admin | No Request Publish, no "Publish approval: Required" | Test as **Company User** for that flow |

---

## Admin Visibility Note

The **Pending Publish Requests** card is rendered **only when there are pending requests**. If the card does not appear, there are no `FormPublishRequest` rows for your company. Create a request via **Request Publish** (not by manually changing form status).

---

## Pass Criteria

- [x] Phase A: Threshold blocking works (Request Publish disabled; Admin publish blocked)
- [x] Phase B: Request Publish creates request; Admin sees card; can publish after review
- [x] Phase C: Duplicate request handled (idempotent)
- [x] Phase D: When RequirePublishApproval off, Company User sees Publish
- [x] No regressions in form save/load or readiness display

---

## API Shortcut (If UI Fails)

To create a publish request without the UI (e.g. for testing Admin queue):

```http
POST /api/forms/56/publish-request
Content-Type: application/json
Authorization: Bearer <company_user_token>

{"message": "Please review"}
```

Requires: Company User token, form in Draft, readiness met (when TestThresholdEnabled=1).

---

---

## Recommended Fixes (Before Next Story)

| Issue | Fix | Status |
|-------|-----|--------|
| Admin sees no indicator when 0 requests | PendingPublishRequestsCard now always shows; displays "No pending publish requests" when empty | Done |
| Manual status change bypasses flow | Consider restricting Edit Form: Company User cannot set Form Status to Pending Admin Review; only Request Publish API should set it | Deferred |
| TestThresholdEnabled=0 masks blocking | Form Workflow Thresholds UI (next story) will make config clearer | Next story |

---

*Refined 2026-02-17 — addresses manual testing confusion.*
