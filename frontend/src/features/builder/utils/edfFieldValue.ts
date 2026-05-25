/** Shared helpers for EDF lookup field values (address / company). */

export const EDF_LOOKUP_COMPONENT_TYPES = ['address-lookup-au', 'company-lookup-abr'] as const;

export type EdfLookupComponentType = (typeof EDF_LOOKUP_COMPONENT_TYPES)[number];

export function isEdfLookupComponentType(type: string): type is EdfLookupComponentType {
  return (EDF_LOOKUP_COMPONENT_TYPES as readonly string[]).includes(type);
}

export function extractEdfDisplayText(value: unknown): string {
  if (value == null) return '';
  if (typeof value === 'string') return value;
  if (typeof value === 'object' && 'displayText' in (value as object)) {
    return String((value as { displayText?: string }).displayText ?? '');
  }
  return '';
}

export function isEdfFieldValueEmpty(value: unknown): boolean {
  return extractEdfDisplayText(value).trim().length === 0;
}
