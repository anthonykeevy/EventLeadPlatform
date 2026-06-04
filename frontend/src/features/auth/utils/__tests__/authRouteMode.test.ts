import { describe, expect, it } from 'vitest'
import { isActiveAuthRoute, isPublicAuthPassiveRoute } from '../authRouteMode'

describe('authRouteMode', () => {
  it('treats token preview shell as passive', () => {
    expect(isPublicAuthPassiveRoute('/forms/abc123/preview')).toBe(true)
    expect(isActiveAuthRoute('/forms/abc123/preview')).toBe(false)
  })

  it('treats public form renderer as passive', () => {
    expect(isPublicAuthPassiveRoute('/forms/abc123')).toBe(true)
  })

  it('treats builder and review as active', () => {
    expect(isPublicAuthPassiveRoute('/forms/42/builder')).toBe(false)
    expect(isPublicAuthPassiveRoute('/forms/42/review')).toBe(false)
    expect(isActiveAuthRoute('/forms/42/builder')).toBe(true)
  })

  it('treats dashboard as active', () => {
    expect(isPublicAuthPassiveRoute('/dashboard')).toBe(false)
    expect(isActiveAuthRoute('/dashboard')).toBe(true)
  })
})
