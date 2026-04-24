# Story 6.4 — Gate Evidence

**Story:** 6.4 — AI Agent Panel Production Polish + User Preferences Architecture Foundation  
**Date:** 2026-04-24  
**Branch:** `story/epic6-6.4-ai-panel-polish-and-prefs-foundation`

---

## §1 — Automated gates

### 1.1 Backend pytest

```
python -m pytest tests/test_user_preferences.py -v

41 passed, 0 failed, 116 warnings in 0.09s
```

New tests cover:
- `TestValidateValueForType` — boolean, integer, decimal, JSON, string, unknown type fallback (12 cases)
- `TestPatchUserPreferences` — unknown key, inactive key, non-editable key, type mismatch, boolean invalid, batch with one bad key (6 cases)
- `TestDefaultValueFallback` — GET with no user rows returns defaults (1 case)
- `TestGetDefaultRetries` — fallback when no session, fallback when setting not found, reads from DB and caches, cache prevents second DB call, invalidate forces reload, clamps 0–10 (6 cases)
- `TestResetUserPreference` — unknown key returns false, existing row soft-deletes (2 cases)

### 1.2 Frontend lint

```
npm run lint
# (no output — 0 errors, 0 warnings, --max-warnings 0)
```

### 1.3 Frontend unit tests

```
npm run test:unit -- --watch=false

Test Files  28 passed (28)
      Tests  283 passed (283)
   Duration  10.71s
```

New tests cover `NotificationsSettingsPopup`:
- Renders loading state, then preference toggles from API response
- Dynamic dispatch: boolean → toggle, integer → number input, string → text input
- Optimistic state flip on toggle change
- PATCH dispatched with correct key/value
- Error rollback when PATCH fails

### 1.4 Migration count

```
git diff --stat master -- backend/migrations/versions/

 backend/migrations/versions/058_story_64_user_pref_tables.py          | new
 backend/migrations/versions/059_story_64_seed_user_pref_categories.py | new
 backend/migrations/versions/060_story_64_seed_user_pref_keys.py       | new
 backend/migrations/versions/061_story_64_seed_form_ai_default_retries.py | new
```

4 files — within AC-17 bound (≤4). No scope creep.

---

## §2 — AC-by-AC evidence matrix

| AC | Statement | Evidence |
|----|-----------|----------|
| AC-1 | Last AI prompt persists across sessions | `AIAgentPanel.tsx` `useEffect` + `setAiAgentSettings`/`saveDraft`; UAT §3.1 PASS |
| AC-2 | Replace-form warning shown on non-empty canvas | `handleGenerate` → `showReplaceWarning`; UAT §3.2.1 PASS |
| AC-3 | "Don't show again" persisted via PATCH | Modal `dontShowAgain` state + `patchPreferences` call; UAT §3.2.3–3.2.5 PASS |
| AC-4 | Warning suppressed on subsequent generations | `suppressWarning` loaded from GET on mount; UAT §3.2.4 PASS |
| AC-5 | Transport selector hidden; backend receives `auto` | Selector removed from JSX; `openaiTransport` locked; UAT §3.3.1 PASS |
| AC-6 | Retry input hidden; backend reads from AppSetting | Input removed; `_get_default_retries` in `form_ai/service.py`; UAT §3.4.1–3.4.2 PASS |
| AC-7 | Soft-validation drafts auto-applied | `executeGenerate` calls `applyValidatedDefinition` on `draftHasValidationIssues` path; UAT §3.5.1 PASS |
| AC-8 | Hard failures still surface error message | `setMessage` on `response.definitionJSON === null`; UAT §3.5.3 PASS |
| AC-9 | `ref.UserPreferenceCategory` created | `058_story_64_user_pref_tables.py`; UAT §2.1 PASS |
| AC-10 | `ref.UserPreferenceKey` created; FK to `ref.SettingType` | `058_story_64_user_pref_tables.py`; UAT §2.1.3 PASS |
| AC-11 | `dbo.UserPreference` created with soft-delete | `058_story_64_user_pref_tables.py`; UAT §2.1 PASS |
| AC-12 | GET returns categories + entries with default fallback | `preferences/service.py` `get_user_preferences`; `TestDefaultValueFallback`; UAT §2.2 PASS |
| AC-13 | PATCH validates atomically before writing | `patch_user_preferences` full validation pass first; `TestPatchUserPreferences::test_multiple_keys_one_bad_no_writes`; UAT §2.3.4 PASS |
| AC-14 | DELETE soft-deletes; GET returns default | `reset_user_preference` sets `IsActive=0`; `TestResetUserPreference`; UAT §2.4 PASS |
| AC-15 | Notifications popup dynamic; second demo key auto-renders | `NotificationsSettingsPopup` `settingType` dispatch; `060` seeds `show_compile_summary`; UAT §2.6.2 PASS |
| AC-16 | Architecture doc at `docs/USER-PREFERENCES-ARCHITECTURE.md` | File present; reviewed in UAT §2.7.1 |
| AC-17 | Migration set ≤ 4 files | 4 files confirmed above |
| AC-18 | `config.AppSetting form_ai.default_retries` seeded = "2" | `061_story_64_seed_form_ai_default_retries.py`; UAT §3.4.3 PASS |
| AC-19 | Existing User preference columns unchanged | `User` model — only `user_preferences` back-ref added; UAT §2.1.5 PASS |

---

## §3 — Key files delivered

| File | Type | Purpose |
|------|------|---------|
| `backend/migrations/versions/058_story_64_user_pref_tables.py` | Migration | DDL: 3 new tables |
| `backend/migrations/versions/059_story_64_seed_user_pref_categories.py` | Migration | Seed: 4 categories |
| `backend/migrations/versions/060_story_64_seed_user_pref_keys.py` | Migration | Seed: 2 preference keys |
| `backend/migrations/versions/061_story_64_seed_form_ai_default_retries.py` | Migration | Seed: form_ai.default_retries AppSetting |
| `backend/models/ref/user_preference_category.py` | Model | SQLAlchemy ORM |
| `backend/models/ref/user_preference_key.py` | Model | SQLAlchemy ORM |
| `backend/models/user_preference.py` | Model | SQLAlchemy ORM |
| `backend/modules/preferences/router.py` | Router | GET/PATCH/DELETE /api/me/preferences |
| `backend/modules/preferences/service.py` | Service | Validation + read/write/reset logic |
| `backend/modules/preferences/schemas.py` | Schemas | Pydantic request/response models |
| `backend/modules/form_ai/service.py` | Modified | `_get_default_retries` startup-cached reader |
| `backend/tests/test_user_preferences.py` | Tests | 41 unit tests |
| `frontend/src/features/preferences/components/NotificationsSettingsPopup.tsx` | Component | Dynamic preferences UI |
| `frontend/src/features/preferences/api/preferencesApi.ts` | API client | getPreferences / patchPreferences / resetPreference |
| `frontend/src/features/preferences/types/preferences.types.ts` | Types | TypeScript interfaces |
| `frontend/src/features/preferences/__tests__/NotificationsSettingsPopup.test.tsx` | Tests | Frontend unit tests |
| `frontend/src/features/builder/components/ai/AIAgentPanel.tsx` | Modified | §B polish: AC-1–8 |
| `docs/USER-PREFERENCES-ARCHITECTURE.md` | Doc | AC-16 architecture reference |
