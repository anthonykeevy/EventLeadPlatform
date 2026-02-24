/**
 * AssetLibrary Component - Story 5.1 Task T04
 * 
 * Modal component for browsing and selecting background assets.
 * Shows recently uploaded assets and allows uploading new ones.
 */

import React, { useState, useRef, useEffect } from 'react';
import { X, Upload, Image as ImageIcon, Loader2, AlertCircle } from 'lucide-react';
import { BackgroundAssetMetadata } from '../../types/builder.types';
import { assetsApi } from '../../api/assetsApi';

interface AssetLibraryProps {
    isOpen: boolean;
    onClose: () => void;
    onSelect: (asset: BackgroundAssetMetadata) => void;
    recentAssets?: BackgroundAssetMetadata[];
}

const MAX_FILE_SIZE_MB = 10; // Match backend limit
const MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024;
const MAX_IMAGE_DIMENSION_PX = 4096; // Match backend limit (width and height)

const IMAGE_EXTENSIONS = /\.(jpe?g|png|gif|webp)$/i;

function looksLikeImageFile(file: File): boolean {
    if (file.type && file.type.startsWith('image/')) return true;
    return IMAGE_EXTENSIONS.test(file.name || '');
}

/** Fetches asset image with auth and shows preview; revokes blob URL on unmount */
const AssetThumbnail: React.FC<{
    asset: BackgroundAssetMetadata;
    onClick: () => void;
}> = ({ asset, onClick }) => {
    const [blobUrl, setBlobUrl] = useState<string | null>(null);
    const [error, setError] = useState(false);

    useEffect(() => {
        let url: string | null = null;
        assetsApi
            .fetchAssetContentBlobUrl(asset.assetId, true)
            .then((u) => {
                url = u;
                setBlobUrl(u);
            })
            .catch(() => setError(true));
        return () => {
            if (url) URL.revokeObjectURL(url);
        };
    }, [asset.assetId]);

    const alt = asset.displayName || asset.originalFilename;
    return (
        <div
            onClick={onClick}
            className="group relative aspect-square rounded-lg overflow-hidden border-2 border-gray-200 dark:border-gray-700 hover:border-indigo-500 dark:hover:border-indigo-400 cursor-pointer transition-colors"
        >
            {blobUrl && !error ? (
                <img
                    src={blobUrl}
                    alt={alt}
                    className="w-full h-full object-cover"
                />
            ) : error ? (
                <div className="w-full h-full flex items-center justify-center bg-gray-100 dark:bg-gray-700">
                    <ImageIcon className="text-gray-400" size={32} />
                </div>
            ) : (
                <div className="w-full h-full flex items-center justify-center bg-gray-100 dark:bg-gray-700">
                    <Loader2 className="animate-spin text-gray-400" size={24} />
                </div>
            )}
            <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-50 transition-opacity flex items-center justify-center">
                <span className="text-white text-xs font-medium opacity-0 group-hover:opacity-100 transition-opacity">
                    Select
                </span>
            </div>
            {asset.displayName && (
                <div className="absolute bottom-0 left-0 right-0 bg-black bg-opacity-60 text-white text-xs p-1 truncate">
                    {asset.displayName}
                </div>
            )}
        </div>
    );
};

