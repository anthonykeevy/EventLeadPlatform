/**
 * Cross-tab refresh coordination (Phase 1).
 * - Single in-flight refresh per browser profile
 * - localStorage lock so only one tab calls POST /api/auth/refresh
 * - Leader election for proactive refresh timers
 */

import type { TokenResponse } from '../types/auth.types'
import {
  ACCESS_TOKEN_KEY,
  getStoredTokens,
  REFRESH_TOKEN_KEY,
  TOKEN_EXPIRY_KEY,
} from './tokenStorage'

const REFRESH_LOCK_KEY = 'eventlead_refresh_lock'
const LEADER_TAB_KEY = 'eventlead_auth_leader'
const LEADER_HEARTBEAT_KEY = 'eventlead_auth_leader_heartbeat'
const TAB_ID_SESSION_KEY = 'eventlead_tab_id'

const REFRESH_LOCK_TTL_MS = 30_000
const LEADER_HEARTBEAT_TTL_MS = 15_000
export const LEADER_HEARTBEAT_INTERVAL_MS = 5_000
const WAIT_FOR_REFRESH_MS = 15_000
const WAIT_POLL_MS = 100

type RefreshLock = { tabId: string; since: number }

let inFlightRefresh: Promise<TokenResponse> | null = null
let cachedTabId: string | null = null

function getTabId(): string {
  if (typeof window === 'undefined') {
    if (!cachedTabId) {
      cachedTabId = 'ssr'
    }
    return cachedTabId
  }
  const stored = sessionStorage.getItem(TAB_ID_SESSION_KEY)
  if (stored) {
    cachedTabId = stored
    return stored
  }
  if (cachedTabId) {
    return cachedTabId
  }
  const tabId =
    typeof crypto !== 'undefined' && crypto.randomUUID
      ? crypto.randomUUID()
      : `tab-${Date.now()}-${Math.random().toString(36).slice(2)}`
  sessionStorage.setItem(TAB_ID_SESSION_KEY, tabId)
  cachedTabId = tabId
  return tabId
}

function readRefreshLock(): RefreshLock | null {
  try {
    const raw = localStorage.getItem(REFRESH_LOCK_KEY)
    if (!raw) return null
    const parsed = JSON.parse(raw) as RefreshLock
    if (!parsed?.tabId || typeof parsed.since !== 'number') return null
    return parsed
  } catch {
    return null
  }
}

function isLockHeldByOtherTab(lock: RefreshLock | null): boolean {
  if (!lock) return false
  const tabId = getTabId()
  if (lock.tabId === tabId) return false
  return Date.now() - lock.since < REFRESH_LOCK_TTL_MS
}

export function tryAcquireRefreshLock(): boolean {
  if (typeof window === 'undefined') return true
  const tabId = getTabId()
  const existing = readRefreshLock()
  if (isLockHeldByOtherTab(existing)) {
    return false
  }
  const next: RefreshLock = { tabId, since: Date.now() }
  localStorage.setItem(REFRESH_LOCK_KEY, JSON.stringify(next))
  const verify = readRefreshLock()
  return verify?.tabId === tabId
}

export function releaseRefreshLock(): void {
  if (typeof window === 'undefined') return
  const lock = readRefreshLock()
  if (lock?.tabId === getTabId()) {
    localStorage.removeItem(REFRESH_LOCK_KEY)
  }
}

function tokensToResponse(tokens: NonNullable<ReturnType<typeof getStoredTokens>>): TokenResponse {
  const currentTime = Math.floor(Date.now() / 1000)
  const expiresIn = Math.max(0, tokens.expiresAt - currentTime)
  return {
    access_token: tokens.accessToken,
    refresh_token: tokens.refreshToken,
    token_type: 'bearer',
    expires_in: expiresIn || 900,
  }
}

