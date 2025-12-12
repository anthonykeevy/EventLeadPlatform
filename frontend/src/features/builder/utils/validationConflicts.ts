/**
 * Validation Rule Conflict Detection - Phase 1
 * 
 * Detects conflicting or redundant validation rules and provides
 * information to disable irrelevant options in the UI.
 * 
 * Example conflicts:
 * - "Allow Zero" is irrelevant when minValue > 0 or maxValue < 0
 * - "Positive Only" implies "Non-Negative" (so non-negative becomes redundant)
 * - "Integer Only" conflicts with "Decimal Precision"
 */

import { ValidationRules } from '../types/builder.types';

/**
 * Describes why a rule is disabled
 */
export interface DisabledRule {
    ruleKey: string;
    reason: string;
    conflictingRules: string[];
}

/**
 * Rule conflict definition
 */
interface ConflictDefinition {
    ruleKey: string;
    displayName: string;
    // Returns true if this rule should be disabled given the current validation state
    isDisabled: (validation: ValidationRules) => boolean;
    // Human-readable reason for the conflict
    getReason: (validation: ValidationRules) => string;
    // Which rules cause this conflict
    getConflictingRules: (validation: ValidationRules) => string[];
}

/**
 * All conflict definitions organized by component type
 */
const NUMBER_CONFLICTS: ConflictDefinition[] = [
    {
        ruleKey: 'nonNegative',
        displayName: 'Non-Negative',
        isDisabled: (v) => v.positiveOnly === true,
        getReason: () => '"Positive Only" already excludes negative numbers and zero',
        getConflictingRules: () => ['positiveOnly'],
    },
    {
        ruleKey: 'nonZero',
        displayName: 'Non-Zero',
        isDisabled: (v) => {
            // Disabled if min > 0 or max < 0 (zero already excluded by range)
            const minExcludesZero = v.minValue !== undefined && v.minValue > 0;
            const maxExcludesZero = v.maxValue !== undefined && v.maxValue < 0;
            return minExcludesZero || maxExcludesZero || v.positiveOnly === true;
        },
        getReason: (v) => {
            if (v.positiveOnly) return '"Positive Only" already excludes zero';
            if (v.minValue !== undefined && v.minValue > 0) return `Min value ${v.minValue} already excludes zero`;
            if (v.maxValue !== undefined && v.maxValue < 0) return `Max value ${v.maxValue} already excludes zero`;
            return 'Zero is already excluded by other rules';
        },
        getConflictingRules: (v) => {
            const rules: string[] = [];
            if (v.positiveOnly) rules.push('positiveOnly');
            if (v.minValue !== undefined && v.minValue > 0) rules.push('minValue');
            if (v.maxValue !== undefined && v.maxValue < 0) rules.push('maxValue');
            return rules;
        },
    },
    {
        ruleKey: 'decimalPrecision',
        displayName: 'Decimal Precision',
        isDisabled: (v) => v.integerOnly === true,
        getReason: () => '"Integer Only" already prevents decimal values',
        getConflictingRules: () => ['integerOnly'],
    },
    {
        ruleKey: 'integerOnly',
        displayName: 'Integer Only',
        isDisabled: (v) => v.decimalPrecision !== undefined && v.decimalPrecision > 0,
        getReason: (v) => `Decimal precision of ${v.decimalPrecision} requires decimals`,
        getConflictingRules: () => ['decimalPrecision'],
    },
    {
        ruleKey: 'oddOnly',
        displayName: 'Odd Only',
        isDisabled: (v) => v.evenOnly === true,
        getReason: () => 'Cannot be both odd and even',
        getConflictingRules: () => ['evenOnly'],
    },
    {
        ruleKey: 'evenOnly',
        displayName: 'Even Only',
        isDisabled: (v) => v.oddOnly === true,
        getReason: () => 'Cannot be both odd and even',
        getConflictingRules: () => ['oddOnly'],
    },
    {
        ruleKey: 'stepIncrement',
        displayName: 'Step Increment',
        isDisabled: (v) => {
            // Step is meaningless if allowed values are specified
            return v.allowedValues !== undefined && v.allowedValues.length > 0;
        },
        getReason: () => '"Allowed Values" already restricts which numbers are valid',
        getConflictingRules: () => ['allowedValues'],
    },
    {
        ruleKey: 'minValue',
        displayName: 'Minimum Value',
        isDisabled: (v) => v.allowedValues !== undefined && v.allowedValues.length > 0,
        getReason: () => '"Allowed Values" already defines the valid range',
        getConflictingRules: () => ['allowedValues'],
    },
    {
        ruleKey: 'maxValue',
        displayName: 'Maximum Value',
        isDisabled: (v) => v.allowedValues !== undefined && v.allowedValues.length > 0,
        getReason: () => '"Allowed Values" already defines the valid range',
        getConflictingRules: () => ['allowedValues'],
    },
];

