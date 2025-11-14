/**
 * Industry Search Component
 * Search and filter functionality for finding industries
 */

import React, { useState, useEffect, useRef } from 'react'
import { X, Search, Star } from 'lucide-react'
import type { IndustryOption } from '../../profile/api/usersApi'
import { useToastNotifications } from '../../ux'

interface IndustrySearchProps {
  availableIndustries: IndustryOption[]
  onSelect: (industryId: number, isPrimary: boolean) => void
  onClose: () => void
  isProcessing?: boolean
  hasPrimaryIndustry?: boolean // Whether user already has a primary industry
}

export function IndustrySearch({
  availableIndustries,
  onSelect,
  onClose,
  isProcessing = false,
  hasPrimaryIndustry = false
}: IndustrySearchProps) {
  const [searchQuery, setSearchQuery] = useState('')
  const [debouncedQuery, setDebouncedQuery] = useState('')
  const [filteredIndustries, setFilteredIndustries] = useState<IndustryOption[]>([])
  const [selectedIndex, setSelectedIndex] = useState(-1)
  const [addAsPrimary, setAddAsPrimary] = useState(!hasPrimaryIndustry) // Default to primary if no primary exists
  const searchInputRef = useRef<HTMLInputElement>(null)
  const resultsRef = useRef<HTMLDivElement>(null)

  // Debounce search query
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedQuery(searchQuery)
    }, 300)

    return () => clearTimeout(timer)
  }, [searchQuery])

  // Filter industries based on search query
  useEffect(() => {
    if (!debouncedQuery.trim()) {
      setFilteredIndustries(availableIndustries.slice(0, 10)) // Show first 10 by default
    } else {
      const query = debouncedQuery.toLowerCase()
      const filtered = availableIndustries.filter(
        industry =>
          industry.name.toLowerCase().includes(query) ||
          industry.code.toLowerCase().includes(query) ||
          industry.description.toLowerCase().includes(query)
      )
      setFilteredIndustries(filtered.slice(0, 20)) // Limit to 20 results
    }
    setSelectedIndex(-1)
  }, [debouncedQuery, availableIndustries])

  // Focus search input on mount
  useEffect(() => {
    searchInputRef.current?.focus()
  }, [])

  // Handle keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'ArrowDown') {
        e.preventDefault()
        setSelectedIndex(prev =>
          prev < filteredIndustries.length - 1 ? prev + 1 : prev
        )
      } else if (e.key === 'ArrowUp') {
        e.preventDefault()
        setSelectedIndex(prev => (prev > 0 ? prev - 1 : -1))
      } else if (e.key === 'Enter' && selectedIndex >= 0) {
        e.preventDefault()
        const industry = filteredIndustries[selectedIndex]
        if (industry) {
          handleAddIndustry(industry.id, false)
        }
      } else if (e.key === 'Escape') {
        onClose()
      }
    }

    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [selectedIndex, filteredIndustries, onClose])

  // Scroll selected item into view
  useEffect(() => {
    if (selectedIndex >= 0 && resultsRef.current) {
      const selectedElement = resultsRef.current.children[selectedIndex] as HTMLElement
      if (selectedElement) {
        selectedElement.scrollIntoView({ block: 'nearest', behavior: 'smooth' })
      }
    }
  }, [selectedIndex])

  const handleAddIndustry = (industryId: number, isPrimary: boolean) => {
    if (isProcessing) return
    onSelect(industryId, isPrimary)
  }

  const handleIndustryClick = (industryId: number) => {
    handleAddIndustry(industryId, addAsPrimary)
  }

  const handlePrimaryClick = (e: React.MouseEvent, industryId: number) => {
    e.stopPropagation()
    handleAddIndustry(industryId, true)
  }

  if (availableIndustries.length === 0) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Add Industry</h3>
            <button
              onClick={onClose}
              className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
              aria-label="Close"
            >
              <X className="w-5 h-5 text-gray-500 dark:text-gray-400" />
            </button>
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            No industries available. Please contact support.
          </p>
          <button
            onClick={onClose}
            className="mt-4 w-full px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-lg w-full max-h-[80vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Add Industry</h3>
          <button
            onClick={onClose}
            className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
            aria-label="Close"
          >
            <X className="w-5 h-5 text-gray-500 dark:text-gray-400" />
          </button>
        </div>

        {/* Search Input */}
        <div className="p-4 border-b border-gray-200 dark:border-gray-700 space-y-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              ref={searchInputRef}
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search industries..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-teal-500 dark:bg-gray-700 dark:text-white"
            />
          </div>
          {searchQuery && (
            <p className="text-xs text-gray-500 dark:text-gray-400">
              {filteredIndustries.length} result{filteredIndustries.length !== 1 ? 's' : ''}
            </p>
          )}
          {/* Primary/Secondary Toggle */}
          {hasPrimaryIndustry && (
            <div className="flex items-center gap-3 p-2 bg-teal-50 dark:bg-teal-900/20 rounded-lg border border-teal-200 dark:border-teal-800">
              <input
                type="checkbox"
                id="addAsPrimary"
                checked={addAsPrimary}
                onChange={(e) => setAddAsPrimary(e.target.checked)}
                className="w-4 h-4 text-teal-600 border-gray-300 rounded focus:ring-teal-500"
              />
              <label htmlFor="addAsPrimary" className="text-sm text-gray-700 dark:text-gray-300 cursor-pointer">
                <span className="font-medium">Add as Primary Industry</span>
                <span className="block text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                  This will replace your current primary industry
                </span>
              </label>
            </div>
          )}
          {!hasPrimaryIndustry && (
            <div className="flex items-center gap-2 p-2 bg-teal-50 dark:bg-teal-900/20 rounded-lg border border-teal-200 dark:border-teal-800">
              <Star className="w-4 h-4 text-teal-600 dark:text-teal-400 fill-current" />
              <p className="text-xs text-teal-800 dark:text-teal-200">
                This will be your <strong>Primary Industry</strong>
              </p>
            </div>
          )}
        </div>

        {/* Results */}
        <div
          ref={resultsRef}
          className="overflow-y-auto max-h-[50vh] p-2"
        >
          {filteredIndustries.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {searchQuery ? 'No industries found matching your search' : 'No industries available'}
              </p>
            </div>
          ) : (
            <div className="space-y-1">
              {filteredIndustries.map((industry, index) => (
                <div
                  key={industry.id}
                  onClick={() => handleIndustryClick(industry.id)}
                  className={`
                    p-3 rounded-lg border-2 cursor-pointer transition-all
                    ${selectedIndex === index
                      ? 'border-teal-500 bg-teal-50 dark:bg-teal-900/20'
                      : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
                    }
                    ${isProcessing ? 'opacity-50 cursor-not-allowed' : ''}
                  `}
                  role="button"
                  tabIndex={0}
                  aria-label={`Select ${industry.name}`}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="font-medium text-sm text-gray-900 dark:text-gray-100">
                        {industry.name}
                      </div>
                      {industry.description && (
                        <div className="text-xs text-gray-600 dark:text-gray-400 mt-1 line-clamp-2">
                          {industry.description}
                        </div>
                      )}
                    </div>
                    <div className="flex items-center gap-1 ml-2">
                      <button
                        onClick={(e) => handlePrimaryClick(e, industry.id)}
                        disabled={isProcessing}
                        className="p-1 text-teal-600 dark:text-teal-400 hover:bg-teal-50 dark:hover:bg-teal-900/20 rounded transition-colors disabled:opacity-50"
                        title="Add as Primary"
                        aria-label="Add as primary industry"
                      >
                        <Star className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800">
          <div className="flex items-center justify-between text-xs text-gray-600 dark:text-gray-400">
            <span>Press Enter to add, or click an industry</span>
            <button
              onClick={onClose}
              className="px-3 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

