import React, { useState } from 'react'
import { AlertCircle, ChevronDown, ChevronUp, User } from 'lucide-react'

interface ReviewFeedbackPanelProps {
  reviewComments: string | null
  reviewBy?: string | null
  reviewDate?: string | null
  onResubmit: () => void
}

/**
 * Review Feedback Panel Component
 * 
 * Displays review feedback for rejected events
 * - Shows admin name and review date
 * - Collapsible panel for review comments
 * - "Address Feedback & Resubmit" button
 */
export const ReviewFeedbackPanel: React.FC<ReviewFeedbackPanelProps> = ({
  reviewComments,
  reviewBy,
  reviewDate,
  onResubmit,
}) => {
  const [isExpanded, setIsExpanded] = useState(true)

  if (!reviewComments) {
    return null
  }

  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-4">
      <div className="flex items-start gap-3">
        <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" aria-hidden="true" />
        <div className="flex-1">
          <div className="flex items-center justify-between mb-2">
            <div>
              <h4 className="font-medium text-red-900">Event Rejected</h4>
              {(reviewBy || reviewDate) && (
                <div className="text-xs text-red-700 mt-1 flex items-center gap-2">
                  {reviewBy && (
                    <span className="flex items-center gap-1">
                      <User className="w-3 h-3" />
                      Reviewed by {reviewBy}
                    </span>
                  )}
                  {reviewDate && (
                    <span>
                      on {new Date(reviewDate).toLocaleDateString('en-AU')}
                    </span>
                  )}
                </div>
              )}
            </div>
            <button
              type="button"
              onClick={() => setIsExpanded(!isExpanded)}
              className="text-red-600 hover:text-red-800"
              aria-label={isExpanded ? 'Collapse feedback' : 'Expand feedback'}
              aria-expanded={isExpanded}
            >
              {isExpanded ? (
                <ChevronUp className="w-5 h-5" />
              ) : (
                <ChevronDown className="w-5 h-5" />
              )}
            </button>
          </div>

          {isExpanded && (
            <div className="mt-3">
              <p className="text-sm text-red-800 whitespace-pre-wrap">
                {reviewComments}
              </p>
              <button
                type="button"
                onClick={onResubmit}
                className="mt-4 px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-colors"
              >
                Address Feedback & Resubmit
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

