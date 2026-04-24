# Story 6.4 — UAT Test Guide

**Story:** 6.4 — AI Agent Panel Production Polish + User Preferences Architecture Foundation  
**Owner:** Anthony (Human UAT)  
**Prep:** Dev provides `STORY-6.4-GATE-EVIDENCE.md` + Draft PR link  
**Protocol:** Multi-Round UAT — 3 rounds expected, single-variable focus per round.

---

## Environment

- Branch: story branch `story/epic6-6.4-ai-panel-polish-and-prefs-foundation`
- Backend: usual local API + DB. Migrations applied by Anthony per workspace `database-migration-validator` rule.
- Frontend: usual `npm run dev`.
- LLM: optional for the polish ACs (AC-1, 2, 3, 7, 8 can use mocked AI responses for deterministic UAT).

---

## §1 — Automated gates (witness)

| Step | Command | Expected |
|------|---------|----------|
| 1.1 | From `backend/`: `python -m pytest --tb=short` | Pass — baseline 705 passed / 26 skipped (end-of-6.3.1) preserved or improved. New tests for UserPreference model, preference catalogue ref tables, the read/write/reset endpoints (happy path + each validation failure mode), AppSetting read for `form_ai.default_retries`. |
| 1.2 | From `frontend/`: `npm run lint` | Pass — 0 warnings |
| 1.3 | From `frontend/`: `npm run test:unit -- --watch=false` | Pass — baseline 272 passed (end-of-6.3.1) preserved or improved. New tests for Notifications UI section render, optimistic update + rollback, dynamic control dispatch by SettingType. |
| 1.4 | Migration count check: `git diff --stat master -- backend/migrations/versions/` | Matches AC-17: 6 expected, ≤4 files if collapsed. Any other count = scope-creep red flag — confirm with SM before proceeding. |

Record summary lines in `STORY-6.4-UAT-RESULTS.md`.

---

## §2 — Foundation layer (Round 1 focus)

Single-variable round: verify the User Preferences architecture in isolation, before any AI Agent panel changes are wired against it.

### §2.1 — Schema (AC-9)

| Step | Action | Expected |
|------|--------|----------|
| 2.1.1 | Inspect schema: `dbo.UserPreference`, `ref.UserPreferenceCategory`, `ref.UserPreferenceKey` | All three tables exist with the column shapes per `story-6.4.md` §2.6.2; standard audit columns; FK constraints enforced. |
| 2.1.2 | Verify unique constraint: try to insert two rows for same `(UserID, PreferenceKeyID)` | Second insert rejected with constraint violation. |
| 2.1.3 | Verify FK to existing `ref.SettingType`: try to insert a `UserPreferenceKey` row with non-existent `SettingTypeID` | Insert rejected. Confirms no parallel type system was created. |
| 2.1.4 | Verify seed rows: query `ref.UserPreferenceCategory` and `ref.UserPreferenceKey` | At least `Notifications` category exists; at least `notifications.ai_agent.suppress_replace_warning` key exists with `DefaultValue = "false"` and Boolean `SettingType`. |
| 2.1.5 | Verify existing User columns unchanged | `User.ThemePreferenceID`, `LayoutDensityID`, `FontSizeID`, `PreferredLanguageID`, `CountryID` columns untouched and still functional (test by loading a user profile that uses them). |

### §2.2 — Read API (AC-10, AC-14)

| Step | Action | Expected |
|------|--------|----------|
| 2.2.1 | As an existing user, call `GET /api/me/preferences` | Returns 200; structure groups prefs by category; each entry has `preferenceKey`, `displayName`, `description`, `settingType`, `defaultValue`, `sortOrder`, `value`. |
| 2.2.2 | As a brand-new user (zero `UserPreference` rows), call `GET /api/me/preferences` | Returns 200; every catalogue entry still appears with `value` = `defaultValue`. **AC-14 default-value fallback verification.** |
| 2.2.3 | Inspect response for the AI panel preference | `notifications.ai_agent.suppress_replace_warning` present with `value = "false"` for both fresh and existing users. |

### §2.3 — Write API (AC-11)

| Step | Action | Expected |
|------|--------|----------|
| 2.3.1 | `PATCH /api/me/preferences` with `{notifications.ai_agent.suppress_replace_warning: "true"}` | Returns 200; subsequent GET shows `value = "true"` for that key; a `UserPreference` row materializes in DB. |
| 2.3.2 | `PATCH /api/me/preferences` with unknown key (e.g. `"made.up.key": "true"`) | Returns 4xx with structured error citing the unknown key; **no UserPreference rows written** (transactional). Verify by checking DB. |
| 2.3.3 | `PATCH /api/me/preferences` with type-mismatch value (e.g. `notifications.ai_agent.suppress_replace_warning: "abc"`) | Returns 4xx with structured error citing the type mismatch; no rows written. |
| 2.3.4 | `PATCH /api/me/preferences` with batch of one valid + one invalid key | Returns 4xx; structured error for the invalid key; **valid key NOT written** (transactional — no partial application). |

