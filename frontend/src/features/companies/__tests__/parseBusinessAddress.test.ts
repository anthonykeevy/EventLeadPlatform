/**
 * parseBusinessAddress Utility Tests
 * Story 1.19: AC-1.19.5 - Parse ABR addresses
 */

import { describe, it, expect } from 'vitest'
import { parseBusinessAddress } from '../api/companiesApi'

describe('parseBusinessAddress', () => {
  it('parses simplified format (STATE POSTCODE only)', () => {
    const result = parseBusinessAddress('NSW 2000')
    
    expect(result.street).toBe('')
    expect(result.suburb).toBe('')
    expect(result.state).toBe('NSW')
    expect(result.postcode).toBe('2000')
  })

  it('parses full Australian address', () => {
    const result = parseBusinessAddress('341 George Street, Sydney NSW 2000')
    
    expect(result.street).toBe('341 George Street')
    expect(result.suburb).toBe('Sydney')
    expect(result.state).toBe('NSW')
    expect(result.postcode).toBe('2000')
  })

  it('parses address with level/suite', () => {
    const result = parseBusinessAddress('Level 5, 123 Main St, Melbourne VIC 3000')
    
    expect(result.street).toBe('Level 5, 123 Main St')
    expect(result.suburb).toBe('Melbourne')
    expect(result.state).toBe('VIC')
    expect(result.postcode).toBe('3000')
  })

  it('parses address with multi-word suburb', () => {
    const result = parseBusinessAddress('45 Smith Road, North Sydney NSW 2060')
    
    expect(result.street).toBe('45 Smith Road')
    expect(result.suburb).toBe('North Sydney')
    expect(result.state).toBe('NSW')
    expect(result.postcode).toBe('2060')
  })

  it('handles null address', () => {
    const result = parseBusinessAddress(null)
    
    expect(result.street).toBe('')
    expect(result.suburb).toBe('')
    expect(result.state).toBe('')
    expect(result.postcode).toBe('')
  })

  it('handles empty string', () => {
    const result = parseBusinessAddress('')
    
    expect(result.street).toBe('')
    expect(result.suburb).toBe('')
    expect(result.state).toBe('')
    expect(result.postcode).toBe('')
  })

  it('handles incomplete address (street only)', () => {
    const result = parseBusinessAddress('123 Main Street')
    
    expect(result.street).toBe('123 Main Street')
    // Other fields should be empty but not crash
    expect(result.suburb).toBeDefined()
    expect(result.state).toBeDefined()
    expect(result.postcode).toBeDefined()
  })

  it('handles address with 3-letter state code', () => {
    const result = parseBusinessAddress('10 Queen St, Brisbane QLD 4000')
    
    expect(result.street).toBe('10 Queen St')
    expect(result.suburb).toBe('Brisbane')
    expect(result.state).toBe('QLD')
    expect(result.postcode).toBe('4000')
  })

  it('preserves full address in street when parsing fails', () => {
    const weirdAddress = 'Some unparseable format'
    const result = parseBusinessAddress(weirdAddress)
    
    expect(result.street).toContain('Some unparseable format')
  })
})

