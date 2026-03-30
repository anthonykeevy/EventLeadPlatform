/**
 * Validation Engine - Phase 2
 * 
 * Executes validation rules against field values with:
 * - Country-aware validation (phone, date, names)
 * - Unicode-aware text validation
 * - Auto-sanitization (auto-fix) support
 * - Structured error messages with i18n keys
 * 
 * @see validationRule.types.ts for type definitions
 * @see validationRuleSeed.ts for rule definitions
 */

import { ValidationRules } from '../types/builder.types';
import {
    ValidationContext,
    ValidationResult,
    ValidationError,
    AutoFixResult,
} from '../types/validationRule.types';
import { getCountryConfig } from '../data/validationRuleSeed';
import { validatePhone } from './phoneValidation';
import { isFreeEmailProvider } from '../data/freeEmailProviders';
import { isDisposableEmailDomain } from '../data/disposableEmailDomains';

// ═══════════════════════════════════════════════════════════════════════════
// AUTO-SANITIZATION (AUTO-FIX) FUNCTIONS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Apply auto-fixes to a string value
 */
function applyAutoFixes(
    value: string,
    rules: ValidationRules,
    componentType: string
): { sanitizedValue: string; fixes: AutoFixResult[] } {
    let result = value;
    const fixes: AutoFixResult[] = [];

    // 1. Trim whitespace (default: ON)
    if (rules.trimWhitespace !== false) {
        const trimmed = result.trim();
        if (trimmed !== result) {
            fixes.push({
                fixType: 'trim',
                originalValue: result,
                fixedValue: trimmed,
                description: 'Removed leading/trailing spaces',
            });
            result = trimmed;
        }
    }

    // 2. Remove consecutive spaces (default: ON when noConsecutiveSpaces is set)
    if (rules.noConsecutiveSpaces !== false) {
        const noDoubleSpaces = result.replace(/  +/g, ' ');
        if (noDoubleSpaces !== result) {
            const spacesRemoved = (result.match(/  +/g) || []).length;
            fixes.push({
                fixType: 'consecutive_spaces',
                originalValue: result,
                fixedValue: noDoubleSpaces,
                description: `Reduced ${spacesRemoved} consecutive space${spacesRemoved > 1 ? 's' : ''} to single spaces`,
            });
            result = noDoubleSpaces;
        }
    }

    // 3. Email lowercase (default: ON for email)
    if (componentType === 'email') {
        const lowercase = result.toLowerCase();
        if (lowercase !== result) {
            fixes.push({
                fixType: 'lowercase',
                originalValue: result,
                fixedValue: lowercase,
                description: 'Converted email to lowercase',
            });
            result = lowercase;
        }
    }

    // 4. Case transform
    if (rules.caseTransform) {
        let transformed = result;
        switch (rules.caseTransform) {
            case 'uppercase':
                transformed = result.toUpperCase();
                break;
            case 'lowercase':
                transformed = result.toLowerCase();
                break;
            case 'titlecase':
                transformed = result.replace(/\b\w/g, c => c.toUpperCase());
                break;
        }
        if (transformed !== result) {
            fixes.push({
                fixType: 'titlecase',
                originalValue: result,
                fixedValue: transformed,
                description: `Converted to ${rules.caseTransform}`,
            });
            result = transformed;
        }
    }

    return { sanitizedValue: result, fixes };
}

// ═══════════════════════════════════════════════════════════════════════════
// TEXT VALIDATION
// ═══════════════════════════════════════════════════════════════════════════

