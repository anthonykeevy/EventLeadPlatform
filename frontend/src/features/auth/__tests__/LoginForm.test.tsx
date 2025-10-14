/**
 * Test suite for LoginForm component - Story 1.1
 * Tests AC-1.8: User cannot log in until email is verified
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { LoginForm } from '../LoginForm'
import { TEST_CONSTANTS } from '@/test/utils'

// Mock the auth service
vi.mock('@/lib/auth', () => ({
  login: vi.fn(),
}))

describe('LoginForm', () => {
  const user = userEvent.setup()
  
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('AC-1.8: User cannot log in until email is verified', () => {
    it('should block login for unverified user', async () => {
      const mockLogin = vi.fn().mockRejectedValue({
        response: {
          status: TEST_CONSTANTS.HTTP_STATUS.FORBIDDEN,
          data: { detail: 'Email not verified. Please check your email and verify your account.' }
        }
      })

      vi.mocked(require('@/lib/auth').login).mockImplementation(mockLogin)

      render(<LoginForm />)

      // Fill login form
      await user.type(screen.getByLabelText(/email/i), TEST_CONSTANTS.VALID_EMAIL)
      await user.type(screen.getByLabelText(/password/i), TEST_CONSTANTS.VALID_PASSWORD)

      // Submit form
      await user.click(screen.getByRole('button', { name: /log in/i }))

      // Verify error message
      await waitFor(() => {
        expect(screen.getByText(/email not verified/i)).toBeInTheDocument()
        expect(screen.getByText(/check your email/i)).toBeInTheDocument()
      })
    })

    it('should show resend verification option for unverified user', async () => {
      const mockLogin = vi.fn().mockRejectedValue({
        response: {
          status: TEST_CONSTANTS.HTTP_STATUS.FORBIDDEN,
          data: { detail: 'Email not verified' }
        }
      })

      vi.mocked(require('@/lib/auth').login).mockImplementation(mockLogin)

      render(<LoginForm />)

      // Fill and submit form
      await user.type(screen.getByLabelText(/email/i), TEST_CONSTANTS.VALID_EMAIL)
      await user.type(screen.getByLabelText(/password/i), TEST_CONSTANTS.VALID_PASSWORD)
      await user.click(screen.getByRole('button', { name: /log in/i }))

      // Verify resend verification button
      await waitFor(() => {
        expect(screen.getByRole('button', { name: /resend verification/i })).toBeInTheDocument()
      })
    })

    it('should allow successful login for verified user', async () => {
      const mockLogin = vi.fn().mockResolvedValue({
        access_token: 'valid-access-token',
        refresh_token: 'valid-refresh-token',
        token_type: 'bearer',
        user: {
          user_id: '123',
          email: TEST_CONSTANTS.VALID_EMAIL,
          email_verified: true
        }
      })

      vi.mocked(require('@/lib/auth').login).mockImplementation(mockLogin)

      const mockNavigate = vi.fn()
      vi.mock('react-router-dom', async () => {
        const actual = await vi.importActual('react-router-dom')
        return {
          ...actual,
          useNavigate: () => mockNavigate,
        }
      })

      render(<LoginForm />)

      // Fill and submit form
      await user.type(screen.getByLabelText(/email/i), TEST_CONSTANTS.VALID_EMAIL)
      await user.type(screen.getByLabelText(/password/i), TEST_CONSTANTS.VALID_PASSWORD)
      await user.click(screen.getByRole('button', { name: /log in/i }))

      // Verify successful login
      await waitFor(() => {
        expect(mockNavigate).toHaveBeenCalledWith('/dashboard')
      })
    })
  })

  describe('Form validation', () => {
    it('should show error for invalid email format', async () => {
      render(<LoginForm />)

      await user.type(screen.getByLabelText(/email/i), TEST_CONSTANTS.INVALID_EMAIL)
      await user.type(screen.getByLabelText(/password/i), TEST_CONSTANTS.VALID_PASSWORD)
      await user.click(screen.getByRole('button', { name: /log in/i }))

      await waitFor(() => {
        expect(screen.getByText(/invalid email format/i)).toBeInTheDocument()
      })
    })

    it('should show error for missing credentials', async () => {
      render(<LoginForm />)

      await user.click(screen.getByRole('button', { name: /log in/i }))

      await waitFor(() => {
        expect(screen.getByText(/email is required/i)).toBeInTheDocument()
        expect(screen.getByText(/password is required/i)).toBeInTheDocument()
      })
    })

    it('should show error for invalid credentials', async () => {
      const mockLogin = vi.fn().mockRejectedValue({
        response: {
          status: TEST_CONSTANTS.HTTP_STATUS.UNAUTHORIZED,
          data: { detail: 'Invalid credentials' }
        }
      })

      vi.mocked(require('@/lib/auth').login).mockImplementation(mockLogin)

      render(<LoginForm />)

      // Fill and submit form
      await user.type(screen.getByLabelText(/email/i), TEST_CONSTANTS.VALID_EMAIL)
      await user.type(screen.getByLabelText(/password/i), 'wrong-password')
      await user.click(screen.getByRole('button', { name: /log in/i }))

      // Verify error message
      await waitFor(() => {
        expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument()
      })
    })
  })

  describe('Rate limiting', () => {
    it('should show rate limit error after multiple failed attempts', async () => {
      const mockLogin = vi.fn().mockRejectedValue({
        response: {
          status: TEST_CONSTANTS.HTTP_STATUS.TOO_MANY_REQUESTS,
          data: { detail: 'Too many login attempts. Please try again later.' }
        }
      })

      vi.mocked(require('@/lib/auth').login).mockImplementation(mockLogin)

      render(<LoginForm />)

      // Fill and submit form multiple times
      for (let i = 0; i < 5; i++) {
        await user.type(screen.getByLabelText(/email/i), TEST_CONSTANTS.VALID_EMAIL)
        await user.type(screen.getByLabelText(/password/i), 'wrong-password')
        await user.click(screen.getByRole('button', { name: /log in/i }))
        
        if (i < 4) {
          await waitFor(() => {
            expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument()
          })
        }
      }

      // Verify rate limit message
      await waitFor(() => {
        expect(screen.getByText(/too many login attempts/i)).toBeInTheDocument()
      })
    })

    it('should disable form during rate limit', async () => {
      const mockLogin = vi.fn().mockRejectedValue({
        response: {
          status: TEST_CONSTANTS.HTTP_STATUS.TOO_MANY_REQUESTS,
          data: { detail: 'Too many login attempts' }
        }
      })

      vi.mocked(require('@/lib/auth').login).mockImplementation(mockLogin)

      render(<LoginForm />)

      // Trigger rate limit
      await user.type(screen.getByLabelText(/email/i), TEST_CONSTANTS.VALID_EMAIL)
      await user.type(screen.getByLabelText(/password/i), 'wrong-password')
      await user.click(screen.getByRole('button', { name: /log in/i }))

      // Verify form is disabled
      await waitFor(() => {
        expect(screen.getByRole('button', { name: /log in/i })).toBeDisabled()
        expect(screen.getByLabelText(/email/i)).toBeDisabled()
        expect(screen.getByLabelText(/password/i)).toBeDisabled()
      })
    })
  })

  describe('Password visibility toggle', () => {
    it('should toggle password visibility', async () => {
      render(<LoginForm />)

      const passwordField = screen.getByLabelText(/password/i)
      const toggleButton = screen.getByRole('button', { name: /toggle password visibility/i })

      // Initially password should be hidden
      expect(passwordField).toHaveAttribute('type', 'password')

      // Click toggle button
      await user.click(toggleButton)

      // Password should be visible
      expect(passwordField).toHaveAttribute('type', 'text')

      // Click toggle button again
      await user.click(toggleButton)

      // Password should be hidden again
      expect(passwordField).toHaveAttribute('type', 'password')
    })
  })

  describe('Remember me functionality', () => {
    it('should remember user email when checked', async () => {
      render(<LoginForm />)

      const emailField = screen.getByLabelText(/email/i)
      const rememberMeCheckbox = screen.getByLabelText(/remember me/i)

      // Fill email and check remember me
      await user.type(emailField, TEST_CONSTANTS.VALID_EMAIL)
      await user.click(rememberMeCheckbox)

      // Verify checkbox is checked
      expect(rememberMeCheckbox).toBeChecked()
    })
  })

  describe('Loading states', () => {
    it('should show loading state during login', async () => {
      const mockLogin = vi.fn().mockImplementation(() => 
        new Promise(resolve => setTimeout(resolve, 1000))
      )

      vi.mocked(require('@/lib/auth').login).mockImplementation(mockLogin)

      render(<LoginForm />)

      // Fill and submit form
      await user.type(screen.getByLabelText(/email/i), TEST_CONSTANTS.VALID_EMAIL)
      await user.type(screen.getByLabelText(/password/i), TEST_CONSTANTS.VALID_PASSWORD)
      await user.click(screen.getByRole('button', { name: /log in/i }))

      // Verify loading state
      expect(screen.getByRole('button', { name: /log in/i })).toBeDisabled()
      expect(screen.getByText(/logging in/i)).toBeInTheDocument()
    })
  })

  describe('Navigation links', () => {
    it('should have link to signup page', () => {
      render(<LoginForm />)

      const signupLink = screen.getByRole('link', { name: /sign up/i })
      expect(signupLink).toHaveAttribute('href', '/signup')
    })

    it('should have link to forgot password page', () => {
      render(<LoginForm />)

      const forgotPasswordLink = screen.getByRole('link', { name: /forgot password/i })
      expect(forgotPasswordLink).toHaveAttribute('href', '/forgot-password')
    })
  })

  describe('Error handling', () => {
    it('should handle network errors', async () => {
      const mockLogin = vi.fn().mockRejectedValue(new Error('Network error'))

      vi.mocked(require('@/lib/auth').login).mockImplementation(mockLogin)

      render(<LoginForm />)

      // Fill and submit form
      await user.type(screen.getByLabelText(/email/i), TEST_CONSTANTS.VALID_EMAIL)
      await user.type(screen.getByLabelText(/password/i), TEST_CONSTANTS.VALID_PASSWORD)
      await user.click(screen.getByRole('button', { name: /log in/i }))

      // Verify error message
      await waitFor(() => {
        expect(screen.getByText(/network error/i)).toBeInTheDocument()
      })
    })

    it('should clear errors when user starts typing', async () => {
      const mockLogin = vi.fn().mockRejectedValue({
        response: {
          status: TEST_CONSTANTS.HTTP_STATUS.UNAUTHORIZED,
          data: { detail: 'Invalid credentials' }
        }
      })

      vi.mocked(require('@/lib/auth').login).mockImplementation(mockLogin)

      render(<LoginForm />)

      // Submit form to trigger error
      await user.click(screen.getByRole('button', { name: /log in/i }))

      await waitFor(() => {
        expect(screen.getByText(/email is required/i)).toBeInTheDocument()
      })

      // Start typing in email field
      await user.type(screen.getByLabelText(/email/i), 't')

      // Error should be cleared
      expect(screen.queryByText(/email is required/i)).not.toBeInTheDocument()
    })
  })
})
