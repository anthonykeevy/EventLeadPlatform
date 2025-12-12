import React from 'react';
import { ChevronDown, Database, FileSpreadsheet } from 'lucide-react';
import { PropertySelect, PropertyTextInput } from './inputs';
import { ComponentProps, ExportMode } from '../../types/builder.types';

interface DataExportSectionProps {
    props: ComponentProps;
    onPropsChange: (updates: Partial<ComponentProps>) => void;
    componentType: string;
}

const EXPORT_MODE_OPTIONS = [
    { value: 'single-value', label: 'Combined (comma-separated)' },
    { value: 'multi-column', label: 'Separate Columns (one per option)' },
];

const BOOLEAN_FORMAT_OPTIONS = [
    { value: 'true-false', label: 'true / false' },
    { value: '1-0', label: '1 / 0' },
    { value: 'yes-no', label: 'Yes / No' },
    { value: 'x-blank', label: 'X / (blank)' },
];

/**
 * DataExportSection - Configuration for how field data is exported
 * 
 * Shown for:
 * - Checkboxes (export mode: single value vs multi-column)
 * - Boolean fields (format selection)
 * 
 * Features:
 * - Export mode selection
 * - Custom separator for combined mode
 * - Boolean format selection
 * - Live preview with actual option labels
 */
export const DataExportSection: React.FC<DataExportSectionProps> = ({
    props,
    onPropsChange,
    componentType,
}) => {
    const [isExpanded, setIsExpanded] = React.useState(false);

    // Only show for checkbox/radio types
    const showExportMode = componentType === 'checkbox';
    const showBooleanFormat = componentType === 'checkbox' || componentType === 'terms';

    // Don't render if not applicable
    if (!showExportMode && !showBooleanFormat) {
        return null;
    }

    const options = props.options || [];
    const exportMode = props.exportMode || 'single-value';
    const separator = props.exportSeparator || ', ';
    const booleanFormat = (props as any).booleanFormat || 'true-false';
    const exportName = props.exportName || 'fieldName';

    // Get boolean values based on format
    const getBooleanValues = (format: string): [string, string] => {
        switch (format) {
            case '1-0': return ['1', '0'];
            case 'yes-no': return ['Yes', 'No'];
            case 'x-blank': return ['X', ''];
            default: return ['true', 'false'];
        }
    };

    const [trueValue, falseValue] = getBooleanValues(booleanFormat);

    // Build preview data
    const buildPreview = () => {
        if (options.length === 0) {
            // Simple boolean checkbox
            return (
                <div className="space-y-1">
                    <div className="flex items-center gap-2">
                        <span className="text-blue-500">{exportName}:</span>
                        <span className="text-green-600">{trueValue}</span>
                        <span className="text-gray-400">or</span>
                        <span className="text-red-500">{falseValue || '(empty)'}</span>
                    </div>
                </div>
            );
        }

        if (exportMode === 'multi-column') {
            // Separate column for each option
            return (
                <div className="space-y-1">
                    {options.slice(0, 3).map((opt, i) => (
                        <div key={i} className="flex items-center gap-2">
                            <span className="text-blue-500">{exportName}_{opt.value}:</span>
                            <span className={i === 0 ? 'text-green-600' : 'text-red-500'}>
                                {i === 0 ? trueValue : (falseValue || '(empty)')}
                            </span>
                        </div>
                    ))}
                    {options.length > 3 && (
                        <div className="text-gray-400 italic">
                            ... and {options.length - 3} more columns
                        </div>
                    )}
                </div>
            );
        } else {
            // Combined single value
            const selectedLabels = options
                .slice(0, 2)
                .map(o => o.label);
            
            return (
                <div className="space-y-1">
                    <div className="flex items-center gap-2">
                        <span className="text-blue-500">{exportName}:</span>
                        <span className="text-green-600">
                            "{selectedLabels.join(separator)}"
                        </span>
                    </div>
                    <div className="text-gray-400 text-[10px]">
                        Example when first {Math.min(2, options.length)} options are selected
                    </div>
                </div>
            );
        }
    };

    return (
        <div className="border-b border-gray-200 dark:border-gray-700">
            {/* Section Header */}
            <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="w-full flex items-center justify-between px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
            >
                <div className="flex items-center gap-2">
                    <Database size={14} className="text-emerald-500" />
                    <span>Data Export</span>
                </div>
                <ChevronDown 
                    size={16} 
                    className={`transform transition-transform ${isExpanded ? 'rotate-180' : ''}`} 
                />
            </button>

            {/* Section Content */}
            {isExpanded && (
                <div className="px-4 pb-4 space-y-4">
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                        Configure how this field's data is formatted for export and integrations.
                    </p>

                    {/* Export Mode (for checkboxes with options) */}
                    {showExportMode && options.length > 0 && (
                        <>
                            <PropertySelect
                                label="Export Mode"
                                value={exportMode}
                                onChange={(value) => onPropsChange({ exportMode: value as ExportMode })}
                                options={EXPORT_MODE_OPTIONS}
                                helpText="How checkbox selections are exported"
                            />

                            {/* Custom Separator (only for combined mode) */}
                            {exportMode === 'single-value' && (
                                <PropertyTextInput
                                    label="Separator"
                                    value={separator}
                                    onChange={(value) => onPropsChange({ exportSeparator: value || ', ' })}
                                    placeholder=", "
                                    helpText="Text between selected values"
                                />
                            )}
                        </>
                    )}

                    {/* Boolean Format */}
                    {showBooleanFormat && (
                        <PropertySelect
                            label="Boolean Format"
                            value={booleanFormat}
                            onChange={(value) => onPropsChange({ booleanFormat: value } as any)}
                            options={BOOLEAN_FORMAT_OPTIONS}
                            helpText="Format for true/false values in export"
                        />
                    )}

                    {/* Export Preview */}
                    <div className="pt-3 border-t border-gray-100 dark:border-gray-800">
                        <div className="flex items-center gap-2 text-xs font-medium text-gray-500 dark:text-gray-400 mb-2">
                            <FileSpreadsheet size={12} />
                            Export Preview
                        </div>
                        <div className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg font-mono text-xs">
                            {buildPreview()}
                        </div>

                        {/* Column count for multi-column mode */}
                        {exportMode === 'multi-column' && options.length > 0 && (
                            <div className="mt-2 text-xs text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-900/20 p-2 rounded">
                                This will create <strong>{options.length} columns</strong> in your export data.
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default DataExportSection;