function validateText(
    value: string,
    rules: ValidationRules,
    context?: ValidationContext
): ValidationError[] {
    const errors: ValidationError[] = [];

    // Get country config for character set validation
    const countryConfig = context?.countryCode 
        ? getCountryConfig(context.countryCode) 
        : undefined;

    // Min length
    if (rules.minLength !== undefined && rules.minLength > 0) {
        // Use grapheme count for proper Unicode handling
        const length = [...value].length;
        
        // Adjust for CJK character sets where shorter names are valid
        let effectiveMinLength = rules.minLength;
        if (countryConfig?.nameCharacterSet === 'cjk' && effectiveMinLength > 2) {
            effectiveMinLength = Math.min(effectiveMinLength, 2);
        }
        
        if (length < effectiveMinLength) {
            errors.push({
                ruleKey: 'minLength',
                message: `Must be at least ${effectiveMinLength} characters`,
                messageKey: 'validation.text.minLength',
                params: { min: effectiveMinLength },
            });
        }
    }

    // Max length
    if (rules.maxLength !== undefined && rules.maxLength > 0) {
        const length = [...value].length;
        if (length > rules.maxLength) {
            errors.push({
                ruleKey: 'maxLength',
                message: `Must be no more than ${rules.maxLength} characters`,
                messageKey: 'validation.text.maxLength',
                params: { max: rules.maxLength },
            });
        }
    }

    // Alpha only (Unicode-aware)
    if (rules.alpha) {
        // Use Unicode property escapes for letters
        const alphaPattern = /^[\p{L}\s'-]+$/u;
        if (!alphaPattern.test(value)) {
            errors.push({
                ruleKey: 'alpha',
                message: 'Only letters are allowed',
                messageKey: 'validation.text.alpha',
            });
        }
    }

    // Alphanumeric (Unicode-aware)
    if (rules.alphanumeric) {
        const alphanumericPattern = /^[\p{L}\p{N}\s]+$/u;
        if (!alphanumericPattern.test(value)) {
            errors.push({
                ruleKey: 'alphanumeric',
                message: 'Only letters and numbers are allowed',
                messageKey: 'validation.text.alphanumeric',
            });
        }
    }

    // Blocked characters
    if (rules.blockedCharacters && rules.blockedCharacters.length > 0) {
        const blockedChars = rules.blockedCharacters.split('');
        const foundBlocked = blockedChars.filter(c => value.includes(c));
        if (foundBlocked.length > 0) {
            errors.push({
                ruleKey: 'blockedCharacters',
                message: `These characters are not allowed: ${foundBlocked.join(' ')}`,
                messageKey: 'validation.text.blockedCharacters',
                params: { chars: foundBlocked.join(' ') },
            });
        }
    }

    // No HTML/Script (security)
    if (rules.noHtmlScript) {
        const htmlPattern = /<[^>]*>|<script|javascript:|on\w+=/i;
        if (htmlPattern.test(value)) {
            errors.push({
                ruleKey: 'noHtmlScript',
                message: 'HTML tags and scripts are not allowed',
                messageKey: 'validation.security.noHtml',
            });
        }
    }

    // Custom pattern (regex)
    if (rules.pattern) {
        try {
            const regex = new RegExp(rules.pattern, 'u');
            if (!regex.test(value)) {
                errors.push({
                    ruleKey: 'pattern',
                    message: rules.customError || 'Value does not match required format',
                    messageKey: 'validation.text.pattern',
                });
            }
        } catch {
            // Invalid regex - skip validation
            console.warn('Invalid regex pattern:', rules.pattern);
        }
    }

    return errors;
}

// ═══════════════════════════════════════════════════════════════════════════
// NUMBER VALIDATION
// ═══════════════════════════════════════════════════════════════════════════

function validateNumber(
    value: number,
    rules: ValidationRules
): ValidationError[] {
    const errors: ValidationError[] = [];

    // Min value
    if (rules.minValue !== undefined) {
        if (value < rules.minValue) {
            errors.push({
                ruleKey: 'minValue',
                message: `Must be at least ${rules.minValue}`,
                messageKey: 'validation.number.minValue',
                params: { min: rules.minValue },
            });
        }
    }

    // Max value
    if (rules.maxValue !== undefined) {
        if (value > rules.maxValue) {
            errors.push({
                ruleKey: 'maxValue',
                message: `Must be no more than ${rules.maxValue}`,
                messageKey: 'validation.number.maxValue',
                params: { max: rules.maxValue },
            });
        }
    }

    // Integer only
    if (rules.integerOnly) {
        if (!Number.isInteger(value)) {
            errors.push({
                ruleKey: 'integerOnly',
                message: 'Must be a whole number (no decimals)',
                messageKey: 'validation.number.integerOnly',
            });
        }
    }

    // Decimal precision
    if (rules.decimalPrecision !== undefined && rules.decimalPrecision >= 0) {
        const decimalPlaces = (value.toString().split('.')[1] || '').length;
        if (decimalPlaces > rules.decimalPrecision) {
            errors.push({
                ruleKey: 'decimalPrecision',
                message: `Must have no more than ${rules.decimalPrecision} decimal places`,
                messageKey: 'validation.number.decimalPrecision',
                params: { precision: rules.decimalPrecision },
            });
        }
    }

    // Positive only
    if (rules.positiveOnly && value <= 0) {
        errors.push({
            ruleKey: 'positiveOnly',
            message: 'Must be a positive number (greater than zero)',
            messageKey: 'validation.number.positiveOnly',
        });
    }

    // Non-negative
    if (rules.nonNegative && value < 0) {
        errors.push({
            ruleKey: 'nonNegative',
            message: 'Cannot be negative',
            messageKey: 'validation.number.nonNegative',
        });
    }

    // Non-zero
    if (rules.nonZero && value === 0) {
        errors.push({
            ruleKey: 'nonZero',
            message: 'Cannot be zero',
            messageKey: 'validation.number.nonZero',
        });
    }

    // Step increment
    if (rules.stepIncrement !== undefined && rules.stepIncrement > 0) {
        const remainder = value % rules.stepIncrement;
        if (Math.abs(remainder) > 0.0001) { // Float precision tolerance
            errors.push({
                ruleKey: 'stepIncrement',
                message: `Must be a multiple of ${rules.stepIncrement}`,
                messageKey: 'validation.number.stepIncrement',
                params: { step: rules.stepIncrement },
            });
        }
    }

    // Odd only
    if (rules.oddOnly && value % 2 === 0) {
        errors.push({
            ruleKey: 'oddOnly',
            message: 'Must be an odd number',
            messageKey: 'validation.number.oddOnly',
        });
    }

    // Even only
    if (rules.evenOnly && value % 2 !== 0) {
        errors.push({
            ruleKey: 'evenOnly',
            message: 'Must be an even number',
            messageKey: 'validation.number.evenOnly',
        });
    }

    // Allowed values
    if (rules.allowedValues && rules.allowedValues.length > 0) {
        if (!rules.allowedValues.includes(value)) {
            errors.push({
                ruleKey: 'allowedValues',
                message: `Must be one of: ${rules.allowedValues.join(', ')}`,
                messageKey: 'validation.number.allowedValues',
                params: { values: rules.allowedValues.join(', ') },
            });
        }
    }

    return errors;
}

// ═══════════════════════════════════════════════════════════════════════════
// EMAIL VALIDATION
// ═══════════════════════════════════════════════════════════════════════════

function validateEmail(
    value: string,
    rules: ValidationRules
): ValidationError[] {
    const errors: ValidationError[] = [];

    // Basic email format
    if (rules.email !== false) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(value)) {
            errors.push({
                ruleKey: 'email',
                message: 'Please enter a valid email address',
                messageKey: 'validation.email.format',
            });
            return errors; // Don't check other email rules if format is wrong
        }
    }

    // Business email only
    if (rules.businessEmailOnly) {
        if (isFreeEmailProvider(value)) {
            errors.push({
                ruleKey: 'businessEmailOnly',
                message: 'Please use a business email (not Gmail, Yahoo, etc.)',
                messageKey: 'validation.email.businessOnly',
            });
        }
    }

    // No disposable email
    if (rules.noDisposableEmail) {
        if (isDisposableEmailDomain(value)) {
            errors.push({
                ruleKey: 'noDisposableEmail',
                message: 'Temporary email addresses are not allowed',
                messageKey: 'validation.email.noDisposable',
            });
        }
    }

    // No plus addressing
    if (rules.noPlusAddressing) {
        if (/\+[^@]*@/.test(value)) {
            errors.push({
                ruleKey: 'noPlusAddressing',
                message: 'Plus addressing (email+tag@) is not allowed',
                messageKey: 'validation.email.noPlusAddressing',
            });
        }
    }

    // Domain whitelist
    if (rules.domainWhitelist && rules.domainWhitelist.length > 0) {
        const domain = value.split('@')[1]?.toLowerCase();
        if (!rules.domainWhitelist.includes(domain)) {
            errors.push({
                ruleKey: 'domainWhitelist',
                message: `Email must be from: ${rules.domainWhitelist.join(', ')}`,
                messageKey: 'validation.email.domainWhitelist',
                params: { domains: rules.domainWhitelist.join(', ') },
            });
        }
    }

    // Domain blacklist
    if (rules.domainBlacklist && rules.domainBlacklist.length > 0) {
        const domain = value.split('@')[1]?.toLowerCase();
        if (rules.domainBlacklist.includes(domain)) {
            errors.push({
                ruleKey: 'domainBlacklist',
                message: `Emails from ${domain} are not accepted`,
                messageKey: 'validation.email.domainBlacklist',
                params: { domain },
            });
        }
    }

    return errors;
}

