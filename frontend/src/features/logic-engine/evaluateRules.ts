import type { FormComponent, LogicRule } from '../builder/types/builder.types';
import type {
  ComponentRuntimeState,
  ComponentRuntimeStateById,
  RuntimeRuleWarning,
} from './types';

export interface EvaluateRulesInput {
  rules: LogicRule[];
  /** Current values keyed by component id */
  valuesByComponentId: Record<string, unknown>;
  /** Components keyed by component id (used for reference validation + type-aware ops) */
  componentsById: Record<string, FormComponent | undefined>;
  /** Base/default state keyed by component id */
  baseStateById: ComponentRuntimeStateById;
}

export interface EvaluateRulesResult {
  stateById: ComponentRuntimeStateById;
  warnings: RuntimeRuleWarning[];
}

/**
 * Extracts the logical value from component payloads.
 * Radio/dropdown emit { value: string, extraTextByValue? }.
 * Checkbox with options emits { values: string[], extraTextByValue? }.
 * Logic rules compare against these logical values, not the raw JSON.
 */
function extractLogicalValue(v: unknown): unknown {
  if (v === null || v === undefined) return v;
  if (typeof v !== 'object' || Array.isArray(v)) return v;
  const o = v as Record<string, unknown>;
  if (typeof o.value === 'string') return o.value;
  if (Array.isArray(o.values)) return o.values;
  return v;
}

function isEmptyValue(v: unknown): boolean {
  const logical = extractLogicalValue(v);
  if (logical === null || logical === undefined) return true;
  if (typeof logical === 'string') return logical.trim().length === 0;
  if (Array.isArray(logical)) return logical.length === 0;
  return false;
}

function normalizeToString(v: unknown): string {
  const logical = extractLogicalValue(v);
  if (logical === null || logical === undefined) return '';
  if (typeof logical === 'string') return logical;
  if (typeof logical === 'number' || typeof logical === 'boolean') return String(logical);
  if (Array.isArray(logical)) {
    if (logical.length === 0) return '';
    if (logical.length === 1) return String(logical[0]);
    return logical.map((x) => String(x)).join(',');
  }
  // Best-effort fallback for other objects
  try {
    return JSON.stringify(v);
  } catch {
    return String(v);
  }
}

function evaluateWhen(rule: LogicRule, input: EvaluateRulesInput): { ok: boolean; warnings?: RuntimeRuleWarning[] } {
  const { componentsById, valuesByComponentId } = input;

  const sourceId = rule.when.sourceComponentId;
  const src = componentsById[sourceId];
  if (!src) {
    return {
      ok: false,
      warnings: [
        {
          ruleId: rule.id,
          code: 'missing_source',
          message: 'Rule ignored: source field is missing.',
          sourceComponentId: sourceId,
          targetComponentId: rule.then.targetComponentId,
        },
      ],
    };
  }

  const op = rule.when.operator;
  const actual = valuesByComponentId[sourceId];

  if (op === 'isEmpty') {
    const val = rule.when.value;
    // If malformed and value was supplied, ignore rule and warn.
    if (val != null && normalizeToString(val).trim() !== '') {
      return {
        ok: false,
        warnings: [
          {
            ruleId: rule.id,
            code: 'invalid_value',
            message: 'Rule ignored: value is not used for “is empty”.',
            sourceComponentId: sourceId,
            targetComponentId: rule.then.targetComponentId,
          },
        ],
      };
    }
    return { ok: isEmptyValue(actual) };
  }

  const requiresValue = op === 'equals' || op === 'notEquals' || op === 'contains';
  if (requiresValue) {
    const expectedRaw = rule.when.value;
    const expected = normalizeToString(expectedRaw).trim();
    if (expected.length === 0) {
      return {
        ok: false,
        warnings: [
          {
            ruleId: rule.id,
            code: 'invalid_value',
            message: `Rule ignored: value is required for ${op}.`,
            sourceComponentId: sourceId,
            targetComponentId: rule.then.targetComponentId,
          },
        ],
      };
    }

    // Normalize both sides consistently (trim) to avoid whitespace-sensitive mismatches.
    const actualStr = normalizeToString(actual).trim();

    if (op === 'equals') return { ok: actualStr === expected };
    if (op === 'notEquals') return { ok: actualStr !== expected };
    if (op === 'contains') return { ok: actualStr.includes(expected) };
  }

  return {
    ok: false,
    warnings: [
      {
        ruleId: rule.id,
        code: 'invalid_operator',
        message: 'Rule ignored: unsupported operator.',
        sourceComponentId: sourceId,
        targetComponentId: rule.then.targetComponentId,
      },
    ],
  };
}

function applyThenAction(state: ComponentRuntimeState, action: LogicRule['then']['action']): ComponentRuntimeState {
  // Last applicable wins is handled by sequential overwrite.
  switch (action) {
    case 'show':
      return { ...state, visible: true };
    case 'hide':
      return { ...state, visible: false };
    case 'enable':
      return { ...state, enabled: true };
    case 'disable':
      return { ...state, enabled: false };
    case 'require':
      return { ...state, required: true };
    case 'unrequire':
      return { ...state, required: false };
    default:
      return state;
  }
}

export function evaluateRules(input: EvaluateRulesInput): EvaluateRulesResult {
  const warnings: RuntimeRuleWarning[] = [];

  // Clone base state so we can mutate safely.
  const stateById: ComponentRuntimeStateById = {};
  for (const [id, state] of Object.entries(input.baseStateById)) {
    stateById[id] = { ...state };
  }

  for (const rule of input.rules) {
    if (!rule.enabled) continue;

    const targetId = rule.then.targetComponentId;
    const tgt = input.componentsById[targetId];
    if (!tgt) {
      warnings.push({
        ruleId: rule.id,
        code: 'missing_target',
        message: 'Rule ignored: target field is missing.',
        sourceComponentId: rule.when.sourceComponentId,
        targetComponentId: targetId,
      });
      continue;
    }

    const whenResult = evaluateWhen(rule, input);
    if (whenResult.warnings?.length) warnings.push(...whenResult.warnings);
    if (!whenResult.ok) continue;

    const prev = stateById[targetId] ?? { visible: true, enabled: true, required: false };
    stateById[targetId] = applyThenAction(prev, rule.then.action);
  }

  return { stateById, warnings };
}
