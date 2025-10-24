/**
 * Onboarding Modal Tests - Story 1.14
 * AC-1.14.1, AC-1.14.2: Modal behavior and dismissal prevention
 */

import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { OnboardingModal } from '../components/OnboardingModal'
import * as authHooks from '../../auth'

// Mock auth hooks
vi.mock('../../auth')

const mockUser = {
  user_id: 1,
  email: 'test@example.com',
  first_name: 'Test',
  last_name: 'User',
  onboarding_complete: false
}

describe('OnboardingModal', () => {
  beforeEach(() => {
    vi.mocked(authHooks.useAuth).mockReturnValue({
      user: mockUser,
      isAuthenticated: true,
      isLoading: false,
      error: null,
      login: vi.fn(),
      signup: vi.fn(),
      logout: vi.fn(),
      refreshToken: vi.fn()
    })
  })

  it('should render when isOpen is true - AC-1.14.1', () => {
    render(
      <BrowserRouter>
        <OnboardingModal isOpen={true} onComplete={vi.fn()} />
      </BrowserRouter>
    )

    expect(screen.getByText(/Welcome to EventLead!/i)).toBeInTheDocument()
  })

  it('should not render when isOpen is false', () => {
    render(
      <BrowserRouter>
        <OnboardingModal isOpen={false} onComplete={vi.fn()} />
      </BrowserRouter>
    )

    expect(screen.queryByText(/Welcome to EventLead!/i)).not.toBeInTheDocument()
  })

  it('should show progress indicator - AC-1.14.6', () => {
    render(
      <BrowserRouter>
        <OnboardingModal isOpen={true} onComplete={vi.fn()} />
      </BrowserRouter>
    )

    expect(screen.getByText('User Details')).toBeInTheDocument()
    expect(screen.getByText('Company Setup')).toBeInTheDocument()
  })

  it('should start on Step 1 by default', () => {
    render(
      <BrowserRouter>
        <OnboardingModal isOpen={true} onComplete={vi.fn()} />
      </BrowserRouter>
    )

    expect(screen.getByText(/Tell us about yourself/i)).toBeInTheDocument()
  })
})



