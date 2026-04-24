# Story 6.4 — Single-Session Dev Prompt

**Story:** 6.4 — AI Agent Panel Production Polish + User Preferences Architecture Foundation  
**Agent:** `@bmad-agent-bmm-dev`  
**Worktree:** _Created by **`@bmad-agent-bmm-sm`** via `./scripts/git/new-story.ps1`_  
**Branch:** `story/epic6-6.4-ai-panel-polish-and-prefs-foundation` (expected)  
**PR:** Draft PR → merge to `master` via GitHub  
**Sizing:** **M-L (12-15 working days)** — multi-session likely. Recommend a clean session boundary between the foundation layer (§A below) and the polish-consumption layer (§B below).

---

## Execution contract

Implement **`docs/stories/story-6.4.md`** using **`docs/stories/story-context-6.4.xml`** as the map.

This story has TWO intertwined deliverables shipping in ONE PR:
- **Foundation layer (§A):** User Preferences architecture (3 new tables + 3 endpoints + Notifications UI section). Mirrors `config.AppSetting` pattern.
- **Polish layer (§B):** AI Agent panel production polish (5 polish items wired against the new foundation).

Build §A FIRST (it's the substrate §B consumes). Do not start §B until §A is green and passes its ACs (9-16).

Do not claim story complete without:

- All 19 ACs verified (8 polish + 8 foundation + 3 process) in `STORY-6.4-GATE-EVIDENCE.md`
- `docs/USER-PREFERENCES-ARCHITECTURE.md` exists per AC-16
- Green test/lint commands recorded
- Migration count matches AC-17 exactly (6 expected, ≤4 files if collapsed)
- 3 UAT rounds completed (single-variable per round per Multi-Round UAT Protocol)
- `STORY-6.4-CLOSEOUT-REPORT.md` (MANDATORY — both criteria (a) public API surface + (b) ≥1 schema migration trigger this from PR #65 rule)

---

## Step 0 — Preflight

After SM creates the worktree and Human opens it in this Cursor window, run:

```powershell
.\scripts\workflow\preflight-story.ps1 `
  -ExpectedWorktreePath "C:\wt\elp\story-epic6-6.4-ai-panel-polish-and-prefs-foundation" `
  -ExpectedBranch "story/epic6-6.4-ai-panel-polish-and-prefs-foundation" `
  -ReportFile "docs/stories/STORY-6.4-PREFLIGHT.md"
```

**These paths will be confirmed by SM after `new-story.ps1` runs — use the actual values from `git worktree list` if they differ.**

---

## Step 1 — Read sources (in order)

1. `docs/stories/story-6.4.md` — the spec (all 19 ACs)
2. `docs/stories/story-context-6.4.xml` — the implementation map (file list, constraints, AC mapping)
3. `docs/stories/EPIC-6-WORKFLOW-GUIDE.md` — closeout checklist + mandatory closeout report rule
4. `backend/models/config/app_setting.py` — the canonical pattern UserPreference must mirror
5. `backend/models/ref/setting_type.py` — REUSE this for UserPreferenceKey.SettingTypeID
6. `backend/models/user.py` — current User model (existing FK preference columns stay UNCHANGED)
7. `backend/schemas/form_definition.py` (line 258 for `aiAgentSettings.lastPrompt` field) + `backend/tests/test_form_definition_ai_agent_settings.py`
8. `frontend/src/features/preferences/components/AccountSettingsPopup.tsx` — pattern reference for the new Notifications section
9. `frontend/src/features/builder/components/ai/AIAgentPanel.tsx` — the polish target (lines 838-857, 860-881, 202-206)
10. `frontend/src/features/builder/stores/useBuilderStore.ts` — Undo reference for the modal copy

---

## §A — Foundation layer (build FIRST)

### Step A.1 — Schema design + migrations

Create three new tables per `story-6.4.md` §2.6.2:

1. `dbo.UserPreference` (per-user × preference values)
2. `ref.UserPreferenceCategory` (catalogue of categories: `Theme`, `Account`, `Notifications`, `AI Agent`)
3. `ref.UserPreferenceKey` (catalogue of available preferences with FK to existing `ref.SettingType`)

Plus seed migrations:

4. `ref.UserPreferenceCategory` initial rows (`Notifications` minimum)
5. `ref.UserPreferenceKey` row for `notifications.ai_agent.suppress_replace_warning` (Boolean type, default `"false"`)
6. `config.AppSetting` row for `form_ai.default_retries` (Integer type, value `"2"`)

**Constraints:**
- Match audit-column pattern from `User` and `AppSetting` (`CreatedDate`, `CreatedBy`, `UpdatedDate`, `UpdatedBy`, `IsDeleted`, `DeletedDate`, `DeletedBy`).
- Unique constraint on `UserPreference (UserID, PreferenceKeyID)`.
- Indexes on all FK columns.
- Verify `ref.SettingType` rows include `Boolean`, `Integer`, `String` at minimum — if missing, seed in a leading migration.
- **DO NOT auto-apply migrations.** Stop and ask Anthony to apply them per the workspace `database-migration-validator` rule.

### Step A.2 — Backend service + endpoints

Create the preferences service module + 3 endpoints:

| Method | Path | Purpose |
|--------|------|---------|
| `GET /api/me/preferences` | Returns prefs grouped by category with default-value fallback (AC-10) |
| `PATCH /api/me/preferences` | Partial upsert; transactional; per-key validation against ref.UserPreferenceKey (AC-11) |
| `DELETE /api/me/preferences/{key}` | Remove override row → next read returns default (AC-12) |

Reuse the same auth middleware as existing `/api/me`.

**Recommended optimization:** fold GET-preferences into the existing user-bootstrap response if there is one, to avoid a round-trip on app load. Dev call.

### Step A.3 — Backend tests

Add tests covering:
- Model layer (UserPreference + 2 ref tables — basic CRUD)
- Default-value fallback (read for user with no rows returns DefaultValue)
- Read endpoint shape + grouping
- Write endpoint validation per error class:
  - Unknown key → structured error
  - Inactive key → structured error
  - Type mismatch (e.g. "abc" for Integer key) → structured error
  - Transactional behavior (one bad key in batch → no writes happen)
- Reset endpoint behavior

### Step A.4 — Frontend Notifications section

Create the new Notifications section under `frontend/src/features/preferences/`:

- Sibling to `AccountSettingsPopup` — follow that pattern for modal/page structure, data loading, hasChanges tracking, toast notifications.
- **Render controls dynamically from API response** — do NOT hardcode the AI panel toggle.
- Dispatch control type by `SettingType`: Boolean → toggle/checkbox, Integer → number input, String → text input. Boolean is the only type required for AC-13; add Integer + String only if AC-15's demo preference uses them. Keep the dispatch logic small and isolated.
- Optimistic UI with rollback on error (use existing `useToastNotifications` for failure feedback).
- Empty-state: if no prefs in a category yet, show the section header with a minimal "No preferences yet" message — don't hide the surface.

### Step A.5 — Frontend tests

Add tests for:
- Section renders all preferences from API response
- Toggle interaction triggers PATCH; optimistic update + rollback on error
- Dynamic control dispatch by `SettingType` (verify with mocked Boolean entry; if §A.6 demo uses other types, verify those too)

### Step A.6 — Future-extensibility verification (AC-15)

Seed a second demo preference key (e.g. `notifications.ai_agent.show_compile_summary`, default `"true"`, Boolean) via the same migration mechanism. Verify the Notifications UI auto-renders a control for it WITHOUT touching frontend code. This is AC-15 — proves the architecture scales.

The demo key may stay as a documented "first additional pref" or be removed before merge — Dev call.

### Step A.7 — Architecture documentation (AC-16)

Create `docs/USER-PREFERENCES-ARCHITECTURE.md`. Cover:

1. **Schema diagram** — UserPreference + 2 ref tables + relationships
2. **Comparison/contrast with AppSetting** — what's the same (key/value/category/type, audit columns, ref.SettingType reuse), what's different (UserID FK on UserPreference; SettingCategoryID becomes UserPreferenceCategoryID with separate ref to allow user-only categories like "Notifications")
3. **3-step recipe for adding a new preference**:
   - Step 1: Add row to `ref.UserPreferenceCategory` if a new category is needed
   - Step 2: Add row to `ref.UserPreferenceKey` (key, category, type, default, displayName, description)
   - Step 3: Consume from feature code via `GET /api/me/preferences` (frontend renders automatically; feature code reads `prefs[categoryName].entries.find(e => e.preferenceKey === "...")?.value`)
4. **Default-value fallback semantics** — when no UserPreference row exists, return DefaultValue
5. **Migration policy** — ref seeds are migration-managed (not runtime-mutable); UserPreference rows are runtime-mutable per user
6. **What's explicitly out of scope** — migrating existing User.ThemePreferenceID etc. into UserPreference; admin UI; net-new notification *delivery* infrastructure

---

## §B — Polish layer (build SECOND, after §A is green)

### Step B.1 — AC-1: Last prompt persistence

- On AIAgentPanel mount: hydrate `prompt` textarea from `definition.aiAgentSettings.lastPrompt`
- On successful generation request dispatch (after API call returns, regardless of AI outcome): write trimmed `prompt` to `definition.aiAgentSettings.lastPrompt` and trigger existing form save flow
- Do NOT save on every keystroke
- Verify with: open form → submit prompt → reload → prompt restored. Switch to different form → that form's last prompt (or empty)

### Step B.2 — AC-2/3/4: Replace-form warning + "don't show again" preference

- Trigger condition: `useBuilderStore.components.length > 0` AND user clicks Generate
- Modal copy must contain words "replace" and "Undo" — suggested wording: *"Generating a new form will replace what's currently on the canvas. You can undo this if needed (Ctrl/Cmd+Z). Continue?"*
- Buttons: Confirm / Cancel
- "Don't show again" checkbox writes to `UserPreference` (`notifications.ai_agent.suppress_replace_warning = true`) on Confirm
- Read preference value on AIAgentPanel mount (via the new GET endpoint or bootstrap response)
- Empty canvas: skip warning entirely
- AC-3 verification requires actual logout/login during UAT (not just a local refresh) to prove server-side persistence

### Step B.3 — AC-5: Hide outbound transport selector

- Remove the `<select>` for "OpenAI outbound transport" (currently lines ~838-857 of `AIAgentPanel.tsx`)
- Keep the state and setter; always pass `"auto"` on requests
- KEEP the trace summary line `"OpenAI transport (resolved): <mode>"` for diagnostic visibility

### Step B.4 — AC-6: Hide retry input

- Remove the `<input type="number">` (currently lines ~860-881)
- Frontend stops sending `maxSystemCorrectionAttempts` on the request payload entirely
- Backend reads `form_ai.default_retries` from AppSetting (cached on startup, with a manual reload endpoint OR per-request — Dev call; favor startup-cached)
- Verification: update AppSetting row to `3`, reload, generation requests use 3 retries

### Step B.5 — AC-7/8: Silent autoload

- Remove any "pending invalid draft" UI / warning banner / decision dialog from `handleGenerate` apply path
- If backend returns a definition: apply it to canvas immediately (regardless of soft validation issues)
- If backend returns no definition: keep existing failure message
- Trace summary still shows validation counts

---

## Step 6 — Gates

```powershell
cd backend; python -m pytest --tb=short
cd ..\frontend; npm run lint; npm run test:unit -- --watch=false
```

Record results in `docs/stories/STORY-6.4-GATE-EVIDENCE.md`. Confirm:

- Backend baseline preserved or improved (end-of-6.3.1 = 705 passed / 26 skipped)
- Frontend baseline preserved or improved (end-of-6.3.1 = 272 passed)
- Migration count matches AC-17 exactly

---

## Step 7 — UAT (Multi-Round Protocol)

Per the new Multi-Round UAT Protocol from PR #65, expect 3 rounds:

- **Round 1:** Foundation only — schema, endpoints, Notifications UI, dynamic dispatch verification (ACs 9-16). One variable focus.
- **Round 2:** Polish layer wired against foundation — last prompt, replace warning + suppress, transport hidden, retry hidden, silent autoload (ACs 1-8). One variable focus per session.
- **Round 3:** Catch-all + regression — verify nothing in 6.3.1 broke; verify default-value fallback for fresh user; verify AC-15 demo preference auto-renders.

Document each round in `STORY-6.4-UAT-RESULTS.md`.

---

## Step 8 — Closeout updates

- Update `story-6.4.md` Dev Agent Record fields (file list, decisions, deviations, sessions used, completion date).
- Write `STORY-6.4-CLOSEOUT-REPORT.md` per `STORY-6.3.1-CLOSEOUT-REPORT.md` template. **MANDATORY** for this story (both triggers (a) and (b) hit).
- Update `EPIC-6-STATUS.md` (mark 6.4 ✅ Complete with merge date and PR #).
- Update `EPIC-6-WORKFLOW-GUIDE.md` Current Focus → Story 6.5 (Image-to-Form).
- Date-stamp parity check (workflow guide row 7): `git log` merge date matches `gh pr view <N> --json mergedAt` matches `Completed:` field in `story-6.4.md`.
- Worktree retired (workflow guide row 8): `git worktree remove "<path>"` after merge confirmed.

---

## Out-of-scope reminders

- ❌ DO NOT modify existing `User.ThemePreferenceID` / `LayoutDensityID` / `FontSizeID` / `PreferredLanguageID` / `CountryID` columns
- ❌ DO NOT migrate existing prefs into `UserPreference` (separate cleanup story if ever needed)
- ❌ DO NOT build Admin UI for the new ref tables
- ❌ DO NOT build notification *delivery* infrastructure (email, push, in-app) — this is preference STORAGE only
- ❌ DO NOT auto-apply Alembic migrations from agent shell — Anthony runs them per `database-migration-validator` rule
- ❌ DO NOT run `new-story.ps1` — that's SM's job; Dev only implements in the worktree
- ❌ DO NOT exceed the AC-17 migration count without pausing for SM/PM confirmation

---

## When in doubt

- Re-read the constraint section of `story-context-6.4.xml`
- Re-read the §2.6.3 design rationale in `story-6.4.md` (preserved there for closeout report use too)
- Ask Anthony before deviating from the bounded migration set or the architecture pattern
