/**
 * Phone Validation Utilities - Phase 1
 * 
 * Uses libphonenumber-js for proper international phone number validation.
 * Provides utilities for validation, formatting, and country detection.
 */

import {
    parsePhoneNumber,
    isValidPhoneNumber,
    CountryCode,
    getCountryCallingCode,
    getExampleNumber,
    AsYouType,
    PhoneNumber,
} from 'libphonenumber-js';

/**
 * Phone validation configuration
 */
export interface PhoneValidationConfig {
    /** Must include country code (+XX) */
    countryCodeRequired?: boolean;
    /** Only accept phone numbers from these countries (ISO codes) */
    allowedCountries?: string[];
    /** Only accept mobile numbers (reject landlines) */
    mobileOnly?: boolean;
    /** Default country for parsing (when no country code) */
    defaultCountry?: CountryCode;
}

/**
 * Validation result
 */
export interface PhoneValidationResult {
    isValid: boolean;
    errors: string[];
    /** Parsed phone number (if valid) */
    phoneNumber?: PhoneNumber;
    /** Detected country code */
    country?: CountryCode;
    /** Is this a mobile number */
    isMobile?: boolean;
    /** Formatted number */
    formatted?: {
        international: string;
        national: string;
        e164: string;
    };
}

/**
 * Common country codes for quick selection
 */
export const COMMON_COUNTRIES: { code: CountryCode; name: string; dialCode: string }[] = [
    { code: 'US', name: 'United States', dialCode: '+1' },
    { code: 'GB', name: 'United Kingdom', dialCode: '+44' },
    { code: 'AU', name: 'Australia', dialCode: '+61' },
    { code: 'CA', name: 'Canada', dialCode: '+1' },
    { code: 'DE', name: 'Germany', dialCode: '+49' },
    { code: 'FR', name: 'France', dialCode: '+33' },
    { code: 'IT', name: 'Italy', dialCode: '+39' },
    { code: 'ES', name: 'Spain', dialCode: '+34' },
    { code: 'NL', name: 'Netherlands', dialCode: '+31' },
    { code: 'BE', name: 'Belgium', dialCode: '+32' },
    { code: 'CH', name: 'Switzerland', dialCode: '+41' },
    { code: 'AT', name: 'Austria', dialCode: '+43' },
    { code: 'SE', name: 'Sweden', dialCode: '+46' },
    { code: 'NO', name: 'Norway', dialCode: '+47' },
    { code: 'DK', name: 'Denmark', dialCode: '+45' },
    { code: 'FI', name: 'Finland', dialCode: '+358' },
    { code: 'IE', name: 'Ireland', dialCode: '+353' },
    { code: 'NZ', name: 'New Zealand', dialCode: '+64' },
    { code: 'SG', name: 'Singapore', dialCode: '+65' },
    { code: 'HK', name: 'Hong Kong', dialCode: '+852' },
    { code: 'JP', name: 'Japan', dialCode: '+81' },
    { code: 'KR', name: 'South Korea', dialCode: '+82' },
    { code: 'CN', name: 'China', dialCode: '+86' },
    { code: 'IN', name: 'India', dialCode: '+91' },
    { code: 'BR', name: 'Brazil', dialCode: '+55' },
    { code: 'MX', name: 'Mexico', dialCode: '+52' },
    { code: 'ZA', name: 'South Africa', dialCode: '+27' },
    { code: 'AE', name: 'UAE', dialCode: '+971' },
    { code: 'SA', name: 'Saudi Arabia', dialCode: '+966' },
];

/**
 * Validate a phone number against configuration
 */
export function validatePhone(
    value: string,
    config: PhoneValidationConfig = {}
): PhoneValidationResult {
    const errors: string[] = [];
    const result: PhoneValidationResult = { isValid: false, errors };

    if (!value || value.trim() === '') {
        errors.push('Phone number is required');
        return result;
    }

    const cleanValue = value.trim();

    // Check if country code is required
    if (config.countryCodeRequired && !cleanValue.startsWith('+')) {
        errors.push('Country code is required (e.g., +1 for US)');
        return result;
    }

    try {
        // Try to parse the phone number
        const phoneNumber = parsePhoneNumber(cleanValue, config.defaultCountry);

        if (!phoneNumber) {
            errors.push('Invalid phone number format');
            return result;
        }

        // Check if it's a valid phone number
        if (!phoneNumber.isValid()) {
            errors.push('Invalid phone number');
            return result;
        }

        const country = phoneNumber.country;

        // Check allowed countries
        if (config.allowedCountries && config.allowedCountries.length > 0) {
            if (!country || !config.allowedCountries.includes(country)) {
                const allowedNames = config.allowedCountries
                    .map(c => COMMON_COUNTRIES.find(cc => cc.code === c)?.name || c)
                    .join(', ');
                errors.push(`Phone number must be from: ${allowedNames}`);
                return result;
            }
        }

        // Check if mobile only
        const numberType = phoneNumber.getType();
        const isMobile = numberType === 'MOBILE' || numberType === 'FIXED_LINE_OR_MOBILE';

        if (config.mobileOnly && !isMobile) {
            errors.push('Only mobile phone numbers are accepted');
            return result;
        }

        // Valid!
        result.isValid = true;
        result.phoneNumber = phoneNumber;
        result.country = country;
        result.isMobile = isMobile;
        result.formatted = {
            international: phoneNumber.formatInternational(),
            national: phoneNumber.formatNational(),
            e164: phoneNumber.format('E.164'),
        };

    } catch (error) {
        errors.push('Invalid phone number format');
    }

    return result;
}

/**
 * Format a phone number as you type
 */
export function formatAsYouType(
    value: string,
    country?: CountryCode
): string {
    if (!value) return '';
    const formatter = new AsYouType(country);
    return formatter.input(value);
}

/**
 * Format a phone number to a specific format
 */
export function formatPhone(
    value: string,
    format: 'international' | 'national' | 'e164' = 'international',
    defaultCountry?: CountryCode
): string {
    try {
        const phoneNumber = parsePhoneNumber(value, defaultCountry);
        if (!phoneNumber || !phoneNumber.isValid()) return value;

        switch (format) {
            case 'international':
                return phoneNumber.formatInternational();
            case 'national':
                return phoneNumber.formatNational();
            case 'e164':
                return phoneNumber.format('E.164');
            default:
                return phoneNumber.formatInternational();
        }
    } catch {
        return value;
    }
}

/**
 * Get an example phone number for a country
 */
export function getExamplePhoneNumber(country: CountryCode): string {
    try {
        const example = getExampleNumber(country);
        return example ? example.formatInternational() : '';
    } catch {
        return '';
    }
}

/**
 * Get the calling code for a country
 */
export function getCountryDialCode(country: CountryCode): string {
    try {
        return `+${getCountryCallingCode(country)}`;
    } catch {
        return '';
    }
}

/**
 * Detect the country from a phone number
 */
export function detectCountry(value: string): CountryCode | undefined {
    try {
        const phoneNumber = parsePhoneNumber(value);
        return phoneNumber?.country;
    } catch {
        return undefined;
    }
}

/**
 * Check if a string looks like a phone number (basic check)
 */
export function looksLikePhoneNumber(value: string): boolean {
    // Remove common formatting characters
    const cleaned = value.replace(/[\s\-().+]/g, '');
    // Should be mostly digits, 7-15 characters
    return /^\d{7,15}$/.test(cleaned);
}

export default {
    validatePhone,
    formatAsYouType,
    formatPhone,
    getExamplePhoneNumber,
    getCountryDialCode,
    detectCountry,
    looksLikePhoneNumber,
    COMMON_COUNTRIES,
};

