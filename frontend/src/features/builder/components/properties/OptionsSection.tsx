import React, { useState, useCallback } from 'react';
import { ChevronDown, List, Plus, Trash2, GripVertical, ToggleLeft, Settings2 } from 'lucide-react';
import { PropertyTextInput, PropertyToggle, PropertyNumberInput } from './inputs';
import { ComponentProps, ComponentType } from '../../types/builder.types';

interface OptionsSectionProps {
    props: ComponentProps;
    onPropsChange: (updates: Partial<ComponentProps>) => void;
    componentType: ComponentType;
}

type OptionItem = NonNullable<ComponentProps['options']>[0];

/**
 * OptionsSection - Configuration for Select/Checkbox/Radio options
 * 
 * Features:
 * - Simple mode: Textarea with one option per line
 * - Advanced mode: Visual builder with add/remove/reorder
 * - Default value selection
 * - Option grouping (for Select)
 * - Min/Max selections (for Checkbox)
 */
export const OptionsSection: React.FC<OptionsSectionProps> = ({
    props,
    onPropsChange,
    componentType,
}) => {
    const [isExpanded, setIsExpanded] = useState(true);
    const [editMode, setEditMode] = useState<'simple' | 'advanced'>('simple');
    const [draggedIndex, setDraggedIndex] = useState<number | null>(null);

    const options = props.options || [];
    const isSelect = componentType === 'select' || componentType === 'dropdown';
    const isCheckbox = componentType === 'checkbox';
    const isRadio = componentType === 'radio';

    // Convert options to simple text format
    const optionsToText = useCallback((opts: OptionItem[]): string => {
        return opts.map(o => {
            if (o.group) return `[${o.group}] ${o.label}`;
            if (o.value !== o.label) return `${o.label} = ${o.value}`;
            return o.label;
        }).join('\n');
    }, []);

    // Parse text to options
    const textToOptions = useCallback((text: string): OptionItem[] => {
        return text.split('\n')
            .map(line => line.trim())
            .filter(line => line.length > 0)
            .map(line => {
                // Check for group prefix [Group Name]
                const groupMatch = line.match(/^\[([^\]]+)\]\s*(.+)$/);
                if (groupMatch) {
                    const label = groupMatch[2].trim();
                    return {
                        label,
                        value: label.toLowerCase().replace(/\s+/g, '_'),
                        group: groupMatch[1].trim(),
                    };
                }
                
                // Check for value assignment "Label = value"
                const valueMatch = line.match(/^(.+?)\s*=\s*(.+)$/);
                if (valueMatch) {
                    return {
                        label: valueMatch[1].trim(),
                        value: valueMatch[2].trim(),
                    };
                }
                
                // Simple label (value = lowercase label)
                return {
                    label: line,
                    value: line.toLowerCase().replace(/\s+/g, '_'),
                };
            });
    }, []);

    // Handle simple mode text change
    const handleTextChange = (text: string) => {
        const newOptions = textToOptions(text);
        onPropsChange({ options: newOptions });
    };

    // Add new option
    const addOption = () => {
        const newOption: OptionItem = {
            label: `Option ${options.length + 1}`,
            value: `option_${options.length + 1}`,
        };
        onPropsChange({ options: [...options, newOption] });
    };

    // Remove option
    const removeOption = (index: number) => {
        const newOptions = options.filter((_, i) => i !== index);
        onPropsChange({ options: newOptions });
    };

    // Update option
    const updateOption = (index: number, updates: Partial<OptionItem>) => {
        const newOptions = options.map((opt, i) => 
            i === index ? { ...opt, ...updates } : opt
        );
        onPropsChange({ options: newOptions });
    };

    // Drag and drop handlers
    const handleDragStart = (index: number) => {
        setDraggedIndex(index);
    };

    const handleDragOver = (e: React.DragEvent, index: number) => {
        e.preventDefault();
        if (draggedIndex === null || draggedIndex === index) return;
        
        const newOptions = [...options];
        const draggedItem = newOptions[draggedIndex];
        newOptions.splice(draggedIndex, 1);
        newOptions.splice(index, 0, draggedItem);
        
        setDraggedIndex(index);
        onPropsChange({ options: newOptions });
    };

    const handleDragEnd = () => {
        setDraggedIndex(null);
    };

    // Get unique groups for select
    const groups = isSelect 
        ? [...new Set(options.filter(o => o.group).map(o => o.group!))]
        : [];

    return (
        <div className="border-b border-gray-200 dark:border-gray-700">
            {/* Section Header */}
            <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="w-full flex items-center justify-between px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
            >
                <div className="flex items-center gap-2">
                    <List size={14} className="text-purple-500" />
                    <span>Options</span>
                    {options.length > 0 && (
                        <span className="text-xs bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400 px-1.5 py-0.5 rounded">
                            {options.length}
                        </span>
                    )}
                </div>
                <ChevronDown 
                    size={16} 
                    className={`transform transition-transform ${isExpanded ? 'rotate-180' : ''}`} 
                />
            </button>

            {/* Section Content */}
            {isExpanded && (
                <div className="px-4 pb-4 space-y-4">
                    {/* Mode Toggle */}
                    <div className="flex items-center justify-between">
                        <span className="text-xs text-gray-500 dark:text-gray-400">Edit Mode</span>
                        <div className="flex rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
                            <button
                                onClick={() => setEditMode('simple')}
                                className={`px-3 py-1 text-xs ${
                                    editMode === 'simple'
                                        ? 'bg-purple-500 text-white'
                                        : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700'
                                }`}
                            >
                                Simple
                            </button>
                            <button
                                onClick={() => setEditMode('advanced')}
                                className={`px-3 py-1 text-xs border-l border-gray-200 dark:border-gray-700 ${
                                    editMode === 'advanced'
                                        ? 'bg-purple-500 text-white'
                                        : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700'
                                }`}
                            >
                                Advanced
                            </button>
                        </div>
                    </div>

                    {/* Simple Mode */}
                    {editMode === 'simple' && (
                        <div className="space-y-2">
                            <textarea
                                value={optionsToText(options)}
                                onChange={(e) => handleTextChange(e.target.value)}
                                placeholder={`Option 1\nOption 2\nOption 3${isSelect ? '\n\n[Group] Grouped Option' : ''}`}
                                className="w-full h-32 px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg 
                                    bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200
                                    focus:ring-2 focus:ring-purple-500 focus:border-purple-500 resize-y"
                            />
                            <div className="text-xs text-gray-400 dark:text-gray-500 space-y-1">
                                <div>• One option per line</div>
                                <div>• Use <code className="bg-gray-100 dark:bg-gray-700 px-1 rounded">Label = value</code> for custom values</div>
                                {isSelect && (
                                    <div>• Use <code className="bg-gray-100 dark:bg-gray-700 px-1 rounded">[Group] Label</code> for grouping</div>
                                )}
                            </div>
                        </div>
                    )}

                    {/* Advanced Mode */}
                    {editMode === 'advanced' && (
                        <div className="space-y-2">
                            {/* Options List */}
                            <div className="space-y-1 max-h-64 overflow-y-auto">
                                {options.map((option, index) => (
                                    <div
                                        key={index}
                                        draggable
                                        onDragStart={() => handleDragStart(index)}
                                        onDragOver={(e) => handleDragOver(e, index)}
                                        onDragEnd={handleDragEnd}
                                        className={`flex items-center gap-2 p-2 bg-gray-50 dark:bg-gray-800 rounded-lg border ${
                                            draggedIndex === index
                                                ? 'border-purple-500 opacity-50'
                                                : 'border-transparent'
                                        }`}
                                    >
                                        {/* Drag Handle */}
                                        <div className="cursor-grab text-gray-400 hover:text-gray-600">
                                            <GripVertical size={14} />
                                        </div>

                                        {/* Label Input */}
                                        <input
                                            type="text"
                                            value={option.label}
                                            onChange={(e) => updateOption(index, { 
                                                label: e.target.value,
                                                value: e.target.value.toLowerCase().replace(/\s+/g, '_'),
                                            })}
                                            placeholder="Label"
                                            className="flex-1 px-2 py-1 text-sm border border-gray-200 dark:border-gray-600 rounded
                                                bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-200"
                                        />

                                        {/* Value Input (collapsed by default) */}
                                        <input
                                            type="text"
                                            value={option.value}
                                            onChange={(e) => updateOption(index, { value: e.target.value })}
                                            placeholder="value"
                                            className="w-24 px-2 py-1 text-xs border border-gray-200 dark:border-gray-600 rounded
                                                bg-white dark:bg-gray-700 text-gray-600 dark:text-gray-400 font-mono"
                                        />

                                        {/* Group Input (Select only) */}
                                        {isSelect && (
                                            <input
                                                type="text"
                                                value={option.group || ''}
                                                onChange={(e) => updateOption(index, { group: e.target.value || undefined })}
                                                placeholder="Group"
                                                className="w-20 px-2 py-1 text-xs border border-gray-200 dark:border-gray-600 rounded
                                                    bg-white dark:bg-gray-700 text-gray-600 dark:text-gray-400"
                                                list={`groups-${index}`}
                                            />
                                        )}
                                        {isSelect && groups.length > 0 && (
                                            <datalist id={`groups-${index}`}>
                                                {groups.map(g => <option key={g} value={g} />)}
                                            </datalist>
                                        )}

                                        {/* Disabled Toggle */}
                                        <button
                                            onClick={() => updateOption(index, { disabled: !option.disabled })}
                                            className={`p-1 rounded ${
                                                option.disabled
                                                    ? 'text-amber-500 bg-amber-50 dark:bg-amber-900/20'
                                                    : 'text-gray-400 hover:text-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700'
                                            }`}
                                            title={option.disabled ? 'Disabled' : 'Click to disable'}
                                        >
                                            <ToggleLeft size={14} />
                                        </button>

                                        {/* Delete Button */}
                                        <button
                                            onClick={() => removeOption(index)}
                                            className="p-1 text-gray-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded"
                                        >
                                            <Trash2 size={14} />
                                        </button>
                                    </div>
                                ))}
                            </div>

                            {/* Add Button */}
                            <button
                                onClick={addOption}
                                className="w-full flex items-center justify-center gap-2 py-2 text-sm text-purple-600 dark:text-purple-400
                                    border border-dashed border-purple-300 dark:border-purple-700 rounded-lg
                                    hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors"
                            >
                                <Plus size={14} />
                                Add Option
                            </button>
                        </div>
                    )}

                    {/* Default Value */}
                    {(isSelect || isRadio) && options.length > 0 && (
                        <div className="pt-3 border-t border-gray-100 dark:border-gray-800">
                            <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">
                                Default Value
                            </label>
                            <select
                                value={props.defaultValue || ''}
                                onChange={(e) => onPropsChange({ defaultValue: e.target.value || undefined })}
                                className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg
                                    bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200
                                    focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                            >
                                <option value="">No default</option>
                                {options.map((opt, i) => (
                                    <option key={i} value={opt.value}>{opt.label}</option>
                                ))}
                            </select>
                        </div>
                    )}

                    {/* Checkbox-specific: Default Checked */}
                    {isCheckbox && options.length > 0 && (
                        <div className="pt-3 border-t border-gray-100 dark:border-gray-800 space-y-2">
                            <label className="block text-xs font-medium text-gray-500 dark:text-gray-400">
                                Default Checked
                            </label>
                            <div className="space-y-1">
                                {options.map((opt, i) => (
                                    <label key={i} className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
                                        <input
                                            type="checkbox"
                                            checked={props.defaultChecked?.includes(opt.value) ?? false}
                                            onChange={(e) => {
                                                const current = props.defaultChecked || [];
                                                const newChecked = e.target.checked
                                                    ? [...current, opt.value]
                                                    : current.filter(v => v !== opt.value);
                                                onPropsChange({ defaultChecked: newChecked.length > 0 ? newChecked : undefined });
                                            }}
                                            className="rounded border-gray-300 text-purple-500 focus:ring-purple-500"
                                        />
                                        {opt.label}
                                    </label>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Select-specific Options */}
                    {isSelect && (
                        <div className="pt-3 border-t border-gray-100 dark:border-gray-800 space-y-3">
                            <PropertyToggle
                                label="Allow Empty Selection"
                                checked={props.allowEmpty ?? true}
                                onChange={(checked) => onPropsChange({ allowEmpty: checked })}
                                helpText="Show 'Select...' placeholder option"
                            />

                            {props.allowEmpty !== false && (
                                <PropertyTextInput
                                    label="Empty Placeholder"
                                    value={props.emptyPlaceholder || ''}
                                    onChange={(value) => onPropsChange({ emptyPlaceholder: value || undefined })}
                                    placeholder="Select an option..."
                                    helpText="Text shown when nothing selected"
                                />
                            )}

                            <PropertyToggle
                                label="Searchable"
                                checked={props.searchable ?? false}
                                onChange={(checked) => onPropsChange({ searchable: checked || undefined })}
                                helpText="Enable search/filter in dropdown"
                            />

                            <PropertyToggle
                                label="Allow Other"
                                checked={props.allowOther ?? false}
                                onChange={(checked) => onPropsChange({ allowOther: checked || undefined })}
                                helpText="Add 'Other' option with free text"
                            />

                            {props.allowOther && (
                                <PropertyTextInput
                                    label="Other Placeholder"
                                    value={props.otherPlaceholder || ''}
                                    onChange={(value) => onPropsChange({ otherPlaceholder: value || undefined })}
                                    placeholder="Please specify..."
                                    helpText="Placeholder for 'Other' input"
                                />
                            )}
                        </div>
                    )}

                    {/* Checkbox-specific Options */}
                    {isCheckbox && (
                        <div className="pt-3 border-t border-gray-100 dark:border-gray-800 space-y-3">
                            <div className="grid grid-cols-2 gap-3">
                                <PropertyNumberInput
                                    label="Min Selections"
                                    value={props.minSelections ?? 0}
                                    onChange={(value) => onPropsChange({ minSelections: value || undefined })}
                                    min={0}
                                    max={options.length}
                                    helpText="Required minimum"
                                />
                                <PropertyNumberInput
                                    label="Max Selections"
                                    value={props.maxSelections ?? 0}
                                    onChange={(value) => onPropsChange({ maxSelections: value || undefined })}
                                    min={0}
                                    max={options.length}
                                    helpText="Allowed maximum"
                                />
                            </div>

                            <div>
                                <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">
                                    Layout Direction
                                </label>
                                <div className="flex gap-2">
                                    <button
                                        onClick={() => onPropsChange({ optionsDirection: 'vertical' })}
                                        className={`flex-1 py-2 text-xs rounded-lg border ${
                                            (props.optionsDirection || 'vertical') === 'vertical'
                                                ? 'bg-purple-500 text-white border-purple-500'
                                                : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-400 border-gray-200 dark:border-gray-700'
                                        }`}
                                    >
                                        Vertical
                                    </button>
                                    <button
                                        onClick={() => onPropsChange({ optionsDirection: 'horizontal' })}
                                        className={`flex-1 py-2 text-xs rounded-lg border ${
                                            props.optionsDirection === 'horizontal'
                                                ? 'bg-purple-500 text-white border-purple-500'
                                                : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-400 border-gray-200 dark:border-gray-700'
                                        }`}
                                    >
                                        Horizontal
                                    </button>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Radio-specific Options */}
                    {isRadio && (
                        <div className="pt-3 border-t border-gray-100 dark:border-gray-800">
                            <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">
                                Layout Direction
                            </label>
                            <div className="flex gap-2">
                                <button
                                    onClick={() => onPropsChange({ optionsDirection: 'vertical' })}
                                    className={`flex-1 py-2 text-xs rounded-lg border ${
                                        (props.optionsDirection || 'vertical') === 'vertical'
                                            ? 'bg-purple-500 text-white border-purple-500'
                                            : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-400 border-gray-200 dark:border-gray-700'
                                    }`}
                                >
                                    Vertical
                                </button>
                                <button
                                    onClick={() => onPropsChange({ optionsDirection: 'horizontal' })}
                                    className={`flex-1 py-2 text-xs rounded-lg border ${
                                        props.optionsDirection === 'horizontal'
                                            ? 'bg-purple-500 text-white border-purple-500'
                                            : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-400 border-gray-200 dark:border-gray-700'
                                    }`}
                                >
                                    Horizontal
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default OptionsSection;

