/**
 * Smart Company Search Component
 * Story 1.19: AC-1.19.1, AC-1.19.2, AC-1.19.3, AC-1.19.4
 * 
 * Features:
 * - Smart search with auto-detection (ABN/ACN/Name)
 * - Debounced input (300ms)
 * - Loading states and error handling
 * - Auto-selection for single results
 */

import React, { useState, useEffect, useCallback } from 'react'
import { Search, Loader2, AlertCircle, Info } from 'lucide-react'
import { useCompanySearch } from '../hooks/useCompanySearch'
import { CompanySearchResults } from './CompanySearchResults'
import type { CompanySearchResult } from '../api/companiesApi'

interface SmartCompanySearchProps {
  onCompanySelected: (company: CompanySearchResult, searchContext?: {searchType: string, query: string}) => void
  onManualEntry: () => void
  autoSelect?: boolean
  className?: string
}

/**
 * Detect search type from query
 */
function detectSearchType(query: string): 'ABN' | 'ACN' | 'Name' | null {
  const normalized = query.replace(/[^\w]/g, '').trim()
  
  if (normalized.length === 0) return null
  
  if (/^\d+$/.test(normalized)) {
    if (normalized.length === 11) return 'ABN'
    if (normalized.length === 9) return 'ACN'
  }
  
  return 'Name'
}

export const SmartCompanySearch = React.memo(function SmartCompanySearch({
  onCompanySelected,
  onManualEntry,
  autoSelect = true,
  className = ''
}: SmartCompanySearchProps) {
  const [searchQuery, setSearchQuery] = useState('')
  const { data, isLoading, error, search } = useCompanySearch(300, 2)
  
  const detectedType = detectSearchType(searchQuery)

  // Auto-select single result (AC-1.19.5)
  useEffect(() => {
    if (autoSelect && data && data.results.length === 1) {
      onCompanySelected(data.results[0], {searchType: data.searchType, query: searchQuery})
    }
  }, [data, autoSelect, onCompanySelected, searchQuery])

  const handleInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setSearchQuery(value)
    search(value)
  }, [search])

  const handleResultSelect = useCallback((result: CompanySearchResult) => {
    onCompanySelected(result, {searchType: data?.searchType || 'Unknown', query: searchQuery})
  }, [onCompanySelected, data, searchQuery])

  return (
    <div className={className}>
      {/* Search Input */}
      <div className="relative">
        <div className="relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={handleInputChange}
            placeholder="Search by ABN, ACN, or company name..."
            className="w-full pl-12 pr-12 py-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent text-base"
          />
          {isLoading && (
            <Loader2 className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-teal-600 animate-spin" />
          )}
        </div>

        {/* Search Type Indicator */}
        {detectedType && searchQuery.length >= 2 && (
          <div className="mt-2 flex items-center gap-2 text-sm text-gray-600">
            <Info className="w-4 h-4" />
            <span>
              Searching by: <span className="font-medium">{detectedType}</span>
              {detectedType === 'ABN' && ' (11 digits)'}
              {detectedType === 'ACN' && ' (9 digits)'}
              {detectedType === 'Name' && ' (company name)'}
            </span>
          </div>
        )}
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="mt-4 text-center py-8">
          <Loader2 className="w-8 h-8 animate-spin text-teal-600 mx-auto mb-2" />
          <p className="text-gray-600">Searching Australian Business Register...</p>
        </div>
      )}

      {/* Error State */}
      {error && !isLoading && (
        <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <p className="text-sm font-medium text-red-800 mb-1">
                {error.error === 'ABR_API_TIMEOUT' && 'Search timeout'}
                {error.error === 'ABR_API_ERROR' && 'Search unavailable'}
                {error.error === 'NETWORK_ERROR' && 'Network error'}
                {!['ABR_API_TIMEOUT', 'ABR_API_ERROR', 'NETWORK_ERROR'].includes(error.error) && 'Search error'}
              </p>
              <p className="text-sm text-red-700 mb-3">{error.message}</p>
              <button
                onClick={onManualEntry}
                className="text-sm font-medium text-red-700 hover:text-red-800 underline"
              >
                Enter company details manually →
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Results */}
      {!isLoading && !error && data && data.results.length > 0 && (
        <div className="mt-4">
          <CompanySearchResults
            results={data.results}
            searchQuery={searchQuery}
            searchType={data.searchType}
            cached={data.cached}
            responseTimeMs={data.responseTimeMs}
            onSelect={handleResultSelect}
          />
        </div>
      )}

      {/* No Results */}
      {!isLoading && !error && data && data.results.length === 0 && (
        <div className="mt-4 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <p className="text-sm font-medium text-yellow-800 mb-1">
                No companies found
              </p>
              <p className="text-sm text-yellow-700 mb-3">
                We couldn't find any companies matching "{searchQuery}". 
                Double-check your ABN/ACN or try searching by company name.
              </p>
              <button
                onClick={onManualEntry}
                className="text-sm font-medium text-yellow-700 hover:text-yellow-800 underline"
              >
                Can't find your company? Enter details manually →
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Manual Entry Link (always visible) */}
      {!error && !data && searchQuery.length < 2 && (
        <div className="mt-4 text-center">
          <button
            onClick={onManualEntry}
            className="text-sm text-gray-600 hover:text-gray-800 underline"
          >
            Can't find your company? Enter details manually
          </button>
        </div>
      )}
    </div>
  )
})