const TEXT_CONFLICTS: ConflictDefinition[] = [
    {
        ruleKey: 'alpha',
        displayName: 'Letters Only',
        isDisabled: (v) => v.alphanumeric === true,
        getReason: () => '"Alphanumeric" already allows all letters (plus numbers)',
        getConflictingRules: () => ['alphanumeric'],
    },
    {
        ruleKey: 'blockedCharacters',
        displayName: 'Blocked Characters',
        isDisabled: (v) => v.alpha === true || v.alphanumeric === true,
        getReason: (v) => {
            if (v.alpha) return '"Letters Only" already restricts to letters - no characters to block';
            if (v.alphanumeric) return '"Alphanumeric" already restricts to letters/numbers - no characters to block';
            return 'Character rules already restrict what can be entered';
        },
        getConflictingRules: (v) => {
            const rules: string[] = [];
            if (v.alpha) rules.push('alpha');
            if (v.alphanumeric) rules.push('alphanumeric');
            return rules;
        },
    },
    {
        ruleKey: 'trimWhitespace',
        displayName: 'Trim Whitespace',
        isDisabled: (v) => v.alpha === true || v.alphanumeric === true,
        getReason: (v) => {
            if (v.alpha) return '"Letters Only" already prevents spaces';
            if (v.alphanumeric) return '"Alphanumeric" already prevents spaces';
            return 'Character rules already prevent spaces';
        },
        getConflictingRules: (v) => {
            const rules: string[] = [];
            if (v.alpha) rules.push('alpha');
            if (v.alphanumeric) rules.push('alphanumeric');
            return rules;
        },
    },
    {
        ruleKey: 'noConsecutiveSpaces',
        displayName: 'No Consecutive Spaces',
        isDisabled: (v) => v.alpha === true || v.alphanumeric === true,
        getReason: (v) => {
            if (v.alpha) return '"Letters Only" already prevents spaces';
            if (v.alphanumeric) return '"Alphanumeric" already prevents spaces';
            return 'Character rules already prevent multiple spaces';
        },
        getConflictingRules: (v) => {
            const rules: string[] = [];
            if (v.alpha) rules.push('alpha');
            if (v.alphanumeric) rules.push('alphanumeric');
            return rules;
        },
    },
    {
        ruleKey: 'pattern',
        displayName: 'Custom Pattern',
        isDisabled: (v) => {
            // Pattern is less useful if strict character rules are in place
            return v.alpha === true || v.numeric === true || v.alphanumeric === true;
        },
        getReason: () => 'Character set rules already restrict the format',
        getConflictingRules: (v) => {
            const rules: string[] = [];
            if (v.alpha) rules.push('alpha');
            if (v.numeric) rules.push('numeric');
            if (v.alphanumeric) rules.push('alphanumeric');
            return rules;
        },
    },
];

const EMAIL_CONFLICTS: ConflictDefinition[] = [
    {
        ruleKey: 'domainWhitelist',
        displayName: 'Allowed Domains',
        isDisabled: (v) => v.domainBlacklist !== undefined && v.domainBlacklist.length > 0,
        getReason: () => 'Cannot use both whitelist and blacklist - choose one approach',
        getConflictingRules: () => ['domainBlacklist'],
    },
    {
        ruleKey: 'domainBlacklist',
        displayName: 'Blocked Domains',
        isDisabled: (v) => v.domainWhitelist !== undefined && v.domainWhitelist.length > 0,
        getReason: () => 'Cannot use both whitelist and blacklist - choose one approach',
        getConflictingRules: () => ['domainWhitelist'],
    },
    {
        ruleKey: 'noDisposableEmail',
        displayName: 'Block Disposable Emails',
        isDisabled: (v) => v.domainWhitelist !== undefined && v.domainWhitelist.length > 0,
        getReason: () => 'Domain whitelist already restricts to specific domains',
        getConflictingRules: () => ['domainWhitelist'],
    },
    {
        ruleKey: 'businessEmailOnly',
        displayName: 'Business Email Only',
        isDisabled: (v) => v.domainWhitelist !== undefined && v.domainWhitelist.length > 0,
        getReason: () => 'Domain whitelist already restricts to specific domains',
        getConflictingRules: () => ['domainWhitelist'],
    },
];

