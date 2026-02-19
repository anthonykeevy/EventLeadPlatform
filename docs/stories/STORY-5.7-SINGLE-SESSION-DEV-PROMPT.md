# Story 5.7 Single-Session Dev Prompt

**Purpose:** Copy this entire prompt into a **new chat** to implement Story 5.7 in one session (skip Ralf-SM decomposition and task cycle).  
**Agent:** @dev (BMAD Developer Agent)  
**Workspace:** Open the Story worktree in Cursor: `C:\wt\elp\story-epic5-5.7-company-settings-hub`

---

## Copy everything below this line into a new chat

```markdown
@dev Implement Story 5.7: Company Settings Hub — Foundation in a single session. Skip Ralf; no task decomposition. Treat story-5.7.md, story-context-5.7.xml, and STORY-5.7-PM-DECISIONS.md as the sole source of truth.

---

## Git discipline (MANDATORY)

- **Work only in the Story worktree:** `C:\wt\elp\story-epic5-5.7-company-settings-hub`
- **Branch:** `story/epic5-5.7-company-settings-hub` (confirm you are on this branch; do NOT work on master)
- **No task branches:** All implementation goes directly on the story branch
- **Commit discipline (from Epic 5 lessons):**
  1. **Implementation commits FIRST** — before any closeout. Run `git status`; if backend/ or frontend/ code is modified, commit it with `feat(5.7): <description>`. Do NOT leave implementation uncommitted.
  2. **Closeout commit = docs only** — UAT results, status updates, completion notes go in a separate commit after implementation is committed.
  3. **Verify clean tree before push** — run `git status`; working tree must be clean (or only intentionally untracked)
- **PowerShell:** Do NOT use `&&`; use `;` for command chaining
- **Migrations:** I (human) will run Alembic commands; you create migration files and provide the exact command. Never run `alembic upgrade` yourself

---

## Story inputs (READ THESE)

- **Story:** `docs/stories/story-5.7.md`
- **Context:** `docs/stories/story-context-5.7.xml`
- **PM Decisions:** `docs/data-domains/CompanySettings/research/STORY-5.7-PM-DECISIONS.md` — source of truth for UX/behaviour
- **UAT guide:** `docs/stories/STORY-5.7-UAT-TEST-GUIDE.md`
- **Data model:** `docs/data-domains/CompanySettings/research/data-model-analysis.md`
- **Existing:** CompanySettingsLayout.tsx, FormBrandingDefaultsPage.tsx, OnboardingStep2.tsx (ABR), UserMenu.tsx, SmartCompanySearch, Asset model, CompanyFormTestConfig

---

## Implementation order (phased)

### Phase 1: Hub + Navigation
1. Extend CompanySettingsLayout: add Company Details, Form Approval Workflow, rename/section Assets (Images | Terms | Documents | Video). Update nav items.
2. Add "Company Settings" to UserMenu (Profile dropdown) — links to active company; **hide if user is not admin** for that company.
3. Mobile (<768px): hamburger + slide-over nav (or horizontal tabs fallback).
4. Entry points: cog (existing); Profile dropdown.

### Phase 2: Company Details
5. Create Company Details page: display name, legal name, ABN, billing (CompanyBillingDetails). GET/PUT APIs for Company + CompanyBillingDetails.
6. ABR search: "Search Australian Business Register" button → modal with SmartCompanySearch → on selection, close and populate form. "Enter manually" in modal and on form. AU only.
7. Non-AU / individuals: manual entry only. Support placeholder company "Your Company".
8. Billing gate: require company details before billing (document; enforce in API when billing is implemented).

### Phase 3: Form Approval Workflow
9. Form Approval Workflow page: CompanyFormTestConfig (test threshold, Require publish approval). Use existing GET/PUT `/api/forms/company-test-config`. Add version table for audit.
10. Help: page header description; second-level descriptions; help buttons beside properties (Form Builder pattern).

### Phase 4: Assets
11. **ref.AssetType migration:** Add TERMS, DOCUMENT, VIDEO. Asset.WidthPx/HeightPx nullable.
12. **Images:** Grid/list toggle; DnD + file picker; delete confirmation; properties panel (display name, metadata, audit trail); forms-using-image (search DefinitionJSON); image swap (dims or aspect ratio; block if different; warn PNG→JPG).
13. **Terms:** Separate section; PDF + URL; URL validation; inline fallback; production simulation.
14. **Terms auto-mapping:** When company has Terms asset, Form Builder Terms component auto-uses it (assetRef support).
15. Save/feedback: useToastNotifications; unsaved-changes warning.

---

## UAT (maximize automation — show evidence for EACH test)

Create `docs/stories/STORY-5.7-UAT-RESULTS.md` with a table:

| Test ID | Description | Command/Action | Result | Evidence |
|---------|-------------|----------------|--------|----------|
| DC1 | Hub nav; cog + Profile; hide if not admin | Manual | — | — |
| DC2 | Company Details; ABR popup; manual entry | Manual | — | — |
| DC3 | Form Approval Workflow; help text | Manual | — | — |
| DC4 | Assets Images; grid/list; swap rules | Manual | — | — |
| DC5 | Terms auto-mapping | Manual | — | — |
| DC6 | Save; unsaved warning | Manual | — | — |
| Build/lint | Backend + frontend | pytest; npm run lint | PASS/FAIL | (snippet) |

**Cap long output** — use `Select-Object -First 50` or redirect to file.

---

## Workflow lessons (from Epic 5)

- **Cap long output** — pytest, npm run build can crash sessions. Limit output.
- **Implementation commits first** — never leave code uncommitted before closeout.
- **Migrations** — create migration files; human runs `alembic upgrade head`.
- **Onboarding refactor** (remove Step 2) — out of scope; separate story.

---

## Deliverables

1. Company Settings hub with full nav (Company Details | Form Approval Workflow | Form Branding | Assets)
2. Profile dropdown "Company Settings" (hide if not admin); mobile hamburger/slide-over
3. Company Details page with ABR popup, display name, billing
4. Form Approval Workflow page with help
5. Assets: Images (grid/list, DnD, delete, display name, forms usage, image swap); Terms (separate, PDF+URL)
6. ref.AssetType TERMS/DOCUMENT/VIDEO; Asset.WidthPx/HeightPx nullable
7. Terms component assetRef + auto-mapping
8. Save/feedback consistent; unsaved-changes warning
9. `docs/stories/STORY-5.7-UAT-RESULTS.md` with evidence table
10. All implementation committed and pushed; working tree clean

---

## Human handoff

After you complete: I will run the migration (you provide command), run manual UAT, then merge the Story PR to master.
```

---

*Prompt created for Story 5.7 single-session implementation*  
*PM decisions from STORY-5.7-PM-DECISIONS.md*  
*Last Updated: 2026-02-17*
