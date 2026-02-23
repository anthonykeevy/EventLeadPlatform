/**
 * Forms API Client for Epic 2 Story 2.8
 * Handles form header management API calls
 */

import {
  Form,
  FormStatus,
  FormApprovalStatus,
  FormCreateRequest,
  FormUpdateRequest,
  FormListResponse,
  CreateFormResponse,
  UpdateFormResponse,
  DeleteFormResponse,
  FormFilters
} from '../types/form.types'
import { apiClient, formatError } from '../../../lib/apiClient'

// =====================================================================
// Transformers: Backend to Frontend
// =====================================================================

function transformFormStatus(backend: any): FormStatus {
  return {
    formStatusId: backend.formStatusId ?? backend.form_status_id ?? backend.FormStatusID ?? 0,
    statusCode: backend.statusCode ?? backend.status_code ?? backend.StatusCode ?? '',
    statusName: backend.statusName ?? backend.status_name ?? backend.StatusName ?? '',
    statusDescription: backend.statusDescription ?? backend.status_description ?? backend.StatusDescription ?? null,
    statusColor: backend.statusColor ?? backend.status_color ?? backend.StatusColor ?? null,
    statusIcon: backend.statusIcon ?? backend.status_icon ?? backend.StatusIcon ?? null,
    isActive: backend.isActive ?? backend.is_active ?? backend.IsActive ?? true,
    sortOrder: backend.sortOrder ?? backend.sort_order ?? backend.SortOrder ?? 0,
  }
}

function transformFormApprovalStatus(backend: any): FormApprovalStatus {
  return {
    formApprovalStatusId: backend.formApprovalStatusId ?? backend.form_approval_status_id ?? backend.FormApprovalStatusID ?? 0,
    approvalStatusCode: backend.approvalStatusCode ?? backend.approval_status_code ?? backend.ApprovalStatusCode ?? '',
    approvalStatusName: backend.approvalStatusName ?? backend.approval_status_name ?? backend.ApprovalStatusName ?? '',
    approvalStatusDescription: backend.approvalStatusDescription ?? backend.approval_status_description ?? backend.ApprovalStatusDescription ?? null,
    isRequiresApproval: backend.isRequiresApproval ?? backend.is_requires_approval ?? backend.IsRequiresApproval ?? false,
    isActive: backend.isActive ?? backend.is_active ?? backend.IsActive ?? true,
    sortOrder: backend.sortOrder ?? backend.sort_order ?? backend.SortOrder ?? 0,
  }
}

function transformForm(backend: any): Form {
  return {
    formId: backend.form_id ?? backend.formId ?? backend.FormID ?? 0,
    formName: backend.form_name ?? backend.formName ?? backend.FormName ?? '',
    formDescription: backend.form_description ?? backend.formDescription ?? backend.FormDescription ?? null,
    companyId: backend.company_id ?? backend.companyId ?? backend.CompanyID ?? 0,
    eventId: backend.event_id ?? backend.eventId ?? backend.EventID ?? null,
    formStatusId: backend.form_status_id ?? backend.formStatusId ?? backend.FormStatusID ?? 0,
    formStatus: (backend.form_status ?? backend.formStatus ?? backend.FormStatus) 
      ? transformFormStatus(backend.form_status ?? backend.formStatus ?? backend.FormStatus) 
      : null,
    formApprovalStatusId: backend.form_approval_status_id ?? backend.formApprovalStatusId ?? backend.FormApprovalStatusID ?? 0,
    formApprovalStatus: (backend.form_approval_status ?? backend.formApprovalStatus ?? backend.FormApprovalStatus)
      ? transformFormApprovalStatus(backend.form_approval_status ?? backend.formApprovalStatus ?? backend.FormApprovalStatus)
      : null,
    isPublic: backend.is_public ?? backend.isPublic ?? backend.IsPublic ?? false,
    deploymentCost: (() => {
      const raw = backend.deployment_cost ?? backend.deploymentCost ?? backend.DeploymentCost
      if (raw == null || raw === '') return null
      const n = Number(raw)
      return Number.isNaN(n) ? null : n
    })(),
    totalSubmissions: backend.total_submissions ?? backend.totalSubmissions ?? backend.TotalSubmissions ?? 0,
    demoLeadsCollected: backend.demo_leads_collected ?? backend.demoLeadsCollected ?? backend.DemoLeadsCollected ?? 0,
    productionLeadsCollected: backend.production_leads_collected ?? backend.productionLeadsCollected ?? backend.ProductionLeadsCollected ?? 0,
    lastSubmissionDate: backend.last_submission_date ?? backend.lastSubmissionDate ?? backend.LastSubmissionDate ?? null,
    lastActivityDate: backend.last_activity_date ?? backend.lastActivityDate ?? backend.LastActivityDate ?? null,
    formThumbnailUrl: backend.form_thumbnail_url ?? backend.formThumbnailUrl ?? backend.FormThumbnailURL ?? null,
    formPreviewUrl: backend.form_preview_url ?? backend.formPreviewUrl ?? backend.FormPreviewURL ?? null,
    productionUrl: backend.production_url ?? backend.productionUrl ?? null,
    willUnpublishOn: backend.will_unpublish_on ?? backend.willUnpublishOn ?? null,
    unpublishMode: backend.unpublish_mode ?? backend.unpublishMode ?? null,
    scheduledUnpublishDate: backend.scheduled_unpublish_date ?? backend.scheduledUnpublishDate ?? null,
    createdDate: backend.created_date ?? backend.createdDate ?? backend.CreatedDate ?? '',
    createdBy: backend.created_by ?? backend.createdBy ?? backend.CreatedBy ?? 0,
    updatedDate: backend.updated_date ?? backend.updatedDate ?? backend.UpdatedDate ?? null,
    updatedBy: backend.updated_by ?? backend.updatedBy ?? backend.UpdatedBy ?? null,
  }
}

