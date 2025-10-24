/**
 * useCountries Hook - Story 1.20
 * Fetches active countries from API for dynamic country selection
 */

import { useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export interface Country {
  id: number
  code: string
  name: string
  phone_prefix: string
  currency_code: string
  currency_symbol: string
  tax_name: string
  tax_rate: number | null
  postal_label: string
  postal_example: string
  state_label: string
  tax_id_label: string
  tax_id_example: string
  tax_id_required: boolean
  has_company_search: boolean
  company_search_label: string | null
}

export interface UseCountriesReturn {
  countries: Country[]
  isLoading: boolean
  error: string | null
  getCountryById: (id: number) => Country | undefined
  getCountryByCode: (code: string) => Country | undefined
}

/**
 * Fetch active countries from API
 * Caches in memory for session duration
 */
export function useCountries(): UseCountriesReturn {
  const [countries, setCountries] = useState<Country[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchCountries = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/api/countries`)
        setCountries(response.data)
        setError(null)
      } catch (err) {
        console.error('Failed to fetch countries:', err)
        setError('Failed to load countries')
        // Fallback to Australia only
        setCountries([{
          id: 1,
          code: 'AU',
          name: 'Australia',
          phone_prefix: '+61',
          currency_code: 'AUD',
          currency_symbol: '$',
          tax_name: 'GST',
          tax_rate: 0.10,
          postal_label: 'Postcode',
          postal_example: '2000',
          state_label: 'State',
          tax_id_label: 'ABN',
          tax_id_example: '53004085616',
          tax_id_required: true,
          has_company_search: true,
          company_search_label: 'Search ABN'
        }])
      } finally {
        setIsLoading(false)
      }
    }

    fetchCountries()
  }, [])

  const getCountryById = (id: number) => {
    return countries.find(c => c.id === id)
  }

  const getCountryByCode = (code: string) => {
    return countries.find(c => c.code === code)
  }

  return {
    countries,
    isLoading,
    error,
    getCountryById,
    getCountryByCode
  }
}

