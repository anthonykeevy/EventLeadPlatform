/**
 * PendingPublishRequestsCard - Story 5.6, 5.8
 * Admin-only card showing pending publish requests. Hidden when RequirePublishApproval=false.
 */
import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { ExternalLink, ClipboardList } from 'lucide-react'
import { getPendingPublishRequests, getCompanyTestConfig } from '../../forms/api/formsApi'
import type { PublishRequest } from '../../forms/api/formsApi'

export function PendingPublishRequestsCard() {
  const [requests, setRequests] = useState<PublishRequest[]>([])
  const [loading, setLoading] = useState(true)
  const [requireApproval, setRequireApproval] = useState(true)

  useEffect(() => {
    Promise.all([getPendingPublishRequests(), getCompanyTestConfig()])
      .then(([reqs, config]) => {
        setRequests(reqs)
        setRequireApproval(config.requirePublishApproval)
      })
      .catch(() => setRequests([]))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return null
  if (!requireApproval) return null

  return (
    <div className="mb-6 bg-amber-50 border border-amber-200 rounded-lg p-4">
      <h3 className="text-sm font-semibold text-amber-900 mb-3 flex items-center gap-2">
        <ClipboardList size={18} />
        Pending Publish Requests {requests.length > 0 ? `(${requests.length})` : ''}
      </h3>
      {requests.length === 0 ? (
        <p className="text-sm text-amber-800">No pending publish requests.</p>
      ) : (
        <ul className="space-y-2">
          {requests.map((r) => (
            <li key={r.formPublishRequestId} className="flex items-center justify-between gap-4 py-2 border-b border-amber-100 last:border-0">
              <div className="flex-1 min-w-0">
                <p className="font-medium text-gray-900 truncate">{r.formName}</p>
                <p className="text-xs text-gray-500">
                  Requested by {r.requestedByEmail ?? 'Unknown'} • {formatDate(r.requestedAt)}
                </p>
              </div>
              <Link
                to={`/forms/${r.formId}/review`}
                className="flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-amber-800 bg-amber-100 rounded-md hover:bg-amber-200 transition-colors shrink-0"
              >
                <ExternalLink size={14} />
                Review & Publish
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

function formatDate(iso: string): string {
  try {
    return new Intl.DateTimeFormat('en-AU', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(new Date(iso))
  } catch {
    return iso
  }
}
