import React from 'react'
import { useLocation, useParams } from 'react-router-dom'
import { apiClient } from '../../../lib/apiClient'
import { requestRepublish } from '../../forms/api/formsApi'
import type { FormDefinition } from '../../builder/types/builder.types'
import { PublicFormArtboard } from '../components/PublicFormArtboard'

function UnpublishedFormPage({ token, message }: { token: string; message: string | null }) {
  const [requesting, setRequesting] = React.useState(false)
  const [requested, setRequested] = React.useState(false)

  const handleRequestRepublish = async () => {
    try {
      setRequesting(true)
      await requestRepublish(token)
      setRequested(true)
    } catch {
      setRequesting(false)
    } finally {
      setRequesting(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6 flex items-center justify-center">
      <div className="max-w-xl mx-auto rounded-lg border border-gray-200 bg-white p-6 text-center">
        <div className="font-semibold text-lg text-gray-900 mb-2">Form no longer active</div>
        <div className="text-gray-600 text-sm mb-4">
          {message ?? 'This form is no longer active. It has been unpublished.'}
        </div>
        {!requested ? (
          <p className="text-sm text-gray-700 mb-3">
            If this form should still be available, you can request the administrator to publish it again.
          </p>
        ) : (
          <p className="text-sm text-green-700 mb-3">
            Your request has been recorded. The administrator will be notified.
          </p>
        )}
        {!requested && (
          <button
            type="button"
            onClick={handleRequestRepublish}
            disabled={requesting}
            className="px-4 py-2 bg-teal-600 text-white rounded-md hover:bg-teal-700 disabled:opacity-50 text-sm font-medium"
          >
            {requesting ? 'Sending…' : 'Request admin to publish again'}
          </button>
        )}
      </div>
    </div>
  )
}

type PublicResolveResponse = {
  linkType: 'PREVIEW' | 'PRODUCTION' | 'UNPUBLISHED' | 'EVENT_ENDED' | string
  definition?: FormDefinition | null
  message?: string
}

export const PublicFormRendererPage: React.FC = () => {
  const { token } = useParams<{ token: string }>()
  const location = useLocation()
  const [isLoading, setIsLoading] = React.useState<boolean>(true)
  const [error, setError] = React.useState<string | null>(null)
  const [definition, setDefinition] = React.useState<FormDefinition | null>(null)
  const [linkType, setLinkType] = React.useState<string>('PREVIEW')
  const [resolveMessage, setResolveMessage] = React.useState<string | null>(null)
  const searchParams = React.useMemo(() => new URLSearchParams(location.search), [location.search])
  const isEmbed = searchParams.get('embed') === '1'
  const action = searchParams.get('action')
  const kioskEnabled = searchParams.get('kiosk') === '1'
  const parseNumberParam = React.useCallback(
    (key: string) => {
      const raw = searchParams.get(key)
      if (!raw) return undefined
      const value = Number(raw)
      return Number.isFinite(value) ? value : undefined
    },
    [searchParams]
  )
  const autoResetSeconds = parseNumberParam('autoResetSeconds')
  const countdownSeconds = parseNumberParam('countdownSeconds')

  React.useEffect(() => {
    let cancelled = false
    async function run() {
      if (!token) {
        setError('Missing form token.')
        setIsLoading(false)
        return
      }
      setIsLoading(true)
      setError(null)
      try {
        const res = await apiClient.get<PublicResolveResponse>(`/api/public/forms/${token}`)
        if (cancelled) return
        setDefinition(res.data.definition ?? null)
        setLinkType(res.data.linkType)
        setResolveMessage(res.data.message ?? null)
      } catch (e: unknown) {
        if (cancelled) return
        const detail = (e as { response?: { data?: { detail?: unknown } } })?.response?.data?.detail
        const message = e instanceof Error ? e.message : undefined
        const msg =
          (typeof detail === 'string' && detail) ||
          message ||
          'Failed to load form. The link may be invalid or expired.'
        setError(msg)
        setDefinition(null)
      } finally {
        if (!cancelled) setIsLoading(false)
      }
    }
    run()
    return () => {
      cancelled = true
    }
  }, [token])

  if (isLoading) {
    return <div className="min-h-screen bg-gray-50 p-6">Loading…</div>
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-xl mx-auto rounded border border-red-200 bg-red-50 p-4 text-red-900">
          <div className="font-semibold mb-1">Unable to open form</div>
          <div className="text-sm">{error}</div>
        </div>
      </div>
    )
  }

  if (linkType === 'UNPUBLISHED') {
    return (
      <UnpublishedFormPage token={token!} message={resolveMessage} />
    )
  }

  if (linkType === 'EVENT_ENDED') {
    return (
      <div className="min-h-screen bg-gray-50 p-6 flex items-center justify-center">
        <div className="max-w-xl mx-auto rounded-lg border border-amber-200 bg-amber-50 p-6 text-amber-900 text-center">
          <div className="font-semibold text-lg mb-2">Form not available</div>
          <div className="text-sm">{resolveMessage ?? 'This form is no longer active. The event has ended.'}</div>
        </div>
      </div>
    )
  }

  if (!definition) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-xl mx-auto rounded border border-gray-200 bg-white p-4 text-gray-800">
          No definition loaded.
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {isEmbed ? null : (
        <header className="bg-white border-b border-gray-200 px-4 py-3">
          <div className="max-w-6xl mx-auto flex items-center justify-between gap-3">
            <div className="font-semibold text-gray-900">Public Form</div>
            <div className="text-xs text-gray-500">Link: {linkType}</div>
          </div>
        </header>
      )}

      <PublicFormArtboard
        definition={definition}
        embed={isEmbed}
        action={action}
        token={token}
        linkType={linkType}
        kioskEnabled={kioskEnabled}
        autoResetSeconds={autoResetSeconds}
        countdownSeconds={countdownSeconds}
      />
    </div>
  )
}

