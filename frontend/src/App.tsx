import { useEffect, useState, Suspense, lazy } from 'react'
import { Routes, Route, Link, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { AuthProvider } from './features/auth'
import { UXProvider, LoadingSpinner, PageLoadingSpinner, useToastNotifications } from './features/ux'
import { OfflineIndicator } from './features/ux/components/OfflineIndicator'
import { ThemeProvider } from './features/theme'
import { unsavedWorkTracker } from './utils/unsavedWorkTracker'
import { offlineQueue } from './utils/offlineQueue'
import { getApiBaseUrl } from './lib/apiBaseUrl'

// Create QueryClient instance for TanStack Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
})

// Lazy load components for better performance
const SignupForm = lazy(() => import('./features/auth').then(module => ({ default: module.SignupForm })))
const EmailVerification = lazy(() => import('./features/auth').then(module => ({ default: module.EmailVerification })))
const LoginForm = lazy(() => import('./features/auth').then(module => ({ default: module.LoginForm })))
const PasswordResetRequest = lazy(() => import('./features/auth').then(module => ({ default: module.PasswordResetRequest })))
const PasswordResetConfirm = lazy(() => import('./features/auth').then(module => ({ default: module.PasswordResetConfirm })))
const DashboardPage = lazy(() => import('./features/dashboard').then(module => ({ default: module.DashboardPage })))
const FormBrandingDefaultsPage = lazy(() => import('./features/dashboard').then(module => ({ default: module.FormBrandingDefaultsPage })))
const CompanySettingsLayout = lazy(() => import('./features/dashboard').then(module => ({ default: module.CompanySettingsLayout })))
const CompanyDetailsPage = lazy(() => import('./features/dashboard').then(module => ({ default: module.CompanyDetailsPage })))
const FormApprovalWorkflowPage = lazy(() => import('./features/dashboard').then(module => ({ default: module.FormApprovalWorkflowPage })))
const AssetsImagesPage = lazy(() => import('./features/dashboard').then(module => ({ default: module.AssetsImagesPage })))
const AssetsTermsPage = lazy(() => import('./features/dashboard').then(module => ({ default: module.AssetsTermsPage })))
const AssetsDocumentsPage = lazy(() => import('./features/dashboard').then(module => ({ default: module.AssetsDocumentsPage })))
const AssetsVideoPage = lazy(() => import('./features/dashboard').then(module => ({ default: module.AssetsVideoPage })))
const CompanyImagesPage = lazy(() => import('./features/dashboard').then(module => ({ default: module.CompanyImagesPage })))
const CompanyTeamPage = lazy(() => import('./features/dashboard').then(module => ({ default: module.CompanyTeamPage })))
const InvitationAcceptancePage = lazy(() => import('./features/invitations').then(module => ({ default: module.InvitationAcceptancePage })))
const AdminDashboard = lazy(() => import('./features/admin/pages/AdminDashboard').then(module => ({ default: module.AdminDashboard })))
const ExternalApprovalPage = lazy(() => import('./features/forms/pages/ExternalApprovalPage').then(module => ({ default: module.ExternalApprovalPage })))
const BuilderPage = lazy(() => import('./features/builder/pages/BuilderPage').then(module => ({ default: module.BuilderPage })))
const FormReviewPage = lazy(() => import('./features/forms/pages/FormReviewPage').then(module => ({ default: module.FormReviewPage })))
const FormRendererPage = lazy(() => import('./features/renderer/pages/FormRendererPage').then(module => ({ default: module.FormRendererPage })))
const PublicFormRendererPage = lazy(() => import('./features/renderer/pages/PublicFormRendererPage').then(module => ({ default: module.PublicFormRendererPage })))
const PublicFormPreviewShellPage = lazy(() => import('./features/renderer/pages/PublicFormPreviewShellPage').then(module => ({ default: module.PublicFormPreviewShellPage })))
import { RequireAuth } from './features/auth/components/RequireAuth'
// Forms are now integrated into the dashboard (Company → Event → Form hierarchy)
// Theme settings now accessible through user menu in dashboard

// Make utilities available globally for testing in browser console
if (typeof window !== 'undefined') {
  window.unsavedWorkTracker = unsavedWorkTracker;
  window.offlineQueue = offlineQueue;
}

interface HealthStatus {
  status: string
  service: string
  environment: string
}

