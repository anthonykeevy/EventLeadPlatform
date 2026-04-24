# Story 6.4 — AI Agent Panel Production Polish + User Preferences Architecture Foundation

**Epic:** 6 — AI Generation & Monetization Engine
**Story ID:** 6.4
**Title:** AI Agent Panel Production Polish + User Preferences Architecture Foundation
**Status:** 📝 **Draft** (SM authoring)
**Branch:** `story/epic6-6.4-ai-panel-polish-and-prefs-foundation` (to be created)
**PR:** *(none yet)*
**Depends On:**
- Story 6.3.1 ✅ Complete (PR #64) — semantic plan + deterministic compiler foundation
- PR #65 (workflow guide post-6.3.1 improvements) — should merge before this story moves to Dev so the new mandatory closeout criteria + Multi-Round UAT Protocol are the active workflow when 6.4 closes
**Unblocks:**
- Story 6.5 (Image-to-Form) — the polish patterns AND the User Preferences architecture both feed forward (6.5 will store image-handling defaults using the same architecture)
- All future stories that need user-scoped preferences (notifications, billing email prefs, etc.) — this is the canonical foundational story
**Created:** 2026-04-23
**Rescoped from:** "AI Iteration on Existing Designs" (deferred post-MVP per 2026-04-23 PM/SM joint scope review). Subsequently expanded same day to include the User Preferences architecture foundation per Tonyk's request for "aligned database architecture to support this level of managing User preferences".

---

## 1) Goal

Two intertwined goals that ship together as one PR:

### 1.1 Tactical: AI Agent panel production polish

Take the AI Agent panel (`frontend/src/features/builder/components/ai/AIAgentPanel.tsx`) from "demonstrably-working POC after Story 6.3.1's many UAT rounds" to **ship-ready production UI** by:

1. Persisting the user's last prompt so a reload doesn't lose work-in-progress (DB-backed).
2. Making destructive actions (regenerate over an existing form) **opt-in safe** — explicit warning, with "don't show again" preference referencing the existing builder Undo (already implemented in `useBuilderStore` history stack).
3. Removing power-user controls that confuse non-developers in MVP — outbound transport selector and per-request retry override become server-managed defaults via `config.AppSetting`.
4. Failing quietly on benign validation issues — load the AI's best-effort definition onto the canvas without surfacing internal validation chatter to the end user.

### 1.2 Foundational: User Preferences architecture

Establish a scalable, schema-aligned User Preferences architecture that mirrors the existing `config.AppSetting` pattern, so:

- The "don't show again" preference from §1.1 has a proper home (not localStorage, not a one-off JSON column).
- A new **Notifications** section appears in the existing `frontend/src/features/preferences/` UI, slotting alongside Theme and Account.
- All future preference-driven features (billing email prefs, notification toggles for any module, image-handling defaults for Story 6.5, etc.) plug into the same key/value/category surface without per-feature schema migrations.

### 1.3 Why these two ship together

Originally Story 6.4 was scoped as polish-only. During 2026-04-23 architectural review, Tonyk identified that bolting the "don't show again" preference onto the existing typed FK pattern (`User.ThemePreferenceID` etc.) would be inconsistent — the existing FK pattern is correct for single-value enums (theme, density, font-size) but creates schema bloat for boolean toggles. Storing it in `localStorage` would also be inconsistent with the platform's commitment to user-portable preferences. The right answer is a `UserPreference` key/value table that mirrors `AppSetting`, and that architecture is foundational enough that the polish work and the architecture should ship together so we don't dual-implement.

This is an **M-L** story (revised 2026-04-23 from initial S sizing): polish UI + new tables + new API surface + new Preferences UI section + integration. Per the new mandatory closeout-report rule from PR #65, Story 6.4 will require a closeout report (triggered by all three criteria: schema migrations, new public API surface, and "first deployment of preferences architecture" is in-scope work that, while not deferred, deserves explicit decision documentation).

---

## 2) In Scope

### 2.1 Persist last prompt (per form, database-backed via existing `aiAgentSettings.lastPrompt`)

| Area | Requirement |
|------|-------------|
| **Storage** | **Existing** `definition.aiAgentSettings.lastPrompt` field (already defined in `backend/schemas/form_definition.py` from Story 6.3 — verify with `backend/tests/test_form_definition_ai_agent_settings.py`). The form's definition JSON is already persisted in the database via the standard form save path, so no schema migration is required. The field already enforces `max_length=4000`. |
| **Save trigger** | Save the trimmed prompt to `definition.aiAgentSettings.lastPrompt` and trigger the existing form-save flow whenever a generation request is **successfully dispatched**. Do **not** save on every keystroke. |
| **Restore behavior** | On `AIAgentPanel` mount, hydrate the `prompt` textarea from `definition.aiAgentSettings.lastPrompt` if present. Different forms remember their own different last prompts. |
| **Migration check** | Confirm the `aiAgentSettings.lastPrompt` field is present in production form schemas — if missing in any environment, that's a Story 6.3 deployment gap, not new 6.4 work. |
| **Privacy** | Prompt is user-authored design intent, stored alongside the form definition with the same access controls as the form itself. |

### 2.2 Replace-existing-form warning (consumer of new User Preferences architecture)

| Area | Requirement |
|------|-------------|
| **Trigger condition** | When user clicks Generate AND the canvas already contains ≥1 user-placed component (i.e. `useBuilderStore.components.length > 0`). |
| **Modal copy** | Plain English. Must explicitly mention that **Undo** (Ctrl/Cmd+Z) will restore the previous form — Undo history is preserved across AI generations. Suggested wording: *"Generating a new form will replace what's currently on the canvas. You can undo this if needed (Ctrl/Cmd+Z). Continue?"* |
| **Buttons** | Confirm (proceed with generation) / Cancel. |
| **"Don't show again" checkbox** | Persisted to the new `UserPreference` table introduced in §2.6, with `PreferenceKey = "notifications.ai_agent.suppress_replace_warning"` (under category `Notifications`). Read on panel mount, written when user checks the box and confirms. |
| **Reset path** | The new Notifications section in the Preferences UI (§2.7) provides a toggle to flip the preference back on. No need for a separate reset link inside the AI Agent panel. |
| **Empty canvas** | Skip the warning entirely — no destructive action. |

### 2.3 Hide outbound transport selector (lock to Auto)

| Area | Requirement |
|------|-------------|
| **UI change** | Remove the `<select>` for "OpenAI outbound transport" (currently lines ~838–857 of `AIAgentPanel.tsx`). |
| **State retention** | Keep the `openaiTransport` state and the `setOpenaiTransport` setter in the component (still needed for the API call), but **always pass `"auto"`** — let the server's `FORM_AI_OPENAI_TRANSPORT` env var be the single source of truth for transport selection. |
| **Diagnostic escape hatch** | The trace summary line that displays `"OpenAI transport (resolved): <mode>"` **stays** so dev/UAT can still see what the server actually used. |

### 2.4 Hide manual retry override (default sourced from `config.AppSetting`)

| Area | Requirement |
|------|-------------|
| **UI change** | Remove the `<input type="number">` for "System correction attempts (retry count)" (currently lines ~860–881 of `AIAgentPanel.tsx`). |
| **Default source** | Add a row to the existing `config.AppSetting` table. Recommended: `SettingKey="form_ai.default_retries"`, `SettingValue="2"`, `DefaultValue="2"`, `SettingTypeID` → Integer ref, `SettingCategoryID` → an appropriate category (`Form AI` or similar — Dev to choose existing or seed one), `IsEditable=true`, `MinValue=0`, `MaxValue=10`. |
| **Backend read** | The form-AI service reads this setting (cached on startup OR per-request — Dev call; favor startup-cached with a manual reload endpoint for ops). |
| **Frontend hardcode** | Frontend stops sending `maxSystemCorrectionAttempts` on the request payload entirely. |
| **Migration** | One seed migration adding the AppSetting row (and its supporting category ref row if not already present). |

### 2.5 Silent autoload on validation issues

| Area | Requirement |
|------|-------------|
| **Current behavior to remove** | Any "pending invalid draft" UI / warning banner / decision dialog that currently asks the user whether to load a definition with validation warnings. |
| **New behavior** | If the backend returns a definition (whether or not validation surfaced soft issues), apply it to the canvas immediately. |
| **Trace surface** | The trace summary line below the panel **still** shows validation counts / fallback counts for diagnostic visibility — only the user-facing modal/banner is removed. |
| **Hard failure exception** | If the backend returns no definition at all, surface the existing failure message — silent autoload only applies to "definition returned, soft validation issues". |

### 2.6 ⭐ NEW: User Preferences architecture foundation

This is the foundational architecture that §2.2 (and all future preference-driven features) consume. **Mirrors the existing `config.AppSetting` pattern.**

#### 2.6.1 New tables

| Table | Schema | Purpose |
|-------|--------|---------|
| `dbo.UserPreference` | One row per user × preference | Stores the **values** users have set |
| `ref.UserPreferenceCategory` | Catalogue of categories | Groups preferences for the UI (`Theme`, `Account`, `Notifications`, `AI Agent`, …) |
| `ref.UserPreferenceKey` | Catalogue of available preferences | Defines what preferences exist, their type, default, category, validation |

#### 2.6.2 Field-level requirements

**`dbo.UserPreference`:**
| Column | Type | Notes |
|--------|------|-------|
| `UserPreferenceID` | BigInteger PK | Auto-increment |
| `UserID` | BigInteger FK → `dbo.User.UserID` | NOT NULL, indexed |
| `PreferenceKeyID` | BigInteger FK → `ref.UserPreferenceKey.UserPreferenceKeyID` | NOT NULL, indexed |
| `PreferenceValue` | NVARCHAR(MAX) | Stored as string, type-converted on read using `SettingType` |
| `CreatedDate`, `CreatedBy`, `UpdatedDate`, `UpdatedBy`, `IsDeleted`, `DeletedDate`, `DeletedBy` | Standard audit columns | Match existing audit pattern (see `User`, `AppSetting`) |
| **Unique constraint** | `(UserID, PreferenceKeyID)` | Prevent duplicate rows for same user × preference |

**`ref.UserPreferenceCategory`:**
| Column | Type | Notes |
|--------|------|-------|
| `UserPreferenceCategoryID` | BigInteger PK | Auto-increment |
| `CategoryName` | NVARCHAR(100) | NOT NULL, unique (`Theme`, `Account`, `Notifications`, `AI Agent`) |
| `Description` | NVARCHAR(500) | Display text for category header in Preferences UI |
| `DisplayOrder` | INT | Sort order in the Preferences UI |
| `IsActive` | BIT | Hide categories without dropping them |
| Standard audit columns | | |

**`ref.UserPreferenceKey`:**
| Column | Type | Notes |
|--------|------|-------|
| `UserPreferenceKeyID` | BigInteger PK | Auto-increment |
| `PreferenceKey` | NVARCHAR(150) | NOT NULL, unique (e.g. `notifications.ai_agent.suppress_replace_warning`) |
| `PreferenceCategoryID` | BigInteger FK → `ref.UserPreferenceCategory.UserPreferenceCategoryID` | NOT NULL, indexed |
| `SettingTypeID` | BigInteger FK → `ref.SettingType.SettingTypeID` | **REUSE existing type ref** — no parallel type system. Boolean, Integer, String, JSON, etc. |
| `DisplayName` | NVARCHAR(200) | Human-readable label for the toggle/control in the Preferences UI |
| `Description` | NVARCHAR(500) | Help text displayed under the control |
| `DefaultValue` | NVARCHAR(MAX) | Used when no `UserPreference` row exists for the user |
| `IsEditable` | BIT | Allow disabling user override (rare but useful) |
| `IsActive` | BIT | Soft-disable a preference without dropping the row |
| `SortOrder` | INT | Order within the category in the Preferences UI |
| Standard audit columns | | |

#### 2.6.3 Why this design (decision rationale, captured here for the closeout report)

- **Mirrors AppSetting** — both surfaces (application-wide config and per-user prefs) follow the same key/value/category/type pattern. One mental model. One review pattern.
- **Reuses `ref.SettingType`** — no parallel type-coercion logic; whatever AppSetting reads/writes for booleans/integers, UserPreference reuses unchanged.
- **Type-safe via FKs** — unlike a pure JSON column, every preference is governed by a catalogue row (`UserPreferenceKey`) that defines its type, default, validation. Enables admin tooling later.
- **Backwards-compatible with existing prefs** — current `User.ThemePreferenceID` / `LayoutDensityID` / `FontSizeID` / `PreferredLanguageID` / `CountryID` columns **stay unchanged** in this story. They're shipped, working, and migrating them to `UserPreference` is a separate concern. (A future cleanup story may unify if useful — explicitly out of scope here.)
- **Default-value fallback** — when no `UserPreference` row exists for a user × key, the read API substitutes `ref.UserPreferenceKey.DefaultValue`. New users have all their defaults immediately without backfill.
- **Scales linearly** — adding a future preference = one ref-table seed row + frontend control. No User-table column churn.

#### 2.6.4 Backend API surface (new endpoints)

| Method | Path | Purpose |
|--------|------|---------|
| `GET /api/me/preferences` | Returns the current user's preferences, grouped by category. Each entry includes the catalogue metadata (`PreferenceKey`, `DisplayName`, `Description`, `SettingType`, `DefaultValue`, `SortOrder`) plus the user's effective `value` (their override OR the default). Used by the Preferences UI to render and by feature panels (like AIAgentPanel) to read individual preferences. |
| `PATCH /api/me/preferences` | Accepts a partial dict of `{preferenceKey: value}` and upserts into `UserPreference`. Validates each key against the catalogue (key exists + active + value parses as `SettingType`). Returns the updated preferences (same shape as GET). |
| `DELETE /api/me/preferences/{preferenceKey}` | Reset a single preference back to default (deletes the `UserPreference` row). Used by the Preferences UI's "Reset to default" affordance. |

**Read-side optimization (recommended)**: fold the GET-preferences response into the existing user-bootstrap call (`/api/me` or equivalent) to avoid an extra round-trip on app load. Dev call.

#### 2.6.5 Documentation deliverable

A new doc `docs/USER-PREFERENCES-ARCHITECTURE.md` (~200-400 lines) covering: schema diagram, comparison/contrast with AppSetting, how to add a new preference (3-step recipe: seed ref row → add UI control → consume from feature code), how default-value fallback works, migration policy. This is the canonical reference for any future story adding prefs.

### 2.7 ⭐ NEW: Notifications section in Preferences UI (first consumer of new architecture)

| Area | Requirement |
|------|-------------|
| **Location** | New section/popup/page (Dev choice based on existing `AccountSettingsPopup` pattern) under `frontend/src/features/preferences/`, sibling to Theme/Account. |
| **Content** | One toggle for the AI panel suppress-warning preference (`notifications.ai_agent.suppress_replace_warning`). Plus structural scaffolding ready for future preferences to slot in. |
| **Toggle behavior** | Reads from `GET /api/me/preferences`, writes via `PATCH /api/me/preferences`. Optimistic UI with rollback on error. |
| **Future-friendly** | The section renders preferences dynamically from the API response (don't hardcode the AI panel toggle). When a future story adds a new ref row in the `Notifications` category, this UI picks it up automatically with no frontend change required for the ref-driven controls. (Type-specific UI controls — boolean toggle, integer input, dropdown — are dispatched from `SettingType`.) |
| **Empty-state** | If no preferences exist in a category yet, the section can either be hidden or show a minimal "No preferences yet" state. Dev call (favor "show with the section header so users know the surface exists"). |

### 2.8 Story pack requirements for SM delivery

| Area | Requirement |
|------|-------------|
| **Context artifact** | SM delivery includes `docs/stories/story-context-6.4.xml` listing the panel file + builder store + new preferences module + `User`/`AppSetting`/`SettingType` model files as the implementation map for Dev. |
| **Prompt artifact** | SM delivery includes `docs/stories/STORY-6.4-SINGLE-SESSION-DEV-PROMPT.md` (Dev-facing kickoff prompt, Step 0 preflight, file list). |
| **UAT artifact** | SM delivery includes `docs/stories/STORY-6.4-UAT-TEST-GUIDE.md` covering the polish ACs AND the preferences foundation ACs (one focused test per AC). Recommend 3 UAT rounds: Round 1 = preferences architecture stand-up + Notifications UI; Round 2 = AI panel polish ACs against the new preferences; Round 3 = catch-all + regression. |
| **Architecture doc** | `docs/USER-PREFERENCES-ARCHITECTURE.md` exists per §2.6.5. |

---

## 3) Out of Scope

| Item | Reason |
|------|--------|
| AI iteration on existing designs (the original 6.4 scope) | **Deferred post-MVP** per 2026-04-23 PM/SM joint review. |
| Migrating existing `User.ThemePreferenceID` / `LayoutDensityID` / `FontSizeID` / `PreferredLanguageID` / `CountryID` columns into `UserPreference` | Out of scope. They're shipped and working. A future cleanup/unification story may do this if benefits emerge — explicitly not 6.4's job. |
| Admin UI for managing the new ref tables | Out of scope. Admin tooling for `ref.UserPreferenceCategory` and `ref.UserPreferenceKey` deferred to a future Admin Console story. For now, ref rows are managed via DB / migrations. |
| Backfilling `UserPreference` rows for existing users | No backfill — default-value fallback per §2.6.3 means new and existing users behave identically without writing rows. Rows materialize naturally on first user override. |
| Cross-device prompt sync via dedicated endpoint | Naturally satisfied because `aiAgentSettings.lastPrompt` lives on the form definition (server-side). |
| Net-new normalized notification *delivery* system (email, push, in-app) | Out of scope. This story only adds **preference storage** for notification toggles — actual delivery infrastructure is a future epic. |
| Third-party preference sync (e.g. browser sync, OAuth provider sync) | Out of scope. |
| Telemetry / event tracking on preference changes | Out of scope for MVP. Capture the gap if useful for post-MVP analytics. |
| Backend `OpenAiTransportMode` enum cleanup / dead-code removal | Not required by ACs. |
| Submit-button validation parity (`g-frontend-submit-parity`) | Lives in `EPIC-6-CARRY-FORWARD-BACKLOG.md`. May be conditionally promoted to optional Story 6.4.1 if a polish task naturally bumps into it. |

---

## 4) Acceptance Criteria

### 4.1 AI Agent panel polish (the tactical layer)

1. **AC-1 (Last prompt persistence — DB-backed via `aiAgentSettings.lastPrompt`):** Submitting a prompt via the AI panel writes the trimmed prompt to `definition.aiAgentSettings.lastPrompt` and triggers form save. Reloading the builder page (same browser, different browser, or different device after re-login) restores the prompt textarea to that value. Switching to a different form shows that form's own last prompt (or empty if none). No reliance on `localStorage`.
2. **AC-2 (Replace-form warning — first time):** With ≥1 component on the canvas, clicking Generate with the warning preference NOT yet suppressed presents a modal dialog containing the words "replace" and "Undo" and offering Confirm / Cancel. Cancel aborts generation; Confirm proceeds.
3. **AC-3 (Replace-form warning — suppressed via `UserPreference`):** With ≥1 component on the canvas and the warning preference suppressed in the user's `UserPreference` row (key `notifications.ai_agent.suppress_replace_warning = true`), clicking Generate proceeds **immediately** without any modal. Suppression survives logout/login and works on a fresh browser session (verified by actually logging out and back in during UAT). Toggling the preference back off in the Notifications section restores warning behavior on the next destructive Generate.
4. **AC-4 (Empty canvas — no warning):** With **0** components on the canvas, clicking Generate proceeds immediately without any modal regardless of preference state.
5. **AC-5 (Outbound transport selector hidden):** The "OpenAI outbound transport" `<select>` is no longer rendered in the panel. The trace summary below the panel still shows the resolved transport string used by the server.
6. **AC-6 (Retry input hidden, default sourced from `config.AppSetting`):** The "System correction attempts" `<input type="number">` is no longer rendered in the panel. The backend reads the default value from a new `config.AppSetting` row (`SettingKey = "form_ai.default_retries"`, default value `2`). A test verifies that updating the AppSetting row to `3` and reloading config causes generation requests to use `3` retries — proving the value is genuinely sourced from the table.
7. **AC-7 (Silent autoload):** A generation that the backend returns with soft validation issues loads onto the canvas immediately. No "pending invalid draft" UI / warning banner / decision dialog is displayed. The trace summary still shows validation counts.
8. **AC-8 (Hard failure unchanged):** A generation that the backend cannot fulfil still surfaces the existing user-visible failure message — silent autoload only applies to "definition returned, soft validation issues".

### 4.2 User Preferences architecture (the foundational layer)

9. **AC-9 (Schema):** Three new tables exist with the column shapes specified in §2.6.2: `dbo.UserPreference` (with unique constraint on `UserID + PreferenceKeyID`), `ref.UserPreferenceCategory`, `ref.UserPreferenceKey` (with FK to existing `ref.SettingType`). All have proper indexes on FK columns and standard audit columns matching the existing `User`/`AppSetting` patterns.
10. **AC-10 (Read API):** `GET /api/me/preferences` returns the current user's preferences grouped by category. Each entry includes `preferenceKey`, `displayName`, `description`, `settingType`, `defaultValue`, `sortOrder`, AND the user's effective `value` (override OR default). For a brand-new user with no `UserPreference` rows, every catalogue entry still appears with its `DefaultValue` as `value` — verified via UAT or test using a fresh user.
11. **AC-11 (Write API):** `PATCH /api/me/preferences` accepts a partial dict of `{preferenceKey: value}`. For each key: (a) verifies the key exists in `ref.UserPreferenceKey` and `IsActive=true`; (b) validates the value parses as the declared `SettingType`; (c) upserts into `UserPreference`. Invalid keys/values return a structured error per key without applying any partial writes (transactional). Returns the updated preferences (same shape as GET).
12. **AC-12 (Reset API):** `DELETE /api/me/preferences/{preferenceKey}` removes the user's override row, causing the next read to return the catalogue's `DefaultValue`.
13. **AC-13 (Notifications UI section):** A new Notifications section is visible in the Preferences UI (`frontend/src/features/preferences/`), following the existing `AccountSettingsPopup` pattern. It contains the AI panel suppress-warning toggle. The toggle reads/writes via the new API endpoints. Optimistic UI with rollback on error.
14. **AC-14 (Default-value fallback works end-to-end):** A user who has never visited the Notifications section sees the default toggle state (warning enabled, since `DefaultValue = "false"` for `notifications.ai_agent.suppress_replace_warning`). Clicking Generate over a non-empty canvas shows the modal. After they check "don't show again" and Confirm, a `UserPreference` row materializes; subsequent loads read it.
15. **AC-15 (Future-extensibility demo):** Add a second "demo" preference key during dev (e.g. `notifications.ai_agent.show_compile_summary`, default `true`, type Boolean) — not surfaced in any feature code, just seeded into `ref.UserPreferenceKey`. Verify the Notifications UI **automatically renders a control for it** without any frontend code change (controls are dispatched from `SettingType`). This proves the architecture genuinely scales. The demo key may stay in the migration as a documented "first additional pref" or can be removed before merge — Dev call.
16. **AC-16 (Architecture doc):** `docs/USER-PREFERENCES-ARCHITECTURE.md` exists and covers schema, comparison with AppSetting, 3-step recipe for adding a new preference, default-value fallback semantics, and migration policy.

### 4.3 Process / hygiene

17. **AC-17 (Bounded migration set):** This story is expected to ship the following migrations and **no others** (treat any additional migration as a scope-creep red flag):
    - One structural migration: `dbo.UserPreference` table
    - One structural migration: `ref.UserPreferenceCategory` table
    - One structural migration: `ref.UserPreferenceKey` table
    - One seed migration: `ref.UserPreferenceCategory` initial rows (`Notifications` minimum; optionally `Theme`, `Account`, `AI Agent` placeholders)
    - One seed migration: `ref.UserPreferenceKey` row for `notifications.ai_agent.suppress_replace_warning`
    - One seed migration: `config.AppSetting` row for `form_ai.default_retries`
    - **Total: 6 migrations.** Dev may collapse the table-creation migrations into 1–2 files at their discretion (target: ≤4 migration files total if collapsed). If the count exceeds the documented set, pause and confirm with SM/PM.
18. **AC-18 (Regression safety):** Existing backend tests (especially `test_form_definition_ai_agent_settings.py` and any Story 6.3.1 generation tests) remain green or are intentionally updated with rationale. Existing frontend tests remain green or are intentionally updated with rationale. End-of-6.3.1 baselines: backend 705 passed / 26 skipped; frontend 272 passed.
19. **AC-19 (SM context pack completeness):** Story cannot move to Dev execution until SM artifacts exist for `story-context-6.4.xml`, `STORY-6.4-SINGLE-SESSION-DEV-PROMPT.md`, and `STORY-6.4-UAT-TEST-GUIDE.md`.

---

## 5) Definition of Done

- [ ] All ACs (1–19) met with evidence in `STORY-6.4-GATE-EVIDENCE.md`
- [ ] `python -m pytest --tb=short` green (no regressions vs end-of-6.3.1 baseline of 705 passed / 26 skipped). New tests added for: `UserPreference` model, preference catalogue ref tables, the read/write/reset API endpoints (happy path + each validation failure mode), `AppSetting` read for `form_ai.default_retries`.
- [ ] `npm run lint` green (0 warnings)
- [ ] `npm run test:unit -- --watch=false` green (no regressions vs end-of-6.3.1 baseline of 272 passed). New tests added for: Notifications UI section render, optimistic update + rollback, dynamic control dispatch by `SettingType`.
- [ ] Human UAT pass recorded in `STORY-6.4-UAT-RESULTS.md` against `STORY-6.4-UAT-TEST-GUIDE.md` (3 rounds expected per §2.8)
- [ ] Migration set matches AC-17 (≤6 new files; precisely the listed set; no others)
- [ ] Each new migration was run by Anthony per the workspace `database-migration-validator` rule (do not auto-apply migrations from agents)
- [ ] `docs/USER-PREFERENCES-ARCHITECTURE.md` exists per AC-16
- [ ] SM story pack artifacts exist: `story-context-6.4.xml`, `STORY-6.4-SINGLE-SESSION-DEV-PROMPT.md`, `STORY-6.4-UAT-TEST-GUIDE.md`
- [ ] **`STORY-6.4-CLOSEOUT-REPORT.md` exists — MANDATORY** (triggered by criterion (a) public API surface change AND (b) ≥1 schema migration of the new rule shipped in PR #65). Report should follow the canonical Story 6.3.1 template and explicitly cover: AC matrix, migration list with one-line rationale per migration, the §2.6.3 design rationale (preserved from this story doc), what this unlocks for Story 6.5 and beyond, hygiene performed (worktree retired, etc.), and decision/sign-off.
- [ ] Story closeout updates in `EPIC-6-STATUS.md` (mark 6.4 ✅ Complete with merge date) and `EPIC-6-WORKFLOW-GUIDE.md` (update Current Focus pointer to Story 6.5 — Image-to-Form)
- [ ] Date-stamp parity check (per workflow guide row 7): `Completed` date in `story-6.4.md` and merge date in `EPIC-6-STATUS.md` both equal the actual GitHub `mergedAt` date (UTC) — verify via `gh pr view <N> --json mergedAt,state,mergeCommit`
- [ ] Worktree retired (per workflow guide row 8): `git worktree remove "<path>"` after merge confirmed

---

## 6) Sizing & Risk

**Sizing:** **M-L** — estimated 12-15 working days.

| Workstream | Estimate |
|------------|----------|
| Schema design + 3 new tables + ref seeds + AppSetting seed (6 migrations) | 2-3 days |
| Backend API endpoints (read/write/reset) + service layer + tests | 2-3 days |
| Frontend Notifications UI section + dynamic control dispatch + tests | 2-3 days |
| AI Agent panel polish items (§2.1–§2.5) wiring against new architecture | 2 days |
| Architecture documentation (`USER-PREFERENCES-ARCHITECTURE.md`) | 0.5-1 day |
| UAT (3 rounds expected — single-variable per round per Multi-Round UAT Protocol) | 2-3 days |
| Closeout report + governance hygiene | 1 day |

**Why this is M-L not S:** Two weighted factors: (a) net-new database tables + new public API surface = real architectural surface to design + test; (b) frontend dynamic-control dispatch (the §2.7 "future-friendly" requirement) is not trivial — needs to handle Boolean / Integer / String / future SettingTypes cleanly and degrade gracefully when an unknown type appears. Both are worthwhile investments because **every future preference-driven feature gets cheaper** once this is in place — but they're real work, not trivial.

**Top risks and mitigations:**

| Risk | Mitigation |
|------|------------|
| `SettingType` ref table doesn't currently include all the types we need for prefs (Boolean specifically — verify) | First step of dev: confirm `SettingType` rows include at least Boolean, Integer, String, JSON. If missing, seed in a leading migration. Should be 1-line additions if needed. |
| Dynamic control dispatch in frontend gets messy across `SettingType`s | Start with Boolean only as the demo (covers the AI panel preference). Add Integer and String controls if AC-15 demo preference needs them, otherwise defer. Keep dispatch logic small and isolated. |
| Future preferences UI design (when there are 20+ prefs across 5 categories) outgrows the simple list-render approach | This story ships the data model + API + a basic UI. UI redesign for scale is a future concern and explicitly out of scope. |
| The "Notifications" category pulls in actual notification *delivery* expectations from the user | Keep the section copy clear: this is **preference storage**. Actual notification delivery (email, push) is a future epic. The toggle for AI panel warnings is honest because the warning is in-product UI, not a notification delivery channel. |
| Token / auth scope on new `/api/me/preferences` endpoints | Reuse the same auth middleware as `/api/me`. Standard pattern; should be a 1-line decorator. |

---

## 7) References

### Architecture & history
- `docs/stories/STORY-6.3.1-CLOSEOUT-REPORT.md` — the architecture this polish sits on top of
- `docs/stories/STORY-6.3.1-UAT-RESULTS.md` — UAT lineage that produced the working POC
- `docs/stories/EPIC-6-STATUS.md` — current roadmap with rescope context
- `docs/stories/EPIC-6-WORKFLOW-GUIDE.md` — workflow rules + 2026-04-23 changelog entries explaining the rescope

### Foundation patterns being mirrored
- `backend/models/config/app_setting.py` — the canonical AppSetting pattern that `UserPreference` mirrors
- `backend/models/ref/setting_type.py` — reusable type ref (REUSE — do not duplicate)
- `backend/models/ref/setting_category.py` — pattern reference for ref category tables
- `backend/models/user.py` — existing User model and its current FK-to-ref preference columns (Theme/Density/FontSize/Language/Country) — these stay unchanged

### Forward-look
- `docs/stories/STORY-6.5-FEASIBILITY-NOTES.md` — Image-to-Form will use the same preferences architecture for its image-handling defaults

### Implementation surface
- `frontend/src/features/builder/components/ai/AIAgentPanel.tsx` — the polish target
- `frontend/src/features/builder/stores/useBuilderStore.ts` — undo/redo history (referenced in modal copy)
- `frontend/src/features/builder/api/aiFormGenerationApi.ts` — request shape; transport + retries handled differently per §2.3, §2.4
- `frontend/src/features/preferences/` — existing preferences module; Notifications section gets added here
- `frontend/src/features/preferences/components/AccountSettingsPopup.tsx` — pattern reference for the new Notifications popup/page
- `backend/modules/users/router.py` — existing user router; new preferences endpoints likely live here or in a sibling `preferences/router.py`

---

## 8) Dev Agent Record

*To be completed by Dev during execution per the standard story template.*

**Agent:** *(TBD — recommend `@bmad-agent-bmm-dev` Amelia)*
**Sessions:** *(TBD — multi-session likely given M-L sizing; recommend a clean session boundary between the foundation layer and the polish-consumption layer)*
**Start:** *(TBD)*
**Closeout:** *(TBD)*

### What was implemented
*(TBD)*

### Decisions / deviations
*(TBD)*

### File List
*(TBD)*