const DATE_CONFLICTS: ConflictDefinition[] = [
    {
        ruleKey: 'pastOnly',
        displayName: 'Past Dates Only',
        isDisabled: (v) => v.futureOnly === true,
        getReason: () => 'Cannot require both past and future dates',
        getConflictingRules: () => ['futureOnly'],
    },
    {
        ruleKey: 'futureOnly',
        displayName: 'Future Dates Only',
        isDisabled: (v) => v.pastOnly === true,
        getReason: () => 'Cannot require both past and future dates',
        getConflictingRules: () => ['pastOnly'],
    },
    {
        ruleKey: 'minimumAge',
        displayName: 'Minimum Age',
        isDisabled: (v) => v.futureOnly === true,
        getReason: () => 'Age validation requires past dates (birthdates)',
        getConflictingRules: () => ['futureOnly'],
    },
    {
        ruleKey: 'maximumAge',
        displayName: 'Maximum Age',
        isDisabled: (v) => v.futureOnly === true,
        getReason: () => 'Age validation requires past dates (birthdates)',
        getConflictingRules: () => ['futureOnly'],
    },
    {
        ruleKey: 'minDate',
        displayName: 'Earliest Date',
        isDisabled: (v) => {
            // If we have age validation, minDate might conflict
            return v.minimumAge !== undefined || v.maximumAge !== undefined;
        },
        getReason: () => 'Age validation already constrains the date range',
        getConflictingRules: (v) => {
            const rules: string[] = [];
            if (v.minimumAge !== undefined) rules.push('minimumAge');
            if (v.maximumAge !== undefined) rules.push('maximumAge');
            return rules;
        },
    },
];

const PHONE_CONFLICTS: ConflictDefinition[] = [
    {
        ruleKey: 'allowedCountries',
        displayName: 'Allowed Countries',
        isDisabled: (v) => v.countryCodeRequired === false,
        getReason: () => 'Country filtering requires country codes to be present',
        getConflictingRules: () => ['countryCodeRequired'],
    },
];

/**
 * Get all conflict definitions for a component type
 */
function getConflictDefinitions(componentType: string): ConflictDefinition[] {
    switch (componentType) {
        case 'number':
            return NUMBER_CONFLICTS;
        case 'text':
        case 'textarea':
        case 'first-name':
            return TEXT_CONFLICTS;
        case 'email':
            return EMAIL_CONFLICTS;
        case 'date':
            return DATE_CONFLICTS;
        case 'phone':
            return PHONE_CONFLICTS;
        default:
            return [];
    }
}

/**
 * Get all disabled rules for the current validation state
 * 
 * @param validation - Current validation rules
 * @param componentType - Type of component being validated
 * @returns Map of rule keys to their disabled state and reason
 */
export function getDisabledRules(
    validation: ValidationRules,
    componentType: string
): Map<string, DisabledRule> {
    const disabledRules = new Map<string, DisabledRule>();
    const definitions = getConflictDefinitions(componentType);
    
    for (const def of definitions) {
        if (def.isDisabled(validation)) {
            disabledRules.set(def.ruleKey, {
                ruleKey: def.ruleKey,
                reason: def.getReason(validation),
                conflictingRules: def.getConflictingRules(validation),
            });
        }
    }
    
    return disabledRules;
}

/**
 * Check if a specific rule is disabled
 */
export function isRuleDisabled(
    ruleKey: string,
    validation: ValidationRules,
    componentType: string
): boolean {
    const disabledRules = getDisabledRules(validation, componentType);
    return disabledRules.has(ruleKey);
}

/**
 * Get the reason why a rule is disabled
 */
export function getDisabledReason(
    ruleKey: string,
    validation: ValidationRules,
    componentType: string
): string | null {
    const disabledRules = getDisabledRules(validation, componentType);
    const rule = disabledRules.get(ruleKey);
    return rule?.reason ?? null;
}

/**
 * Validate that the current rules don't have impossible combinations
 * Returns list of warnings/errors
 */
