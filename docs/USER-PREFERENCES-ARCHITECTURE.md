# User Preferences Architecture

> Story 6.4 — canonical foundation for per-user preference storage in the EventLead Platform.

---

## Overview

The User Preferences system provides a type-safe, per-user key–value store that mirrors the existing `config.AppSetting` pattern used for platform-wide configuration.  It is **not** a replacement for the existing per-user profile columns (`User.ThemePreferenceID`, `LayoutDensityID`, etc.) — those are first-class FK-linked columns that exist for high-frequency joins and remain unchanged.  Instead, this system handles behavioural toggles, notification preferences, and feature-flag-style per-user settings that change rarely and do not need a dedicated FK column.

---

## Database Schema

Three tables are added, all following the platform's standard audit-column pattern.

### `ref.UserPreferenceCategory`

Logical grouping for keys (e.g. *Notifications*, *Theme*, *Account*, *AI Agent*).

| Column | Type | Notes |
|---|---|---|
| `UserPreferenceCategoryID` | `INT IDENTITY` PK | |
| `CategoryCode` | `NVARCHAR(50)` | Unique, e.g. `notifications` |
| `CategoryName` | `NVARCHAR(100)` | Display label |
| `Description` | `NVARCHAR(500)` | Optional |
| `SortOrder` | `INT` | |
| `IsActive` | `BIT` | Soft-disable whole category |
| `CreatedAt`, `UpdatedAt` | `DATETIME2` | Standard audit |

### `ref.UserPreferenceKey`

Metadata for every settable preference — analogous to a row in `config.AppSetting` that defines the *schema* of the setting.

| Column | Type | Notes |
|---|---|---|
| `UserPreferenceKeyID` | `INT IDENTITY` PK | |
| `PreferenceKey` | `NVARCHAR(200)` | Unique dotted key, e.g. `notifications.ai_agent.suppress_replace_warning` |
| `UserPreferenceCategoryID` | `INT` FK → `ref.UserPreferenceCategory` | |
| `SettingTypeID` | `INT` FK → **`ref.SettingType`** | Reuses the platform type system — no parallel type table |
| `DefaultValue` | `NVARCHAR(1000)` | Returned when no user row exists |
| `Description` | `NVARCHAR(500)` | |
| `IsEditable` | `BIT` | Prevents writes to system-managed keys |
| `IsActive` | `BIT` | Soft-disable individual key |
| `SortOrder` | `INT` | |
| `CreatedAt`, `UpdatedAt` | `DATETIME2` | |

### `dbo.UserPreference`

Per-user value overrides.  A row here means "this user has explicitly set this preference".  Absence means "use the key's `DefaultValue`".

| Column | Type | Notes |
|---|---|---|
| `UserPreferenceID` | `INT IDENTITY` PK | |
| `UserID` | `INT` FK → `dbo.[User]` | |
| `UserPreferenceKeyID` | `INT` FK → `ref.UserPreferenceKey` | |
| `PreferenceValue` | `NVARCHAR(1000)` | Stored as a string; validated against `SettingTypeID` on write |
| `IsActive` | `BIT` | Soft-delete; `DELETE` endpoint sets to `0` rather than hard-deleting |
| `CreatedAt`, `UpdatedAt` | `DATETIME2` | |
| `CreatedByUserID`, `UpdatedByUserID` | `INT` | Standard audit |

Unique constraint: `(UserID, UserPreferenceKeyID)` — one value per user per key.

---

## SQLAlchemy Models

| Model | Module |
|---|---|
| `UserPreferenceCategory` | `backend/models/ref/user_preference_category.py` |
| `UserPreferenceKey` | `backend/models/ref/user_preference_key.py` |
| `UserPreference` | `backend/models/user_preference.py` |

Back-references are added to `ref.SettingType` (`user_preference_keys`) and `dbo.User` (`user_preferences`) using `relationship()` with explicit `foreign_keys`.

---

## API Endpoints

All endpoints require an authenticated session.  The authenticated user's ID is inferred from the JWT; no `user_id` is ever accepted in the request body.

