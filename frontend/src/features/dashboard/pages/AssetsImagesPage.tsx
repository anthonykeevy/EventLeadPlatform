/**
 * Assets — Images Page - Story 5.7
 * Company Settings → Assets → Images
 * Grid/list view, selection, properties panel (display name), image swap.
 */

import { useState, useEffect, useCallback, useRef } from 'react'
import { useParams } from 'react-router-dom'
import { Image, Grid3X3, List, ArrowRightLeft, Upload, Trash2 } from 'lucide-react'
import { getCompanyImageAssets, updateAssetDisplayName, deleteAsset, uploadAssetImage, fetchAssetContentBlobUrl } from '../api/companyAssetsApi'
import { useToastNotifications } from '../../ux'
import type { BackgroundAssetMetadata } from '../../builder/types/builder.types'

/** Fetches asset image with auth (Bearer token) and displays it; img src alone causes 401. */
function AuthenticatedAssetImage({
  assetId,
  alt,
  className,
  useThumbnail = false,
}: { assetId: number; alt: string; className?: string; useThumbnail?: boolean }) {
  const [blobUrl, setBlobUrl] = useState<string | null>(null)
  const [error, setError] = useState(false)

  useEffect(() => {
    let url: string | null = null
    fetchAssetContentBlobUrl(assetId, useThumbnail)
      .then((u) => {
        url = u
        setBlobUrl(u)
      })
      .catch(() => setError(true))
    return () => {
      if (url) URL.revokeObjectURL(url)
    }
  }, [assetId, useThumbnail])

  if (error || !blobUrl) {
    return (
      <div className={`flex items-center justify-center bg-gray-100 dark:bg-gray-700 ${className ?? ''}`}>
        <Image className="w-8 h-8 text-gray-400" />
      </div>
    )
  }
  return <img src={blobUrl} alt={alt} className={className} />
}

