import React, { useState, useEffect } from 'react'
import { X, UserCheck, AlertTriangle, ArrowRight, Files, CheckCircle } from 'lucide-react'
import { transferFormOwnership } from '../api/ownershipApi'
import { TeamMember } from '../../dashboard/types/dashboard.types'
import { getCompanyUsers } from '../../dashboard/api/dashboardApi'
import { useToastNotifications } from '../../ux'

interface BulkTransferOwnershipModalProps {
  isOpen: boolean
  onClose: () => void
  fromUser: TeamMember
  companyId: number
  companyName: string
  onSuccess?: () => void
}

export function BulkTransferOwnershipModal({
  isOpen,
  onClose,
  fromUser,
  companyId,
  companyName,
  onSuccess
}: BulkTransferOwnershipModalProps) {
  const [users, setUsers] = useState<TeamMember[]>([])
  const [selectedToUser, setSelectedToUser] = useState<number | null>(null)
  const [reason, setReason] = useState('Off-boarding / Role Change')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isLoadingUsers, setIsLoadingUsers] = useState(false)
  const [result, setResult] = useState<{ forms: number; access: number } | null>(null)
  const toast = useToastNotifications()

  // Load potential recipients (other active users in company)
  useEffect(() => {
    if (isOpen) {
      loadUsers()
    }
  }, [isOpen, companyId])

  const loadUsers = async () => {
    setIsLoadingUsers(true)
    try {
      const response = await getCompanyUsers(companyId)
      // Filter out the 'from' user and non-active users
      const eligibleUsers = response.users.filter(
        u => u.userId !== fromUser.userId && u.status === 'Active'
      )
      setUsers(eligibleUsers)
    } catch (error) {
      console.error('Failed to load users:', error)
      toast.error('Failed to load team members', 'Error')
    } finally {
      setIsLoadingUsers(false)
    }
  }

  const handleTransfer = async () => {
    if (!selectedToUser) return

    setIsSubmitting(true)
    try {
      const response = await transferFormOwnership({
        from_user_id: fromUser.userId,
        to_user_id: selectedToUser,
        company_id: companyId,
        reason: reason
      })

      setResult({
        forms: response.forms_transferred,
        access: response.access_controls_transferred
      })
      
      toast.success('Ownership transferred successfully', 'Success')
      onSuccess?.()
    } catch (error) {
      const msg = error instanceof Error ? error.message : 'Transfer failed'
      toast.error(msg, 'Error')
    } finally {
      setIsSubmitting(false)
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div 
        className="bg-white rounded-lg shadow-xl w-full max-w-lg transform transition-all"
        role="dialog"
        aria-modal="true"
        aria-labelledby="transfer-ownership-title"
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-amber-600 to-amber-500 text-white px-6 py-4 rounded-t-lg flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Files className="w-5 h-5" />
            <h2 id="transfer-ownership-title" className="text-xl font-bold">
              Transfer Form Ownership
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

        {/* Content */}
        <div className="p-6 space-y-6">
          {result ? (
            // Success State
            <div className="text-center space-y-4">
              <div className="w-16 h-16 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto">
                <CheckCircle className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-bold text-gray-900">Transfer Complete!</h3>
              <p className="text-gray-600">
                Successfully transferred assets from <strong>{fromUser.firstName} {fromUser.lastName}</strong>.
              </p>
              <div className="bg-gray-50 rounded-lg p-4 inline-block text-left">
                <ul className="space-y-2 text-sm">
                  <li className="flex items-center gap-2">
                    <Files className="w-4 h-4 text-teal-600" />
                    <span>{result.forms} Forms Transferred</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <UserCheck className="w-4 h-4 text-blue-600" />
                    <span>{result.access} Access Records Updated</span>
                  </li>
                </ul>
              </div>
              <div className="pt-4">
                <button
                  onClick={onClose}
                  className="px-6 py-2 bg-gray-900 text-white rounded-md hover:bg-gray-800 transition-colors"
                >
                  Close
                </button>
              </div>
            </div>
          ) : (
            // Form State
            <>
              <div className="bg-amber-50 border border-amber-100 rounded-md p-4 flex items-start gap-3">
                <AlertTriangle className="w-5 h-5 text-amber-600 mt-0.5" />
                <div>
                  <h3 className="font-medium text-amber-900">Bulk Transfer Warning</h3>
                  <p className="text-sm text-amber-700 mt-1">
                    This action will transfer <strong>ALL</strong> forms owned by {fromUser.firstName} {fromUser.lastName} to another user. This cannot be easily undone.
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-[1fr,auto,1fr] items-center gap-4 text-center">
                <div className="p-3 bg-gray-100 rounded-lg border border-gray-200">
                  <div className="text-xs text-gray-500 uppercase font-bold mb-1">From</div>
                  <div className="font-medium text-gray-900">{fromUser.firstName} {fromUser.lastName}</div>
                  <div className="text-xs text-gray-500 truncate">{fromUser.email}</div>
                </div>
                
                <ArrowRight className="w-5 h-5 text-gray-400" />
                
                <div className="relative">
                  <div className="text-xs text-gray-500 uppercase font-bold mb-1 text-left">To</div>
                  {isLoadingUsers ? (
                    <div className="text-sm text-gray-500">Loading users...</div>
                  ) : (
                    <select
                      className="w-full p-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
                      value={selectedToUser || ''}
                      onChange={(e) => setSelectedToUser(Number(e.target.value))}
                    >
                      <option value="">Select recipient...</option>
                      {users.map(u => (
                        <option key={u.userId} value={u.userId}>
                          {u.firstName} {u.lastName}
                        </option>
                      ))}
                    </select>
                  )}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Reason for Transfer</label>
                <input 
                  type="text" 
                  className="w-full p-2 border border-gray-300 rounded-md text-sm"
                  value={reason}
                  onChange={(e) => setReason(e.target.value)}
                  placeholder="e.g., Employee off-boarding"
                />
              </div>
            </>
          )}
        </div>

        {/* Footer */}
        {!result && (
          <div className="border-t border-gray-200 bg-gray-50 px-6 py-4 flex items-center justify-end gap-3 rounded-b-lg">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors"
              disabled={isSubmitting}
            >
              Cancel
            </button>
            <button
              type="button"
              onClick={handleTransfer}
              disabled={!selectedToUser || isSubmitting}
              className={`
                px-4 py-2 rounded-md text-sm font-medium text-white flex items-center gap-2 transition-colors
                ${!selectedToUser || isSubmitting
                  ? 'bg-amber-400 cursor-not-allowed' 
                  : 'bg-amber-600 hover:bg-amber-700'}
              `}
            >
              {isSubmitting ? (
                <>
                  <span className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
                  Transferring...
                </>
              ) : (
                <>
                  <Files className="w-4 h-4" />
                  Transfer Ownership
                </>
              )}
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