### §2.4 — Reset API (AC-12)

| Step | Action | Expected |
|------|--------|----------|
| 2.4.1 | After §2.3.1 (override exists), call `DELETE /api/me/preferences/notifications.ai_agent.suppress_replace_warning` | Returns 200/204; UserPreference row removed; subsequent GET returns `value = "false"` (back to default). |

### §2.5 — Notifications UI section (AC-13, AC-14)

| Step | Action | Expected |
|------|--------|----------|
| 2.5.1 | Open the Preferences UI | New "Notifications" section visible alongside Theme/Account. |
| 2.5.2 | Inspect the section's content | AI panel suppress-warning toggle present, with the `displayName` and `description` from the catalogue. |
| 2.5.3 | Toggle the preference ON | Optimistic UI flip; PATCH dispatched; toast confirms (or no toast on success — UX call); refresh page → toggle stays ON. |
| 2.5.4 | Toggle OFF | Same behavior in reverse. |
| 2.5.5 | Simulate API failure (e.g. throttle network or stop backend mid-toggle) | Optimistic state rolls back; error toast displayed. |

### §2.6 — Future-extensibility verification (AC-15)

| Step | Action | Expected |
|------|--------|----------|
| 2.6.1 | Inspect the demo preference key (per AC-15, e.g. `notifications.ai_agent.show_compile_summary`) — confirm Dev seeded it | Key exists in `ref.UserPreferenceKey` with Boolean type. |
| 2.6.2 | Open the Notifications section in the Preferences UI | A second toggle for the demo preference auto-appears, **with no frontend code change**. Verifies the `SettingType`-dispatch architecture genuinely scales. |
| 2.6.3 | Toggle the demo preference and verify read/write works | Same behavior as AC-13 — proves the surface is generic, not bespoke for the AI panel preference. |

### §2.7 — Architecture documentation (AC-16)

| Step | Action | Expected |
|------|--------|----------|
| 2.7.1 | Open `docs/USER-PREFERENCES-ARCHITECTURE.md` | Document exists; covers schema diagram, AppSetting comparison, 3-step recipe for adding a preference, default-value fallback semantics, migration policy. Quality bar: an engineer who has never touched the codebase could add a new preference using only this doc. |

---

## §3 — AI Agent panel polish (Round 2 focus)

After Round 1 is green, verify the polish ACs that consume the foundation.

### §3.1 — Last prompt persistence (AC-1)

| Step | Action | Expected |
|------|--------|----------|
| 3.1.1 | Open Form Builder on a form with no prior prompts; submit prompt "Create an RSVP form" via AI Agent | Generation runs; canvas updates. |
| 3.1.2 | Reload the page (F5) | Prompt textarea pre-populated with "Create an RSVP form". **No reliance on localStorage** — verify by clearing browser localStorage between submit and reload, prompt should still restore. |
| 3.1.3 | Open the same form in a different browser (or incognito after re-login) | Prompt textarea still shows "Create an RSVP form". Confirms cross-browser DB-backed persistence. |
| 3.1.4 | Switch to a different form that has its own last prompt | That form's prompt restored (not the previous form's). |
| 3.1.5 | Switch to a brand-new form with no prior prompt | Textarea is empty. |

### §3.2 — Replace-form warning (AC-2, AC-3, AC-4)

| Step | Action | Expected |
|------|--------|----------|
| 3.2.1 | On a non-empty canvas (≥1 component), with `notifications.ai_agent.suppress_replace_warning = "false"` (default), click Generate | Modal appears with words "replace" and "Undo"; Confirm/Cancel buttons. |
| 3.2.2 | Click Cancel | Generation aborted; canvas unchanged. |
| 3.2.3 | Click Generate again, this time check "don't show again" + Confirm | Generation proceeds; PATCH /api/me/preferences fires writing the suppression preference. |
| 3.2.4 | Click Generate again with non-empty canvas | **No modal**; generation proceeds immediately. |
| 3.2.5 | **Logout, log back in, return to Form Builder** | Suppression survives; clicking Generate over non-empty canvas still skips modal. **AC-3 server-side persistence verification.** |
| 3.2.6 | Open Preferences UI → Notifications section → toggle the AI panel suppress-warning OFF | Returns to default state. |
| 3.2.7 | Click Generate over non-empty canvas | Modal appears again. Confirms toggle restores warning behavior. |
| 3.2.8 | On an **empty** canvas (0 components), click Generate | **No modal** regardless of preference state. AC-4 verification. |

### §3.3 — Outbound transport selector hidden (AC-5)

| Step | Action | Expected |
|------|--------|----------|
| 3.3.1 | Open AI Agent panel | The "OpenAI outbound transport" `<select>` is no longer rendered. |
| 3.3.2 | Submit a prompt and observe the trace summary line | "OpenAI transport (resolved): &lt;mode&gt;" still shows the server-side resolved transport. |

