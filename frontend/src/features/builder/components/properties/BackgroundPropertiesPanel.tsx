/**
 * BackgroundPropertiesPanel.tsx - Story 3.5
 * Panel for editing canvas/page background properties
 */

import React, { useState } from 'react';
import { ChevronDown, Palette, Image as ImageIcon, Layers, X } from 'lucide-react';
import { PropertyColorPicker } from './inputs/PropertyColorPicker';
import { PropertyNumberInput } from './inputs/PropertyNumberInput';
import { PropertyTextInput } from './inputs/PropertyTextInput';
import { PropertySelect } from './inputs/PropertySelect';
import { FormPage } from '../../types/builder.types';

interface BackgroundPropertiesPanelProps {
    pageBackground?: FormPage['background'];
    onBackgroundChange: (updates: Partial<NonNullable<FormPage['background']>>) => void;
}

const IMAGE_SIZE_OPTIONS = [
    { value: 'cover', label: 'Cover' },
    { value: 'contain', label: 'Contain' },
    { value: 'tile', label: 'Tile' },
    { value: 'auto', label: 'Auto' },
];

const IMAGE_POSITION_OPTIONS = [
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
}) => {
    const [isExpanded, setIsExpanded] = useState(true);

    const currentType = pageBackground?.type || 'color';
    const currentValue = pageBackground?.value || '#FFFFFF';

    const handleTypeChange = (type: 'color' | 'image') => {
        onBackgroundChange({ 
            type, 
            value: type === 'color' ? '#FFFFFF' : '',
        });
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                onBackgroundChange({ type: 'image', value: reader.result as string });
            };
            reader.readAsDataURL(file);
        }
    };

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

                        {/* Color Background Options */}
                        {currentType === 'color' && (
                            <PropertyColorPicker
                                label="Background Color"
                                value={currentValue}
                                onChange={(color) => onBackgroundChange({ value: color })}
                            />
                        )}

                        {/* Image Background Options */}
                        {currentType === 'image' && (
                            <div className="space-y-4">
                                <div>
                                    <label 
                                        htmlFor="background-image-upload" 
                                        className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1 block"
                                    >
                                        Background Image
                                    </label>
                                    <input 
                                        id="background-image-upload" 
                                        type="file" 
                                        accept="image/*" 
                                        onChange={handleFileChange} 
                                        className="w-full text-sm text-gray-500 file:mr-2 file:py-1.5 file:px-3 file:rounded file:border-0 file:text-sm file:font-medium file:bg-gray-100 file:text-gray-700 hover:file:bg-gray-200 dark:file:bg-gray-700 dark:file:text-gray-200"
                                    />
                                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                                        Upload an image or enter a URL below.
                                    </p>
                                </div>

                                <PropertyTextInput
                                    label="Image URL"
                                    value={currentValue.startsWith('data:') ? '' : currentValue}
                                    onChange={(value) => onBackgroundChange({ value })}
                                    placeholder="https://example.com/image.jpg"
                                />

                                {currentValue && currentValue.startsWith('data:') && (
                                    <div className="relative rounded-md overflow-hidden border border-gray-200 dark:border-gray-700">
                                        <img 
                                            src={currentValue} 
                                            alt="Preview" 
                                            className="w-full h-24 object-cover"
                                        />
                                        <button
                                            onClick={() => onBackgroundChange({ value: '' })}
                                            className="absolute top-1 right-1 bg-red-500 text-white rounded-full p-0.5 hover:bg-red-600"
                                            title="Remove image"
                                        >
                                            <X size={14} />
                                        </button>
                                    </div>
                                )}

                                <PropertySelect
                                    label="Image Size"
                                    value={pageBackground?.imageSize || 'cover'}
                                    onChange={(value) => onBackgroundChange({ imageSize: value as 'cover' | 'contain' | 'tile' | 'auto' })}
                                    options={IMAGE_SIZE_OPTIONS}
                                />

                                <PropertySelect
                                    label="Image Position"
                                    value={pageBackground?.imagePosition || 'center'}
                                    onChange={(value) => onBackgroundChange({ imagePosition: value })}
                                    options={IMAGE_POSITION_OPTIONS}
                                />
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
        </>
    );
};
