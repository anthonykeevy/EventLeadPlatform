import { useLocation } from 'react-router-dom'
import { useAuth } from '../../auth'
import { OfflineIndicator } from './OfflineIndicator'
import { shouldShowOfflineIndicator } from '../utils/offlineIndicatorVisibility'

/**
 * Offline badge only where it helps: authenticated app and public form capture.
 * Hidden on marketing/legal and other pre-auth surfaces so a down API does not
 * look like a broken landing page.
 */
export function AppOfflineIndicator() {
  const { pathname } = useLocation()
  const { isAuthenticated } = useAuth()

  if (!shouldShowOfflineIndicator(pathname, isAuthenticated)) {
    return null
  }

  return <OfflineIndicator />
}
