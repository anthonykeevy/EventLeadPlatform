/**
 * Audit Feature Module (Story 2.13)
 * Provides audit trail and compliance reporting components
 */

// Types (FormAuditReport type imported only from types/audit.types where needed to avoid duplicate with component name)
export type {
  AuditEntry,
  ApprovalChainEntry,
  AccessEntry,
  FormMetadata,
  EventAuditReport,
  PaginatedActivityLog
} from './types/audit.types';

// API
export {
  getFormAuditReport,
  getEventAuditReport,
  getCompanyActivityLog
} from './api/auditApi';

// Components
export { AuditTimeline } from './components/AuditTimeline';
export { AuditTable } from './components/AuditTable';
export { FormAuditReport } from './components/FormAuditReport';

