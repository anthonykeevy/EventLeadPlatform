import React, { useState, useMemo, useEffect, useRef } from 'react';
import { 
    ChevronDown, ChevronRight, AlertTriangle, Info, Lock, FlaskConical, 
    CheckCircle, XCircle, Sparkles, Shield, Settings2, Type, Hash, Calendar, AtSign, Phone 
} from 'lucide-react';
import { PropertyTextInput, PropertyNumberInput, PropertyToggle, PropertySelect } from './inputs';
import { ValidationRules, ComponentType } from '../../types/builder.types';
import { getDisabledRules, validateRuleConsistency, DisabledRule } from '../../utils/validationConflicts';
import { getRuleEducationalInfo, getCountryOptions, getDomainFieldInfo, getMustMatchFieldInfo, getBlockedCharactersInfo } from '../../data/validationRuleSeed';
import { InfoTooltip } from '../ui/InfoTooltip';
import { validateField } from '../../utils/validationEngine';

/** Available field for Must Match dropdown */
interface AvailableField {
    id: string;
    label: string;
    exportName?: string;
    type?: string;
}

interface ValidationSectionProps {
    validation: ValidationRules | undefined;
    onValidationChange: (updates: Partial<ValidationRules>) => void;
    componentType: ComponentType;
    componentId?: string;
    availableFields?: AvailableField[];
}

// ═══════════════════════════════════════════════════════════════════════════════
// RULE VISIBILITY CONFIG - which rules to show per component type
// ═══════════════════════════════════════════════════════════════════════════════
const HIDDEN_RULES: Record<string, string[]> = {
    // Email: hide character rules, length rules, formatting (inherent in email format)
    email: ['alpha', 'alphanumeric', 'blockedCharacters', 'minLength', 'maxLength', 
            'caseTransform', 'noConsecutiveSpaces', 'trimWhitespace', 'pattern', 'mustMatchField'],
    // Number: hide all text-related rules
    number: ['alpha', 'alphanumeric', 'blockedCharacters', 'minLength', 'maxLength',
             'caseTransform', 'noConsecutiveSpaces', 'trimWhitespace', 'pattern', 'noHtmlScript',
             'email', 'phone', 'mustMatchField'],
    // Phone: hide all text-related rules
    phone: ['alpha', 'alphanumeric', 'blockedCharacters', 'minLength', 'maxLength',
            'caseTransform', 'noConsecutiveSpaces', 'trimWhitespace', 'pattern', 'noHtmlScript',
            'email'],
    // Date: hide all text-related rules
    date: ['alpha', 'alphanumeric', 'blockedCharacters', 'minLength', 'maxLength',
           'caseTransform', 'noConsecutiveSpaces', 'trimWhitespace', 'pattern', 'noHtmlScript',
           'email', 'phone', 'mustMatchField'],
    // Select/Checkbox/Radio: only show selection limits
    select: ['all-text-rules'],
    checkbox: ['all-text-rules'],
    radio: ['all-text-rules'],
};

// Check if a rule should be hidden for this component type
const _isRuleHidden = (ruleKey: string, componentType: string): boolean => {
    const hidden = HIDDEN_RULES[componentType];
    if (!hidden) return false;
    if (hidden.includes('all-text-rules')) return true; // Selection types hide everything
    return hidden.includes(ruleKey);
};

/**
 * Wrapper for validation controls that shows disabled state with INLINE explanation
 */
const ValidationControl: React.FC<{
    ruleKey: string;
    disabledRules: Map<string, DisabledRule>;
    children: React.ReactNode;
}> = ({ ruleKey, disabledRules, children }) => {
    const disabled = disabledRules.get(ruleKey);
    
    if (disabled) {
        return (
            <div className="relative">
                <div className="opacity-40 pointer-events-none">
                    {children}
                </div>
                {/* Inline explanation instead of just hover */}
                <div className="flex items-center gap-1.5 mt-1 text-[10px] text-gray-500 dark:text-gray-400 italic">
                    <Lock size={10} className="text-gray-400" />
                    <span>Disabled: {disabled.reason}</span>
                </div>
            </div>
        );
    }
    
    return <>{children}</>;
};

/**
 * Rule label with optional info tooltip
 */
const RuleLabel: React.FC<{
    label: string;
    ruleKey: string;
}> = ({ label, ruleKey }) => {
    const info = getRuleEducationalInfo(ruleKey);
    
    return (
        <div className="flex items-center gap-1.5">
            <span>{label}</span>
            {info && <InfoTooltip info={info} size={12} />}
        </div>
    );
};

/**
 * Collapsible Tier Component - groups related rules with visual distinction
 */
const CollapsibleTier: React.FC<{
    title: string;
    icon: React.ElementType;
    iconColor: string;
    bgColor?: string;
    defaultOpen?: boolean;
    children: React.ReactNode;
    badge?: React.ReactNode;
}> = ({ title, icon: Icon, iconColor, bgColor = '', defaultOpen = true, children, badge }) => {
    const [isExpanded, setIsExpanded] = useState(defaultOpen);

    return (
        <div className={`rounded-lg overflow-hidden ${bgColor}`}>
            <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="w-full flex items-center justify-between px-3 py-2 text-xs font-medium 
                    text-gray-600 dark:text-gray-400 hover:bg-black/5 dark:hover:bg-white/5"
            >
                <div className="flex items-center gap-2">
                    {isExpanded ? <ChevronDown size={12} /> : <ChevronRight size={12} />}
                    <Icon size={12} className={iconColor} />
                    <span>{title}</span>
                    {badge}
                </div>
            </button>
            {isExpanded && (
                <div className="px-3 pb-3 space-y-3">
                    {children}
                </div>
            )}
        </div>
    );
};

