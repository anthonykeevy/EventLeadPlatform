/**
 * LoginForm Component Tests - Story 1.9 (AC-1.9.2, AC-1.9.4)
 * Tests for login form rendering, validation, and interaction
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { BrowserRouter } from 'react-router-dom'
import { LoginForm } from '../components/LoginForm'
import { AuthProvider } from '../context/AuthContext'
import * as authApi from '../api/authApi'

// Mock the API
vi.mock('../api/authApi')

const mockNavigate = vi.fn()
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom')
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  }
})

function renderLoginForm() {
  return render(
    <BrowserRouter>
      <AuthProvider>
        <LoginForm />
      </AuthProvider>
    </BrowserRouter>
  )
}

describe('LoginForm Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.clear()
  })
  
  describe('Rendering', () => {
    it('should render login form with all fields', () => {
      renderLoginForm()
      
      expect(screen.getByLabelText(/email address/i)).toBeInTheDocument()
      expect(screen.getByLabelText(/^password/i)).toBeInTheDocument()
      expect(screen.getByLabelText(/remember me/i)).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /log in/i })).toBeInTheDocument()
    })
    
    it('should have submit button disabled initially', () => {
      renderLoginForm()
      
      const submitButton = screen.getByRole('button', { name: /log in/i })
      expect(submitButton).toBeDisabled()
    })
    
    it('should render "Forgot password?" link', () => {
      renderLoginForm()
      
      expect(screen.getByRole('link', { name: /forgot password/i })).toBeInTheDocument()
      expect(screen.getByRole('link', { name: /forgot password/i })).toHaveAttribute('href', '/forgot-password')
    })
    
    it('should render link to signup page', () => {
      renderLoginForm()
      
      expect(screen.getByRole('link', { name: /sign up/i })).toBeInTheDocument()
    })
  })
  
  describe('Validation', () => {
    it('should show error for invalid email format', async () => {
      const user = userEvent.setup()
      renderLoginForm()
      
      const emailInput = screen.getByLabelText(/email address/i)
      await user.type(emailInput, 'invalid-email')
      await user.tab()
      
      await waitFor(() => {
        expect(screen.getByText(/please enter a valid email address/i)).toBeInTheDocument()
      })
    })
    
    it('should show error for empty password', async () => {
      const user = userEvent.setup()
      renderLoginForm()
      
      const emailInput = screen.getByLabelText(/email address/i)
      await user.type(emailInput, 'test@example.com')
      const submitButton = screen.getByRole('button', { name: /log in/i })
      
      // Should remain disabled without password
      expect(submitButton).toBeDisabled()
    })
    
    it('should enable submit button when fields are valid', async () => {
      const user = userEvent.setup()
      renderLoginForm()
      
      await user.type(screen.getByLabelText(/email address/i), 'test@example.com')
      await user.type(screen.getByLabelText(/^password/i), 'Password123!')
      
      await waitFor(() => {
        const submitButton = screen.getByRole('button', { name: /log in/i })
        expect(submitButton).not.toBeDisabled()
      })
    })
  })
  
  describe('Password Visibility Toggle', () => {
    it('should toggle password visibility', async () => {
      const user = userEvent.setup()
      renderLoginForm()
      
      const passwordInput = screen.getByLabelText(/^password/i) as HTMLInputElement
      expect(passwordInput.type).toBe('password')
      
      const toggleButton = screen.getByLabelText(/show password/i)
      await user.click(toggleButton)
      
      expect(passwordInput.type).toBe('text')
      expect(screen.getByLabelText(/hide password/i)).toBeInTheDocument()
    })
  })
  
  describe('Remember Me Checkbox', () => {
    it('should toggle remember me checkbox', async () => {
      const user = userEvent.setup()
      renderLoginForm()
      
      const checkbox = screen.getByLabelText(/remember me/i) as HTMLInputElement
      expect(checkbox.checked).toBe(false)
      
      await user.click(checkbox)
      expect(checkbox.checked).toBe(true)
    })
  })
  
  describe('Form Submission', () => {
    it('should call login API on valid form submission', async () => {
      const user = userEvent.setup()
      const mockLogin = vi.mocked(authApi.loginUser)
      mockLogin.mockResolvedValueOnce({
        access_token: 'access_token_123',
        refresh_token: 'refresh_token_456',
        token_type: 'Bearer',
        user: {
          id: 1,
          email: 'test@example.com',
          first_name: 'Test',
          last_name: 'User',
          email_verified: true,
          is_active: true,
          onboarding_complete: true,
          created_at: '2025-01-01',
        },
      })
      
      renderLoginForm()
      
      await user.type(screen.getByLabelText(/email address/i), 'test@example.com')
      await user.type(screen.getByLabelText(/^password/i), 'Password123!')
      await user.click(screen.getByRole('button', { name: /log in/i }))
      
      await waitFor(() => {
        expect(mockLogin).toHaveBeenCalledWith({
          email: 'test@example.com',
          password: 'Password123!',
        })
      })
    })
    
    it('should navigate to dashboard after successful login (onboarding complete)', async () => {
      const user = userEvent.setup()
      const mockLogin = vi.mocked(authApi.loginUser)
      mockLogin.mockResolvedValueOnce({
        access_token: 'access_token_123',
        refresh_token: 'refresh_token_456',
        token_type: 'Bearer',
        user: {
          id: 1,
          email: 'test@example.com',
          first_name: 'Test',
          last_name: 'User',
          email_verified: true,
          is_active: true,
          onboarding_complete: true,
          created_at: '2025-01-01',
        },
      })
      
      renderLoginForm()
      
      await user.type(screen.getByLabelText(/email address/i), 'test@example.com')
      await user.type(screen.getByLabelText(/^password/i), 'Password123!')
      await user.click(screen.getByRole('button', { name: /log in/i }))
      
      await waitFor(() => {
        expect(mockNavigate).toHaveBeenCalledWith('/dashboard')
      })
    })
    
    it('should navigate to onboarding after successful login (onboarding incomplete)', async () => {
      const user = userEvent.setup()
      const mockLogin = vi.mocked(authApi.loginUser)
      mockLogin.mockResolvedValueOnce({
        access_token: 'access_token_123',
        refresh_token: 'refresh_token_456',
        token_type: 'Bearer',
        user: {
          id: 1,
          email: 'test@example.com',
          first_name: 'Test',
          last_name: 'User',
          email_verified: true,
          is_active: true,
          onboarding_complete: false,
          created_at: '2025-01-01',
        },
      })
      
      renderLoginForm()
      
      await user.type(screen.getByLabelText(/email address/i), 'test@example.com')
      await user.type(screen.getByLabelText(/^password/i), 'Password123!')
      await user.click(screen.getByRole('button', { name: /log in/i }))
      
      await waitFor(() => {
        expect(mockNavigate).toHaveBeenCalledWith('/onboarding')
      })
    })
    
    it('should show error message on invalid credentials', async () => {
      const user = userEvent.setup()
      const mockLogin = vi.mocked(authApi.loginUser)
      mockLogin.mockRejectedValueOnce(new Error('Email or password is incorrect.'))
      
      renderLoginForm()
      
      await user.type(screen.getByLabelText(/email address/i), 'test@example.com')
      await user.type(screen.getByLabelText(/^password/i), 'WrongPassword')
      await user.click(screen.getByRole('button', { name: /log in/i }))
      
      await waitFor(() => {
        expect(screen.getByText(/email or password is incorrect/i)).toBeInTheDocument()
      })
    })
    
    it('should show error message for unverified email', async () => {
      const user = userEvent.setup()
      const mockLogin = vi.mocked(authApi.loginUser)
      mockLogin.mockRejectedValueOnce(new Error('Please verify your email before logging in.'))
      
      renderLoginForm()
      
      await user.type(screen.getByLabelText(/email address/i), 'unverified@example.com')
      await user.type(screen.getByLabelText(/^password/i), 'Password123!')
      await user.click(screen.getByRole('button', { name: /log in/i }))
      
      await waitFor(() => {
        expect(screen.getByText(/verify your email/i)).toBeInTheDocument()
      })
    })
    
    it('should show loading state during submission', async () => {
      const user = userEvent.setup()
      const mockLogin = vi.mocked(authApi.loginUser)
      mockLogin.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 1000)))
      
      renderLoginForm()
      
      await user.type(screen.getByLabelText(/email address/i), 'test@example.com')
      await user.type(screen.getByLabelText(/^password/i), 'Password123!')
      await user.click(screen.getByRole('button', { name: /log in/i }))
      
      expect(screen.getByText(/logging in/i)).toBeInTheDocument()
      const submitButton = screen.getByRole('button', { name: /logging in/i })
      expect(submitButton).toBeDisabled()
    })
  })
  
  describe('Accessibility', () => {
    it('should have proper ARIA labels', () => {
      renderLoginForm()
      
      expect(screen.getByLabelText(/email address/i)).toHaveAttribute('aria-required', 'true')
      expect(screen.getByLabelText(/^password/i)).toHaveAttribute('aria-required', 'true')
    })
    
    it('should announce validation errors', async () => {
      const user = userEvent.setup()
      renderLoginForm()
      
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



