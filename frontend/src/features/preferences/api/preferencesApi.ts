/**
 * Preferences API client (Story 6.4).
 *
 * Wraps GET / PATCH / DELETE /api/me/preferences endpoints.
 */

import { apiClient } from '../../../lib/apiClient'
import type {
  PreferencesResponse,
  PatchPreferencesRequest,
} from '../types/preferences.types'

/** Fetch all user preferences (grouped by category, with default fallback). */
export async function getPreferences(): Promise<PreferencesResponse> {
  const response = await apiClient.get<PreferencesResponse>('/api/me/preferences')
  return response.data
}

/**
 * Partially update user preferences.
 * Values are string-serialised on the wire; the server type-validates against
 * ref.UserPreferenceKey.SettingTypeID.
 *
 * @throws If any key fails validation — no preferences are written.
 */
export async function patchPreferences(
  preferences: Record<string, string>
): Promise<PreferencesResponse> {
  const body: PatchPreferencesRequest = { preferences }
  const response = await apiClient.patch<PreferencesResponse>('/api/me/preferences', body)
  return response.data
}

/**
 * Reset a single preference to its catalogue default.
 * The user's override row is removed; the next GET returns DefaultValue.
 */
export async function resetPreference(preferenceKey: string): Promise<PreferencesResponse> {
  const encoded = encodeURIComponent(preferenceKey)
  const response = await apiClient.delete<PreferencesResponse>(
    `/api/me/preferences/${encoded}`
  )
  return response.data
}
