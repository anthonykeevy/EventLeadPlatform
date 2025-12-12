import React from 'react';
import { ChevronDown, MousePointer } from 'lucide-react';
import { PropertyTextInput, PropertySelect, PropertyToggle } from './inputs';
import { ComponentProps, ButtonAction, ButtonWidth, AlignType } from '../../types/builder.types';

interface ButtonPropertiesSectionProps {
    props: ComponentProps;
    onPropsChange: (updates: Partial<ComponentProps>) => void;
}

const BUTTON_ACTION_OPTIONS = [
    { value: 'submit', label: 'Submit Form' },
    { value: 'submit-and-reset', label: 'Submit & Start New' },
    { value: 'next-page', label: 'Next Page' },
];

const BUTTON_WIDTH_OPTIONS = [
    { value: 'auto', label: 'Auto (fit content)' },
    { value: 'full', label: 'Full Width' },
];

const BUTTON_ALIGN_OPTIONS = [
    { value: 'left', label: 'Left' },
    { value: 'center', label: 'Center' },
    { value: 'right', label: 'Right' },
];

/**
 * ButtonPropertiesSection - Properties specific to Submit Button component
 * 
 * Includes:
 * - Button text
 * - Button action (submit, submit-and-reset, next-page)
 * - Width (auto, full)
 * - Alignment
 * - Loading state toggle
 * - Disable until valid toggle
 */
export const ButtonPropertiesSection: React.FC<ButtonPropertiesSectionProps> = ({
    props,
    onPropsChange,
}) => {
    const [isExpanded, setIsExpanded] = React.useState(true);

    return (
        <div className="border-b border-gray-200 dark:border-gray-700">
            {/* Section Header */}
            <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="w-full flex items-center justify-between px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
            >
                <div className="flex items-center gap-2">
                    <MousePointer size={14} className="text-green-500" />
                    <span>Button Settings</span>
                </div>
                <ChevronDown 
                    size={16} 
                    className={`transform transition-transform ${isExpanded ? 'rotate-180' : ''}`} 
                />
            </button>

            {/* Section Content */}
            {isExpanded && (
                <div className="px-4 pb-4 space-y-4">
                    {/* Button Text */}
                    <PropertyTextInput
                        label="Button Text"
                        value={props.buttonText || 'Submit'}
                        onChange={(value) => onPropsChange({ buttonText: value })}
                        placeholder="Submit"
                        helpText="Text displayed on the button"
                    />

                    {/* Button Action */}
                    <PropertySelect
                        label="Button Action"
                        value={props.buttonAction || 'submit'}
                        onChange={(value) => onPropsChange({ buttonAction: value as ButtonAction })}
                        options={BUTTON_ACTION_OPTIONS}
                        helpText="What happens when button is clicked"
                    />

                    {/* Layout Row: Width & Alignment */}
                    <div className="grid grid-cols-2 gap-3">
                        <PropertySelect
                            label="Width"
                            value={props.buttonWidth || 'auto'}
                            onChange={(value) => onPropsChange({ buttonWidth: value as ButtonWidth })}
                            options={BUTTON_WIDTH_OPTIONS}
                        />
                        <PropertySelect
                            label="Alignment"
                            value={props.buttonAlign || 'left'}
                            onChange={(value) => onPropsChange({ buttonAlign: value as AlignType })}
                            options={BUTTON_ALIGN_OPTIONS}
                        />
                    </div>

                    {/* Behavior Toggles */}
                    <div className="pt-3 border-t border-gray-100 dark:border-gray-700">
                        <div className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">
                            Behavior
                        </div>
                        
                        <div className="space-y-3">
                            <PropertyToggle
                                label="Show Loading State"
                                checked={props.showLoadingState ?? true}
                                onChange={(checked) => onPropsChange({ showLoadingState: checked })}
                                helpText="Display spinner while submitting"
                            />

                            <PropertyToggle
                                label="Disable Until Valid"
                                checked={props.disableUntilValid ?? true}
                                onChange={(checked) => onPropsChange({ disableUntilValid: checked })}
                                helpText="Button disabled until all required fields are filled"
                            />
                        </div>
                    </div>

                    {/* Preview */}
                    <div className="pt-3 border-t border-gray-100 dark:border-gray-700">
                        <div className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">
                            Preview
                        </div>
                        <div className={`flex ${props.buttonAlign === 'center' ? 'justify-center' : props.buttonAlign === 'right' ? 'justify-end' : 'justify-start'}`}>
                            <button
                                type="button"
                                disabled
                                className={`${props.buttonWidth === 'full' ? 'w-full' : ''} px-6 py-2 bg-blue-600 text-white rounded-md text-sm font-medium cursor-not-allowed`}
                            >
                                {props.buttonText || 'Submit'}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ButtonPropertiesSection;

