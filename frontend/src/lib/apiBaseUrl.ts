/**
 * Shared API base URL for frontend requests.
 * Uses VITE_API_BASE_URL env var with fallback for local dev.
 */
export function getApiBaseUrl(): string {
  const base = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
  return base.replace(/\/$/, '');
}
