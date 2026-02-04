import type {
  PublicFormSubmissionRequest,
  PublicFormSubmissionResponse,
} from '../types/publicSubmission.types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
const PUBLIC_SUBMISSION_ENDPOINT = `${API_BASE_URL.replace(/\/$/, '')}/api/public/forms`

export async function submitPublicFormSubmission(
  token: string,
  request: PublicFormSubmissionRequest,
  init?: RequestInit,
): Promise<PublicFormSubmissionResponse> {
  if (!token) {
    throw new Error('Public submission token is required.')
  }

  const response = await fetch(`${PUBLIC_SUBMISSION_ENDPOINT}/${token}/submissions`, {
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