### `GET /api/me/preferences`

Returns all active preference keys grouped by category.  For each key, the response includes the stored value (or `DefaultValue` if no user row exists), plus the `SettingType` metadata needed for the frontend to render the appropriate control without hardcoding.

**Response shape (abridged):**
```json
{
  "categories": [
    {
      "categoryCode": "notifications",
      "categoryName": "Notifications",
      "preferences": [
        {
          "preferenceKey": "notifications.ai_agent.suppress_replace_warning",
          "settingType": "boolean",
          "currentValue": "false",
          "defaultValue": "false",
          "description": "Suppress the replace-form confirmation dialog in the AI Agent panel",
          "isEditable": true
        }
      ]
    }
  ]
}
```

### `PATCH /api/me/preferences`

Atomically writes one or more preference values.  All keys are validated first; if any fails validation the entire request is rejected with a `422` listing every error.  No partial writes.

**Request body:**
```json
{ "notifications.ai_agent.suppress_replace_warning": "true" }
```

### `DELETE /api/me/preferences/{preferenceKey}`

Soft-deletes the user's stored value for a single key (sets `IsActive = 0`).  Subsequent `GET` requests return `DefaultValue` for that key.

---

## Type Validation

Values are validated against `ref.SettingType.TypeCode` before write:

| `TypeCode` | Accepted values |
|---|---|
| `boolean` | `"true"` or `"false"` (case-insensitive) |
| `integer` | Parseable as a whole number, no decimal point |
| `decimal` | Parseable as `float` |
| `json` | Valid JSON string |
| `string` | Any non-null value |

---

## Frontend Integration

### Dynamic control dispatch

`NotificationsSettingsPopup.tsx` (and any future preference section) renders controls **dynamically** based on `settingType` returned from the API:

```
settingType === "boolean"  → <Toggle />
settingType === "integer"  → <input type="number" step="1" />
settingType === "string"   → <input type="text" />
```

Adding a new preference requires **only a database seed** — no frontend code changes.

### Barrel exports

All public types and API helpers are re-exported from `frontend/src/features/preferences/index.ts`:

- `NotificationsSettingsPopup`
- `getPreferences`, `patchPreferences`, `resetPreference`
- `PreferenceEntry`, `PreferenceCategory`, `PreferencesResponse`, `PatchPreferencesRequest`

---

## Adding a New Preference — Step-by-step

1. Decide on a `PreferenceKey` using dotted notation: `<category>.<subcategory>.<name>`.
2. Choose or create the `ref.UserPreferenceCategory` row for the category.
3. Add a `ref.UserPreferenceKey` seed row referencing the correct `SettingTypeID` (look up by `TypeCode`) and `DefaultValue`.
4. The `GET /api/me/preferences` endpoint automatically returns the new key in the relevant category section.
5. The frontend renders the correct control without any code change.

---

## What This System Does NOT Replace

- `User.ThemePreferenceID`, `LayoutDensityID`, `FontSizeID`, `PreferredLanguageID`, `CountryID` — These FK columns are first-class, high-frequency joins managed via dedicated reference tables.  They are not stored in `dbo.UserPreference`.
- `config.AppSetting` — Platform-wide defaults.  `form_ai.default_retries` lives here because it is an admin-configurable default, not a per-user override.

---

## Migration Files (Story 6.4)

| File | Purpose |
|---|---|
| `058_story_64_user_pref_tables.py` | DDL: create `ref.UserPreferenceCategory`, `ref.UserPreferenceKey`, `dbo.UserPreference` |
| `059_story_64_seed_user_pref_categories.py` | Seed: 4 initial categories (Notifications, Theme, Account, AI Agent) |
| `060_story_64_seed_user_pref_keys.py` | Seed: 2 initial keys (`suppress_replace_warning`, `show_compile_summary`) |
| `061_story_64_seed_form_ai_default_retries.py` | Seed: `config.AppSetting` row `form_ai.default_retries = "2"` |
