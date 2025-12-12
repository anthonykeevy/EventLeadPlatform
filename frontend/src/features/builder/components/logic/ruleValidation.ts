import { FormComponent, LogicAction, LogicOperator, LogicRule } from '../../types/builder.types';

export type RuleValidationField =
  | 'name'
  | 'source'
  | 'operator'
  | 'value'
  | 'target'
  | 'action'
  | 'broken'
  | 'general';

export interface RuleValidationError {
  field: RuleValidationField;
  message: string;
}

const TEXT_CAPABLE = new Set<FormComponent['type']>(['text', 'textarea', 'email', 'phone', 'first-name']);

export function isTextCapableComponent(type: FormComponent['type']): boolean {
  return TEXT_CAPABLE.has(type);
}

export function allowedOperatorsForSourceType(type: FormComponent['type'] | undefined): LogicOperator[] {
  if (!type) return ['equals', 'notEquals', 'isEmpty'];
  const base: LogicOperator[] = ['equals', 'notEquals', 'isEmpty'];
  return isTextCapableComponent(type) ? [...base, 'contains'] : base;
}

export const ALL_ACTIONS: Array<{ value: LogicAction; label: string }> = [
  { value: 'show', label: 'Show' },
  { value: 'hide', label: 'Hide' },
  { value: 'require', label: 'Require' },
  { value: 'unrequire', label: 'Unrequire' },
  { value: 'enable', label: 'Enable' },
  { value: 'disable', label: 'Disable' },
];

export function validateRule(rule: Partial<LogicRule>, componentsById: Record<string, FormComponent>): RuleValidationError[] {
  const errors: RuleValidationError[] = [];

  const sourceId = rule.when?.sourceComponentId;
  const targetId = rule.then?.targetComponentId;
  const operator = rule.when?.operator;
  const action = rule.then?.action;

  if (!sourceId) errors.push({ field: 'source', message: 'Choose a source field.' });
  if (!operator) errors.push({ field: 'operator', message: 'Choose an operator.' });
  if (!targetId) errors.push({ field: 'target', message: 'Choose a target field.' });
  if (!action) errors.push({ field: 'action', message: 'Choose an action.' });

  if (sourceId && targetId && sourceId === targetId) {
    errors.push({ field: 'general', message: 'Source field cannot be the same as target field.' });
  }

  if (sourceId && !componentsById[sourceId]) {
    errors.push({ field: 'broken', message: 'Source field was deleted.' });
  }
  if (targetId && !componentsById[targetId]) {
    errors.push({ field: 'broken', message: 'Target field was deleted.' });
  }

  const sourceType = sourceId ? componentsById[sourceId]?.type : undefined;
  if (operator === 'contains' && sourceType && !isTextCapableComponent(sourceType)) {
    errors.push({ field: 'operator', message: 'Contains is only available for text fields.' });
  }

  const value = rule.when?.value;
  const requiresValue = operator === 'equals' || operator === 'notEquals' || operator === 'contains';
  if (requiresValue && (!value || String(value).trim() === '')) {
    errors.push({ field: 'value', message: `Value is required for ${operator}.` });
  }
  if (operator === 'isEmpty' && value !== undefined && String(value).trim() !== '') {
    errors.push({ field: 'value', message: 'Value is not used for “is empty”.' });
  }

  return errors;
}

