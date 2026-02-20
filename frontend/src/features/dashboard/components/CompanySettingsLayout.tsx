/**
 * Company Settings Layout - Story 5.2 T04, Story 5.7
 * Shared layout for Company Settings pages with nav menu.
 * PM decisions: Company Details | Form Approval Workflow | Form Branding | Assets (Images | Terms | Documents | Video)
 * Mobile (<768px): Hamburger + slide-over nav.
 * Assets: 2-level menu (like Form Branding) — parent "Assets" with nested Images, Terms, Documents, Video.
 */

import { useState, useEffect } from 'react'
import { NavLink, Outlet, useParams, useNavigate, useLocation } from 'react-router-dom'
import { ArrowLeft, Palette, Image, Users, Settings, Building2, GitBranch, FileText, Video, Menu, X, ChevronDown, ChevronRight, FolderOpen } from 'lucide-react'

const topNavItems: { path: string; label: string; icon: typeof Building2 }[] = [
  { path: 'company-details', label: 'Company Details', icon: Building2 },
  { path: 'form-approval-workflow', label: 'Form Approval Workflow', icon: GitBranch },
  { path: 'form-branding-defaults', label: 'Form Branding', icon: Palette },
  { path: 'team', label: 'User Management', icon: Users },
]

const assetSubItems: { path: string; label: string; icon: typeof Image }[] = [
  { path: 'assets/images', label: 'Images', icon: Image },
  { path: 'assets/terms', label: 'Terms', icon: FileText },
  { path: 'assets/documents', label: 'Documents', icon: FileText },
  { path: 'assets/video', label: 'Video', icon: Video },
]

export function CompanySettingsLayout() {
  const { companyId } = useParams<{ companyId: string }>()
  const navigate = useNavigate()
  const location = useLocation()
  const base = `/dashboard/companies/${companyId}/settings`
  const [mobileNavOpen, setMobileNavOpen] = useState(false)
  const [assetsExpanded, setAssetsExpanded] = useState(false)

  const pathname = location.pathname
  const isAssetsRoute = pathname.includes('/settings/assets/')

  useEffect(() => {
    if (isAssetsRoute) setAssetsExpanded(true)
  }, [isAssetsRoute])

  const renderNavLinks = () => (
    <>
      {topNavItems.slice(0, 3).map(({ path, label, icon: Icon }) => (
        <li key={path}>
          <NavLink
            to={`${base}/${path}`}
            onClick={() => setMobileNavOpen(false)}
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
      {/* Assets - 2-level expandable section */}
      <li>
        <button
          type="button"
          onClick={() => setAssetsExpanded((e) => !e)}
          className="flex w-full items-center gap-2 px-3 py-2 rounded-md text-sm font-medium text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800"
        >
          {assetsExpanded ? (
            <ChevronDown className="w-4 h-4 flex-shrink-0" />
          ) : (
            <ChevronRight className="w-4 h-4 flex-shrink-0" />
          )}
          <FolderOpen className="w-4 h-4 flex-shrink-0" />
          Assets
        </button>
        {assetsExpanded && (
          <ul className="mt-0.5 ml-4 pl-2 border-l border-gray-200 dark:border-gray-600 space-y-0.5">
            {assetSubItems.map(({ path, label, icon: Icon }) => (
              <li key={path}>
                <NavLink
                  to={`${base}/${path}`}
                  onClick={() => setMobileNavOpen(false)}
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
        )}
      </li>
      {topNavItems.slice(3).map(({ path, label, icon: Icon }) => (
        <li key={path}>
          <NavLink
            to={`${base}/${path}`}
            onClick={() => setMobileNavOpen(false)}
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
    </>
  )

  return (
    <div className="h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <div className="flex-shrink-0 flex items-center gap-4 px-4 py-3 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
        {/* Mobile hamburger - visible <768px */}
        <button
          onClick={() => setMobileNavOpen((o) => !o)}
          className="md:hidden p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-400"
          aria-label={mobileNavOpen ? 'Close menu' : 'Open menu'}
        >
          {mobileNavOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
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
        {/* Desktop sidebar - hidden on mobile */}
        <nav className="hidden md:block w-52 flex-shrink-0 border-r border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 py-4 overflow-y-auto">
          <ul className="space-y-0.5 px-2">
            {renderNavLinks()}
          </ul>
        </nav>

        {/* Mobile slide-over - visible when open */}
        {mobileNavOpen && (
          <>
            <div
              className="md:hidden fixed inset-0 bg-black/30 z-40"
              onClick={() => setMobileNavOpen(false)}
              aria-hidden="true"
            />
            <nav className="md:hidden fixed left-0 top-0 bottom-0 w-64 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 z-50 py-4 overflow-y-auto">
              <div className="flex items-center justify-between px-4 mb-4">
                <span className="font-semibold text-gray-900 dark:text-gray-100">Menu</span>
                <button onClick={() => setMobileNavOpen(false)} className="p-2">
                  <X className="w-5 h-5" />
                </button>
              </div>
              <ul className="space-y-0.5 px-2">
                {renderNavLinks()}
              </ul>
            </nav>
          </>
        )}

        {/* Content */}
        <main className="flex-1 overflow-hidden min-w-0">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
