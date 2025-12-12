import React from 'react';
import { Send, Loader2 } from 'lucide-react';
import { AlignType, ButtonAction, ButtonWidth } from '../../types/builder.types';
import { ComputedFieldStyles } from '../../utils/styleUtils';

interface SubmitButtonFieldProps {
    buttonText?: string;
    buttonAction?: ButtonAction;
    buttonWidth?: ButtonWidth;
    buttonAlign?: AlignType;
    showLoadingState?: boolean;
    disableUntilValid?: boolean;
    fieldStyles?: ComputedFieldStyles;
    // For preview mode
    isLoading?: boolean;
}

/**
 * Submit Button Field Component
 * 
 * A styled button for form submission with configurable:
 * - Button text
 * - Action type (submit, submit-and-reset, next-page)
 * - Width (auto, full)
 * - Alignment
 * - Loading state indicator
 */
export const SubmitButtonField: React.FC<SubmitButtonFieldProps> = ({
    buttonText = 'Submit',
    buttonAction = 'submit',
    buttonWidth = 'auto',
    buttonAlign = 'left',
    showLoadingState = true,
    disableUntilValid = true,
    fieldStyles,
    isLoading = false,
}) => {
    // Get primary color from field styles
    const primaryColor = fieldStyles?.computed?.primaryColor || '#0055FF';
    const fontFamily = fieldStyles?.computed?.fontFamily || 'Inter';
    const borderRadius = fieldStyles?.computed?.borderRadius || 6;

    // Alignment classes
    const alignmentClass = {
        left: 'justify-start',
        center: 'justify-center',
        right: 'justify-end',
    }[buttonAlign];

    // Width classes
    const widthClass = buttonWidth === 'full' ? 'w-full' : 'w-auto';

    // Action icon
    const ActionIcon = () => {
        if (isLoading && showLoadingState) {
            return <Loader2 size={16} className="animate-spin" />;
        }
        return <Send size={16} />;
    };

    // Get button label based on action
    const getActionLabel = () => {
        switch (buttonAction) {
            case 'submit-and-reset':
                return 'Submit & Start New';
            case 'next-page':
                return 'Next';
            default:
                return buttonText;
        }
    };

    return (
        <div
            className="border border-dashed border-gray-300 rounded-lg p-3 bg-white hover:border-blue-400 
                transition-colors group relative"
        >
            {/* Drag Handle */}
            <div className="absolute -left-1 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity">
                <Send size={14} className="text-gray-400" />
            </div>

            {/* Button Container - respects alignment */}
            <div className={`flex ${alignmentClass}`}>
                <button
                    type="button"
                    disabled
                    className={`${widthClass} px-6 py-2.5 text-white font-medium text-sm
                        flex items-center justify-center gap-2 transition-all
                        disabled:cursor-not-allowed shadow-sm hover:shadow-md`}
                    style={{
                        backgroundColor: primaryColor,
                        fontFamily,
                        borderRadius: `${borderRadius}px`,
                    }}
                >
                    <ActionIcon />
                    {getActionLabel()}
                </button>
            </div>

            {/* Feature badges */}
            <div className="flex items-center gap-2 mt-2 opacity-0 group-hover:opacity-100 transition-opacity">
                {showLoadingState && (
                    <span className="text-[9px] bg-blue-100 text-blue-600 px-1.5 py-0.5 rounded">
                        Loading State
                    </span>
                )}
                {disableUntilValid && (
                    <span className="text-[9px] bg-amber-100 text-amber-600 px-1.5 py-0.5 rounded">
                        Validates Form
                    </span>
                )}
            </div>

            {/* Component type badge */}
            <div className="absolute top-1 right-1 opacity-0 group-hover:opacity-100 transition-opacity">
                <span className="text-[9px] bg-green-100 text-green-600 px-1.5 py-0.5 rounded font-medium">
                    BUTTON
                </span>
            </div>
        </div>
    );
};

export default SubmitButtonField;

