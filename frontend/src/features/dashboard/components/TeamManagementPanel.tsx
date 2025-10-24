/**
 * Team Management Panel - Story 1.18
 * AC-1.18.7: User icon opens contextual team panel
 */

import React, { useEffect, useState } from 'react'
import { X, UserPlus, Mail, Users } from 'lucide-react'
import { getCompanyUsers } from '../api/dashboardApi'
import type { TeamMember } from '../types/dashboard.types'

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
  const [isLoading, setIsLoading] = useState(false)
  const isAdmin = userRole === 'Company Admin'

  useEffect(() => {
    if (isOpen && companyId) {
      loadUsers()
    }
  }, [isOpen, companyId])

  const loadUsers = async () => {
    setIsLoading(true)
    try {
      const data = await getCompanyUsers(companyId)
      setUsers(data.users)
    } catch (error) {
      console.error('Failed to load team members:', error)
    } finally {
      setIsLoading(false)
    }
  }

  if (!isOpen) return null

  return (
    <>
      {/* Overlay */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 z-40 transition-opacity"
        onClick={onClose}
      />

      {/* Panel - AC-1.18.7: Slides in from right */}
      <div className="fixed right-0 top-0 bottom-0 w-full md:w-96 bg-white shadow-2xl z-50 transform transition-transform duration-250">
        {/* Header */}
        <div className="bg-teal-600 text-white p-6">
          <div className="flex items-center justify-between mb-2">
            <h2 className="text-xl font-semibold">Team Members</h2>
            <button
              onClick={onClose}
              className="text-white hover:text-gray-200 p-1 rounded"
              aria-label="Close"
            >
              <X className="w-6 h-6" />
            </button>
          </div>
          <p className="text-teal-100 text-sm">{companyName}</p>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto" style={{ height: 'calc(100% - 140px)' }}>
          {isLoading ? (
            <div className="space-y-3">
              {[1, 2, 3].map(i => (
                <div key={i} className="animate-pulse">
                  <div className="h-16 bg-gray-200 rounded"></div>
                </div>
              ))}
            </div>
          ) : users.length === 0 ? (
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
                    
                    {/* Edit button - Only for admins */}
                    {isAdmin && user.status === 'Active' && (
                      <button
                        onClick={() => {/* TODO: Story 1.16 - Edit user role */}}
                        className="text-sm text-teal-600 hover:text-teal-700 font-medium"
                      >
                        Edit
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer - Invite button for admins */}
        {isAdmin && (
          <div className="absolute bottom-0 left-0 right-0 bg-gray-50 border-t border-gray-200 p-4">
            <button
              onClick={() => {/* TODO: Story 1.16 - Invite user modal */}}
              className="w-full py-3 px-4 bg-teal-600 hover:bg-teal-700 text-white rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
            >
              <UserPlus className="w-5 h-5" />
              Invite User
            </button>
          </div>
        )}
      </div>
    </>
  )
}



