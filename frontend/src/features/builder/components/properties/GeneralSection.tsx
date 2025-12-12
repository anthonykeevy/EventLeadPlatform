import React, { useEffect, useRef } from 'react';
import { ChevronDown, AlertCircle, AlertTriangle, User, Database } from 'lucide-react';
import { PropertyTextInput, PropertyToggle, PropertySelect, PropertyNumberInput } from './inputs';
import { ComponentProps, LayoutType } from '../../types/builder.types';
import { InfoTooltip } from '../ui/InfoTooltip';
import { getExportNameInfo } from '../../data/validationRuleSeed';

interface GeneralSectionProps {
    props: ComponentProps;
    onPropsChange: (updates: Partial<ComponentProps>) => void;
    componentType: string;
    /** Global default layout for "use global" indicator */
    globalDefaultLayout?: 'vertical' | 'horizontal';
}

const LAYOUT_OPTIONS = [
    { value: 'vertical', label: 'Vertical (Label Above)' },
    { value: 'horizontal', label: 'Horizontal (Label Left)' },
];

/**
 * Validate export name: camelCase, no spaces, alphanumeric + underscore
 */
function validateExportName(name: string): string | null {
    if (!name) return null;
    if (/\s/.test(name)) return 'No spaces allowed';
    if (!/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(name)) return 'Use letters, numbers, underscore only';
    return null;
}

/**
 * Convert label to suggested export name (PascalCase)
 */
function suggestExportName(label: string): string {
    if (!label) return '';
    return label
        .replace(/[^a-zA-Z0-9\s]/g, '')
        .split(/\s+/)
        .filter(word => word.length > 0)
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join('');
}

