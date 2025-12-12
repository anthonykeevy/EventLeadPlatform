import React from 'react';
import { ChevronDown, Maximize2, Wand2 } from 'lucide-react';
import { PropertySelect, PropertyNumberInput } from './inputs';
import { ComponentProps, AlignType } from '../../types/builder.types';

interface DimensionsSectionProps {
    props: ComponentProps;
    onPropsChange: (updates: Partial<ComponentProps>) => void;
    componentType: string;
    /** Global font properties for auto-width calculation */
    globalFontFamily?: string;
    globalFontSize?: number;
}

const WIDTH_PRESET_OPTIONS = [
    { value: 'auto', label: 'Auto' },
    { value: '25%', label: '25%' },
    { value: '33%', label: '33%' },
    { value: '50%', label: '50%' },
    { value: '66%', label: '66%' },
    { value: '75%', label: '75%' },
    { value: '100%', label: '100%' },
    { value: 'custom', label: 'Custom (px)' },
];

const ALIGN_OPTIONS = [
    { value: 'left', label: 'Left' },
    { value: 'center', label: 'Center' },
    { value: 'right', label: 'Right' },
];

/**
 * DimensionsSection - Width, height, and alignment settings
 * 
 * Includes:
 * - Width presets (%, auto, custom px)
 * - Custom width input (when custom selected)
 * - Height (for applicable components)
 * - Auto-fit to content toggle
 * - Text alignment
 */
export const DimensionsSection: React.FC<DimensionsSectionProps> = ({
    props,
    onPropsChange,
    componentType,
}) => {
    const [isExpanded, setIsExpanded] = React.useState(false);
    const [customWidth, setCustomWidth] = React.useState<number>(300);

    // Determine if width is a preset or custom
    const isCustomWidth = props.width?.endsWith('px');
    const currentPreset = isCustomWidth ? 'custom' : (props.width || 'auto');

    // Components that support height
    const supportsHeight = ['textarea'].includes(componentType);
    
    // Components that support auto-fit
    const supportsAutoFit = ['text', 'email', 'number', 'select', 'phone'].includes(componentType);

    const handleWidthPresetChange = (value: string) => {
        if (value === 'custom') {
            onPropsChange({ width: `${customWidth}px` });
        } else {
            onPropsChange({ width: value });
        }
    };

    const handleCustomWidthChange = (value: number) => {
        setCustomWidth(value);
        onPropsChange({ width: `${value}px` });
    };

    return (
        <div className="border-b border-gray-200 dark:border-gray-700">
            {/* Section Header */}
            <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="w-full flex items-center justify-between px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
            >
                <div className="flex items-center gap-2">
                    <Maximize2 size={14} className="text-gray-400" />
                    <span>Dimensions</span>
                </div>
                <ChevronDown 
                    size={16} 
                    className={`transform transition-transform ${isExpanded ? 'rotate-180' : ''}`} 
                />
            </button>

            {/* Section Content */}
            {isExpanded && (
                <div className="px-4 pb-4 space-y-4">
                    {/* Width Preset */}
                    <PropertySelect
                        label="Width"
                        value={currentPreset}
                        onChange={handleWidthPresetChange}
                        options={WIDTH_PRESET_OPTIONS}
                        helpText="Component width"
                    />

                    {/* Custom Width Input */}
                    {isCustomWidth && (
                        <PropertyNumberInput
                            label="Custom Width"
                            value={parseInt(props.width || '300')}
                            onChange={handleCustomWidthChange}
                            min={50}
                            max={2000}
                            step={10}
                            unit="px"
                        />
                    )}

                    {/* Auto-fit to Content */}
                    {supportsAutoFit && (
                        <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                            <div className="flex items-start gap-2">
                                <Wand2 size={14} className="text-blue-500 mt-0.5" />
                                <div className="flex-1">
                                    <div className="flex items-center justify-between">
                                        <span className="text-sm font-medium text-blue-700 dark:text-blue-300">
                                            Auto-fit Width
                                        </span>
                                        <button
                                            type="button"
                                            onClick={() => {
                                                // Responsive fit: use ~90% of the active canvas width
                                                onPropsChange({ width: '90%', inputWidthMode: 'fill' });
                                            }}
                                            className="px-2 py-1 text-xs bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
                                        >
                                            Calculate
                                        </button>
                                    </div>
                                    <p className="text-xs text-blue-600 dark:text-blue-400 mt-1">
                                        Sets width to fit ~90% of content based on font settings
                                    </p>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Height (for textarea) */}
                    {supportsHeight && (
                        <PropertyNumberInput
                            label="Height"
                            value={props.height || 100}
                            onChange={(value) => onPropsChange({ height: value })}
                            min={40}
                            max={500}
                            step={10}
                            unit="px"
                            helpText="Component height"
                        />
                    )}

                    {/* Text Alignment */}
                    <PropertySelect
                        label="Text Alignment"
                        value={props.textAlign || 'left'}
                        onChange={(value) => onPropsChange({ textAlign: value as AlignType })}
                        options={ALIGN_OPTIONS}
                        helpText="Alignment of text within the input"
                    />

                    {/* Current dimensions display */}
                    <div className="pt-2 border-t border-gray-100 dark:border-gray-700">
                        <div className="flex items-center justify-between text-xs text-gray-400">
                            <span>Current Size</span>
                            <span className="font-mono">
                                {props.width || 'auto'} 
                                {supportsHeight && ` × ${props.height || 100}px`}
                            </span>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default DimensionsSection;