/**
 * Mini Validation Tester Component
 */
const ValidationTester: React.FC<{
    validation: ValidationRules;
    componentType: string;
    componentId?: string;
}> = ({ validation, componentType, componentId }) => {
    const [testValue, setTestValue] = useState('');
    const [selectedCountry, setSelectedCountry] = useState('AU');
    const [isExpanded, setIsExpanded] = useState(false);
    const prevComponentIdRef = useRef(componentId);
    
    const countryOptions = useMemo(() => getCountryOptions(), []);
    
    useEffect(() => {
        if (prevComponentIdRef.current !== componentId) {
            setTestValue('');
            prevComponentIdRef.current = componentId;
        }
    }, [componentId]);
    
    const result = useMemo(() => {
        if (!testValue) return null;
        return validateField(testValue, validation, componentType, {
            countryCode: selectedCountry,
        });
    }, [testValue, validation, componentType, selectedCountry]);

    const getInputType = () => {
        switch (componentType) {
            case 'email': return 'email';
            case 'number': return 'number';
            case 'date': return 'date';
            default: return 'text';
        }
    };

    return (
        <div className="border border-dashed border-purple-300 dark:border-purple-600 rounded-lg overflow-hidden bg-purple-50/30 dark:bg-purple-900/10">
            <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="w-full flex items-center justify-between px-3 py-2 text-xs font-medium 
                    text-purple-700 dark:text-purple-300 hover:bg-purple-100/50 dark:hover:bg-purple-900/30"
            >
                <div className="flex items-center gap-2">
                    <FlaskConical size={12} className="text-purple-500" />
                    <span>Test Validation Rules</span>
                </div>
                <ChevronDown 
                    size={14} 
                    className={`transform transition-transform ${isExpanded ? 'rotate-180' : ''}`} 
                />
            </button>

            {isExpanded && (
                <div className="px-3 pb-3 space-y-3">
                    <div>
                        <label className="block text-xs text-gray-500 dark:text-gray-400 mb-1">
                            Enter test value:
                        </label>
                        <input
                            type={getInputType()}
                            value={testValue}
                            onChange={(e) => setTestValue(e.target.value)}
                            placeholder={`Test ${componentType} value...`}
                            className="w-full px-2 py-1.5 text-sm border border-gray-300 dark:border-gray-600 
                                rounded bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200
                                focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                        />
                    </div>

                    {componentType === 'phone' && (
                        <div>
                            <label className="block text-xs text-gray-500 dark:text-gray-400 mb-1">
                                Test Country:
                            </label>
                            <select
                                value={selectedCountry}
                                onChange={(e) => setSelectedCountry(e.target.value)}
                                className="w-full px-2 py-1.5 text-sm border border-gray-300 dark:border-gray-600 
                                    rounded bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200"
                            >
                                {countryOptions.map(opt => (
                                    <option key={opt.value} value={opt.value}>{opt.label}</option>
                                ))}
                            </select>
                            <p className="text-xs text-gray-400 mt-1">
                                In live form: uses Event timezone setting
                            </p>
                        </div>
                    )}

                    {result && (
                        <div className="space-y-2">
                            <div className={`flex items-center gap-2 p-2 rounded text-sm ${
                                result.isValid 
                                    ? 'bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400'
                                    : 'bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400'
                            }`}>
                                {result.isValid ? (
                                    <>
                                        <CheckCircle size={14} />
                                        <span>Valid</span>
                                    </>
                                ) : (
                                    <>
                                        <XCircle size={14} />
                                        <span>Invalid</span>
                                    </>
                                )}
                            </div>

                            {result.errors.length > 0 && (
                                <div className="text-xs text-red-600 dark:text-red-400 space-y-1">
                                    {result.errors.map((err, i) => (
                                        <div key={i} className="flex items-start gap-1.5">
                                            <span className="text-red-500 mt-0.5">•</span>
                                            <span>{err.message}</span>
                                        </div>
                                    ))}
                                </div>
                            )}

                            {result.autoFixesApplied && result.autoFixesApplied.length > 0 && (
                                <div className="text-xs text-purple-600 dark:text-purple-400 bg-purple-50 dark:bg-purple-900/20 p-2 rounded">
                                    <div className="flex items-center gap-1.5 font-medium mb-1">
                                        <Sparkles size={12} />
                                        <span>Auto-fixed:</span>
                                    </div>
                                    {result.autoFixesApplied.map((fix, i) => (
                                        <div key={i} className="ml-4">
                                            • {fix.description}
                                        </div>
                                    ))}
                                    {result.sanitizedValue !== testValue && (
                                        <div className="mt-1 font-mono">
                                            Result: "{result.sanitizedValue}"
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>
                    )}

                    {!testValue && (
                        <div className="text-xs text-gray-400 dark:text-gray-500 italic">
                            Enter a value above to test your validation rules
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

const parseDomainInput = (value: string): string[] => {
    return value
        .split(',')
        .map(s => s.trim().toLowerCase())
        .filter(s => s.length > 0);
};

export const ValidationSection: React.FC<ValidationSectionProps> = ({
    validation = {},
    onValidationChange,
    componentType,
    componentId,
    availableFields = [],
}) => {
    const [isExpanded, setIsExpanded] = React.useState(false);

    const disabledRules = getDisabledRules(validation, componentType);
    const warnings = validateRuleConsistency(validation, componentType);

    const activeRuleCount = Object.entries(validation).filter(([_, value]) => {
        if (value === undefined || value === null || value === false) return false;
        if (typeof value === 'string' && value === '') return false;
        if (Array.isArray(value) && value.length === 0) return false;
        return true;
    }).length;

    const isTextType = ['text', 'textarea', 'first-name'].includes(componentType);
    const isNumberType = componentType === 'number';
    const isEmailType = componentType === 'email';
    const isPhoneType = componentType === 'phone';
    const isDateType = componentType === 'date';
    const isSelectionType = ['select', 'checkbox', 'radio'].includes(componentType);

    // ═══════════════════════════════════════════════════════════════════════════════
    // AUTO-CASCADE LOGIC: Auto-disable/update related rules
    // ═══════════════════════════════════════════════════════════════════════════════
    useEffect(() => {
        const updates: Partial<ValidationRules> = {};
        
        // When Min Value > 0, non-zero is implied
        if (validation.minValue !== undefined && validation.minValue > 0 && validation.nonZero) {
            updates.nonZero = undefined;
        }
        
        // When Positive Only, Non-Negative is implied
        if (validation.positiveOnly && validation.nonNegative) {
            updates.nonNegative = undefined;
        }
        
        // When Integer Only, decimal precision is irrelevant
        if (validation.integerOnly && validation.decimalPrecision !== undefined) {
            updates.decimalPrecision = undefined;
        }
        
        // When Future Only, set min date to today
        if (validation.futureOnly && validation.minDate !== 'today') {
            updates.minDate = 'today';
        }
        
        // When Minimum Age set, implies Past Only
        if (validation.minimumAge !== undefined && validation.minimumAge > 0 && !validation.pastOnly) {
            updates.pastOnly = true;
            updates.futureOnly = undefined;
        }
        
        // Apply updates if any
        if (Object.keys(updates).length > 0) {
            onValidationChange(updates);
        }
    }, [
        validation.minValue, validation.nonZero, validation.positiveOnly, 
        validation.nonNegative, validation.integerOnly, validation.decimalPrecision,
        validation.futureOnly, validation.minDate, validation.minimumAge, validation.pastOnly
    ]);

    return (
        <div className="border-b border-gray-200 dark:border-gray-700">
            {/* Section Header */}
            <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="w-full flex items-center justify-between px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
            >
                <div className="flex items-center gap-2">
                    <Shield size={14} className="text-amber-500" />
                    <span>Validation Rules</span>
                    {activeRuleCount > 0 && (
                        <span className="text-xs bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400 px-1.5 py-0.5 rounded">
                            {activeRuleCount} active
                        </span>
                    )}
                </div>
                <ChevronDown 
                    size={16} 
                    className={`transform transition-transform ${isExpanded ? 'rotate-180' : ''}`} 
                />
            </button>

            {isExpanded && (
                <div className="px-4 pb-4 space-y-3">
                    {/* Warnings */}
                    {warnings.length > 0 && (
                        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-3">
                            <div className="flex items-start gap-2">
                                <AlertTriangle size={14} className="text-red-500 mt-0.5 flex-shrink-0" />
                                <div className="text-xs text-red-600 dark:text-red-400 space-y-1">
                                    {warnings.map((warning, i) => (
                                        <div key={i}>{warning}</div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    )}

                    {/* ═══════════════════════════════════════════════════════════════ */}
                    {/* SELECTION TYPE (Checkbox, Radio, Select) - Only show selection rules */}
                    {/* ═══════════════════════════════════════════════════════════════ */}
                    {isSelectionType && (
                        <CollapsibleTier
                            title="Selection Limits"
                            icon={Settings2}
                            iconColor="text-blue-500"
                            bgColor="bg-blue-50/50 dark:bg-blue-900/10"
                        >
                            <div className="grid grid-cols-2 gap-3">
                                <PropertyNumberInput
                                    label={<RuleLabel label="Min Selections" ruleKey="minSelections" />}
                                    value={validation.minSelections ?? 0}
                                    onChange={(value) => onValidationChange({ minSelections: value || undefined })}
                                    min={0}
                                    max={100}
                                    helpText="Minimum options to select"
                                />
                                <PropertyNumberInput
                                    label={<RuleLabel label="Max Selections" ruleKey="maxSelections" />}
                                    value={validation.maxSelections ?? 0}
                                    onChange={(value) => onValidationChange({ maxSelections: value || undefined })}
                                    min={0}
                                    max={100}
                                    helpText="Maximum options allowed"
                                />
                            </div>
                        </CollapsibleTier>
                    )}

                    {/* ═══════════════════════════════════════════════════════════════ */}
                    {/* TEXT VALIDATION RULES */}
                    {/* ═══════════════════════════════════════════════════════════════ */}
                    {isTextType && (
                        <>
                            {/* TIER 1: Primary Constraints (always visible, no background) */}
                            <CollapsibleTier
                                title="Primary Constraints"
                                icon={Type}
                                iconColor="text-blue-500"
                            >
                                {/* Character Rules - ordered most restrictive first */}
                                <div className="space-y-2 mb-4">
                                    <div className="text-[10px] uppercase tracking-wide text-gray-400 font-medium">Character Type</div>
                                    
                                    <ValidationControl ruleKey="alpha" disabledRules={disabledRules}>
                                        <PropertyToggle
                                            label={<RuleLabel label="Letters Only (A-Z)" ruleKey="alpha" />}
                                            checked={validation.alpha ?? false}
                                            onChange={(checked) => onValidationChange({ 
                                                alpha: checked || undefined,
                                                alphanumeric: checked ? undefined : validation.alphanumeric 
                                            })}
                                            helpText="Most restrictive - letters only"
                                        />
                                    </ValidationControl>
                                    
                                    <ValidationControl ruleKey="alphanumeric" disabledRules={disabledRules}>
                                        <PropertyToggle
                                            label={<RuleLabel label="Alphanumeric (A-Z, 0-9)" ruleKey="alphanumeric" />}
                                            checked={validation.alphanumeric ?? false}
                                            onChange={(checked) => onValidationChange({ alphanumeric: checked || undefined })}
                                            helpText="Letters and numbers, no special chars"
                                        />
                                    </ValidationControl>

                                    <ValidationControl ruleKey="blockedCharacters" disabledRules={disabledRules}>
                                        <div>
                                            <div className="flex items-center gap-1.5 mb-1">
                                                <span className="text-xs font-medium text-gray-700 dark:text-gray-300">Blocked Characters</span>
                                                <InfoTooltip info={getBlockedCharactersInfo()} size={12} />
                                            </div>
                                            <PropertyTextInput
                                                label=""
                                                value={validation.blockedCharacters || ''}
                                                onChange={(value) => onValidationChange({ blockedCharacters: value || undefined })}
                                                placeholder="<>{}[]\/"
                                                helpText="Type characters to block (no separator needed)"
                                            />
                                        </div>
                                    </ValidationControl>
                                </div>

                                {/* Length Constraints */}
                                <div className="space-y-2">
                                    <div className="text-[10px] uppercase tracking-wide text-gray-400 font-medium">Length</div>
                                    <div className="grid grid-cols-2 gap-3">
                                        <PropertyNumberInput
                                            label={<RuleLabel label="Min Length" ruleKey="minLength" />}
                                            value={validation.minLength ?? 0}
                                            onChange={(value) => onValidationChange({ minLength: value || undefined })}
                                            min={0}
                                            max={10000}
                                            helpText="Minimum characters"
                                        />
                                        <PropertyNumberInput
                                            label={<RuleLabel label="Max Length" ruleKey="maxLength" />}
                                            value={validation.maxLength ?? 0}
                                            onChange={(value) => onValidationChange({ maxLength: value || undefined })}
                                            min={0}
                                            max={10000}
                                            helpText="Maximum characters"
                                        />
                                    </div>
                                </div>
                            </CollapsibleTier>

                            {/* TIER 2: Auto-Fix & Formatting (light gray bg) */}
                            <CollapsibleTier
                                title="Auto-Fix & Formatting"
                                icon={Sparkles}
                                iconColor="text-purple-500"
                                bgColor="bg-gray-50 dark:bg-gray-800/50"
                            >
                                <ValidationControl ruleKey="trimWhitespace" disabledRules={disabledRules}>
                                    <PropertyToggle
                                        label={<RuleLabel label="Trim Whitespace" ruleKey="trimWhitespace" />}
                                        checked={validation.trimWhitespace ?? true}
                                        onChange={(checked) => onValidationChange({ trimWhitespace: checked })}
                                        helpText="Auto-remove leading/trailing spaces"
                                    />
                                </ValidationControl>

                                <ValidationControl ruleKey="noConsecutiveSpaces" disabledRules={disabledRules}>
                                    <PropertyToggle
                                        label={<RuleLabel label="No Consecutive Spaces" ruleKey="noConsecutiveSpaces" />}
                                        checked={validation.noConsecutiveSpaces ?? false}
                                        onChange={(checked) => onValidationChange({ noConsecutiveSpaces: checked || undefined })}
                                        helpText="Collapse double spaces to single"
                                    />
                                </ValidationControl>

                                <PropertySelect
                                    label={<RuleLabel label="Case Transform" ruleKey="caseTransform" />}
                                    value={validation.caseTransform || ''}
                                    onChange={(value) => onValidationChange({ caseTransform: (value as ValidationRules['caseTransform']) || undefined })}
                                    options={[
                                        { value: '', label: 'None' },
                                        { value: 'uppercase', label: 'UPPERCASE' },
                                        { value: 'lowercase', label: 'lowercase' },
                                        { value: 'titlecase', label: 'Title Case' },
                                    ]}
                                    helpText="Auto-convert text case"
                                />
                            </CollapsibleTier>

                            {/* TIER 3: Security (amber bg - draws attention) */}
                            <CollapsibleTier
                                title="Security"
                                icon={Shield}
                                iconColor="text-amber-500"
                                bgColor="bg-amber-50/50 dark:bg-amber-900/10"
                            >
                                <PropertyToggle
                                    label={<RuleLabel label="No HTML/Script" ruleKey="noHtmlScript" />}
                                    checked={validation.noHtmlScript ?? true}
                                    onChange={(checked) => onValidationChange({ noHtmlScript: checked })}
                                    helpText="Block HTML tags and scripts"
                                />
                                {validation.noHtmlScript === false && (
                                    <div className="text-xs text-amber-700 dark:text-amber-300 bg-amber-100 dark:bg-amber-900/30 p-2 rounded flex items-start gap-1.5 border border-amber-200 dark:border-amber-800">
                                        <AlertTriangle size={12} className="mt-0.5 flex-shrink-0" />
                                        <span>
                                            <strong>Security Warning:</strong> Disabling this may expose your form to security vulnerabilities.
                                            Only disable if you need to collect code snippets.
                                        </span>
                                    </div>
                                )}
                            </CollapsibleTier>

                            {/* TIER 4: Advanced (blue bg - collapsed by default) */}
                            <CollapsibleTier
                                title="Advanced"
                                icon={Settings2}
                                iconColor="text-blue-500"
                                bgColor="bg-blue-50/50 dark:bg-blue-900/10"
                                defaultOpen={false}
                            >
                                <ValidationControl ruleKey="mustMatchField" disabledRules={disabledRules}>
                                    <div>
                                        <div className="flex items-center gap-1.5 mb-1">
                                            <span className="text-xs font-medium text-gray-700 dark:text-gray-300">Must Match Field</span>
                                            <InfoTooltip info={getMustMatchFieldInfo()} size={12} />
                                        </div>
                                        {availableFields.length > 0 ? (
                                            <select
                                                value={validation.mustMatchField || ''}
                                                onChange={(e) => onValidationChange({ mustMatchField: e.target.value || undefined })}
                                                className="w-full px-2 py-1.5 text-sm border border-gray-300 dark:border-gray-600 
                                                    rounded bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200
                                                    focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                            >
                                                <option value="">-- Select a field to match --</option>
                                                {availableFields.map(field => (
                                                    <option key={field.id} value={field.exportName || field.label}>
                                                        {field.label} {field.type ? `(${field.type})` : ''}
                                                    </option>
                                                ))}
                                            </select>
                                        ) : (
                                            <div className="text-xs text-gray-400 italic py-2 bg-gray-100 dark:bg-gray-800 rounded px-2">
                                                (No compatible fields on canvas)
                                            </div>
                                        )}
                                        <p className="text-xs text-gray-500 mt-1">
                                            Value must exactly match the selected field
                                        </p>
                                    </div>
                                </ValidationControl>

                                <ValidationControl ruleKey="pattern" disabledRules={disabledRules}>
                                    <PropertyTextInput
                                        label={<RuleLabel label="Custom Pattern (Regex)" ruleKey="pattern" />}
                                        value={validation.pattern || ''}
                                        onChange={(value) => onValidationChange({ pattern: value || undefined })}
                                        placeholder="^[A-Za-z]+$"
                                        helpText="Unicode-aware regex pattern"
                                    />
                                </ValidationControl>

                                {/* Custom Error Message - grouped with pattern */}
                                <PropertyTextInput
                                    label="Custom Error Message"
                                    value={validation.customError || ''}
                                    onChange={(value) => onValidationChange({ customError: value || undefined })}
                                    placeholder="Please enter a valid value..."
                                    helpText="Shown when any validation fails"
                                />
                            </CollapsibleTier>
                        </>
                    )}

                    {/* ═══════════════════════════════════════════════════════════════ */}
                    {/* NUMBER VALIDATION RULES */}
                    {/* ═══════════════════════════════════════════════════════════════ */}
                    {isNumberType && (
                        <>
                            {/* Primary Constraints */}
                            <CollapsibleTier
                                title="Range & Sign"
                                icon={Hash}
                                iconColor="text-blue-500"
                            >
                                {/* Enumeration - most restrictive, shown first */}
                                <ValidationControl ruleKey="allowedValues" disabledRules={disabledRules}>
                                    <PropertyTextInput
                                        label={<RuleLabel label="Allowed Values (exact)" ruleKey="allowedValues" />}
                                        value={validation.allowedValues?.join(', ') || ''}
                                        onChange={(value) => {
                                            const nums = value
                                                .split(',')
                                                .map(s => parseFloat(s.trim()))
                                                .filter(n => !isNaN(n));
                                            onValidationChange({ allowedValues: nums.length > 0 ? nums : undefined });
                                        }}
                                        placeholder="1, 5, 10, 25, 50, 100"
                                        helpText="Most restrictive: only these values allowed"
                                    />
                                </ValidationControl>

                                {/* Min/Max Range */}
                                <div className="grid grid-cols-2 gap-3">
                                    <ValidationControl ruleKey="minValue" disabledRules={disabledRules}>
                                        <PropertyNumberInput
                                            label={<RuleLabel label="Min Value" ruleKey="minValue" />}
                                            value={validation.minValue ?? 0}
                                            onChange={(value) => onValidationChange({ minValue: value })}
                                            min={-9999999}
                                            max={9999999}
                                            helpText="Minimum allowed"
                                        />
                                    </ValidationControl>
                                    <ValidationControl ruleKey="maxValue" disabledRules={disabledRules}>
                                        <PropertyNumberInput
                                            label={<RuleLabel label="Max Value" ruleKey="maxValue" />}
                                            value={validation.maxValue ?? 0}
                                            onChange={(value) => onValidationChange({ maxValue: value })}
                                            min={-9999999}
                                            max={9999999}
                                            helpText="Maximum allowed"
                                        />
                                    </ValidationControl>
                                </div>

                                {/* Sign Constraints - ordered by restrictiveness */}
                                <ValidationControl ruleKey="positiveOnly" disabledRules={disabledRules}>
                                    <PropertyToggle
                                        label={<RuleLabel label="Positive Only (> 0)" ruleKey="positiveOnly" />}
                                        checked={validation.positiveOnly ?? false}
                                        onChange={(checked) => onValidationChange({ positiveOnly: checked || undefined })}
                                        helpText="Must be greater than zero"
                                    />
                                </ValidationControl>

                                <ValidationControl ruleKey="nonNegative" disabledRules={disabledRules}>
                                    <PropertyToggle
                                        label="Non-Negative (>= 0)"
                                        checked={validation.nonNegative ?? false}
                                        onChange={(checked) => onValidationChange({ nonNegative: checked || undefined })}
                                        helpText="Zero or positive only"
                                    />
                                </ValidationControl>

                                <ValidationControl ruleKey="nonZero" disabledRules={disabledRules}>
                                    <PropertyToggle
                                        label="Non-Zero"
                                        checked={validation.nonZero ?? false}
                                        onChange={(checked) => onValidationChange({ nonZero: checked || undefined })}
                                        helpText="Cannot be exactly zero"
                                    />
                                </ValidationControl>
                            </CollapsibleTier>

                            {/* Type Constraints */}
                            <CollapsibleTier
                                title="Number Type"
                                icon={Settings2}
                                iconColor="text-purple-500"
                                bgColor="bg-gray-50 dark:bg-gray-800/50"
                            >
                                <ValidationControl ruleKey="integerOnly" disabledRules={disabledRules}>
                                    <PropertyToggle
                                        label={<RuleLabel label="Integer Only (no decimals)" ruleKey="integerOnly" />}
                                        checked={validation.integerOnly ?? false}
                                        onChange={(checked) => onValidationChange({ integerOnly: checked || undefined })}
                                        helpText="Whole numbers only"
                                    />
                                </ValidationControl>

                                <ValidationControl ruleKey="decimalPrecision" disabledRules={disabledRules}>
                                    <PropertyNumberInput
                                        label="Decimal Precision"
                                        value={validation.decimalPrecision ?? 0}
                                        onChange={(value) => onValidationChange({ decimalPrecision: value || undefined })}
                                        min={0}
                                        max={10}
                                        helpText="Maximum decimal places"
                                    />
                                </ValidationControl>

                                <ValidationControl ruleKey="stepIncrement" disabledRules={disabledRules}>
                                    <PropertyNumberInput
                                        label="Step Increment"
                                        value={validation.stepIncrement ?? 0}
                                        onChange={(value) => onValidationChange({ stepIncrement: value || undefined })}
                                        min={0}
                                        max={1000}
                                        step={0.01}
                                        helpText="Value must be multiple of this"
                                    />
                                </ValidationControl>

                                <div className="grid grid-cols-2 gap-3">
                                    <ValidationControl ruleKey="oddOnly" disabledRules={disabledRules}>
                                        <PropertyToggle
                                            label="Odd Only"
                                            checked={validation.oddOnly ?? false}
                                            onChange={(checked) => onValidationChange({ 
                                                oddOnly: checked || undefined, 
                                                evenOnly: checked ? undefined : validation.evenOnly 
                                            })}
                                            helpText="Odd numbers"
                                        />
                                    </ValidationControl>
                                    <ValidationControl ruleKey="evenOnly" disabledRules={disabledRules}>
                                        <PropertyToggle
                                            label="Even Only"
                                            checked={validation.evenOnly ?? false}
                                            onChange={(checked) => onValidationChange({ 
                                                evenOnly: checked || undefined, 
                                                oddOnly: checked ? undefined : validation.oddOnly 
                                            })}
                                            helpText="Even numbers"
                                        />
                                    </ValidationControl>
                                </div>

                                {/* Custom Error Message */}
                                <PropertyTextInput
                                    label="Custom Error Message"
                                    value={validation.customError || ''}
                                    onChange={(value) => onValidationChange({ customError: value || undefined })}
                                    placeholder="Please enter a valid number..."
                                    helpText="Shown when any validation fails"
                                />
                            </CollapsibleTier>
                        </>
                    )}

                    {/* ═══════════════════════════════════════════════════════════════ */}
                    {/* EMAIL VALIDATION RULES */}
                    {/* ═══════════════════════════════════════════════════════════════ */}
                    {isEmailType && (
                        <>
                            <CollapsibleTier
                                title="Email Format"
                                icon={AtSign}
                                iconColor="text-blue-500"
                            >
                                <PropertyToggle
                                    label={<RuleLabel label="Valid Email Format" ruleKey="email" />}
                                    checked={validation.email ?? true}
                                    onChange={(checked) => onValidationChange({ email: checked })}
                                    helpText="Must be valid email structure"
                                />

                                <PropertyToggle
                                    label={<RuleLabel label="No Plus Addressing" ruleKey="noPlusAddressing" />}
                                    checked={validation.noPlusAddressing ?? false}
                                    onChange={(checked) => onValidationChange({ noPlusAddressing: checked || undefined })}
                                    helpText="Block email+tag@domain format"
                                />
                            </CollapsibleTier>

                            <CollapsibleTier
                                title="Domain Rules"
                                icon={Shield}
                                iconColor="text-amber-500"
                                bgColor="bg-amber-50/50 dark:bg-amber-900/10"
                            >
                                <ValidationControl ruleKey="businessEmailOnly" disabledRules={disabledRules}>
                                    <PropertyToggle
                                        label={<RuleLabel label="Business Email Only" ruleKey="businessEmailOnly" />}
                                        checked={validation.businessEmailOnly ?? false}
                                        onChange={(checked) => onValidationChange({ businessEmailOnly: checked || undefined })}
                                        helpText="Block free providers (Gmail, Yahoo)"
                                    />
                                </ValidationControl>

                                <ValidationControl ruleKey="noDisposableEmail" disabledRules={disabledRules}>
                                    <PropertyToggle
                                        label={<RuleLabel label="No Disposable Emails" ruleKey="noDisposableEmail" />}
                                        checked={validation.noDisposableEmail ?? false}
                                        onChange={(checked) => onValidationChange({ noDisposableEmail: checked || undefined })}
                                        helpText="Block temporary email services"
                                    />
                                </ValidationControl>

                                <ValidationControl ruleKey="domainWhitelist" disabledRules={disabledRules}>
                                    <div>
                                        <div className="flex items-center gap-1.5 mb-1">
                                            <span className="text-xs font-medium text-gray-700 dark:text-gray-300">Allowed Domains</span>
                                            <InfoTooltip info={getDomainFieldInfo('whitelist')} size={12} />
                                        </div>
                                        <PropertyTextInput
                                            label=""
                                            value={validation.domainWhitelist?.join(', ') || ''}
                                            onChange={(value) => {
                                                const domains = parseDomainInput(value);
                                                onValidationChange({ domainWhitelist: domains.length > 0 ? domains : undefined });
                                            }}
                                            placeholder="company.com, partner.org"
                                            helpText="Comma-separated domain names"
                                        />
                                    </div>
                                </ValidationControl>

                                <ValidationControl ruleKey="domainBlacklist" disabledRules={disabledRules}>
                                    <div>
                                        <div className="flex items-center gap-1.5 mb-1">
                                            <span className="text-xs font-medium text-gray-700 dark:text-gray-300">Blocked Domains</span>
                                            <InfoTooltip info={getDomainFieldInfo('blacklist')} size={12} />
                                        </div>
                                        <PropertyTextInput
                                            label=""
                                            value={validation.domainBlacklist?.join(', ') || ''}
                                            onChange={(value) => {
                                                const domains = parseDomainInput(value);
                                                onValidationChange({ domainBlacklist: domains.length > 0 ? domains : undefined });
                                            }}
                                            placeholder="spam.com, fake.org"
                                            helpText="Comma-separated domain names"
                                        />
                                    </div>
                                </ValidationControl>

                                {/* Custom Error Message */}
                                <PropertyTextInput
                                    label="Custom Error Message"
                                    value={validation.customError || ''}
                                    onChange={(value) => onValidationChange({ customError: value || undefined })}
                                    placeholder="Please enter a valid email..."
                                    helpText="Shown when any validation fails"
                                />
                            </CollapsibleTier>
                        </>
                    )}

                    {/* ═══════════════════════════════════════════════════════════════ */}
                    {/* PHONE VALIDATION RULES */}
                    {/* ═══════════════════════════════════════════════════════════════ */}
                    {isPhoneType && (
                        <>
                            <CollapsibleTier
                                title="Phone Format"
                                icon={Phone}
                                iconColor="text-blue-500"
                            >
                                <PropertyToggle
                                    label={<RuleLabel label="Valid Phone Format" ruleKey="phone" />}
                                    checked={validation.phone ?? true}
                                    onChange={(checked) => onValidationChange({ phone: checked })}
                                    helpText="Must be valid phone number"
                                />

                                <PropertyToggle
                                    label={<RuleLabel label="Country Code Required" ruleKey="countryCodeRequired" />}
                                    checked={validation.countryCodeRequired ?? false}
                                    onChange={(checked) => onValidationChange({ countryCodeRequired: checked || undefined })}
                                    helpText="Must include +XX country prefix"
                                />
                            </CollapsibleTier>

                            <CollapsibleTier
                                title="Restrictions"
                                icon={Shield}
                                iconColor="text-amber-500"
                                bgColor="bg-amber-50/50 dark:bg-amber-900/10"
                            >
                                <PropertyToggle
                                    label={<RuleLabel label="Mobile Numbers Only" ruleKey="mobileOnly" />}
                                    checked={validation.mobileOnly ?? false}
                                    onChange={(checked) => onValidationChange({ mobileOnly: checked || undefined })}
                                    helpText="Reject landline numbers"
                                />

                                <ValidationControl ruleKey="allowedCountries" disabledRules={disabledRules}>
                                    <PropertyTextInput
                                        label="Allowed Countries"
                                        value={validation.allowedCountries?.join(', ') || ''}
                                        onChange={(value) => {
                                            const countries = value
                                                .split(',')
                                                .map(s => s.trim().toUpperCase())
                                                .filter(s => s.length === 2);
                                            onValidationChange({ allowedCountries: countries.length > 0 ? countries : undefined });
                                        }}
                                        placeholder="US, CA, GB, AU"
                                        helpText="ISO country codes"
                                    />
                                </ValidationControl>

                                {/* Custom Error Message */}
                                <PropertyTextInput
                                    label="Custom Error Message"
                                    value={validation.customError || ''}
                                    onChange={(value) => onValidationChange({ customError: value || undefined })}
                                    placeholder="Please enter a valid phone number..."
                                    helpText="Shown when any validation fails"
                                />
                            </CollapsibleTier>
                        </>
                    )}

                    {/* ═══════════════════════════════════════════════════════════════ */}
                    {/* DATE VALIDATION RULES */}
                    {/* ═══════════════════════════════════════════════════════════════ */}
                    {isDateType && (
                        <>
                            <CollapsibleTier
                                title="Date Range"
                                icon={Calendar}
                                iconColor="text-blue-500"
                            >
                                <div className="space-y-2">
                                    <label className="text-xs font-medium text-gray-700 dark:text-gray-300">Earliest Date</label>
                                    <div className="flex gap-2">
                                        <input
                                            type="date"
                                            value={validation.minDate === 'today' ? '' : (validation.minDate || '')}
                                            onChange={(e) => onValidationChange({ minDate: e.target.value || undefined })}
                                            className="flex-1 px-2 py-1.5 text-sm border border-gray-300 dark:border-gray-600 
                                                rounded bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200"
                                        />
                                        <button
                                            type="button"
                                            onClick={() => onValidationChange({ minDate: validation.minDate === 'today' ? undefined : 'today' })}
                                            className={`px-2 py-1 text-xs rounded border ${
                                                validation.minDate === 'today'
                                                    ? 'bg-blue-100 dark:bg-blue-900/30 border-blue-300 dark:border-blue-700 text-blue-700 dark:text-blue-300'
                                                    : 'bg-gray-100 dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-400'
                                            }`}
                                        >
                                            Today
                                        </button>
                                    </div>
                                </div>

                                <div className="space-y-2">
                                    <label className="text-xs font-medium text-gray-700 dark:text-gray-300">Latest Date</label>
                                    <div className="flex gap-2">
                                        <input
                                            type="date"
                                            value={validation.maxDate === 'today' ? '' : (validation.maxDate || '')}
                                            onChange={(e) => onValidationChange({ maxDate: e.target.value || undefined })}
                                            className="flex-1 px-2 py-1.5 text-sm border border-gray-300 dark:border-gray-600 
                                                rounded bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200"
                                        />
                                        <button
                                            type="button"
                                            onClick={() => onValidationChange({ maxDate: validation.maxDate === 'today' ? undefined : 'today' })}
                                            className={`px-2 py-1 text-xs rounded border ${
                                                validation.maxDate === 'today'
                                                    ? 'bg-blue-100 dark:bg-blue-900/30 border-blue-300 dark:border-blue-700 text-blue-700 dark:text-blue-300'
                                                    : 'bg-gray-100 dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-400'
                                            }`}
                                        >
                                            Today
                                        </button>
                                    </div>
                                </div>

                                <ValidationControl ruleKey="futureOnly" disabledRules={disabledRules}>
                                    <PropertyToggle
                                        label={<RuleLabel label="Future Dates Only" ruleKey="futureOnly" />}
                                        checked={validation.futureOnly ?? false}
                                        onChange={(checked) => onValidationChange({ 
                                            futureOnly: checked || undefined, 
                                            pastOnly: checked ? undefined : validation.pastOnly 
                                        })}
                                        helpText="Must be after today"
                                    />
                                </ValidationControl>

                                <ValidationControl ruleKey="pastOnly" disabledRules={disabledRules}>
                                    <PropertyToggle
                                        label={<RuleLabel label="Past Dates Only" ruleKey="pastOnly" />}
                                        checked={validation.pastOnly ?? false}
                                        onChange={(checked) => onValidationChange({ 
                                            pastOnly: checked || undefined, 
                                            futureOnly: checked ? undefined : validation.futureOnly 
                                        })}
                                        helpText="Must be before today"
                                    />
                                </ValidationControl>
                            </CollapsibleTier>

                            <CollapsibleTier
                                title="Age Validation"
                                icon={Settings2}
                                iconColor="text-purple-500"
                                bgColor="bg-gray-50 dark:bg-gray-800/50"
                            >
                                <ValidationControl ruleKey="minimumAge" disabledRules={disabledRules}>
                                    <PropertyNumberInput
                                        label={<RuleLabel label="Minimum Age (years)" ruleKey="minimumAge" />}
                                        value={validation.minimumAge ?? 0}
                                        onChange={(value) => onValidationChange({ minimumAge: value || undefined })}
                                        min={0}
                                        max={150}
                                        helpText="User must be at least this old"
                                    />
                                </ValidationControl>

                                <ValidationControl ruleKey="maximumAge" disabledRules={disabledRules}>
                                    <PropertyNumberInput
                                        label="Maximum Age (years)"
                                        value={validation.maximumAge ?? 0}
                                        onChange={(value) => onValidationChange({ maximumAge: value || undefined })}
                                        min={0}
                                        max={150}
                                        helpText="User cannot be older than this"
                                    />
                                </ValidationControl>
                            </CollapsibleTier>

                            <CollapsibleTier
                                title="Day Restrictions"
                                icon={Calendar}
                                iconColor="text-amber-500"
                                bgColor="bg-amber-50/50 dark:bg-amber-900/10"
                                defaultOpen={false}
                            >
                                <PropertyToggle
                                    label={<RuleLabel label="Weekdays Only" ruleKey="weekdaysOnly" />}
                                    checked={validation.weekdaysOnly ?? false}
                                    onChange={(checked) => onValidationChange({ weekdaysOnly: checked || undefined })}
                                    helpText="No weekends allowed"
                                />

                                <PropertyToggle
                                    label="Enable Date Range"
                                    checked={validation.isDateRange ?? false}
                                    onChange={(checked) => onValidationChange({ isDateRange: checked || undefined })}
                                    helpText="Allow selecting start and end dates"
                                />

                                {validation.isDateRange && (
                                    <div className="grid grid-cols-2 gap-3 mt-2">
                                        <PropertyNumberInput
                                            label="Min Span (days)"
                                            value={validation.minDateRangeSpan ?? 0}
                                            onChange={(value) => onValidationChange({ minDateRangeSpan: value || undefined })}
                                            min={0}
                                            max={365}
                                            helpText="Min days between"
                                        />
                                        <PropertyNumberInput
                                            label="Max Span (days)"
                                            value={validation.maxDateRangeSpan ?? 0}
                                            onChange={(value) => onValidationChange({ maxDateRangeSpan: value || undefined })}
                                            min={0}
                                            max={365}
                                            helpText="Max days between"
                                        />
                                    </div>
                                )}

                                {/* Custom Error Message */}
                                <PropertyTextInput
                                    label="Custom Error Message"
                                    value={validation.customError || ''}
                                    onChange={(value) => onValidationChange({ customError: value || undefined })}
                                    placeholder="Please enter a valid date..."
                                    helpText="Shown when any validation fails"
                                />
                            </CollapsibleTier>
                        </>
                    )}

                    {/* ═══════════════════════════════════════════════════════════════ */}
                    {/* VALIDATION TESTER */}
                    {/* ═══════════════════════════════════════════════════════════════ */}
                    {!isSelectionType && (
                        <ValidationTester 
                            validation={validation} 
                            componentType={componentType}
                            componentId={componentId}
                        />
                    )}

                    {/* Info Note */}
                    <div className="flex items-start gap-2 text-xs text-gray-400 dark:text-gray-500 bg-gray-50 dark:bg-gray-800 p-3 rounded-lg">
                        <Info size={14} className="mt-0.5 flex-shrink-0" />
                        <div>
                            Validation runs in the public form. Conflicting rules auto-disable.
                            Click <span className="inline-flex items-center">?</span> for tips.
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};
