import React from 'react'
import { useLocation, useParams } from 'react-router-dom'
import { apiClient } from '../../../lib/apiClient'
import type { FormDefinition } from '../../builder/types/builder.types'
import { PublicFormArtboard } from '../components/PublicFormArtboard'

type PublicResolveResponse = {
  linkType: 'PREVIEW' | 'PRODUCTION' | string
  definition: FormDefinition
}

export const PublicFormRendererPage: React.FC = () => {
  const { token } = useParams<{ token: string }>()
  const location = useLocation()
  const [isLoading, setIsLoading] = React.useState<boolean>(true)
  const [error, setError] = React.useState<string | null>(null)
  const [definition, setDefinition] = React.useState<FormDefinition | null>(null)
  const [linkType, setLinkType] = React.useState<string>('PREVIEW')
  const searchParams = React.useMemo(() => new URLSearchParams(location.search), [location.search])
  const isEmbed = searchParams.get('embed') === '1'
  const action = searchParams.get('action')

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
        setDefinition(res.data.definition)
        setLinkType(res.data.linkType)
      } catch (e: any) {
        if (cancelled) return
        const msg =
          e?.response?.data?.detail ||
          e?.message ||
          'Failed to load form. The link may be invalid or expired.'
        setError(String(msg))
        setDefinition(null)
      } finally {
        if (cancelled) return
        setIsLoading(false)
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

      {/* Renderer body is implemented in subsequent tasks (artboard + registry + runtime rules). */}
      <PublicFormArtboard definition={definition} embed={isEmbed} action={action} />
    </div>
  )
}

