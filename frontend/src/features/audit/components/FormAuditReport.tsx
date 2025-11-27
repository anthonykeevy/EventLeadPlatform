/**
 * FormAuditReport Component (Story 2.13)
 * Complete compliance report view for a form
 */
import React, { useState, useEffect } from 'react';
import { FormAuditReport as FormAuditReportType, ApprovalChainEntry, AccessEntry } from '../types/audit.types';
import { getFormAuditReport } from '../api/auditApi';
import { AuditTimeline } from './AuditTimeline';

interface FormAuditReportProps {
  formId: number;
  onClose?: () => void;
}

/**
 * Format timestamp for display in user's local timezone.
 * Backend stores all dates in UTC, this function converts to local timezone.
 * Pattern consistent with EventDetailView.tsx and other components.
 */
function formatTimestamp(timestamp: string | null): string {
  if (!timestamp) return '—';
  try {
    const date = new Date(timestamp);
    // Use Intl.DateTimeFormat for consistent cross-browser behavior
    // No timeZone specified = uses browser's local timezone (correct for user display)
    return new Intl.DateTimeFormat('en-AU', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    }).format(date);
  } catch {
    return timestamp;
  }
}

function formatCurrency(amount: number | null): string {
  if (amount === null) return '—';
  return new Intl.NumberFormat('en-AU', {
    style: 'currency',
    currency: 'AUD'
  }).format(amount);
}

/**
 * Format user display as: email (FirstName LastName)
 */
function formatUserDisplay(email: string | null | undefined, name: string | null | undefined): string {
  if (!email && !name) return 'System';
  if (email && name) return `${email} (${name})`;
  return email || name || 'Unknown';
}

