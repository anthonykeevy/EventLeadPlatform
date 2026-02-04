/**
 * Privacy-safe diagnostics for a value. This MUST NOT include raw values.
 * Used for validation-failure telemetry (Story 3.11).
 */
export type ValueDiagnostics = {
  type: 'null' | 'string' | 'number' | 'boolean' | 'array' | 'object' | 'unknown'
  length?: number
  trimmedLength?: number
  flags?: {
    hasWhitespace?: boolean
    hasPlus?: boolean
    digitCountBucket?: '0' | '1-3' | '4-7' | '8-12' | '13+'
  }
}

type DigitCountBucket = NonNullable<ValueDiagnostics['flags']>['digitCountBucket']

function toDigitCountBucket(digitCount: number): DigitCountBucket {
  if (digitCount <= 0) return '0'
  if (digitCount <= 3) return '1-3'
  if (digitCount <= 7) return '4-7'
  if (digitCount <= 12) return '8-12'
  return '13+'
}

export function getValueDiagnostics(value: unknown): ValueDiagnostics {
  if (value === null) {
    return { type: 'null' }
  }

  if (Array.isArray(value)) {
    return { type: 'array', length: value.length }
  }

  switch (typeof value) {
    case 'string': {
      const length = value.length
      const trimmedLength = value.trim().length
      const digitCount = value.match(/\d/g)?.length ?? 0

      return {
        type: 'string',
        length,
        trimmedLength,
        flags: {
          hasWhitespace: /\s/.test(value),
          hasPlus: value.includes('+'),
          digitCountBucket: toDigitCountBucket(digitCount),
        },
      }
    }
    case 'number':
      return { type: 'number' }
    case 'boolean':
      return { type: 'boolean' }
    case 'object':
      return { type: 'object' }
    default:
      return { type: 'unknown' }
  }
}

