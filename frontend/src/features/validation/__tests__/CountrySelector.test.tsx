/**
 * CountrySelector Component Tests - Story 1.20
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { CountrySelector } from '../components/CountrySelector'
import * as useCountriesHook from '../hooks/useCountries'

// Mock useCountries hook
vi.mock('../hooks/useCountries')

describe('CountrySelector Component', () => {
  const mockOnChange = vi.fn()
  
  const mockCountries = [
    { id: 1, code: 'AU', name: 'Australia', phone_prefix: '+61', postal_label: 'Postcode', tax_id_label: 'ABN', state_label: 'State', tax_id_example: '', postal_example: '', tax_id_required: true, has_company_search: true, company_search_label: 'Search ABN', currency_code: 'AUD', currency_symbol: '$', tax_name: 'GST', tax_rate: 0.10 },
    { id: 14, code: 'NZ', name: 'New Zealand', phone_prefix: '+64', postal_label: 'Postcode', tax_id_label: 'NZBN', state_label: 'Region', tax_id_example: '', postal_example: '', tax_id_required: false, has_company_search: false, company_search_label: null, currency_code: 'NZD', currency_symbol: '$', tax_name: 'GST', tax_rate: 0.15 },
    { id: 15, code: 'US', name: 'United States', phone_prefix: '+1', postal_label: 'ZIP Code', tax_id_label: 'EIN', state_label: 'State', tax_id_example: '', postal_example: '', tax_id_required: false, has_company_search: false, company_search_label: null, currency_code: 'USD', currency_symbol: '$', tax_name: 'Sales Tax', tax_rate: null },
    { id: 16, code: 'GB', name: 'United Kingdom', phone_prefix: '+44', postal_label: 'Postcode', tax_id_label: 'VAT', state_label: 'County', tax_id_example: '', postal_example: '', tax_id_required: false, has_company_search: true, company_search_label: 'Companies House', currency_code: 'GBP', currency_symbol: '£', tax_name: 'VAT', tax_rate: 0.20 },
    { id: 17, code: 'CA', name: 'Canada', phone_prefix: '+1', postal_label: 'Postal Code', tax_id_label: 'BN', state_label: 'Province', tax_id_example: '', postal_example: '', tax_id_required: false, has_company_search: false, company_search_label: null, currency_code: 'CAD', currency_symbol: '$', tax_name: 'GST', tax_rate: 0.05 }
  ]
  
  beforeEach(() => {
    vi.clearAllMocks()
    vi.mocked(useCountriesHook.useCountries).mockReturnValue({
      countries: mockCountries,
      isLoading: false,
      error: null,
      getCountryById: (id) => mockCountries.find(c => c.id === id),
      getCountryByCode: (code) => mockCountries.find(c => c.code === code)
    })
  })

  it('should render country dropdown', () => {
    render(<CountrySelector value={1} onChange={mockOnChange} />)

    expect(screen.getByLabelText(/country/i)).toBeInTheDocument()
    expect(screen.getByRole('combobox')).toBeInTheDocument()
  })

  it('should display all 5 countries', () => {
    render(<CountrySelector value={1} onChange={mockOnChange} />)

    const select = screen.getByRole('combobox')
    const options = select.querySelectorAll('option')
    
    expect(options).toHaveLength(5)
    expect(options[0]).toHaveTextContent('+61 Australia')
    expect(options[1]).toHaveTextContent('+64 New Zealand')
    expect(options[2]).toHaveTextContent('+1 United States')
    expect(options[3]).toHaveTextContent('+44 United Kingdom')
    expect(options[4]).toHaveTextContent('+1 Canada')
  })

  it('should call onChange when country selected', async () => {
    const user = userEvent.setup()
    render(<CountrySelector value={1} onChange={mockOnChange} />)

    const select = screen.getByRole('combobox')
    await user.selectOptions(select, '14')  // Select New Zealand (CountryID=14)

    expect(mockOnChange).toHaveBeenCalledWith(14)
  })

  it('should show auto-detect help text', () => {
    render(<CountrySelector value={1} onChange={mockOnChange} />)

    expect(screen.getByText(/auto-detected based on your location/i)).toBeInTheDocument()
  })

  it('should have required indicator', () => {
    render(<CountrySelector value={1} onChange={mockOnChange} />)

    expect(screen.getByText('*')).toBeInTheDocument()
  })
})

