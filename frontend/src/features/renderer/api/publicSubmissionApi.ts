import type {
  PublicFormSubmissionRequest,
  PublicFormSubmissionResponse,
} from '../types/publicSubmission.types'
import type { PublicValidationEventRequest } from '../types/telemetry.types'
import { getApiBaseUrl } from '../../../lib/apiBaseUrl'

function publicFormsBaseUrl(): string {
  const prefix = getApiBaseUrl().replace(/\/$/, '')
  return `${prefix}/api/public/forms`
}

export interface PublicUrlDnsValidationResponse {
  isValid: boolean
  normalizedUrl?: string
  hostname?: string
  reason?: string
}

export async function submitPublicFormSubmission(
  token: string,
  request: PublicFormSubmissionRequest,
  init?: RequestInit,
): Promise<PublicFormSubmissionResponse> {
  if (!token) {
    throw new Error('Public submission token is required.')
  }

  const response = await fetch(`${publicFormsBaseUrl()}/${token}/submissions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
    ...init,
  })

  if (!response.ok) {
    throw new Error(`Public submission failed (${response.status}).`)
  }

  return (await response.json()) as PublicFormSubmissionResponse
}

export async function submitPublicValidationTelemetry(
  token: string,
  request: PublicValidationEventRequest,
  init?: RequestInit,
): Promise<void> {
  if (!token) {
    throw new Error('Public submission token is required.')
  }

  const response = await fetch(`${publicFormsBaseUrl()}/${token}/telemetry/validation`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
    ...init,
  })

  if (!response.ok) {
    throw new Error(`Validation telemetry failed (${response.status}).`)
  }
}

export interface PublicAttachmentUploadResponse {
  attachmentId: string
  duplicateOfExisting?: boolean
}

export async function uploadPublicFormAttachment(
  token: string,
  params: { file: File; componentId: string; clientSessionId: string },
  init?: RequestInit,
): Promise<PublicAttachmentUploadResponse> {
  if (!token) {
    throw new Error('Public form token is required.')
  }

  const formData = new FormData()
  formData.append('file', params.file)
  formData.append('componentId', params.componentId)
  formData.append('clientSessionId', params.clientSessionId)

  const response = await fetch(`${publicFormsBaseUrl()}/${token}/attachments`, {
    method: 'POST',
    body: formData,
    ...init,
  })

  if (!response.ok) {
    throw new Error(`Attachment upload failed (${response.status}).`)
  }

  return (await response.json()) as PublicAttachmentUploadResponse
}

export async function validatePublicUrlDns(
  token: string,
  url: string,
  init?: RequestInit,
): Promise<PublicUrlDnsValidationResponse> {
  if (!token) {
    throw new Error('Public submission token is required.')
  }

  const response = await fetch(`${publicFormsBaseUrl()}/${token}/validate-url-dns`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ url, checkDns: true }),
    ...init,
  })

  if (!response.ok) {
    throw new Error(`URL DNS validation failed (${response.status}).`)
  }

  return (await response.json()) as PublicUrlDnsValidationResponse
}
