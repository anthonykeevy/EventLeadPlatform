export type RuntimeRuleWarningCode =
  | 'missing_source'
  | 'missing_target'
  | 'invalid_operator'
  | 'invalid_value';

export interface RuntimeRuleWarning {
  ruleId: string;
  code: RuntimeRuleWarningCode;
  message: string;
  /** Optional component ids to help UI highlight issues */
  sourceComponentId?: string;
  targetComponentId?: string;
}

export interface ComponentRuntimeState {
  visible: boolean;
  enabled: boolean;
  required: boolean;
}

export type ComponentRuntimeStateById = Record<string, ComponentRuntimeState>;
