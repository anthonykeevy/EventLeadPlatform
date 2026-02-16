/**
 * Definition Resolver — Story 5.2 T06
 * Merges Global → Company → Form for preview and public renderer parity.
 * Same resolution order as backend resolve_definition_for_render.
 */

import type { FormDefinition } from '../types/builder.types';

/** Defaults from Init API (Global+Company merged) */
export type DefaultsLike = {
  theme?: unknown;
  globalStyles?: unknown;
  canvasSettings?: unknown;
} | null;

/**
 * Deep merge: override recursively overrides base.
 * Nested objects are merged; arrays and scalars are replaced.
 */
function deepMerge(
  base: Record<string, unknown>,
  override: Record<string, unknown>
): Record<string, unknown> {
  const result = { ...base };
  for (const key of Object.keys(override)) {
    const baseVal = result[key];
    const overrideVal = override[key];
    if (
      baseVal != null &&
      overrideVal != null &&
      typeof baseVal === 'object' &&
      !Array.isArray(baseVal) &&
      typeof overrideVal === 'object' &&
      !Array.isArray(overrideVal)
    ) {
      result[key] = deepMerge(
        baseVal as Record<string, unknown>,
        overrideVal as Record<string, unknown>
      );
    } else {
      result[key] = overrideVal;
    }
  }
  return result;
}

/**
 * Resolve definition for render: merges defaults (Global+Company) with form overrides.
 * Use in builder preview when initDefaults exists; matches public renderer behavior.
 */
export function resolveDefinitionForRender(
  defaults: DefaultsLike,
  formDefinition: FormDefinition
): FormDefinition {
  if (!defaults) {
    return formDefinition;
  }

  const result = { ...formDefinition };

  // Theme: form overrides merge over defaults
  const baseTheme: Record<string, unknown> = defaults.theme && typeof defaults.theme === 'object'
    ? (defaults.theme as Record<string, unknown>)
    : {};
  const formTheme = formDefinition.theme;
  result.theme = (formTheme
    ? deepMerge(baseTheme, formTheme as unknown as Record<string, unknown>)
    : baseTheme) as unknown as FormDefinition['theme'];

  // GlobalStyles: form overrides merge over defaults
  const baseGs: Record<string, unknown> = defaults.globalStyles && typeof defaults.globalStyles === 'object'
    ? (defaults.globalStyles as Record<string, unknown>)
    : {};
  const formGs = formDefinition.globalStyles;
  result.globalStyles = (formGs
    ? deepMerge(baseGs, formGs as unknown as Record<string, unknown>)
    : baseGs) as unknown as FormDefinition['globalStyles'];

  // CanvasSettings: form overrides merge over defaults
  const baseCanvas: Record<string, unknown> = defaults.canvasSettings && typeof defaults.canvasSettings === 'object'
    ? (defaults.canvasSettings as Record<string, unknown>)
    : {};
  const formCanvas = formDefinition.canvasSettings;
  result.canvasSettings = (formCanvas
    ? deepMerge(baseCanvas, formCanvas as unknown as Record<string, unknown>)
    : baseCanvas) as unknown as FormDefinition['canvasSettings'];

  return result;
}
