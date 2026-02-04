import { describe, expect, it } from 'vitest'
import { getValueDiagnostics } from './valueDiagnostics'

describe('getValueDiagnostics', () => {
  it('returns privacy-safe diagnostics for strings (no raw value)', () => {
    const diag = getValueDiagnostics('  test  ')

    expect(diag.type).toBe('string')
    expect(diag.length).toBe(8)
    expect(diag.trimmedLength).toBe(4)
    expect(diag.flags?.hasWhitespace).toBe(true)
    expect(diag.flags?.hasPlus).toBe(false)

    // Ensure we never include raw values in telemetry payloads.
    expect(JSON.stringify(diag)).not.toContain('test')
  })

  it('returns safe shape info for arrays and objects', () => {
    expect(getValueDiagnostics(['a', 'b'])).toEqual({ type: 'array', length: 2 })
    expect(getValueDiagnostics({ a: 1 })).toEqual({ type: 'object' })
  })
})

