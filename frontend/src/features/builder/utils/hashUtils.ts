// Stable stringify + lightweight hash for client-side dedupe.
// Goal: avoid unnecessary Save calls when DefinitionJSON hasn't changed.

export function stableStringify(value: unknown): string {
  const seen = new WeakSet<object>()

  const stringify = (v: any): any => {
    if (v === null || v === undefined) return v

    const t = typeof v
    if (t === 'number' || t === 'boolean' || t === 'string') return v

    if (Array.isArray(v)) {
      return v.map(item => stringify(item))
    }

    if (t === 'object') {
      if (seen.has(v)) {
        // Cycles should not exist in DefinitionJSON; represent deterministically.
        return '[Circular]'
      }
      seen.add(v)

      const keys = Object.keys(v).sort()
      const out: Record<string, any> = {}
      for (const k of keys) {
        out[k] = stringify(v[k])
      }
      return out
    }

    // Functions/symbols should not be present; stringify deterministically.
    return String(v)
  }

  return JSON.stringify(stringify(value))
}

// FNV-1a 32-bit hash (fast, non-crypto). Suitable for dedupe keys.
export function fnv1a32(input: string): string {
  let hash = 0x811c9dc5
  for (let i = 0; i < input.length; i++) {
    hash ^= input.charCodeAt(i)
    // hash *= 16777619 with overflow
    hash = (hash + ((hash << 1) + (hash << 4) + (hash << 7) + (hash << 8) + (hash << 24))) >>> 0
  }
  return hash.toString(16).padStart(8, '0')
}

export function hashDefinition(definition: unknown): string {
  return fnv1a32(stableStringify(definition))
}
