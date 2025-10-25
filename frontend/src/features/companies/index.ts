/**
 * Companies Feature Exports
 * Story 1.19: ABR Smart Search Integration
 */

export { SmartCompanySearch } from './components/SmartCompanySearch'
export { CompanySearchResults } from './components/CompanySearchResults'
export { useCompanySearch } from './hooks/useCompanySearch'
export { searchCompanies, parseBusinessAddress, enrichCompanyByABN } from './api/companiesApi'
export type { CompanySearchResult, CompanySearchResponse, CompanySearchError } from './api/companiesApi'

