/**
 * Password Reset Request Component Tests - Story 1.15 (AC-1.15.1, AC-1.15.4)
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { BrowserRouter } from 'react-router-dom'
import { PasswordResetRequest } from '../pages/PasswordResetRequest'
import * as passwordResetApi from '../api/passwordResetApi'

// Mock the password reset API
vi.mock('../api/passwordResetApi')

const renderComponent = () => {
  return render(
    <BrowserRouter>
      <PasswordResetRequest />
    </BrowserRouter>
  )
}

describe('PasswordResetRequest Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('Initial Render - AC-1.15.1', () => {
    it('should render password reset request form', () => {
      renderComponent()

      expect(screen.getByRole('heading', { name: /reset password/i })).toBeInTheDocument()
      expect(screen.getByLabelText(/email address/i)).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /send reset link/i })).toBeInTheDocument()
    })

    it('should have a link back to login page', () => {
      renderComponent()

      const backLink = screen.getByRole('link', { name: /back to login/i })
      expect(backLink).toBeInTheDocument()
      expect(backLink).toHaveAttribute('href', '/login')
    })

    it('should disable submit button when email is empty', () => {
      renderComponent()

      const submitButton = screen.getByRole('button', { name: /send reset link/i })
      expect(submitButton).toBeDisabled()
    })
  })

  describe('Email Validation - AC-1.15.1', () => {
    it('should validate email format', async () => {
      const user = userEvent.setup()
      renderComponent()

      const emailInput = screen.getByLabelText(/email address/i)
      await user.type(emailInput, 'invalid-email')
      await user.tab() // Trigger blur

      await waitFor(() => {
        expect(screen.getByText(/please enter a valid email address/i)).toBeInTheDocument()
      })
    })

    it('should enable submit button when valid email is entered', async () => {
      const user = userEvent.setup()
      renderComponent()

      const emailInput = screen.getByLabelText(/email address/i)
      await user.type(emailInput, 'user@example.com')

      await waitFor(() => {
        const submitButton = screen.getByRole('button', { name: /send reset link/i })
        expect(submitButton).not.toBeDisabled()
      })
    })

    // Email is required field is already tested via "should disable submit button when email is empty"
  })

  describe('Form Submission - AC-1.15.1', () => {
    it('should call requestPasswordReset API on form submission', async () => {
      const user = userEvent.setup()
      const mockRequestPasswordReset = vi.mocked(passwordResetApi.requestPasswordReset)
      mockRequestPasswordReset.mockResolvedValue({
        success: true,
        message: 'If the email exists, a password reset link has been sent.',
      })

      renderComponent()

      const emailInput = screen.getByLabelText(/email address/i)
      await user.type(emailInput, 'user@example.com')

      const submitButton = screen.getByRole('button', { name: /send reset link/i })
      await user.click(submitButton)

      await waitFor(() => {
        expect(mockRequestPasswordReset).toHaveBeenCalledWith('user@example.com')
      })
    })

    it('should show loading state during submission', async () => {
      const user = userEvent.setup()
      const mockRequestPasswordReset = vi.mocked(passwordResetApi.requestPasswordReset)
      mockRequestPasswordReset.mockImplementation(
        () => new Promise((resolve) => setTimeout(resolve, 1000))
      )

      renderComponent()

      const emailInput = screen.getByLabelText(/email address/i)
      await user.type(emailInput, 'user@example.com')

      const submitButton = screen.getByRole('button', { name: /send reset link/i })
      await user.click(submitButton)

      expect(screen.getByText(/sending reset link/i)).toBeInTheDocument()
      expect(submitButton).toBeDisabled()
    })
  })

  describe('Success State - AC-1.15.1', () => {
    it('should display success message after successful submission', async () => {
      const user = userEvent.setup()
      const mockRequestPasswordReset = vi.mocked(passwordResetApi.requestPasswordReset)
      mockRequestPasswordReset.mockResolvedValue({
        success: true,
        message: 'If the email exists, a password reset link has been sent.',
      })

      renderComponent()

      const emailInput = screen.getByLabelText(/email address/i)
      await user.type(emailInput, 'user@example.com')

      const submitButton = screen.getByRole('button', { name: /send reset link/i })
      await user.click(submitButton)

      await waitFor(() => {
        expect(screen.getByText(/password reset email sent/i)).toBeInTheDocument()
        expect(screen.getByText(/user@example.com/i)).toBeInTheDocument()
      })
    })

    it('should show "Return to Login" button after success', async () => {
      const user = userEvent.setup()
      const mockRequestPasswordReset = vi.mocked(passwordResetApi.requestPasswordReset)
      mockRequestPasswordReset.mockResolvedValue({
        success: true,
        message: 'If the email exists, a password reset link has been sent.',
      })

      renderComponent()

      const emailInput = screen.getByLabelText(/email address/i)
      await user.type(emailInput, 'user@example.com')
      await user.click(screen.getByRole('button', { name: /send reset link/i }))

      await waitFor(() => {
        const returnLink = screen.getByRole('link', { name: /return to login/i })
        expect(returnLink).toBeInTheDocument()
        expect(returnLink).toHaveAttribute('href', '/login')
      })
    })

    it('should allow trying again via help text link after success', async () => {
      const user = userEvent.setup()
      const mockRequestPasswordReset = vi.mocked(passwordResetApi.requestPasswordReset)
      mockRequestPasswordReset.mockResolvedValue({
        success: true,
        message: 'If the email exists, a password reset link has been sent.',
      })

      renderComponent()

      const emailInput = screen.getByLabelText(/email address/i)
      await user.type(emailInput, 'user@example.com')
      await user.click(screen.getByRole('button', { name: /send reset link/i }))

      await waitFor(() => {
        expect(screen.getByText(/password reset email sent/i)).toBeInTheDocument()
      })

      const tryAgainButton = screen.getByRole('button', { name: /try again/i })
      await user.click(tryAgainButton)

      await waitFor(() => {
        expect(screen.getByRole('heading', { name: /reset password/i })).toBeInTheDocument()
        expect(screen.getByLabelText(/email address/i)).toBeInTheDocument()
      })
    })
  })

  describe('Error Handling - AC-1.15.4', () => {
    it('should display error message on API failure', async () => {
      const user = userEvent.setup()
      const mockRequestPasswordReset = vi.mocked(passwordResetApi.requestPasswordReset)
      mockRequestPasswordReset.mockRejectedValue(
        new Error('Connection error. Please check your internet and try again.')
      )

      renderComponent()

      const emailInput = screen.getByLabelText(/email address/i)
      await user.type(emailInput, 'user@example.com')
      await user.click(screen.getByRole('button', { name: /send reset link/i }))

      await waitFor(() => {
        expect(screen.getByText(/connection error/i)).toBeInTheDocument()
      })
    })

    it('should allow retry after error', async () => {
      const user = userEvent.setup()
      const mockRequestPasswordReset = vi.mocked(passwordResetApi.requestPasswordReset)
      mockRequestPasswordReset.mockRejectedValueOnce(new Error('Network error'))
      mockRequestPasswordReset.mockResolvedValueOnce({
        success: true,
        message: 'If the email exists, a password reset link has been sent.',
      })

      renderComponent()

      const emailInput = screen.getByLabelText(/email address/i)
      await user.type(emailInput, 'user@example.com')
      await user.click(screen.getByRole('button', { name: /send reset link/i }))

      await waitFor(() => {
        expect(screen.getByText(/network error/i)).toBeInTheDocument()
      })

      // Retry
      await user.click(screen.getByRole('button', { name: /send reset link/i }))

      await waitFor(() => {
        expect(screen.getByText(/password reset email sent/i)).toBeInTheDocument()
      })
    })
  })

  describe('Accessibility - AC-1.15.5', () => {
    it('should have accessible form labels', () => {
      renderComponent()

      expect(screen.getByLabelText(/email address/i)).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /send reset link/i })).toBeInTheDocument()
    })

    it('should have ARIA attributes for validation errors', async () => {
      const user = userEvent.setup()
      renderComponent()

      const emailInput = screen.getByLabelText(/email address/i)
      await user.type(emailInput, 'invalid')
      await user.tab()

      await waitFor(() => {
        expect(emailInput).toHaveAttribute('aria-invalid', 'true')
        expect(emailInput).toHaveAttribute('aria-describedby', 'email-error')
      })
    })

    // Autofocus attribute is present in component code - tested manually
  })
})

