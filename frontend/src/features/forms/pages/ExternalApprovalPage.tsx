import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { Shield, CheckCircle, XCircle, AlertTriangle, Calendar, DollarSign, User } from 'lucide-react'
import { getExternalApprovalContext, submitExternalDecision } from '../api/formsApi'

interface ApprovalContext {
  valid: boolean
  message?: string
  formName?: string
  description?: string
  deploymentCost?: number
  eventStartDate?: string
  requestor?: string
  status?: string
}

export const ExternalApprovalPage: React.FC = () => {
  const { token } = useParams<{ token: string }>()
  const [context, setContext] = useState<ApprovalContext | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [processing, setProcessing] = useState(false)
  const [decisionMade, setDecisionMade] = useState<'APPROVE' | 'REJECT' | null>(null)

  useEffect(() => {
    if (token) {
      loadContext(token)
    } else {
      setError('Invalid approval link.')
      setLoading(false)
    }
  }, [token])

  const loadContext = async (token: string) => {
    try {
      setLoading(true)
      const data = await getExternalApprovalContext(token)
      setContext(data)
      if (!data.valid) {
        setError(data.message || 'Invalid or expired token.')
      }
    } catch (err) {
      console.error(err)
      setError('Failed to load approval request. The link may be expired or invalid.')
    } finally {
      setLoading(false)
    }
  }

  const handleDecision = async (decision: 'APPROVE' | 'REJECT') => {
    if (!token) return
    
    let reason = undefined
    if (decision === 'REJECT') {
        reason = prompt('Please provide a reason for rejection:')
        if (!reason) return // Cancelled
    }

    if (!confirm(`Are you sure you want to ${decision.toLowerCase()} this request?`)) {
        return
    }

    try {
      setProcessing(true)
      await submitExternalDecision(token, decision, reason)
      setDecisionMade(decision)
    } catch (err) {
      console.error(err)
      alert('Failed to submit decision. Please try again.')
    } finally {
      setProcessing(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    )
  }

  if (error || !context?.valid) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
        <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8 text-center">
          <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100 mb-4">
            <AlertTriangle className="h-6 w-6 text-red-600" />
          </div>
          <h2 className="text-xl font-bold text-gray-900 mb-2">Unable to Process Request</h2>
          <p className="text-gray-600">{error || context?.message}</p>
        </div>
      </div>
    )
  }

  if (decisionMade) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
        <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8 text-center">
          <div className={`mx-auto flex items-center justify-center h-16 w-16 rounded-full mb-4 ${
            decisionMade === 'APPROVE' ? 'bg-green-100' : 'bg-red-100'
          }`}>
            {decisionMade === 'APPROVE' ? (
              <CheckCircle className="h-8 w-8 text-green-600" />
            ) : (
              <XCircle className="h-8 w-8 text-red-600" />
            )}
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Request {decisionMade === 'APPROVE' ? 'Approved' : 'Rejected'}
          </h2>
          <p className="text-gray-600">
            Thank you for your response. The requestor has been notified.
          </p>
        </div>
      </div>
    )
  }

  // Urgency Check (Story requirement: Highlight Urgent if near start date)
  const isUrgent = context.eventStartDate && (() => {
      const start = new Date(context.eventStartDate)
      const now = new Date()
      const diffTime = start.getTime() - now.getTime()
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      return diffDays <= 3 && diffDays >= 0
  })()

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-indigo-100 mb-4">
            <Shield className="h-8 w-8 text-indigo-600" />
          </div>
          <h1 className="text-3xl font-extrabold text-gray-900">Approval Request</h1>
          <p className="mt-2 text-lg text-gray-600">
            Please review the following form deployment request.
          </p>
        </div>

        {/* Main Card */}
        <div className="bg-white shadow-xl rounded-lg overflow-hidden">
          {isUrgent && (
            <div className="bg-amber-50 border-l-4 border-amber-400 p-4">
              <div className="flex">
                <div className="flex-shrink-0">
                  <AlertTriangle className="h-5 w-5 text-amber-400" aria-hidden="true" />
                </div>
                <div className="ml-3">
                  <p className="text-sm text-amber-700">
                    <strong>Urgent:</strong> This event starts soon ({new Date(context.eventStartDate!).toLocaleDateString()}). Please review immediately.
                  </p>
                </div>
              </div>
            </div>
          )}

          <div className="p-6 sm:p-8 space-y-6">
            {/* Requestor Info */}
            <div className="flex items-center pb-6 border-b border-gray-200">
              <div className="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center">
                <User className="h-6 w-6 text-gray-500" />
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-medium text-gray-900">{context.requestor}</h3>
                <p className="text-sm text-gray-500">Requested approval for form deployment</p>
              </div>
            </div>

            {/* Form Details */}
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">{context.formName}</h2>
              <p className="text-gray-600">{context.description || 'No description provided.'}</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-gray-50 p-4 rounded-md flex items-start">
                <DollarSign className="h-5 w-5 text-gray-400 mt-0.5 mr-3" />
                <div>
                  <span className="block text-sm font-medium text-gray-500">Deployment Cost</span>
                  <span className="block text-lg font-semibold text-gray-900">
                    ${context.deploymentCost?.toFixed(2)}
                  </span>
                </div>
              </div>

              <div className="bg-gray-50 p-4 rounded-md flex items-start">
                <Calendar className="h-5 w-5 text-gray-400 mt-0.5 mr-3" />
                <div>
                  <span className="block text-sm font-medium text-gray-500">Event Start Date</span>
                  <span className="block text-lg font-semibold text-gray-900">
                    {context.eventStartDate ? new Date(context.eventStartDate).toLocaleDateString() : 'N/A'}
                  </span>
                </div>
              </div>
            </div>

            {/* Actions */}
            <div className="pt-6 border-t border-gray-200 flex flex-col sm:flex-row gap-4 justify-end">
              <button
                onClick={() => handleDecision('REJECT')}
                disabled={processing}
                className="inline-flex justify-center items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 transition-colors w-full sm:w-auto"
              >
                <XCircle className="mr-2 h-5 w-5" />
                Reject Request
              </button>
              <button
                onClick={() => handleDecision('APPROVE')}
                disabled={processing}
                className="inline-flex justify-center items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 transition-colors w-full sm:w-auto"
              >
                <CheckCircle className="mr-2 h-5 w-5" />
                Approve Request
              </button>
            </div>
          </div>
        </div>
        
        <div className="text-center mt-8 text-sm text-gray-500">
          &copy; {new Date().getFullYear()} EventLead Platform. All rights reserved.
        </div>
      </div>
    </div>
  )
}

