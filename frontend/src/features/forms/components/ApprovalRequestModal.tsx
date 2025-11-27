import React, { useState } from 'react'
import { X, Send, Building, Globe, AlertCircle } from 'lucide-react'
import { submitFormForApproval, requestExternalApproval } from '../api/formsApi'

interface ApprovalRequestModalProps {
  isOpen: boolean
  formId: number
  formName: string
  deploymentCost: number
  onClose: () => void
  onSuccess: () => void
}

export function ApprovalRequestModal({
  isOpen,
  formId,
  formName,
  deploymentCost,
  onClose,
  onSuccess
}: ApprovalRequestModalProps) {
  const [mode, setMode] = useState<'INTERNAL' | 'EXTERNAL'>('INTERNAL')
  const [email, setEmail] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)
  const [error, setError] = useState<string | null>(null)

  if (!isOpen) return null

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setIsProcessing(true)

    try {
      if (mode === 'INTERNAL') {
        await submitFormForApproval(formId)
      } else {
        if (!email || !email.includes('@')) {
            throw new Error("Please enter a valid email address.")
        }
        await requestExternalApproval(formId, email)
      }
      onSuccess()
      onClose()
    } catch (err: any) {
      console.error(err)
      setError(err.message || 'Failed to submit request')
    } finally {
      setIsProcessing(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-md overflow-hidden">
        {/* Header */}
        <div className="bg-indigo-600 px-6 py-4 flex justify-between items-center">
          <h3 className="text-white text-lg font-semibold flex items-center gap-2">
            <Send className="w-5 h-5" />
            Request Approval
          </h3>
          <button onClick={onClose} className="text-white hover:text-indigo-200 transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          <div className="bg-blue-50 p-4 rounded-md border border-blue-100">
            <p className="text-sm text-blue-800">
              <strong>{formName}</strong> requires approval before publishing because the estimated cost (${deploymentCost.toFixed(2)}) exceeds the auto-approval threshold.
            </p>
          </div>

          {error && (
            <div className="bg-red-50 p-3 rounded-md flex items-start gap-2 text-red-700 text-sm">
              <AlertCircle className="w-4 h-4 mt-0.5 flex-shrink-0" />
              <p>{error}</p>
            </div>
          )}

          <div className="space-y-4">
            <label className="block text-sm font-medium text-gray-700">Who should approve this request?</label>
            
            {/* Internal Option */}
            <div 
                className={`border rounded-lg p-4 cursor-pointer transition-all ${mode === 'INTERNAL' ? 'border-indigo-500 bg-indigo-50 ring-1 ring-indigo-500' : 'border-gray-200 hover:border-indigo-300'}`}
                onClick={() => setMode('INTERNAL')}
            >
                <div className="flex items-center gap-3">
                    <div className={`w-4 h-4 rounded-full border flex items-center justify-center ${mode === 'INTERNAL' ? 'border-indigo-600' : 'border-gray-400'}`}>
                        {mode === 'INTERNAL' && <div className="w-2 h-2 rounded-full bg-indigo-600" />}
                    </div>
                    <Building className={`w-5 h-5 ${mode === 'INTERNAL' ? 'text-indigo-600' : 'text-gray-500'}`} />
                    <div>
                        <div className="font-medium text-gray-900">Internal Approval</div>
                        <div className="text-xs text-gray-500">Send to Company Administrators</div>
                    </div>
                </div>
            </div>

            {/* External Option */}
            <div 
                className={`border rounded-lg p-4 cursor-pointer transition-all ${mode === 'EXTERNAL' ? 'border-indigo-500 bg-indigo-50 ring-1 ring-indigo-500' : 'border-gray-200 hover:border-indigo-300'}`}
                onClick={() => setMode('EXTERNAL')}
            >
                <div className="flex items-center gap-3 mb-2">
                    <div className={`w-4 h-4 rounded-full border flex items-center justify-center ${mode === 'EXTERNAL' ? 'border-indigo-600' : 'border-gray-400'}`}>
                        {mode === 'EXTERNAL' && <div className="w-2 h-2 rounded-full bg-indigo-600" />}
                    </div>
                    <Globe className={`w-5 h-5 ${mode === 'EXTERNAL' ? 'text-indigo-600' : 'text-gray-500'}`} />
                    <div>
                        <div className="font-medium text-gray-900">External Approval</div>
                        <div className="text-xs text-gray-500">Send to Client or Partner</div>
                    </div>
                </div>
                
                {mode === 'EXTERNAL' && (
                    <div className="mt-3 ml-7 animate-fadeIn">
                        <label className="block text-xs font-medium text-gray-700 mb-1">Approver Email</label>
                        <input
                            type="email"
                            required
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="client@example.com"
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 text-sm"
                            onClick={(e) => e.stopPropagation()} 
                        />
                    </div>
                )}
            </div>
          </div>

          <div className="flex justify-end gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isProcessing}
              className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 flex items-center gap-2 disabled:opacity-50"
            >
              {isProcessing ? 'Sending...' : 'Send Request'}
              <Send className="w-4 h-4" />
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