export function validateRuleConsistency(
    validation: ValidationRules,
    componentType: string
): string[] {
    const warnings: string[] = [];
    
    // Number-specific consistency checks
    if (componentType === 'number') {
        if (validation.minValue !== undefined && validation.maxValue !== undefined) {
            if (validation.minValue > validation.maxValue) {
                warnings.push('Minimum value cannot be greater than maximum value');
            }
        }
        
        if (validation.allowedValues && validation.allowedValues.length > 0) {
            const values = validation.allowedValues;
            if (validation.minValue !== undefined) {
                const belowMin = values.filter(v => v < validation.minValue!);
                if (belowMin.length > 0) {
                    warnings.push(`Some allowed values are below minimum: ${belowMin.join(', ')}`);
                }
            }
            if (validation.maxValue !== undefined) {
                const aboveMax = values.filter(v => v > validation.maxValue!);
                if (aboveMax.length > 0) {
                    warnings.push(`Some allowed values are above maximum: ${aboveMax.join(', ')}`);
                }
            }
        }
    }
    
    // Text-specific consistency checks
    if (['text', 'textarea', 'first-name'].includes(componentType)) {
        if (validation.minLength !== undefined && validation.maxLength !== undefined) {
            if (validation.minLength > validation.maxLength) {
                warnings.push('Minimum length cannot be greater than maximum length');
            }
        }
    }
    
    // Date-specific consistency checks
    if (componentType === 'date') {
        if (validation.minimumAge !== undefined && validation.maximumAge !== undefined) {
            if (validation.minimumAge > validation.maximumAge) {
                warnings.push('Minimum age cannot be greater than maximum age');
            }
        }
    }
    
    return warnings;
}

/**
 * Rule metadata for display in the UI
 */
export interface RuleMetadata {
    key: string;
    displayName: string;
    description: string;
    category: string;
    inputType: 'boolean' | 'number' | 'string' | 'array' | 'select';
    selectOptions?: { value: string; label: string }[];
    min?: number;
    max?: number;
    placeholder?: string;
}

/**
 * Get all available rules for a component type with their metadata
 */
