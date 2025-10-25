/**
 * Companies API Client
 * Story 1.19: ABR Smart Search Integration
 * 
 * Handles:
 * - Smart company search (ABN/ACN/Name auto-detection)
 * - snake_case/camelCase transformations
 * - Error handling with user-friendly messages
 */

const API_BASE_URL = 'http://localhost:8000'

/**
 * Backend response format (snake_case)
 */
interface BackendSearchResult {
  company_name: string
  abn: string | null
  acn: string | null
  abn_formatted: string | null
  gst_registered: boolean | null
  entity_type: string | null
  business_address: string | null
  status: string | null
}

interface BackendSearchResponse {
  search_type: 'ABN' | 'ACN' | 'Name'
  query: string
  results: BackendSearchResult[]
  result_count: number
  cached: boolean
  response_time_ms: number
}

interface BackendSearchError {
  error: string
  message: string
  fallback_url?: string
}

/**
 * Frontend format (camelCase)
 */
export interface CompanySearchResult {
  companyName: string
  abn: string | null
  acn: string | null
  abnFormatted: string | null
  gstRegistered: boolean | null
  entityType: string | null
  businessAddress: string | null
  status: string | null
}

export interface CompanySearchResponse {
  searchType: 'ABN' | 'ACN' | 'Name'
  query: string
  results: CompanySearchResult[]
  resultCount: number
  cached: boolean
  responseTimeMs: number
}

export interface CompanySearchError {
  error: string
  message: string
  fallbackUrl?: string
}

/**
 * Transform backend result (snake_case) to frontend format (camelCase)
 */
function transformSearchResult(backendResult: BackendSearchResult): CompanySearchResult {
  return {
    companyName: backendResult.company_name,
    abn: backendResult.abn,
    acn: backendResult.acn,
    abnFormatted: backendResult.abn_formatted,
    gstRegistered: backendResult.gst_registered,
    entityType: backendResult.entity_type,
    businessAddress: backendResult.business_address,
    status: backendResult.status
  }
}

/**
 * Transform backend response (snake_case) to frontend format (camelCase)
 */
function transformSearchResponse(backendResponse: BackendSearchResponse): CompanySearchResponse {
  return {
    searchType: backendResponse.search_type,
    query: backendResponse.query,
    results: backendResponse.results.map(transformSearchResult),
    resultCount: backendResponse.result_count,
    cached: backendResponse.cached,
    responseTimeMs: backendResponse.response_time_ms
  }
}

/**
 * Enrich company data by searching ABN
 * 
 * Story 1.19: Two-step enrichment for name search results
 * When user selects from name search, automatically search by ABN to get full details
 * 
 * NOTE: This function makes a direct API call without using the search hook
 * to avoid triggering auto-select cascades
 * 
 * @param abn Company ABN to enrich
 * @returns Promise with enriched company data or null if fails
 */
export async function enrichCompanyByABN(abn: string): Promise<CompanySearchResult | null> {
  try {
    // Make direct API call (don't use searchCompanies to avoid state updates)
    const response = await fetch(`${API_BASE_URL}/api/companies/smart-search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        query: abn.trim(),
        max_results: 1
      })
    })

    if (!response.ok) {
      return null
    }

    const backendData: BackendSearchResponse = await response.json()
    const transformed = transformSearchResponse(backendData)
    
    return transformed.results[0] || null
    
  } catch (error) {
    console.warn('ABN enrichment failed:', error)
    return null
  }
}

/**
 * Search for companies by ABN, ACN, or name
 * 
 * Story 1.19: AC-1.19.1, AC-1.19.2, AC-1.19.3
 * 
 * Features:
 * - Auto-detects search type (ABN/ACN/Name)
 * - Returns cached results when available (~5ms)
 * - Handles errors gracefully
 * - No authentication required (public endpoint)
 * 
 * @param query Search query (ABN, ACN, or company name)
 * @param maxResults Maximum number of results (default: 10)
 * @returns Promise with search results or throws error
 */
export async function searchCompanies(
  query: string,
  maxResults: number = 10
): Promise<CompanySearchResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/companies/smart-search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        query: query.trim(),
        max_results: maxResults
      })
    })

    if (!response.ok) {
      // Handle error responses
      const errorData: BackendSearchError = await response.json().catch(() => ({
        error: 'UNKNOWN_ERROR',
        message: 'An unexpected error occurred. Please try again or enter details manually.'
      }))

      // Transform to frontend format
      const error: CompanySearchError = {
        error: errorData.error,
        message: errorData.message,
        fallbackUrl: errorData.fallback_url
      }

      throw error
    }

    // Success - transform response to camelCase
    const backendData: BackendSearchResponse = await response.json()
    return transformSearchResponse(backendData)

  } catch (error) {
    // Network errors or JSON parse errors
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw {
        error: 'NETWORK_ERROR',
        message: 'Unable to connect to server. Please check your internet connection.',
        fallbackUrl: undefined
      } as CompanySearchError
    }

    // Re-throw API errors
    throw error
  }
}

/**
 * Parse ABR business address into address components
 * 
 * Story 1.19: AC-1.19.5
 * 
 * Handles two formats:
 * - SimpleProtocol: "NSW 2000" (state postcode only)
 * - Full protocol: "341 George Street, Sydney NSW 2000"
 * 
 * @param businessAddress Business address from ABR (may be limited format)
 * @returns Address components (may be incomplete if parsing fails)
 */
export function parseBusinessAddress(businessAddress: string | null): {
  street: string
  suburb: string
  state: string
  postcode: string
} {
  if (!businessAddress) {
    return { street: '', suburb: '', state: '', postcode: '' }
  }

  // Default fallback
  const result = {
    street: '',
    suburb: '',
    state: '',
    postcode: ''
  }

  try {
    // Check if it's simplified format (just "STATE POSTCODE" like "NSW 2000")
    const simpleFormatMatch = businessAddress.match(/^([A-Z]{2,3})\s+(\d{4})$/)
    if (simpleFormatMatch) {
      result.state = simpleFormatMatch[1]
      result.postcode = simpleFormatMatch[2]
      return result
    }

    // Full address parsing
    let remaining = businessAddress
    
    // Try to extract postcode (4 digits at end)
    const postcodeMatch = businessAddress.match(/\b(\d{4})\s*$/)
    if (postcodeMatch) {
      result.postcode = postcodeMatch[1]
      remaining = businessAddress.substring(0, postcodeMatch.index).trim()
    }

    // Try to extract state (2-3 letter code before postcode)
    const stateMatch = remaining.match(/\b([A-Z]{2,3})\s*$/)
    if (stateMatch) {
      result.state = stateMatch[1]
      remaining = remaining.substring(0, stateMatch.index).trim()
    }

    // Split remaining by comma
    const parts = remaining.split(',').map(p => p.trim()).filter(Boolean)
    
    if (parts.length >= 2) {
      // Last part is likely suburb, everything else is street
      result.suburb = parts[parts.length - 1]
      result.street = parts.slice(0, -1).join(', ')
    } else if (parts.length === 1) {
      result.street = parts[0]
    }

  } catch (error) {
    // Parsing failed
    console.warn('Failed to parse business address:', error)
  }

  return result
}

