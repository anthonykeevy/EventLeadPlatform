/**
 * Test suite for EmailVerification component - Story 1.1
 * Tests AC-1.5, AC-1.6, AC-1.7
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { EmailVerification } from '../EmailVerification'
import { TEST_CONSTANTS } from '@/test/utils'

// Mock the auth service
vi.mock('@/lib/auth', () => ({
  verifyEmail: vi.fn(),
}))

describe('EmailVerification', () => {
  const user = userEvent.setup()
  
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('AC-1.5: Verification email contains secure token link that expires in 24 hours', () => {
    it('should display verification instructions', () => {
      render(<EmailVerification />)

      expect(screen.getByText(/check your email/i)).toBeInTheDocument()
      expect(screen.getByText(/verification link/i)).toBeInTheDocument()
      expect(screen.getByText(/24 hours/i)).toBeInTheDocument()
    })

    it('should show email address if provided', () => {
      const email = TEST_CONSTANTS.VALID_EMAIL
      render(<EmailVerification email={email} />)

      expect(screen.getByText(email)).toBeInTheDocument()
    })
  })

  describe('AC-1.6: User clicking verification link marks email_verified = true', () => {
    it('should verify email with valid token', async () => {
      const mockVerifyEmail = vi.fn().mockResolvedValue({
        message: 'Email verified successfully',
        email_verified: true
      })

      vi.mocked(require('@/lib/auth').verifyEmail).mockImplementation(mockVerifyEmail)

      // Mock URL search params
      const mockSearchParams = new URLSearchParams('?token=valid-token-123')
      vi.mock('react-router-dom', async () => {
        const actual = await vi.importActual('react-router-dom')
        return {
          ...actual,
          useSearchParams: () => [mockSearchParams],
        }
      })

      render(<EmailVerification />)

      // Wait for automatic verification
      await waitFor(() => {
        expect(mockVerifyEmail).toHaveBeenCalledWith('valid-token-123')
      })

      // Verify success message
      await waitFor(() => {
        expect(screen.getByText(/email verified successfully/i)).toBeInTheDocument()
      })
    })

    it('should handle invalid token', async () => {
      const mockVerifyEmail = vi.fn().mockRejectedValue({
        response: {
          status: TEST_CONSTANTS.HTTP_STATUS.BAD_REQUEST,
          data: { detail: 'Invalid verification token' }
        }
      })

      vi.mocked(require('@/lib/auth').verifyEmail).mockImplementation(mockVerifyEmail)

      // Mock URL search params with invalid token
      const mockSearchParams = new URLSearchParams('?token=invalid-token')
      vi.mock('react-router-dom', async () => {
        const actual = await vi.importActual('react-router-dom')
        return {
          ...actual,
          useSearchParams: () => [mockSearchParams],
        }
      })

      render(<EmailVerification />)

      // Verify error message
      await waitFor(() => {
        expect(screen.getByText(/invalid verification token/i)).toBeInTheDocument()
      })
    })

    it('should handle expired token', async () => {
      const mockVerifyEmail = vi.fn().mockRejectedValue({
        response: {
          status: TEST_CONSTANTS.HTTP_STATUS.BAD_REQUEST,
          data: { detail: 'Verification token has expired' }
        }
      })

      vi.mocked(require('@/lib/auth').verifyEmail).mockImplementation(mockVerifyEmail)

      // Mock URL search params with expired token
      const mockSearchParams = new URLSearchParams('?token=expired-token')
      vi.mock('react-router-dom', async () => {
        const actual = await vi.importActual('react-router-dom')
        return {
          ...actual,
          useSearchParams: () => [mockSearchParams],
        }
      })

      render(<EmailVerification />)

      // Verify error message
      await waitFor(() => {
        expect(screen.getByText(/verification token has expired/i)).toBeInTheDocument()
      })
    })
  })

  describe('AC-1.7: System displays success message and redirects to login page', () => {
    it('should show success message and redirect after verification', async () => {
      const mockVerifyEmail = vi.fn().mockResolvedValue({
        message: 'Email verified successfully',
        email_verified: true
      })

      vi.mocked(require('@/lib/auth').verifyEmail).mockImplementation(mockVerifyEmail)

      const mockNavigate = vi.fn()
      vi.mock('react-router-dom', async () => {
        const actual = await vi.importActual('react-router-dom')
        return {
          ...actual,
          useNavigate: () => mockNavigate,
          useSearchParams: () => [new URLSearchParams('?token=valid-token')],
        }
      })

      render(<EmailVerification />)

      // Wait for verification and redirect
      await waitFor(() => {
        expect(screen.getByText(/email verified successfully/i)).toBeInTheDocument()
      })

      // Verify redirect to login
      await waitFor(() => {
        expect(mockNavigate).toHaveBeenCalledWith('/login')
      })
    })

    it('should show redirect countdown', async () => {
      const mockVerifyEmail = vi.fn().mockResolvedValue({
        message: 'Email verified successfully',
        email_verified: true
      })

      vi.mocked(require('@/lib/auth').verifyEmail).mockImplementation(mockVerifyEmail)

      vi.mock('react-router-dom', async () => {
        const actual = await vi.importActual('react-router-dom')
        return {
          ...actual,
          useSearchParams: () => [new URLSearchParams('?token=valid-token')],
        }
      })

      render(<EmailVerification />)

      // Wait for success message
      await waitFor(() => {
        expect(screen.getByText(/redirecting/i)).toBeInTheDocument()
      })
    })
  })

  describe('Manual verification flow', () => {
    it('should allow manual token entry', async () => {
      const mockVerifyEmail = vi.fn().mockResolvedValue({
        message: 'Email verified successfully',
        email_verified: true
      })

      vi.mocked(require('@/lib/auth').verifyEmail).mockImplementation(mockVerifyEmail)

      render(<EmailVerification />)

      // Enter token manually
      const tokenInput = screen.getByLabelText(/verification token/i)
      await user.type(tokenInput, 'manual-token-123')

      // Click verify button
      await user.click(screen.getByRole('button', { name: /verify email/i }))

      // Verify API call
      await waitFor(() => {
        expect(mockVerifyEmail).toHaveBeenCalledWith('manual-token-123')
      })
    })

    it('should show error for empty token', async () => {
      render(<EmailVerification />)

      // Try to verify without token
      await user.click(screen.getByRole('button', { name: /verify email/i }))

      // Verify error message
      await waitFor(() => {
        expect(screen.getByText(/token is required/i)).toBeInTheDocument()
      })
    })
  })

  describe('Resend verification email', () => {
    it('should allow resending verification email', async () => {
      const mockResendVerification = vi.fn().mockResolvedValue({
        message: 'Verification email sent'
      })

      vi.mocked(require('@/lib/auth').resendVerification).mockImplementation(mockResendVerification)

      render(<EmailVerification email={TEST_CONSTANTS.VALID_EMAIL} />)

      // Click resend button
      await user.click(screen.getByRole('button', { name: /resend/i }))

      // Verify API call
      await waitFor(() => {
        expect(mockResendVerification).toHaveBeenCalledWith(TEST_CONSTANTS.VALID_EMAIL)
      })

      // Verify success message
      await waitFor(() => {
        expect(screen.getByText(/verification email sent/i)).toBeInTheDocument()
      })
    })

    it('should show cooldown period for resend', async () => {
      const mockResendVerification = vi.fn().mockResolvedValue({
        message: 'Verification email sent'
      })

      vi.mocked(require('@/lib/auth').resendVerification).mockImplementation(mockResendVerification)

      render(<EmailVerification email={TEST_CONSTANTS.VALID_EMAIL} />)

      // Click resend button
      await user.click(screen.getByRole('button', { name: /resend/i }))

      // Verify button is disabled during cooldown
      await waitFor(() => {
        expect(screen.getByRole('button', { name: /resend/i })).toBeDisabled()
      })
    })
  })

  describe('Error handling', () => {
    it('should handle network errors', async () => {
      const mockVerifyEmail = vi.fn().mockRejectedValue(new Error('Network error'))

      vi.mocked(require('@/lib/auth').verifyEmail).mockImplementation(mockVerifyEmail)

      vi.mock('react-router-dom', async () => {
        const actual = await vi.importActual('react-router-dom')
        return {
          ...actual,
          useSearchParams: () => [new URLSearchParams('?token=test-token')],
        }
      })

      render(<EmailVerification />)

      // Verify error message
      await waitFor(() => {
        expect(screen.getByText(/network error/i)).toBeInTheDocument()
      })
    })

    it('should show retry option for failed verification', async () => {
      const mockVerifyEmail = vi.fn().mockRejectedValue({
        response: {
          status: TEST_CONSTANTS.HTTP_STATUS.INTERNAL_SERVER_ERROR,
          data: { detail: 'Server error' }
        }
      })

      vi.mocked(require('@/lib/auth').verifyEmail).mockImplementation(mockVerifyEmail)

      vi.mock('react-router-dom', async () => {
        const actual = await vi.importActual('react-router-dom')
        return {
          ...actual,
          useSearchParams: () => [new URLSearchParams('?token=test-token')],
        }
      })

      render(<EmailVerification />)

      // Verify retry button
      await waitFor(() => {
        expect(screen.getByRole('button', { name: /try again/i })).toBeInTheDocument()
      })
    })
  })
})
