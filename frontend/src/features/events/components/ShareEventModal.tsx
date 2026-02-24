import { useState, useEffect } from 'react'
import { X, Share2, Mail, AlertCircle, Building2, Trash2, Shield } from 'lucide-react'
import { shareEventByEmail, getEventCompanies, leaveEvent } from '../api/eventsApi'
import { useToastNotifications } from '../../ux'
import { LoadingSpinner } from '../../ux/components/LoadingSpinner'

interface ShareEventModalProps {
  isOpen: boolean
  eventId: number
  eventName: string
  onClose: () => void
  onSuccess?: () => void
}

export function ShareEventModal({
  isOpen,
  eventId,
  eventName,
  onClose,
  onSuccess
}: ShareEventModalProps) {
  const [email, setEmail] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  const [sharedCompanies, setSharedCompanies] = useState<Array<{
    event_company_id: number
    company_id: number
    company_name: string
    role_code: string
    role_name: string
    is_active: boolean
    forms_created: number
    first_used_date: string | null
    last_used_date: string | null
  }>>([])
  const [isLoadingCompanies, setIsLoadingCompanies] = useState(false)
  
  const toast = useToastNotifications()

  useEffect(() => {
    if (isOpen) {
      loadSharedCompanies()
    }
  }, [isOpen, eventId])

  const loadSharedCompanies = async () => {
    setIsLoadingCompanies(true)
    try {
      const result = await getEventCompanies(eventId)
      if (result.success) {
        setSharedCompanies(result.companies)
      }
    } catch (err) {
      console.error('Failed to load shared companies', err)
    } finally {
      setIsLoadingCompanies(false)
    }
  }

  if (!isOpen) return null

  const handleShare = async () => {
    if (!email) return

    setIsSubmitting(true)
    setError(null)

    try {
      // Default role is 'agency_form_builder' as per requirements
      const response = await shareEventByEmail(eventId, email, 'agency_form_builder')
      
      if (response.alreadyExists) {
         toast.info(response.message, 'Already Shared')
      } else {
         toast.success(response.message, 'Success')
         setEmail('') // Clear email on success
         loadSharedCompanies() // Reload list
      }
      
      onSuccess?.()
      // Don't close modal automatically, let user see the list updated
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to share event'
      setError(errorMessage)
      // Don't show toast for validation errors (like user not found), just show inline error
      if (!errorMessage.includes("User not found")) {
          toast.error(errorMessage, 'Error sharing event')
      }
    } finally {
      setIsSubmitting(false)
    }
  }
  
  const handleRevoke = async (companyId: number, companyName: string) => {
    if (!window.confirm(`Are you sure you want to revoke access for ${companyName}?`)) return

    try {
      // Using leaveEvent which calls the disassociate endpoint.
      // We updated backend to allow owners to disassociate others.
      await leaveEvent(eventId, companyId)
      toast.success(`Access revoked for ${companyName}`, 'Success')
      loadSharedCompanies()
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to revoke access'
      toast.error(errorMessage, 'Error')
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div 
        className="bg-white rounded-lg shadow-xl w-full max-w-2xl transform transition-all max-h-[90vh] flex flex-col"
        role="dialog"
        aria-modal="true"
        aria-labelledby="share-event-title"
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-indigo-600 to-indigo-500 text-white px-6 py-4 rounded-t-lg flex items-center justify-between flex-shrink-0">
          <div className="flex items-center gap-2">
            <Share2 className="w-5 h-5" />
            <h2 id="share-event-title" className="text-xl font-bold">
              Share Event
            </h2>
          </div>
          <button
            onClick={onClose}
            className="text-white hover:text-gray-200 p-1 rounded transition-colors"
            aria-label="Close modal"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-6 space-y-8">
          {/* Share Section */}
          <div className="space-y-6">
            <div className="bg-indigo-50 border border-indigo-100 rounded-md p-4 flex items-start gap-3">
              <Mail className="w-5 h-5 text-indigo-600 mt-0.5" />
              <div>
                <h3 className="font-medium text-indigo-900">Share "{eventName}" with an Agency User</h3>
                <p className="text-sm text-indigo-700 mt-1">
                  Enter the email address of the agency user. If they are already on the platform, their company will be granted access to manage forms for this event.
                </p>
              </div>
            </div>

            <div className="flex gap-3 items-end">
              <div className="flex-1 space-y-1">
                <label className="block text-sm font-medium text-gray-700">
                  User Email Address
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Mail className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 sm:text-sm"
                    placeholder="colleague@agency.com"
                  />
                </div>
              </div>
              <button
                type="button"
                onClick={handleShare}
                disabled={!email || isSubmitting}
                className={`
                  px-4 py-2 rounded-md text-sm font-medium text-white flex items-center gap-2 transition-colors h-[38px]
                  ${!email || isSubmitting
                    ? 'bg-indigo-400 cursor-not-allowed' 
                    : 'bg-indigo-600 hover:bg-indigo-700'}
                `}
              >
                {isSubmitting ? (
                  <>
                    <LoadingSpinner size="sm" color="white" />
                    Sharing...
                  </>
                ) : (
                  <>
                    <Share2 className="w-4 h-4" />
                    Grant Access
                  </>
                )}
              </button>
            </div>

            {error && (
              <div className="bg-red-50 border-l-4 border-red-500 p-4">
                <div className="flex items-start">
                  <AlertCircle className="w-5 h-5 text-red-500 mr-2" />
                  <p className="text-sm text-red-700">{error}</p>
                </div>
              </div>
            )}
          </div>
          
          <hr className="border-gray-200" />
          
          {/* Access List Section */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
              <Shield className="w-5 h-5 text-gray-500" />
              Existing Access
            </h3>
            
            {isLoadingCompanies ? (
               <div className="flex justify-center py-8">
                 <LoadingSpinner size="md" />
               </div>
            ) : sharedCompanies.length === 0 ? (
               <p className="text-gray-500 text-center py-4">No other companies have access to this event.</p>
            ) : (
              <div className="border border-gray-200 rounded-md overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Company</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
                      <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {sharedCompanies.map((company) => (
                      <tr key={company.event_company_id}>
                        <td className="px-4 py-3 whitespace-nowrap">
                          <div className="flex items-center">
                            <div className="flex-shrink-0 h-8 w-8 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-600">
                              <Building2 className="w-4 h-4" />
                            </div>
                            <div className="ml-3">
                              <div className="text-sm font-medium text-gray-900">{company.company_name}</div>
                              <div className="text-xs text-gray-500">ID: {company.company_id}</div>
                            </div>
                          </div>
                        </td>
                        <td className="px-4 py-3 whitespace-nowrap">
                          <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                            ${company.role_code === 'event_owner' ? 'bg-green-100 text-green-800' : 
                              company.role_code === 'event_organizer' ? 'bg-blue-100 text-blue-800' : 
                              'bg-purple-100 text-purple-800'}`}>
                            {company.role_name}
                          </span>
                        </td>
                        <td className="px-4 py-3 whitespace-nowrap text-right text-sm font-medium">
                          {company.role_code !== 'event_owner' && (
                            <button
                              onClick={() => handleRevoke(company.company_id, company.company_name)}
                              className="text-red-600 hover:text-red-900 p-1 rounded hover:bg-red-50 transition-colors"
                              title="Revoke Access"
                            >
                              <Trash2 className="w-4 h-4" />
                            </button>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="border-t border-gray-200 bg-gray-50 px-6 py-4 flex items-center justify-end gap-3 rounded-b-lg flex-shrink-0">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  )
}


