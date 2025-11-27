/**
 * Audit API (Story 2.13)
 * API functions for audit trail and compliance reports
 */
import { apiClient, formatError } from '../../../lib/apiClient';
import { FormAuditReport, EventAuditReport, PaginatedActivityLog } from '../types/audit.types';

/**
 * Get compliance report for a form
 * @param formId Form ID
 * @returns FormAuditReport
 */
export async function getFormAuditReport(formId: number): Promise<FormAuditReport> {
  try {
    const response = await apiClient.get<FormAuditReport>(`/api/audit/form/${formId}`);
    return response.data;
  } catch (error) {
    throw formatError(error);
  }
}

/**
 * Get compliance report for an event
 * @param eventId Event ID
 * @returns EventAuditReport
 */
export async function getEventAuditReport(eventId: number): Promise<EventAuditReport> {
  try {
    const response = await apiClient.get<EventAuditReport>(`/api/audit/event/${eventId}`);
    return response.data;
  } catch (error) {
    throw formatError(error);
  }
}

/**
 * Get paginated activity log for the company
 * @param page Page number (1-based)
 * @param pageSize Items per page
 * @param entityType Optional filter by entity type
 * @param actionFilter Optional filter by action
 * @param companyIdFilter Optional filter by company ID (System Admin only)
 * @param userIdFilter Optional filter by user ID
 * @param formIdFilter Optional filter by form ID
 * @param eventIdFilter Optional filter by event ID
 * @returns PaginatedActivityLog
 */
export async function getCompanyActivityLog(
  page: number = 1,
  pageSize: number = 50,
  entityType?: string,
  actionFilter?: string,
  companyIdFilter?: number,
  userIdFilter?: number,
  formIdFilter?: number,
  eventIdFilter?: number
): Promise<PaginatedActivityLog> {
  try {
    const params = new URLSearchParams();
    params.set('page', page.toString());
    params.set('page_size', pageSize.toString());
    if (entityType) params.set('entity_type', entityType);
    if (actionFilter) params.set('action_filter', actionFilter);
    if (companyIdFilter) params.set('company_id_filter', companyIdFilter.toString());
    if (userIdFilter) params.set('user_id_filter', userIdFilter.toString());
    if (formIdFilter) params.set('form_id_filter', formIdFilter.toString());
    if (eventIdFilter) params.set('event_id_filter', eventIdFilter.toString());

    const response = await apiClient.get<PaginatedActivityLog>(
      `/api/audit/company/activity?${params.toString()}`
    );
    return response.data;
  } catch (error) {
    throw formatError(error);
  }
}

