/**
 * BackgroundPropertiesPanel.tsx - Story 3.5, 5.1 Task T04, T06
 * Panel for editing canvas/page background properties
 * T06: placement metadata, cropping, off-canvas auto-remove
 */

import React, { useState, useEffect } from 'react';
import { ChevronDown, Palette, Image as ImageIcon, Layers, X, FolderOpen, Loader2 } from 'lucide-react';
import { PropertyColorPicker } from './inputs/PropertyColorPicker';
import { PropertyNumberInput } from './inputs/PropertyNumberInput';
import { PropertyTextInput } from './inputs/PropertyTextInput';
import { PropertySelect } from './inputs/PropertySelect';
import { AssetLibrary } from './AssetLibrary';
import { FormPage, BackgroundAssetMetadata, isHexColor } from '../../types/builder.types';
import { assetsApi } from '../../api/assetsApi';
import { createDefaultPlacement } from '../../utils/backgroundPlacementUtils';

interface BackgroundPropertiesPanelProps {
    pageBackground?: FormPage['background'];
    onBackgroundChange: (updates: Partial<NonNullable<FormPage['background']>>) => void;
    canvasWidth?: number;
    canvasHeight?: number;
}

/** When Fit (locked): which part of image stays visible */
const ANCHOR_OPTIONS = [
    { value: 'center', label: 'Center' },
    { value: 'top', label: 'Top' },
    { value: 'bottom', label: 'Bottom' },
    { value: 'left', label: 'Left' },
    { value: 'right', label: 'Right' },
    { value: 'top left', label: 'Top Left' },
    { value: 'top right', label: 'Top Right' },
    { value: 'bottom left', label: 'Bottom Left' },
    { value: 'bottom right', label: 'Bottom Right' },
];