function waitForRefreshedTokens(): Promise<TokenResponse> {
  return new Promise((resolve, reject) => {
    if (typeof window === 'undefined') {
      reject(new Error('Refresh wait unavailable'))
      return
    }

    const tryResolve = () => {
      const tokens = getStoredTokens()
      if (tokens && !isAccessTokenStale(tokens.expiresAt)) {
        cleanup()
        resolve(tokensToResponse(tokens))
        return true
      }
      return false
    }

    const cleanup = () => {
      window.clearTimeout(timeoutId)
      window.clearInterval(pollId)
      window.removeEventListener('storage', onStorage)
      window.removeEventListener('eventlead:tokens-updated', onTokensUpdated as EventListener)
    }

    const onStorage = (event: StorageEvent) => {
      if (
        event.key === ACCESS_TOKEN_KEY ||
        event.key === REFRESH_TOKEN_KEY ||
        event.key === TOKEN_EXPIRY_KEY ||
        event.key === null
      ) {
        tryResolve()
      }
    }

    const onTokensUpdated = () => {
      tryResolve()
    }

    if (tryResolve()) {
      return
    }

    window.addEventListener('storage', onStorage)
    window.addEventListener('eventlead:tokens-updated', onTokensUpdated as EventListener)

    const pollId = window.setInterval(() => {
      if (!readRefreshLock() || !isLockHeldByOtherTab(readRefreshLock())) {
        tryResolve()
      }
    }, WAIT_POLL_MS)

    const timeoutId = window.setTimeout(() => {
      cleanup()
      reject(new Error('Timed out waiting for token refresh in another tab'))
    }, WAIT_FOR_REFRESH_MS)
  })
}

function isAccessTokenStale(expiresAt: number, bufferSeconds = 5): boolean {
  const now = Math.floor(Date.now() / 1000)
  return now >= expiresAt - bufferSeconds
}

/**
 * Run refresh HTTP at most once per profile; other tabs wait for updated tokens.
 */
export async function coordinatedRefreshAccessToken(
  executeRefresh: () => Promise<TokenResponse>
): Promise<TokenResponse> {
  if (inFlightRefresh) {
    return inFlightRefresh
  }

  if (!tryAcquireRefreshLock()) {
    return waitForRefreshedTokens()
  }

  inFlightRefresh = executeRefresh()
    .then((result) => result)
    .catch((error) => {
      throw error
    })
    .finally(() => {
      releaseRefreshLock()
      inFlightRefresh = null
    })

  return inFlightRefresh
}

export function tryClaimAuthRefreshLeader(): boolean {
  if (typeof window === 'undefined') return false
  const tabId = getTabId()
  const now = Date.now()
  const leader = localStorage.getItem(LEADER_TAB_KEY)
  const heartbeat = Number(localStorage.getItem(LEADER_HEARTBEAT_KEY) || '0')
  const leaderStale = !leader || now - heartbeat > LEADER_HEARTBEAT_TTL_MS

  if (leaderStale) {
    localStorage.setItem(LEADER_TAB_KEY, tabId)
    localStorage.setItem(LEADER_HEARTBEAT_KEY, String(now))
  }

  return localStorage.getItem(LEADER_TAB_KEY) === tabId
}

export function renewAuthRefreshLeaderHeartbeat(): void {
  if (typeof window === 'undefined') return
  if (localStorage.getItem(LEADER_TAB_KEY) === getTabId()) {
    localStorage.setItem(LEADER_HEARTBEAT_KEY, String(Date.now()))
  }
}

export function releaseAuthRefreshLeader(): void {
  if (typeof window === 'undefined') return
  if (localStorage.getItem(LEADER_TAB_KEY) === getTabId()) {
    localStorage.removeItem(LEADER_TAB_KEY)
    localStorage.removeItem(LEADER_HEARTBEAT_KEY)
  }
}

export function isAuthRefreshLeader(): boolean {
  if (typeof window === 'undefined') return false
  const tabId = getTabId()
  if (localStorage.getItem(LEADER_TAB_KEY) !== tabId) {
    return false
  }
  const heartbeat = Number(localStorage.getItem(LEADER_HEARTBEAT_KEY) || '0')
  return Date.now() - heartbeat <= LEADER_HEARTBEAT_TTL_MS
}

/** @internal test helpers */
export const __test__ = {
  getTabId,
  readRefreshLock,
  resetModuleState: () => {
    inFlightRefresh = null
    cachedTabId = null
  },
}
