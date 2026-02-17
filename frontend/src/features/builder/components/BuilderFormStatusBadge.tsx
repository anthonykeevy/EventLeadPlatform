/**
 * BuilderFormStatusBadge - Story 5.6
 * Displays actual form status in Builder header (Draft, Pending Admin Review, etc.)
 * Replaces hardcoded "Draft" so Builder matches Edit Form / Dashboard status.
 */
import { useState, useEffect } from 'react'
import { getForm } from '../../forms/api/formsApi'

interface BuilderFormStatusBadgeProps {
  formId: string
}

const STATUS_STYLES: Record<string, { bg: string; text: string }> = {
  DRAFT: { bg: 'bg-yellow-100', text: 'text-yellow-800' },
  PENDING_REVIEW: { bg: 'bg-amber-100', text: 'text-amber-800' },
  UNDER_REVIEW: { bg: 'bg-blue-100', text: 'text-blue-800' },
  PUBLISHED: { bg: 'bg-green-100', text: 'text-green-800' },
  PAUSED: { bg: 'bg-gray-100', text: 'text-gray-800' },
}

export function BuilderFormStatusBadge({ formId }: BuilderFormStatusBadgeProps) {
  const [status, setStatus] = useState<{ code: string; name: string } | null>(null)

  useEffect(() => {
    const id = Number(formId)
    if (!id) return
    getForm(id)
      .then((f) => {
        const s = f.formStatus
        if (s) setStatus({ code: s.statusCode, name: s.statusName || s.statusCode })
        else setStatus({ code: 'DRAFT', name: 'Draft' })
      })
      .catch(() => setStatus({ code: 'DRAFT', name: 'Draft' }))
  }, [formId])

  if (!status) return <span className="bg-gray-100 text-gray-600 text-xs px-2 py-0.5 rounded-full font-medium">…</span>

  const style = STATUS_STYLES[status.code.toUpperCase()] ?? { bg: 'bg-gray-100', text: 'text-gray-800' }
  return (
    <span className={`${style.bg} ${style.text} text-xs px-2 py-0.5 rounded-full font-medium`}>
      {status.name}
    </span>
  )
}
