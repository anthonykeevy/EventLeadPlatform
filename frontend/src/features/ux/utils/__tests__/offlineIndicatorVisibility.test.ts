import { describe, it, expect } from 'vitest'
import { isPublicFormCaptureRoute, shouldShowOfflineIndicator } from '../offlineIndicatorVisibility'

describe('shouldShowOfflineIndicator', () => {
  it('hides on marketing and legal pages', () => {
    expect(shouldShowOfflineIndicator('/', false)).toBe(false)
    expect(shouldShowOfflineIndicator('/privacy', false)).toBe(false)
    expect(shouldShowOfflineIndicator('/terms', false)).toBe(false)
  })

  it('hides on pre-auth routes such as signup', () => {
    expect(shouldShowOfflineIndicator('/signup', false)).toBe(false)
    expect(shouldShowOfflineIndicator('/login', false)).toBe(false)
  })

  it('shows when authenticated', () => {
    expect(shouldShowOfflineIndicator('/dashboard', true)).toBe(true)
    expect(shouldShowOfflineIndicator('/', true)).toBe(false)
  })

  it('shows on public form capture without login', () => {
    expect(shouldShowOfflineIndicator('/forms/abc-token', false)).toBe(true)
    expect(shouldShowOfflineIndicator('/forms/abc-token/preview', false)).toBe(true)
  })
})

describe('isPublicFormCaptureRoute', () => {
  it('matches public form paths only', () => {
    expect(isPublicFormCaptureRoute('/forms/token123')).toBe(true)
    expect(isPublicFormCaptureRoute('/forms/token123/preview')).toBe(true)
    expect(isPublicFormCaptureRoute('/forms/1/builder')).toBe(false)
  })
})
