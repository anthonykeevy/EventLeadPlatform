import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import {
  ACCESS_TOKEN_KEY,
  REFRESH_TOKEN_KEY,
  TOKEN_EXPIRY_KEY,
} from '../tokenStorage'
import {
  __test__,
  coordinatedRefreshAccessToken,
  isAuthRefreshLeader,
  releaseAuthRefreshLeader,
  tryAcquireRefreshLock,
  tryClaimAuthRefreshLeader,
  renewAuthRefreshLeaderHeartbeat,
} from '../refreshCoordinator'

describe('refreshCoordinator', () => {
  beforeEach(() => {
    localStorage.clear()
    sessionStorage.clear()
    __test__.resetModuleState()
  })

  afterEach(() => {
    releaseAuthRefreshLeader()
    localStorage.clear()
    sessionStorage.clear()
    __test__.resetModuleState()
  })

  it('allows only one tab to hold the refresh lock at a time', () => {
    const tabA = 'tab-a'
    const tabB = 'tab-b'
    sessionStorage.setItem('eventlead_tab_id', tabA)
    __test__.resetModuleState()
    expect(tryAcquireRefreshLock()).toBe(true)

    sessionStorage.setItem('eventlead_tab_id', tabB)
    __test__.resetModuleState()
    expect(tryAcquireRefreshLock()).toBe(false)
  })

  it('elects a single refresh leader with heartbeat', () => {
    sessionStorage.setItem('eventlead_tab_id', 'leader-tab')
    __test__.resetModuleState()
    expect(tryClaimAuthRefreshLeader()).toBe(true)
    renewAuthRefreshLeaderHeartbeat()
    expect(isAuthRefreshLeader()).toBe(true)
  })

  it('dedupes in-flight refresh within the same tab', async () => {
    const execute = vi.fn(async () => ({
      access_token: 'new-access',
      refresh_token: 'refresh',
      token_type: 'bearer',
      expires_in: 900,
    }))

    const [first, second] = await Promise.all([
      coordinatedRefreshAccessToken(execute),
      coordinatedRefreshAccessToken(execute),
    ])

    expect(execute).toHaveBeenCalledTimes(1)
    expect(first.access_token).toBe('new-access')
    expect(second.access_token).toBe('new-access')
  })

  it('waits for tokens updated by another tab when lock is held', async () => {
    sessionStorage.setItem('eventlead_tab_id', 'holder')
    __test__.resetModuleState()
    expect(tryAcquireRefreshLock()).toBe(true)

    sessionStorage.setItem('eventlead_tab_id', 'waiter')
    __test__.resetModuleState()
    const waitPromise = coordinatedRefreshAccessToken(async () => {
      throw new Error('should not call API while waiting')
    })

    const expiresAt = Math.floor(Date.now() / 1000) + 900
    localStorage.setItem(ACCESS_TOKEN_KEY, 'shared-access')
    localStorage.setItem(REFRESH_TOKEN_KEY, 'shared-refresh')
    localStorage.setItem(TOKEN_EXPIRY_KEY, String(expiresAt))
    window.dispatchEvent(
      new CustomEvent('eventlead:tokens-updated', {
        detail: {
          accessToken: 'shared-access',
          refreshToken: 'shared-refresh',
          expiresAt,
        },
      })
    )

    const result = await waitPromise
    expect(result.access_token).toBe('shared-access')
  })
})
