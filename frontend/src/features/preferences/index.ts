/**
 * Preferences Feature Exports
 * Epic 2 Story 2.3 - User Preferences & Industries Management
 * Story 6.4 - User Preferences Architecture Foundation
 */

export { AccountSettingsPopup } from './components/AccountSettingsPopup'
export { IndustryManager } from './components/IndustryManager'
export { IndustrySearch } from './components/IndustrySearch'
export { NotificationsSettingsPopup } from './components/NotificationsSettingsPopup'
export { getPreferences, patchPreferences, resetPreference } from './api/preferencesApi'
export type {
  PreferenceEntry,
  PreferenceCategory,
  PreferencesResponse,
  PatchPreferencesRequest,
} from './types/preferences.types'

