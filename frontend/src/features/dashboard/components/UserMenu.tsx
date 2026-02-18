/**
 * User Menu Component for Dashboard
 * Provides user settings and theme customization access
 * Story 2.6: Added Admin Dashboard access for system admins
 * Story 5.7: Company Settings link (hide if user is not admin for active company)
 */

import { useState, useRef, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { User as UserIcon, LogOut, Settings, Palette, ChevronDown, Shield, Building2 } from 'lucide-react'
import { useAuth } from '../../auth'
import { ThemeSettingsPopup } from './ThemeSettingsPopup'
import { AccountSettingsPopup } from '../../preferences/components/AccountSettingsPopup'

interface UserMenuProps {
  user: {
    first_name: string
    last_name: string
    email: string
    role?: string  // Story 2.6: System role (e.g., 'system_admin') or company role
  }
  /** Story 5.7: Show Company Settings link when user is admin for active company */
  companySettingsLink?: string | null
}

export function UserMenu({ user, companySettingsLink }: UserMenuProps) {
  const { logout } = useAuth()
  const navigate = useNavigate()
  const [isOpen, setIsOpen] = useState(false)
  const [showThemePopup, setShowThemePopup] = useState(false)
  const [showAccountPopup, setShowAccountPopup] = useState(false)
  const menuRef = useRef<HTMLDivElement>(null)

  // Check if user is system admin
  const isSystemAdmin = user.role === 'system_admin'

  // Close menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [])

  const handleLogout = () => {
    logout()
    navigate('/login')
    setIsOpen(false)
  }

  const handleThemeSettings = () => {
    setShowThemePopup(true)
    setIsOpen(false)
  }

  const handleAccountSettings = () => {
    setShowAccountPopup(true)
    setIsOpen(false)
  }

  // Story 2.6: Admin Dashboard navigation handler
  const handleAdminDashboard = () => {
    navigate('/admin/dashboard')
    setIsOpen(false)
  }

  return (
    <>
      <div className="relative" ref={menuRef}>
        {/* User Menu Trigger */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="flex items-center gap-2 px-3 py-2 text-sm text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
          aria-expanded={isOpen}
          aria-haspopup="true"
        >
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-teal-100 rounded-full flex items-center justify-center">
              <UserIcon className="w-4 h-4 text-teal-600" />
            </div>
            <div className="text-left">
              <div className="font-medium text-gray-900">
                {user.first_name} {user.last_name}
              </div>
              <div className="text-xs text-gray-500 truncate max-w-32">
                {user.email}
              </div>
            </div>
          </div>
          <ChevronDown className={`w-4 h-4 text-gray-400 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
        </button>

        {/* Dropdown Menu */}
        {isOpen && (
          <div className="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50">
            {/* User Info Header */}
            <div className="px-4 py-3 border-b border-gray-100">
              <div className="font-medium text-gray-900">
                {user.first_name} {user.last_name}
              </div>
              <div className="text-sm text-gray-500">
                {user.email}
              </div>
            </div>

            {/* Menu Items */}
            <div className="py-2">
              {/* Admin Dashboard - Story 2.6: Only show for system admins */}
              {isSystemAdmin && (
                <>
                  <button
                    onClick={handleAdminDashboard}
                    className="w-full flex items-center gap-3 px-4 py-2 text-sm text-purple-700 hover:bg-purple-50 transition-colors"
                  >
                    <Shield className="w-4 h-4 text-purple-600" />
                    <span>Admin Dashboard</span>
                  </button>
                  <div className="border-t border-gray-100 my-2"></div>
                </>
              )}

              {/* Company Settings - Story 5.7: Only show when admin for active company */}
              {companySettingsLink && (
                <button
                  onClick={() => {
                    navigate(companySettingsLink)
                    setIsOpen(false)
                  }}
                  className="w-full flex items-center gap-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                >
                  <Building2 className="w-4 h-4 text-gray-500" />
                  <span>Company Settings</span>
                </button>
              )}

              {/* Theme Settings */}
              <button
                onClick={handleThemeSettings}
                className="w-full flex items-center gap-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
              >
                <Palette className="w-4 h-4 text-gray-500" />
                <span>Theme Settings</span>
              </button>

              {/* Account Settings */}
              <button
                onClick={handleAccountSettings}
                className="w-full flex items-center gap-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
              >
                <Settings className="w-4 h-4 text-gray-500" />
                <span>Account Settings</span>
              </button>

              {/* Divider */}
              <div className="border-t border-gray-100 my-2"></div>

              {/* Logout */}
              <button
                onClick={handleLogout}
                className="w-full flex items-center gap-3 px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
              >
                <LogOut className="w-4 h-4" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Theme Settings Popup - Always rendered to prevent mount/unmount loops */}
      <ThemeSettingsPopup
        isOpen={showThemePopup}
        onClose={() => setShowThemePopup(false)}
      />

      {/* Account Settings Popup - Always rendered to prevent mount/unmount loops */}
      <AccountSettingsPopup
        isOpen={showAccountPopup}
        onClose={() => setShowAccountPopup(false)}
      />
    </>
  )
}