// ═══════════════════════════════════════════════════════════════════════════
// URL VALIDATION
// ═══════════════════════════════════════════════════════════════════════════

function validateUrl(
    value: string,
    rules: ValidationRules,
    context?: ValidationContext
): ValidationError[] {
    const errors: ValidationError[] = [];

    // Reuse generic text rules such as min/max length and custom regex.
    errors.push(...validateText(value, rules, context));

    if (rules.url === false) {
        return errors;
    }

    const trimmed = value.trim();
    const candidate = /^[a-zA-Z][a-zA-Z\d+\-.]*:\/\//.test(trimmed) ? trimmed : `https://${trimmed}`;

    try {
        const parsed = new URL(candidate);
        const isHttp = parsed.protocol === 'http:' || parsed.protocol === 'https:';
        if (!isHttp || parsed.hostname.length === 0) {
            errors.push({
                ruleKey: 'url',
                message: 'Please enter a valid URL',
                messageKey: 'validation.url.format',
            });
        }
    } catch {
        errors.push({
            ruleKey: 'url',
            message: 'Please enter a valid URL',
            messageKey: 'validation.url.format',
        });
    }

    return errors;
}

// ═══════════════════════════════════════════════════════════════════════════
// PHONE VALIDATION
// ═══════════════════════════════════════════════════════════════════════════