export const GeneralSection: React.FC<GeneralSectionProps> = ({
    props,
    onPropsChange,
    componentType,
    globalDefaultLayout = 'vertical',
}) => {
    const [isExpanded, setIsExpanded] = React.useState(true);
    const [isDataExpanded, setIsDataExpanded] = React.useState(true);
    const prevLabelRef = useRef(props.label);
    
    // Determine effective layout (component override or global default)
    const hasLayoutOverride = props.layout !== undefined;
    const effectiveLayout = props.layout || globalDefaultLayout;
    
    // Auto-generate Export Name when Label changes (only if Export Name is empty or matches previous suggestion)
    useEffect(() => {
        const prevSuggestion = suggestExportName(prevLabelRef.current || '');
        const currentSuggestion = suggestExportName(props.label || '');
        
        // Update export name if it was empty or matched the previous auto-generated name
        if (props.label && (!props.exportName || props.exportName === prevSuggestion)) {
            onPropsChange({ exportName: currentSuggestion });
        }
        
        prevLabelRef.current = props.label;
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [props.label]); // Only react to label changes
    
    // Validation for export name
    const exportNameError = validateExportName(props.exportName || '');
    const exportNameWarning = !props.exportName ? 'Export name is required for data collection' : null;

    return (
        <>
            {/* ═══════════════════════════════════════════════════════════════ */}
            {/* IDENTITY & BEHAVIOR SECTION */}
            {/* ═══════════════════════════════════════════════════════════════ */}
            <div className="border-b border-gray-200 dark:border-gray-700">
                {/* Section Header */}
                <button
                    onClick={() => setIsExpanded(!isExpanded)}
                    className="w-full flex items-center justify-between px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
                >
                    <div className="flex items-center gap-2">
                        <User size={14} className="text-blue-500" />
                        <span>Identity & Behavior</span>
                    </div>
                    <ChevronDown 
                        size={16} 
                        className={`transform transition-transform ${isExpanded ? 'rotate-180' : ''}`} 
                    />
                </button>

                {/* Section Content */}
                {isExpanded && (
                    <div className="px-4 pb-4 space-y-4">
                        {/* Label */}
                        <PropertyTextInput
                            label="Label"
                            value={props.label || ''}
                            onChange={(value) => onPropsChange({ label: value })}
                            placeholder="Field Label"
                            helpText="The text displayed above/beside the input"
                        />

                        {/* Placeholder */}
                        <PropertyTextInput
                            label="Placeholder"
                            value={props.placeholder || ''}
                            onChange={(value) => onPropsChange({ placeholder: value })}
                            placeholder="Placeholder text..."
                            helpText="Hint text shown inside the empty input"
                        />

                        {/* Help Text */}
                        <PropertyTextInput
                            label="Help Text"
                            value={props.helpText || ''}
                            onChange={(value) => onPropsChange({ helpText: value })}
                            placeholder="Additional instructions..."
                            helpText="Descriptive text shown below the input"
                        />

                        {/* Required Toggle - Prominent position */}
                        <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                            <PropertyToggle
                                label={
                                    <span className="flex items-center gap-1">
                                        Required
                                        <span className="text-red-500">*</span>
                                    </span>
                                }
                                checked={props.required || false}
                                onChange={(checked) => onPropsChange({ required: checked })}
                                helpText="Users must fill this field to submit the form"
                            />
                        </div>

                        {/* Layout Dropdown */}
                        <div className="space-y-1">
                            <PropertySelect
                                label="Layout"
                                value={effectiveLayout}
                                onChange={(value) => onPropsChange({ layout: value as LayoutType })}
                                options={LAYOUT_OPTIONS}
                                helpText={hasLayoutOverride 
                                    ? "Custom layout for this component" 
                                    : `Using global default (${globalDefaultLayout})`
                                }
                            />
                            {hasLayoutOverride && (
                                <button
                                    type="button"
                                    onClick={() => onPropsChange({ layout: undefined })}
                                    className="text-xs text-blue-600 hover:text-blue-800 underline"
                                >
                                    Reset to global default
                                </button>
                            )}
                        </div>

                        {/* Component Type Badge */}
                        <div className="pt-2 border-t border-gray-100 dark:border-gray-700">
                            <div className="flex items-center justify-between">
                                <span className="text-xs text-gray-400">Component Type</span>
                                <span className="text-xs font-mono bg-gray-100 dark:bg-gray-700 px-2 py-0.5 rounded">
                                    {componentType}
                                </span>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* ═══════════════════════════════════════════════════════════════ */}
            {/* DATA COLLECTION SECTION */}
            {/* ═══════════════════════════════════════════════════════════════ */}
            <div className="border-b border-gray-200 dark:border-gray-700">
                {/* Section Header */}
                <button
                    onClick={() => setIsDataExpanded(!isDataExpanded)}
                    className="w-full flex items-center justify-between px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
                >
                    <div className="flex items-center gap-2">
                        <Database size={14} className="text-green-500" />
                        <span>Data Collection</span>
                    </div>
                    <ChevronDown 
                        size={16} 
                        className={`transform transition-transform ${isDataExpanded ? 'rotate-180' : ''}`} 
                    />
                </button>

                {/* Section Content */}
                {isDataExpanded && (
                    <div className="px-4 pb-4 space-y-4">
                        {/* Export Name */}
                        <div className="space-y-1.5">
                            <div className="flex items-center gap-1.5">
                                <span className="text-xs font-medium text-gray-700 dark:text-gray-300">
                                    Export Field Name <span className="text-red-500">*</span>
                                </span>
                                <InfoTooltip info={getExportNameInfo()} size={12} />
                            </div>
                            <div className="flex items-center gap-2">
                                <div className="flex-1">
                                    <PropertyTextInput
                                        label=""
                                        value={props.exportName || ''}
                                        onChange={(value) => {
                                            // Sanitize: remove spaces and special chars as they type
                                            const sanitized = value.replace(/[^a-zA-Z0-9_]/g, '');
                                            onPropsChange({ exportName: sanitized });
                                        }}
                                        placeholder={suggestExportName(props.label || '') || 'FieldName'}
                                        helpText="Column name in CSV exports"
                                    />
                                </div>
                                <button
                                    type="button"
                                    className="text-xs text-blue-600 hover:text-blue-800 underline whitespace-nowrap"
                                    onClick={() => {
                                        const suggestion = suggestExportName(props.label || '') || 'FieldName';
                                        const sanitized = suggestion.replace(/[^a-zA-Z0-9_]/g, '');
                                        onPropsChange({ exportName: sanitized });
                                    }}
                                >
                                    Use suggested
                                </button>
                            </div>
                            {exportNameError && (
                                <div className="flex items-center gap-1 text-xs text-red-500">
                                    <AlertCircle size={12} />
                                    {exportNameError}
                                </div>
                            )}
                            {exportNameWarning && !exportNameError && (
                                <div className="flex items-center gap-1 text-xs text-amber-500">
                                    <AlertTriangle size={12} />
                                    {exportNameWarning}
                                </div>
                            )}
                        </div>

                        {/* Tab Order */}
                        <PropertyNumberInput
                            label="Tab Order"
                            value={props.tabOrder || 0}
                            onChange={(value) => onPropsChange({ tabOrder: value })}
                            min={0}
                            max={999}
                            helpText="Keyboard navigation order (0 = auto)"
                        />
                    </div>
                )}
            </div>
        </>
    );
};
