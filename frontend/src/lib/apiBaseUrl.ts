/**
 * Shared API base URL for frontend HTTP clients.
 *
 * Priority:
 * 1. VITE_API_BASE_URL — explicit origin when the SPA and API live on different
 *    hostnames (e.g. CDN + separate API subdomain).
 * 2. Empty string — same-origin requests (`/api/...`). Matches production where the
 *    SPA is bundled into the FastAPI app, and matches local `vite` dev (`server.proxy`)
 *    which forwards `/api` to the backend.
 */
export function getApiBaseUrl(): string {
  const raw = import.meta.env.VITE_API_BASE_URL
  const explicit = typeof raw === 'string' && raw.trim().length > 0 ? raw.trim() : ''
  if (explicit) {
    return explicit.replace(/\/$/, '')
  }
  return ''
}
