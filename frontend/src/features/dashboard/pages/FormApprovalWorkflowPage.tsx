/**
 * Form Approval Workflow Page - Story 5.7
 * Company Settings → Form Approval Workflow
 * Test threshold, Require publish approval; help text per PM decisions
 */

import { useState, useEffect } from 'react'
import { Save, HelpCircle } from 'lucide-react'
import {
  getCompanyTestConfig,
  putCompanyTestConfig,
  type CompanyTestConfig,
} from '../../forms/api/formsApi'
import { useToastNotifications } from '../../ux'

export function FormApprovalWorkflowPage() {
  const toast = useToastNotifications()
  const [config, setConfig] = useState<CompanyTestConfig | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)

  useEffect(() => {
    let cancelled = false
    getCompanyTestConfig()
      .then((c) => {
        if (!cancelled) setConfig(c)
      })
      .catch(() => {
        if (!cancelled) {
          toast.error('Failed to load workflow settings', 'Error')
          setConfig({
            testThresholdEnabled: false,
            testThresholdValue: 3,
            requirePublishApproval: false,
          })
        }
      })
      .finally(() => {
        if (!cancelled) setIsLoading(false)
      })
    return () => {
      cancelled = true
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps -- run once on mount; toast in catch is fine
  }, [])

  const handleSave = async () => {
    if (!config) return
    setIsSaving(true)
    try {
      await putCompanyTestConfig(config)
      toast.success('Form approval workflow saved', 'Success')
    } catch (err) {
      toast.error('Failed to save workflow settings', 'Error')
    } finally {
      setIsSaving(false)
    }
  }

  if (isLoading) {
    return <div className="p-8 text-gray-500">Loading...</div>
  }

  if (!config) {
    return <div className="p-8 text-red-600">Failed to load settings</div>
  }

  return (
    <div className="h-full flex flex-col overflow-hidden">
      <div className="flex-shrink-0 px-4 py-3 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Form Approval Workflow</h2>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
          Configure demo test requirements and publish approval for forms. These settings apply to all forms in your company.
        </p>
      </div>

      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {/* Test threshold */}
        <div className="space-y-3">
          <div className="flex items-center gap-2">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={config.testThresholdEnabled}
                onChange={(e) => setConfig((c) => (c ? { ...c, testThresholdEnabled: e.target.checked } : c))}
                className="rounded border-gray-300"
              />
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                Enforce demo test requirement
              </span>
            </label>
            <span title="Require forms to pass a minimum number of demo test runs before they can be published.">
              <HelpCircle className="w-4 h-4 text-gray-400" />
            </span>
          </div>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            When enabled, forms must complete at least the specified number of demo test runs before they can be published.
          </p>
          {config.testThresholdEnabled && (
            <label className="block">
              <span className="text-sm text-gray-600 dark:text-gray-400">Required demo runs (0–100)</span>
              <input
                type="number"
                min={0}
                max={100}
                value={config.testThresholdValue}
                onChange={(e) =>
                  setConfig((c) =>
                    c ? { ...c, testThresholdValue: Math.min(100, Math.max(0, parseInt(e.target.value, 10) || 0)) } : c
                  )
                }
                className="mt-1 block w-32 rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-3 py-2 text-sm"
              />
            </label>
          )}
        </div>

        {/* Require publish approval */}
        <div className="space-y-3">
          <div className="flex items-center gap-2">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={config.requirePublishApproval}
                onChange={(e) => setConfig((c) => (c ? { ...c, requirePublishApproval: e.target.checked } : c))}
                className="rounded border-gray-300"
              />
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                Require publish approval
              </span>
            </label>
            <span
              title="When enabled, Company Users must submit a publish request; a Company Admin approves before the form goes live."
            >
              <HelpCircle className="w-4 h-4 text-gray-400" />
            </span>
          </div>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            When enabled, Company Users cannot publish forms directly. They must submit a publish request, which a Company Admin approves.
          </p>
        </div>
      </div>

      <div className="flex-shrink-0 flex justify-end gap-2 px-4 py-3 border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
        <button
          onClick={handleSave}
          disabled={isSaving}
          className="inline-flex items-center gap-2 px-3 py-1.5 text-sm bg-teal-600 text-white rounded-md hover:bg-teal-700 disabled:opacity-50"
        >
          <Save className="w-4 h-4" />
          {isSaving ? 'Saving...' : 'Save'}
        </button>
      </div>
    </div>
  )
}
