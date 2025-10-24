/**
 * SignupForm Component Tests - Story 1.9 (AC-1.9.1, AC-1.9.4)
 * Tests for signup form rendering, validation, and interaction
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { BrowserRouter } from 'react-router-dom'
import { SignupForm } from '../components/SignupForm'
import { AuthProvider } from '../context/AuthContext'
import * as authApi from '../api/authApi'

// Mock the API
vi.mock('../api/authApi')

function renderSignupForm() {
  return render(
    <BrowserRouter>
      <AuthProvider>
        <SignupForm />
      </AuthProvider>
    </BrowserRouter>
  )
}

describe('SignupForm Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })
  
  describe('Rendering', () => {
    it('should render signup form with all fields', () => {
      renderSignupForm()
      
      expect(screen.getByLabelText(/first name/i)).toBeInTheDocument()
      expect(screen.getByLabelText(/last name/i)).toBeInTheDocument()
      expect(screen.getByLabelText(/email address/i)).toBeInTheDocument()
      expect(screen.getByLabelText(/^password$/i)).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /sign up/i })).toBeInTheDocument()
    })
    
    it('should have submit button disabled initially', () => {
      renderSignupForm()
      
      const submitButton = screen.getByRole('button', { name: /sign up/i })
      expect(submitButton).toBeDisabled()
    })
    
    it('should render link to login page', () => {
      renderSignupForm()
      
      expect(screen.getByRole('link', { name: /log in/i })).toBeInTheDocument()
    })
  })
  
  describe('Validation', () => {
    it('should show error for invalid email format', async () => {
      const user = userEvent.setup()
      renderSignupForm()
      
      const emailInput = screen.getByLabelText(/email address/i)
      await user.type(emailInput, 'invalid-email')
      await user.tab() // Trigger blur
      
      await waitFor(() => {
        expect(screen.getByText(/please enter a valid email address/i)).toBeInTheDocument()
      })
    })
    
    it('should show error for short first name', async () => {
      const user = userEvent.setup()
      renderSignupForm()
      
      const firstNameInput = screen.getByLabelText(/first name/i)
      await user.type(firstNameInput, 'A')
      await user.tab()
      
      await waitFor(() => {
        expect(screen.getByText(/at least 2 characters/i)).toBeInTheDocument()
      })
    })
    
    it('should show error for weak password', async () => {
      const user = userEvent.setup()
      renderSignupForm()
      
      const passwordInput = screen.getByLabelText(/^password/i)
      await user.type(passwordInput, 'weak')
      
      // Password strength indicator should show weak
      await waitFor(() => {
        expect(screen.getByText(/weak/i)).toBeInTheDocument()
      })
    })
    
    it('should display password strength indicator', async () => {
      const user = userEvent.setup()
      renderSignupForm()
      
      const passwordInput = screen.getByLabelText(/^password/i)
      await user.type(passwordInput, 'Test1234!')
      
      await waitFor(() => {
        expect(screen.getByText(/strong/i)).toBeInTheDocument()
      })
    })
    
    it('should enable submit button when all fields are valid', async () => {
      const user = userEvent.setup()
      renderSignupForm()
      
      await user.type(screen.getByLabelText(/first name/i), 'John')
      await user.type(screen.getByLabelText(/last name/i), 'Doe')
      await user.type(screen.getByLabelText(/email address/i), 'john@example.com')
      await user.type(screen.getByLabelText(/^password/i), 'Test1234!')
      
      await waitFor(() => {
        const submitButton = screen.getByRole('button', { name: /sign up/i })
        expect(submitButton).not.toBeDisabled()
      })
    })
  })
  
  describe('Password Visibility Toggle', () => {
    it('should toggle password visibility', async () => {
      const user = userEvent.setup()
      renderSignupForm()
      
      const passwordInput = screen.getByLabelText(/^password/i) as HTMLInputElement
      expect(passwordInput.type).toBe('password')
      
      const toggleButton = screen.getByLabelText(/show password/i)
      await user.click(toggleButton)
      
      expect(passwordInput.type).toBe('text')
      expect(screen.getByLabelText(/hide password/i)).toBeInTheDocument()
    })
  })
  
  describe('Form Submission', () => {
    it('should call signup API on valid form submission', async () => {
      const user = userEvent.setup()
      const mockSignup = vi.mocked(authApi.signupUser)
      mockSignup.mockResolvedValueOnce({
        user_id: 1,
        email: 'john@example.com',
        message: 'Verification email sent',
      })
      
      renderSignupForm()
      
      await user.type(screen.getByLabelText(/first name/i), 'John')
      await user.type(screen.getByLabelText(/last name/i), 'Doe')
      await user.type(screen.getByLabelText(/email address/i), 'john@example.com')
      await user.type(screen.getByLabelText(/^password/i), 'Test1234!')
      
      const submitButton = screen.getByRole('button', { name: /sign up/i })
      await user.click(submitButton)
      
      await waitFor(() => {
        expect(mockSignup).toHaveBeenCalledWith({
          first_name: 'John',
          last_name: 'Doe',
          email: 'john@example.com',
          password: 'Test1234!',
        })
      })
    })
    
    it('should show success message after successful signup', async () => {
      const user = userEvent.setup()
      const mockSignup = vi.mocked(authApi.signupUser)
      mockSignup.mockResolvedValueOnce({
        user_id: 1,
        email: 'john@example.com',
        message: 'Verification email sent',
      })
      
      renderSignupForm()
      
      await user.type(screen.getByLabelText(/first name/i), 'John')
      await user.type(screen.getByLabelText(/last name/i), 'Doe')
      await user.type(screen.getByLabelText(/email address/i), 'john@example.com')
      await user.type(screen.getByLabelText(/^password/i), 'Test1234!')
      await user.click(screen.getByRole('button', { name: /sign up/i }))
      
      await waitFor(() => {
        expect(screen.getByText(/check your email/i)).toBeInTheDocument()
        expect(screen.getByText(/account created successfully/i)).toBeInTheDocument()
      })
    })
    
    it('should show error message on API failure', async () => {
      const user = userEvent.setup()
      const mockSignup = vi.mocked(authApi.signupUser)
      mockSignup.mockRejectedValueOnce(new Error('This email is already registered. Try logging in.'))
      
      renderSignupForm()
      
      await user.type(screen.getByLabelText(/first name/i), 'John')
      await user.type(screen.getByLabelText(/last name/i), 'Doe')
      await user.type(screen.getByLabelText(/email address/i), 'existing@example.com')
      await user.type(screen.getByLabelText(/^password/i), 'Test1234!')
      await user.click(screen.getByRole('button', { name: /sign up/i }))
      
      await waitFor(() => {
        expect(screen.getByText(/already registered/i)).toBeInTheDocument()
      })
    })
    
    it('should show loading state during submission', async () => {
      const user = userEvent.setup()
      const mockSignup = vi.mocked(authApi.signupUser)
      mockSignup.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 1000)))
      
      renderSignupForm()
      
      await user.type(screen.getByLabelText(/first name/i), 'John')
      await user.type(screen.getByLabelText(/last name/i), 'Doe')
      await user.type(screen.getByLabelText(/email address/i), 'john@example.com')
      await user.type(screen.getByLabelText(/^password/i), 'Test1234!')
      await user.click(screen.getByRole('button', { name: /sign up/i }))
      
      expect(screen.getByText(/creating account/i)).toBeInTheDocument()
      const submitButton = screen.getByRole('button', { name: /creating account/i })
      expect(submitButton).toBeDisabled()
    })
  })
  
  describe('Accessibility', () => {
    it('should have proper ARIA labels', () => {
      renderSignupForm()
      
      expect(screen.getByLabelText(/first name/i)).toHaveAttribute('aria-required', 'true')
      expect(screen.getByLabelText(/last name/i)).toHaveAttribute('aria-required', 'true')
      expect(screen.getByLabelText(/email address/i)).toHaveAttribute('aria-required', 'true')
      expect(screen.getByLabelText(/^password/i)).toHaveAttribute('aria-required', 'true')
    })
    
    it('should announce validation errors', async () => {
      const user = userEvent.setup()
      renderSignupForm()
      
      const emailInput = screen.getByLabelText(/email address/i)
      await user.type(emailInput, 'invalid')
      await user.tab()
      
      await waitFor(() => {
        const errorMessage = screen.getByRole('alert')
        expect(errorMessage).toBeInTheDocument()
      })
    })
  })
})