### §3.4 — Retry input hidden + AppSetting-backed default (AC-6)

| Step | Action | Expected |
|------|--------|----------|
| 3.4.1 | Open AI Agent panel | The "System correction attempts" `<input type="number">` is no longer rendered. |
| 3.4.2 | Inspect the request payload (browser DevTools Network tab) when submitting a prompt | `maxSystemCorrectionAttempts` field is absent from the request body. |
| 3.4.3 | Default-value verification: with AppSetting `form_ai.default_retries = "2"`, force a generation that requires retries (e.g. malformed initial response prompt) | Backend logs/trace show 2 retry attempts. |
| 3.4.4 | **Settings-driven verification**: update AppSetting row to `"3"`, restart backend (or call manual reload endpoint), repeat 3.4.3 | Backend now uses 3 retries. **Proves the value is genuinely sourced from the table, not hardcoded.** Restore to `"2"` after test. |

### §3.5 — Silent autoload on validation issues (AC-7, AC-8)

| Step | Action | Expected |
|------|--------|----------|
| 3.5.1 | Submit a prompt designed to surface soft validation issues (use a known-marginal prompt or a fixture) | Generation completes; canvas updates immediately. **No "pending invalid draft" UI / warning banner / decision dialog.** |
| 3.5.2 | Inspect trace summary | Validation counts still shown (e.g. "validation: 2 soft warnings"). |
| 3.5.3 | Force a hard failure (e.g. transport error, empty response simulator) | Existing user-visible failure message still displayed. AC-8 verification — silent autoload only applies to "definition returned". |

---

## §4 — Catch-all + regression (Round 3 focus)

### §4.1 — Regression suite (AC-18)

| Step | Action | Expected |
|------|--------|----------|
| 4.1.1 | Run full backend pytest | Baseline preserved (705 passed / 26 skipped from end-of-6.3.1) or improved (new tests added by 6.4 work) |
| 4.1.2 | Run full frontend test:unit | Baseline preserved (272 passed) or improved |
| 4.1.3 | Smoke-test Story 6.3.1 functionality (run a benchmark prompt, observe deterministic compile + canvas output) | No regression — generation path still works |
| 4.1.4 | Smoke-test other touched surfaces (Theme settings, Account settings, login/logout) | No regression — existing User pref columns and flows still functional |

### §4.2 — Mandatory closeout artifacts (AC-16, AC-17, AC-19, DoD)

| Step | Action | Expected |
|------|--------|----------|
| 4.2.1 | `docs/USER-PREFERENCES-ARCHITECTURE.md` exists and is reviewed | AC-16 confirmed |
| 4.2.2 | Migration count check (workflow guide row 4 + AC-17): `git diff --stat master -- backend/migrations/versions/` | Matches AC-17 exactly: 6 expected, ≤4 files if collapsed. **Treat any other count as scope-creep — block closeout until investigated.** |
| 4.2.3 | `STORY-6.4-CLOSEOUT-REPORT.md` exists per the new PR #65 mandatory rule (criteria (a) + (b) trigger) | Report covers AC matrix, migration list with rationale, §2.6.3 design rationale preserved, what this unlocks for Story 6.5+, hygiene, decision/sign-off |
| 4.2.4 | `STORY-6.4-GATE-EVIDENCE.md` exists with all the §1 gate evidence and AC-by-AC matrix | All ACs mapped to evidence (test name, screenshot, trace excerpt, etc.) |

### §4.3 — Date-stamp + worktree hygiene (workflow guide rows 7-8)

| Step | Action | Expected |
|------|--------|----------|
| 4.3.1 | After PR merge, check `gh pr view <N> --json mergedAt,state,mergeCommit` | `state = "MERGED"`, mergedAt recorded |
| 4.3.2 | Compare merge date to `Completed:` field in `story-6.4.md` and merge date in `EPIC-6-STATUS.md` | All three match (UTC) |
| 4.3.3 | `git worktree remove "<merged story worktree path>"` | Worktree retired cleanly; no stale IDE windows pointing at deleted branch |

---

## Sign-off

UAT considered PASS when:

- §1 automated gates green
- §2 (Round 1) all rows pass — foundation works in isolation
- §3 (Round 2) all rows pass — polish layer works against foundation
- §4 (Round 3) all rows pass — regression clean, mandatory artifacts exist, hygiene done

Any FAIL in §2 or §3 should trigger a single-variable fix + re-test the affected sub-section only (per Multi-Round UAT Protocol). Avoid making multiple unrelated fixes in a single iteration.

**Anthony's sign-off goes here:**

```
Round 1 (foundation): __________________  Date: __________
Round 2 (polish): _____________________  Date: __________
Round 3 (regression + hygiene): _______  Date: __________
Final UAT PASS: ______________________  Date: __________
```
