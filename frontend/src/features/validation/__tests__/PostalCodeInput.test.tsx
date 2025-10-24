/**
 * PostalCodeInput Component Tests - Story 1.20 (AC-1.20.3, AC-1.20.4, AC-1.20.5)
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { PostalCodeInput } from '../components/PostalCodeInput'
import * as useValidationHook from '../hooks/useValidation'

// Mock the useValidation hook
vi.mock('../hooks/useValidation')

describe('PostalCodeInput Component', () => {
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

  describe('AC-1.20.3: Postal code input with validation', () => {
    it('should render postal code input field', () => {
      render(<PostalCodeInput value="" onChange={mockOnChange} />)

      expect(screen.getByLabelText(/postcode/i)).toBeInTheDocument()
      expect(screen.getByPlaceholderText('2000')).toBeInTheDocument()
    })

    it('should call onChange when user types', async () => {
      const user = userEvent.setup()
      render(<PostalCodeInput value="" onChange={mockOnChange} />)

      const input = screen.getByLabelText(/postcode/i)
      await user.type(input, '2000')

      expect(mockOnChange).toHaveBeenCalled()
    })

    it('should validate on blur', async () => {
      const user = userEvent.setup()
      mockValidate.mockResolvedValue({ isValid: true })

      render(<PostalCodeInput value="2000" onChange={mockOnChange} />)

      const input = screen.getByLabelText(/postcode/i)
      await user.click(input)
      await user.tab() // Trigger blur

      await waitFor(() => {
        expect(mockValidate).toHaveBeenCalledWith('postal_code', '2000')
      })
    })

    it('should not validate empty values', async () => {
      const user = userEvent.setup()
      render(<PostalCodeInput value="" onChange={mockOnChange} />)

      const input = screen.getByLabelText(/postcode/i)
      await user.click(input)
      await user.tab()

      expect(mockValidate).not.toHaveBeenCalled()
    })

    // maxLength now dynamic from backend (Story 1.20 alignment mechanism)
  })

  describe('AC-1.20.4: Display error messages and examples', () => {
    it('should display error message from backend', async () => {
      const user = userEvent.setup()
      mockValidate.mockResolvedValue({
        isValid: false,
        errorMessage: 'Postcode must be 4 digits',
        exampleValue: '2000'
      })

      render(<PostalCodeInput value="200" onChange={mockOnChange} />)

      const input = screen.getByLabelText(/postcode/i)
      await user.click(input)
      await user.tab()

      await waitFor(() => {
        expect(screen.getByText(/postcode must be 4 digits/i)).toBeInTheDocument()
      })
    })

    it('should display example value when validation fails', async () => {
      const user = userEvent.setup()
      mockValidate.mockResolvedValue({
        isValid: false,
        errorMessage: 'Invalid postcode',
        exampleValue: '2000'
      })

      render(<PostalCodeInput value="999" onChange={mockOnChange} />)

      const input = screen.getByLabelText(/postcode/i)
      await user.click(input)
      await user.tab()

      await waitFor(() => {
        expect(screen.getByText(/example:/i)).toBeInTheDocument()
        expect(screen.getByText('2000')).toBeInTheDocument()
      })
    })

    it('should display success indicator when valid', async () => {
      const user = userEvent.setup()
      mockValidate.mockResolvedValue({ isValid: true })

      render(<PostalCodeInput value="2000" onChange={mockOnChange} />)

      const input = screen.getByLabelText(/postcode/i)
      await user.click(input)
      await user.tab()

      await waitFor(() => {
        expect(screen.getByText(/valid postcode/i)).toBeInTheDocument()
      })
    })
  })

  describe('AC-1.20.5: Mobile responsive and accessible', () => {
    it('should have mobile-friendly input type', () => {
      render(<PostalCodeInput value="" onChange={mockOnChange} />)

      const input = screen.getByLabelText(/postcode/i)
      expect(input).toHaveAttribute('type', 'text')
      expect(input).toHaveAttribute('inputMode', 'numeric')
    })

    it('should have ARIA attributes', () => {
      render(<PostalCodeInput value="" onChange={mockOnChange} required={true} />)

      const input = screen.getByLabelText(/postcode/i)
      expect(input).toHaveAttribute('aria-label', 'Postcode')
      expect(input).toHaveAttribute('aria-required', 'true')
    })

    it('should have ARIA invalid state when validation fails', async () => {
      const user = userEvent.setup()
      mockValidate.mockResolvedValue({
        isValid: false,
        errorMessage: 'Invalid'
      })

      render(<PostalCodeInput value="invalid" onChange={mockOnChange} />)

      const input = screen.getByLabelText(/postcode/i)
      await user.click(input)
      await user.tab()

      await waitFor(() => {
        expect(input).toHaveAttribute('aria-invalid', 'true')
        expect(input).toHaveAttribute('aria-describedby', 'postalCode-error')
      })
    })

    it('should be touch-friendly with proper padding', () => {
      render(<PostalCodeInput value="" onChange={mockOnChange} />)

      const input = screen.getByLabelText(/postcode/i)
      expect(input).toHaveClass('py-3', 'px-4') // 44px minimum touch target
    })
  })

  describe('Loading state', () => {
    it('should show loading spinner during validation', () => {
      vi.mocked(useValidationHook.useValidation).mockReturnValue({
        validate: mockValidate,
        isValidating: true
      })

      render(<PostalCodeInput value="2000" onChange={mockOnChange} />)

      const spinner = document.querySelector('.animate-spin')
      expect(spinner).toBeInTheDocument()
    })
  })

  describe('Visual feedback', () => {
    it('should show green border when valid', async () => {
      const user = userEvent.setup()
      mockValidate.mockResolvedValue({ isValid: true })

      render(<PostalCodeInput value="2000" onChange={mockOnChange} />)

      const input = screen.getByLabelText(/postcode/i)
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

      render(<PostalCodeInput value="999" onChange={mockOnChange} />)

      const input = screen.getByLabelText(/postcode/i)
      await user.click(input)
      await user.tab()

      await waitFor(() => {
        expect(input).toHaveClass('border-red-500')
      })
    })
  })

  describe('Required field indicator', () => {
    it('should show asterisk when required', () => {
      render(<PostalCodeInput value="" onChange={mockOnChange} required={true} />)

      expect(screen.getByText('*')).toBeInTheDocument()
    })

    it('should not show asterisk when optional', () => {
      render(<PostalCodeInput value="" onChange={mockOnChange} required={false} />)

      const label = screen.getByText(/postcode/i)
      expect(label).not.toContainHTML('*')
    })
  })

  describe('Disabled state', () => {
    it('should disable input when disabled prop is true', () => {
      render(<PostalCodeInput value="" onChange={mockOnChange} disabled={true} />)

      const input = screen.getByLabelText(/postcode/i)
      expect(input).toBeDisabled()
      expect(input).toHaveClass('bg-gray-100')
    })
  })
})

