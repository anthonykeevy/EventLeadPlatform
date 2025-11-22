/**
 * Grant Access Form Component - Story 2.9
 * Form for granting access to a form
 */

import React, { useState, useEffect, useRef } from 'react'
import { User, Building2, Calendar, Search, Loader2, WifiOff, AlertCircle } from 'lucide-react'
import { 
  grantFormAccess, 
  getAccessTypes, 
  getRelationshipTypes, 
  getCompanyMembersForForm,
  getRelatedCompaniesForForm,
  searchUsers, 
  searchCompanies, 
  type UserSearchResult, 
  type CompanySearchResult 
} from '../api/formAccessApi'
import { GrantAccessRequest, FormAccessControlAccessType, CompanyRelationshipType } from '../types/form-access.types'
import { useToastNotifications } from '../../ux'

interface GrantAccessFormProps {
  formId: number
  onSuccess: () => void
  onCancel: () => void
}

export function GrantAccessForm({ formId, onSuccess, onCancel }: GrantAccessFormProps) {
  const [granteeType, setGranteeType] = useState<'user' | 'company' | null>(null)
  const [formData, setFormData] = useState<GrantAccessRequest>({
    userId: null,
    companyId: null,
    formAccessControlAccessTypeId: 0,
    companyRelationshipTypeId: 0,
    expiryDate: null,
  })
  
  const [accessTypes, setAccessTypes] = useState<FormAccessControlAccessType[]>([])
  const [relationshipTypes, setRelationshipTypes] = useState<CompanyRelationshipType[]>([])
  const [companyMembers, setCompanyMembers] = useState<UserSearchResult[]>([])
  const [relatedCompanies, setRelatedCompanies] = useState<CompanySearchResult[]>([])
  
  const [isLoading, setIsLoading] = useState(false)
  const [isLoadingData, setIsLoadingData] = useState(true)
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [networkError, setNetworkError] = useState(false)
  
  // User/Company search state (for filtering dropdowns)
  const [userSearchQuery, setUserSearchQuery] = useState('')
  const [companySearchQuery, setCompanySearchQuery] = useState('')
  const [selectedUser, setSelectedUser] = useState<UserSearchResult | null>(null)
  const [selectedCompany, setSelectedCompany] = useState<CompanySearchResult | null>(null)
  
  const userDropdownRef = useRef<HTMLDivElement>(null)
  const companyDropdownRef = useRef<HTMLDivElement>(null)
  
  const toast = useToastNotifications()

  // Load all reference data and prepopulated lists
  useEffect(() => {
    const loadData = async () => {
      try {
        setIsLoadingData(true)
        console.log('Loading reference data and prepopulated lists...')
        const [accessTypesData, relationshipTypesData, membersData, companiesData] = await Promise.all([
          getAccessTypes(),
          getRelationshipTypes(),
          getCompanyMembersForForm(formId),
          getRelatedCompaniesForForm(formId),
        ])
        console.log('Access types loaded:', accessTypesData)
        console.log('Relationship types loaded:', relationshipTypesData)
        console.log('Company members loaded:', membersData)
        console.log('Related companies loaded:', companiesData)
        
        setAccessTypes(accessTypesData)
        setRelationshipTypes(relationshipTypesData)
        setCompanyMembers(membersData)
        setRelatedCompanies(companiesData)
        
        // Set defaults
        if (accessTypesData.length > 0) {
          setFormData(prev => ({ ...prev, formAccessControlAccessTypeId: accessTypesData[0].formAccessControlAccessTypeId }))
        }
        // Don't set default relationship type - user should choose
      } catch (err) {
        console.error('Error loading data:', err)
        const errorMessage = err instanceof Error ? err.message : 'Failed to load data'
        
        // Check if this is a network error
        const isNetworkError = err instanceof Error && (
          errorMessage.includes('Network Error') ||
          errorMessage.includes('ERR_INTERNET_DISCONNECTED') ||
          errorMessage.includes('Failed to fetch') ||
          errorMessage.includes('network') ||
          (!navigator.onLine)
        )
        
        if (isNetworkError) {
          setNetworkError(true)
          toast.error('Unable to connect to server. Please check your internet connection.', 'Connection Error')
        } else {
          toast.error(errorMessage, 'Error')
        }
        
        setAccessTypes([])
        setRelationshipTypes([])
        setCompanyMembers([])
        setRelatedCompanies([])
      } finally {
        setIsLoadingData(false)
      }
    }
    
    loadData()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [formId]) // Reload when formId changes

  // Close dropdowns when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (userDropdownRef.current && !userDropdownRef.current.contains(event.target as Node)) {
        setUserSearchQuery('')
      }
      if (companyDropdownRef.current && !companyDropdownRef.current.contains(event.target as Node)) {
        setCompanySearchQuery('')
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  // Filter users/companies based on search query
  const filteredUsers = companyMembers.filter(user => {
    if (!userSearchQuery) return true
    const query = userSearchQuery.toLowerCase()
    const fullName = `${user.firstName || ''} ${user.lastName || ''}`.toLowerCase()
    const email = (user.email || '').toLowerCase()
    return fullName.includes(query) || email.includes(query)
  })

  const filteredCompanies = relatedCompanies.filter(company => {
    if (!companySearchQuery) return true
    return company.companyName.toLowerCase().includes(companySearchQuery.toLowerCase())
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setErrors({})

    // Validation
    const newErrors: Record<string, string> = {}
    if (!formData.companyRelationshipTypeId || formData.companyRelationshipTypeId === 0) {
      newErrors.relationshipType = 'Relationship type is required'
    }
    if (granteeType === null || (!formData.userId && !formData.companyId)) {
      newErrors.grantee = 'Either user or company must be selected'
    }
    if (granteeType === 'user' && (!formData.userId || formData.userId === 0)) {
      newErrors.grantee = 'Please select a user'
    }
    if (granteeType === 'company' && (!formData.companyId || formData.companyId === 0)) {
      newErrors.grantee = 'Please select a company'
    }
    if (!formData.formAccessControlAccessTypeId || formData.formAccessControlAccessTypeId === 0) {
      newErrors.accessType = 'Access type is required'
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    setIsLoading(true)
    try {
      // Convert expiry date from local time to UTC if provided
      // datetime-local input returns a string like "2025-11-20T16:15:00" (local time, no timezone)
      // We need to convert it to UTC ISO string before sending to the backend
      const requestData: GrantAccessRequest = {
        ...formData,
        expiryDate: convertLocalDateTimeToUTC(formData.expiryDate)
      }
      
      await grantFormAccess(formId, requestData)
      toast.success('Access granted successfully', 'Success')
      onSuccess()
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to grant access'
      toast.error(errorMessage, 'Error granting access')
      setErrors({ submit: errorMessage })
    } finally {
      setIsLoading(false)
    }
  }

  // Show network error banner if network is unavailable
  if (networkError || (!navigator.onLine && isLoadingData)) {
    return (
      <div className="p-6">
        <div className="bg-red-50 border-l-4 border-red-400 p-4 rounded-md mb-4">
          <div className="flex items-start">
            <AlertCircle className="w-5 h-5 text-red-400 mt-0.5 mr-3 flex-shrink-0" />
            <div className="flex-1">
              <h3 className="text-sm font-medium text-red-800 mb-1">
                Connection Error
              </h3>
              <p className="text-sm text-red-700">
                Unable to connect to the server. Please check your internet connection and try again.
              </p>
              <button
                onClick={() => {
                  setNetworkError(false)
                  setIsLoadingData(true)
                  // Retry loading data
                  const loadData = async () => {
                    try {
                      const [accessTypesData, relationshipTypesData, membersData, companiesData] = await Promise.all([
                        getAccessTypes(),
                        getRelationshipTypes(),
                        getCompanyMembersForForm(formId),
                        getRelatedCompaniesForForm(formId),
                      ])
                      setAccessTypes(accessTypesData)
                      setRelationshipTypes(relationshipTypesData)
                      setCompanyMembers(membersData)
                      setRelatedCompanies(companiesData)
                      setNetworkError(false)
                      if (accessTypesData.length > 0) {
                        setFormData(prev => ({ ...prev, formAccessControlAccessTypeId: accessTypesData[0].formAccessControlAccessTypeId }))
                      }
                    } catch (err) {
                      const errorMessage = err instanceof Error ? err.message : 'Failed to load data'
                      const isNetworkError = err instanceof Error && (
                        errorMessage.includes('Network Error') ||
                        errorMessage.includes('ERR_INTERNET_DISCONNECTED') ||
                        errorMessage.includes('Failed to fetch') ||
                        errorMessage.includes('network') ||
                        (!navigator.onLine)
                      )
                      if (isNetworkError) {
                        setNetworkError(true)
                        toast.error('Unable to connect to server. Please check your internet connection.', 'Connection Error')
                      } else {
                        toast.error(errorMessage, 'Error')
                      }
                    } finally {
                      setIsLoadingData(false)
                    }
                  }
                  loadData()
                }}
                className="mt-3 text-sm font-medium text-red-800 hover:text-red-900 underline"
              >
                Retry Connection
              </button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (isLoadingData) {
    return (
      <div className="p-6">
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-600 mx-auto"></div>
          <p className="mt-2 text-sm text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Relationship Type - FIRST (helps scope who to grant access to) */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Relationship Type <span className="text-red-500">*</span>
        </label>
        <select
          value={formData.companyRelationshipTypeId}
          onChange={(e) => setFormData(prev => ({ ...prev, companyRelationshipTypeId: parseInt(e.target.value) }))}
          disabled={networkError || (!navigator.onLine) || relationshipTypes.length === 0}
          className={`w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500 ${
            networkError || (!navigator.onLine) || relationshipTypes.length === 0
              ? 'border-red-300 bg-red-50 cursor-not-allowed'
              : 'border-gray-300'
          }`}
        >
          <option value={0}>
            {networkError || (!navigator.onLine) 
              ? 'Unavailable - check connection' 
              : relationshipTypes.length === 0 
              ? 'Loading relationship types...' 
              : 'Select relationship type'}
          </option>
          {relationshipTypes.map((rt) => (
            <option key={rt.companyRelationshipTypeId} value={rt.companyRelationshipTypeId}>
              {rt.typeName}{rt.typeDescription ? ` - ${rt.typeDescription}` : ''}
            </option>
          ))}
        </select>
        {(networkError || (!navigator.onLine)) && relationshipTypes.length === 0 && (
          <p className="mt-1 text-sm text-red-600 flex items-center gap-1">
            <WifiOff className="w-4 h-4" />
            Unable to load relationship types - please check your connection
          </p>
        )}
        {errors.relationshipType && (
          <p className="mt-1 text-sm text-red-600">{errors.relationshipType}</p>
        )}
        <p className="mt-1 text-xs text-gray-500">
          Select the relationship type to help determine who can be granted access
        </p>
      </div>

      {/* User/Company Selection */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Grant Access To <span className="text-red-500">*</span>
        </label>
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <input
              type="radio"
              id="grant-user"
              name="grantee-type"
              checked={granteeType === 'user'}
              onChange={() => {
                setGranteeType('user')
                setFormData(prev => ({ ...prev, userId: null, companyId: null }))
                setSelectedUser(null)
                setSelectedCompany(null)
                setUserSearchQuery('')
                setCompanySearchQuery('')
              }}
              className="w-4 h-4 text-teal-600 focus:ring-teal-500"
            />
            <label htmlFor="grant-user" className="flex items-center gap-2 cursor-pointer">
              <User className="w-4 h-4 text-gray-500" />
              <span>User</span>
            </label>
          </div>
          {granteeType === 'user' && (
            <div className="ml-6 relative" ref={userDropdownRef}>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search or select from dropdown..."
                  value={selectedUser ? `${selectedUser.firstName || ''} ${selectedUser.lastName || ''} (${selectedUser.email})`.trim() : userSearchQuery}
                  onChange={(e) => {
                    setUserSearchQuery(e.target.value)
                    setSelectedUser(null)
                    setFormData(prev => ({ ...prev, userId: null, companyId: null }))
                  }}
                  onFocus={() => setUserSearchQuery('')}
                  className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                />
              </div>
              {(userSearchQuery || !selectedUser) && (
                <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto">
                  {filteredUsers.length > 0 ? (
                    filteredUsers.map((user) => (
                      <div
                        key={user.userId}
                        onClick={() => {
                          setSelectedUser(user)
                          setUserSearchQuery('')
                          setFormData(prev => ({ ...prev, userId: user.userId, companyId: null }))
                        }}
                        className="px-4 py-2 hover:bg-teal-50 cursor-pointer border-b border-gray-100 last:border-b-0"
                      >
                        <div className="font-medium">{user.firstName} {user.lastName}</div>
                        <div className="text-sm text-gray-500">{user.email}</div>
                      </div>
                    ))
                  ) : (
                    <div className="px-4 py-2 text-center text-gray-500">
                      {networkError || (!navigator.onLine) ? (
                        <div className="flex items-center justify-center gap-2 text-red-600">
                          <WifiOff className="w-4 h-4" />
                          <span>Unable to load users - check connection</span>
                        </div>
                      ) : companyMembers.length === 0 ? (
                        'No company members available'
                      ) : (
                        'No users found'
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
          
          <div className="flex items-center gap-2">
            <input
              type="radio"
              id="grant-company"
              name="grantee-type"
              checked={granteeType === 'company'}
              onChange={() => {
                setGranteeType('company')
                setFormData(prev => ({ ...prev, userId: null, companyId: null }))
                setSelectedUser(null)
                setSelectedCompany(null)
                setUserSearchQuery('')
                setCompanySearchQuery('')
              }}
              className="w-4 h-4 text-teal-600 focus:ring-teal-500"
            />
            <label htmlFor="grant-company" className="flex items-center gap-2 cursor-pointer">
              <Building2 className="w-4 h-4 text-gray-500" />
              <span>Company</span>
            </label>
          </div>
          {granteeType === 'company' && (
            <div className="ml-6 relative" ref={companyDropdownRef}>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search or select from dropdown..."
                  value={selectedCompany ? selectedCompany.companyName : companySearchQuery}
                  onChange={(e) => {
                    setCompanySearchQuery(e.target.value)
                    setSelectedCompany(null)
                    setFormData(prev => ({ ...prev, companyId: null, userId: null }))
                  }}
                  onFocus={() => setCompanySearchQuery('')}
                  className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                />
              </div>
              {(companySearchQuery || !selectedCompany) && (
                <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto">
                  {filteredCompanies.length > 0 ? (
                    filteredCompanies.map((company) => (
                      <div
                        key={company.companyId}
                        onClick={() => {
                          setSelectedCompany(company)
                          setCompanySearchQuery('')
                          setFormData(prev => ({ ...prev, companyId: company.companyId, userId: null }))
                        }}
                        className="px-4 py-2 hover:bg-teal-50 cursor-pointer border-b border-gray-100 last:border-b-0"
                      >
                        <div className="font-medium">{company.companyName}</div>
                      </div>
                    ))
                  ) : (
                    <div className="px-4 py-2 text-center text-gray-500">
                      {networkError || (!navigator.onLine) ? (
                        <div className="flex items-center justify-center gap-2 text-red-600">
                          <WifiOff className="w-4 h-4" />
                          <span>Unable to load companies - check connection</span>
                        </div>
                      ) : relatedCompanies.length === 0 ? (
                        'No related companies available'
                      ) : (
                        'No companies found'
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
        {errors.grantee && (
          <p className="mt-1 text-sm text-red-600">{errors.grantee}</p>
        )}
      </div>

      {/* Access Type */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Access Type <span className="text-red-500">*</span>
        </label>
        <select
          value={formData.formAccessControlAccessTypeId}
          onChange={(e) => setFormData(prev => ({ ...prev, formAccessControlAccessTypeId: parseInt(e.target.value) }))}
          disabled={networkError || (!navigator.onLine) || accessTypes.length === 0}
          className={`w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500 ${
            networkError || (!navigator.onLine) || accessTypes.length === 0
              ? 'border-red-300 bg-red-50 cursor-not-allowed'
              : 'border-gray-300'
          }`}
        >
          <option value={0}>
            {networkError || (!navigator.onLine) 
              ? 'Unavailable - check connection' 
              : accessTypes.length === 0 
              ? 'Loading access types...' 
              : 'Select access type'}
          </option>
          {accessTypes.map((at) => (
            <option key={at.formAccessControlAccessTypeId} value={at.formAccessControlAccessTypeId}>
              {at.accessTypeName}{at.accessTypeDescription ? ` - ${at.accessTypeDescription}` : ''}
            </option>
          ))}
        </select>
        {(networkError || (!navigator.onLine)) && accessTypes.length === 0 && (
          <p className="mt-1 text-sm text-red-600 flex items-center gap-1">
            <WifiOff className="w-4 h-4" />
            Unable to load access types - please check your connection
          </p>
        )}
        {errors.accessType && (
          <p className="mt-1 text-sm text-red-600">{errors.accessType}</p>
        )}
      </div>

      {/* Expiry Date (Optional) */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center gap-2">
          <Calendar className="w-4 h-4 text-gray-500" />
          Expiry Date (Optional)
        </label>
        <input
          type="datetime-local"
          value={formData.expiryDate || ''}
          onChange={(e) => setFormData(prev => ({ ...prev, expiryDate: e.target.value || null }))}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
        />
        <p className="mt-1 text-xs text-gray-500">Leave empty for permanent access</p>
      </div>

      {errors.submit && (
        <div className="p-3 bg-red-50 border border-red-200 rounded-md">
          <p className="text-sm text-red-600">{errors.submit}</p>
        </div>
      )}

      {/* Actions */}
      <div className="flex justify-end gap-3 pt-4 border-t border-gray-200">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={isLoading}
          className="px-4 py-2 text-sm font-medium text-white bg-teal-600 rounded-md hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Granting...' : 'Grant Access'}
        </button>
      </div>
    </form>
  )
}

// Helper function to convert local datetime to UTC ISO string
// datetime-local input returns a string like "2025-11-20T16:15:00" (local time, no timezone)
// This function converts it to UTC before sending to the backend
function convertLocalDateTimeToUTC(localDateTimeString: string | null): string | undefined {
  if (!localDateTimeString) {
    return undefined
  }
  
  // Parse the local datetime string (browser interprets it as local time)
  const localDate = new Date(localDateTimeString)
  
  // Check if the date is valid
  if (isNaN(localDate.getTime())) {
    return undefined
  }
  
  // Convert to UTC ISO string (e.g., "2025-11-20T06:15:00.000Z")
  return localDate.toISOString()
}