function validatePhoneNumber(
    value: string,
    rules: ValidationRules,
    context?: ValidationContext
): ValidationError[] {
    const errors: ValidationError[] = [];

    // Use the phone validation utility
    const result = validatePhone(value, {
        countryCodeRequired: rules.countryCodeRequired,
        allowedCountries: rules.allowedCountries,
        mobileOnly: rules.mobileOnly,
        defaultCountry: context?.countryCode as string,
    });

    if (!result.isValid) {
        for (const error of result.errors) {
            errors.push({
                ruleKey: 'phone',
                message: error,
                messageKey: 'validation.phone.format',
            });
        }
    }

    return errors;
}

// ═══════════════════════════════════════════════════════════════════════════
// DATE VALIDATION
// ═══════════════════════════════════════════════════════════════════════════

function validateDate(
    value: string | Date,
    rules: ValidationRules,
    _context?: ValidationContext
): ValidationError[] {
    const errors: ValidationError[] = [];

    // Parse the date
    const date = value instanceof Date ? value : new Date(value);
    if (isNaN(date.getTime())) {
        errors.push({
            ruleKey: 'date',
            message: 'Please enter a valid date',
            messageKey: 'validation.date.format',
        });
        return errors;
    }

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    // Future only
    if (rules.futureOnly) {
        if (date <= today) {
            errors.push({
                ruleKey: 'futureOnly',
                message: 'Date must be in the future',
                messageKey: 'validation.date.futureOnly',
            });
        }
    }

    // Past only
    if (rules.pastOnly) {
        if (date >= today) {
            errors.push({
                ruleKey: 'pastOnly',
                message: 'Date must be in the past',
                messageKey: 'validation.date.pastOnly',
            });
        }
    }

    // Min date
    if (rules.minDate) {
        const minDate = rules.minDate === 'today' 
            ? today 
            : new Date(rules.minDate);
        if (date < minDate) {
            errors.push({
                ruleKey: 'minDate',
                message: `Date must be on or after ${minDate.toLocaleDateString()}`,
                messageKey: 'validation.date.minDate',
                params: { date: minDate.toISOString() },
            });
        }
    }

    // Max date
    if (rules.maxDate) {
        const maxDate = rules.maxDate === 'today' 
            ? today 
            : new Date(rules.maxDate);
        if (date > maxDate) {
            errors.push({
                ruleKey: 'maxDate',
                message: `Date must be on or before ${maxDate.toLocaleDateString()}`,
                messageKey: 'validation.date.maxDate',
                params: { date: maxDate.toISOString() },
            });
        }
    }

    // Minimum age
    if (rules.minimumAge !== undefined && rules.minimumAge > 0) {
        const age = getAge(date);
        if (age < rules.minimumAge) {
            errors.push({
                ruleKey: 'minimumAge',
                message: `You must be at least ${rules.minimumAge} years old`,
                messageKey: 'validation.date.minimumAge',
                params: { min: rules.minimumAge },
            });
        }
    }

    // Maximum age
    if (rules.maximumAge !== undefined && rules.maximumAge > 0) {
        const age = getAge(date);
        if (age > rules.maximumAge) {
            errors.push({
                ruleKey: 'maximumAge',
                message: `You cannot be older than ${rules.maximumAge} years`,
                messageKey: 'validation.date.maximumAge',
                params: { max: rules.maximumAge },
            });
        }
    }

    // Weekdays only
    if (rules.weekdaysOnly) {
        const dayOfWeek = date.getDay();
        if (dayOfWeek === 0 || dayOfWeek === 6) {
            errors.push({
                ruleKey: 'weekdaysOnly',
                message: 'Please select a weekday (Monday-Friday)',
                messageKey: 'validation.date.weekdaysOnly',
            });
        }
    }

    return errors;
}

