import type { PublicOutboxItem } from '../types/publicSubmission.types'

const BASE_BACKOFF_MS = 2_000
const MAX_BACKOFF_MS = 5 * 60_000

export function getBackoffMs(retryCount: number): number {
  if (!Number.isFinite(retryCount) || retryCount <= 0) {
    return BASE_BACKOFF_MS
  }

  return Math.min(BASE_BACKOFF_MS * 2 ** retryCount, MAX_BACKOFF_MS)
}

export function shouldAttemptOutboxItem(
  nowMs: number,
  item: Pick<PublicOutboxItem, 'retryCount' | 'lastTriedAt'>,
): boolean {
  if (!item.lastTriedAt || !Number.isFinite(item.lastTriedAt)) {
    return true
  }

  const backoffMs = getBackoffMs(item.retryCount)
  return nowMs >= item.lastTriedAt + backoffMs
}
