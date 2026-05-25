export function normalizeAbnStatus(status: string | null | undefined): string {
  return (status ?? '').trim().toLowerCase();
}

export function isActiveAbnStatus(status: string | null | undefined): boolean {
  return normalizeAbnStatus(status) === 'active';
}

export function isInactiveAbnStatus(status: string | null | undefined): boolean {
  const normalized = normalizeAbnStatus(status);
  if (!normalized) return false;
  return normalized !== 'active';
}

/** Badge colours for ABR status in lookup results and post-select warnings. */
export function abnStatusPresentation(status: string | null | undefined): {
  label: string;
  className: string;
} | null {
  const raw = (status ?? '').trim();
  if (!raw) return null;

  const normalized = raw.toLowerCase();
  if (normalized === 'active') {
    return {
      label: raw,
      className:
        'inline-flex items-center rounded px-1.5 py-0.5 text-[10px] font-medium bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300',
    };
  }
  if (normalized.includes('cancel')) {
    return {
      label: raw,
      className:
        'inline-flex items-center rounded px-1.5 py-0.5 text-[10px] font-medium bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300',
    };
  }
  return {
    label: raw,
    className:
      'inline-flex items-center rounded px-1.5 py-0.5 text-[10px] font-medium bg-amber-100 text-amber-900 dark:bg-amber-900/30 dark:text-amber-200',
  };
}
