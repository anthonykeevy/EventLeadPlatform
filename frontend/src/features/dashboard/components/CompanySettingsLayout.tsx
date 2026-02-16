/**
 * Company Settings Layout - Story 5.2 T04
 * Shared layout for Company Settings pages with nav menu
 */

import { NavLink, Outlet, useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Palette, Image, Users, Settings } from 'lucide-react'

const NAV_ITEMS = [
  { path: 'form-branding-defaults', label: 'Form Branding', icon: Palette },
  { path: 'images', label: 'Company Images', icon: Image },
  { path: 'team', label: 'User Management', icon: Users },
] as const

export function CompanySettingsLayout() {
  const { companyId } = useParams<{ companyId: string }>()
  const navigate = useNavigate()
  const base = `/dashboard/companies/${companyId}/settings`

  return (
    <div className="h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <div className="flex-shrink-0 flex items-center gap-4 px-4 py-3 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
        <button
          onClick={() => navigate('/dashboard')}
          className="p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-400"
          aria-label="Back to Dashboard"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>
        <div className="flex items-center gap-2">
          <Settings className="w-5 h-5 text-teal-500" />
          <h1 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
            Company Settings
          </h1>
        </div>
      </div>

      <div className="flex-1 flex overflow-hidden">
        {/* Left nav menu */}
        <nav className="w-52 flex-shrink-0 border-r border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 py-4">
          <ul className="space-y-0.5 px-2">
            {NAV_ITEMS.map(({ path, label, icon: Icon }) => (
              <li key={path}>
                <NavLink
                  to={`${base}/${path}`}
                  className={({ isActive }) =>
                    `flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      isActive
                        ? 'bg-teal-50 dark:bg-teal-900/20 text-teal-700 dark:text-teal-300'
                        : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
                    }`
                  }
                >
                  <Icon className="w-4 h-4 flex-shrink-0" />
                  {label}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>

        {/* Content */}
        <main className="flex-1 overflow-hidden">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
