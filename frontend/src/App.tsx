import { useEffect, Suspense, lazy } from 'react'
import { Routes, Route, Navigate, useLocation, useNavigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { AuthProvider } from './features/auth'
import { UXProvider, PageLoadingSpinner } from './features/ux'
import { AppOfflineIndicator } from './features/ux/components/AppOfflineIndicator'
import { ThemeProvider } from './features/theme'
import { unsavedWorkTracker } from './utils/unsavedWorkTracker'
import { offlineQueue } from './utils/offlineQueue'

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
const BetaLandingPage = lazy(() => import('./features/marketing').then(module => ({ default: module.BetaLandingPage })))
const PrivacyPolicyPage = lazy(() => import('./features/legal').then(module => ({ default: module.PrivacyPolicyPage })))
const TermsOfUsePage = lazy(() => import('./features/legal').then(module => ({ default: module.TermsOfUsePage })))
import { RequireAuth } from './features/auth/components/RequireAuth'
// Forms are now integrated into the dashboard (Company → Event → Form hierarchy)
// Theme settings now accessible through user menu in dashboard

// Make utilities available globally for testing in browser console
if (typeof window !== 'undefined') {
  window.unsavedWorkTracker = unsavedWorkTracker;
  window.offlineQueue = offlineQueue;
}

/**
 * Collapse duplicate leading slashes and duplicate segments (e.g. //reset-password/confirm from
 * FRONTEND_URL with trailing slash + email template path). React Router won't match those URLs.
 */
function NormalizeBrowserPathname() {
  const location = useLocation()
  const navigate = useNavigate()

  useEffect(() => {
    const segments = location.pathname.split('/').filter(Boolean)
    const normalized = segments.length === 0 ? '/' : `/${segments.join('/')}`
    if (normalized !== location.pathname) {
      navigate(
        { pathname: normalized, search: location.search, hash: location.hash },
        { replace: true },
      )
    }
  }, [location.pathname, location.search, location.hash, navigate])

  return null
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <ThemeProvider>
          <UXProvider>
            <AppOfflineIndicator />
            <NormalizeBrowserPathname />
            <Suspense fallback={<PageLoadingSpinner message="Loading page..." />}>
              <Routes>
                <Route path="/" element={<BetaLandingPage />} />
                <Route path="/privacy" element={<PrivacyPolicyPage />} />
                <Route path="/terms" element={<TermsOfUsePage />} />
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

