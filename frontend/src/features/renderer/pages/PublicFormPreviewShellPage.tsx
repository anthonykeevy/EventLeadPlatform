import React from 'react'
import { useParams } from 'react-router-dom'

export const PublicFormPreviewShellPage: React.FC = () => {
  const { token } = useParams<{ token: string }>()
  const [action, setAction] = React.useState<string>('')
  const [nonce, setNonce] = React.useState(0)

  if (!token) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-xl mx-auto rounded border border-red-200 bg-red-50 p-4 text-red-900">
          Missing preview token.
        </div>
      </div>
    )
  }

  const embedUrl = `/forms/${token}?embed=1${action ? `&action=${action}` : ''}&nonce=${nonce}`
  const publicUrl = `/forms/${token}`

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 px-4 py-3">
        <div className="max-w-6xl mx-auto flex items-center justify-between gap-3">
          <div>
            <div className="font-semibold text-gray-900">Preview Helper</div>
            <div className="text-xs text-gray-500">Token preview with validation/reset helpers.</div>
          </div>
          <div className="flex items-center gap-2">
            <button
              className="btn-secondary text-sm"
              onClick={() => {
                setAction('validate')
                setNonce(n => n + 1)
              }}
              title="Trigger validation in the preview"
            >
              Validate
            </button>
            <button
              className="btn-secondary text-sm"
              onClick={() => {
                setAction('reset')
                setNonce(n => n + 1)
              }}
              title="Reset preview values"
            >
              Reset
            </button>
            <button
              className="btn-secondary text-sm"
              onClick={() => window.open(publicUrl, '_blank', 'noopener,noreferrer')}
              title="Open the public preview without the helper shell"
            >
              Open Public
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto p-4">
        <div className="rounded border border-gray-200 bg-white shadow-sm overflow-hidden">
          <iframe
            title="Public form preview (embedded)"
            src={embedUrl}
            className="w-full"
            style={{ height: 'calc(100vh - 140px)', border: 0 }}
          />
        </div>
      </main>
    </div>
  )
}
