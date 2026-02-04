import type { PublicSubmissionLinkType } from './publicSubmission.types'
import type { ValueDiagnostics } from '../utils/valueDiagnostics'

/**
 * Story 3.11 - Validation telemetry (privacy-safe).
 *
 * Canonical endpoint (backend):
 * - POST /api/public/forms/{token}/telemetry/validation
 *   - Request: PublicValidationEventRequest
 *   - Response: 204 No Content (or minimal ACK)
 *
 * Notes:
 * - `token` is supplied via the URL path, not the request body.
 * - Raw field values MUST NOT be included; use `valueDiagnostics` only.
 * - Storage/ingest wiring is handled in T07 (this file is contract-only).
 */

export type PublicValidationEventType = 'validation_failed_submit'

export type PublicValidationErrorCategory =
  | 'required'
  | 'min'
  | 'max'
  | 'pattern'
  | 'range'
  | 'custom'
  | 'unknown'

export type PublicValidationFailure = {
  componentId: string
  componentType: string
  ruleId?: string
  ruleType?: string
  ruleCode?: string
  errorCategory?: PublicValidationErrorCategory
  valueDiagnostics?: ValueDiagnostics
}

export type PublicValidationEventRequest = {
  eventType: PublicValidationEventType
  occurredAtClient: string // ISO
  linkType?: PublicSubmissionLinkType
  clientDeviceId: string
  clientSessionId: string
  submitAttemptId: string
  failures: PublicValidationFailure[]
}

