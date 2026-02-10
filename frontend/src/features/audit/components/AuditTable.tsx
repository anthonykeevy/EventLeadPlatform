/**
 * AuditTable Component (Story 2.13)
 * Detailed table view of audit events with filtering and pagination
 */
import { useState, useEffect, useCallback } from 'react';
import { AuditEntry, PaginatedActivityLog } from '../types/audit.types';
import { getCompanyActivityLog } from '../api/auditApi';

/**
 * Parse JSON string and extract details for display
 * Handles both valid JSON (double quotes) and Python dict-style (single quotes)
 */
function parseDetailsForDisplay(jsonStr: string | null | undefined): string {
  if (!jsonStr) return '—';
  
  const trimmed = jsonStr.trim();
  
  // If not JSON-like, return as-is
  if (!trimmed.startsWith('{') && !trimmed.startsWith('[')) {
    return jsonStr;
  }
  
  try {
    // First try standard JSON parse
    const parsed = JSON.parse(jsonStr);
    if (typeof parsed === 'object' && parsed !== null) {
      if (parsed.details) return parsed.details;
      const keys = Object.keys(parsed);
      if (keys.length === 0) return '—';
      return keys.map(k => `${formatFieldName(k)}: ${parsed[k]}`).join(', ');
    }
    return String(parsed);
  } catch {
    // Try converting Python dict style to JSON
    try {
      const jsonified = jsonStr
        .replace(/'/g, '"')
        .replace(/None/g, 'null')
        .replace(/True/g, 'true')
        .replace(/False/g, 'false');
      
      const parsed = JSON.parse(jsonified);
      if (typeof parsed === 'object' && parsed !== null) {
        if (parsed.details) return parsed.details;
        const keys = Object.keys(parsed);
        if (keys.length === 0) return '—';
        return keys.map(k => `${formatFieldName(k)}: ${parsed[k]}`).join(', ');
      }
      return String(parsed);
    } catch {
      return jsonStr;
    }
  }
}

/**
 * Format a field name for display (snake_case/camelCase to Title Case)
 */
function formatFieldName(key: string): string {
  return key
    .replace(/_/g, ' ')
    .replace(/([A-Z])/g, ' $1')
    .replace(/^./, str => str.toUpperCase())
    .trim();
}

/**
 * Format user display as: email (FirstName LastName)
 */
function formatUserDisplay(email: string | null | undefined, name: string | null | undefined): string {
  if (!email && !name) return 'System';
  if (email && name) return `${email} (${name})`;
  return email || name || 'Unknown';
}

interface AuditTableProps {
  /** If provided, uses these entries instead of fetching */
  entries?: AuditEntry[];
  /** Title for the table */
  title?: string;
  /** Whether to show the filter controls */
  showFilters?: boolean;
  /** Whether to enable pagination (only when fetching) */
  enablePagination?: boolean;
  /** Page size for pagination */
  pageSize?: number;
  /** Whether to show extended columns (Company, Event, Form) */
  showExtendedColumns?: boolean;
}

// Action badge colors
const actionBadgeColors: Record<string, string> = {
  created: 'bg-emerald-100 text-emerald-700',
  updated: 'bg-sky-100 text-sky-700',
  deleted: 'bg-slate-100 text-slate-700',
  submitted: 'bg-amber-100 text-amber-700',
  approved: 'bg-emerald-100 text-emerald-700',
  rejected: 'bg-rose-100 text-rose-700',
  granted: 'bg-cyan-100 text-cyan-700',
  revoked: 'bg-orange-100 text-orange-700',
  transferred: 'bg-indigo-100 text-indigo-700',
  requested: 'bg-violet-100 text-violet-700',
  published: 'bg-green-100 text-green-700',
  default: 'bg-slate-100 text-slate-600'
};

function getActionBadgeColor(action: string): string {
  for (const [key, color] of Object.entries(actionBadgeColors)) {
    if (action.toLowerCase().includes(key)) return color;
  }
  return actionBadgeColors.default;
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

export function AuditTable({
  entries: providedEntries,
  title = 'Activity Log',
  showFilters = true,
  enablePagination = true,
  pageSize = 20,
  showExtendedColumns = true
}: AuditTableProps) {
  const [entries, setEntries] = useState<AuditEntry[]>(providedEntries || []);
  const [loading, setLoading] = useState(!providedEntries);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);

  // Filters
  const [entityTypeFilter, setEntityTypeFilter] = useState<string>('');
  const [actionFilter, setActionFilter] = useState<string>('');
  const [userFilter, setUserFilter] = useState<string>('');
  const [formFilter, setFormFilter] = useState<string>('');
  const [eventFilter, setEventFilter] = useState<string>('');
  const [companyFilter, setCompanyFilter] = useState<string>('');

  const fetchData = useCallback(async () => {
    if (providedEntries) return;

    setLoading(true);
    setError(null);
    try {
      const response = await getCompanyActivityLog(
        page,
        pageSize,
        entityTypeFilter || undefined,
        actionFilter || undefined,
        undefined, // companyIdFilter - we use text filter instead
        undefined, // userIdFilter - we use text filter instead
        undefined, // formIdFilter - we use text filter instead
        undefined  // eventIdFilter - we use text filter instead
      );
      setEntries(response.items);
      setTotalPages(response.total_pages);
      setTotalCount(response.total_count);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load activity log');
    } finally {
      setLoading(false);
    }
  }, [providedEntries, page, pageSize, entityTypeFilter, actionFilter]);

  useEffect(() => {
    if (!providedEntries) {
      fetchData();
    }
  }, [fetchData, providedEntries]);

  // Reset to page 1 when filters change
  useEffect(() => {
    if (!providedEntries) {
      setPage(1);
    }
  }, [entityTypeFilter, actionFilter, providedEntries]);

  const handlePrevPage = () => {
    if (page > 1) setPage(page - 1);
  };

  const handleNextPage = () => {
    if (page < totalPages) setPage(page + 1);
  };

  // Apply local text filters on fetched data
  const displayEntries = (providedEntries || entries).filter(entry => {
    // Action filter
    if (actionFilter && !entry.action.toLowerCase().includes(actionFilter.toLowerCase())) {
      return false;
    }
    // User filter (search in email or name)
    if (userFilter) {
      const userStr = `${entry.user_email || ''} ${entry.user_name || ''}`.toLowerCase();
      if (!userStr.includes(userFilter.toLowerCase())) return false;
    }
    // Form filter
    if (formFilter && entry.form_name) {
      if (!entry.form_name.toLowerCase().includes(formFilter.toLowerCase())) return false;
    } else if (formFilter && !entry.form_name) {
      return false;
    }
    // Event filter
    if (eventFilter && entry.event_name) {
      if (!entry.event_name.toLowerCase().includes(eventFilter.toLowerCase())) return false;
    } else if (eventFilter && !entry.event_name) {
      return false;
    }
    // Company filter
    if (companyFilter && entry.company_name) {
      if (!entry.company_name.toLowerCase().includes(companyFilter.toLowerCase())) return false;
    } else if (companyFilter && !entry.company_name) {
      return false;
    }
    return true;
  });

  const clearFilters = () => {
    setEntityTypeFilter('');
    setActionFilter('');
    setUserFilter('');
    setFormFilter('');
    setEventFilter('');
    setCompanyFilter('');
  };

  const hasActiveFilters = entityTypeFilter || actionFilter || userFilter || formFilter || eventFilter || companyFilter;

  return (
    <div className="rounded-lg border border-slate-200 bg-white overflow-hidden">
      {/* Header */}
      <div className="px-6 py-4 border-b border-slate-200">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-slate-800">{title}</h3>
          <div className="flex items-center gap-4">
            {hasActiveFilters && (
              <button
                onClick={clearFilters}
                className="text-sm text-indigo-600 hover:text-indigo-800 flex items-center gap-1"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
                Clear Filters
              </button>
            )}
            {!providedEntries && (
              <span className="text-sm text-slate-500">
                {totalCount} total entries
              </span>
            )}
          </div>
        </div>

        {/* Filters */}
        {showFilters && (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 mt-4">
            <div>
              <label className="block text-xs text-slate-500 mb-1">Entity Type</label>
              <select
                value={entityTypeFilter}
                onChange={(e) => setEntityTypeFilter(e.target.value)}
                className="w-full px-2 py-1.5 border border-slate-300 rounded text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option value="">All Types</option>
                <option value="Form">Forms</option>
                <option value="Event">Events</option>
                <option value="User">Users</option>
              </select>
            </div>
            <div>
              <label className="block text-xs text-slate-500 mb-1">Action</label>
              <input
                type="text"
                value={actionFilter}
                onChange={(e) => setActionFilter(e.target.value)}
                placeholder="e.g., approved"
                className="w-full px-2 py-1.5 border border-slate-300 rounded text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            <div>
              <label className="block text-xs text-slate-500 mb-1">Company</label>
              <input
                type="text"
                value={companyFilter}
                onChange={(e) => setCompanyFilter(e.target.value)}
                placeholder="Company name..."
                className="w-full px-2 py-1.5 border border-slate-300 rounded text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            <div>
              <label className="block text-xs text-slate-500 mb-1">Event</label>
              <input
                type="text"
                value={eventFilter}
                onChange={(e) => setEventFilter(e.target.value)}
                placeholder="Event name..."
                className="w-full px-2 py-1.5 border border-slate-300 rounded text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            <div>
              <label className="block text-xs text-slate-500 mb-1">Form</label>
              <input
                type="text"
                value={formFilter}
                onChange={(e) => setFormFilter(e.target.value)}
                placeholder="Form name..."
                className="w-full px-2 py-1.5 border border-slate-300 rounded text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            <div>
              <label className="block text-xs text-slate-500 mb-1">User</label>
              <input
                type="text"
                value={userFilter}
                onChange={(e) => setUserFilter(e.target.value)}
                placeholder="Email or name..."
                className="w-full px-2 py-1.5 border border-slate-300 rounded text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
          </div>
        )}
      </div>

      {/* Error state */}
      {error && (
        <div className="p-6 text-center">
          <p className="text-rose-600">{error}</p>
          <button
            onClick={fetchData}
            className="mt-2 text-sm text-indigo-600 hover:text-indigo-800"
          >
            Retry
          </button>
        </div>
      )}

      {/* Loading state */}
      {loading && !error && (
        <div className="p-6 text-center">
          <div className="inline-flex items-center gap-2 text-slate-500">
            <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            Loading activity log...
          </div>
        </div>
      )}

      {/* Table */}
      {!loading && !error && (
        <>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="bg-slate-50 border-b border-slate-200">
                  <th className="px-3 py-3 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">
                    Timestamp
                  </th>
                  <th className="px-3 py-3 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">
                    Action
                  </th>
                  {showExtendedColumns && (
                    <>
                      <th className="px-3 py-3 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">
                        Company
                      </th>
                      <th className="px-3 py-3 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">
                        Event
                      </th>
                      <th className="px-3 py-3 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">
                        Form
                      </th>
                    </>
                  )}
                  <th className="px-3 py-3 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">
                    User
                  </th>
                  <th className="px-3 py-3 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">
                    Details
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {displayEntries.length === 0 ? (
                  <tr>
                    <td colSpan={showExtendedColumns ? 7 : 4} className="px-4 py-8 text-center text-slate-500">
                      No activity found
                    </td>
                  </tr>
                ) : (
                  displayEntries.map((entry, index) => (
                    <tr key={index} className="hover:bg-slate-50 transition-colors">
                      <td className="px-3 py-2.5 text-sm text-slate-600 whitespace-nowrap">
                        {formatTimestamp(entry.timestamp)}
                      </td>
                      <td className="px-3 py-2.5">
                        <span className={`inline-flex px-2 py-0.5 rounded text-xs font-medium ${getActionBadgeColor(entry.action)}`}>
                          {entry.action_display}
                        </span>
                      </td>
                      {showExtendedColumns && (
                        <>
                          <td className="px-3 py-2.5 text-sm text-slate-700 max-w-[150px] truncate" title={entry.company_name || ''}>
                            {entry.company_name || '—'}
                          </td>
                          <td className="px-3 py-2.5 text-sm text-slate-700 max-w-[150px] truncate" title={entry.event_name || ''}>
                            {entry.event_name || '—'}
                          </td>
                          <td className="px-3 py-2.5 text-sm text-slate-700 max-w-[150px] truncate" title={entry.form_name || ''}>
                            {entry.form_name || '—'}
                          </td>
                        </>
                      )}
                      <td className="px-3 py-2.5">
                        <div className="flex items-center gap-1.5">
                          <span className="text-sm text-slate-800 truncate max-w-[180px]" title={formatUserDisplay(entry.user_email, entry.user_name)}>
                            {formatUserDisplay(entry.user_email, entry.user_name)}
                          </span>
                          {entry.is_external && (
                            <span className="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium bg-violet-100 text-violet-700">
                              External
                            </span>
                          )}
                        </div>
                      </td>
                      <td className="px-3 py-2.5 text-sm text-slate-600 max-w-[200px] truncate" title={parseDetailsForDisplay(entry.new_value || entry.details)}>
                        {parseDetailsForDisplay(entry.new_value || entry.details)}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {enablePagination && !providedEntries && totalPages > 1 && (
            <div className="px-6 py-4 border-t border-slate-200 flex items-center justify-between">
              <span className="text-sm text-slate-500">
                Page {page} of {totalPages} ({displayEntries.length} shown)
              </span>
              <div className="flex gap-2">
                <button
                  onClick={handlePrevPage}
                  disabled={page === 1}
                  className={`px-4 py-2 text-sm rounded-md border ${
                    page === 1
                      ? 'border-slate-200 text-slate-400 cursor-not-allowed'
                      : 'border-slate-300 text-slate-700 hover:bg-slate-50'
                  }`}
                >
                  Previous
                </button>
                <button
                  onClick={handleNextPage}
                  disabled={page === totalPages}
                  className={`px-4 py-2 text-sm rounded-md border ${
                    page === totalPages
                      ? 'border-slate-200 text-slate-400 cursor-not-allowed'
                      : 'border-slate-300 text-slate-700 hover:bg-slate-50'
                  }`}
                >
                  Next
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default AuditTable;
