/**
 * Forms API Client for Epic 2 Story 2.8
 * Handles form header management API calls
 */

import axios, { AxiosInstance, AxiosError } from 'axios'
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
import { getAccessToken, getRefreshToken, storeTokens, clearTokens } from '../../auth/utils/tokenStorage'
import { refreshAccessToken } from '../../auth/api/authApi'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

// Create axios instance for forms requests
const formsClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
})

// Add request interceptor to attach access token
formsClient.interceptors.request.use(
  (config) => {
    const token = getAccessToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Add response interceptor to handle token refresh on 401 errors
formsClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // Check if offline
    if (!navigator.onLine) {
      if (!error.response) {
        return Promise.reject(error)
      }
      return Promise.reject(error)
    }

    // If error is 401 and we haven't already retried
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const tokenResponse = await refreshAccessToken()
        const expiresIn = tokenResponse.expires_in || 3600
        storeTokens(tokenResponse.access_token, tokenResponse.refresh_token, expiresIn)
        originalRequest.headers.Authorization = `Bearer ${tokenResponse.access_token}`
        return formsClient(originalRequest)
      } catch (refreshError) {
        if (navigator.onLine) {
          clearTokens()
        }
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

// Format error for display
function formatError(error: unknown): Error {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError
    if (axiosError.response) {
      return new Error(
        (axiosError.response.data as any)?.detail || 
        axiosError.response.statusText || 
        'An error occurred'
      )
    }
  }
  return new Error(error instanceof Error ? error.message : 'An unknown error occurred')
}

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
    deploymentCost: backend.deployment_cost ?? backend.deploymentCost ?? backend.DeploymentCost ?? null,
    totalSubmissions: backend.total_submissions ?? backend.totalSubmissions ?? backend.TotalSubmissions ?? 0,
    demoLeadsCollected: backend.demo_leads_collected ?? backend.demoLeadsCollected ?? backend.DemoLeadsCollected ?? 0,
    productionLeadsCollected: backend.production_leads_collected ?? backend.productionLeadsCollected ?? backend.ProductionLeadsCollected ?? 0,
    lastSubmissionDate: backend.last_submission_date ?? backend.lastSubmissionDate ?? backend.LastSubmissionDate ?? null,
    lastActivityDate: backend.last_activity_date ?? backend.lastActivityDate ?? backend.LastActivityDate ?? null,
    formThumbnailUrl: backend.form_thumbnail_url ?? backend.formThumbnailUrl ?? backend.FormThumbnailURL ?? null,
    formPreviewUrl: backend.form_preview_url ?? backend.formPreviewUrl ?? backend.FormPreviewURL ?? null,
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
    const response = await formsClient.get('/api/forms/statuses')
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
    const response = await formsClient.get('/api/forms/approval-statuses')
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
    
    const response = await formsClient.get('/api/forms', { params })
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
    const response = await formsClient.get(`/api/forms/${formId}`)
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
    const response = await formsClient.post('/api/forms', request)
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
    const response = await formsClient.put(`/api/forms/${formId}`, request)
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
    const response = await formsClient.delete(`/api/forms/${formId}`)
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
    const response = await formsClient.get(`/api/forms/event/${eventId}`)
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

