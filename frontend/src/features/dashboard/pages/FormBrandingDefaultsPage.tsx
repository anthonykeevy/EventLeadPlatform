/**
 * Form Branding Defaults Page - Story 5.2 T04
 * Company Settings → Form Branding Defaults
 * Controls matching Global Properties Panel + Toolbox preview + Audit trail
 */

import { useState, useEffect, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Save, History } from 'lucide-react'
import {
  getCompanyFormDefaults,
  putCompanyFormDefaults,
  getCompanyFormDefaultsHistory,
  type FormDefaultsPayload,
  type FormDefaultsVersionEntry
} from '../api/formDefaultsApi'
import { useToastNotifications } from '../../ux'

export function FormBrandingDefaultsPage() {
  const { companyId } = useParams<{ companyId: string }>()
  const navigate = useNavigate()
  const toast = useToastNotifications()

  const [defaults, setDefaults] = useState<FormDefaultsPayload | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [history, setHistory] = useState<FormDefaultsVersionEntry[]>([])
  const [showHistory, setShowHistory] = useState(false)

  const id = companyId ? parseInt(companyId, 10) : NaN

  const loadDefaults = useCallback(async () => {
    if (isNaN(id)) return
    setIsLoading(true)
    try {
      const res = await getCompanyFormDefaults(id)
      setDefaults(res.defaults ?? {})
    } catch (err) {
      toast.error('Failed to load form defaults', 'Error')
      setDefaults({})
    } finally {
      setIsLoading(false)
    }
  }, [id, toast])

  const loadHistory = useCallback(async () => {
    if (isNaN(id)) return
    try {
      const res = await getCompanyFormDefaultsHistory(id)
      setHistory(res.items ?? [])
    } catch {
      setHistory([])
    }
  }, [id])

  useEffect(() => {
    loadDefaults()
  }, [loadDefaults])

  useEffect(() => {
    if (showHistory) loadHistory()
  }, [showHistory, loadHistory])

  const handleSave = async () => {
    if (isNaN(id) || !defaults) return
    setIsSaving(true)
    try {
      await putCompanyFormDefaults(id, defaults, 'Updated from Company Settings')
      toast.success('Form branding defaults saved', 'Success')
      loadDefaults()
      if (showHistory) loadHistory()
    } catch (err) {
      toast.error('Failed to save form defaults', 'Error')
    } finally {
      setIsSaving(false)
    }
  }

  const updateTheme = (key: string, value: string) => {
    setDefaults((prev) => ({
      ...prev,
      theme: {
        ...(prev?.theme ?? {}),
        [key]: value
      }
    }))
  }

  const updateGlobalStyle = (key: string, value: string | number) => {
    setDefaults((prev) => ({
      ...prev,
      globalStyles: {
        ...(prev?.globalStyles ?? {}),
        [key]: value
      }
    }))
  }

  const updateCanvas = (key: string, value: number) => {
    setDefaults((prev) => ({
      ...prev,
      canvasSettings: {
        ...(prev?.canvasSettings ?? {}),
        [key]: value
      }
    }))
  }

  const theme = defaults?.theme ?? {}
  const gs = (defaults?.globalStyles ?? {}) as Record<string, unknown>
  const canvas = defaults?.canvasSettings ?? {}
  const primaryColor = (theme.primaryColor as string) ?? '#0055FF'
  const backgroundColor = (theme.backgroundColor as string) ?? '#FFFFFF'
  const fontFamily = (theme.fontFamily as string) ?? 'Inter'

  if (isNaN(id)) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <p className="text-red-600">Invalid company ID</p>
        <button onClick={() => navigate('/dashboard')} className="mt-4 text-teal-600 hover:underline">
          Back to Dashboard
        </button>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="flex items-center gap-4 mb-6">
        <button
          onClick={() => navigate('/dashboard')}
          className="p-2 rounded hover:bg-gray-100 text-gray-600"
          aria-label="Back to Dashboard"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Form Branding Defaults</h1>
          <p className="text-sm text-gray-500">Configure default styling for all forms in this company</p>
        </div>
      </div>

      {isLoading ? (
        <div className="bg-white rounded-lg border p-8 text-center text-gray-500">Loading...</div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left: Controls */}
          <div className="space-y-6">
            {/* Theme */}
            <section className="bg-white rounded-lg border p-4">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Theme</h2>
              <div className="space-y-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Primary Color</label>
                  <div className="flex items-center gap-2">
                    <input
                      type="color"
                      value={primaryColor}
                      onChange={(e) => updateTheme('primaryColor', e.target.value)}
                      className="w-10 h-10 rounded border cursor-pointer"
                    />
                    <input
                      type="text"
                      value={primaryColor}
                      onChange={(e) => updateTheme('primaryColor', e.target.value)}
                      className="flex-1 px-2 py-1.5 border rounded text-sm"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Background Color</label>
                  <div className="flex items-center gap-2">
                    <input
                      type="color"
                      value={backgroundColor}
                      onChange={(e) => updateTheme('backgroundColor', e.target.value)}
                      className="w-10 h-10 rounded border cursor-pointer"
                    />
                    <input
                      type="text"
                      value={backgroundColor}
                      onChange={(e) => updateTheme('backgroundColor', e.target.value)}
                      className="flex-1 px-2 py-1.5 border rounded text-sm"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Font Family</label>
                  <select
                    value={fontFamily}
                    onChange={(e) => updateTheme('fontFamily', e.target.value)}
                    className="w-full px-2 py-1.5 border rounded text-sm"
                  >
                    <option value="Inter">Inter</option>
                    <option value="Roboto">Roboto</option>
                    <option value="Open Sans">Open Sans</option>
                    <option value="Lato">Lato</option>
                    <option value="Arial">Arial</option>
                  </select>
                </div>
              </div>
            </section>

            {/* Global Styles (Typography) */}
            <section className="bg-white rounded-lg border p-4">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Typography</h2>
              <div className="space-y-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Base Font Family</label>
                  <input
                    type="text"
                    value={(gs.fontFamily as string) ?? 'Inter'}
                    onChange={(e) => updateGlobalStyle('fontFamily', e.target.value)}
                    className="w-full px-2 py-1.5 border rounded text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Base Font Size (px)</label>
                  <input
                    type="number"
                    value={(gs.fontSize as number) ?? 14}
                    onChange={(e) => updateGlobalStyle('fontSize', parseInt(e.target.value, 10) || 14)}
                    min={10}
                    max={24}
                    className="w-full px-2 py-1.5 border rounded text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Label Font Family</label>
                  <input
                    type="text"
                    value={(gs.labelFontFamily as string) ?? 'Inter'}
                    onChange={(e) => updateGlobalStyle('labelFontFamily', e.target.value)}
                    className="w-full px-2 py-1.5 border rounded text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Label Color</label>
                  <input
                    type="text"
                    value={(gs.labelColor as string) ?? '#374151'}
                    onChange={(e) => updateGlobalStyle('labelColor', e.target.value)}
                    className="w-full px-2 py-1.5 border rounded text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Input Text Color</label>
                  <input
                    type="text"
                    value={(gs.textColor as string) ?? '#111827'}
                    onChange={(e) => updateGlobalStyle('textColor', e.target.value)}
                    className="w-full px-2 py-1.5 border rounded text-sm"
                  />
                </div>
              </div>
            </section>

            {/* Canvas Settings */}
            <section className="bg-white rounded-lg border p-4">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Canvas Settings</h2>
              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Width</label>
                  <input
                    type="number"
                    value={(canvas.width as number) ?? 1920}
                    onChange={(e) => updateCanvas('width', parseInt(e.target.value, 10) || 1920)}
                    min={800}
                    max={3840}
                    className="w-full px-2 py-1.5 border rounded text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Height</label>
                  <input
                    type="number"
                    value={(canvas.height as number) ?? 980}
                    onChange={(e) => updateCanvas('height', parseInt(e.target.value, 10) || 980)}
                    min={400}
                    max={2160}
                    className="w-full px-2 py-1.5 border rounded text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Grid Size</label>
                  <input
                    type="number"
                    value={(canvas.gridSize as number) ?? 8}
                    onChange={(e) => updateCanvas('gridSize', parseInt(e.target.value, 10) || 8)}
                    min={4}
                    max={32}
                    className="w-full px-2 py-1.5 border rounded text-sm"
                  />
                </div>
              </div>
            </section>

            <div className="flex gap-3">
              <button
                onClick={handleSave}
                disabled={isSaving}
                className="inline-flex items-center gap-2 px-4 py-2 bg-teal-600 text-white rounded-md hover:bg-teal-700 disabled:opacity-50"
              >
                <Save className="w-4 h-4" />
                {isSaving ? 'Saving...' : 'Save'}
              </button>
              <button
                onClick={() => setShowHistory(!showHistory)}
                className="inline-flex items-center gap-2 px-4 py-2 border rounded-md hover:bg-gray-50"
              >
                <History className="w-4 h-4" />
                {showHistory ? 'Hide' : 'Show'} History
              </button>
            </div>
          </div>

          {/* Right: Toolbox Preview */}
          <div className="space-y-6">
            <section className="bg-white rounded-lg border p-4">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Component Preview</h2>
              <p className="text-sm text-gray-500 mb-4">Live preview of components with current defaults</p>
              <div
                className="rounded-lg border p-6 space-y-4"
                style={{
                  backgroundColor: backgroundColor as string,
                  fontFamily: (gs.fontFamily as string) ?? 'Inter'
                }}
              >
                {/* Text field preview */}
                <div>
                  <label
                    className="block text-sm mb-1"
                    style={{
                      fontFamily: (gs.labelFontFamily as string) ?? 'Inter',
                      fontSize: `${(gs.labelFontSize as number) ?? (gs.fontSize as number) ?? 14}px`,
                      color: (gs.labelColor as string) ?? '#374151'
                    }}
                  >
                    Full Name
                  </label>
                  <input
                    type="text"
                    placeholder="Enter your name"
                    readOnly
                    className="w-full px-3 py-2 border rounded"
                    style={{
                      fontFamily: (gs.fontFamily as string) ?? 'Inter',
                      fontSize: `${(gs.fontSize as number) ?? 14}px`,
                      color: (gs.textColor as string) ?? '#111827',
                      borderColor: (gs.textBorderColor as string) ?? '#d1d5db'
                    }}
                  />
                </div>
                {/* Email field preview */}
                <div>
                  <label
                    className="block text-sm mb-1"
                    style={{
                      fontFamily: (gs.labelFontFamily as string) ?? 'Inter',
                      fontSize: `${(gs.labelFontSize as number) ?? (gs.fontSize as number) ?? 14}px`,
                      color: (gs.labelColor as string) ?? '#374151'
                    }}
                  >
                    Email
                  </label>
                  <input
                    type="email"
                    placeholder="you@example.com"
                    readOnly
                    className="w-full px-3 py-2 border rounded"
                    style={{
                      fontFamily: (gs.fontFamily as string) ?? 'Inter',
                      fontSize: `${(gs.fontSize as number) ?? 14}px`,
                      color: (gs.textColor as string) ?? '#111827',
                      borderColor: (gs.textBorderColor as string) ?? '#d1d5db'
                    }}
                  />
                </div>
                {/* Primary color sample */}
                <button
                  type="button"
                  disabled
                  className="px-4 py-2 rounded text-white text-sm font-medium"
                  style={{ backgroundColor: primaryColor }}
                >
                  Submit (primary color)
                </button>
              </div>
            </section>

            {/* Version History */}
            {showHistory && (
              <section className="bg-white rounded-lg border p-4">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Change History</h2>
                <div className="space-y-2 max-h-64 overflow-y-auto">
                  {history.length === 0 ? (
                    <p className="text-sm text-gray-500">No changes yet</p>
                  ) : (
                    history.map((entry) => (
                      <div
                        key={entry.versionNumber}
                        className="flex justify-between items-start gap-2 p-2 rounded bg-gray-50 text-sm"
                      >
                        <div>
                          <span className="font-medium">Version {entry.versionNumber}</span>
                          {entry.changeSummary && (
                            <span className="text-gray-600 ml-2">— {entry.changeSummary}</span>
                          )}
                          <div className="text-xs text-gray-500 mt-0.5">
                            {entry.createdDate ? new Date(entry.createdDate).toLocaleString() : ''}
                            {entry.createdBy && ` • User ID ${entry.createdBy}`}
                          </div>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </section>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