export function AssetsImagesPage() {
  const { companyId } = useParams<{ companyId: string }>()
  const toast = useToastNotifications()
  const id = companyId ? parseInt(companyId, 10) : NaN
  const [assets, setAssets] = useState<BackgroundAssetMetadata[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
  const [selectedAssetId, setSelectedAssetId] = useState<number | null>(null)
  const [displayNameEdit, setDisplayNameEdit] = useState('')
  const [isSaving, setIsSaving] = useState(false)
  const [showSwapModal, setShowSwapModal] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [showDeleteModal, setShowDeleteModal] = useState(false)
  const [isDeleting, setIsDeleting] = useState(false)
  const [isDragOver, setIsDragOver] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const loadAssets = useCallback(async () => {
    if (isNaN(id)) return
    setIsLoading(true)
    try {
      const list = await getCompanyImageAssets(id)
      setAssets(list)
    } catch {
      setAssets([])
    } finally {
      setIsLoading(false)
    }
  }, [id])

  useEffect(() => {
    loadAssets()
  }, [loadAssets])

  const selectedAsset = selectedAssetId ? assets.find((a) => a.assetId === selectedAssetId) : null

  useEffect(() => {
    if (selectedAsset) {
      setDisplayNameEdit(selectedAsset.displayName ?? selectedAsset.originalFilename ?? '')
    } else {
      setDisplayNameEdit('')
    }
  }, [selectedAsset])

  const handleUpload = async (files: FileList | null) => {
    if (!files?.length || isUploading) return
    const imageFiles = Array.from(files).filter((f) => f.type.startsWith('image/'))
    if (imageFiles.length === 0) {
      toast.error('Please select image files (PNG, JPEG, WebP)', 'Invalid files')
      return
    }
    setIsUploading(true)
    let ok = 0
    let fail = 0
    for (const file of imageFiles) {
      try {
        await uploadAssetImage(file)
        ok += 1
      } catch {
        fail += 1
      }
    }
    if (ok > 0) {
      toast.success(
        fail > 0 ? `${ok} uploaded, ${fail} failed` : (ok === 1 ? 'Image uploaded' : `${ok} images uploaded`),
        'Success'
      )
      loadAssets()
    }
    if (fail > 0 && ok === 0) toast.error('Failed to upload images', 'Error')
    setIsUploading(false)
    if (fileInputRef.current) fileInputRef.current.value = ''
  }

  const handleDelete = async () => {
    if (!selectedAssetId || isDeleting) return
    setIsDeleting(true)
    try {
      await deleteAsset(selectedAssetId)
      setSelectedAssetId(null)
      setShowDeleteModal(false)
      toast.success('Image deleted', 'Success')
      loadAssets()
    } catch {
      toast.error('Failed to delete image', 'Error')
    } finally {
      setIsDeleting(false)
    }
  }

  const handleSaveDisplayName = async () => {
    if (!selectedAssetId || isSaving) return
    setIsSaving(true)
    try {
      await updateAssetDisplayName(selectedAssetId, displayNameEdit.trim() || '')
      setAssets((prev) =>
        prev.map((a) =>
          a.assetId === selectedAssetId
            ? { ...a, displayName: displayNameEdit.trim() || undefined }
            : a
        )
      )
      toast.success('Display name updated', 'Success')
    } catch {
      toast.error('Failed to update display name', 'Error')
    } finally {
      setIsSaving(false)
    }
  }

  if (isNaN(id)) {
    return <div className="p-8 text-red-600">Invalid company ID</div>
  }

  return (
    <div className="h-full flex flex-col overflow-hidden">
      <div className="flex-shrink-0 px-4 py-3 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Assets — Images</h2>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            Company images used in form backgrounds and components. Upload here or in Form Builder.
          </p>
        </div>
        <div className="flex gap-2 items-center">
          <input
            ref={fileInputRef}
            type="file"
            accept="image/png,image/jpeg,image/webp,image/jpg"
            multiple
            className="hidden"
            onChange={(e) => handleUpload(e.target.files)}
          />
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            disabled={isUploading}
            className="flex items-center gap-2 px-3 py-2 text-sm bg-teal-600 text-white rounded-md hover:bg-teal-700 disabled:opacity-50"
          >
            <Upload className="w-4 h-4" />
            {isUploading ? 'Uploading...' : 'Upload images'}
          </button>
          <button
            type="button"
            onClick={() => setViewMode('grid')}
            className={`p-2 rounded border ${viewMode === 'grid' ? 'border-teal-500 bg-teal-50 dark:bg-teal-900/20' : 'border-gray-300 dark:border-gray-600'}`}
            title="Grid view"
          >
            <Grid3X3 className="w-5 h-5" />
          </button>
          <button
            type="button"
            onClick={() => setViewMode('list')}
            className={`p-2 rounded border ${viewMode === 'list' ? 'border-teal-500 bg-teal-50 dark:bg-teal-900/20' : 'border-gray-300 dark:border-gray-600'}`}
            title="List view"
          >
            <List className="w-5 h-5" />
          </button>
        </div>
      </div>

      <div className="flex-1 flex overflow-hidden min-h-0">
        <div className={`overflow-y-auto p-6 ${selectedAsset ? 'flex-1 min-w-0' : 'flex-1'}`}>
          {/* Upload zone - drag and drop + click to browse */}
          <div
            onDragOver={(e) => { e.preventDefault(); setIsDragOver(true) }}
            onDragLeave={() => setIsDragOver(false)}
            onDrop={(e) => { e.preventDefault(); setIsDragOver(false); handleUpload(e.dataTransfer.files) }}
            onClick={() => fileInputRef.current?.click()}
            className={`mb-6 rounded-lg border-2 border-dashed p-8 text-center cursor-pointer transition-colors ${
              isDragOver ? 'border-teal-500 bg-teal-50 dark:bg-teal-900/20' : 'border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'
            }`}
          >
            <Upload className="w-10 h-10 mx-auto text-gray-400 dark:text-gray-500 mb-2" />
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Drag and drop images here, or click to browse (multiple allowed)
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">
              PNG, JPEG, WebP — used in form backgrounds and components
            </p>
          </div>

          {isLoading ? (
            <div className="flex items-center justify-center py-12 text-gray-500">Loading...</div>
          ) : assets.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <Image className="w-16 h-16 text-gray-400 mb-4" />
              <h3 className="text-lg font-medium text-gray-700 dark:text-gray-300 mb-2">No images yet</h3>
              <p className="text-gray-500 dark:text-gray-400 max-w-md">
                Upload images above or when adding form backgrounds in Form Builder. They will appear here.
              </p>
            </div>
          ) : viewMode === 'grid' ? (
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
              {assets.map((a) => (
                <button
                  key={a.assetId}
                  type="button"
                  onClick={() => setSelectedAssetId(a.assetId)}
                  className={`text-left rounded-lg border overflow-hidden transition-colors ${
                    selectedAssetId === a.assetId
                      ? 'border-teal-500 ring-2 ring-teal-500/30 bg-teal-50/50 dark:bg-teal-900/20'
                      : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:border-gray-300 dark:hover:border-gray-600'
                  }`}
                >
                  <div className="aspect-video bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
                    <AuthenticatedAssetImage
                      assetId={a.assetId}
                      alt={a.displayName ?? a.originalFilename}
                      className="max-w-full max-h-full object-contain"
                      useThumbnail
                    />
                  </div>
                  <div className="p-2 text-sm truncate" title={a.displayName ?? a.originalFilename}>
                    {a.displayName ?? a.originalFilename}
                  </div>
                </button>
              ))}
            </div>
          ) : (
            <ul className="divide-y divide-gray-200 dark:divide-gray-700">
              {assets.map((a) => (
                <li key={a.assetId}>
                  <button
                    type="button"
                    onClick={() => setSelectedAssetId(a.assetId)}
                    className={`w-full py-3 flex items-center gap-4 text-left rounded-md transition-colors ${
                      selectedAssetId === a.assetId
                        ? 'bg-teal-50 dark:bg-teal-900/20'
                        : 'hover:bg-gray-50 dark:hover:bg-gray-800'
                    }`}
                  >
                    <div className="w-16 h-16 flex-shrink-0 rounded border border-gray-200 dark:border-gray-600 overflow-hidden bg-gray-100 dark:bg-gray-700">
                      <AuthenticatedAssetImage
                        assetId={a.assetId}
                        alt={a.displayName ?? a.originalFilename}
                        className="w-full h-full object-cover"
                        useThumbnail
                      />
                    </div>
                    <div className="min-w-0 flex-1">
                      <div className="font-medium text-gray-900 dark:text-gray-100 truncate">
                        {a.displayName ?? a.originalFilename}
                      </div>
                      <div className="text-sm text-gray-500 dark:text-gray-400">
                        {a.widthPx != null && a.heightPx != null ? `${a.widthPx} × ${a.heightPx}` : a.originalFilename}
                      </div>
                    </div>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Properties panel - shown when image selected */}
        {selectedAsset && (
          <div className="w-80 flex-shrink-0 border-l border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 flex flex-col overflow-hidden">
            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
              <h3 className="font-medium text-gray-900 dark:text-gray-100">Properties</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">
                Edit display name or swap this image across forms.
              </p>
            </div>
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Display name
                </label>
                <input
                  type="text"
                  value={displayNameEdit}
                  onChange={(e) => setDisplayNameEdit(e.target.value)}
                  className="block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-3 py-2 text-sm"
                  placeholder="e.g. Company logo"
                />
                <button
                  type="button"
                  onClick={handleSaveDisplayName}
                  disabled={isSaving}
                  className="mt-2 px-3 py-1.5 text-sm bg-teal-600 text-white rounded-md hover:bg-teal-700 disabled:opacity-50"
                >
                  {isSaving ? 'Saving...' : 'Save'}
                </button>
              </div>
              {selectedAsset.widthPx != null && selectedAsset.heightPx != null && (
                <div>
                  <span className="text-sm text-gray-500 dark:text-gray-400">
                    Dimensions: {selectedAsset.widthPx} × {selectedAsset.heightPx}
                  </span>
                </div>
              )}
              <div>
                <button
                  type="button"
                  onClick={() => setShowSwapModal(true)}
                  className="flex items-center gap-2 px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-800"
                >
                  <ArrowRightLeft className="w-4 h-4" />
                  Swap with another image
                </button>
                <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
                  Replace this image across all forms that use it.
                </p>
              </div>
              <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
                <button
                  type="button"
                  onClick={() => setShowDeleteModal(true)}
                  className="flex items-center gap-2 px-3 py-2 text-sm text-red-600 dark:text-red-400 border border-red-300 dark:border-red-700 rounded-md hover:bg-red-50 dark:hover:bg-red-900/20"
                >
                  <Trash2 className="w-4 h-4" />
                  Delete image
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Delete confirmation modal */}
      {showDeleteModal && selectedAsset && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
          <div className="bg-white dark:bg-gray-900 rounded-lg shadow-xl max-w-md w-full p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
              Delete image?
            </h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
              This will remove &quot;{selectedAsset.displayName ?? selectedAsset.originalFilename}&quot; from your library. Forms using this image may show a broken background until you choose a different image.
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
                {isDeleting ? 'Deleting...' : 'Delete'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Swap modal - placeholder for future implementation */}
      {showSwapModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
          <div className="bg-white dark:bg-gray-900 rounded-lg shadow-xl max-w-md w-full p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
              Swap image
            </h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
              Image swap will replace this image across all forms that use it. Choose an image with the same dimensions or aspect ratio to avoid layout changes. This feature is coming soon.
            </p>
            <button
              type="button"
              onClick={() => setShowSwapModal(false)}
              className="px-3 py-1.5 text-sm bg-gray-200 dark:bg-gray-700 rounded-md hover:bg-gray-300 dark:hover:bg-gray-600"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
