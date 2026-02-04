import type {
  PublicFormSubmissionRequest,
  PublicFormSubmissionResponse,
} from '../types/publicSubmission.types'

const PUBLIC_SUBMISSION_ENDPOINT = '/api/public/forms'

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
