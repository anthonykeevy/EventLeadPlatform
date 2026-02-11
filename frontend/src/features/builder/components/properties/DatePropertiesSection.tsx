import React from 'react';
import { ChevronDown, Calendar, Clock } from 'lucide-react';
import { PropertyTextInput, PropertySelect } from './inputs';
import { ComponentProps } from '../../types/builder.types';

interface DatePropertiesSectionProps {
    props: ComponentProps;
    onPropsChange: (updates: Partial<ComponentProps>) => void;
}

const DATE_TYPE_OPTIONS = [
    { value: 'date', label: 'Date Only' },
    { value: 'datetime', label: 'Date & Time' },
    { value: 'time', label: 'Time Only' },
];

const PICKER_STYLE_OPTIONS = [
    { value: 'calendar', label: 'Calendar Popup' },
    { value: 'dropdown', label: 'Dropdowns (Day/Month/Year)' },
    { value: 'native', label: 'Native Browser Picker' },
];

const DATE_FORMAT_OPTIONS = [
    { value: 'DD/MM/YYYY', label: 'DD/MM/YYYY (UK/AU)' },
    { value: 'MM/DD/YYYY', label: 'MM/DD/YYYY (US)' },
    { value: 'YYYY-MM-DD', label: 'YYYY-MM-DD (ISO)' },
    { value: 'DD-MM-YYYY', label: 'DD-MM-YYYY' },
    { value: 'DD.MM.YYYY', label: 'DD.MM.YYYY (EU)' },
    { value: 'MMMM D, YYYY', label: 'January 1, 2024' },
    { value: 'D MMMM YYYY', label: '1 January 2024' },
];

/**
 * DatePropertiesSection - Configuration for date/time input
 * 
 * Features:
 * - Date type selection (date, datetime, time)
 * - Picker style (calendar, dropdown, native)
 * - Display format
 * - Date parts selection
 * - Date range configuration
 */
