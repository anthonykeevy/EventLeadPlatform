/**
 * ReadinessBadge - Story 5.5
 * Shows publish readiness: "Ready to publish" or "X more test runs needed"
 */
import { CheckCircle, AlertCircle } from 'lucide-react'
import type { FormReadiness } from '../api/formsApi'

interface ReadinessBadgeProps {
  readiness: FormReadiness
  onRecordTestRun?: () => void
  loading?: boolean
}

export function ReadinessBadge({ readiness, onRecordTestRun, loading }: ReadinessBadgeProps) {
  if (loading) {
    return (
      <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-gray-100 text-gray-600 text-sm">
        <span className="animate-pulse">Checking readiness...</span>
      </div>
    )
  }

  if (readiness.canPublish) {
    return (
      <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-green-100 text-green-800 text-sm">
        <CheckCircle className="w-4 h-4" />
        <span>Ready to publish</span>
      </div>
    )
  }

  return (
    <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-amber-100 text-amber-800 text-sm">
      <AlertCircle className="w-4 h-4" />
      <span>{readiness.message}</span>
      {onRecordTestRun && readiness.testThresholdRequired > 0 && (
        <button
          type="button"
          onClick={onRecordTestRun}
          className="ml-1 underline font-medium hover:no-underline"
        >
          Record test run
        </button>
      )}
    </div>
  )
}
