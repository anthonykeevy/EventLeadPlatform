/**
 * Story 3.11 - Dynamic Submission (Public / Auth-free)
 *
 * Canonical endpoints (backend):
 * - POST /api/public/forms/{token}/submissions
 *   - Request: PublicFormSubmissionRequest
 *   - Response: PublicFormSubmissionResponse
 *
 * Notes:
 * - `token` is supplied via the URL path, not the request body.
 * - The IndexedDB outbox implementation (T04) persists `PublicOutboxItem` records.
 */
export type PublicSubmissionLinkType = 'PREVIEW' | 'PRODUCTION'

export type PublicAnswersByComponentId = Record<string, unknown>

export type PublicSubmissionContext = {
  clientDeviceId: string
  clientSessionId: string
  submitAttemptId: string
  clientTimezone?: string
  clientLocale?: string
  clientUserAgent?: string
  clientScreen?: { width: number; height: number; dpr?: number }
  clientViewport?: { width: number; height: number }
  renderCanvasWidth?: number
  renderCanvasHeight?: number
  renderScaleAtSubmit?: number
  appVersion?: string
  buildSha?: string
}

export type PublicFormSubmissionRequest = {
  idempotencyKey: string
  submittedAtClient: string // ISO
  answersByComponentId: PublicAnswersByComponentId
  context: PublicSubmissionContext
}

export type PublicFormSubmissionResponse = {
  submissionId: number | string
  status: 'ACCEPTED' | 'DUPLICATE'
}

export type PublicOutboxStatus = 'pending' | 'uploading' | 'failed' | 'success'

/**
 * The IndexedDB outbox record stored client-side (T04).
 * This contract exists so the renderer submit flow (T05) can enqueue deterministically.
 */
export type PublicOutboxItem = {
  outboxItemId: string // client UUID
  token: string
  linkType?: PublicSubmissionLinkType
  request: PublicFormSubmissionRequest
  status: PublicOutboxStatus
  retryCount: number
  lastError?: string
  createdAt: number
  lastTriedAt?: number
}