// =====================================================================
// API Functions
// =====================================================================

/**
 * Get all form statuses (reference data)
 */
export async function getFormStatuses(): Promise<FormStatus[]> {
  try {
    const response = await apiClient.get('/api/forms/statuses')
    return (response.data as any[]).map(transformFormStatus)
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Get all form approval statuses (reference data)
 */
export async function getFormApprovalStatuses(): Promise<FormApprovalStatus[]> {
  try {
    const response = await apiClient.get('/api/forms/approval-statuses')
    return (response.data as any[]).map(transformFormApprovalStatus)
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Get all forms for the company with optional filters
 */
export async function getForms(filters?: FormFilters, page: number = 1, pageSize: number = 20): Promise<FormListResponse> {
  try {
    const params: any = {
      page,
      page_size: pageSize,
    }
    
    if (filters?.formStatusId) {
      params.form_status_id = filters.formStatusId
    }
    if (filters?.eventId) {
      params.event_id = filters.eventId
    }
    if (filters?.search) {
      params.search = filters.search
    }
    
    const response = await apiClient.get('/api/forms', { params })
    return {
      forms: (response.data.forms ?? []).map(transformForm),
      total: response.data.total ?? 0,
      page: response.data.page ?? page,
      pageSize: response.data.page_size ?? response.data.pageSize ?? pageSize,
    }
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Get a single form by ID
 */
export async function getForm(formId: number): Promise<Form> {
  try {
    const response = await apiClient.get(`/api/forms/${formId}`)
    return transformForm(response.data)
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Create a new form
 */
export async function createForm(request: FormCreateRequest): Promise<CreateFormResponse> {
  try {
    const response = await apiClient.post('/api/forms', request)
    // Handle response structure: backend returns { success, message, formId, form }
    const formData = response.data.form || response.data
    if (!formData || !formData.formId) {
      throw new Error('Invalid response format: form data missing')
    }
    return {
      success: response.data.success ?? true,
      message: response.data.message ?? 'Form created successfully',
      formId: response.data.formId ?? response.data.form_id ?? formData.formId ?? 0,
      form: transformForm(formData),
    }
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Update an existing form
 */
export async function updateForm(formId: number, request: FormUpdateRequest): Promise<UpdateFormResponse> {
  try {
    const response = await apiClient.put(`/api/forms/${formId}`, request)
    return {
      success: response.data.success ?? true,
      message: response.data.message ?? 'Form updated successfully',
      formId: response.data.form_id ?? response.data.formId ?? formId,
      form: transformForm(response.data.form ?? response.data),
    }
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Delete (soft delete) a form
 */
export async function deleteForm(formId: number): Promise<DeleteFormResponse> {
  try {
    const response = await apiClient.delete(`/api/forms/${formId}`)
    return {
      success: response.data.success ?? true,
      message: response.data.message ?? 'Form deleted successfully',
      formId: response.data.form_id ?? response.data.formId ?? formId,
    }
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Get all forms for a specific event
 */
export async function getFormsByEvent(eventId: number): Promise<FormListResponse> {
  try {
    const response = await apiClient.get(`/api/forms/event/${eventId}`)
    return {
      forms: (response.data.forms ?? []).map(transformForm),
      total: response.data.total ?? 0,
      page: response.data.page ?? 1,
      pageSize: response.data.page_size ?? response.data.pageSize ?? 20,
    }
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Submit a form for approval
 */
export async function submitFormForApproval(formId: number): Promise<UpdateFormResponse> {
  try {
    const response = await apiClient.post(`/api/forms/${formId}/submit`)
    return {
      success: response.data.success ?? true,
      message: response.data.message ?? 'Form submitted for approval',
      formId: response.data.formId ?? formId,
      form: transformForm(response.data.form ?? response.data),
    }
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Request External Approval (Story 2.12)
 */
export async function requestExternalApproval(formId: number, email: string): Promise<any> {
    try {
        const response = await apiClient.post(`/api/forms/${formId}/request-external-approval`, { email })
        return response.data
    } catch (error) {
        throw formatError(error)
    }
}

/**
 * Get External Approval Context (Story 2.12)
 */
export async function getExternalApprovalContext(token: string): Promise<any> {
    try {
        // Note: Public endpoint, but apiClient might attach auth header if token exists. 
        // Should be fine as backend ignores it for public routes or handles it.
        const response = await apiClient.get(`/api/public/approval/${token}`)
        return response.data
    } catch (error) {
        throw formatError(error)
    }
}

/**
 * Submit External Decision (Story 2.12)
 */
export async function submitExternalDecision(token: string, decision: string, reason?: string): Promise<any> {
    try {
        const response = await apiClient.post(`/api/public/approval/${token}/decide`, { decision, reason })
        return response.data
    } catch (error) {
        throw formatError(error)
    }
}

/**
 * Approve a pending form
 */
export async function approveForm(formId: number): Promise<UpdateFormResponse> {
  try {
    const response = await apiClient.post(`/api/forms/${formId}/approve`)
    return {
      success: response.data.success ?? true,
      message: response.data.message ?? 'Form approved',
      formId: response.data.formId ?? formId,
      form: transformForm(response.data.form ?? response.data),
    }
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Reject a pending form
 */
export async function rejectForm(formId: number, reason: string): Promise<UpdateFormResponse> {
  try {
    const response = await apiClient.post(`/api/forms/${formId}/reject`, { reason })
    return {
      success: response.data.success ?? true,
      message: response.data.message ?? 'Form rejected',
      formId: response.data.formId ?? formId,
      form: transformForm(response.data.form ?? response.data),
    }
  } catch (error) {
    throw formatError(error)
  }
}

// =====================================================================
// Story 5.5: Preview/Production Governance
// =====================================================================

export type FormReadiness = {
  canPublish: boolean
  testRunCount: number
  testThresholdRequired: number
  testRunsNeeded: number
  message: string
}

/**
 * Get form publish readiness (test run count vs threshold)
 */
export async function getFormReadiness(formId: number): Promise<FormReadiness> {
  try {
    const response = await apiClient.get(`/api/forms/${formId}/readiness`)
    const d = response.data
    return {
      canPublish: d.canPublish ?? d.can_publish ?? false,
      testRunCount: d.testRunCount ?? d.test_run_count ?? 0,
      testThresholdRequired: d.testThresholdRequired ?? d.test_threshold_required ?? 0,
      testRunsNeeded: d.testRunsNeeded ?? d.test_runs_needed ?? 0,
      message: d.message ?? 'Ready to publish',
    }
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Record explicit test run (for static/no-input forms)
 */
export async function recordTestRun(formId: number): Promise<void> {
  try {
    await apiClient.post(`/api/forms/${formId}/record-test-run`)
  } catch (error) {
    throw formatError(error)
  }
}

/**
 * Create a preview link and return the preview URL.
 * Used to open form in preview so user can complete a real test submission.
 */
export async function createPreviewLink(formId: number): Promise<string> {
  const response = await apiClient.post(`/api/forms/${formId}/public-links`, { linkType: 'PREVIEW' })
  const link = response?.data?.link
  const token = link?.token ?? link?.Token
  if (!token) {
    throw new Error('Preview link was created but no token was returned.')
  }
  return `${window.location.origin}/forms/${token}/preview`
}

// =====================================================================
// Story 5.5: Company Test Config (includes RequirePublishApproval for 5.6)
// =====================================================================

export type CompanyTestConfig = {
  testThresholdEnabled: boolean
  testThresholdValue: number
  requirePublishApproval: boolean
  formCostThreshold: number | null
}

export async function getCompanyTestConfig(): Promise<CompanyTestConfig> {
  try {
    const response = await apiClient.get('/api/forms/company-test-config')
    const d = response.data
    const raw = d.formCostThreshold ?? d.form_cost_threshold
    return {
      testThresholdEnabled: d.testThresholdEnabled ?? d.test_threshold_enabled ?? false,
      testThresholdValue: d.testThresholdValue ?? d.test_threshold_value ?? 3,
      requirePublishApproval: d.requirePublishApproval ?? d.require_publish_approval ?? false,
      formCostThreshold: raw != null ? Number(raw) : null,
    }
  } catch (error) {
    throw formatError(error)
  }
}

export type CompanyTestConfigUpdate = Partial<CompanyTestConfig>

/** Requires full config - pass result of getCompanyTestConfig() with desired changes. */
export async function putCompanyTestConfig(update: CompanyTestConfigUpdate): Promise<CompanyTestConfig> {
  try {
    const payload = {
      testThresholdEnabled: update.testThresholdEnabled ?? false,
      testThresholdValue: update.testThresholdValue ?? 3,
      requirePublishApproval: update.requirePublishApproval ?? false,
      formCostThreshold: update.formCostThreshold ?? null,
    }
    const response = await apiClient.put('/api/forms/company-test-config', payload)
    const d = response.data
    const raw = d.formCostThreshold ?? d.form_cost_threshold
    return {
      testThresholdEnabled: d.testThresholdEnabled ?? d.test_threshold_enabled ?? false,
      testThresholdValue: d.testThresholdValue ?? d.test_threshold_value ?? 3,
      requirePublishApproval: d.requirePublishApproval ?? d.require_publish_approval ?? false,
      formCostThreshold: raw != null ? Number(raw) : null,
    }
  } catch (error) {
    throw formatError(error)
  }
}

// =====================================================================
// Story 5.6: Publish Request Workflow
// =====================================================================

export type PublishRequest = {
  formPublishRequestId: number
  formId: number
  formName: string
  requestedBy: number
  requestedByEmail: string | null
  requestedAt: string
  message: string | null
  status: string
}

export async function createPublishRequest(formId: number, message?: string): Promise<PublishRequest> {
  try {
    const response = await apiClient.post(`/api/forms/${formId}/publish-request`, { message: message ?? '' })
    const d = response.data
    return {
      formPublishRequestId: d.formPublishRequestId ?? d.form_publish_request_id ?? 0,
      formId: d.formId ?? d.form_id ?? formId,
      formName: d.formName ?? d.form_name ?? '',
      requestedBy: d.requestedBy ?? d.requested_by ?? 0,
      requestedByEmail: d.requestedByEmail ?? d.requested_by_email ?? null,
      requestedAt: d.requestedAt ?? d.requested_at ?? '',
      message: d.message ?? null,
      status: d.status ?? 'pending',
    }
  } catch (error) {
    throw formatError(error)
  }
}

export async function getPendingPublishRequests(): Promise<PublishRequest[]> {
  try {
    const response = await apiClient.get('/api/forms/publish-requests/pending')
    const arr = response.data
    return (Array.isArray(arr) ? arr : []).map((d: any) => ({
      formPublishRequestId: d.formPublishRequestId ?? d.form_publish_request_id ?? 0,
      formId: d.formId ?? d.form_id ?? 0,
      formName: d.formName ?? d.form_name ?? '',
      requestedBy: d.requestedBy ?? d.requested_by ?? 0,
      requestedByEmail: d.requestedByEmail ?? d.requested_by_email ?? null,
      requestedAt: d.requestedAt ?? d.requested_at ?? '',
      message: d.message ?? null,
      status: d.status ?? 'pending',
    }))
  } catch (error) {
    throw formatError(error)
  }
}

export type ApprovePublishOptions = {
  publish?: boolean  // true = Approve & Publish; false = Approve only
  comment?: string
  unpublishMode?: 'MANUAL' | 'EVENT_END' | 'SCHEDULED'
  scheduledUnpublishDate?: string  // ISO date when SCHEDULED
}

export async function approvePublishRequest(
  formId: number,
  options?: ApprovePublishOptions | string
): Promise<PublishRequest> {
  const opts = typeof options === 'string' ? { comment: options, publish: true } : (options ?? { publish: true })
  try {
    const response = await apiClient.post(`/api/forms/${formId}/publish-request/approve`, {
      comment: opts.comment ?? '',
      publish: opts.publish ?? true,
      unpublishMode: opts.unpublishMode ?? 'MANUAL',
      scheduledUnpublishDate: opts.scheduledUnpublishDate ?? null,
    })
    const d = response.data
    return {
      formPublishRequestId: d.formPublishRequestId ?? d.form_publish_request_id ?? 0,
      formId: d.formId ?? d.form_id ?? formId,
      formName: d.formName ?? d.form_name ?? '',
      requestedBy: d.requestedBy ?? d.requested_by ?? 0,
      requestedByEmail: d.requestedByEmail ?? d.requested_by_email ?? null,
      requestedAt: d.requestedAt ?? d.requested_at ?? '',
      message: d.message ?? null,
      status: d.status ?? 'approved',
    }
  } catch (error) {
    throw formatError(error)
  }
}

export async function publishForm(
  formId: number,
  options?: { unpublishMode?: 'MANUAL' | 'EVENT_END' | 'SCHEDULED'; scheduledUnpublishDate?: string }
): Promise<PublishRequest> {
  try {
    const response = await apiClient.post(`/api/forms/${formId}/publish`, {
      unpublishMode: options?.unpublishMode ?? 'MANUAL',
      scheduledUnpublishDate: options?.scheduledUnpublishDate ?? null,
    })
    const d = response.data
    return {
      formPublishRequestId: d.formPublishRequestId ?? d.form_publish_request_id ?? 0,
      formId: d.formId ?? d.form_id ?? formId,
      formName: d.formName ?? d.form_name ?? '',
      requestedBy: d.requestedBy ?? d.requested_by ?? 0,
      requestedByEmail: d.requestedByEmail ?? d.requested_by_email ?? null,
      requestedAt: d.requestedAt ?? d.requested_at ?? '',
      message: d.message ?? null,
      status: d.status ?? 'approved',
    }
  } catch (error) {
    throw formatError(error)
  }
}

export async function unpublishForm(formId: number): Promise<{ success: boolean; message: string }> {
  try {
    const response = await apiClient.post(`/api/forms/${formId}/unpublish`)
    return {
      success: response.data.success ?? true,
      message: response.data.message ?? 'Form unpublished',
    }
  } catch (error) {
    throw formatError(error)
  }
}

export type FormPublicUrl = { url: string | null; token: string | null; isPublished: boolean }

export type FormReviewContext = {
  formStatus: string
  hasPendingRequest: boolean
  hasApprovedRequest: boolean
  productionUrl: string | null
  productionToken: string | null
  unpublishMode: string
  scheduledUnpublishDate: string | null
  eventEndDate: string | null
}

export async function getFormReviewContext(formId: number): Promise<FormReviewContext> {
  try {
    const response = await apiClient.get(`/api/forms/${formId}/review-context`)
    const d = response.data
    return {
      formStatus: d.formStatus ?? d.form_status ?? '',
      hasPendingRequest: d.hasPendingRequest ?? d.has_pending_request ?? false,
      hasApprovedRequest: d.hasApprovedRequest ?? d.has_approved_request ?? false,
      productionUrl: d.productionUrl ?? d.production_url ?? null,
      productionToken: d.productionToken ?? d.production_token ?? null,
      unpublishMode: d.unpublishMode ?? d.unpublish_mode ?? 'MANUAL',
      scheduledUnpublishDate: d.scheduledUnpublishDate ?? d.scheduled_unpublish_date ?? null,
      eventEndDate: d.eventEndDate ?? d.event_end_date ?? null,
    }
  } catch (error) {
    throw formatError(error)
  }
}

export async function getFormPublicUrl(formId: number): Promise<FormPublicUrl> {
  try {
    const response = await apiClient.get(`/api/forms/${formId}/public-url`)
    const d = response.data
    return {
      url: d.url ?? null,
      token: d.token ?? null,
      isPublished: d.isPublished ?? false,
    }
  } catch (error) {
    throw formatError(error)
  }
}

export async function requestRepublish(token: string): Promise<{ success: boolean; message: string }> {
  try {
    const response = await apiClient.post(`/api/public/forms/${token}/request-republish`)
    return {
      success: response.data.success ?? true,
      message: response.data.message ?? 'Request recorded',
    }
  } catch (error) {
    throw formatError(error)
  }
}

export async function rejectPublishRequest(formId: number, reason?: string): Promise<PublishRequest> {
  try {
    const response = await apiClient.post(`/api/forms/${formId}/publish-request/reject`, { reason: reason ?? '' })
    const d = response.data
    return {
      formPublishRequestId: d.formPublishRequestId ?? d.form_publish_request_id ?? 0,
      formId: d.formId ?? d.form_id ?? formId,
      formName: d.formName ?? d.form_name ?? '',
      requestedBy: d.requestedBy ?? d.requested_by ?? 0,
      requestedByEmail: d.requestedByEmail ?? d.requested_by_email ?? null,
      requestedAt: d.requestedAt ?? d.requested_at ?? '',
      message: d.message ?? null,
      status: d.status ?? 'declined',
    }
  } catch (error) {
    throw formatError(error)
  }
}
