/**
 * Company Details API - Story 5.7
 * Company Settings → Company Details + Billing
 */

import { apiClient } from '../../../lib/apiClient'

export interface CompanySettingsDetails {
  companyId: number
  displayName: string
  legalEntityName?: string | null
  companyName: string
  customDisplayName?: string | null
  displayNameSource: string
  abn?: string | null
  acn?: string | null
  abnStatus?: string | null
  entityType?: string | null
  gstRegistered?: boolean | null
  phone?: string | null
  email?: string | null
  website?: string | null
  countryId: number
  industryId?: number | null
  billingContactName?: string | null
  billingEmail?: string | null
  billingPhone?: string | null
  billingAddressLine1?: string | null
  billingAddressLine2?: string | null
  billingCity?: string | null
  billingState?: string | null
  billingPostalCode?: string | null
  billingCountryId?: number | null
}

export interface UpdateCompanySettingsDetails {
  displayName?: string
  legalEntityName?: string
  companyName?: string
  customDisplayName?: string
  displayNameSource?: string
  abn?: string
  acn?: string
  abnStatus?: string
  entityType?: string
  gstRegistered?: boolean
  phone?: string
  email?: string
  website?: string
  countryId?: number
  billingContactName?: string
  billingEmail?: string
  billingPhone?: string
  billingAddressLine1?: string
  billingAddressLine2?: string
  billingCity?: string
  billingState?: string
  billingPostalCode?: string
  billingCountryId?: number
}

function fromBackend(d: Record<string, unknown>): CompanySettingsDetails {
  return {
    companyId: d.company_id as number,
    displayName: (d.display_name as string) ?? '',
    legalEntityName: d.legal_entity_name as string | null,
    companyName: (d.company_name as string) ?? '',
    customDisplayName: d.custom_display_name as string | null,
    displayNameSource: (d.display_name_source as string) ?? 'User',
    abn: d.abn as string | null,
    acn: d.acn as string | null,
    abnStatus: d.abn_status as string | null,
    entityType: d.entity_type as string | null,
    gstRegistered: d.gst_registered as boolean | null,
    phone: d.phone as string | null,
    email: d.email as string | null,
    website: d.website as string | null,
    countryId: d.country_id as number,
    industryId: d.industry_id as number | null,
    billingContactName: d.billing_contact_name as string | null,
    billingEmail: d.billing_email as string | null,
    billingPhone: d.billing_phone as string | null,
    billingAddressLine1: d.billing_address_line1 as string | null,
    billingAddressLine2: d.billing_address_line2 as string | null,
    billingCity: d.billing_city as string | null,
    billingState: d.billing_state as string | null,
    billingPostalCode: d.billing_postal_code as string | null,
    billingCountryId: d.billing_country_id as number | null,
  }
}

export async function getCompanySettingsDetails(
  companyId: number
): Promise<CompanySettingsDetails> {
  const response = await apiClient.get(`/api/companies/${companyId}/details`)
  return fromBackend(response.data)
}

export async function putCompanySettingsDetails(
  companyId: number,
  update: UpdateCompanySettingsDetails
): Promise<CompanySettingsDetails> {
  const payload: Record<string, unknown> = {}
  if (update.displayName !== undefined) payload.display_name = update.displayName
  if (update.legalEntityName !== undefined) payload.legal_entity_name = update.legalEntityName
  if (update.companyName !== undefined) payload.company_name = update.companyName
  if (update.customDisplayName !== undefined) payload.custom_display_name = update.customDisplayName
  if (update.displayNameSource !== undefined) payload.display_name_source = update.displayNameSource
  if (update.abn !== undefined) payload.abn = update.abn
  if (update.acn !== undefined) payload.acn = update.acn
  if (update.abnStatus !== undefined) payload.abn_status = update.abnStatus
  if (update.entityType !== undefined) payload.entity_type = update.entityType
  if (update.gstRegistered !== undefined) payload.gst_registered = update.gstRegistered
  if (update.phone !== undefined) payload.phone = update.phone
  if (update.email !== undefined) payload.email = update.email
  if (update.website !== undefined) payload.website = update.website
  if (update.countryId !== undefined) payload.country_id = update.countryId
  if (update.billingContactName !== undefined) payload.billing_contact_name = update.billingContactName
  if (update.billingEmail !== undefined) payload.billing_email = update.billingEmail
  if (update.billingPhone !== undefined) payload.billing_phone = update.billingPhone
  if (update.billingAddressLine1 !== undefined) payload.billing_address_line1 = update.billingAddressLine1
  if (update.billingAddressLine2 !== undefined) payload.billing_address_line2 = update.billingAddressLine2
  if (update.billingCity !== undefined) payload.billing_city = update.billingCity
  if (update.billingState !== undefined) payload.billing_state = update.billingState
  if (update.billingPostalCode !== undefined) payload.billing_postal_code = update.billingPostalCode
  if (update.billingCountryId !== undefined) payload.billing_country_id = update.billingCountryId
  const response = await apiClient.put(`/api/companies/${companyId}/details`, payload)
  return fromBackend(response.data)
}