export const BackgroundPropertiesPanel: React.FC<BackgroundPropertiesPanelProps> = ({
    pageBackground,
    onBackgroundChange,
    canvasWidth = 1920,
    canvasHeight = 980,
}) => {
    const [isExpanded, setIsExpanded] = useState(true);
    const [showAssetLibrary, setShowAssetLibrary] = useState(false);
    const [recentAssets, setRecentAssets] = useState<BackgroundAssetMetadata[]>([]);
    const [libraryLoading, setLibraryLoading] = useState(false);
    const [previewBlobUrl, setPreviewBlobUrl] = useState<string | null>(null);

    const openAssetLibrary = async () => {
        setLibraryLoading(true);
        try {
            const assets = await assetsApi.listBackgrounds();
            setRecentAssets(assets);
            setShowAssetLibrary(true);
        } catch (err) {
            console.error('Failed to load background asset library:', err);
            setRecentAssets([]);
            setShowAssetLibrary(true);
        } finally {
            setLibraryLoading(false);
        }
    };

    const currentType = pageBackground?.type || 'color';
    const currentValue = pageBackground?.value || '#FFFFFF';
    const currentAsset = pageBackground?.asset;

    // Fetch authenticated blob URL for asset preview so <img> can display it
    useEffect(() => {
        const assetId = currentAsset?.assetId;
        if (assetId == null) {
            setPreviewBlobUrl(null);
            return;
        }
        let revoked = false;
        const blobUrlRef: { current: string | null } = { current: null };
        assetsApi
            .fetchAssetContentBlobUrl(assetId)
            .then((url) => {
                if (!revoked) {
                    blobUrlRef.current = url;
                    setPreviewBlobUrl(url);
                } else {
                    URL.revokeObjectURL(url);
                }
            })
            .catch(() => setPreviewBlobUrl(null));
        return () => {
            revoked = true;
            if (blobUrlRef.current) {
                URL.revokeObjectURL(blobUrlRef.current);
                blobUrlRef.current = null;
            }
            setPreviewBlobUrl(null);
        };
    }, [currentAsset?.assetId]);

    const handleTypeChange = (type: 'color' | 'image') => {
        if (type === 'color') {
            // Keep image settings (asset, imageSize, imagePosition); only switch type and set colour from stored colorValue or current value if hex
            const colour =
                pageBackground?.colorValue ??
                (pageBackground?.value && isHexColor(pageBackground.value) ? pageBackground.value : null) ??
                '#FFFFFF';
            onBackgroundChange({ type, value: colour });
        } else {
            // Keep colour and image settings; only switch type (do not clear value/asset/imageSize/imagePosition)
            onBackgroundChange({ type });
        }
    };

    const handleAssetSelect = (asset: BackgroundAssetMetadata) => {
        const placement = createDefaultPlacement(canvasWidth, canvasHeight);
        // Store asset reference and resolve URL for preview. Default: Fit so full image visible, then user can resize frame.
        assetsApi.resolveAssetUrl(asset.assetId).then((url) => {
            onBackgroundChange({
                type: 'image',
                asset: asset,
                value: url,
                placement,
                imageSize: 'contain',
                imagePosition: 'center',
                lockAspectRatio: true,
            });
            setShowAssetLibrary(false);
            
            // Add to recent assets
            setRecentAssets((prev) => {
                if (prev.some(a => a.assetId === asset.assetId)) {
                    return prev;
                }
                return [asset, ...prev];
            });
        }).catch((err) => {
            console.error('Failed to resolve asset URL:', err);
            // Still store the asset reference even if URL resolution fails
            onBackgroundChange({
                type: 'image',
                asset: asset,
                value: assetsApi.getAssetContentUrl(asset.assetId),
                placement,
                imageSize: 'contain',
                imagePosition: 'center',
                lockAspectRatio: true,
            });
            setShowAssetLibrary(false);
        });
    };

    const handleRemoveAsset = () => {
        onBackgroundChange({
            type: 'image',
            value: '',
            asset: undefined,
        });
    };

    // Preview URL: use fetched blob URL for asset (auth-aware), or external URL when no asset
    const previewUrl = currentAsset
        ? previewBlobUrl
        : (currentValue && !currentValue.startsWith('data:') ? currentValue : null);

    return (
        <>
            {/* Panel Header - Fixed at top */}
            <div className="p-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between bg-gradient-to-r from-indigo-50 to-purple-50 dark:from-indigo-900/20 dark:to-purple-900/20 flex-shrink-0">
                <div className="flex items-center gap-2">
                    <Layers className="text-indigo-500" size={18} />
                    <div>
                        <h3 className="font-semibold text-gray-800 dark:text-gray-200 text-sm">
                            Canvas Background
                        </h3>
                        <p className="text-xs text-gray-500 dark:text-gray-400">
                            Page-level styling
                        </p>
                    </div>
                </div>
            </div>

            {/* Scrollable Content - using scroll to always reserve scrollbar space */}
            <div className="flex-1 overflow-y-scroll overflow-x-hidden">
            {/* Background Style Section */}
            <div className="border-b border-gray-200 dark:border-gray-700">
                <button
                    onClick={() => setIsExpanded(!isExpanded)}
                    className="w-full flex items-center justify-between px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
                >
                    <span>Background Style</span>
                    <ChevronDown 
                        size={16} 
                        className={`transform transition-transform ${isExpanded ? 'rotate-180' : ''}`} 
                    />
                </button>

                {isExpanded && (
                    <div className="px-4 pb-4 space-y-4">
                        {/* Type Selector */}
                        <div className="space-y-2">
                            <div className="flex space-x-2">
                                <button 
                                    onClick={() => handleTypeChange('color')}
                                    className={`flex-1 flex items-center justify-center gap-1.5 px-3 py-2 text-sm font-medium rounded-md border transition-colors ${
                                        currentType === 'color' 
                                            ? 'bg-indigo-600 text-white border-indigo-600' 
                                            : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50 dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600'
                                    }`}
                                >
                                    <Palette size={14} /> Color
                                </button>
                                <button 
                                    onClick={() => handleTypeChange('image')}
                                    className={`flex-1 flex items-center justify-center gap-1.5 px-3 py-2 text-sm font-medium rounded-md border transition-colors ${
                                        currentType === 'image' 
                                            ? 'bg-indigo-600 text-white border-indigo-600' 
                                            : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50 dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600'
                                    }`}
                                >
                                    <ImageIcon size={14} /> Image
                                </button>
                            </div>
                            <p className="text-xs text-gray-500 dark:text-gray-400">
                                Choose <strong>Image</strong> to upload or select a background from the library.
                            </p>
                        </div>

                        {/* Color Background Options */}
                        {currentType === 'color' && (
                            <PropertyColorPicker
                                label="Background Color"
                                value={currentValue}
                                onChange={(color) => onBackgroundChange({ value: color, colorValue: color })}
                            />
                        )}

                        {/* Image Background Options */}
                        {currentType === 'image' && (
                            <div className="space-y-4">
                                <div>
                                    <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">
                                        Background Image
                                    </label>
                                    
                                    {/* Asset Library Button */}
                                    <button
                                        onClick={openAssetLibrary}
                                        disabled={libraryLoading}
                                        className="w-full flex items-center justify-center gap-2 px-4 py-2.5 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors text-sm font-medium text-gray-700 dark:text-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
                                    >
                                        {libraryLoading ? (
                                            <Loader2 size={16} className="animate-spin" />
                                        ) : (
                                            <FolderOpen size={16} />
                                        )}
                                        {libraryLoading ? 'Loading library...' : (currentAsset ? 'Select or add image' : 'Select from Library')}
                                    </button>
                                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1.5">
                                        Opens the library to choose an image or upload more.
                                    </p>

                                    {/* Preview */}
                                    {(currentAsset || previewUrl) && (
                                        <div className="mt-3 relative rounded-md overflow-hidden border border-gray-200 dark:border-gray-700">
                                            {previewUrl ? (
                                            <img 
                                                src={previewUrl} 
                                                alt={currentAsset?.displayName || currentAsset?.originalFilename || 'Background preview'} 
                                                className="w-full h-32 object-cover"
                                            />
                                            ) : (
                                            <div className="w-full h-32 flex items-center justify-center bg-gray-100 dark:bg-gray-700">
                                                <Loader2 className="animate-spin text-gray-400" size={24} />
                                            </div>
                                            )}
                                            <button
                                                onClick={handleRemoveAsset}
                                                className="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600 transition-colors"
                                                title="Remove image"
                                            >
                                                <X size={14} />
                                            </button>
                                            {currentAsset && (
                                                <div className="absolute bottom-0 left-0 right-0 bg-black bg-opacity-60 text-white text-xs p-2">
                                                    <div className="font-medium truncate">
                                                        {currentAsset.displayName || currentAsset.originalFilename}
                                                    </div>
                                                    {currentAsset.widthPx && currentAsset.heightPx && (
                                                        <div className="text-xs opacity-75">
                                                            {currentAsset.widthPx} × {currentAsset.heightPx}px
                                                        </div>
                                                    )}
                                                </div>
                                            )}
                                        </div>
                                    )}

                                    {/* Legacy URL Input (for external URLs) */}
                                    <div className="mt-3">
                                        <PropertyTextInput
                                            label="Or enter image URL"
                                            value={currentAsset ? '' : (currentValue && !currentValue.startsWith('data:') ? currentValue : '')}
                                            onChange={(value) => {
                                                // Only allow non-Data URLs
                                                if (!value.startsWith('data:')) {
                                                    onBackgroundChange({ 
                                                        value,
                                                        asset: undefined, // Clear asset when using URL
                                                    });
                                                }
                                            }}
                                            placeholder="https://example.com/image.jpg"
                                        />
                                        <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                                            External URLs are supported, but uploading assets is recommended.
                                        </p>
                                    </div>
                                </div>

                                {/* T06 WYSIWYG: Frame defined by drag/resize; these control how image fills that frame */}
                                <div className="rounded-md bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-200 dark:border-indigo-700 p-3 space-y-3">
                                    <div>
                                        <p className="text-sm font-medium text-indigo-800 dark:text-indigo-200">
                                            Canvas: drag & resize
                                        </p>
                                        <p className="text-xs text-indigo-600 dark:text-indigo-300 mt-1">
                                            Switch to <strong>Background</strong> mode, drag to move, use handles to resize. Off-canvas = remove.
                                        </p>
                                    </div>
                                    <div className="grid grid-cols-1 gap-3 pt-2 border-t border-indigo-200 dark:border-indigo-700">
                                        <div className="flex items-center justify-between">
                                            <label className="text-sm font-medium text-indigo-800 dark:text-indigo-200">
                                                Lock aspect ratio
                                            </label>
                                            <button
                                                type="button"
                                                onClick={() => {
                                                    const nextLock = !(pageBackground?.lockAspectRatio ?? true);
                                                    onBackgroundChange({
                                                        lockAspectRatio: nextLock,
                                                        imageSize: nextLock ? 'contain' : 'fill',
                                                    });
                                                }}
                                                className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 ${
                                                    (pageBackground?.lockAspectRatio ?? true)
                                                        ? 'bg-indigo-600'
                                                        : 'bg-gray-200 dark:bg-gray-600'
                                                }`}
                                                role="switch"
                                            >
                                                <span
                                                    className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition ${
                                                        (pageBackground?.lockAspectRatio ?? true)
                                                            ? 'translate-x-5'
                                                            : 'translate-x-1'
                                                    }`}
                                                />
                                            </button>
                                        </div>
                                        <p className="text-xs text-gray-500 dark:text-gray-400 -mt-2">
                                            Lock: Fit to frame, corner handles only. Unlock: Stretch to frame, all 8 handles.
                                        </p>
                                        <div>
                                            <PropertySelect
                                                label="Anchor"
                                                value={pageBackground?.imagePosition || 'center'}
                                                onChange={(value) => onBackgroundChange({ imagePosition: value })}
                                                options={ANCHOR_OPTIONS}
                                            />
                                            <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                                                When locked, which part of the image stays centered
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Overlay Settings (applies to both color and image) */}
                        <div className="pt-3 border-t border-gray-100 dark:border-gray-800">
                            <p className="text-xs font-medium text-gray-500 dark:text-gray-400 mb-3">
                                Overlay
                            </p>
                            
                            <div className="space-y-3">
                                <PropertyColorPicker
                                    label="Overlay Color"
                                    value={pageBackground?.overlayColor || '#000000'}
                                    onChange={(color) => onBackgroundChange({ overlayColor: color })}
                                />

                                <PropertyNumberInput
                                    label="Overlay Opacity"
                                    value={pageBackground?.overlayOpacity ?? 0}
                                    onChange={(value) => onBackgroundChange({ overlayOpacity: value })}
                                    min={0}
                                    max={100}
                                    step={5}
                                    unit="%"
                                />
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* Help Text */}
            <div className="p-4 text-xs text-gray-500 dark:text-gray-400">
                <p className="mb-2">
                    <strong>Tip:</strong> Background settings apply to the current page only.
                </p>
                <p>
                    Switch to "Elements" mode to edit form components.
                </p>
            </div>
            </div>

            {/* Asset Library Modal */}
            <AssetLibrary
                isOpen={showAssetLibrary}
                onClose={() => setShowAssetLibrary(false)}
                onSelect={handleAssetSelect}
                recentAssets={recentAssets}
            />
        </>
    );
};
