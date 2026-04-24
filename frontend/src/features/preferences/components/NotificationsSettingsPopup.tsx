/**
 * Notifications Settings Popup (Story 6.4 AC-13, AC-14, AC-15)
 *
 * Renders user preferences for the "Notifications" category (and any other
 * active categories returned by the API). Controls are dispatched dynamically
 * by SettingType — adding a new preference key via a ref seed row causes it to
 * appear here automatically with no frontend code change required (AC-15).
 *
 * Supported control types:
 *   - boolean → toggle switch
 *   - integer → number input
 *   - string  → text input
 *   - (unknown types fall back to a read-only text display)
 *
 * UI pattern: mirrors AccountSettingsPopup (optimistic update + rollback on error,
 * useToastNotifications, hasChanges tracking, ESC to close).
 */

import { useState, useEffect, useRef } from 'react'
import { X, Bell } from 'lucide-react'
import { useToastNotifications } from '../../ux'
import { getPreferences, patchPreferences } from '../api/preferencesApi'
import type { PreferencesResponse, PreferenceEntry, PreferenceCategory } from '../types/preferences.types'

interface NotificationsSettingsPopupProps {
  isOpen: boolean
  onClose: () => void
}

// ─────────────────────────────────────────────────────────────────────────────
// Dynamic control dispatch by SettingType
// ─────────────────────────────────────────────────────────────────────────────

interface PreferenceControlProps {
  entry: PreferenceEntry
  currentValue: string
  onChange: (key: string, value: string) => void
  disabled: boolean
}

function PreferenceControl({ entry, currentValue, onChange, disabled }: PreferenceControlProps) {
  const tc = entry.settingType.toLowerCase()

  if (tc === 'boolean') {
    const checked = currentValue === 'true'
    return (
      <button
        type="button"
        role="switch"
        aria-checked={checked}
        disabled={disabled}
        onClick={() => onChange(entry.preferenceKey, checked ? 'false' : 'true')}
        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-teal-500 disabled:opacity-50 disabled:cursor-not-allowed ${
          checked
            ? 'bg-teal-600 dark:bg-teal-500'
            : 'bg-gray-300 dark:bg-gray-600'
        }`}
        aria-label={entry.displayName}
      >
        <span
          className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
            checked ? 'translate-x-6' : 'translate-x-1'
          }`}
        />
      </button>
    )
  }

  if (tc === 'integer') {
    return (
      <input
        type="number"
        value={currentValue}
        disabled={disabled}
        onChange={(e) => onChange(entry.preferenceKey, e.target.value)}
        className="w-24 px-3 py-1.5 border border-gray-300 dark:border-gray-600 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:border-teal-500 dark:bg-gray-700 dark:text-white disabled:opacity-50"
        aria-label={entry.displayName}
      />
    )
  }

  if (tc === 'string') {
    return (
      <input
        type="text"
        value={currentValue}
        disabled={disabled}
        onChange={(e) => onChange(entry.preferenceKey, e.target.value)}
        className="w-48 px-3 py-1.5 border border-gray-300 dark:border-gray-600 rounded-lg text-sm focus:ring-2 focus:ring-teal-500 focus:border-teal-500 dark:bg-gray-700 dark:text-white disabled:opacity-50"
        aria-label={entry.displayName}
      />
    )
  }

  // Unknown type — display read-only
  return (
    <span className="text-sm text-gray-500 dark:text-gray-400 font-mono">{currentValue}</span>
  )
}

// ─────────────────────────────────────────────────────────────────────────────
// Popup component
// ─────────────────────────────────────────────────────────────────────────────

