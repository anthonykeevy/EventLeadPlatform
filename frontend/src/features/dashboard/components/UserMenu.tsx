/**
 * User Menu Component for Dashboard
 * Provides user settings and theme customization access
 */

import React, { useState, useRef, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { User as UserIcon, LogOut, Settings, Palette, ChevronDown } from 'lucide-react'
import { useAuth } from '../../auth'
import { ThemeSettingsPopup } from './ThemeSettingsPopup'

interface UserMenuProps {
  user: {
    first_name: string
    last_name: string
    email: string
  }
}

export function UserMenu({ user }: UserMenuProps) {
  const { logout } = useAuth()
  const navigate = useNavigate()
  const [isOpen, setIsOpen] = useState(false)
  const [showThemePopup, setShowThemePopup] = useState(false)
  const menuRef = useRef<HTMLDivElement>(null)

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
                onClick={() => {
                  // TODO: Navigate to account settings
                  setIsOpen(false)
                }}
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
    </>
  )
}