/**
 * Calculate age from a birthdate
 */
function getAge(birthDate: Date): number {
    const today = new Date();
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();
    
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }
    
    return age;
}

// ═══════════════════════════════════════════════════════════════════════════
// MAIN VALIDATION FUNCTION
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Validate a field value against its rules
 * 
 * @param value - The field value to validate
 * @param rules - Validation rules to apply
 * @param componentType - Type of component (text, email, number, etc.)
 * @param context - Optional context (country, language)
 * @returns ValidationResult with errors, sanitized value, and auto-fixes
 */
export function validateField(
    value: unknown,
    rules: ValidationRules,
    componentType: string,
    context?: ValidationContext
): ValidationResult {
    const result: ValidationResult = {
        isValid: true,
        errors: [],
        autoFixesApplied: [],
    };

    // Handle required check first
    const isEmpty = value === undefined || value === null || value === '';
    
    if (rules.required && isEmpty) {
        result.isValid = false;
        result.errors.push({
            ruleKey: 'required',
            message: 'This field is required',
            messageKey: 'validation.general.required',
        });
        return result;
    }

    // If empty and not required, skip further validation
    if (isEmpty) {
        return result;
    }

    // Apply auto-fixes for string values
    let processedValue = value;
    if (typeof value === 'string') {
        const { sanitizedValue, fixes } = applyAutoFixes(value, rules, componentType);
        processedValue = sanitizedValue;
        result.sanitizedValue = sanitizedValue;
        result.autoFixesApplied = fixes;
    }

    // Route to appropriate validator based on component type
    let errors: ValidationError[] = [];

    switch (componentType) {
        case 'text':
        case 'textarea':
        case 'first-name':
            errors = validateText(processedValue as string, rules, context);
            break;

        case 'number': {
            const numValue = typeof processedValue === 'number'
                ? processedValue
                : parseFloat(processedValue as string);
            if (isNaN(numValue)) {
                errors.push({
                    ruleKey: 'number',
                    message: 'Please enter a valid number',
                    messageKey: 'validation.number.format',
                });
            } else {
                errors = validateNumber(numValue, rules);
            }
            break;
        }

        case 'email':
            errors = validateEmail(processedValue as string, rules);
            break;

        case 'url':
            errors = validateUrl(processedValue as string, rules, context);
            break;

        case 'phone':
            errors = validatePhoneNumber(processedValue as string, rules, context);
            break;

        case 'date':
            errors = validateDate(processedValue as string, rules, context);
            break;

        default:
            // Generic text validation for unknown types
            if (typeof processedValue === 'string') {
                errors = validateText(processedValue, rules, context);
            }
    }

    result.errors = errors;
    result.isValid = errors.length === 0;

    return result;
}

/**
 * Validate a form field and return a simple boolean
 */
export function isFieldValid(
    value: unknown,
    rules: ValidationRules,
    componentType: string,
    context?: ValidationContext
): boolean {
    return validateField(value, rules, componentType, context).isValid;
}

/**
 * Get the first error message for a field
 */
export function getFirstError(
    value: unknown,
    rules: ValidationRules,
    componentType: string,
    context?: ValidationContext
): string | null {
    const result = validateField(value, rules, componentType, context);
    return result.errors[0]?.message || null;
}

export default {
    validateField,
    isFieldValid,
    getFirstError,
    applyAutoFixes,
};

