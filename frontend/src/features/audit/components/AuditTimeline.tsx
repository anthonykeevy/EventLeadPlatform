/**
 * AuditTimeline Component (Story 2.13)
 * Visual timeline of audit events for compliance reporting
 */
import { AuditEntry } from '../types/audit.types';

interface AuditTimelineProps {
  entries: AuditEntry[];
  title?: string;
  maxItems?: number;
  showViewAll?: boolean;
  onViewAll?: () => void;
}

/**
 * Parse JSON string and return key-value pairs for display
 * Handles both valid JSON (double quotes) and Python dict-style (single quotes)
 */
function parseJsonToKeyValues(jsonStr: string | null | undefined): Record<string, any> | null {
  if (!jsonStr) return null;
  
  // Check if it looks like JSON or Python dict
  const trimmed = jsonStr.trim();
  if (!trimmed.startsWith('{') && !trimmed.startsWith('[')) {
    return null;
  }
  
  try {
    // First try standard JSON parse
    const parsed = JSON.parse(jsonStr);
    return typeof parsed === 'object' && parsed !== null ? parsed : null;
  } catch {
    // If that fails, try converting Python dict style (single quotes) to JSON (double quotes)
    try {
      // Replace single quotes with double quotes, being careful about apostrophes in values
      const jsonified = jsonStr
        .replace(/'/g, '"')  // Convert single quotes to double quotes
        .replace(/None/g, 'null')  // Python None to JSON null
        .replace(/True/g, 'true')  // Python True to JSON true
        .replace(/False/g, 'false');  // Python False to JSON false
      
      const parsed = JSON.parse(jsonified);
      return typeof parsed === 'object' && parsed !== null ? parsed : null;
    } catch {
      return null;
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
 * Format a value for display
 */
function formatValue(value: any): string {
  if (value === null || value === undefined) return '—';
  if (typeof value === 'boolean') return value ? 'Yes' : 'No';
  if (typeof value === 'object') return JSON.stringify(value);
  return String(value);
}

/**
 * Check if two values are different (for change detection)
 */
function valuesAreDifferent(oldVal: any, newVal: any): boolean {
  if (oldVal === newVal) return false;
  if (oldVal === undefined && newVal === undefined) return false;
  if (oldVal === null && newVal === null) return false;
  return String(oldVal) !== String(newVal);
}

/**
 * Format user display as: email (FirstName LastName)
 */
function formatUserDisplay(email: string | null | undefined, name: string | null | undefined): string {
  if (!email && !name) return 'System';
  if (email && name) return `${email} (${name})`;
  return email || name || 'Unknown';
}

/**
 * Render details as a formatted table display
 * Now supports the new structured "changes" format from backend
 */
function DetailsTable({ oldValue, newValue, details, action }: { 
  oldValue?: string | null; 
  newValue?: string | null;
  details?: string | null;
  action?: string;
}) {
  const oldData = parseJsonToKeyValues(oldValue);
  let newData = parseJsonToKeyValues(newValue);
  
  // If newData is null but details is JSON, try parsing details
  if (!newData && details) {
    newData = parseJsonToKeyValues(details);
  }
  
  // Fields to exclude from display (IDs and meta fields)
  const excludeFields = ['details', 'changes', 'updated_by', 'created_by', 'approved_by', 'form_id', 'event_id', 'company_id', 'user_id', 'access_control_id', 'access_type_id'];
  
  // For UPDATES: Check for new structured "changes" format first
  // New format: { "changes": { "Field Name": { "old": "...", "new": "..." }, ... }, "details": "...", "updated_by": "..." }
  if (action?.includes('updated') && newData?.changes && typeof newData.changes === 'object') {
    const changes = newData.changes as Record<string, { old: string; new: string }>;
    const changeKeys = Object.keys(changes);
    
    if (changeKeys.length > 0) {
      return (
        <div className="mt-2 bg-slate-50 rounded-lg overflow-hidden border border-slate-200">
          <table className="w-full text-sm">
            <thead className="bg-slate-100 border-b border-slate-200">
              <tr>
                <th className="px-3 py-2 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider w-1/3">Field</th>
                <th className="px-3 py-2 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider w-1/3">Original</th>
                <th className="px-3 py-2 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider w-1/3">New Value</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {changeKeys.map(fieldName => {
                const change = changes[fieldName];
                return (
                  <tr key={fieldName} className="hover:bg-slate-100">
                    <td className="px-3 py-2 text-slate-700 font-medium">{fieldName}</td>
                    <td className="px-3 py-2 text-rose-600 line-through">{change.old}</td>
                    <td className="px-3 py-2 text-emerald-600 font-medium">{change.new}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      );
    }
  }
  
  // Legacy format: For UPDATES with both old and new data (flat structure)
  if (oldData && newData && action?.includes('updated')) {
    const changedFields = Object.keys(newData)
      .filter(key => !excludeFields.includes(key))
      .filter(key => valuesAreDifferent(oldData[key], newData[key]));
    
    if (changedFields.length === 0) {
      const detailText = newData.details || details;
      if (detailText && typeof detailText === 'string' && !detailText.startsWith('{')) {
        return <p className="text-sm text-slate-600 mt-2 bg-slate-50 rounded px-3 py-2">{detailText}</p>;
      }
      return <p className="text-sm text-slate-500 mt-2 italic">Record updated (details not captured)</p>;
    }
    
    return (
      <div className="mt-2 bg-slate-50 rounded-lg overflow-hidden border border-slate-200">
        <table className="w-full text-sm">
          <thead className="bg-slate-100 border-b border-slate-200">
            <tr>
              <th className="px-3 py-2 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider w-1/3">Field</th>
              <th className="px-3 py-2 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider w-1/3">Original</th>
              <th className="px-3 py-2 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider w-1/3">New Value</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200">
            {changedFields.map(key => (
              <tr key={key} className="hover:bg-slate-100">
                <td className="px-3 py-2 text-slate-700 font-medium">{formatFieldName(key)}</td>
                <td className="px-3 py-2 text-rose-600 line-through">{formatValue(oldData[key])}</td>
                <td className="px-3 py-2 text-emerald-600 font-medium">{formatValue(newData![key])}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }
  
  // For UPDATES without old data but has details: Show the summary text
  if (newData && action?.includes('updated')) {
    if (newData.details && typeof newData.details === 'string' && !newData.details.startsWith('{')) {
      return <p className="text-sm text-slate-600 mt-2 bg-slate-50 rounded px-3 py-2">{newData.details}</p>;
    }
    
    const fieldsToShow = Object.keys(newData).filter(key => !excludeFields.includes(key));
    if (fieldsToShow.length === 0) {
      return <p className="text-sm text-slate-500 mt-2 italic">Record updated</p>;
    }
    
    return (
      <div className="mt-2 bg-slate-50 rounded-lg overflow-hidden border border-slate-200">
        <table className="w-full text-sm">
          <thead className="bg-slate-100 border-b border-slate-200">
            <tr>
              <th className="px-3 py-2 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider w-1/3">Field</th>
              <th className="px-3 py-2 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">Value</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200">
            {fieldsToShow.map(key => (
              <tr key={key} className="hover:bg-slate-100">
                <td className="px-3 py-2 text-slate-700 font-medium">{formatFieldName(key)}</td>
                <td className="px-3 py-2 text-slate-800">{formatValue(newData![key])}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }
  
  // For CREATES: Show meaningful fields
  if (newData && action?.includes('created')) {
    // Check for a details text first
    if (newData.details && typeof newData.details === 'string' && !newData.details.startsWith('{')) {
      return <p className="text-sm text-slate-600 mt-2 bg-slate-50 rounded px-3 py-2">{newData.details}</p>;
    }
    
    const fieldsToShow = Object.keys(newData).filter(key => !excludeFields.includes(key));
    if (fieldsToShow.length === 0) {
      return null;
    }
    
    return (
      <div className="mt-2 bg-slate-50 rounded-lg overflow-hidden border border-slate-200">
        <table className="w-full text-sm">
          <thead className="bg-slate-100 border-b border-slate-200">
            <tr>
              <th className="px-3 py-2 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider w-1/3">Field</th>
              <th className="px-3 py-2 text-left text-xs font-semibold text-slate-600 uppercase tracking-wider">Value</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200">
            {fieldsToShow.map(key => (
              <tr key={key} className="hover:bg-slate-100">
                <td className="px-3 py-2 text-slate-700 font-medium">{formatFieldName(key)}</td>
                <td className="px-3 py-2 text-slate-800">{formatValue(newData![key])}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }
  
  // For other actions: Show the details text
  if (newData?.details && typeof newData.details === 'string' && !newData.details.startsWith('{')) {
    return <p className="text-sm text-slate-600 mt-2 bg-slate-50 rounded px-3 py-2">{newData.details}</p>;
  }
  
  // Fallback to showing details as plain text
  if (details && !details.startsWith('{') && !details.startsWith('[')) {
    return <p className="text-sm text-slate-600 mt-2 bg-slate-50 rounded px-3 py-2">{details}</p>;
  }
  
  return null;
}

// Action to color mapping for visual distinction
const actionColors: Record<string, { bg: string; border: string; icon: string }> = {
  'form.created': { bg: 'bg-emerald-100', border: 'border-emerald-500', icon: '✨' },
  'form.updated': { bg: 'bg-sky-100', border: 'border-sky-500', icon: '📝' },
  'form.deleted': { bg: 'bg-slate-100', border: 'border-slate-500', icon: '🗑️' },
  'form.submitted_for_approval': { bg: 'bg-amber-100', border: 'border-amber-500', icon: '📤' },
  'form.approved': { bg: 'bg-emerald-100', border: 'border-emerald-600', icon: '✅' },
  'form.rejected': { bg: 'bg-rose-100', border: 'border-rose-500', icon: '❌' },
  'form.approved_external': { bg: 'bg-teal-100', border: 'border-teal-500', icon: '✅🌐' },
  'form.rejected_external': { bg: 'bg-rose-100', border: 'border-rose-400', icon: '❌🌐' },
  'form.published': { bg: 'bg-green-100', border: 'border-green-600', icon: '🚀' },
  'form.external_approval_requested': { bg: 'bg-violet-100', border: 'border-violet-500', icon: '📧' },
  'form.ownership_transferred': { bg: 'bg-indigo-100', border: 'border-indigo-500', icon: '🔄' },
  'form.access.granted': { bg: 'bg-cyan-100', border: 'border-cyan-500', icon: '🔓' },
  'form.access.revoked': { bg: 'bg-orange-100', border: 'border-orange-500', icon: '🔒' },
  'form.access.updated': { bg: 'bg-sky-100', border: 'border-sky-400', icon: '🔧' },
  'event.created': { bg: 'bg-emerald-100', border: 'border-emerald-500', icon: '📅' },
  'event.updated': { bg: 'bg-sky-100', border: 'border-sky-500', icon: '📅' },
  'default': { bg: 'bg-slate-100', border: 'border-slate-400', icon: '📋' }
};

function getActionStyle(action: string) {
  return actionColors[action] || actionColors['default'];
}

/**
 * Format timestamp for display in user's local timezone.
 * Backend stores all dates in UTC, this function converts to local timezone.
 * Pattern consistent with EventDetailView.tsx and other components.
 */
function formatTimestamp(timestamp: string | null): string {
  if (!timestamp) return 'Unknown time';
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

export function AuditTimeline({
  entries,
  title = 'Activity Timeline',
  maxItems,
  showViewAll = false,
  onViewAll
}: AuditTimelineProps) {
  const displayEntries = maxItems ? entries.slice(0, maxItems) : entries;
  const hasMore = maxItems && entries.length > maxItems;

  if (entries.length === 0) {
    return (
      <div className="rounded-lg border border-slate-200 bg-white p-6">
        <h3 className="text-lg font-semibold text-slate-800 mb-4">{title}</h3>
        <p className="text-slate-500 text-center py-8">No activity recorded yet.</p>
      </div>
    );
  }

  return (
    <div className="rounded-lg border border-slate-200 bg-white p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-slate-800">{title}</h3>
        {showViewAll && onViewAll && (
          <button
            onClick={onViewAll}
            className="text-sm text-indigo-600 hover:text-indigo-800 font-medium"
          >
            View All →
          </button>
        )}
      </div>

      <div className="relative">
        {/* Timeline line */}
        <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-slate-200" />

        {/* Timeline entries */}
        <div className="space-y-6">
          {displayEntries.map((entry, index) => {
            const style = getActionStyle(entry.action);
            
            return (
              <div key={index} className="relative flex gap-4">
                {/* Timeline dot */}
                <div 
                  className={`flex-shrink-0 w-12 h-12 rounded-full ${style.bg} ${style.border} border-2 flex items-center justify-center text-lg z-10`}
                >
                  {style.icon}
                </div>

                {/* Content */}
                <div className="flex-grow pb-2">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="font-medium text-slate-800">
                        {entry.action_display}
                      </p>
                      <p className="text-sm text-slate-500 mt-0.5">
                        {formatUserDisplay(entry.user_email, entry.user_name)}
                        {entry.is_external && (
                          <span className="ml-2 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-violet-100 text-violet-700">
                            External
                          </span>
                        )}
                      </p>
                    </div>
                    <span className="text-xs text-slate-400 whitespace-nowrap ml-4">
                      {formatTimestamp(entry.timestamp)}
                    </span>
                  </div>

                  {/* Details - render based on action type */}
                  <DetailsTable 
                    oldValue={entry.old_value} 
                    newValue={entry.new_value} 
                    details={entry.details}
                    action={entry.action}
                  />

                  {/* Token ID for external approvals */}
                  {entry.token_id && (
                    <p className="text-xs text-slate-400 mt-1">
                      Token ID: {entry.token_id}
                    </p>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {/* View more indicator */}
        {hasMore && (
          <div className="text-center pt-4">
            <button
              onClick={onViewAll}
              className="text-sm text-slate-500 hover:text-slate-700"
            >
              + {entries.length - (maxItems || 0)} more entries
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default AuditTimeline;

