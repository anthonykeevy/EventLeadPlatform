/**
 * Assets — Terms Page - Story 5.7
 * Company Settings → Assets → Terms
 * PDF upload + URL; URL validation; production simulation (popup emulates form users)
 */

import { useState, useEffect, useCallback, useRef } from 'react'
import { useParams } from 'react-router-dom'
import { FileText, Upload, Link as LinkIcon, Trash2, ExternalLink, AlertCircle, X, Save, Eye, Settings, Info, ChevronDown, ChevronUp } from 'lucide-react'
import {
  getCompanyTermsAssets,
  uploadTermsPdf,
  addTermsUrl,
  validateTermsUrl,
  deleteAsset,
  fetchAssetContentBlobUrl,
  updateTermsDisplaySettings,
  setDefaultTermsAsset,
} from '../api/companyAssetsApi'
import { useToastNotifications } from '../../ux'
import type { TermsAssetMetadata, TermsUrlValidateResult } from '../api/companyAssetsApi'

const SIZE_PRESETS = [
  { label: 'Small', w: 600, h: 500 },
  { label: 'Medium', w: 720, h: 600 },
  { label: 'Large', w: 900, h: 750 },
  { label: 'Full', w: '90vw', h: '85vh' },
] as const

export function AssetsTermsPage() {
  const { companyId } = useParams<{ companyId: string }>()
  const toast = useToastNotifications()
  const id = companyId ? parseInt(companyId, 10) : NaN
  const [assets, setAssets] = useState<TermsAssetMetadata[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [selectedAsset, setSelectedAsset] = useState<TermsAssetMetadata | null>(null)
  const [showDeleteModal, setShowDeleteModal] = useState(false)
  const [isDeleting, setIsDeleting] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [isAddingUrl, setIsAddingUrl] = useState(false)
  const [urlInput, setUrlInput] = useState('')
  const [urlDisplayName, setUrlDisplayName] = useState('')
  const [validateResult, setValidateResult] = useState<TermsUrlValidateResult | null>(null)
  const [isValidating, setIsValidating] = useState(false)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [isDragOver, setIsDragOver] = useState(false)
  const [modalWidth, setModalWidth] = useState<number | string>(720)
  const [modalHeight, setModalHeight] = useState<number | string>(600)
  const [viewMode, setViewMode] = useState<'edit' | 'prod'>('edit')
  const [hasUnsavedDisplayChanges, setHasUnsavedDisplayChanges] = useState(false)
  const [isSavingDisplay, setIsSavingDisplay] = useState(false)
  const [showUrlBlockersInfo, setShowUrlBlockersInfo] = useState(false)
  const [defaultTermsAssetId, setDefaultTermsAssetId] = useState<number | null>(null)
  const [isSettingDefault, setIsSettingDefault] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const loadAssets = useCallback(async () => {
    if (isNaN(id)) return
    setIsLoading(true)
    try {
      const { assets: list, defaultTermsAssetId: defaultId } = await getCompanyTermsAssets(id)
      setAssets(list)
      setDefaultTermsAssetId(defaultId ?? null)
    } catch {
      setAssets([])
      setDefaultTermsAssetId(null)
    } finally {
      setIsLoading(false)
    }
  }, [id])

  useEffect(() => {
    loadAssets()
  }, [loadAssets])

  const handleUpload = async (files: FileList | null) => {
    if (!files?.length || isUploading) return
    const pdfFiles = Array.from(files).filter((f) => f.type === 'application/pdf' || f.name.toLowerCase().endsWith('.pdf'))
    if (pdfFiles.length === 0) {
      toast.error('Please select PDF files', 'Invalid files')
      return
    }
    setIsUploading(true)
    let ok = 0
    let fail = 0
    for (const file of pdfFiles) {
      try {
        await uploadTermsPdf(file)
        ok += 1
      } catch (e: unknown) {
        fail += 1
        const detail = (e as { response?: { data?: { detail?: string | object } } })?.response?.data?.detail
        const msg = typeof detail === 'string' ? detail : (detail as { message?: string })?.message ?? 'Unknown error'
        toast.error(msg, 'Upload failed')
      }
    }
    if (ok > 0) {
      toast.success(
        fail > 0 ? `${ok} uploaded, ${fail} failed` : ok === 1 ? 'PDF uploaded' : `${ok} PDFs uploaded`,
        'Success'
      )
      loadAssets()
    }
    if (fail > 0 && ok === 0) toast.error('Failed to upload PDFs', 'Error')
    setIsUploading(false)
    if (fileInputRef.current) fileInputRef.current.value = ''
  }

  const handleValidateUrl = async () => {
    const url = urlInput.trim()
    if (!url) return
    setIsValidating(true)
    setValidateResult(null)
    try {
      const result = await validateTermsUrl(url)
      setValidateResult(result)
      if (result.embeddable) {
        toast.success('URL can be displayed in a pop-up', 'Valid')
      } else {
        toast.error(result.reason || 'Cannot display in pop-up', 'Validation')
      }
    } catch (e: unknown) {
      const detail = (e as { response?: { data?: { detail?: string | object } } })?.response?.data?.detail
      const msg = typeof detail === 'string' ? detail : (detail as { message?: string })?.message ?? 'Could not reach URL'
      toast.error(msg, 'Error')
      setValidateResult({ embeddable: false, reason: msg })
    } finally {
      setIsValidating(false)
    }
  }

  const handleAddUrl = async (displayMode: 'popup' | 'new_tab') => {
    const url = urlInput.trim()
    if (!url || isAddingUrl) return
    if (!url.startsWith('https://')) {
      toast.error('URL must use HTTPS', 'Invalid')
      return
    }
    if (displayMode === 'popup' && (!validateResult || !validateResult.embeddable)) {
      toast.error('Validate for pop-up first', 'Cannot add')
      return
    }
    setIsAddingUrl(true)
    try {
      await addTermsUrl(url, urlDisplayName.trim() || undefined, displayMode)
      toast.success(
        displayMode === 'popup' ? 'Terms URL added (pop-up)' : 'Terms URL added (new tab)',
        'Success'
      )
      loadAssets()
      setUrlInput('')
      setUrlDisplayName('')
      setValidateResult(null)
    } catch (e: unknown) {
      const msg = (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail
      toast.error(typeof msg === 'string' ? msg : 'Failed to add URL', 'Error')
    } finally {
      setIsAddingUrl(false)
    }
  }

  const handleDelete = async () => {
    if (!selectedAsset || isDeleting) return
    setIsDeleting(true)
    try {
      await deleteAsset(selectedAsset.assetId)
      setSelectedAsset(null)
      setShowDeleteModal(false)
      setPreviewUrl(null)
      toast.success('Terms removed', 'Success')
      loadAssets()
    } catch {
      toast.error('Failed to remove', 'Error')
    } finally {
      setIsDeleting(false)
    }
  }

  const buildPdfHash = (page: number) =>
    `page=${page}&view=FitH&zoom=page-width&toolbar=0`

  const handleView = (asset: TermsAssetMetadata) => {
    // URL with new_tab display mode → open in new browser tab
    if (asset.sourceType === 'url' && asset.termsDisplayMode === 'new_tab' && asset.sourceUrl) {
      window.open(asset.sourceUrl, '_blank', 'noopener,noreferrer')
      return
    }
    // PDF or URL with popup → show in terms viewer modal
    setSelectedAsset(asset)
    setViewMode('edit')
    const w = asset.displayWidthPx ?? 720
    const h = asset.displayHeightPx ?? 600
    setModalWidth(w)
    setModalHeight(h)
    setHasUnsavedDisplayChanges(false)
    if (asset.sourceType === 'url' && asset.sourceUrl) {
      const base = asset.sourceUrl.split('#')[0]
      setPreviewUrl(`${base}#${buildPdfHash(1)}`)
    } else {
      fetchAssetContentBlobUrl(asset.assetId)
        .then((url) => {
          const base = url.split('#')[0]
          setPreviewUrl(`${base}#${buildPdfHash(1)}`)
        })
        .catch(() => setPreviewUrl(null))
    }
  }

  const closeViewModal = () => {
    if (previewUrl && previewUrl.startsWith('blob:')) {
      URL.revokeObjectURL(previewUrl)
    }
    setSelectedAsset(null)
    setPreviewUrl(null)
  }

  const handleSizePreset = (preset: typeof SIZE_PRESETS[number]) => {
    setModalWidth(preset.w)
    setModalHeight(preset.h)
    // Full uses vw/vh — not persistable; only Small/Medium/Large can be saved
    setHasUnsavedDisplayChanges(preset.label !== 'Full')
  }

  const handleSetDefault = async (assetId: number) => {
    if (isNaN(id) || isSettingDefault || defaultTermsAssetId === assetId) return
    setIsSettingDefault(true)
    try {
      await setDefaultTermsAsset(id, assetId)
      setDefaultTermsAssetId(assetId)
      toast.success('Default Terms updated', 'Success')
    } catch {
      toast.error('Failed to set default', 'Error')
    } finally {
      setIsSettingDefault(false)
    }
  }

  const handleSaveDisplaySettings = async () => {
    if (!selectedAsset || !hasUnsavedDisplayChanges || isSavingDisplay) return
    const w = typeof modalWidth === 'string' ? 720 : modalWidth
    const h = typeof modalHeight === 'string' ? 600 : modalHeight
    setIsSavingDisplay(true)
    try {
      await updateTermsDisplaySettings(selectedAsset.assetId, {
        display_width_px: w,
        display_height_px: h,
      })
      setHasUnsavedDisplayChanges(false)
      toast.success('Display settings saved', 'Success')
      loadAssets()
    } catch {
      toast.error('Failed to save display settings', 'Error')
    } finally {
      setIsSavingDisplay(false)
    }
  }

  useEffect(() => {
    return () => {
      if (previewUrl && previewUrl.startsWith('blob:')) {
        URL.revokeObjectURL(previewUrl)
      }
    }
  }, [previewUrl])

  if (isNaN(id)) {
    return <div className="p-8 text-red-600">Invalid company ID</div>
  }

  return (
    <div className="h-full flex flex-col overflow-hidden">
      <div className="flex-shrink-0 px-4 py-3 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Assets — Terms of Agreement</h2>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
          Upload PDF or add URL for Terms of Service. We display Terms in a pop-up to keep form users on the form so they complete it. When defined, forms with Terms component use these automatically. With URL-based Terms, some hosts require your organisation to add our domain to their allowlist.
        </p>
      </div>

      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {/* PDF Upload */}
        <section>
          <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Upload PDF</h3>
          <input
            ref={fileInputRef}
            type="file"
            accept="application/pdf,.pdf"
            multiple
            className="hidden"
            onChange={(e) => handleUpload(e.target.files)}
          />
          <div
            onDragOver={(e) => { e.preventDefault(); setIsDragOver(true) }}
            onDragLeave={() => setIsDragOver(false)}
            onDrop={(e) => { e.preventDefault(); setIsDragOver(false); handleUpload(e.dataTransfer.files) }}
            onClick={() => fileInputRef.current?.click()}
            className={`rounded-lg border-2 border-dashed p-6 text-center cursor-pointer transition-colors ${
              isDragOver ? 'border-teal-500 bg-teal-50 dark:bg-teal-900/20' : 'border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'
            }`}
          >
            <Upload className="w-10 h-10 mx-auto text-gray-400 mb-2" />
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Drag and drop PDFs here, or click to browse
            </p>
            <p className="text-xs text-gray-500 mt-1">Terms of Service, Privacy Policy, consent documents</p>
          </div>
        </section>

        {/* Add URL */}
        <section>
          <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Or add Terms by URL</h3>
          <div className="space-y-2">
            {/* Blockers info — upfront so clients understand what can block URL use */}
            <div className="rounded-lg border border-blue-200 dark:border-blue-800 bg-blue-50 dark:bg-blue-900/20">
              <button
                type="button"
                onClick={() => setShowUrlBlockersInfo(!showUrlBlockersInfo)}
                className="w-full flex items-center justify-between gap-2 px-3 py-2 text-left text-sm text-blue-800 dark:text-blue-200 hover:bg-blue-100 dark:hover:bg-blue-900/30 rounded-lg transition-colors"
              >
                <span className="flex items-center gap-2">
                  <Info className="w-4 h-4" />
                  What can block URL-based Terms?
                </span>
                {showUrlBlockersInfo ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
              </button>
              {showUrlBlockersInfo && (
                <div className="px-3 pb-3 pt-0 text-xs text-blue-700 dark:text-blue-300 space-y-2">
                  <p><strong>Embedding:</strong> X-Frame-Options or CSP can prevent inline display. Form users can still open in a new tab.</p>
                  <p><strong>Reachability:</strong> 404, 403, 401, timeout, or DNS issues mean we cannot load the URL. For 403, your IT team may need to add our domain to the host's allowlist.</p>
                  <p><strong>Content:</strong> HTTPS required. Wrong Content-Type may affect display.</p>
                  <p><strong>Over time:</strong> Host may change policy or URL. Validate before adding; PDF upload is more reliable.</p>
                  <p className="text-blue-600 dark:text-blue-400">Use Validate to check. If blocked, ask IT to add our domain to the host's allowlist, or upload a PDF for full control.</p>
                </div>
              )}
            </div>
            <input
              type="url"
              value={urlInput}
              onChange={(e) => { setUrlInput(e.target.value); setValidateResult(null) }}
              placeholder="https://example.com/terms.pdf"
              className="block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-3 py-2 text-sm"
            />
            <input
              type="text"
              value={urlDisplayName}
              onChange={(e) => setUrlDisplayName(e.target.value)}
              placeholder="Display name (optional)"
              className="block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-3 py-2 text-sm"
            />
            {validateResult && !validateResult.embeddable && (
              <div className="flex flex-col gap-2 p-3 rounded-lg bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800">
                <div className="flex items-start gap-2">
                  <AlertCircle className="w-4 h-4 text-amber-600 flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-amber-800 dark:text-amber-200">
                      Cannot display in pop-up
                    </p>
                    <p className="text-xs text-amber-700 dark:text-amber-300 mt-0.5">{validateResult.reason}</p>
                  </div>
                </div>
                {validateResult.next_action && (
                  <p className="text-xs text-amber-800 dark:text-amber-200 pl-6 border-l-2 border-amber-300 dark:border-amber-700">
                    <strong>Next:</strong> {validateResult.next_action}
                  </p>
                )}
                <p className="text-xs text-amber-600 dark:text-amber-400 pl-6">
                  Add as new tab — form users will open it in a new tab. Once your organisation has added our domain to the host&apos;s allowlist, return here and validate again to add as pop-up. Or upload a PDF for full control.
                </p>
              </div>
            )}
            {validateResult && validateResult.embeddable && (
              <div className="p-2 rounded bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800">
                <p className="text-xs text-green-800 dark:text-green-200">
                  URL can be displayed in a pop-up. Form users will stay on the form. External URLs may stop working if the host changes policy.
                </p>
              </div>
            )}
            <p className="text-xs text-gray-500">
              Validate for pop-up before adding. Pop-up keeps form users on the form. New tab opens a separate window.
            </p>
            <div className="flex flex-wrap gap-2">
              <button
                type="button"
                onClick={handleValidateUrl}
                disabled={!urlInput.trim() || isValidating}
                className="px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-800 disabled:opacity-50"
              >
                {isValidating ? 'Validating...' : 'Validate for pop-up'}
              </button>
              <button
                type="button"
                onClick={() => handleAddUrl('popup')}
                disabled={!urlInput.trim().startsWith('https://') || isAddingUrl || !validateResult?.embeddable}
                className="px-3 py-1.5 text-sm bg-teal-600 text-white rounded-md hover:bg-teal-700 disabled:opacity-50"
              >
                {isAddingUrl ? 'Adding...' : 'Add URL (pop-up)'}
              </button>
              <button
                type="button"
                onClick={() => handleAddUrl('new_tab')}
                disabled={!urlInput.trim().startsWith('https://') || isAddingUrl}
                className="px-3 py-1.5 text-sm border border-teal-600 text-teal-600 dark:text-teal-400 rounded-md hover:bg-teal-50 dark:hover:bg-teal-900/30 disabled:opacity-50"
              >
                {isAddingUrl ? 'Adding...' : 'Add URL (new tab)'}
              </button>
            </div>
          </div>
        </section>

        {/* List */}
        <section>
          <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Your Terms</h3>
          {assets.length >= 2 && (
            <p className="text-xs text-gray-500 dark:text-gray-400 mb-2">
              Select which document forms will use when the Terms component is on a form.
            </p>
          )}
          {isLoading ? (
            <div className="text-gray-500 py-4">Loading...</div>
          ) : assets.length === 0 ? (
            <div className="text-center py-8 text-gray-500 dark:text-gray-400">
              <FileText className="w-12 h-12 mx-auto mb-3 opacity-50" />
              <p>No Terms yet. Upload a PDF or add a URL above.</p>
            </div>
          ) : (
            <ul className="divide-y divide-gray-200 dark:divide-gray-700">
              {assets.map((a) => (
                <li
                  key={a.assetId}
                  className="py-3 flex items-center justify-between gap-4"
                >
                  <div className="min-w-0 flex-1 flex items-center gap-3">
                    {assets.length >= 2 && (
                      <input
                        type="radio"
                        name="defaultTerms"
                        id={`default-${a.assetId}`}
                        checked={
                          defaultTermsAssetId === a.assetId ||
                          (defaultTermsAssetId == null && assets[0]?.assetId === a.assetId)
                        }
                        onChange={() => handleSetDefault(a.assetId)}
                        disabled={isSettingDefault}
                        className="w-4 h-4 text-teal-600 border-gray-300 focus:ring-teal-500"
                        title="Use this document for forms"
                      />
                    )}
                    <FileText className="w-8 h-8 text-gray-400 flex-shrink-0" />
                    <div className="min-w-0">
                      <div className="font-medium text-gray-900 dark:text-gray-100 truncate">
                        {a.displayName || (a.sourceType === 'url' ? a.sourceUrl : 'PDF')}
                      </div>
                      <div className="text-xs text-gray-500 flex items-center gap-1 flex-wrap">
                        {a.sourceType === 'url' ? <LinkIcon className="w-3 h-3" /> : 'PDF'}
                        {a.sourceType === 'url' && a.termsDisplayMode && (
                          <span className="text-teal-600 dark:text-teal-400">
                            · {a.termsDisplayMode === 'popup' ? 'pop-up' : 'new tab'}
                          </span>
                        )}
                        {a.byteSize > 0 && ` · ${(a.byteSize / 1024).toFixed(1)} KB`}
                      </div>
                    </div>
                  </div>
                  <div className="flex gap-2 flex-shrink-0">
                    <button
                      type="button"
                      onClick={() => handleView(a)}
                      className="px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded hover:bg-gray-50 dark:hover:bg-gray-800"
                    >
                      View
                    </button>
                    <button
                      type="button"
                      onClick={() => { setSelectedAsset(a); setShowDeleteModal(true) }}
                      className="p-1 text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded"
                      title="Delete"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>

      {/* View popup modal — emulates form users' Terms popup */}
      {selectedAsset && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
          onClick={closeViewModal}
        >
          <div
            className="bg-white dark:bg-gray-900 rounded-lg shadow-xl flex flex-col overflow-hidden"
            style={{
              width: typeof modalWidth === 'string' ? modalWidth : `${modalWidth}px`,
              height: typeof modalHeight === 'string' ? modalHeight : `${modalHeight}px`,
              maxWidth: '95vw',
              maxHeight: '95vh',
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex-shrink-0 px-4 py-3 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between gap-2">
              <div className="flex items-center gap-3">
                <div className="flex rounded border border-gray-300 dark:border-gray-600 p-0.5">
                  <button
                    type="button"
                    onClick={() => setViewMode('edit')}
                    className={`flex items-center gap-1 px-2 py-0.5 text-xs rounded ${viewMode === 'edit' ? 'bg-teal-600 text-white' : 'hover:bg-gray-100 dark:hover:bg-gray-800'}`}
                    title="Configure size and display"
                  >
                    <Settings className="w-3.5 h-3.5" />
                    Edit
                  </button>
                  <button
                    type="button"
                    onClick={() => setViewMode('prod')}
                    className={`flex items-center gap-1 px-2 py-0.5 text-xs rounded ${viewMode === 'prod' ? 'bg-teal-600 text-white' : 'hover:bg-gray-100 dark:hover:bg-gray-800'}`}
                    title="Preview what form users see (no controls)"
                  >
                    <Eye className="w-3.5 h-3.5" />
                    Prod view
                  </button>
                </div>
                {viewMode === 'edit' && (
                  <p className="text-xs text-gray-500 hidden sm:inline">
                    Configure size; save for form users.
                  </p>
                )}
                {viewMode === 'prod' && (
                  <p className="text-xs text-gray-500 hidden sm:inline">
                    What form users see — no controls.
                  </p>
                )}
              </div>
              <div className="flex items-center gap-2">
                {viewMode === 'edit' && (
                  <>
                    <span className="text-xs text-gray-500">Size:</span>
                    {SIZE_PRESETS.map((p) => (
                      <button
                        key={p.label}
                        type="button"
                        onClick={() => handleSizePreset(p)}
                        className="px-2 py-0.5 text-xs border border-gray-300 dark:border-gray-600 rounded hover:bg-gray-100 dark:hover:bg-gray-800"
                      >
                        {p.label}
                      </button>
                    ))}
                    {hasUnsavedDisplayChanges && (
                      <button
                        type="button"
                        onClick={handleSaveDisplaySettings}
                        disabled={isSavingDisplay}
                        className="flex items-center gap-1 px-2 py-1 text-xs bg-teal-600 text-white rounded hover:bg-teal-700 disabled:opacity-50"
                      >
                        <Save className="w-3 h-3" />
                        {isSavingDisplay ? 'Saving...' : 'Save'}
                      </button>
                    )}
                  </>
                )}
                <button
                  type="button"
                  onClick={closeViewModal}
                  className="p-1 text-gray-400 hover:text-gray-600 rounded"
                  title="Close"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>
            <div className="flex-1 overflow-hidden flex flex-col min-h-0">
              {viewMode === 'edit' && selectedAsset.sourceType === 'url' && (
                <div className="p-3 bg-amber-50 dark:bg-amber-900/20 border-b border-amber-200 dark:border-amber-800">
                  <p className="text-xs text-amber-800 dark:text-amber-200">
                    Some sites block embedding. If the preview is blank, use the link below to open in a new tab.
                  </p>
                </div>
              )}
              {previewUrl ? (
                <div className="flex-1 flex flex-col min-h-0 bg-gray-100 dark:bg-gray-800">
                  {viewMode === 'edit' && (
                    <div className="flex-shrink-0 px-4 py-2 border-b border-gray-200 dark:border-gray-700">
                      <p className="text-xs text-gray-500">
                        Click the PDF to focus it, then use arrow keys or scroll to change pages.
                      </p>
                    </div>
                  )}
                  <div className="flex-1 min-h-0 overflow-hidden">
                    {selectedAsset.sourceType === 'url' ? (
                      <iframe
                        src={previewUrl}
                        title="Terms preview"
                        className="w-full h-full min-h-[300px] border-0"
                        sandbox="allow-same-origin allow-scripts"
                      />
                    ) : (
                      <iframe
                        src={previewUrl}
                        title="Terms preview"
                        className="w-full h-full min-h-[300px] border-0"
                      />
                    )}
                  </div>
                </div>
              ) : (
                <div className="flex-1 flex items-center justify-center text-gray-500">
                  Loading...
                </div>
              )}
              {viewMode === 'edit' && (
                <div className="flex-shrink-0 p-3 border-t border-gray-200 dark:border-gray-700">
                  <a
                    href={previewUrl ?? (selectedAsset.sourceType === 'url' ? selectedAsset.sourceUrl : '#')}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 px-3 py-2 bg-teal-600 text-white rounded-md hover:bg-teal-700 text-sm font-medium"
                  >
                    <ExternalLink className="w-4 h-4" />
                    Open in new tab
                  </a>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Delete modal */}
      {showDeleteModal && selectedAsset && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
          <div className="bg-white dark:bg-gray-900 rounded-lg shadow-xl max-w-md w-full p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
              Remove Terms?
            </h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
              This will remove &quot;{selectedAsset.displayName || (selectedAsset.sourceType === 'url' ? selectedAsset.sourceUrl : 'PDF')}&quot; from your library.
            </p>
            <div className="flex gap-2 justify-end">
              <button
                type="button"
                onClick={() => setShowDeleteModal(false)}
                disabled={isDeleting}
                className="px-3 py-1.5 text-sm bg-gray-200 dark:bg-gray-700 rounded-md hover:bg-gray-300 dark:hover:bg-gray-600 disabled:opacity-50"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleDelete}
                disabled={isDeleting}
                className="px-3 py-1.5 text-sm bg-red-600 text-white rounded-md hover:bg-red-700 disabled:opacity-50"
              >
                {isDeleting ? 'Removing...' : 'Remove'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