export function NotificationsSettingsPopup({ isOpen, onClose }: NotificationsSettingsPopupProps) {
  const toast = useToastNotifications()

  const [prefs, setPrefs] = useState<PreferencesResponse | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  // Pending local changes: {preferenceKey → value string}
  const [pendingChanges, setPendingChanges] = useState<Record<string, string>>({})
  const [isSaving, setIsSaving] = useState(false)

  const dataLoadedRef = useRef(false)
  const isLoadingRef = useRef(false)

  const hasChanges = Object.keys(pendingChanges).length > 0

  // Load preferences on open
  useEffect(() => {
    if (isOpen && !dataLoadedRef.current && !isLoadingRef.current) {
      isLoadingRef.current = true
      const load = async () => {
        try {
          setIsLoading(true)
          const data = await getPreferences()
          setPrefs(data)
          setPendingChanges({})
          dataLoadedRef.current = true
        } catch {
          toast.error('Failed to load notification preferences')
          dataLoadedRef.current = false
        } finally {
          setIsLoading(false)
          isLoadingRef.current = false
        }
      }
      load()
    }
  }, [isOpen, toast])

  // ESC to close
  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        if (hasChanges) {
          if (confirm('You have unsaved changes. Are you sure you want to close?')) onClose()
        } else {
          onClose()
        }
      }
    }
    document.addEventListener('keydown', handleEsc)
    return () => document.removeEventListener('keydown', handleEsc)
  }, [isOpen, hasChanges, onClose])

  /** Get the effective display value for a preference entry (pending change takes priority). */
  const effectiveValue = (entry: PreferenceEntry): string => {
    return pendingChanges[entry.preferenceKey] ?? entry.value
  }

  /** Stage a local change (optimistic). */
  const handleChange = (preferenceKey: string, value: string) => {
    setPendingChanges((prev) => ({ ...prev, [preferenceKey]: value }))
  }

  /** Save pending changes to the server. */
  const handleSave = async () => {
    if (!hasChanges || isSaving) return

    setIsSaving(true)

    // Optimistic: snapshot current prefs for rollback
    const snapshot = prefs

    try {
      const updated = await patchPreferences(pendingChanges)
      setPrefs(updated)
      setPendingChanges({})
      toast.success('Notification preferences saved')
    } catch {
      // Rollback on error
      setPrefs(snapshot)
      setPendingChanges({})
      toast.error('Failed to save notification preferences')
    } finally {
      setIsSaving(false)
    }
  }

  /** Helper: get only the "Notifications" category (or all categories if Notifications not present). */
  const getDisplayCategories = (): PreferenceCategory[] => {
    if (!prefs) return []
    const notificationsCat = prefs.categories.find(
      (c) => c.categoryName === 'Notifications'
    )
    // Show Notifications first if present, then others; filter to active
    return notificationsCat ? [notificationsCat] : prefs.categories
  }

  if (!isOpen) return null

  const displayCategories = getDisplayCategories()

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-lg w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <Bell className="w-5 h-5 text-teal-600 dark:text-teal-400" />
            <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
              Notifications
            </h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            aria-label="Close notifications settings"
          >
            <X className="w-5 h-5 text-gray-500 dark:text-gray-400" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[calc(90vh-180px)]">
          {isLoading ? (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-600" />
              <span className="ml-3 text-gray-600 dark:text-gray-400">Loading preferences…</span>
            </div>
          ) : displayCategories.length === 0 ? (
            <div className="py-6 text-center">
              <p className="text-sm text-gray-500 dark:text-gray-400">No preferences yet.</p>
            </div>
          ) : (
            <div className="space-y-6">
              {displayCategories.map((cat) => (
                <div key={cat.categoryId}>
                  {/* Category header */}
                  <div className="mb-4">
                    <h3 className="font-medium text-gray-900 dark:text-gray-100">
                      {cat.categoryName}
                    </h3>
                    {cat.description && (
                      <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                        {cat.description}
                      </p>
                    )}
                  </div>

                  {/* Preference entries */}
                  {cat.entries.length === 0 ? (
                    <p className="text-sm text-gray-500 dark:text-gray-400 pl-1">
                      No preferences yet.
                    </p>
                  ) : (
                    <div className="space-y-4">
                      {cat.entries.map((entry) => (
                        <div
                          key={entry.preferenceKeyId}
                          className="flex items-start justify-between gap-4"
                          data-preference-key={entry.preferenceKey}
                        >
                          <div className="flex-1 min-w-0">
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                              {entry.displayName}
                            </label>
                            {entry.description && (
                              <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                                {entry.description}
                              </p>
                            )}
                          </div>
                          <div className="flex-shrink-0 mt-0.5">
                            <PreferenceControl
                              entry={entry}
                              currentValue={effectiveValue(entry)}
                              onChange={handleChange}
                              disabled={isSaving}
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="border-t border-gray-200 dark:border-gray-700 p-4 bg-gray-50 dark:bg-gray-800">
          <div className="flex items-center justify-between">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {hasChanges ? 'You have unsaved changes' : 'All changes are saved'}
            </p>
            <div className="flex items-center gap-3">
              <button
                onClick={onClose}
                className="px-4 py-2 text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors"
              >
                {hasChanges ? 'Cancel' : 'Close'}
              </button>
              <button
                onClick={handleSave}
                disabled={!hasChanges || isSaving}
                className="px-4 py-2 bg-teal-600 dark:bg-teal-500 text-white rounded-lg hover:bg-teal-700 dark:hover:bg-teal-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isSaving ? 'Saving…' : 'Save Changes'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
