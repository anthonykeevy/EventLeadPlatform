import React from 'react';
import { ChevronDown, AlignLeft } from 'lucide-react';
import { PropertySelect, PropertyToggle, PropertyNumberInput } from './inputs';
import { ComponentProps, ResizeMode } from '../../types/builder.types';

interface TextareaPropertiesSectionProps {
    props: ComponentProps;
    onPropsChange: (updates: Partial<ComponentProps>) => void;
}

const RESIZE_MODE_OPTIONS = [
    { value: 'none', label: 'No Resize' },
    { value: 'vertical', label: 'Vertical Only' },
    { value: 'horizontal', label: 'Horizontal Only' },
    { value: 'both', label: 'Both Directions' },
    { value: 'auto-grow', label: 'Auto-grow (Future)' },
];

/**
 * TextareaPropertiesSection - Properties specific to Textarea component
 * 
 * Includes:
 * - Resize mode (none, vertical, horizontal, both, auto-grow)
 * - Max characters
 * - Show character count toggle
 * - Height setting
 */
export const TextareaPropertiesSection: React.FC<TextareaPropertiesSectionProps> = ({
    props,
    onPropsChange,
}) => {
    const [isExpanded, setIsExpanded] = React.useState(false);

    // Get current max length from validation
    const maxLength = props.validation?.maxLength;

    const handleMaxLengthChange = (value: number) => {
        onPropsChange({
            validation: {
                ...props.validation,
                maxLength: value > 0 ? value : undefined,
            },
        });
    };

    return (
        <div className="border-b border-gray-200 dark:border-gray-700">
            {/* Section Header */}
            <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="w-full flex items-center justify-between px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
            >
                <div className="flex items-center gap-2">
                    <AlignLeft size={14} className="text-blue-500" />
                    <span>Textarea Settings</span>
                </div>
                <ChevronDown 
                    size={16} 
                    className={`transform transition-transform ${isExpanded ? 'rotate-180' : ''}`} 
                />
            </button>

            {/* Section Content */}
            {isExpanded && (
                <div className="px-4 pb-4 space-y-4">
                    {/* Resize Mode */}
                    <PropertySelect
                        label="Resize Mode"
                        value={props.resizeMode || 'vertical'}
                        onChange={(value) => onPropsChange({ resizeMode: value as ResizeMode })}
                        options={RESIZE_MODE_OPTIONS}
                        helpText="How users can resize the textarea"
                    />

                    {/* Height */}
                    <PropertyNumberInput
                        label="Default Height"
                        value={props.height || 100}
                        onChange={(value) => onPropsChange({ height: value })}
                        min={50}
                        max={500}
                        step={10}
                        unit="px"
                        helpText="Initial height of the textarea"
                    />

                    {/* Character Limit Section */}
                    <div className="pt-3 border-t border-gray-100 dark:border-gray-700">
                        <div className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">
                            Character Limit
                        </div>

                        <div className="space-y-3">
                            <PropertyNumberInput
                                label="Max Characters"
                                value={maxLength || 0}
                                onChange={handleMaxLengthChange}
                                min={0}
                                max={10000}
                                step={100}
                                helpText="0 = no limit"
                            />

                            <PropertyToggle
                                label="Show Character Count"
                                checked={props.showCharacterCount ?? false}
                                onChange={(checked) => onPropsChange({ showCharacterCount: checked })}
                                helpText="Display 'X / Y characters' below textarea"
                            />
                        </div>
                    </div>

                    {/* Preview */}
                    <div className="pt-3 border-t border-gray-100 dark:border-gray-700">
                        <div className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">
                            Preview
                        </div>
                        <div className="relative">
                            <textarea
                                disabled
                                placeholder="Sample text input..."
                                className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 
                                    rounded-md bg-gray-50 dark:bg-gray-800 text-gray-500 cursor-not-allowed"
                                style={{
                                    height: `${props.height || 100}px`,
                                    resize: props.resizeMode === 'none' ? 'none' 
                                        : props.resizeMode === 'vertical' ? 'vertical'
                                        : props.resizeMode === 'horizontal' ? 'horizontal'
                                        : props.resizeMode === 'both' ? 'both'
                                        : 'none',
                                }}
                            />
                            {props.showCharacterCount && (
                                <div className="text-xs text-gray-400 mt-1 text-right">
                                    0 / {maxLength || '∞'} characters
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default TextareaPropertiesSection;

