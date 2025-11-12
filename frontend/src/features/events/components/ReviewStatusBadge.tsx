import React from 'react'
import { Clock, CheckCircle, XCircle, AlertCircle } from 'lucide-react'

interface ReviewStatusBadgeProps {
  status: 'PENDING' | 'APPROVED' | 'REJECTED' | null
  statusName?: string
  onResubmit?: () => void
  onViewGuidelines?: () => void
  onPublish?: () => void
}

/**
 * Review Status Badge Component
 * 
 * Displays color-coded status badges with icons and text labels
 * - Pending: Orange/Yellow badge
 * - Approved: Green badge
 * - Rejected: Red badge
 * 
 * Includes action buttons based on status:
 * - Pending: View Guidelines
 * - Approved: Publish Event (if not already published)
 * - Rejected: Resubmit, View Guidelines
 */
export const ReviewStatusBadge: React.FC<ReviewStatusBadgeProps> = ({
  status,
  statusName,
  onResubmit,
  onViewGuidelines,
  onPublish,
}) => {
  if (!status) {
    return null
  }

  const getStatusConfig = () => {
    switch (status) {
      case 'PENDING':
        return {
          icon: Clock,
          bgColor: 'bg-yellow-100',
          textColor: 'text-yellow-800',
          borderColor: 'border-yellow-300',
          iconColor: 'text-yellow-600',
          label: statusName || 'Pending Review',
        }
      case 'APPROVED':
        return {
          icon: CheckCircle,
          bgColor: 'bg-green-100',
          textColor: 'text-green-800',
          borderColor: 'border-green-300',
          iconColor: 'text-green-600',
          label: statusName || 'Approved',
        }
      case 'REJECTED':
        return {
          icon: XCircle,
          bgColor: 'bg-red-100',
          textColor: 'text-red-800',
          borderColor: 'border-red-300',
          iconColor: 'text-red-600',
          label: statusName || 'Rejected',
        }
      default:
        return null
    }
  }

  const config = getStatusConfig()
  if (!config) return null

  const Icon = config.icon

  return (
    <div
      className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-md border ${config.bgColor} ${config.textColor} ${config.borderColor}`}
      role="status"
      aria-live="polite"
      aria-label={`Review status: ${config.label}`}
    >
      <Icon className={`w-4 h-4 ${config.iconColor}`} aria-hidden="true" />
      <span className="font-medium text-sm">{config.label}</span>

      {/* Action Buttons */}
      <div className="ml-2 flex items-center gap-2">
        {status === 'PENDING' && onViewGuidelines && (
          <button
            type="button"
            onClick={onViewGuidelines}
            className="text-xs underline hover:no-underline"
            aria-label="View public event guidelines"
          >
            View Guidelines
          </button>
        )}
        {status === 'APPROVED' && onPublish && (
          <button
            type="button"
            onClick={onPublish}
            className="text-xs underline hover:no-underline"
            aria-label="Publish event"
          >
            Publish Event
          </button>
        )}
        {status === 'REJECTED' && (
          <>
            {onResubmit && (
              <button
                type="button"
                onClick={onResubmit}
                className="text-xs underline hover:no-underline"
                aria-label="Resubmit event for review"
              >
                Resubmit
              </button>
            )}
            {onViewGuidelines && (
              <button
                type="button"
                onClick={onViewGuidelines}
                className="text-xs underline hover:no-underline"
                aria-label="View public event guidelines"
              >
                View Guidelines
              </button>
            )}
          </>
        )}
      </div>
    </div>
  )
}

