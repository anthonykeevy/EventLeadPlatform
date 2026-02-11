import React from 'react';
import type { FormComponent, FormDefinition } from '../../types/builder.types';
import { evaluateRules } from '../../../logic-engine/evaluateRules';
import type { ComponentRuntimeState } from '../../../logic-engine/types';
import { useBuilderStore } from '../../stores/useBuilderStore';

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

function isRenderableField(_type: FormComponent['type']): boolean {
  // Non-input display components are still renderable but not value-bearing.
  return true;
}

function sortByPositionStable(a: FormComponent, b: FormComponent): number {
  const ay = a.position?.y ?? 0;
  const by = b.position?.y ?? 0;
  if (ay !== by) return ay - by;
  const ax = a.position?.x ?? 0;
  const bx = b.position?.x ?? 0;
  if (ax !== bx) return ax - bx;
  return a.id.localeCompare(b.id);
}

function getBaseRequired(component: FormComponent): boolean {
  // Builder schema supports required flag; also support validation.required as fallback.
  const requiredFromProps = component.props.required;
  const requiredFromValidation = (component.props.validation as any)?.required;
  return Boolean(requiredFromProps ?? requiredFromValidation ?? false);
}

type ValueMap = Record<string, unknown>;

type FieldErrorMap = Record<string, string>;

