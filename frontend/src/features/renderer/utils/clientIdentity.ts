/**
 * Story 3.11 - Public renderer client identity.
 *
 * Rules (contract):
 * - `clientDeviceId` is a stable, random UUID persisted locally (NO fingerprinting).
 * - `clientSessionId` is a per-respondent/session UUID:
 *   - create on each page load
 *   - rotate on kiosk reset / "new submission" flows
 * - `submitAttemptId` is a UUID created per submit click (used to correlate validation failures).
 */

const CLIENT_DEVICE_ID_STORAGE_KEY = 'eventlead:public:clientDeviceId'

function safeGetLocalStorageItem(key: string): string | null {
  try {
    return typeof window === 'undefined' ? null : window.localStorage.getItem(key)
  } catch {
    return null
  }
}

function safeSetLocalStorageItem(key: string, value: string): void {
  try {
    if (typeof window !== 'undefined') {
      window.localStorage.setItem(key, value)
    }
  } catch {
    // Best-effort persistence only (some environments block storage).
  }
}

function generateUuidV4(): string {
  const cryptoObj = globalThis.crypto

  if (cryptoObj && typeof cryptoObj.randomUUID === 'function') {
    return cryptoObj.randomUUID()
  }

  if (cryptoObj && typeof cryptoObj.getRandomValues === 'function') {
    const bytes = new Uint8Array(16)
    cryptoObj.getRandomValues(bytes)

    // RFC 4122 v4
    bytes[6] = (bytes[6] & 0x0f) | 0x40
    bytes[8] = (bytes[8] & 0x3f) | 0x80

    const hex = Array.from(bytes, (b) => b.toString(16).padStart(2, '0')).join('')
    return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`
  }

  // Last resort: not cryptographically strong, but still non-identifying.
  return `fallback-${Math.random().toString(16).slice(2)}-${Date.now().toString(16)}`
}

export function getOrCreateClientDeviceId(): string {
  const existing = safeGetLocalStorageItem(CLIENT_DEVICE_ID_STORAGE_KEY)
  if (existing) return existing

  const created = generateUuidV4()
  safeSetLocalStorageItem(CLIENT_DEVICE_ID_STORAGE_KEY, created)
  return created
}

export function createNewClientSessionId(): string {
  // Contract: caller is responsible for rotating on page-load and kiosk reset boundaries.
  return generateUuidV4()
}

export function createSubmitAttemptId(): string {
  return generateUuidV4()
}

export function createIdempotencyKey(): string {
  return generateUuidV4()
}

