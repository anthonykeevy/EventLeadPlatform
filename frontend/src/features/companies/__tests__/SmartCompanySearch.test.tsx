/**
 * SmartCompanySearch Component Tests
 * Story 1.19: AC-1.19.1, AC-1.19.2, AC-1.19.3
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { SmartCompanySearch } from '../components/SmartCompanySearch'
import * as companiesApi from '../api/companiesApi'

// Mock the API module
vi.mock('../api/companiesApi', () => ({
  searchCompanies: vi.fn(),
  parseBusinessAddress: vi.fn()
}))

describe('SmartCompanySearch', () => {
  const mockOnCompanySelected = vi.fn()
  const mockOnManualEntry = vi.fn()

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders search input', () => {
    render(
      <SmartCompanySearch
        onCompanySelected={mockOnCompanySelected}
        onManualEntry={mockOnManualEntry}
      />
    )

    expect(screen.getByPlaceholderText(/search by abn, acn, or company name/i)).toBeInTheDocument()
  })

  it('shows manual entry link', () => {
    render(
      <SmartCompanySearch
        onCompanySelected={mockOnCompanySelected}
        onManualEntry={mockOnManualEntry}
      />
    )

    expect(screen.getByText(/can't find your company\? enter details manually/i)).toBeInTheDocument()
  })

  it('detects ABN search type (11 digits)', async () => {
    const user = userEvent.setup()
    render(
      <SmartCompanySearch
        onCompanySelected={mockOnCompanySelected}
        onManualEntry={mockOnManualEntry}
      />
    )

    const input = screen.getByPlaceholderText(/search by abn, acn, or company name/i)
    await user.type(input, '53102443916')

    await waitFor(() => {
      expect(screen.getByText(/searching by:/i)).toBeInTheDocument()
      expect(screen.getByText(/ABN/)).toBeInTheDocument()
    })
  })

  it('detects ACN search type (9 digits)', async () => {
    const user = userEvent.setup()
    render(
      <SmartCompanySearch
        onCompanySelected={mockOnCompanySelected}
        onManualEntry={mockOnManualEntry}
      />
    )

    const input = screen.getByPlaceholderText(/search by abn, acn, or company name/i)
    await user.type(input, '123456789')

    await waitFor(() => {
      expect(screen.getByText(/ACN/)).toBeInTheDocument()
    })
  })

  it('detects Name search type (text)', async () => {
    const user = userEvent.setup()
    render(
      <SmartCompanySearch
        onCompanySelected={mockOnCompanySelected}
        onManualEntry={mockOnManualEntry}
      />
    )

    const input = screen.getByPlaceholderText(/search by abn, acn, or company name/i)
    await user.type(input, 'Atlassian')

    await waitFor(() => {
      expect(screen.getByText(/Name/)).toBeInTheDocument()
    })
  })

  it('shows loading state during search', async () => {
    const user = userEvent.setup()
    
    // Mock API to delay response
    vi.mocked(companiesApi.searchCompanies).mockImplementation(
      () => new Promise(resolve => setTimeout(resolve, 1000))
    )

    render(
      <SmartCompanySearch
        onCompanySelected={mockOnCompanySelected}
        onManualEntry={mockOnManualEntry}
      />
    )

    const input = screen.getByPlaceholderText(/search by abn, acn, or company name/i)
    await user.type(input, 'Atlassian')

    // Should show loading state after debounce
    await waitFor(() => {
      expect(screen.getByText(/searching australian business register/i)).toBeInTheDocument()
    }, { timeout: 500 })
  })

  it('handles search error gracefully', async () => {
    const user = userEvent.setup()
    
    // Mock API error
    vi.mocked(companiesApi.searchCompanies).mockRejectedValue({
      error: 'ABR_API_ERROR',
      message: 'Unable to search ABR. Please check your internet connection.',
      fallbackUrl: '/companies/manual-entry'
    })

    render(
      <SmartCompanySearch
        onCompanySelected={mockOnCompanySelected}
        onManualEntry={mockOnManualEntry}
      />
    )

    const input = screen.getByPlaceholderText(/search by abn, acn, or company name/i)
    await user.type(input, 'Atlassian')

    await waitFor(() => {
      expect(screen.getByText(/search unavailable/i)).toBeInTheDocument()
      expect(screen.getByText(/unable to search abr/i)).toBeInTheDocument()
    }, { timeout: 1000 })

    // Should show manual entry button in error state
    const manualButton = screen.getByText(/enter company details manually/i)
    await user.click(manualButton)
    expect(mockOnManualEntry).toHaveBeenCalled()
  })

  it('displays search results', async () => {
    const user = userEvent.setup()
    
    // Mock successful search
    vi.mocked(companiesApi.searchCompanies).mockResolvedValue({
      searchType: 'Name',
      query: 'Atlassian',
      results: [
        {
          companyName: 'Atlassian Pty Ltd',
          abn: '53102443916',
          abnFormatted: '53 102 443 916',
          gstRegistered: true,
          entityType: 'Australian Private Company',
          businessAddress: '341 George Street, Sydney NSW 2000',
          status: 'Active'
        }
      ],
      resultCount: 1,
      cached: false,
      responseTimeMs: 1250
    })

    render(
      <SmartCompanySearch
        onCompanySelected={mockOnCompanySelected}
        onManualEntry={mockOnManualEntry}
      />
    )

    const input = screen.getByPlaceholderText(/search by abn, acn, or company name/i)
    await user.type(input, 'Atlassian')

    await waitFor(() => {
      // Text is split by highlight - use regex matcher
      expect(screen.getByText(/Atlassian/)).toBeInTheDocument()
      expect(screen.getByText(/Pty Ltd/)).toBeInTheDocument()
      expect(screen.getByText('53 102 443 916')).toBeInTheDocument()
    }, { timeout: 1000 })
  })

  it('shows no results message', async () => {
    const user = userEvent.setup()
    
    // Mock empty results
    vi.mocked(companiesApi.searchCompanies).mockResolvedValue({
      searchType: 'Name',
      query: 'NonExistentCompany',
      results: [],
      resultCount: 0,
      cached: false,
      responseTimeMs: 850
    })

    render(
      <SmartCompanySearch
        onCompanySelected={mockOnCompanySelected}
        onManualEntry={mockOnManualEntry}
      />
    )

    const input = screen.getByPlaceholderText(/search by abn, acn, or company name/i)
    await user.type(input, 'NonExistentCompany')

    await waitFor(() => {
      expect(screen.getByText(/no companies found/i)).toBeInTheDocument()
    }, { timeout: 1000 })
  })

  it('calls onManualEntry when clicking manual entry link', async () => {
    const user = userEvent.setup()
    render(
      <SmartCompanySearch
        onCompanySelected={mockOnCompanySelected}
        onManualEntry={mockOnManualEntry}
      />
    )

    const link = screen.getByText(/can't find your company\? enter details manually/i)
    await user.click(link)

    expect(mockOnManualEntry).toHaveBeenCalled()
  })
})

