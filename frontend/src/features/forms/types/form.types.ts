/**
 * Forms Types for Epic 2 Story 2.8
 * Type definitions for form header management
 */

// Reference Data Types
export interface FormStatus {
  formStatusId: number
  statusCode: string
  statusName: string
  statusDescription: string | null
  statusColor: string | null
  statusIcon: string | null
  isActive: boolean
  sortOrder: number
}

export interface FormApprovalStatus {
  formApprovalStatusId: number
  approvalStatusCode: string
  approvalStatusName: string
  approvalStatusDescription: string | null
  isRequiresApproval: boolean
  isActive: boolean
  sortOrder: number
}

// Main Form Type
export interface Form {
  formId: number
  formName: string
  formDescription: string | null
  companyId: number
  eventId: number | null
  formStatusId: number
  formStatus: FormStatus | null
  formApprovalStatusId: number
  formApprovalStatus: FormApprovalStatus | null
  isPublic: boolean
  deploymentCost: number | null
  totalSubmissions: number
  demoLeadsCollected: number
  productionLeadsCollected: number
  lastSubmissionDate: string | null
  lastActivityDate: string | null
  formThumbnailUrl: string | null
  formPreviewUrl: string | null
  createdDate: string
  createdBy: number
  updatedDate: string | null
  updatedBy: number | null
}

// Request Types
export interface FormCreateRequest {
  formName: string
  formDescription?: string | null
  eventId?: number | null
  formStatusId: number
  formApprovalStatusId: number
  isPublic?: boolean
  deploymentCost?: number | null
  formThumbnailUrl?: string | null
  formPreviewUrl?: string | null
}

export interface FormUpdateRequest {
  formName?: string
  formDescription?: string | null
  eventId?: number | null
  formStatusId?: number
  formApprovalStatusId?: number
  isPublic?: boolean
  deploymentCost?: number | null
  formThumbnailUrl?: string | null
  formPreviewUrl?: string | null
}

// Response Types
export interface FormListResponse {
  forms: Form[]
  total: number
  page: number
  pageSize: number
}

export interface CreateFormResponse {
  success: boolean
  message: string
  formId: number
  form: Form
}

export interface UpdateFormResponse {
  success: boolean
  message: string
  formId: number
  form: Form
}

export interface DeleteFormResponse {
  success: boolean
  message: string
  formId: number
}

// Filter Types
export interface FormFilters {
  formStatusId?: number
  eventId?: number
  search?: string
}