export const RuntimeFormView: React.FC<{ definition: FormDefinition; title?: string }> = ({ definition, title }) => {
  const { setRuntimeWarnings, clearRuntimeWarnings } = useBuilderStore(state => ({
    setRuntimeWarnings: state.setRuntimeWarnings,
    clearRuntimeWarnings: state.clearRuntimeWarnings,
  }));
  const page = definition.pages?.[0];
  const components = React.useMemo(() => {
    if (!page) return [];
    return flattenComponents(page.components).filter(c => isRenderableField(c.type));
  }, [page]);
  const sorted = React.useMemo(() => [...components].sort(sortByPositionStable), [components]);

  const componentsById = React.useMemo(() => {
    const map: Record<string, FormComponent> = {};
    for (const c of sorted) map[c.id] = c;
    return map;
  }, [sorted]);

  const baseStateById = React.useMemo(() => {
    const base: Record<string, ComponentRuntimeState> = {};
    for (const c of sorted) {
      base[c.id] = {
        visible: true,
        enabled: true,
        required: getBaseRequired(c),
      };
    }
    return base;
  }, [sorted]);

  const rules = definition.logic?.rules ?? [];

  const [values, setValues] = React.useState<ValueMap>({});
  const [showValidation, setShowValidation] = React.useState(false);

  const { stateById, warnings } = React.useMemo(() => {
    return evaluateRules({
      rules,
      valuesByComponentId: values,
      componentsById,
      baseStateById,
    });
  }, [rules, values, componentsById, baseStateById]);

  // Surface warnings in shared UI (builder header etc.) without creating a render loop.
  const warningsSignature = React.useMemo(() => {
    if (!warnings.length) return '';
    return warnings
      .map(w => `${w.ruleId}:${w.code}:${w.sourceComponentId ?? ''}:${w.targetComponentId ?? ''}:${w.message}`)
      .join('|');
  }, [warnings]);

  const lastWarningsSignatureRef = React.useRef<string>('');
  const storeWarningsLen = useBuilderStore(state => state.runtimeWarnings.length);
  React.useEffect(() => {
    // Ensure the store is cleared when warnings transition to empty.
    if (!warnings.length) {
      lastWarningsSignatureRef.current = '';
      if (storeWarningsLen !== 0) setRuntimeWarnings([]);
      return;
    }

    if (warningsSignature === lastWarningsSignatureRef.current) return;
    lastWarningsSignatureRef.current = warningsSignature;
    setRuntimeWarnings(warnings);
  }, [warningsSignature, warnings, setRuntimeWarnings, storeWarningsLen]);

  React.useEffect(() => {
    return () => {
      lastWarningsSignatureRef.current = '';
      clearRuntimeWarnings();
    };
  }, [clearRuntimeWarnings]);

  const errors: FieldErrorMap = React.useMemo(() => {
    if (!showValidation) return {};
    const next: FieldErrorMap = {};
    for (const c of sorted) {
      const runtime = stateById[c.id];
      if (!runtime?.visible) continue;
      if (!runtime?.required) continue;

      const v = values[c.id];
      // Important: boolean false is a deliberate value (e.g., unchecked checkbox) and is NOT "empty".
      // Only truly empty values (null/undefined/empty string/empty array) should fail required validation.
      const isEmpty =
        v === null ||
        v === undefined ||
        (typeof v === 'string' && v.trim().length === 0) ||
        (Array.isArray(v) && v.length === 0);
      if (isEmpty) {
        next[c.id] = 'This field is required.';
      }
    }
    return next;
  }, [showValidation, sorted, stateById, values]);

  const setValue = (id: string, v: unknown) => {
    setValues(prev => ({ ...prev, [id]: v }));
  };

  const reset = () => {
    setValues({});
    setShowValidation(false);
  };

  return (
    <div className="max-w-3xl mx-auto p-6">
      <div className="flex items-center justify-between gap-3 mb-4">
        <div>
          <h2 className="text-xl font-semibold text-gray-900">{title ?? 'Preview'}</h2>
          <p className="text-sm text-gray-500">Runtime rules apply live as you change values.</p>
        </div>
        <div className="flex items-center gap-2">
          <button className="btn-secondary text-sm" onClick={() => setShowValidation(true)}>
            Validate
          </button>
          <button className="btn-secondary text-sm" onClick={reset}>
            Reset
          </button>
        </div>
      </div>

      {warnings.length > 0 && (
        <div className="mb-4 rounded border border-yellow-200 bg-yellow-50 p-3 text-sm text-yellow-900">
          <div className="font-medium">Warnings</div>
          <ul className="list-disc pl-5 mt-1">
            {warnings.map(w => (
              <li key={`${w.ruleId}-${w.code}-${w.sourceComponentId ?? ''}-${w.targetComponentId ?? ''}`}>{w.message}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="space-y-4">
        {sorted.map(c => {
          const runtime = stateById[c.id] ?? { visible: true, enabled: true, required: getBaseRequired(c) };
          if (!runtime.visible) return null;

          const label = (c.props.label || c.type).toString();
          const required = runtime.required;
          const disabled = !runtime.enabled;
          const helpText = c.props.helpText as string | undefined;
          const placeholder = c.props.placeholder as string | undefined;
          const err = errors[c.id];

          const commonLabel = (
            <label className="block text-sm font-medium text-gray-800 mb-1">
              {label}
              {required && <span className="text-red-600"> *</span>}
            </label>
          );

          const commonError = err ? <div className="mt-1 text-sm text-red-700">{err}</div> : null;
          const commonHelp = helpText ? <div className="mt-1 text-sm text-gray-500">{helpText}</div> : null;

          const baseInputClass = `w-full rounded-md border px-3 py-2 text-sm ${
            err ? 'border-red-300 focus:ring-red-400 focus:border-red-400' : 'border-gray-300 focus:ring-teal-500 focus:border-teal-500'
          } ${disabled ? 'bg-gray-100 text-gray-500 cursor-not-allowed' : 'bg-white'} `;

          switch (c.type) {
            case 'textarea':
              return (
                <div key={c.id}>
                  {commonLabel}
                  <textarea
                    className={baseInputClass}
                    placeholder={placeholder}
                    disabled={disabled}
                    value={(values[c.id] as string) ?? ''}
                    onChange={e => setValue(c.id, e.target.value)}
                  />
                  {commonError}
                  {commonHelp}
                </div>
              );

            case 'select':
              return (
                <div key={c.id}>
                  {commonLabel}
                  <select
                    className={baseInputClass}
                    disabled={disabled}
                    value={(values[c.id] as string) ?? ''}
                    onChange={e => setValue(c.id, e.target.value)}
                  >
                    <option value="">{placeholder ?? 'Select…'}</option>
                    {(c.props.options as any[] | undefined)?.map(opt => (
                      <option key={opt.value} value={opt.value} disabled={Boolean(opt.disabled)}>
                        {opt.label}
                      </option>
                    ))}
                  </select>
                  {commonError}
                  {commonHelp}
                </div>
              );

            case 'checkbox':
              return (
                <div key={c.id} className="flex items-start gap-3">
                  <input
                    type="checkbox"
                    className="mt-1"
                    disabled={disabled}
                    checked={Boolean(values[c.id])}
                    onChange={e => setValue(c.id, e.target.checked)}
                  />
                  <div className="flex-1">
                    <div className="text-sm font-medium text-gray-800">
                      {label}
                      {required && <span className="text-red-600"> *</span>}
                    </div>
                    {commonError}
                    {commonHelp}
                  </div>
                </div>
              );

            case 'radio':
              return (
                <div key={c.id}>
                  {commonLabel}
                  <div className="space-y-2">
                    {(c.props.options as any[] | undefined)?.map(opt => (
                      <label key={opt.value} className="flex items-center gap-2 text-sm text-gray-700">
                        <input
                          type="radio"
                          name={c.id}
                          value={opt.value}
                          disabled={disabled || Boolean(opt.disabled)}
                          checked={(values[c.id] as string) === opt.value}
                          onChange={() => setValue(c.id, opt.value)}
                        />
                        <span>{opt.label}</span>
                      </label>
                    ))}
                  </div>
                  {commonError}
                  {commonHelp}
                </div>
              );

            case 'header':
              return (
                <div key={c.id}>
                  <h3 className="text-lg font-semibold text-gray-900">{label}</h3>
                </div>
              );

            case 'paragraph':
              return (
                <div key={c.id}>
                  <p className="text-gray-700">{label}</p>
                </div>
              );

            case 'divider':
              return <hr key={c.id} className="border-gray-200" />;

            default: {
              const inputType =
                c.type === 'email' ? 'email' : c.type === 'number' ? 'number' : c.type === 'date' ? 'date' : 'text';
              return (
                <div key={c.id}>
                  {commonLabel}
                  <input
                    className={baseInputClass}
                    type={inputType}
                    placeholder={placeholder}
                    disabled={disabled}
                    value={(values[c.id] as string) ?? ''}
                    onChange={e => setValue(c.id, e.target.value)}
                  />
                  {commonError}
                  {commonHelp}
                </div>
              );
            }
          }
        })}
      </div>
    </div>
  );
};