function HomePage() {
  const [apiStatus, setApiStatus] = useState<'loading' | 'connected' | 'error'>('loading')
  const [healthData, setHealthData] = useState<HealthStatus | null>(null)
  const toast = useToastNotifications()

  useEffect(() => {
    // Test API connection
    fetch(`${getApiBaseUrl()}/api/health`)
      .then(res => res.json())
      .then(data => {
        setHealthData(data)
        setApiStatus('connected')
        toast.success('Backend API connected successfully!')
      })
      .catch(err => {
        console.error('API connection failed:', err)
        setApiStatus('error')
        toast.error('Failed to connect to backend API. Please start the backend server.')
      })
  }, []) // Remove toast dependency to prevent continuous re-runs

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-8">
      <main className="max-w-2xl w-full bg-white rounded-lg shadow-lg p-8 card-interactive" role="main">
        <header className="text-center mb-8 animate-fade-in">
          <h1 className="text-5xl font-bold text-teal-600 mb-2">
            EventLead Platform
          </h1>
          <p className="text-gray-500 text-lg">
            Multi-Tenant Event Lead Collection Platform
          </p>
        </header>

        <section className="space-y-4" aria-label="Platform status and navigation">
          {/* Environment Status */}
          <section className="bg-green-50 border border-green-200 rounded-lg p-4 card-lift" aria-labelledby="env-status">
            <h2 id="env-status" className="font-semibold text-green-900 mb-2 flex items-center">
              <span className="mr-2" aria-hidden="true">✅</span>
              Development Environment Ready
            </h2>
            <ul className="text-sm text-green-700 space-y-1" role="list">
              <li>• Python 3.13.3 installed</li>
              <li>• Node.js 22.17.1 installed</li>
              <li>• SQL Server 2022 running</li>
              <li>• Docker 28.4.0 installed</li>
              <li>• Frontend dependencies installed (511 packages)</li>
              <li>• Backend dependencies installed</li>
            </ul>
          </section>

          {/* API Connection Status */}
          <section className={`border rounded-lg p-4 card-lift ${
            apiStatus === 'connected' ? 'bg-green-50 border-green-200' :
            apiStatus === 'error' ? 'bg-red-50 border-red-200' :
            'bg-blue-50 border-blue-200'
          }`} aria-labelledby="api-status">
            <h2 id="api-status" className="font-semibold mb-2 flex items-center">
              {apiStatus === 'connected' && (
                <span className="mr-2 text-green-900 flex items-center">
                  <span className="mr-2" aria-hidden="true">✅</span>
                  Backend API Connected
                </span>
              )}
              {apiStatus === 'error' && (
                <span className="mr-2 text-red-900 flex items-center">
                  <span className="mr-2" aria-hidden="true">❌</span>
                  Backend API Not Running
                </span>
              )}
              {apiStatus === 'loading' && (
                <span className="mr-2 text-blue-900 flex items-center">
                  <LoadingSpinner size="sm" className="mr-2" aria-label="Loading" />
                  Connecting to API...
                </span>
              )}
            </h2>
            
            {healthData && (
              <div className="text-sm text-green-700" role="status" aria-live="polite">
                <p>• Service: {healthData.service}</p>
                <p>• Status: {healthData.status}</p>
                <p>• Environment: {healthData.environment}</p>
              </div>
            )}
            
            {apiStatus === 'error' && (
              <div className="text-sm text-red-700" role="alert" aria-live="assertive">
                <p>Backend not running. Start it with:</p>
                <code className="block bg-red-100 px-2 py-1 rounded mt-2" aria-label="Command to start backend">
                  cd backend && python main.py
                </code>
              </div>
            )}
          </section>

          {/* Authentication Links - Story 1.1 */}
          <nav className="bg-blue-50 border border-blue-200 rounded-lg p-4 card-lift" aria-labelledby="auth-nav">
            <h2 id="auth-nav" className="font-semibold text-blue-900 mb-3">
              <span className="mr-2" aria-hidden="true">🔐</span>
              Story 1.1: User Signup & Email Verification
            </h2>
            <div className="space-y-2" role="group" aria-label="Authentication options">
              <Link 
                to="/signup" 
                className="btn-primary block w-full text-center"
                aria-describedby="auth-nav"
              >
                Sign Up
              </Link>
              <Link 
                to="/login" 
                className="btn-secondary block w-full text-center"
                aria-describedby="auth-nav"
              >
                Log In
              </Link>
            </div>
          </nav>

          {/* Theme System - Story 2.2 */}
          <nav className="bg-purple-50 border border-purple-200 rounded-lg p-4 card-lift" aria-labelledby="theme-nav">
            <h2 id="theme-nav" className="font-semibold text-purple-900 mb-3">
              <span className="mr-2" aria-hidden="true">🎨</span>
              Story 2.2: Theme System Implementation
            </h2>
            <div className="space-y-2" role="group" aria-label="Theme options">
              <Link 
                to="/dashboard" 
                className="btn-primary block w-full text-center"
                aria-describedby="theme-nav"
              >
                Access Dashboard
              </Link>
              <p className="text-sm text-purple-700 text-center">
                Theme settings are available in the user menu after login
              </p>
            </div>
          </nav>

          {/* Useful Links */}
          <nav className="bg-gray-50 border border-gray-200 rounded-lg p-4 card-lift" aria-labelledby="useful-links">
            <h2 id="useful-links" className="font-semibold text-gray-900 mb-2">
              <span className="mr-2" aria-hidden="true">🔗</span>
              Useful Links
            </h2>
            <ul className="text-sm text-gray-700 space-y-1" role="list">
              <li>
                <a 
                  href={`${getApiBaseUrl()}/docs`} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-teal-600 hover:underline link-color"
                  aria-label="API Documentation (opens in new tab)"
                >
                  API Docs (Swagger UI)
                </a>
              </li>
              <li>
                <a 
                  href={`${getApiBaseUrl()}/api/test-database`} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-teal-600 hover:underline link-color"
                  aria-label="Database Connection Test (opens in new tab)"
                >
                  Database Connection Test
                </a>
              </li>
              <li>
                <a 
                  href="http://localhost:8025" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-teal-600 hover:underline link-color"
                  aria-label="MailHog Email Testing (opens in new tab)"
                >
                  MailHog (Email Testing)
                </a>
              </li>
            </ul>
          </nav>
        </section>

        <footer className="mt-8 text-center text-sm text-gray-500" role="contentinfo">
          <p>Built with React 18.2.0 + FastAPI 0.115.7 + SQL Server 2022</p>
          <p className="mt-1">Architecture: Modular Monolith | Repository: Monorepo</p>
        </footer>
      </main>
    </div>
  )
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <ThemeProvider>
          <UXProvider>
            <OfflineIndicator />
            <Suspense fallback={<PageLoadingSpinner message="Loading page..." />}>
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/signup" element={<SignupForm />} />
                <Route path="/login" element={<LoginForm />} />
                <Route path="/verify-email" element={<EmailVerification />} />
                <Route path="/reset-password" element={<PasswordResetRequest />} />
                <Route path="/reset-password/confirm" element={<PasswordResetConfirm />} />
                <Route path="/invitations/accept" element={<InvitationAcceptancePage />} />
                <Route path="/approval/external/:token" element={<ExternalApprovalPage />} />
                <Route path="/dashboard" element={<DashboardPage />} />
                <Route
                  path="/dashboard/companies/:companyId/settings"
                  element={
                    <RequireAuth>
                      <Suspense fallback={<PageLoadingSpinner />}>
                        <CompanySettingsLayout />
                      </Suspense>
                    </RequireAuth>
                  }
                >
                  <Route index element={<Navigate to="company-details" replace />} />
                  <Route path="company-details" element={<CompanyDetailsPage />} />
                  <Route path="form-approval-workflow" element={<FormApprovalWorkflowPage />} />
                  <Route path="form-branding-defaults" element={<FormBrandingDefaultsPage />} />
                  <Route path="assets/images" element={<AssetsImagesPage />} />
                  <Route path="assets/terms" element={<AssetsTermsPage />} />
                  <Route path="assets/documents" element={<AssetsDocumentsPage />} />
                  <Route path="assets/video" element={<AssetsVideoPage />} />
                  <Route path="images" element={<CompanyImagesPage />} />
                  <Route path="team" element={<CompanyTeamPage />} />
                </Route>
                <Route
                  path="/admin/dashboard"
                  element={
                    <RequireAuth>
                      <Suspense fallback={<PageLoadingSpinner />}>
                        <AdminDashboard />
                      </Suspense>
                    </RequireAuth>
                  }
                />
                <Route
                  path="/forms/:formId/review"
                  element={
                    <RequireAuth>
                      <Suspense fallback={<PageLoadingSpinner />}>
                        <FormReviewPage />
                      </Suspense>
                    </RequireAuth>
                  }
                />
                <Route
                  path="/forms/:formId/builder"
                  element={
                    <RequireAuth>
                      <Suspense fallback={<PageLoadingSpinner />}>
                        <BuilderPage />
                      </Suspense>
                    </RequireAuth>
                  }
                />
                <Route
                  path="/builder"
                  element={
                    <RequireAuth>
                      <Suspense fallback={<PageLoadingSpinner />}>
                        <BuilderPage />
                      </Suspense>
                    </RequireAuth>
                  }
                />
                <Route
                  path="/forms/:formId/render"
                  element={
                    <RequireAuth>
                      <Suspense fallback={<PageLoadingSpinner />}>
                        <FormRendererPage />
                      </Suspense>
                    </RequireAuth>
                  }
                />
                <Route
                  path="/forms/:token"
                  element={
                    <Suspense fallback={<PageLoadingSpinner />}>
                      <PublicFormRendererPage />
                    </Suspense>
                  }
                />
                <Route
                  path="/forms/:token/preview"
                  element={
                    <Suspense fallback={<PageLoadingSpinner />}>
                      <PublicFormPreviewShellPage />
                    </Suspense>
                  }
                />
                {/* Forms are now integrated into the dashboard (Company → Event → Form hierarchy) */}
                {/* Theme settings now accessible through user menu in dashboard */}
              </Routes>
            </Suspense>
          </UXProvider>
        </ThemeProvider>
      </AuthProvider>
    </QueryClientProvider>
  )
}

export default App

