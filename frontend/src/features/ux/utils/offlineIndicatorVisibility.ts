/** Paths where offline/queue UI would suggest the product is broken for anonymous visitors. */
const MARKETING_AND_LEGAL_PATHS = new Set(['/', '/privacy', '/terms'])

/** Public form renderer — offline queue may still matter for event capture without login. */
export function isPublicFormCaptureRoute(pathname: string): boolean {
  return /^\/forms\/[^/]+(\/preview)?$/.test(pathname)
}

export function shouldShowOfflineIndicator(pathname: string, isAuthenticated: boolean): boolean {
  if (MARKETING_AND_LEGAL_PATHS.has(pathname)) {
    return false
  }
  return isAuthenticated || isPublicFormCaptureRoute(pathname)
}