export const DatePropertiesSection: React.FC<DatePropertiesSectionProps> = ({
    props,
    onPropsChange,
}) => {
    const [isExpanded, setIsExpanded] = React.useState(true);

    const dateType = props.dateType || 'date';
    const showDateParts = dateType !== 'time';
    const showTimeParts = dateType === 'datetime' || dateType === 'time';
    const isDateRange = props.validation?.isDateRange ?? false;

    // Current date parts
    const dateParts = props.dateParts || { year: true, month: true, day: true };

    const updateDateParts = (updates: Partial<typeof dateParts>) => {
        onPropsChange({ dateParts: { ...dateParts, ...updates } });
    };

    return (
        <div className="border-b border-gray-200 dark:border-gray-700">
            {/* Section Header */}
            <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="w-full flex items-center justify-between px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
            >
                <div className="flex items-center gap-2">
                    <Calendar size={14} className="text-blue-500" />
                    <span>Date Settings</span>
                </div>
                <ChevronDown 
                    size={16} 
                    className={`transform transition-transform ${isExpanded ? 'rotate-180' : ''}`} 
                />
            </button>

            {/* Section Content */}
            {isExpanded && (
                <div className="px-4 pb-4 space-y-4">
                    {/* Date Type */}
                    <PropertySelect
                        label="Date Type"
                        value={dateType}
                        onChange={(value) => onPropsChange({ dateType: value as ComponentProps['dateType'] })}
                        options={DATE_TYPE_OPTIONS}
                        helpText="What date/time parts to capture"
                    />

                    {/* Picker Style */}
                    <PropertySelect
                        label="Picker Style"
                        value={props.pickerStyle || 'calendar'}
                        onChange={(value) => onPropsChange({ pickerStyle: value as ComponentProps['pickerStyle'] })}
                        options={PICKER_STYLE_OPTIONS}
                        helpText="How the date picker is displayed"
                    />

                    {/* Display Format */}
                    {showDateParts && (
                        <PropertySelect
                            label="Display Format"
                            value={props.dateFormat || 'DD/MM/YYYY'}
                            onChange={(value) => onPropsChange({ dateFormat: value })}
                            options={DATE_FORMAT_OPTIONS}
                            helpText="How dates are shown to users"
                        />
                    )}

                    {/* Date Parts Selection */}
                    {showDateParts && (
                        <div className="space-y-2">
                            <label className="block text-xs font-medium text-gray-500 dark:text-gray-400">
                                Required Date Parts
                            </label>
                            <div className="flex gap-3">
                                <label className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
                                    <input
                                        type="checkbox"
                                        checked={dateParts.day !== false}
                                        onChange={(e) => updateDateParts({ day: e.target.checked })}
                                        className="rounded border-gray-300 text-blue-500 focus:ring-blue-500"
                                    />
                                    Day
                                </label>
                                <label className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
                                    <input
                                        type="checkbox"
                                        checked={dateParts.month !== false}
                                        onChange={(e) => updateDateParts({ month: e.target.checked })}
                                        className="rounded border-gray-300 text-blue-500 focus:ring-blue-500"
                                    />
                                    Month
                                </label>
                                <label className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
                                    <input
                                        type="checkbox"
                                        checked={dateParts.year !== false}
                                        onChange={(e) => updateDateParts({ year: e.target.checked })}
                                        className="rounded border-gray-300 text-blue-500 focus:ring-blue-500"
                                    />
                                    Year
                                </label>
                            </div>
                        </div>
                    )}

                    {/* Time Parts Selection */}
                    {showTimeParts && (
                        <div className="space-y-2">
                            <label className="block text-xs font-medium text-gray-500 dark:text-gray-400">
                                Time Precision
                            </label>
                            <div className="flex gap-3">
                                <label className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
                                    <input
                                        type="checkbox"
                                        checked={dateParts.hour !== false}
                                        onChange={(e) => updateDateParts({ hour: e.target.checked })}
                                        className="rounded border-gray-300 text-blue-500 focus:ring-blue-500"
                                    />
                                    Hour
                                </label>
                                <label className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
                                    <input
                                        type="checkbox"
                                        checked={dateParts.minute !== false}
                                        onChange={(e) => updateDateParts({ minute: e.target.checked })}
                                        className="rounded border-gray-300 text-blue-500 focus:ring-blue-500"
                                    />
                                    Minute
                                </label>
                            </div>
                        </div>
                    )}

                    {/* Date Range Labels */}
                    {isDateRange && (
                        <div className="pt-3 border-t border-gray-100 dark:border-gray-800 space-y-3">
                            <div className="flex items-center gap-2 text-xs font-medium text-gray-500 dark:text-gray-400">
                                <Clock size={12} />
                                Date Range Labels
                            </div>
                            
                            <div className="grid grid-cols-2 gap-3">
                                <PropertyTextInput
                                    label="Start Label"
                                    value={props.dateRangeLabels?.start || ''}
                                    onChange={(value) => onPropsChange({ 
                                        dateRangeLabels: { 
                                            ...props.dateRangeLabels, 
                                            start: value || undefined 
                                        } 
                                    })}
                                    placeholder="Start Date"
                                />
                                <PropertyTextInput
                                    label="End Label"
                                    value={props.dateRangeLabels?.end || ''}
                                    onChange={(value) => onPropsChange({ 
                                        dateRangeLabels: { 
                                            ...props.dateRangeLabels, 
                                            end: value || undefined 
                                        } 
                                    })}
                                    placeholder="End Date"
                                />
                            </div>

                            <div className="text-xs text-gray-400 dark:text-gray-500 bg-blue-50 dark:bg-blue-900/20 p-2 rounded">
                                <strong>Tip:</strong> Enable "Date Range" in the Validation section to use this feature.
                            </div>
                        </div>
                    )}

                    {/* Preview */}
                    <div className="pt-3 border-t border-gray-100 dark:border-gray-800">
                        <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-2">
                            Preview
                        </label>
                        <div className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                            <div className="flex items-center gap-3 text-sm text-gray-700 dark:text-gray-300">
                                {dateType !== 'time' && (
                                    <div className="flex items-center gap-2">
                                        <Calendar size={16} className="text-blue-500" />
                                        <span className="font-mono">
                                            {props.dateFormat || 'DD/MM/YYYY'}
                                        </span>
                                    </div>
                                )}
                                {showTimeParts && (
                                    <div className="flex items-center gap-2">
                                        <Clock size={16} className="text-blue-500" />
                                        <span className="font-mono">
                                            {dateParts.hour !== false ? 'HH' : '--'}
                                            :
                                            {dateParts.minute !== false ? 'MM' : '--'}
                                        </span>
                                    </div>
                                )}
                            </div>
                            {isDateRange && (
                                <div className="mt-2 text-xs text-gray-500 dark:text-gray-400">
                                    {props.dateRangeLabels?.start || 'Start Date'} → {props.dateRangeLabels?.end || 'End Date'}
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default DatePropertiesSection;

