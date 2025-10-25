/**
 * Company Search Hook
 * Story 1.19: AC-1.19.2 - Debounced search with loading states
 */

import { useState, useEffect, useRef, useCallback } from 'react'
import { searchCompanies, CompanySearchResponse, CompanySearchError } from '../api/companiesApi'

interface UseCompanySearchResult {
  data: CompanySearchResponse | null
  isLoading: boolean
  error: CompanySearchError | null
  search: (query: string) => void
  clearResults: () => void
}

/**
 * Hook for debounced company search
 * 
 * Features:
 * - Debounces search input (300ms default)
 * - Cancels previous searches when new query entered
 * - Loading states
 * - Error handling
 * 
 * @param debounceMs Debounce delay in milliseconds (default: 300)
 * @param minQueryLength Minimum query length to trigger search (default: 2)
 */
export function useCompanySearch(
  debounceMs: number = 300,
  minQueryLength: number = 2
): UseCompanySearchResult {
  const [data, setData] = useState<CompanySearchResponse | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<CompanySearchError | null>(null)
  const [query, setQuery] = useState('')
  
  // Debounce timer
  const debounceTimer = useRef<NodeJS.Timeout | null>(null)
  
  // Current search abort controller
  const abortController = useRef<AbortController | null>(null)

  useEffect(() => {
    return () => {
      // Cleanup on unmount
      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current)
      }
      if (abortController.current) {
        abortController.current.abort()
      }
    }
  }, [])

  useEffect(() => {
    // Clear previous debounce timer
    if (debounceTimer.current) {
      clearTimeout(debounceTimer.current)
    }

    // Clear results if query is too short
    if (query.length < minQueryLength) {
      setData(null)
      setError(null)
      setIsLoading(false)
      return
    }

    // Clear error immediately, but DON'T set loading yet (wait for debounce)
    setError(null)

    // Debounce the search
    debounceTimer.current = setTimeout(async () => {
      // NOW set loading state (after debounce delay)
      setIsLoading(true)
      
      // Cancel previous search
      if (abortController.current) {
        abortController.current.abort()
      }

      // Create new abort controller
      abortController.current = new AbortController()

      try {
        const results = await searchCompanies(query)
        
        setData(results)
        setError(null)
        setIsLoading(false)
      } catch (err) {
        // Check if error was from abort
        if (err instanceof DOMException && err.name === 'AbortError') {
          // Search was cancelled - don't update state
          return
        }

        setError(err as CompanySearchError)
        setData(null)
        setIsLoading(false)
      }
    }, debounceMs)

    return () => {
      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current)
      }
    }
  }, [query, debounceMs, minQueryLength])

  const search = useCallback((newQuery: string) => {
    setQuery(newQuery)
  }, [])

  const clearResults = useCallback(() => {
    setQuery('')
    setData(null)
    setError(null)
    setIsLoading(false)
  }, [])

  return {
    data,
    isLoading,
    error,
    search,
    clearResults
  }
}

