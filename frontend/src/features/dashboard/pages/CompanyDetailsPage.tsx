/**
 * Company Details Page - Story 5.7
 * Company Settings → Company Details
 * Display name, legal name, ABN, billing; ABR popup (AU); Enter manually
 */

import { useState, useEffect, useCallback } from 'react'
import { useParams } from 'react-router-dom'
import { Save } from 'lucide-react'
import {
  getCompanySettingsDetails,
  putCompanySettingsDetails,
  type CompanySettingsDetails,
  type UpdateCompanySettingsDetails,
} from '../api/companyDetailsApi'
import { useToastNotifications } from '../../ux'
import { SmartCompanySearch, parseBusinessAddress, enrichCompanyByABN, type CompanySearchResult } from '../../companies'
import { getCountryConfig } from '../../validation/utils/countryConfig'

export function CompanyDetailsPage() {
  const { companyId } = useParams<{ companyId: string }>()
  const toast = useToastNotifications()
  const id = companyId ? parseInt(companyId, 10) : NaN
  const [details, setDetails] = useState<CompanySettingsDetails | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [showAbrModal, setShowAbrModal] = useState(false)
  const [isDirty, setIsDirty] = useState(false)

  const countryConfig = getCountryConfig(details?.countryId ?? 1)
  const showAbrButton = countryConfig.hasCompanySearch && countryConfig.code === 'AU'

  const loadDetails = useCallback(async () => {
    if (isNaN(id)) return
    setIsLoading(true)
    try {
      const d = await getCompanySettingsDetails(id)
      setDetails(d)
    } catch (err) {
      toast.error('Failed to load company details', 'Error')
      setDetails(null)
    } finally {
      setIsLoading(false)
    }
  }, [id, toast])

  useEffect(() => {
    loadDetails()
  }, [loadDetails])

  const applyAbrResult = useCallback(
    async (company: CompanySearchResult, searchContext?: { searchType: string; query: string }) => {
      if (!details) return
      let enriched = company
      if (searchContext?.searchType === 'Name' && company.abn) {
        const full = await enrichCompanyByABN(company.abn)
        if (full) enriched = full
      }
      const addressParts = parseBusinessAddress(enriched.businessAddress)
      setDetails((prev) => {
        if (!prev) return prev
        return {
          ...prev,
          legalEntityName: enriched.companyName ?? prev.legalEntityName,
          companyName: enriched.companyName ?? prev.companyName,
          abn: enriched.abn ?? prev.abn,
          acn: enriched.acn ?? prev.acn,
          billingAddressLine1: addressParts.street || prev.billingAddressLine1,
          billingCity: addressParts.suburb || prev.billingCity,
          billingState: addressParts.state || prev.billingState,
          billingPostalCode: addressParts.postcode || prev.billingPostalCode,
        }
      })
      setShowAbrModal(false)
      toast.success('Company details filled from ABR', 'Success')
    },
    [details, toast]
  )

  const handleSave = async () => {
    if (isNaN(id) || !details) return
    setIsSaving(true)
    try {
      const update: UpdateCompanySettingsDetails = {
        displayName: details.customDisplayName ?? details.displayName,
        customDisplayName: details.customDisplayName ?? details.displayName,
        legalEntityName: details.legalEntityName,
        companyName: details.companyName,
        abn: details.abn ?? undefined,
        acn: details.acn ?? undefined,
        phone: details.phone ?? undefined,
        email: details.email ?? undefined,
        website: details.website ?? undefined,
        countryId: details.countryId,
        billingContactName: details.billingContactName ?? undefined,
        billingEmail: details.billingEmail ?? undefined,
        billingPhone: details.billingPhone ?? undefined,
        billingAddressLine1: details.billingAddressLine1 ?? undefined,
        billingAddressLine2: details.billingAddressLine2 ?? undefined,
        billingCity: details.billingCity ?? undefined,
        billingState: details.billingState ?? undefined,
        billingPostalCode: details.billingPostalCode ?? undefined,
        billingCountryId: details.billingCountryId ?? undefined,
      }
      await putCompanySettingsDetails(id, update)
      toast.success('Company details saved', 'Success')
      setIsDirty(false)
      loadDetails()
    } catch (err) {
      toast.error('Failed to save company details', 'Error')
    } finally {
      setIsSaving(false)
    }
  }

  const updateField = (key: keyof CompanySettingsDetails, value: string | number | null | undefined) => {
    setDetails((prev) => (prev ? { ...prev, [key]: value } : prev))
    setIsDirty(true)
  }

  useEffect(() => {
    const handleBeforeUnload = (e: BeforeUnloadEvent) => {
      if (isDirty) e.preventDefault()
    }
    window.addEventListener('beforeunload', handleBeforeUnload)
    return () => window.removeEventListener('beforeunload', handleBeforeUnload)
  }, [isDirty])

  if (isNaN(id)) {
    return <div className="p-8 text-red-600">Invalid company ID</div>
  }

  if (isLoading) {
    return <div className="p-8 text-gray-500">Loading...</div>
  }

  if (!details) {
    return <div className="p-8 text-red-600">Failed to load company details</div>
  }

  return (
    <div className="h-full flex flex-col overflow-hidden">
      <div className="flex-shrink-0 px-4 py-3 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Company Details</h2>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
          Manage company name, ABN, and billing address for invoicing.
        </p>
      </div>

      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {/* ABR Search (AU only) */}
        {showAbrButton && (
          <div className="rounded-lg border border-teal-200 dark:border-teal-800 bg-teal-50 dark:bg-teal-900/20 p-4">
            <button
              type="button"
              onClick={() => setShowAbrModal(true)}
              className="px-4 py-2 bg-teal-600 text-white rounded-md hover:bg-teal-700 text-sm font-medium"
            >
              Search Australian Business Register
            </button>
            <button
              type="button"
              onClick={() => setShowAbrModal(false)}
              className="ml-3 text-sm text-teal-700 dark:text-teal-300 hover:underline"
            >
              Enter manually
            </button>
          </div>
        )}

        {/* Company info section */}
        <div className="space-y-4">
          <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300">Company information</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <label className="block">
              <span className="text-sm text-gray-600 dark:text-gray-400">Display name (platform-wide)</span>
              <input
                type="text"
                value={details.customDisplayName ?? details.displayName ?? ''}
                onChange={(e) => updateField('customDisplayName', e.target.value)}
                className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-3 py-2 text-sm"
              />
            </label>
            <label className="block">
              <span className="text-sm text-gray-600 dark:text-gray-400">Legal entity name</span>
              <input
                type="text"
                value={details.legalEntityName ?? ''}
                onChange={(e) => updateField('legalEntityName', e.target.value)}
                className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-3 py-2 text-sm"
              />
            </label>
            <label className="block">
              <span className="text-sm text-gray-600 dark:text-gray-400">ABN (11 digits)</span>
              <input
                type="text"
                value={details.abn ?? ''}
                onChange={(e) => updateField('abn', e.target.value.replace(/\D/g, '').slice(0, 11))}
                className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-3 py-2 text-sm"
                maxLength={11}
              />
            </label>
            <label className="block">
              <span className="text-sm text-gray-600 dark:text-gray-400">Phone</span>
              <input
                type="text"
                value={details.phone ?? ''}
                onChange={(e) => updateField('phone', e.target.value)}
                className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-3 py-2 text-sm"
              />
            </label>
            <label className="block md:col-span-2">
              <span className="text-sm text-gray-600 dark:text-gray-400">Email</span>
              <input
                type="email"
                value={details.email ?? ''}
                onChange={(e) => updateField('email', e.target.value)}
                className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-3 py-2 text-sm"
              />
            </label>
          </div>
        </div>

        {/* Billing section */}
        <div className="space-y-4">
          <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300">Billing address</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <label className="block md:col-span-2">
              <span className="text-sm text-gray-600 dark:text-gray-400">Billing contact name</span>
              <input
                type="text"
                value={details.billingContactName ?? ''}
                onChange={(e) => updateField('billingContactName', e.target.value)}
                className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-3 py-2 text-sm"
              />
            </label>
            <label className="block md:col-span-2">
              <span className="text-sm text-gray-600 dark:text-gray-400">Address line 1</span>
              <input
                type="text"
                value={details.billingAddressLine1 ?? ''}
                onChange={(e) => updateField('billingAddressLine1', e.target.value)}
                className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-3 py-2 text-sm"
              />
            </label>
            <label className="block">
              <span className="text-sm text-gray-600 dark:text-gray-400">City</span>
              <input
                type="text"
                value={details.billingCity ?? ''}
                onChange={(e) => updateField('billingCity', e.target.value)}
                className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-3 py-2 text-sm"
              />
            </label>
            <label className="block">
              <span className="text-sm text-gray-600 dark:text-gray-400">State</span>
              <input
                type="text"
                value={details.billingState ?? ''}
                onChange={(e) => updateField('billingState', e.target.value)}
                className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-3 py-2 text-sm"
              />
            </label>
            <label className="block">
              <span className="text-sm text-gray-600 dark:text-gray-400">Postcode</span>
              <input
                type="text"
                value={details.billingPostalCode ?? ''}
                onChange={(e) => updateField('billingPostalCode', e.target.value)}
                className="mt-1 block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-3 py-2 text-sm"
              />
            </label>
          </div>
        </div>
      </div>

      {/* Toolbar */}
      <div className="flex-shrink-0 flex justify-end gap-2 px-4 py-3 border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
        <button
          onClick={handleSave}
          disabled={isSaving || !details}
          className="inline-flex items-center gap-2 px-3 py-1.5 text-sm bg-teal-600 text-white rounded-md hover:bg-teal-700 disabled:opacity-50"
        >
          <Save className="w-4 h-4" />
          {isSaving ? 'Saving...' : 'Save'}
        </button>
      </div>

      {/* ABR Modal */}
      {showAbrModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
          <div className="bg-white dark:bg-gray-900 rounded-lg shadow-xl max-w-lg w-full max-h-[90vh] overflow-y-auto p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
              Search Australian Business Register
            </h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
              Search by ABN, ACN, or company name. Selected company details will fill the form.
            </p>
            <SmartCompanySearch
              onCompanySelected={applyAbrResult}
              onManualEntry={() => setShowAbrModal(false)}
            />
            <button
              type="button"
              onClick={() => setShowAbrModal(false)}
              className="mt-4 text-sm text-gray-600 hover:text-gray-900"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