export function getAvailableRules(componentType: string): RuleMetadata[] {
    const rules: RuleMetadata[] = [];
    
    // Common rules
    rules.push({
        key: 'required',
        displayName: 'Required',
        description: 'Field must have a value',
        category: 'general',
        inputType: 'boolean',
    });
    
    switch (componentType) {
        case 'number':
            rules.push(
                { key: 'minValue', displayName: 'Minimum Value', description: 'Lowest allowed number', category: 'range', inputType: 'number' },
                { key: 'maxValue', displayName: 'Maximum Value', description: 'Highest allowed number', category: 'range', inputType: 'number' },
                { key: 'integerOnly', displayName: 'Integer Only', description: 'No decimal values allowed', category: 'type', inputType: 'boolean' },
                { key: 'decimalPrecision', displayName: 'Decimal Precision', description: 'Maximum decimal places', category: 'type', inputType: 'number', min: 0, max: 10 },
                { key: 'stepIncrement', displayName: 'Step Increment', description: 'Value must be multiple of this', category: 'type', inputType: 'number', placeholder: '0.01, 0.5, 1, 5' },
                { key: 'positiveOnly', displayName: 'Positive Only', description: 'Must be greater than zero', category: 'range', inputType: 'boolean' },
                { key: 'nonNegative', displayName: 'Non-Negative', description: 'Zero or positive only', category: 'range', inputType: 'boolean' },
                { key: 'nonZero', displayName: 'Non-Zero', description: 'Cannot be exactly zero', category: 'range', inputType: 'boolean' },
                { key: 'oddOnly', displayName: 'Odd Numbers', description: 'Only odd values allowed', category: 'parity', inputType: 'boolean' },
                { key: 'evenOnly', displayName: 'Even Numbers', description: 'Only even values allowed', category: 'parity', inputType: 'boolean' },
                { key: 'allowedValues', displayName: 'Allowed Values', description: 'Only these specific numbers', category: 'enumeration', inputType: 'array', placeholder: '1, 5, 10, 25, 50, 100' },
            );
            break;
            
        case 'text':
        case 'textarea':
        case 'first-name':
            rules.push(
                { key: 'minLength', displayName: 'Min Length', description: 'Minimum characters required', category: 'length', inputType: 'number', min: 0 },
                { key: 'maxLength', displayName: 'Max Length', description: 'Maximum characters allowed', category: 'length', inputType: 'number', min: 0 },
                { key: 'pattern', displayName: 'Pattern (Regex)', description: 'Custom regex pattern', category: 'format', inputType: 'string', placeholder: '^[A-Za-z]+$' },
                { key: 'alpha', displayName: 'Letters Only', description: 'A-Z and a-z only', category: 'characters', inputType: 'boolean' },
                { key: 'alphanumeric', displayName: 'Alphanumeric', description: 'Letters and numbers only', category: 'characters', inputType: 'boolean' },
                { key: 'noHtmlScript', displayName: 'No HTML/Script', description: 'Block HTML tags and scripts', category: 'security', inputType: 'boolean' },
                { key: 'trimWhitespace', displayName: 'Trim Whitespace', description: 'Remove leading/trailing spaces', category: 'formatting', inputType: 'boolean' },
                { key: 'noConsecutiveSpaces', displayName: 'No Consecutive Spaces', description: 'Only single spaces allowed', category: 'formatting', inputType: 'boolean' },
                { key: 'caseTransform', displayName: 'Case Transform', description: 'Auto-convert text case', category: 'formatting', inputType: 'select', selectOptions: [
                    { value: 'uppercase', label: 'UPPERCASE' },
                    { value: 'lowercase', label: 'lowercase' },
                    { value: 'titlecase', label: 'Title Case' },
                ]},
                { key: 'blockedCharacters', displayName: 'Blocked Characters', description: 'Characters not allowed', category: 'characters', inputType: 'string', placeholder: '<>{}[]' },
                { key: 'mustMatchField', displayName: 'Must Match Field', description: 'Value must match another field', category: 'cross-field', inputType: 'string', placeholder: 'fieldId' },
            );
            break;
            
        case 'email':
            rules.push(
                { key: 'email', displayName: 'Valid Email Format', description: 'Must be valid email structure', category: 'format', inputType: 'boolean' },
                { key: 'businessEmailOnly', displayName: 'Business Email Only', description: 'Block free email providers', category: 'domain', inputType: 'boolean' },
                { key: 'noDisposableEmail', displayName: 'No Disposable Emails', description: 'Block temporary email services', category: 'domain', inputType: 'boolean' },
                { key: 'noPlusAddressing', displayName: 'No Plus Addressing', description: 'Block email+tag@ format', category: 'format', inputType: 'boolean' },
                { key: 'domainWhitelist', displayName: 'Allowed Domains', description: 'Only these domains accepted', category: 'domain', inputType: 'array', placeholder: 'company.com, partner.org' },
                { key: 'domainBlacklist', displayName: 'Blocked Domains', description: 'These domains rejected', category: 'domain', inputType: 'array', placeholder: 'spam.com, fake.org' },
            );
            break;
            
        case 'phone':
            rules.push(
                { key: 'phone', displayName: 'Valid Phone Format', description: 'Must be valid phone structure', category: 'format', inputType: 'boolean' },
                { key: 'countryCodeRequired', displayName: 'Country Code Required', description: 'Must include +XX prefix', category: 'format', inputType: 'boolean' },
                { key: 'mobileOnly', displayName: 'Mobile Numbers Only', description: 'Reject landline numbers', category: 'type', inputType: 'boolean' },
                { key: 'allowedCountries', displayName: 'Allowed Countries', description: 'Only these country codes', category: 'location', inputType: 'array', placeholder: 'US, CA, GB, AU' },
            );
            break;
            
        case 'date':
            rules.push(
                { key: 'minDate', displayName: 'Earliest Date', description: 'Cannot be before this date', category: 'range', inputType: 'string', placeholder: 'YYYY-MM-DD or "today"' },
                { key: 'maxDate', displayName: 'Latest Date', description: 'Cannot be after this date', category: 'range', inputType: 'string', placeholder: 'YYYY-MM-DD or "today"' },
                { key: 'futureOnly', displayName: 'Future Dates Only', description: 'Must be after today', category: 'range', inputType: 'boolean' },
                { key: 'pastOnly', displayName: 'Past Dates Only', description: 'Must be before today', category: 'range', inputType: 'boolean' },
                { key: 'minimumAge', displayName: 'Minimum Age', description: 'User must be at least N years old', category: 'age', inputType: 'number', min: 0, max: 150, placeholder: '18' },
                { key: 'maximumAge', displayName: 'Maximum Age', description: 'User cannot be older than N years', category: 'age', inputType: 'number', min: 0, max: 150 },
                { key: 'weekdaysOnly', displayName: 'Weekdays Only', description: 'No weekends allowed', category: 'days', inputType: 'boolean' },
                { key: 'isDateRange', displayName: 'Date Range', description: 'Allow selecting start and end dates', category: 'type', inputType: 'boolean' },
            );
            break;
    }
    
    // Custom error message (all types)
    rules.push({
        key: 'customError',
        displayName: 'Custom Error Message',
        description: 'Message shown when validation fails',
        category: 'general',
        inputType: 'string',
        placeholder: 'Please enter a valid value...',
    });
    
    return rules;
}

export default {
    getDisabledRules,
    isRuleDisabled,
    getDisabledReason,
    validateRuleConsistency,
    getAvailableRules,
};

