/**
 * Team Management Panel - Story 1.16 (Enhanced)
 * AC-1.16.1: Team Management Dashboard
 * AC-1.16.3: Invitation List with Actions
 * AC-1.16.8: Pending invitations show status and resend option
 */

import { useEffect, useState, useCallback } from 'react'
import { X, UserPlus, Mail, Users, RotateCw, XCircle, Edit } from 'lucide-react'
import { getCompanyUsers } from '../api/dashboardApi'
import { listInvitations, resendInvitation, cancelInvitation } from '../api/teamApi'
import { InviteUserModal } from './InviteUserModal'
import { EditRoleModal } from './EditRoleModal'
import type { TeamMember } from '../types/dashboard.types'
import type { Invitation } from '../types/team.types'

interface TeamManagementPanelProps {
  companyId: number
  companyName: string
  userRole: 'Company Admin' | 'Company User'
  isOpen: boolean
  onClose: () => void
}

export function TeamManagementPanel({
  companyId,
  companyName,
  userRole,
  isOpen,
  onClose
}: TeamManagementPanelProps) {
  const [users, setUsers] = useState<TeamMember[]>([])
  const [invitations, setInvitations] = useState<Invitation[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [activeTab, setActiveTab] = useState<'members' | 'invitations'>('members')
  
  // Modal states
  const [showInviteModal, setShowInviteModal] = useState(false)
  const [showEditModal, setShowEditModal] = useState(false)
  const [selectedUser, setSelectedUser] = useState<TeamMember | null>(null)
  
  const isAdmin = userRole === 'Company Admin'

  const loadData = useCallback(async () => {
    setIsLoading(true)
    try {
      // Load users
      const userData = await getCompanyUsers(companyId)
      setUsers(userData.users)
      
      // Load invitations (only if admin)
      if (isAdmin) {
        const invitationData = await listInvitations(companyId, 'pending')
        setInvitations(invitationData.invitations)
      }
    } catch (error) {
      console.error('Failed to load team data:', error)
    } finally {
      setIsLoading(false)
    }
  }, [companyId, isAdmin])

  useEffect(() => {
    if (isOpen && companyId) {
      loadData()
    }
  }, [isOpen, companyId, loadData])

  const handleResendInvitation = useCallback(async (invitationId: number) => {
    try {
      await resendInvitation(companyId, invitationId)
      // Reload data to show updated resend count
      await loadData()
      // TODO: Show success toast
    } catch (error) {
      console.error('Failed to resend invitation:', error)
      // TODO: Show error toast
    }
  }, [companyId, loadData])

  const handleCancelInvitation = useCallback(async (invitationId: number) => {
    if (!confirm('Are you sure you want to cancel this invitation?')) {
      return
    }
    
    try {
      await cancelInvitation(companyId, invitationId)
      // Reload data to remove cancelled invitation
      await loadData()
      // TODO: Show success toast
    } catch (error) {
      console.error('Failed to cancel invitation:', error)
      // TODO: Show error toast
    }
  }, [companyId, loadData])

  const handleEditRole = useCallback((user: TeamMember) => {
    setSelectedUser(user)
    setShowEditModal(true)
  }, [])

  const handleInviteSuccess = useCallback(() => {
    // Reload data to show new invitation
    loadData()
    // TODO: Show success toast
  }, [loadData])

  const handleEditSuccess = useCallback(() => {
    // Reload data to show updated role
    loadData()
    // TODO: Show success toast
  }, [loadData])

  if (!isOpen) return null

  return (
    <>
      {/* Overlay */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 z-40 transition-opacity"
        onClick={onClose}
      />

      {/* Panel - AC-1.16.1: Team Management Dashboard */}
      <div className="fixed right-0 top-0 bottom-0 w-full md:w-96 bg-white shadow-2xl z-50 transform transition-transform duration-250">
        {/* Header */}
        <div className="bg-teal-600 text-white p-6">
          <div className="flex items-center justify-between mb-2">
            <h2 className="text-xl font-semibold">Team Management</h2>
            <button
              onClick={onClose}
              className="text-white hover:text-gray-200 p-1 rounded"
              aria-label="Close"
            >
              <X className="w-6 h-6" />
            </button>
          </div>
          <p className="text-teal-100 text-sm">{companyName}</p>
          
          {/* Tabs */}
          <div className="flex gap-2 mt-4">
            <button
              onClick={() => setActiveTab('members')}
              className={`flex-1 px-4 py-2 rounded-lg font-medium transition-colors ${
                activeTab === 'members'
                  ? 'bg-white text-teal-600'
                  : 'bg-teal-700 text-white hover:bg-teal-800'
              }`}
            >
              Members ({users.length})
            </button>
            {isAdmin && (
              <button
                onClick={() => setActiveTab('invitations')}
                className={`flex-1 px-4 py-2 rounded-lg font-medium transition-colors ${
                  activeTab === 'invitations'
                    ? 'bg-white text-teal-600'
                    : 'bg-teal-700 text-white hover:bg-teal-800'
                }`}
              >
                Invitations ({invitations.length})
              </button>
            )}
          </div>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto" style={{ height: 'calc(100% - 240px)' }}>
          {isLoading ? (
            <div className="space-y-3">
              {[1, 2, 3].map(i => (
                <div key={i} className="animate-pulse">
                  <div className="h-16 bg-gray-200 rounded"></div>
                </div>
              ))}
            </div>
          ) : activeTab === 'members' ? (
            // Members Tab
            users.length === 0 ? (
              <div className="text-center text-gray-500 py-8">
                <Users className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                <p>No team members yet</p>
              </div>
            ) : (
              <div className="space-y-3">
                {users.map(user => (
                  <div
                    key={user.userId}
                    className="border border-gray-200 rounded-lg p-4 hover:border-gray-300 transition-colors"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="font-medium text-gray-900">
                          {user.firstName} {user.lastName}
                        </div>
                        <div className="text-sm text-gray-500 flex items-center gap-1 mt-1">
                          <Mail className="w-3 h-3" />
                          {user.email}
                        </div>
                        <div className="flex items-center gap-2 mt-2">
                          {/* Role Badge */}
                          <span className="text-xs px-2 py-1 rounded-full bg-blue-100 text-blue-700">
                            {user.role}
                          </span>
                          {/* Status Badge */}
                          <span className={`text-xs px-2 py-1 rounded-full ${
                            user.status === 'Active' ? 'bg-green-100 text-green-700' :
                            user.status === 'Pending' ? 'bg-yellow-100 text-yellow-700' :
                            'bg-gray-100 text-gray-700'
                          }`}>
                            {user.status}
                          </span>
                        </div>
                      </div>
                      
                      {/* Edit button - AC-1.16.3: Only for admins on active users */}
                      {isAdmin && user.status === 'Active' && (
                        <button
                          onClick={() => handleEditRole(user)}
                          className="text-sm text-teal-600 hover:text-teal-700 font-medium flex items-center gap-1"
                        >
                          <Edit className="w-4 h-4" />
                          Edit
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )
          ) : (
            // Invitations Tab - AC-1.16.3: Invitation List with Actions
            invitations.length === 0 ? (
              <div className="text-center text-gray-500 py-8">
                <Mail className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                <p>No pending invitations</p>
                <p className="text-sm mt-1">Click "Invite User" below to send an invitation</p>
              </div>
            ) : (
              <div className="space-y-3">
                {invitations.map(invitation => (
                  <div
                    key={invitation.invitationId}
                    className="border border-gray-200 rounded-lg p-4 hover:border-gray-300 transition-colors"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="font-medium text-gray-900">
                          {invitation.firstName} {invitation.lastName}
                        </div>
                        <div className="text-sm text-gray-500 flex items-center gap-1 mt-1">
                          <Mail className="w-3 h-3" />
                          {invitation.email}
                        </div>
                        <div className="flex items-center gap-2 mt-2">
                          {/* Role Badge */}
                          <span className="text-xs px-2 py-1 rounded-full bg-blue-100 text-blue-700">
                            {invitation.role === 'company_admin' ? 'Company Admin' : 'Company User'}
                          </span>
                          {/* Status Badge - AC-1.16.8 */}
                          <span className="text-xs px-2 py-1 rounded-full bg-yellow-100 text-yellow-700">
                            {invitation.status}
                          </span>
                        </div>
                        <div className="text-xs text-gray-500 mt-2">
                          Invited by {invitation.invitedBy}
                          {invitation.resendCount > 0 && ` • Resent ${invitation.resendCount}x`}
                        </div>
                      </div>
                    </div>
                    
                    {/* Action buttons - AC-1.16.3: Resend, Cancel */}
                    {invitation.status === 'pending' && (
                      <div className="flex gap-2 mt-3">
                        <button
                          onClick={() => handleResendInvitation(invitation.invitationId)}
                          className="flex-1 text-sm py-2 px-3 border border-teal-600 text-teal-600 hover:bg-teal-50 rounded-lg font-medium transition-colors flex items-center justify-center gap-1"
                        >
                          <RotateCw className="w-4 h-4" />
                          Resend
                        </button>
                        <button
                          onClick={() => handleCancelInvitation(invitation.invitationId)}
                          className="flex-1 text-sm py-2 px-3 border border-red-600 text-red-600 hover:bg-red-50 rounded-lg font-medium transition-colors flex items-center justify-center gap-1"
                        >
                          <XCircle className="w-4 h-4" />
                          Cancel
                        </button>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )
          )}
          
          {/* Non-admin message - AC-1.16.4 */}
          {!isAdmin && (
            <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
              <p className="text-sm text-blue-700">
                Contact a Company Admin to manage team members and send invitations.
              </p>
            </div>
          )}
        </div>

        {/* Footer - Invite button for admins - AC-1.16.2 */}
        {isAdmin && (
          <div className="absolute bottom-0 left-0 right-0 bg-gray-50 border-t border-gray-200 p-4">
            <button
              onClick={() => setShowInviteModal(true)}
              className="w-full py-3 px-4 bg-teal-600 hover:bg-teal-700 text-white rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
            >
              <UserPlus className="w-5 h-5" />
              Invite User
            </button>
          </div>
        )}
      </div>

      {/* Modals */}
      <InviteUserModal
        companyId={companyId}
        companyName={companyName}
        isOpen={showInviteModal}
        onClose={() => setShowInviteModal(false)}
        onSuccess={handleInviteSuccess}
      />
      
      {selectedUser && (
        <EditRoleModal
          companyId={companyId}
          companyName={companyName}
          userId={selectedUser.userId}
          userName={`${selectedUser.firstName} ${selectedUser.lastName}`}
          currentRole={selectedUser.role}
          currentUserRole={userRole}
          isOpen={showEditModal}
          onClose={() => {
            setShowEditModal(false)
            setSelectedUser(null)
          }}
          onSuccess={handleEditSuccess}
        />
      )}
    </>
  )
}
