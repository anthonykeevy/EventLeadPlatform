/**
 * Route classification for multi-tab auth (Phase 1).
 * Preview/public form routes share tokens but should not drive session recovery.
 */

const PROTECTED_FORM_SUFFIX =
  /^\/forms\/[^/]+\/(builder|review|render)(?:\/|$)/

const PUBLIC_PREVIEW_SUFFIX = /^\/forms\/[^/]+\/preview\/?$/

const PUBLIC_FORM_TOKEN_ONLY = /^\/forms\/[^/]+\/?$/

/**
 * True for public preview/renderer routes (token-based URLs).
 * These tabs read shared localStorage but must not clear tokens on refresh failure.
 */
export function isPublicAuthPassiveRoute(pathname: string): boolean {
  if (PUBLIC_PREVIEW_SUFFIX.test(pathname)) {
    return true
  }
  if (PROTECTED_FORM_SUFFIX.test(pathname)) {
    return false
  }
  return PUBLIC_FORM_TOKEN_ONLY.test(pathname)
}

/**
 * Routes that may run proactive refresh scheduling and claim refresh leader.
 */
export function isActiveAuthRoute(pathname: string): boolean {
  return !isPublicAuthPassiveRoute(pathname)
}