// Approval chain visualization
function ApprovalChainSection({ chain }: { chain: ApprovalChainEntry[] }) {
  if (chain.length === 0) {
    return (
      <div className="text-slate-500 text-center py-4">
        No approvals recorded yet.
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {chain.map((entry, index) => (
        <div
          key={index}
          className={`p-4 rounded-lg border ${
            entry.decision === 'Approved'
              ? 'border-emerald-200 bg-emerald-50'
              : entry.decision === 'Rejected'
              ? 'border-rose-200 bg-rose-50'
              : 'border-amber-200 bg-amber-50'
          }`}
        >
          <div className="flex items-start justify-between">
            <div>
              <div className="flex items-center gap-2">
                <span className={`text-lg ${
                  entry.decision === 'Approved' ? 'text-emerald-600' : 
                  entry.decision === 'Rejected' ? 'text-rose-600' : 'text-amber-600'
                }`}>
                  {entry.decision === 'Approved' ? '✅' : entry.decision === 'Rejected' ? '❌' : '⏳'}
                </span>
                <span className="font-medium text-slate-800">
                  {entry.decision}
                </span>
                {entry.is_external && (
                  <span className="px-2 py-0.5 rounded text-xs font-medium bg-violet-100 text-violet-700">
                    External Approver
                  </span>
                )}
              </div>
              <p className="text-sm text-slate-600 mt-1">
                {formatUserDisplay(entry.approver_email, entry.approver_name)}
              </p>
              {entry.reason && (
                <p className="text-sm text-slate-500 mt-2 italic">
                  Reason: {entry.reason}
                </p>
              )}
            </div>
            <div className="text-right text-sm">
              {entry.decided_at && (
                <p className="text-slate-500">{formatTimestamp(entry.decided_at)}</p>
              )}
              {entry.token_id && (
                <p className="text-xs text-slate-400 mt-1">Token #{entry.token_id}</p>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

// Access list table
function AccessListSection({ accessList }: { accessList: AccessEntry[] }) {
  if (accessList.length === 0) {
    return (
      <div className="text-slate-500 text-center py-4">
        No access grants recorded.
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr className="border-b border-slate-200">
            <th className="px-4 py-2 text-left text-xs font-semibold text-slate-600 uppercase">User</th>
            <th className="px-4 py-2 text-left text-xs font-semibold text-slate-600 uppercase">Access</th>
            <th className="px-4 py-2 text-left text-xs font-semibold text-slate-600 uppercase">Granted By</th>
            <th className="px-4 py-2 text-left text-xs font-semibold text-slate-600 uppercase">Granted</th>
            <th className="px-4 py-2 text-left text-xs font-semibold text-slate-600 uppercase">Expires</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {accessList.map((entry, index) => (
            <tr key={index} className="hover:bg-slate-50">
              <td className="px-4 py-3">
                <div className="text-sm font-medium text-slate-800">
                  {formatUserDisplay(entry.user_email, entry.user_name)}
                </div>
              </td>
              <td className="px-4 py-3">
                <span className="inline-flex px-2 py-1 rounded text-xs font-medium bg-indigo-100 text-indigo-700">
                  {entry.access_type_display}
                </span>
              </td>
              <td className="px-4 py-3 text-sm text-slate-600">{entry.granted_by_name}</td>
              <td className="px-4 py-3 text-sm text-slate-500">{formatTimestamp(entry.granted_at)}</td>
              <td className="px-4 py-3 text-sm text-slate-500">
                {entry.expires_at ? formatTimestamp(entry.expires_at) : 'Never'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function FormAuditReport({ formId, onClose }: FormAuditReportProps) {
  const [report, setReport] = useState<FormAuditReportType | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'approvals' | 'access' | 'timeline'>('overview');

  useEffect(() => {
    async function loadReport() {
      setLoading(true);
      setError(null);
      try {
        const data = await getFormAuditReport(formId);
        setReport(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load audit report');
      } finally {
        setLoading(false);
      }
    }
    loadReport();
  }, [formId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center p-12">
        <div className="inline-flex items-center gap-3 text-slate-500">
          <svg className="animate-spin h-6 w-6" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
          <span className="text-lg">Loading compliance report...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8 text-center">
        <p className="text-rose-600 text-lg">{error}</p>
        {onClose && (
          <button
            onClick={onClose}
            className="mt-4 px-4 py-2 text-sm text-slate-600 hover:text-slate-800"
          >
            Close
          </button>
        )}
      </div>
    );
  }

  if (!report) return null;

  const { form_metadata, approval_chain, current_access_list, activity_timeline } = report;

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden max-w-6xl mx-auto">
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 px-6 py-6 text-white">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-2xl font-bold">Compliance Report</h2>
            <p className="text-indigo-100 mt-1">{form_metadata.form_name}</p>
          </div>
          {onClose && (
            <button
              onClick={onClose}
              className="p-2 hover:bg-white/10 rounded-lg transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>
        <p className="text-xs text-indigo-200 mt-4">
          Report generated: {formatTimestamp(report.report_generated_at)}
        </p>
      </div>

      {/* Tabs */}
      <div className="border-b border-slate-200">
        <nav className="flex -mb-px">
          {(['overview', 'approvals', 'access', 'timeline'] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-6 py-3 text-sm font-medium border-b-2 transition-colors ${
                activeTab === tab
                  ? 'border-indigo-500 text-indigo-600'
                  : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
              }`}
            >
              {tab === 'overview' && 'Overview'}
              {tab === 'approvals' && `Approvals (${approval_chain.length})`}
              {tab === 'access' && `Access (${current_access_list.length})`}
              {tab === 'timeline' && `Timeline (${activity_timeline.length})`}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab content */}
      <div className="p-6">
        {activeTab === 'overview' && (
          <div className="grid grid-cols-2 gap-6">
            {/* Form Metadata */}
            <div className="bg-slate-50 rounded-lg p-4">
              <h4 className="text-sm font-semibold text-slate-700 uppercase mb-4">Form Details</h4>
              <dl className="space-y-3">
                <div>
                  <dt className="text-xs text-slate-500">Form ID</dt>
                  <dd className="text-sm text-slate-800">{form_metadata.form_id}</dd>
                </div>
                <div>
                  <dt className="text-xs text-slate-500">Description</dt>
                  <dd className="text-sm text-slate-800">{form_metadata.form_description || '—'}</dd>
                </div>
                <div>
                  <dt className="text-xs text-slate-500">Deployment Cost</dt>
                  <dd className="text-sm text-slate-800 font-semibold">{formatCurrency(form_metadata.deployment_cost)}</dd>
                </div>
                <div>
                  <dt className="text-xs text-slate-500">Event</dt>
                  <dd className="text-sm text-slate-800">{form_metadata.event_name || 'Not linked to event'}</dd>
                </div>
              </dl>
            </div>

            {/* Status & Creator */}
            <div className="bg-slate-50 rounded-lg p-4">
              <h4 className="text-sm font-semibold text-slate-700 uppercase mb-4">Status & Ownership</h4>
              <dl className="space-y-3">
                <div>
                  <dt className="text-xs text-slate-500">Current Status</dt>
                  <dd className="text-sm">
                    <span className="inline-flex px-2 py-1 rounded bg-sky-100 text-sky-700 font-medium">
                      {form_metadata.current_status}
                    </span>
                  </dd>
                </div>
                <div>
                  <dt className="text-xs text-slate-500">Approval Status</dt>
                  <dd className="text-sm">
                    <span className={`inline-flex px-2 py-1 rounded font-medium ${
                      form_metadata.current_approval_status === 'Approved'
                        ? 'bg-emerald-100 text-emerald-700'
                        : form_metadata.current_approval_status === 'Rejected'
                        ? 'bg-rose-100 text-rose-700'
                        : 'bg-amber-100 text-amber-700'
                    }`}>
                      {form_metadata.current_approval_status}
                    </span>
                  </dd>
                </div>
                <div>
                  <dt className="text-xs text-slate-500">Created By</dt>
                  <dd className="text-sm text-slate-800">
                    {formatUserDisplay(form_metadata.created_by_email, form_metadata.created_by_name)}
                  </dd>
                </div>
                <div>
                  <dt className="text-xs text-slate-500">Created At</dt>
                  <dd className="text-sm text-slate-800">{formatTimestamp(form_metadata.created_at)}</dd>
                </div>
                <div>
                  <dt className="text-xs text-slate-500">Company</dt>
                  <dd className="text-sm text-slate-800">{form_metadata.company_name}</dd>
                </div>
              </dl>
            </div>
          </div>
        )}

        {activeTab === 'approvals' && (
          <ApprovalChainSection chain={approval_chain} />
        )}

        {activeTab === 'access' && (
          <AccessListSection accessList={current_access_list} />
        )}

        {activeTab === 'timeline' && (
          <AuditTimeline entries={activity_timeline} title="" />
        )}
      </div>
    </div>
  );
}

export default FormAuditReport;

