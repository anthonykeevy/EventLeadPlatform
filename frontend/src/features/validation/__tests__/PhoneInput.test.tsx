/**
 * PhoneInput Component Tests - Story 1.20 (AC-1.20.2, AC-1.20.4, AC-1.20.5)
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { PhoneInput } from '../components/PhoneInput'
import * as useValidationHook from '../hooks/useValidation'

// Mock the useValidation hook
vi.mock('../hooks/useValidation')

describe('PhoneInput Component', () => {
  const mockValidate = vi.fn()
  const mockOnChange = vi.fn()
  const mockOnBlur = vi.fn()

  beforeEach(() => {
    vi.clearAllMocks()
    vi.mocked(useValidationHook.useValidation).mockReturnValue({
      validate: mockValidate,
      isValidating: false
    })
  })

  describe('AC-1.20.2: Phone input with validation', () => {
    it('should render phone input field', () => {
      render(<PhoneInput value="" onChange={mockOnChange} />)

      expect(screen.getByLabelText(/phone number/i)).toBeInTheDocument()
      expect(screen.getByPlaceholderText('0412345678')).toBeInTheDocument()  // Local format placeholder
    })

    it('should call onChange when user types', async () => {
      const user = userEvent.setup()
      render(<PhoneInput value="" onChange={mockOnChange} />)

      const input = screen.getByLabelText(/phone number/i)
      await user.type(input, '+61412345678')

      expect(mockOnChange).toHaveBeenCalled()
    })

    it('should validate on blur', async () => {
      const user = userEvent.setup()
      mockValidate.mockResolvedValue({ isValid: true })

      render(<PhoneInput value="+61412345678" onChange={mockOnChange} />)

      const input = screen.getByLabelText(/phone number/i)
      await user.click(input)
      await user.tab() // Trigger blur

      await waitFor(() => {
        expect(mockValidate).toHaveBeenCalledWith('phone', '+61412345678')
      })
    })

    it('should not validate empty values', async () => {
      const user = userEvent.setup()
      render(<PhoneInput value="" onChange={mockOnChange} />)

      const input = screen.getByLabelText(/phone number/i)
      await user.click(input)
      await user.tab()

      expect(mockValidate).not.toHaveBeenCalled()
    })
  })

  describe('AC-1.20.4: Display error messages and examples', () => {
    it('should display error message from backend', async () => {
      const user = userEvent.setup()
      mockValidate.mockResolvedValue({
        isValid: false,
        errorMessage: 'Mobile phone must be +61 followed by 4 or 5 and 8 digits',
        exampleValue: '+61412345678'
      })

      render(<PhoneInput value="invalid" onChange={mockOnChange} />)

      const input = screen.getByLabelText(/phone number/i)
      await user.click(input)
      await user.tab()

      await waitFor(() => {
        expect(screen.getByText(/mobile phone must be \+61/i)).toBeInTheDocument()
      })
    })

    it('should display example value when validation fails', async () => {
      const user = userEvent.setup()
      mockValidate.mockResolvedValue({
        isValid: false,
        errorMessage: 'Invalid phone number',
        exampleValue: '+61412345678'
      })

      render(<PhoneInput value="invalid" onChange={mockOnChange} />)

      const input = screen.getByLabelText(/phone number/i)
      await user.click(input)
      await user.tab()

      await waitFor(() => {
        expect(screen.getByText(/example:/i)).toBeInTheDocument()
        expect(screen.getByText('+61412345678')).toBeInTheDocument()
      })
    })

    it('should display success indicator when valid', async () => {
      const user = userEvent.setup()
      mockValidate.mockResolvedValue({ isValid: true })

      render(<PhoneInput value="+61412345678" onChange={mockOnChange} />)

      const input = screen.getByLabelText(/phone number/i)
      await user.click(input)
      await user.tab()

      await waitFor(() => {
        expect(screen.getByText(/valid phone number/i)).toBeInTheDocument()
      })
    })
  })

  describe('AC-1.20.5: Mobile responsive and accessible', () => {
    it('should have mobile-friendly input type', () => {
      render(<PhoneInput value="" onChange={mockOnChange} />)

      const input = screen.getByLabelText(/phone number/i)
      expect(input).toHaveAttribute('type', 'tel')
      expect(input).toHaveAttribute('inputMode', 'tel')
    })

    it('should have ARIA attributes', () => {
      render(<PhoneInput value="" onChange={mockOnChange} required={true} />)

      const input = screen.getByLabelText(/phone number/i)
      expect(input).toHaveAttribute('aria-label', 'Phone Number')
      expect(input).toHaveAttribute('aria-required', 'true')
    })

    it('should have ARIA invalid state when validation fails', async () => {
      const user = userEvent.setup()
      mockValidate.mockResolvedValue({
        isValid: false,
        errorMessage: 'Invalid'
      })

      render(<PhoneInput value="invalid" onChange={mockOnChange} />)

      const input = screen.getByLabelText(/phone number/i)
      await user.click(input)
      await user.tab()

      await waitFor(() => {
        expect(input).toHaveAttribute('aria-invalid', 'true')
        expect(input).toHaveAttribute('aria-describedby', 'phone-error')
      })
    })
  })

  describe('Loading state', () => {
    it('should show loading spinner during validation', () => {
      vi.mocked(useValidationHook.useValidation).mockReturnValue({
        validate: mockValidate,
        isValidating: true
      })

      render(<PhoneInput value="+61412345678" onChange={mockOnChange} />)

      // Loading spinner should be visible
      const spinner = document.querySelector('.animate-spin')
      expect(spinner).toBeInTheDocument()
    })
  })

  describe('Visual feedback', () => {
    it('should show green border when valid', async () => {
      const user = userEvent.setup()
      mockValidate.mockResolvedValue({ isValid: true })

      render(<PhoneInput value="+61412345678" onChange={mockOnChange} />)

      const input = screen.getByLabelText(/phone number/i)
      await user.click(input)
      await user.tab()

      await waitFor(() => {
        expect(input).toHaveClass('border-green-500')
      })
    })

    it('should show red border when invalid', async () => {
      const user = userEvent.setup()
      mockValidate.mockResolvedValue({
        isValid: false,
        errorMessage: 'Invalid'
      })

      render(<PhoneInput value="invalid" onChange={mockOnChange} />)

      const input = screen.getByLabelText(/phone number/i)
      await user.click(input)
      await user.tab()

      await waitFor(() => {
        expect(input).toHaveClass('border-red-500')
      })
    })
  })

  describe('Disabled state', () => {
    it('should disable input when disabled prop is true', () => {
      render(<PhoneInput value="" onChange={mockOnChange} disabled={true} />)

      const input = screen.getByLabelText(/phone number/i)
      expect(input).toBeDisabled()
      expect(input).toHaveClass('bg-gray-100')
    })
  })
})

