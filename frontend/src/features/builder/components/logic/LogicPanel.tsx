import React from 'react';
import { AlertTriangle, CheckCircle2, ChevronDown, GitBranch, Plus, Search, Trash2, Pencil, ArrowUp, ArrowDown } from 'lucide-react';
import { useBuilderStore } from '../../stores/useBuilderStore';
import { FormComponent, LogicOperator, LogicRule } from '../../types/builder.types';
import { ALL_ACTIONS, allowedOperatorsForSourceType, validateRule } from './ruleValidation';

type FilterMode = 'all' | 'enabled' | 'errors';

function makeId(prefix: string) {
    try {
        // Modern browsers
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const uuid = (crypto as any).randomUUID?.();
        if (uuid) return `${prefix}-${uuid}`;
    } catch {
        // ignore
    }
    return `${prefix}-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function flattenComponents(list: FormComponent[]): FormComponent[] {
    const out: FormComponent[] = [];
    const walk = (items: FormComponent[]) => {
        for (const c of items) {
            out.push(c);
            if (c.children?.length) walk(c.children);
        }
    };
    walk(list);
    return out;
}

function isFieldLike(type: FormComponent['type']) {
    return !['submit-button', 'divider', 'header', 'paragraph'].includes(type);
}

function getDisplayLabel(c: FormComponent) {
    const label = (c.props.label || c.type).trim();
    const meta = c.props.exportName ? c.props.exportName : c.id;
    return `${label} (${meta})`;
}

function summarizeRule(rule: LogicRule, componentsById: Record<string, FormComponent>) {
    const src = componentsById[rule.when.sourceComponentId];
    const tgt = componentsById[rule.then.targetComponentId];
    const srcLabel = src ? (src.props.label || src.type) : 'Missing field';
    const tgtLabel = tgt ? (tgt.props.label || tgt.type) : 'Missing field';

    const op = rule.when.operator;
    const val = rule.when.value;
    const whenText =
        op === 'isEmpty'
            ? `${srcLabel} is empty`
            : `${srcLabel} ${op === 'notEquals' ? 'does not equal' : op === 'contains' ? 'contains' : 'equals'} ${val ?? ''}`.trim();

    const actionText =
        rule.then.action === 'unrequire'
            ? 'Unrequire'
            : rule.then.action.charAt(0).toUpperCase() + rule.then.action.slice(1);

    return `If ${whenText} → ${actionText} ${tgtLabel}`;
}

export const LogicPanel: React.FC = () => {
    const {
        formDefinition,
        activePageId,
        addRule,
        updateRule,
        removeRule,
        swapRules,
        toggleRuleEnabled,
    } = useBuilderStore();

    const [filter, setFilter] = React.useState<FilterMode>('all');
    const [editingRuleId, setEditingRuleId] = React.useState<string | null>(null);
    const [draft, setDraft] = React.useState<Partial<LogicRule> | null>(null);
    const [draftErrors, setDraftErrors] = React.useState<Record<string, string>>({});
    const [searchSource, setSearchSource] = React.useState('');
    const [searchTarget, setSearchTarget] = React.useState('');

    const savedRules = formDefinition?.logic?.rules || [];
    const isCreatingNew = !!(editingRuleId && draft && !savedRules.some(r => r.id === editingRuleId));
    const displayRules: LogicRule[] = isCreatingNew && draft ? [...savedRules, draft as LogicRule] : savedRules;
    const currentPage = formDefinition?.pages.find(p => p.id === activePageId);
    const allComponents = currentPage ? flattenComponents(currentPage.components) : [];
    const fieldComponents = allComponents.filter(c => isFieldLike(c.type));

    const componentsById = React.useMemo(() => {
        const map: Record<string, FormComponent> = {};
        fieldComponents.forEach(c => {
            map[c.id] = c;
        });
        return map;
    }, [fieldComponents]);

    const ruleErrorsById = React.useMemo(() => {
        const m: Record<string, ReturnType<typeof validateRule>> = {};
        displayRules.forEach(r => {
            m[r.id] = validateRule(r, componentsById);
        });
        return m;
    }, [displayRules, componentsById]);

    const errorCount = Object.values(ruleErrorsById).filter(errs => errs.length > 0).length;

    const filteredRules = displayRules.filter(r => {
        const hasErrors = (ruleErrorsById[r.id] || []).length > 0;
        if (filter === 'enabled') return r.enabled;
        if (filter === 'errors') return hasErrors;
        return true;
    });

    // IMPORTANT: When the list is filtered (enabled/errors), "Move up/down" must operate on the
    // *displayed* (filtered) order, but apply the swap to the underlying saved rule list.
    const moveRuleInView = React.useCallback(
        (ruleId: string, direction: 'up' | 'down') => {
            const idx = filteredRules.findIndex(r => r.id === ruleId);
            if (idx === -1) return;
            const neighborIdx = direction === 'up' ? idx - 1 : idx + 1;
            if (neighborIdx < 0 || neighborIdx >= filteredRules.length) return;
            const neighborId = filteredRules[neighborIdx].id;
            swapRules(ruleId, neighborId);
        },
        [filteredRules, swapRules]
    );

    const startNewRule = () => {
        const id = makeId('rule');
        setEditingRuleId(id);
        setDraft({
            id,
            enabled: true,
            name: '',
            when: { sourceComponentId: '', operator: 'equals', value: '' },
            then: { targetComponentId: '', action: 'show' },
        } as LogicRule);
        setDraftErrors({});
        setSearchSource('');
        setSearchTarget('');
    };

    const startEditRule = (rule: LogicRule) => {
        setEditingRuleId(rule.id);
        setDraft(JSON.parse(JSON.stringify(rule)) as LogicRule);
        setDraftErrors({});
        setSearchSource('');
        setSearchTarget('');
    };

    const cancelEdit = () => {
        setEditingRuleId(null);
        setDraft(null);
        setDraftErrors({});
    };

    const normalizeForSave = (r: LogicRule): LogicRule | null => {
        const next: LogicRule = JSON.parse(JSON.stringify(r));

        // Normalize/guard value handling. Even though UI validation should prevent invalid rules,
        // this provides a safe backstop (e.g., import/API/state corruption).
        const op = next.when.operator;
        const requiresValue = op === 'equals' || op === 'notEquals' || op === 'contains';

        if (op === 'isEmpty') {
            delete next.when.value;
        } else if (requiresValue) {
            const cleaned = String(next.when.value ?? '').trim();
            if (cleaned.length === 0) return null;
            next.when.value = cleaned;
        } else if (typeof next.when.value === 'string') {
            next.when.value = next.when.value.trim();
        }

        if (next.name !== undefined) {
            const cleaned = String(next.name).trim();
            if (cleaned.length === 0) delete next.name;
            else next.name = cleaned;
        }
        return next;
    };

    const saveDraft = () => {
        if (!draft) return;
        const full = draft as LogicRule;
        const errs = validateRule(full, componentsById);
        if (errs.length > 0) {
            const map: Record<string, string> = {};
            errs.forEach(e => {
                // prefer first error per field
                if (!map[e.field]) map[e.field] = e.message;
            });
            setDraftErrors(map);
            return;
        }

        const normalized = normalizeForSave(full);
        if (!normalized) {
            setDraftErrors(prev => ({
                ...prev,
                value: 'Value is required for this operator.',
            }));
            return;
        }

        const exists = savedRules.some(r => r.id === normalized.id);
        if (exists) updateRule(normalized.id, normalized);
        else addRule(normalized);

        cancelEdit();
    };

    const operatorOptions = (sourceType: FormComponent['type'] | undefined) => {
        const allowed = allowedOperatorsForSourceType(sourceType);
        const labels: Record<LogicOperator, string> = {
            equals: 'Equals',
            notEquals: 'Not equals',
            contains: 'Contains',
            isEmpty: 'Is empty',
            greaterThan: 'Greater than',
            greaterThanOrEqual: 'Greater than or equal',
            lessThan: 'Less than',
            lessThanOrEqual: 'Less than or equal',
        };
        return allowed.map(op => ({ value: op, label: labels[op] }));
    };

    const sourceId = draft?.when?.sourceComponentId || '';
    const sourceComp = sourceId ? componentsById[sourceId] : undefined;
    const sourceType = sourceComp?.type;
    const sourceOptions = sourceComp?.props?.options || [];

    const isOptionsValuePicker =
        !!sourceComp &&
        ['select', 'radio', 'checkbox'].includes(sourceComp.type) &&
        Array.isArray(sourceOptions) &&
        sourceOptions.length > 0;

    const availableSources = fieldComponents
        .filter(c => getDisplayLabel(c).toLowerCase().includes(searchSource.toLowerCase()))
        .map(c => ({ id: c.id, label: getDisplayLabel(c) }));

    const availableTargets = fieldComponents
        .filter(c => c.id !== (draft?.when?.sourceComponentId || ''))
        .filter(c => getDisplayLabel(c).toLowerCase().includes(searchTarget.toLowerCase()))
        .map(c => ({ id: c.id, label: getDisplayLabel(c) }));

    return (
        <div className="flex flex-col h-full">
            {/* Header */}
            <div className="p-4 border-b border-gray-200 dark:border-gray-700 bg-gradient-to-r from-indigo-50 to-purple-50 dark:from-indigo-900/20 dark:to-purple-900/20">
                <div className="flex items-center justify-between gap-2">
                    <div className="flex items-center gap-2">
                        <GitBranch className="text-indigo-500" size={18} />
                        <div>
                            <h3 className="font-semibold text-gray-800 dark:text-gray-200">Logic</h3>
                            <p className="text-xs text-gray-500 dark:text-gray-400">
                                Rules are saved now; they take effect when the evaluation engine ships (Story 3.7).
                            </p>
                        </div>
                    </div>
                    <button
                        onClick={startNewRule}
                        className="btn-primary text-xs py-1.5 px-3 flex items-center gap-2"
                        title="Add Rule"
                    >
                        <Plus size={14} /> Add Rule
                    </button>
                </div>

                {/* Filters */}
                <div className="mt-3 flex items-center gap-2">
                    <button
                        onClick={() => setFilter('all')}
                        className={`px-2 py-1 rounded text-[11px] border ${
                            filter === 'all'
                                ? 'bg-white dark:bg-gray-900 border-indigo-300 dark:border-indigo-700 text-indigo-700 dark:text-indigo-300'
                                : 'bg-transparent border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-300 hover:bg-white/60 dark:hover:bg-gray-900/40'
                        }`}
                    >
                        All ({displayRules.length})
                    </button>
                    <button
                        onClick={() => setFilter('enabled')}
                        className={`px-2 py-1 rounded text-[11px] border ${
                            filter === 'enabled'
                                ? 'bg-white dark:bg-gray-900 border-indigo-300 dark:border-indigo-700 text-indigo-700 dark:text-indigo-300'
                                : 'bg-transparent border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-300 hover:bg-white/60 dark:hover:bg-gray-900/40'
                        }`}
                    >
                        Enabled ({displayRules.filter(r => r.enabled).length})
                    </button>
                    <button
                        onClick={() => setFilter('errors')}
                        className={`px-2 py-1 rounded text-[11px] border flex items-center gap-1 ${
                            filter === 'errors'
                                ? 'bg-white dark:bg-gray-900 border-red-300 dark:border-red-700 text-red-700 dark:text-red-300'
                                : 'bg-transparent border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-300 hover:bg-white/60 dark:hover:bg-gray-900/40'
                        }`}
                        title="Rules with errors"
                    >
                        With errors
                        {errorCount > 0 && (
                            <span className="ml-1 px-1.5 py-0.5 text-[10px] rounded bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300">
                                {errorCount}
                            </span>
                        )}
                    </button>
                </div>
            </div>

            {/* Content */}
            <div className="flex-1 overflow-y-scroll p-4 space-y-3">
                {savedRules.length === 0 && !isCreatingNew && (
                    <div className="text-sm text-gray-500 dark:text-gray-400 border border-dashed border-gray-300 dark:border-gray-700 rounded-lg p-4">
                        No rules yet. Click <strong>Add Rule</strong> to create your first condition.
                    </div>
                )}

                {filteredRules.map((rule, idx) => {
                    const errs = ruleErrorsById[rule.id] || [];
                    const hasErrors = errs.length > 0;
                    const isEditing = editingRuleId === rule.id;
                    const isDraftRow = isCreatingNew && isEditing;
                    const realIdx = savedRules.findIndex(r => r.id === rule.id);

                    return (
                        <div
                            key={rule.id}
                            className={`rounded-lg border ${
                                hasErrors
                                    ? 'border-red-200 dark:border-red-900/50 bg-red-50/50 dark:bg-red-900/10'
                                    : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900'
                            }`}
                        >
                            <div className="p-3 flex items-start justify-between gap-3">
                                <div className="flex items-start gap-3 flex-1">
                                    <input
                                        type="checkbox"
                                        checked={rule.enabled}
                                        onChange={(e) => {
                                            if (isDraftRow && draft) {
                                                setDraft({ ...(draft as any), enabled: e.target.checked });
                                                return;
                                            }
                                            toggleRuleEnabled(rule.id, e.target.checked);
                                        }}
                                        className="mt-1 accent-indigo-500"
                                        title="Enabled"
                                    />
                                    <div className="min-w-0 flex-1">
                                        <div className="flex items-center gap-2">
                                            <div className="text-xs font-medium text-gray-800 dark:text-gray-200 truncate">
                                                {rule.name ? rule.name : (isDraftRow ? 'New rule (draft)' : `Rule ${realIdx + 1}`)}
                                            </div>
                                            {hasErrors ? (
                                                <span className="inline-flex items-center gap-1 text-[10px] px-2 py-0.5 rounded bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300">
                                                    <AlertTriangle size={12} /> Needs attention
                                                </span>
                                            ) : (
                                                <span className="inline-flex items-center gap-1 text-[10px] px-2 py-0.5 rounded bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300">
                                                    <CheckCircle2 size={12} /> OK
                                                </span>
                                            )}
                                        </div>
                                        <div className="text-[11px] text-gray-600 dark:text-gray-400 mt-1">
                                            {summarizeRule(rule, componentsById)}
                                        </div>
                                        {hasErrors && (
                                            <div className="mt-2 text-[11px] text-red-700 dark:text-red-300">
                                                {errs[0]?.message}
                                            </div>
                                        )}
                                    </div>
                                </div>

                                <div className="flex items-center gap-1 flex-shrink-0">
                                    <button
                                        onClick={() => moveRuleInView(rule.id, 'up')}
                                        className="p-1.5 rounded hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-500"
                                        title="Move up"
                                        disabled={isDraftRow || idx <= 0}
                                    >
                                        <ArrowUp size={14} />
                                    </button>
                                    <button
                                        onClick={() => moveRuleInView(rule.id, 'down')}
                                        className="p-1.5 rounded hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-500"
                                        title="Move down"
                                        disabled={isDraftRow || idx === -1 || idx >= filteredRules.length - 1}
                                    >
                                        <ArrowDown size={14} />
                                    </button>
                                    <button
                                        onClick={() => (isEditing ? cancelEdit() : startEditRule(rule))}
                                        className="p-1.5 rounded hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-500"
                                        title={isDraftRow ? 'Close editor' : (isEditing ? 'Close editor' : 'Edit')}
                                    >
                                        <Pencil size={14} />
                                    </button>
                                    <button
                                        onClick={() => {
                                            if (isDraftRow) {
                                                cancelEdit();
                                                return;
                                            }
                                            if (window.confirm('Delete this rule?')) removeRule(rule.id);
                                        }}
                                        className="p-1.5 rounded hover:bg-gray-100 dark:hover:bg-gray-800 text-red-600 dark:text-red-400"
                                        title={isDraftRow ? 'Discard draft' : 'Delete'}
                                    >
                                        <Trash2 size={14} />
                                    </button>
                                </div>
                            </div>

                            {isEditing && draft && (
                                <div className="px-3 pb-3">
                                    <div className="border-t border-gray-200 dark:border-gray-700 pt-3 space-y-3">
                                        {/* Rule name */}
                                        <div>
                                            <label className="block text-[11px] font-medium text-gray-700 dark:text-gray-300 mb-1">
                                                Rule name (optional)
                                            </label>
                                            <input
                                                value={(draft.name as string) || ''}
                                                onChange={(e) => setDraft({ ...draft, name: e.target.value })}
                                                className="w-full px-2 py-1.5 text-sm rounded border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900"
                                                placeholder="e.g., Show Company when Opt-in is Yes"
                                            />
                                        </div>

                                        {/* IF */}
                                        <div className="grid grid-cols-1 gap-3">
                                            <div className="text-[11px] font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
                                                If
                                            </div>

                                            <div>
                                                <label className="block text-[11px] font-medium text-gray-700 dark:text-gray-300 mb-1">
                                                    Source field
                                                </label>
                                                <div className="flex items-center gap-2 mb-1">
                                                    <div className="relative flex-1">
                                                        <Search size={14} className="absolute left-2 top-2 text-gray-400" />
                                                        <input
                                                            value={searchSource}
                                                            onChange={(e) => setSearchSource(e.target.value)}
                                                            className="w-full pl-7 pr-2 py-1.5 text-sm rounded border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900"
                                                            placeholder="Search fields..."
                                                        />
                                                    </div>
                                                </div>
                                                <select
                                                    value={draft.when?.sourceComponentId || ''}
                                                    onChange={(e) => {
                                                        const nextSource = e.target.value;
                                                        const nextType = componentsById[nextSource]?.type;
                                                        const allowedOps = allowedOperatorsForSourceType(nextType);
                                                        const currentOp = draft.when?.operator;
                                                        const nextOp = currentOp && allowedOps.includes(currentOp) ? currentOp : allowedOps[0];
                                                        setDraft({
                                                            ...draft,
                                                            when: {
                                                                ...draft.when,
                                                                sourceComponentId: nextSource,
                                                                operator: nextOp,
                                                            },
                                                        });
                                                        setDraftErrors(prev => ({ ...prev, source: '' }));
                                                    }}
                                                    className="w-full px-2 py-1.5 text-sm rounded border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900"
                                                >
                                                    <option value="">Select a field…</option>
                                                    {availableSources.map(o => (
                                                        <option key={o.id} value={o.id}>
                                                            {o.label}
                                                        </option>
                                                    ))}
                                                </select>
                                                {draftErrors.source && (
                                                    <div className="mt-1 text-[11px] text-red-700 dark:text-red-300">{draftErrors.source}</div>
                                                )}
                                            </div>

                                            <div>
                                                <label className="block text-[11px] font-medium text-gray-700 dark:text-gray-300 mb-1">
                                                    Operator
                                                </label>
                                                <select
                                                    value={draft.when?.operator || ''}
                                                    onChange={(e) => {
                                                        const op = e.target.value as LogicOperator;
                                                        const nextWhen = { ...(draft.when || {}) };
                                                        nextWhen.operator = op;
                                                        if (op === 'isEmpty') delete nextWhen.value;
                                                        setDraft({ ...draft, when: nextWhen as any });
                                                        setDraftErrors(prev => ({ ...prev, operator: '', value: '' }));
                                                    }}
                                                    className="w-full px-2 py-1.5 text-sm rounded border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900"
                                                    disabled={!draft.when?.sourceComponentId}
                                                >
                                                    <option value="">Select an operator…</option>
                                                    {operatorOptions(sourceType).map(o => (
                                                        <option key={o.value} value={o.value}>
                                                            {o.label}
                                                        </option>
                                                    ))}
                                                </select>
                                                {draftErrors.operator && (
                                                    <div className="mt-1 text-[11px] text-red-700 dark:text-red-300">{draftErrors.operator}</div>
                                                )}
                                            </div>

                                            <div>
                                                <label className="block text-[11px] font-medium text-gray-700 dark:text-gray-300 mb-1">
                                                    Value
                                                </label>

                                                {draft.when?.operator === 'isEmpty' ? (
                                                    <div className="text-[11px] text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-800 p-2 rounded border border-gray-200 dark:border-gray-700">
                                                        No value needed for “is empty”.
                                                    </div>
                                                ) : isOptionsValuePicker ? (
                                                    <select
                                                        value={draft.when?.value || ''}
                                                        onChange={(e) => {
                                                            setDraft({
                                                                ...draft,
                                                                when: { ...draft.when!, value: e.target.value },
                                                            });
                                                            setDraftErrors(prev => ({ ...prev, value: '' }));
                                                        }}
                                                        className="w-full px-2 py-1.5 text-sm rounded border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900"
                                                        disabled={!draft.when?.operator}
                                                    >
                                                        <option value="">Select a value…</option>
                                                        {sourceOptions.map(opt => (
                                                            <option key={opt.value} value={opt.value}>
                                                                {opt.label}
                                                            </option>
                                                        ))}
                                                    </select>
                                                ) : (
                                                    <input
                                                        value={draft.when?.value || ''}
                                                        onChange={(e) => {
                                                            setDraft({
                                                                ...draft,
                                                                when: { ...draft.when!, value: e.target.value },
                                                            });
                                                            setDraftErrors(prev => ({ ...prev, value: '' }));
                                                        }}
                                                        className="w-full px-2 py-1.5 text-sm rounded border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900"
                                                        placeholder="Enter a value…"
                                                        disabled={!draft.when?.operator || !draft.when?.sourceComponentId}
                                                    />
                                                )}

                                                {draftErrors.value && (
                                                    <div className="mt-1 text-[11px] text-red-700 dark:text-red-300">{draftErrors.value}</div>
                                                )}
                                            </div>
                                        </div>

                                        {/* THEN */}
                                        <div className="grid grid-cols-1 gap-3">
                                            <div className="text-[11px] font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
                                                Then
                                            </div>

                                            <div>
                                                <label className="block text-[11px] font-medium text-gray-700 dark:text-gray-300 mb-1">
                                                    Target field
                                                </label>
                                                <div className="flex items-center gap-2 mb-1">
                                                    <div className="relative flex-1">
                                                        <Search size={14} className="absolute left-2 top-2 text-gray-400" />
                                                        <input
                                                            value={searchTarget}
                                                            onChange={(e) => setSearchTarget(e.target.value)}
                                                            className="w-full pl-7 pr-2 py-1.5 text-sm rounded border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900"
                                                            placeholder="Search fields..."
                                                        />
                                                    </div>
                                                </div>
                                                <select
                                                    value={draft.then?.targetComponentId || ''}
                                                    onChange={(e) => {
                                                        setDraft({
                                                            ...draft,
                                                            then: { ...draft.then!, targetComponentId: e.target.value },
                                                        });
                                                        setDraftErrors(prev => ({ ...prev, target: '', general: '' }));
                                                    }}
                                                    className="w-full px-2 py-1.5 text-sm rounded border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900"
                                                >
                                                    <option value="">Select a field…</option>
                                                    {availableTargets.map(o => (
                                                        <option key={o.id} value={o.id}>
                                                            {o.label}
                                                        </option>
                                                    ))}
                                                </select>
                                                {draftErrors.target && (
                                                    <div className="mt-1 text-[11px] text-red-700 dark:text-red-300">{draftErrors.target}</div>
                                                )}
                                            </div>

                                            <div>
                                                <label className="block text-[11px] font-medium text-gray-700 dark:text-gray-300 mb-1">
                                                    Action
                                                </label>
                                                <select
                                                    value={draft.then?.action || ''}
                                                    onChange={(e) => {
                                                        setDraft({
                                                            ...draft,
                                                            then: { ...draft.then!, action: e.target.value as any },
                                                        });
                                                        setDraftErrors(prev => ({ ...prev, action: '' }));
                                                    }}
                                                    className="w-full px-2 py-1.5 text-sm rounded border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900"
                                                >
                                                    <option value="">Select an action…</option>
                                                    {ALL_ACTIONS.map(a => (
                                                        <option key={a.value} value={a.value}>
                                                            {a.label}
                                                        </option>
                                                    ))}
                                                </select>
                                                {draftErrors.action && (
                                                    <div className="mt-1 text-[11px] text-red-700 dark:text-red-300">{draftErrors.action}</div>
                                                )}
                                            </div>
                                        </div>

                                        {draftErrors.general && (
                                            <div className="text-[11px] text-red-700 dark:text-red-300 flex items-center gap-2">
                                                <AlertTriangle size={14} /> {draftErrors.general}
                                            </div>
                                        )}

                                        <div className="flex items-center gap-2 pt-2">
                                            <button onClick={saveDraft} className="btn-primary text-xs py-1.5 px-3">
                                                Save rule
                                            </button>
                                            <button onClick={cancelEdit} className="btn-secondary text-xs py-1.5 px-3">
                                                Cancel
                                            </button>
                                            <div className="text-[11px] text-gray-500 dark:text-gray-400 flex items-center gap-1">
                                                <ChevronDown size={12} className="opacity-0" />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    );
                })}

            </div>
        </div>
    );
};

