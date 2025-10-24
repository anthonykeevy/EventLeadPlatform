/**
 * Country Configuration - Story 1.20
 * Country-specific labels and validation rules
 */

export interface CountryConfig {
  id: number
  code: string
  name: string
  phonePrefix: string
  taxIdLabel: string
  taxIdExample: string
  taxIdRequired: boolean
  postcodeLabel: string
  postcodeExample: string
  stateLabel: string
  hasCompanySearch: boolean
  companySearchLabel?: string
  taxLabel: string
  taxRate: number | null
}

export const COUNTRY_CONFIGS: Record<number, CountryConfig> = {
  1: {  // Australia
    id: 1,
    code: 'AU',
    name: 'Australia',
    phonePrefix: '+61',
    taxIdLabel: 'ABN (Australian Business Number)',
    taxIdExample: '53004085616',
    taxIdRequired: true,
    postcodeLabel: 'Postcode',
    postcodeExample: '2000',
    stateLabel: 'State',
    hasCompanySearch: true,
    companySearchLabel: 'Search ABN/ACN',
    taxLabel: 'GST',
    taxRate: 0.10
  },
  14: {  // New Zealand (CountryID from database)
    id: 14,
    code: 'NZ',
    name: 'New Zealand',
    phonePrefix: '+64',
    taxIdLabel: 'NZBN (NZ Business Number)',
    taxIdExample: '9429031595513',
    taxIdRequired: false,
    postcodeLabel: 'Postcode',
    postcodeExample: '1010',
    stateLabel: 'Region',
    hasCompanySearch: false,
    taxLabel: 'GST',
    taxRate: 0.15
  },
  15: {  // USA (CountryID from database)
    id: 15,
    code: 'US',
    name: 'United States',
    phonePrefix: '+1',
    taxIdLabel: 'EIN (Employer ID Number)',
    taxIdExample: '12-3456789',
    taxIdRequired: false,
    postcodeLabel: 'ZIP Code',
    postcodeExample: '94102',
    stateLabel: 'State',
    hasCompanySearch: false,
    taxLabel: 'Sales Tax',
    taxRate: null  // Varies by state
  },
  16: {  // UK (CountryID from database)
    id: 16,
    code: 'GB',
    name: 'United Kingdom',
    phonePrefix: '+44',
    taxIdLabel: 'VAT Number',
    taxIdExample: 'GB123456789',
    taxIdRequired: false,
    postcodeLabel: 'Postcode',
    postcodeExample: 'SW1A 1AA',
    stateLabel: 'County',
    hasCompanySearch: true,
    companySearchLabel: 'Search Companies House',
    taxLabel: 'VAT',
    taxRate: 0.20
  },
  17: {  // Canada (CountryID from database)
    id: 17,
    code: 'CA',
    name: 'Canada',
    phonePrefix: '+1',
    taxIdLabel: 'BN (Business Number)',
    taxIdExample: '123456789RC0001',
    taxIdRequired: false,
    postcodeLabel: 'Postal Code',
    postcodeExample: 'M5H 2N2',
    stateLabel: 'Province',
    hasCompanySearch: false,
    taxLabel: 'GST',
    taxRate: 0.05
  }
}

export function getCountryConfig(countryId: number): CountryConfig {
  return COUNTRY_CONFIGS[countryId] || COUNTRY_CONFIGS[1]  // Default to Australia
}

// State/Province/County options per country (using actual database CountryIDs)
export const STATE_OPTIONS: Record<number, Array<{value: string, label: string}>> = {
  1: [  // Australia
    { value: 'NSW', label: 'NSW' },
    { value: 'VIC', label: 'VIC' },
    { value: 'QLD', label: 'QLD' },
    { value: 'SA', label: 'SA' },
    { value: 'WA', label: 'WA' },
    { value: 'TAS', label: 'TAS' },
    { value: 'NT', label: 'NT' },
    { value: 'ACT', label: 'ACT' }
  ],
  14: [  // New Zealand
    { value: 'AUK', label: 'Auckland' },
    { value: 'WGN', label: 'Wellington' },
    { value: 'CAN', label: 'Canterbury' },
    { value: 'OTA', label: 'Otago' },
    { value: 'WAI', label: 'Waikato' },
    { value: 'BOP', label: 'Bay of Plenty' }
  ],
  15: [  // USA
    { value: 'CA', label: 'California' },
    { value: 'NY', label: 'New York' },
    { value: 'TX', label: 'Texas' },
    { value: 'FL', label: 'Florida' },
    { value: 'IL', label: 'Illinois' },
    { value: 'Other', label: 'Other...' }
  ],
  16: [  // UK
    { value: '', label: 'Not specified' },
    { value: 'Greater London', label: 'Greater London' },
    { value: 'Greater Manchester', label: 'Greater Manchester' },
    { value: 'West Midlands', label: 'West Midlands' },
    { value: 'Other', label: 'Other...' }
  ],
  17: [  // Canada
    { value: 'ON', label: 'Ontario' },
    { value: 'QC', label: 'Quebec' },
    { value: 'BC', label: 'British Columbia' },
    { value: 'AB', label: 'Alberta' },
    { value: 'MB', label: 'Manitoba' },
    { value: 'SK', label: 'Saskatchewan' }
  ]
}

export function getStateOptions(countryId: number) {
  return STATE_OPTIONS[countryId] || STATE_OPTIONS[1]
}

