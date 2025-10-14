/**
 * Test suite for SignupForm component - Story 1.1
 * Tests AC-1.1, AC-1.2, AC-1.3, AC-1.4
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { SignupForm } from '../SignupForm'
import { mockFetchSuccess, mockFetchError, TEST_CONSTANTS } from '@/test/utils'

// Mock the auth service
vi.mock('@/lib/auth', () => ({
  signup: vi.fn(),
}))

describe('SignupForm', () => {
  const user = userEvent.setup()
  
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('AC-1.1: User can submit signup form with valid email and password', () => {
    it('should submit form with valid data', async () => {
      const mockSignup = vi.fn().mockResolvedValue({
        user_id: '123',
        email: TEST_CONSTANTS.VALID_EMAIL,
        email_verified: false,
        message: 'User created successfully'
      })

      vi.mocked(require('@/lib/auth').signup).mockImplementation(mockSignup)

      render(<SignupForm />)

      // Fill form fields
      await user.type(screen.getByLabelText(/email/i), TEST_CONSTANTS.VALID_EMAIL)
      await user.type(screen.getByLabelText(/password/i), TEST_CONSTANTS.VALID_PASSWORD)
      await user.type(screen.getByLabelText(/first name/i), 'Test')
      await user.type(screen.getByLabelText(/last name/i), 'User')

      // Submit form
      await user.click(screen.getByRole('button', { name: /sign up/i }))

      // Verify API call
      await waitFor(() => {
        expect(mockSignup).toHaveBeenCalledWith({
          email: TEST_CONSTANTS.VALID_EMAIL,
          password: TEST_CONSTANTS.VALID_PASSWORD,
          first_name: 'Test',
          last_name: 'User'
        })
      })
    })

    it('should show success message after successful signup', async () => {
      const mockSignup = vi.fn().mockResolvedValue({
        user_id: '123',
        email: TEST_CONSTANTS.VALID_EMAIL,
        email_verified: false,
        message: 'User created successfully'
      })

      vi.mocked(require('@/lib/auth').signup).mockImplementation(mockSignup)

      render(<SignupForm />)

      // Fill and submit form
      await user.type(screen.getByLabelText(/email/i), TEST_CONSTANTS.VALID_EMAIL)
      await user.type(screen.getByLabelText(/password/i), TEST_CONSTANTS.VALID_PASSWORD)
      await user.type(screen.getByLabelText(/first name/i), 'Test')
      await user.type(screen.getByLabelText(/last name/i), 'User')
      await user.click(screen.getByRole('button', { name: /sign up/i }))

      // Verify success message
      await waitFor(() => {
        expect(screen.getByText(/user created successfully/i)).toBeInTheDocument()
      })
    })
  })

  describe('AC-1.2: System validates email format and password minimum length', () => {
    it('should show error for invalid email format', async () => {
      render(<SignupForm />)

      await user.type(screen.getByLabelText(/email/i), TEST_CONSTANTS.INVALID_EMAIL)
      await user.type(screen.getByLabelText(/password/i), TEST_CONSTANTS.VALID_PASSWORD)
      await user.type(screen.getByLabelText(/first name/i), 'Test')
      await user.type(screen.getByLabelText(/last name/i), 'User')
      await user.click(screen.getByRole('button', { name: /sign up/i }))

      await waitFor(() => {
        expect(screen.getByText(/invalid email format/i)).toBeInTheDocument()
      })
    })

    it('should show error for password too short', async () => {
      render(<SignupForm />)

      await user.type(screen.getByLabelText(/email/i), TEST_CONSTANTS.VALID_EMAIL)
      await user.type(screen.getByLabelText(/password/i), TEST_CONSTANTS.WEAK_PASSWORD)
      await user.type(screen.getByLabelText(/first name/i), 'Test')
      await user.type(screen.getByLabelText(/last name/i), 'User')
      await user.click(screen.getByRole('button', { name: /sign up/i }))

      await waitFor(() => {
        expect(screen.getByText(/password must be at least 8 characters/i)).toBeInTheDocument()
      })
    })

    it('should show error for missing required fields', async () => {
      render(<SignupForm />)

      await user.click(screen.getByRole('button', { name: /sign up/i }))

      await waitFor(() => {
        expect(screen.getByText(/email is required/i)).toBeInTheDocument()
        expect(screen.getByText(/password is required/i)).toBeInTheDocument()
        expect(screen.getByText(/first name is required/i)).toBeInTheDocument()
        expect(screen.getByText(/last name is required/i)).toBeInTheDocument()
      })
    })
  })

  describe('AC-1.3: System prevents duplicate email registration', () => {
    it('should show error for duplicate email', async () => {
      const mockSignup = vi.fn().mockRejectedValue({
        response: {
          status: TEST_CONSTANTS.HTTP_STATUS.CONFLICT,
          data: { detail: 'Email already exists' }
        }
      })

      vi.mocked(require('@/lib/auth').signup).mockImplementation(mockSignup)

      render(<SignupForm />)

      // Fill and submit form
      await user.type(screen.getByLabelText(/email/i), TEST_CONSTANTS.VALID_EMAIL)
      await user.type(screen.getByLabelText(/password/i), TEST_CONSTANTS.VALID_PASSWORD)
      await user.type(screen.getByLabelText(/first name/i), 'Test')
      await user.type(screen.getByLabelText(/last name/i), 'User')
      await user.click(screen.getByRole('button', { name: /sign up/i }))

      // Verify error message
      await waitFor(() => {
        expect(screen.getByText(/email already exists/i)).toBeInTheDocument()
      })
    })
  })

  describe('AC-1.4: System sends verification email', () => {
    it('should show verification email sent message', async () => {
      const mockSignup = vi.fn().mockResolvedValue({
        user_id: '123',
        email: TEST_CONSTANTS.VALID_EMAIL,
        email_verified: false,
        message: 'User created successfully',
        verification_sent: true
      })

      vi.mocked(require('@/lib/auth').signup).mockImplementation(mockSignup)

      render(<SignupForm />)

      // Fill and submit form
      await user.type(screen.getByLabelText(/email/i), TEST_CONSTANTS.VALID_EMAIL)
      await user.type(screen.getByLabelText(/password/i), TEST_CONSTANTS.VALID_PASSWORD)
      await user.type(screen.getByLabelText(/first name/i), 'Test')
      await user.type(screen.getByLabelText(/last name/i), 'User')
      await user.click(screen.getByRole('button', { name: /sign up/i }))

      // Verify verification email message
      await waitFor(() => {
        expect(screen.getByText(/verification email sent/i)).toBeInTheDocument()
      })
    })

    it('should redirect to verification page after signup', async () => {
      const mockSignup = vi.fn().mockResolvedValue({
        user_id: '123',
        email: TEST_CONSTANTS.VALID_EMAIL,
        email_verified: false,
        message: 'User created successfully',
        verification_sent: true
      })

      vi.mocked(require('@/lib/auth').signup).mockImplementation(mockSignup)

      const mockNavigate = vi.fn()
      vi.mock('react-router-dom', async () => {
        const actual = await vi.importActual('react-router-dom')
        return {
          ...actual,
          useNavigate: () => mockNavigate,
        }
      })

      render(<SignupForm />)

      // Fill and submit form
      await user.type(screen.getByLabelText(/email/i), TEST_CONSTANTS.VALID_EMAIL)
      await user.type(screen.getByLabelText(/password/i), TEST_CONSTANTS.VALID_PASSWORD)
      await user.type(screen.getByLabelText(/first name/i), 'Test')
      await user.type(screen.getByLabelText(/last name/i), 'User')
      await user.click(screen.getByRole('button', { name: /sign up/i }))

      // Verify navigation
      await waitFor(() => {
        expect(mockNavigate).toHaveBeenCalledWith('/verify-email')
      })
    })
  })

  describe('Form validation and UX', () => {
    it('should disable submit button while loading', async () => {
      const mockSignup = vi.fn().mockImplementation(() => 
        new Promise(resolve => setTimeout(resolve, 1000))
      )

      vi.mocked(require('@/lib/auth').signup).mockImplementation(mockSignup)

      render(<SignupForm />)

      // Fill form
      await user.type(screen.getByLabelText(/email/i), TEST_CONSTANTS.VALID_EMAIL)
      await user.type(screen.getByLabelText(/password/i), TEST_CONSTANTS.VALID_PASSWORD)
      await user.type(screen.getByLabelText(/first name/i), 'Test')
      await user.type(screen.getByLabelText(/last name/i), 'User')

      // Submit form
      const submitButton = screen.getByRole('button', { name: /sign up/i })
      await user.click(submitButton)

      // Verify button is disabled
      expect(submitButton).toBeDisabled()
      expect(screen.getByText(/creating account/i)).toBeInTheDocument()
    })

    it('should show password strength indicator', async () => {
      render(<SignupForm />)

      const passwordField = screen.getByLabelText(/password/i)
      
      // Test weak password
      await user.type(passwordField, '123')
      expect(screen.getByText(/weak/i)).toBeInTheDocument()

      // Test strong password
      await user.clear(passwordField)
      await user.type(passwordField, TEST_CONSTANTS.VALID_PASSWORD)
      expect(screen.getByText(/strong/i)).toBeInTheDocument()
    })

    it('should handle network errors gracefully', async () => {
      const mockSignup = vi.fn().mockRejectedValue(new Error('Network error'))

      vi.mocked(require('@/lib/auth').signup).mockImplementation(mockSignup)

      render(<SignupForm />)

      // Fill and submit form
      await user.type(screen.getByLabelText(/email/i), TEST_CONSTANTS.VALID_EMAIL)
      await user.type(screen.getByLabelText(/password/i), TEST_CONSTANTS.VALID_PASSWORD)
      await user.type(screen.getByLabelText(/first name/i), 'Test')
      await user.type(screen.getByLabelText(/last name/i), 'User')
      await user.click(screen.getByRole('button', { name: /sign up/i }))

      // Verify error message
      await waitFor(() => {
        expect(screen.getByText(/network error/i)).toBeInTheDocument()
      })
    })
  })
})
