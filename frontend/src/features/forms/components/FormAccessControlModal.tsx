/**
 * Form Access Control Modal - Story 2.9
 * Modal for managing form access control (grant, revoke, view access list)
 */

import { useState, useEffect } from 'react'
import { X, UserPlus, Trash2, Shield, Clock, User, Building2, AlertCircle } from 'lucide-react'
import { getFormAccessList, revokeFormAccess, checkFormAccess } from '../api/formAccessApi'
import { AccessControlResponse, AccessCheckResponse } from '../types/form-access.types'
import { useToastNotifications } from '../../ux'
import { GrantAccessForm } from './GrantAccessForm'

interface FormAccessControlModalProps {
  isOpen: boolean
  formId: number
  onClose: () => void
}

export function FormAccessControlModal({ isOpen, formId, onClose }: FormAccessControlModalProps) {
  const [accessList, setAccessList] = useState<AccessControlResponse[]>([])
  const [currentUserAccess, setCurrentUserAccess] = useState<AccessCheckResponse | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [showGrantForm, setShowGrantForm] = useState(false)
  const [revokingId, setRevokingId] = useState<number | null>(null)
  
  const toast = useToastNotifications()

  // Load access list and current user access
  useEffect(() => {
    if (isOpen && formId) {
      loadAccessData()
    }
  }, [isOpen, formId])

  const loadAccessData = async () => {
    try {
      setIsLoading(true)
      const [accessListData, userAccessData] = await Promise.all([
        getFormAccessList(formId),
        checkFormAccess(formId),
      ])
      setAccessList(accessListData.accessEntries)
      setCurrentUserAccess(userAccessData)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load access data'
      toast.error(errorMessage, 'Error')
    } finally {
      setIsLoading(false)
    }
  }

  const handleRevoke = async (accessId: number) => {
    if (!confirm('Are you sure you want to revoke this access?')) {
      return
    }

    try {
      setRevokingId(accessId)
      await revokeFormAccess(formId, accessId)
      toast.success('Access revoked successfully', 'Success')
      loadAccessData() // Reload access list
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to revoke access'
      toast.error(errorMessage, 'Error')
    } finally {
      setRevokingId(null)
    }
  }

  const handleGrantSuccess = () => {
    setShowGrantForm(false)
    loadAccessData() // Reload access list
  }

  const canManageAccess = currentUserAccess?.accessLevel === 'MANAGE' || currentUserAccess?.hasAccess === true

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-teal-600 to-teal-500 text-white px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Shield className="w-6 h-6" />
            <h2 className="text-2xl font-bold">Form Access Control</h2>
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
        <div className="overflow-y-auto max-h-[calc(90vh-180px)] p-6">
          {/* Current User Access Info */}
          {currentUserAccess && (
            <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-md">
              <div className="flex items-center gap-2 mb-2">
                <Shield className="w-5 h-5 text-blue-600" />
                <span className="font-semibold text-blue-900">Your Access Level</span>
              </div>
              <p className="text-sm text-blue-800">
                {currentUserAccess.accessLevel ? (
                  <span className="font-medium">{currentUserAccess.accessLevel}</span>
                ) : (
                  <span className="text-gray-600">No access</span>
                )}
              </p>
            </div>
          )}

          {/* Grant Access Form or Access List */}
          {showGrantForm ? (
            <GrantAccessForm
              formId={formId}
              onSuccess={handleGrantSuccess}
              onCancel={() => setShowGrantForm(false)}
            />
          ) : (
            <>
              {/* Actions */}
              {canManageAccess && (
                <div className="mb-6 flex justify-end">
                  <button
                    onClick={() => setShowGrantForm(true)}
                    className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-teal-600 rounded-md hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500"
                  >
                    <UserPlus className="w-4 h-4" />
                    Grant Access
                  </button>
                </div>
              )}

              {/* Access List */}
              {isLoading ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-600 mx-auto"></div>
                  <p className="mt-2 text-sm text-gray-600">Loading access list...</p>
                </div>
              ) : accessList.length === 0 ? (
                <div className="text-center py-8">
                  <Shield className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                  <p className="text-gray-600">No access grants found for this form.</p>
                  {canManageAccess && (
                    <button
                      onClick={() => setShowGrantForm(true)}
                      className="mt-4 text-teal-600 hover:text-teal-700 font-medium"
                    >
                      Grant the first access
                    </button>
                  )}
                </div>
              ) : (
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-gray-900">
                    Access Grants {accessList.length > 0 && (
                      <span className="text-sm font-normal text-gray-500">({accessList.length})</span>
                    )}
                  </h3>
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            User/Company
                          </th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Access Type
                          </th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Relationship
                          </th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Granted By
                          </th>
                          <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Expiry
                          </th>
                          {canManageAccess && (
                            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                              Actions
                            </th>
                          )}
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {accessList.map((access) => (
                          <tr key={access.formAccessControlId} className={access.isExpired ? 'bg-gray-50 opacity-60' : ''}>
                            <td className="px-4 py-3 whitespace-nowrap text-sm">
                              <div className="flex items-center gap-2">
                                {access.userId && access.user ? (
                                  <>
                                    <User className="w-4 h-4 text-gray-400" />
                                    <div className="flex flex-col">
                                      <span className="font-medium text-gray-900">
                                        {access.user.firstName || access.user.lastName
                                          ? `${access.user.firstName || ''} ${access.user.lastName || ''}`.trim()
                                          : access.user.email}
                                      </span>
                                      {access.user.firstName || access.user.lastName ? (
                                        <span className="text-xs text-gray-500">{access.user.email}</span>
                                      ) : null}
                                    </div>
                                  </>
                                ) : access.companyId && access.company ? (
                                  <>
                                    <Building2 className="w-4 h-4 text-gray-400" />
                                    <span className="font-medium text-gray-900">{access.company.companyName}</span>
                                  </>
                                ) : access.userId ? (
                                  <>
                                    <User className="w-4 h-4 text-gray-400" />
                                    <span className="text-gray-500">User ID: {access.userId}</span>
                                  </>
                                ) : access.companyId ? (
                                  <>
                                    <Building2 className="w-4 h-4 text-gray-400" />
                                    <span className="text-gray-500">Company ID: {access.companyId}</span>
                                  </>
                                ) : (
                                  <span className="text-gray-500">Unknown</span>
                                )}
                              </div>
                            </td>
                            <td className="px-4 py-3 whitespace-nowrap text-sm">
                              <span className="px-2 py-1 text-xs font-medium rounded-full bg-teal-100 text-teal-800">
                                {access.accessType?.accessTypeName || 'Unknown'}
                              </span>
                            </td>
                            <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-600">
                              {access.relationshipType?.typeName || 'Unknown'}
                            </td>
                            <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-600">
                              {access.grantedBy ? (
                                <span>{access.grantedBy.email}</span>
                              ) : (
                                <span className="text-gray-400">Unknown</span>
                              )}
                            </td>
                            <td className="px-4 py-3 whitespace-nowrap text-sm">
                              {access.isExpired ? (
                                <span className="flex items-center gap-1 text-red-600">
                                  <AlertCircle className="w-4 h-4" />
                                  Expired
                                </span>
                              ) : access.expiryDate ? (
                                <span className="flex items-center gap-1 text-gray-600">
                                  <Clock className="w-4 h-4" />
                                  {(() => {
                                    try {
                                      // Format expiry date using country-specific format (en-AU)
                                      // Backend sends UTC datetime, display in local time with country format
                                      const date = new Date(access.expiryDate)
                                      return new Intl.DateTimeFormat('en-AU', {
                                        year: 'numeric',
                                        month: 'short',
                                        day: 'numeric',
                                        hour: '2-digit',
                                        minute: '2-digit',
                                        hour12: true
                                      }).format(date)
                                    } catch {
                                      return new Date(access.expiryDate).toLocaleDateString('en-AU')
                                    }
                                  })()}
                                </span>
                              ) : (
                                <span className="text-gray-400">Permanent</span>
                              )}
                            </td>
                            {canManageAccess && (
                              <td className="px-4 py-3 whitespace-nowrap text-sm">
                                <button
                                  onClick={() => handleRevoke(access.formAccessControlId)}
                                  disabled={revokingId === access.formAccessControlId}
                                  className="text-red-600 hover:text-red-700 disabled:opacity-50 disabled:cursor-not-allowed"
                                  title="Revoke access"
                                >
                                  <Trash2 className="w-4 h-4" />
                                </button>
                              </td>
                            )}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </>
          )}
        </div>

        {/* Footer */}
        <div className="bg-gray-50 px-6 py-4 border-t border-gray-200 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  )
}

