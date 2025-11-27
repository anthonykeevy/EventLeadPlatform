/**
 * Audit Types (Story 2.13)
 * TypeScript types for audit trail and compliance reports
 */

export interface AuditEntry {
  timestamp: string | null;
  action: string;
  action_display: string;
  user_id: number | null;
  user_email: string | null;
  user_name: string | null;
  is_external: boolean;
  details: string | null;
  old_value?: string | null;  // Previous value for tracking changes
  new_value?: string | null;  // New value for tracking changes
  token_id?: number | null;
  // Additional context fields for Activity Log table
  company_id?: number | null;
  company_name?: string | null;
  entity_id?: number | null;
  entity_type?: string | null;
  form_name?: string | null;
  event_name?: string | null;
}

export interface ApprovalChainEntry {
  approver_id: number | null;
  approver_email: string;
  approver_name: string | null;
  is_external: boolean;
  decision: string;
  decided_at: string | null;
  token_id: number | null;
  reason: string | null;
}

export interface AccessEntry {
  user_id: number;
  user_email: string;
  user_name: string;
  access_type: string;
  access_type_display: string;
  granted_by_id: number;
  granted_by_name: string;
  granted_at: string | null;
  expires_at: string | null;
}

export interface FormMetadata {
  form_id: number;
  form_name: string;
  form_description: string | null;
  created_by_id: number;
  created_by_email: string;
  created_by_name: string;
  created_at: string | null;
  current_status: string;
  current_approval_status: string;
  deployment_cost: number | null;
  company_id: number;
  company_name: string;
  event_id: number | null;
  event_name: string | null;
}

export interface FormAuditReport {
  report_generated_at: string;
  form_metadata: FormMetadata;
  approval_chain: ApprovalChainEntry[];
  current_access_list: AccessEntry[];
  activity_timeline: AuditEntry[];
}

export interface EventAuditReport {
  report_generated_at: string;
  event_id: number;
  event_name: string;
  company_id: number;
  company_name: string;
  created_by_id: number;
  created_by_name: string;
  created_at: string | null;
  current_status: string;
  forms_count: number;
  activity_timeline: AuditEntry[];
}

export interface PaginatedActivityLog {
  items: AuditEntry[];
  total_count: number;
  page: number;
  page_size: number;
  total_pages: number;
}

