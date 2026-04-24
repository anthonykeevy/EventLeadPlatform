/**
 * Types for the User Preferences architecture (Story 6.4).
 *
 * These types mirror the backend Pydantic schemas in
 * backend/modules/preferences/schemas.py.
 */

/** A single preference key with its effective value for the current user. */
export interface PreferenceEntry {
  preferenceKeyId: number
  preferenceKey: string
  displayName: string
  description: string
  /** TypeCode from ref.SettingType — 'boolean' | 'integer' | 'decimal' | 'json' | 'string' */
  settingType: string
  defaultValue: string
  sortOrder: number
  /** Effective value: user override if set, otherwise defaultValue */
  value: string
  /** True when a UserPreference override row exists for this user × key */
  isOverridden: boolean
}

/** One preference category with its entries. */
export interface PreferenceCategory {
  categoryId: number
  categoryName: string
  description: string
  displayOrder: number
  entries: PreferenceEntry[]
}

/** Full response from GET /api/me/preferences */
export interface PreferencesResponse {
  categories: PreferenceCategory[]
}

/** Request body for PATCH /api/me/preferences */
export interface PatchPreferencesRequest {
  preferences: Record<string, string | boolean | number>
}