export const AssetLibrary: React.FC<AssetLibraryProps> = ({
    isOpen,
    onClose,
    onSelect,
    recentAssets = [],
}) => {
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [uploadedAssets, setUploadedAssets] = useState<BackgroundAssetMetadata[]>(recentAssets);
    const fileInputRef = useRef<HTMLInputElement>(null);

    // Sync with parent's recentAssets when modal opens (so form-persisted assets show after reopen)
    useEffect(() => {
        if (isOpen) setUploadedAssets(recentAssets);
    }, [isOpen, recentAssets]);

    if (!isOpen) return null;

    const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        const fileInfo = { name: file.name, type: file.type, size: file.size };

        // Validate file type: allow by MIME or by image extension (some browsers report type as "" for .jpg)
        if (!looksLikeImageFile(file)) {
            console.warn('[AssetLibrary] Upload rejected (client): not an image', fileInfo);
            setError('Please select an image file (PNG, JPG, GIF, etc.)');
            return;
        }

        // Validate file size
        if (file.size > MAX_FILE_SIZE_BYTES) {
            setError(`File size exceeds ${MAX_FILE_SIZE_MB}MB limit. Please choose a smaller image.`);
            return;
        }

        setError(null);
        setUploading(true);

        try {
            const response = await assetsApi.uploadBackground(file, file.name);
            const newAsset = response.asset;
            
            // Add to uploaded assets list (avoid duplicates)
            setUploadedAssets((prev) => {
                if (prev.some(a => a.assetId === newAsset.assetId)) {
                    return prev;
                }
                return [newAsset, ...prev];
            });

            // Auto-select the uploaded asset
            onSelect(newAsset);
            setUploading(false);
            
            // Reset file input
            if (fileInputRef.current) {
                fileInputRef.current.value = '';
            }
        } catch (err: unknown) {
            setUploading(false);
            const detail = err.response?.data?.detail ?? err.message ?? 'Upload failed. Please try again.';
            console.warn('[AssetLibrary] Upload failed', {
                ...fileInfo,
                status: err.response?.status,
                detail,
            });
            
            // Handle specific error codes
            if (err.response?.status === 413) {
                setError(`File size exceeds ${MAX_FILE_SIZE_MB}MB limit. Please choose a smaller image.`);
            } else if (err.response?.status === 400) {
                setError(typeof detail === 'string' ? detail : 'Invalid file type. Please select an image file (PNG, JPG, GIF, etc.)');
            } else {
                setError(typeof detail === 'string' ? detail : 'Upload failed. Please try again.');
            }
        }
    };

    const handleUploadClick = () => {
        fileInputRef.current?.click();
    };

    const allAssets = uploadedAssets;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] flex flex-col">
                {/* Header */}
                <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
                    <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-200">
                        Background Asset Library
                    </h2>
                    <button
                        onClick={onClose}
                        className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                    >
                        <X size={20} />
                    </button>
                </div>

                {/* Content */}
                <div className="flex-1 overflow-y-auto p-4">
                    {/* Upload Section */}
                    <div className="mb-6">
                        <input
                            ref={fileInputRef}
                            type="file"
                            accept="image/*"
                            onChange={handleFileSelect}
                            className="hidden"
                        />
                        <button
                            onClick={handleUploadClick}
                            disabled={uploading}
                            className="w-full flex items-center justify-center gap-2 px-4 py-3 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg hover:border-indigo-500 dark:hover:border-indigo-400 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {uploading ? (
                                <>
                                    <Loader2 className="animate-spin" size={20} />
                                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                                        Uploading...
                                    </span>
                                </>
                            ) : (
                                <>
                                    <Upload size={20} className="text-gray-500 dark:text-gray-400" />
                                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                                        Upload New Image
                                    </span>
                                </>
                            )}
                        </button>
                        <p className="text-xs text-gray-500 dark:text-gray-400 mt-2 text-center">
                            Max file size: {MAX_FILE_SIZE_MB}MB. Max dimensions: {MAX_IMAGE_DIMENSION_PX}×{MAX_IMAGE_DIMENSION_PX} px. Supported formats: PNG, JPG, GIF, WebP
                        </p>
                    </div>

                    {/* Error Display */}
                    {error && (
                        <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg flex items-start gap-2">
                            <AlertCircle className="text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" size={16} />
                            <p className="text-sm text-red-700 dark:text-red-300">{error}</p>
                        </div>
                    )}

                    {/* Asset Grid */}
                    {allAssets.length === 0 ? (
                        <div className="text-center py-12 text-gray-500 dark:text-gray-400">
                            <ImageIcon size={48} className="mx-auto mb-3 opacity-50" />
                            <p className="text-sm">No assets uploaded yet.</p>
                            <p className="text-xs mt-1">Upload an image to get started.</p>
                        </div>
                    ) : (
                        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                            {allAssets.map((asset) => (
                                <AssetThumbnail
                                    key={asset.assetId}
                                    asset={asset}
                                    onClick={() => onSelect(asset)}
                                />
                            ))}
                        </div>
                    )}
                </div>

                {/* Footer */}
                <div className="p-4 border-t border-gray-200 dark:border-gray-700 flex justify-end">
                    <button
                        onClick={onClose}
                        className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 rounded-md hover:bg-gray-200 dark:hover:bg-gray-600"
                    >
                        Close
                    </button>
                </div>
            </div>
        </div>
    );
};
