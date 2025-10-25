/**
 * Company Search Results Component
 * Story 1.19: AC-1.19.4 - Display results in card format
 * 
 * Features:
 * - Card-based layout
 * - Company details (name, ABN, GST, entity type, address)
 * - Highlight search terms
 * - Result count and cache indicator
 */

import React from 'react'
import { Building2, CheckCircle, XCircle, MapPin, Clock } from 'lucide-react'
import type { CompanySearchResult } from '../api/companiesApi'

interface CompanySearchResultsProps {
  results: CompanySearchResult[]
  searchQuery: string
  searchType: 'ABN' | 'ACN' | 'Name'
  cached: boolean
  responseTimeMs: number
  onSelect: (result: CompanySearchResult) => void
}

/**
 * Highlight search terms in text
 */
function highlightText(text: string, query: string): React.ReactNode {
  if (!query || query.length < 2) return text

  const parts = text.split(new RegExp(`(${query})`, 'gi'))
  
  return (
    <>
      {parts.map((part, index) =>
        part.toLowerCase() === query.toLowerCase() ? (
          <mark key={index} className="bg-yellow-200 font-medium">
            {part}
          </mark>
        ) : (
          <span key={index}>{part}</span>
        )
      )}
    </>
  )
}

export function CompanySearchResults({
  results,
  searchQuery,
  searchType,
  cached,
  responseTimeMs,
  onSelect
}: CompanySearchResultsProps) {
  return (
    <div>
      {/* Results Header */}
      <div className="flex items-center justify-between mb-3">
        <p className="text-sm text-gray-600">
          <span className="font-medium text-gray-900">{results.length}</span>{' '}
          {results.length === 1 ? 'company' : 'companies'} found
        </p>
        {cached && responseTimeMs < 100 && (
          <div className="flex items-center gap-1.5 text-xs text-teal-600">
            <Clock className="w-3.5 h-3.5" />
            <span>Instant (cached)</span>
          </div>
        )}
      </div>

      {/* Results List */}
      <div className="space-y-3">
        {results.map((result, index) => (
          <button
            key={`${result.abn}-${index}`}
            onClick={() => onSelect(result)}
            className="w-full text-left bg-white border border-gray-200 rounded-lg p-4 hover:border-teal-500 hover:bg-teal-50 transition-all focus:outline-none focus:ring-2 focus:ring-teal-500"
          >
            {/* Company Name */}
            <div className="flex items-start justify-between gap-3 mb-2">
              <div className="flex items-start gap-3 flex-1 min-w-0">
                <Building2 className="w-5 h-5 text-teal-600 flex-shrink-0 mt-0.5" />
                <div className="flex-1 min-w-0">
                  <h4 className="text-lg font-semibold text-gray-900 mb-1 break-words">
                    {searchType === 'Name' ? (
                      highlightText(result.companyName, searchQuery)
                    ) : (
                      result.companyName
                    )}
                  </h4>

                  {/* Status Badge */}
                  {result.status && (
                    <span
                      className={`inline-block px-2 py-0.5 text-xs font-medium rounded ${
                        result.status.toLowerCase() === 'active'
                          ? 'bg-green-100 text-green-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}
                    >
                      {result.status}
                    </span>
                  )}
                </div>
              </div>
            </div>

            {/* Company Details Grid */}
            <div className="pl-8 space-y-2">
              {/* ABN */}
              {result.abnFormatted && (
                <div className="flex items-center gap-2 text-sm">
                  <span className="text-gray-500 font-medium min-w-[80px]">ABN:</span>
                  <span className="text-gray-900 font-mono">
                    {searchType === 'ABN' ? (
                      highlightText(result.abnFormatted, searchQuery)
                    ) : (
                      result.abnFormatted
                    )}
                  </span>
                </div>
              )}

              {/* GST Registration */}
              {result.gstRegistered !== null && (
                <div className="flex items-center gap-2 text-sm">
                  <span className="text-gray-500 font-medium min-w-[80px]">GST:</span>
                  <div className="flex items-center gap-1.5">
                    {result.gstRegistered ? (
                      <>
                        <CheckCircle className="w-4 h-4 text-green-600" />
                        <span className="text-green-700 font-medium">Registered</span>
                      </>
                    ) : (
                      <>
                        <XCircle className="w-4 h-4 text-gray-400" />
                        <span className="text-gray-600">Not Registered</span>
                      </>
                    )}
                  </div>
                </div>
              )}

              {/* Entity Type */}
              {result.entityType && (
                <div className="flex items-center gap-2 text-sm">
                  <span className="text-gray-500 font-medium min-w-[80px]">Entity Type:</span>
                  <span className="text-gray-700">{result.entityType}</span>
                </div>
              )}

              {/* Business Address */}
              {result.businessAddress && (
                <div className="flex items-start gap-2 text-sm">
                  <MapPin className="w-4 h-4 text-gray-400 flex-shrink-0 mt-0.5" />
                  <span className="text-gray-700">{result.businessAddress}</span>
                </div>
              )}
            </div>

            {/* Select Indicator */}
            <div className="mt-3 pl-8 text-sm text-teal-600 font-medium">
              Click to select →
            </div>
          </button>
        ))}
      </div>

      {/* Single Result Note */}
      {results.length === 1 && (
        <p className="mt-3 text-sm text-gray-500 text-center">
          Single result found - click to auto-fill your company details
        </p>
      )}
    </div>
  )
}

