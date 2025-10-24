/**
 * Validation Feature - Story 1.20
 * Country-specific validation components and hooks
 */

// Hooks
export { useValidation } from './hooks/useValidation'
export type { ValidationResult, UseValidationReturn } from './hooks/useValidation'
export { useCountries } from './hooks/useCountries'
export type { Country, UseCountriesReturn } from './hooks/useCountries'

// Components
export { PhoneInput } from './components/PhoneInput'
export { PostalCodeInput } from './components/PostalCodeInput'
export { CountrySelector } from './components/CountrySelector'

// Utils
export { getCountryConfig, getStateOptions, COUNTRY_CONFIGS, STATE_OPTIONS } from './utils/countryConfig'
export type { CountryConfig } from './utils/countryConfig'

