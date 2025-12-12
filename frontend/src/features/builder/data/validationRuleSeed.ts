/**
 * Validation Rule Seed Data - Phase 2
 * 
 * Hardcoded seed data matching future database records.
 * This will be replaced with API calls when the backend is implemented.
 * 
 * Structure mirrors:
 * - config.ValidationRule table
 * - ref.Country table
 * 
 * @see docs/database-schema.md
 */

import { 
    ValidationRuleDefinition, 
    CountryValidationConfig, 
    RuleEducationalInfo,
    RuleEducationalMap 
} from '../types/validationRule.types';

// ═══════════════════════════════════════════════════════════════════════════
// COUNTRY VALIDATION CONFIGS
// ═══════════════════════════════════════════════════════════════════════════

export const COUNTRY_CONFIGS: CountryValidationConfig[] = [
    // Australia
    {
        countryId: 13,
        countryCode: 'AU',
        countryName: 'Australia',
        phonePrefix: '+61',
        dateFormat: 'DD/MM/YYYY',
        currencyCode: 'AUD',
        nameCharacterSet: 'latin',
        minNameLength: 2,
        isRtl: false,
        phoneDisplayFormat: '+61 X XXXX XXXX',
        phoneExample: '+61 412 345 678',
        postalCodePattern: '^\\d{4}$',
        postalCodeExample: '2000',
    },
    // United States
    {
        countryId: 1,
        countryCode: 'US',
        countryName: 'United States',
        phonePrefix: '+1',
        dateFormat: 'MM/DD/YYYY',
        currencyCode: 'USD',
        nameCharacterSet: 'latin',
        minNameLength: 2,
        isRtl: false,
        phoneDisplayFormat: '+1 (XXX) XXX-XXXX',
        phoneExample: '+1 (555) 123-4567',
        postalCodePattern: '^\\d{5}(-\\d{4})?$',
        postalCodeExample: '90210',
    },
    // United Kingdom
    {
        countryId: 2,
        countryCode: 'GB',
        countryName: 'United Kingdom',
        phonePrefix: '+44',
        dateFormat: 'DD/MM/YYYY',
        currencyCode: 'GBP',
        nameCharacterSet: 'latin',
        minNameLength: 2,
        isRtl: false,
        phoneDisplayFormat: '+44 XXXX XXXXXX',
        phoneExample: '+44 7911 123456',
        postalCodePattern: '^[A-Z]{1,2}\\d[A-Z\\d]? ?\\d[A-Z]{2}$',
        postalCodeExample: 'SW1A 1AA',
    },
    // Germany
    {
        countryId: 3,
        countryCode: 'DE',
        countryName: 'Germany',
        phonePrefix: '+49',
        dateFormat: 'DD/MM/YYYY',
        currencyCode: 'EUR',
        nameCharacterSet: 'latin',
        minNameLength: 2,
        isRtl: false,
        phoneDisplayFormat: '+49 XXX XXXXXXXX',
        phoneExample: '+49 151 12345678',
        postalCodePattern: '^\\d{5}$',
        postalCodeExample: '10115',
    },
    // France
    {
        countryId: 4,
        countryCode: 'FR',
        countryName: 'France',
        phonePrefix: '+33',
        dateFormat: 'DD/MM/YYYY',
        currencyCode: 'EUR',
        nameCharacterSet: 'latin',
        minNameLength: 2,
        isRtl: false,
        phoneDisplayFormat: '+33 X XX XX XX XX',
        phoneExample: '+33 6 12 34 56 78',
        postalCodePattern: '^\\d{5}$',
        postalCodeExample: '75001',
    },
    // Japan
    {
        countryId: 5,
        countryCode: 'JP',
        countryName: 'Japan',
        phonePrefix: '+81',
        dateFormat: 'YYYY-MM-DD',
        currencyCode: 'JPY',
        nameCharacterSet: 'cjk',
        minNameLength: 1,
        isRtl: false,
        phoneDisplayFormat: '+81 XX-XXXX-XXXX',
        phoneExample: '+81 90-1234-5678',
        postalCodePattern: '^\\d{3}-\\d{4}$',
        postalCodeExample: '100-0001',
    },
    // China
    {
        countryId: 6,
        countryCode: 'CN',
        countryName: 'China',
        phonePrefix: '+86',
        dateFormat: 'YYYY-MM-DD',
        currencyCode: 'CNY',
        nameCharacterSet: 'cjk',
        minNameLength: 2,
        isRtl: false,
        phoneDisplayFormat: '+86 XXX XXXX XXXX',
        phoneExample: '+86 138 1234 5678',
        postalCodePattern: '^\\d{6}$',
        postalCodeExample: '100000',
    },
    // Saudi Arabia
    {
        countryId: 7,
        countryCode: 'SA',
        countryName: 'Saudi Arabia',
        phonePrefix: '+966',
        dateFormat: 'DD/MM/YYYY',
        currencyCode: 'SAR',
        nameCharacterSet: 'arabic',
        minNameLength: 2,
        isRtl: true,
        phoneDisplayFormat: '+966 XX XXX XXXX',
        phoneExample: '+966 50 123 4567',
        postalCodePattern: '^\\d{5}$',
        postalCodeExample: '11564',
    },
    // United Arab Emirates
    {
        countryId: 8,
        countryCode: 'AE',
        countryName: 'United Arab Emirates',
        phonePrefix: '+971',
        dateFormat: 'DD/MM/YYYY',
        currencyCode: 'AED',
        nameCharacterSet: 'mixed',
        minNameLength: 2,
        isRtl: true,
        phoneDisplayFormat: '+971 XX XXX XXXX',
        phoneExample: '+971 50 123 4567',
        postalCodePattern: '^\\d{5}$',
        postalCodeExample: '00000',
    },
    // India
    {
        countryId: 9,
        countryCode: 'IN',
        countryName: 'India',
        phonePrefix: '+91',
        dateFormat: 'DD/MM/YYYY',
        currencyCode: 'INR',
        nameCharacterSet: 'mixed',
        minNameLength: 2,
        isRtl: false,
        phoneDisplayFormat: '+91 XXXXX XXXXX',
        phoneExample: '+91 98765 43210',
        postalCodePattern: '^\\d{6}$',
        postalCodeExample: '110001',
    },
    // New Zealand
    {
        countryId: 10,
        countryCode: 'NZ',
        countryName: 'New Zealand',
        phonePrefix: '+64',
        dateFormat: 'DD/MM/YYYY',
        currencyCode: 'NZD',
        nameCharacterSet: 'latin',
        minNameLength: 2,
        isRtl: false,
        phoneDisplayFormat: '+64 XX XXX XXXX',
        phoneExample: '+64 21 123 4567',
        postalCodePattern: '^\\d{4}$',
        postalCodeExample: '1010',
    },
    // Singapore
    {
        countryId: 11,
        countryCode: 'SG',
        countryName: 'Singapore',
        phonePrefix: '+65',
        dateFormat: 'DD/MM/YYYY',
        currencyCode: 'SGD',
        nameCharacterSet: 'mixed',
        minNameLength: 2,
        isRtl: false,
        phoneDisplayFormat: '+65 XXXX XXXX',
        phoneExample: '+65 9123 4567',
        postalCodePattern: '^\\d{6}$',
        postalCodeExample: '018956',
    },
    // Canada
    {
        countryId: 12,
        countryCode: 'CA',
        countryName: 'Canada',
        phonePrefix: '+1',
        dateFormat: 'DD/MM/YYYY',
        currencyCode: 'CAD',
        nameCharacterSet: 'latin',
        minNameLength: 2,
        isRtl: false,
        phoneDisplayFormat: '+1 (XXX) XXX-XXXX',
        phoneExample: '+1 (416) 123-4567',
        postalCodePattern: '^[A-Z]\\d[A-Z] ?\\d[A-Z]\\d$',
        postalCodeExample: 'M5V 3L9',
    },
];

// ═══════════════════════════════════════════════════════════════════════════
// VALIDATION RULE DEFINITIONS WITH EDUCATIONAL CONTENT
// ═══════════════════════════════════════════════════════════════════════════

export const VALIDATION_RULES: ValidationRuleDefinition[] = [
    // ─────────────────────────────────────────────────────────────────────
    // TEXT RULES
    // ─────────────────────────────────────────────────────────────────────
    {
        ruleKey: 'minLength',
        ruleTypeId: 1,
        ruleTypeCode: 'text',
        validationMessage: 'Must be at least {min} characters',
        messageKey: 'validation.text.minLength',
        description: 'Minimum character length requirement',
        priority: 10,
        sortOrder: 1,
        isActive: true,
        pros: [
            'Ensures meaningful input (not just initials)',
            'Prevents accidental partial submissions',
            'Helps collect usable data for follow-up',
        ],
        cons: [
            'May frustrate mobile users with small keyboards',
            'Can block valid short names (e.g., "Li", "Wu")',
            'Some cultures have single-character names',
        ],
        bestFor: 'Fields requiring complete information (addresses, descriptions)',
        example: 'Min Length: 3 → "Jo" ❌ fails, "Joe" ✓ passes',
        canAutoFix: false,
        autoFixDefault: false,
    },
    {
        ruleKey: 'maxLength',
        ruleTypeId: 1,
        ruleTypeCode: 'text',
        validationMessage: 'Must be no more than {max} characters',
        messageKey: 'validation.text.maxLength',
        description: 'Maximum character length limit',
        priority: 10,
        sortOrder: 2,
        isActive: true,
        pros: [
            'Prevents database overflow issues',
            'Keeps data consistent for exports',
            'Enables smart input field sizing',
        ],
        cons: [
            'May truncate legitimate long entries',
            'Frustrating if limit is too restrictive',
        ],
        bestFor: 'Structured data fields (names, codes, reference numbers)',
        example: 'Max Length: 50 → Limits name field to 50 characters',
        canAutoFix: false,
        autoFixDefault: false,
    },
    {
        ruleKey: 'alpha',
        ruleTypeId: 1,
        ruleTypeCode: 'text',
        validationPattern: '^[\\p{L}]+$',
        validationMessage: 'Only letters are allowed',
        messageKey: 'validation.text.alpha',
        description: 'Letters only (Unicode-aware)',
        priority: 20,
        sortOrder: 3,
        isActive: true,
        pros: [
            'Ensures clean name data',
            'Prevents injection of special characters',
            'Works with international alphabets (Unicode)',
        ],
        cons: [
            'Blocks hyphenated names (O\'Brien, Mary-Jane)',
            'Blocks names with apostrophes',
            'May need exceptions for spaces in names',
        ],
        bestFor: 'Single-word fields like first name, last name (without spaces)',
        warning: 'Consider allowing hyphens and apostrophes for names',
        example: '"John" ✓ | "John123" ❌ | "日本語" ✓ (Unicode letters)',
        canAutoFix: false,
        autoFixDefault: false,
    },
    {
        ruleKey: 'alphanumeric',
        ruleTypeId: 1,
        ruleTypeCode: 'text',
        validationPattern: '^[\\p{L}\\p{N}]+$',
        validationMessage: 'Only letters and numbers are allowed',
        messageKey: 'validation.text.alphanumeric',
        description: 'Letters and numbers only (Unicode-aware). Includes all letters, so "Letters Only" is redundant when this is enabled.',
        priority: 20,
        sortOrder: 4,
        isActive: true,
        pros: [
            'Good for reference codes and IDs',
            'Prevents special character injection',
            'Clean data for system integration',
        ],
        cons: [
            'Blocks common separators (dashes, underscores)',
            'May be too restrictive for some use cases',
        ],
        bestFor: 'Order numbers, product codes, usernames',
        example: '"ABC123" ✓ | "ABC-123" ❌ | "ABC 123" ❌',
        canAutoFix: false,
        autoFixDefault: false,
    },
    {
        ruleKey: 'trimWhitespace',
        ruleTypeId: 1,
        ruleTypeCode: 'formatting',
        validationMessage: 'Leading and trailing spaces will be removed',
        messageKey: 'validation.formatting.trim',
        description: 'Auto-remove leading/trailing whitespace only (at start and end). Does NOT affect spaces between words.',
        priority: 5,
        sortOrder: 10,
        isActive: true,
        pros: [
            'Cleans up accidental spaces from copy/paste',
            'Consistent data without user effort',
            'Prevents "hidden" validation failures',
        ],
        cons: [
            'User may not realize input was modified',
            'Rare edge case: intentional leading space',
        ],
        bestFor: 'All text fields - should be enabled by default',
        example: '"  John Smith  " → "John Smith" (edges trimmed only)',
        canAutoFix: true,
        autoFixDefault: true,
        autoFixDescription: 'Automatically removes spaces at the start and end of input',
    },
    {
        ruleKey: 'noConsecutiveSpaces',
        ruleTypeId: 1,
        ruleTypeCode: 'formatting',
        validationMessage: 'Multiple consecutive spaces are not allowed',
        messageKey: 'validation.formatting.noConsecutiveSpaces',
        description: 'Prevent multiple spaces in a row (between words). This is separate from Trim Whitespace which only handles edges.',
        priority: 5,
        sortOrder: 11,
        isActive: true,
        pros: [
            'Cleaner data for display and export',
            'Fixes common typing mistakes',
            'Better for search and matching',
        ],
        cons: [
            'Very rare: some formatted text needs multiple spaces',
        ],
        bestFor: 'All text fields - typically auto-fixed rather than validated',
        example: '"John  Smith" → "John Smith" (double space reduced)',
        canAutoFix: true,
        autoFixDefault: true,
        autoFixDescription: 'Automatically reduces multiple spaces to a single space',
    },
    {
        ruleKey: 'noHtmlScript',
        ruleTypeId: 1,
        ruleTypeCode: 'security',
        validationPattern: '<[^>]*>|<script|javascript:|on\\w+=',
        validationMessage: 'HTML tags and scripts are not allowed',
        messageKey: 'validation.security.noHtml',
        description: 'Block HTML tags and script content (XSS prevention)',
        priority: 1,
        sortOrder: 20,
        isActive: true,
        pros: [
            'Critical security protection against XSS attacks',
            'Protects your database and other users',
            'Required for public-facing forms',
        ],
        cons: [
            'May block legitimate angle brackets in text',
            'Could frustrate technical users',
        ],
        bestFor: 'All public-facing forms - essential security measure',
        warning: 'Disabling this rule may expose your form to security vulnerabilities',
        example: '"<script>alert()</script>" ❌ | "I love coding" ✓',
        canAutoFix: false,
        autoFixDefault: false,
    },
    {
        ruleKey: 'caseTransform',
        ruleTypeId: 1,
        ruleTypeCode: 'formatting',
        validationMessage: 'Text will be converted to {format} case',
        messageKey: 'validation.formatting.caseTransform',
        description: 'Auto-transform text case',
        priority: 5,
        sortOrder: 12,
        isActive: true,
        pros: [
            'Consistent data formatting',
            'Proper capitalization without user effort',
            'Better for display and reports',
        ],
        cons: [
            'May incorrectly change names (McDonald → Mcdonald)',
            'Acronyms may be incorrectly cased',
            'Some names have specific casing (de Vil, van Gogh)',
        ],
        bestFor: 'Email (lowercase), company names (titlecase)',
        warning: 'Use with caution on names - some have unusual capitalization',
        example: 'Title Case: "john smith" → "John Smith"',
        canAutoFix: true,
        autoFixDefault: false,
        autoFixDescription: 'Automatically adjusts capitalization based on selected format',
    },

    // ─────────────────────────────────────────────────────────────────────
    // NUMBER RULES
    // ─────────────────────────────────────────────────────────────────────
    {
        ruleKey: 'minValue',
        ruleTypeId: 2,
        ruleTypeCode: 'number',
        validationMessage: 'Must be at least {min}',
        messageKey: 'validation.number.minValue',
        description: 'Minimum numeric value',
        priority: 10,
        sortOrder: 1,
        isActive: true,
        pros: [
            'Ensures values are within valid range',
            'Prevents data entry errors',
            'Good for quantities, ages, amounts',
        ],
        cons: [
            'May reject legitimate edge cases',
            'Consider if zero or negative is valid',
        ],
        bestFor: 'Quantities, ages, prices, ratings',
        canAutoFix: false,
        autoFixDefault: false,
    },
    {
        ruleKey: 'maxValue',
        ruleTypeId: 2,
        ruleTypeCode: 'number',
        validationMessage: 'Must be no more than {max}',
        messageKey: 'validation.number.maxValue',
        description: 'Maximum numeric value',
        priority: 10,
        sortOrder: 2,
        isActive: true,
        pros: [
            'Prevents unrealistic values',
            'Protects against data entry errors',
            'Useful for ratings, percentages, limits',
        ],
        cons: [
            'May need updating as limits change',
        ],
        bestFor: 'Ratings (1-5), percentages (0-100), quantities with limits',
        canAutoFix: false,
        autoFixDefault: false,
    },
    {
        ruleKey: 'integerOnly',
        ruleTypeId: 2,
        ruleTypeCode: 'number',
        validationMessage: 'Must be a whole number (no decimals)',
        messageKey: 'validation.number.integerOnly',
        description: 'No decimal values allowed',
        priority: 15,
        sortOrder: 3,
        isActive: true,
        pros: [
            'Clean data for counts and quantities',
            'Avoids precision issues in calculations',
            'Simpler data handling',
        ],
        cons: [
            'Cannot accept fractional values',
            'May not suit all numeric data',
        ],
        bestFor: 'Quantities, counts, years, ages',
        canAutoFix: false,
        autoFixDefault: false,
    },
    {
        ruleKey: 'positiveOnly',
        ruleTypeId: 2,
        ruleTypeCode: 'number',
        validationMessage: 'Must be a positive number (greater than zero)',
        messageKey: 'validation.number.positiveOnly',
        description: 'Must be greater than zero',
        priority: 15,
        sortOrder: 5,
        isActive: true,
        pros: [
            'Ensures meaningful positive values',
            'Good for quantities, prices, ratings',
        ],
        cons: [
            'Excludes zero which may be valid',
            'No negative values even if meaningful',
        ],
        bestFor: 'Prices, quantities to order, ratings',
        canAutoFix: false,
        autoFixDefault: false,
    },

    // ─────────────────────────────────────────────────────────────────────
    // EMAIL RULES
    // ─────────────────────────────────────────────────────────────────────
    {
        ruleKey: 'email',
        ruleTypeId: 3,
        ruleTypeCode: 'email',
        validationPattern: '^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$',
        validationMessage: 'Please enter a valid email address',
        messageKey: 'validation.email.format',
        description: 'Valid email format',
        priority: 10,
        sortOrder: 1,
        isActive: true,
        pros: [
            'Ensures email has correct structure',
            'Catches obvious typos',
            'Required for email delivery',
        ],
        cons: [
            'Cannot verify email actually exists',
            'Some valid emails have unusual formats',
        ],
        bestFor: 'All email fields - essential validation',
        example: '"john@company.com" ✓ | "john@company" ❌ | "john.com" ❌',
        canAutoFix: true,
        autoFixDefault: true,
        autoFixDescription: 'Converts email to lowercase and trims whitespace',
    },
    {
        ruleKey: 'businessEmailOnly',
        ruleTypeId: 3,
        ruleTypeCode: 'email',
        validationMessage: 'Please use a business email (not Gmail, Yahoo, etc.)',
        messageKey: 'validation.email.businessOnly',
        description: 'Block free email providers',
        priority: 20,
        sortOrder: 2,
        isActive: true,
        pros: [
            'Higher quality B2B leads',
            'Filters out personal inquiries',
            'Better for enterprise sales',
        ],
        cons: [
            'Excludes freelancers and consultants',
            'May lose legitimate business prospects',
            'Small businesses often use free email',
            'Startups may not have custom domains',
        ],
        bestFor: 'B2B lead forms, enterprise contacts',
        warning: 'May significantly reduce form submissions',
        example: '"john@company.com" ✓ | "john@gmail.com" ❌',
        canAutoFix: false,
        autoFixDefault: false,
    },
    {
        ruleKey: 'noDisposableEmail',
        ruleTypeId: 3,
        ruleTypeCode: 'email',
        validationMessage: 'Temporary email addresses are not allowed',
        messageKey: 'validation.email.noDisposable',
        description: 'Block known disposable/temporary email services',
        priority: 20,
        sortOrder: 3,
        isActive: true,
        pros: [
            'Prevents spam and fake submissions',
            'Ensures you can follow up with leads',
            'Higher quality contact database',
        ],
        cons: [
            'Privacy-conscious users may be blocked',
            'Disposable email list needs maintenance',
            'New disposable services may not be blocked',
        ],
        bestFor: 'Lead capture forms, registration forms',
        example: '"john@mailinator.com" ❌ | "john@tempmail.com" ❌',
        canAutoFix: false,
        autoFixDefault: false,
    },
    {
        ruleKey: 'noPlusAddressing',
        ruleTypeId: 3,
        ruleTypeCode: 'email',
        validationPattern: '\\+[^@]*@',
        validationMessage: 'Plus addressing (email+tag@) is not allowed',
        messageKey: 'validation.email.noPlusAddressing',
        description: 'Block email+tag@domain format',
        priority: 20,
        sortOrder: 4,
        isActive: true,
        pros: [
            'Prevents duplicate submissions from same person',
            'Blocks common spam filtering technique',
        ],
        cons: [
            'Blocks legitimate email organization',
            'Power users may be frustrated',
            'Some businesses use plus addressing',
        ],
        bestFor: 'Competition entries, one-per-person offers',
        example: '"john+promo@gmail.com" ❌ | "john@gmail.com" ✓',
        canAutoFix: false,
        autoFixDefault: false,
    },

    // ─────────────────────────────────────────────────────────────────────
    // PHONE RULES
    // ─────────────────────────────────────────────────────────────────────
    {
        ruleKey: 'phone',
        ruleTypeId: 4,
        ruleTypeCode: 'phone',
        validationMessage: 'Please enter a valid phone number',
        messageKey: 'validation.phone.format',
        description: 'Valid phone number structure',
        priority: 10,
        sortOrder: 1,
        isActive: true,
        pros: [
            'Ensures phone number is properly formatted',
            'Validates against known phone number patterns',
            'Works with international formats',
        ],
        cons: [
            'Some valid numbers may be rejected',
            'New area codes may not be recognized',
        ],
        bestFor: 'All phone number fields',
        example: '"+61 412 345 678" ✓ | "0412345678" ✓ (AU)',
        canAutoFix: true,
        autoFixDefault: false,
        autoFixDescription: 'Formats phone number with proper spacing',
    },
    {
        ruleKey: 'countryCodeRequired',
        ruleTypeId: 4,
        ruleTypeCode: 'phone',
        validationMessage: 'Please include country code (e.g., +61 for Australia)',
        messageKey: 'validation.phone.countryCodeRequired',
        description: 'Must include +XX country prefix',
        priority: 15,
        sortOrder: 2,
        isActive: true,
        pros: [
            'Ensures international dialing works',
            'Unambiguous phone number storage',
            'Required for SMS/WhatsApp integration',
        ],
        cons: [
            'Extra effort for users in local forms',
            'Some users don\'t know their country code',
        ],
        bestFor: 'International events, SMS notifications',
        example: '"+61 412 345 678" ✓ | "0412 345 678" ❌ (missing +61)',
        canAutoFix: false,
        autoFixDefault: false,
    },
    {
        ruleKey: 'mobileOnly',
        ruleTypeId: 4,
        ruleTypeCode: 'phone',
        validationMessage: 'Please enter a mobile phone number',
        messageKey: 'validation.phone.mobileOnly',
        description: 'Only accept mobile numbers (reject landlines)',
        priority: 20,
        sortOrder: 3,
        isActive: true,
        pros: [
            'Ensures SMS delivery is possible',
            'Better for mobile marketing',
            'More likely to be personal contact',
        ],
        cons: [
            'Excludes office/business landlines',
            'Some attendees prefer office numbers',
            'Detection not 100% accurate',
        ],
        bestFor: 'SMS campaigns, mobile app follow-up',
        example: '"+61 412 345 678" ✓ (mobile) | "+61 2 9876 5432" ❌ (landline)',
        canAutoFix: false,
        autoFixDefault: false,
    },

    // ─────────────────────────────────────────────────────────────────────
    // DATE RULES
    // ─────────────────────────────────────────────────────────────────────
    {
        ruleKey: 'futureOnly',
        ruleTypeId: 5,
        ruleTypeCode: 'date',
        validationMessage: 'Date must be in the future',
        messageKey: 'validation.date.futureOnly',
        description: 'Date must be after today',
        priority: 15,
        sortOrder: 1,
        isActive: true,
        pros: [
            'Ensures booking/event dates are valid',
            'Prevents expired date selection',
        ],
        cons: [
            'Cannot be used for birthdates',
            'Time zone considerations',
        ],
        bestFor: 'Event dates, booking dates, deadlines',
        canAutoFix: false,
        autoFixDefault: false,
    },
    {
        ruleKey: 'pastOnly',
        ruleTypeId: 5,
        ruleTypeCode: 'date',
        validationMessage: 'Date must be in the past',
        messageKey: 'validation.date.pastOnly',
        description: 'Date must be before today',
        priority: 15,
        sortOrder: 2,
        isActive: true,
        pros: [
            'Ensures birthdates and historical dates are valid',
            'Prevents invalid future dates',
        ],
        cons: [
            'Cannot be used for future events',
        ],
        bestFor: 'Birthdates, start dates, historical dates',
        canAutoFix: false,
        autoFixDefault: false,
    },
    {
        ruleKey: 'minimumAge',
        ruleTypeId: 5,
        ruleTypeCode: 'date',
        validationMessage: 'You must be at least {min} years old',
        messageKey: 'validation.date.minimumAge',
        description: 'User must be at least N years old',
        priority: 20,
        sortOrder: 3,
        isActive: true,
        pros: [
            'Legal compliance (alcohol, gambling, contracts)',
            'Age-restricted content protection',
            'Required for many industries',
        ],
        cons: [
            'Can be bypassed with fake dates',
            'May need additional verification',
        ],
        bestFor: 'Alcohol events (18/21), legal forms, age-restricted services',
        warning: 'Not a substitute for proper age verification systems',
        example: 'Min Age: 18 → Birthdate before today - 18 years required',
        canAutoFix: false,
        autoFixDefault: false,
    },
    {
        ruleKey: 'weekdaysOnly',
        ruleTypeId: 5,
        ruleTypeCode: 'date',
        validationMessage: 'Please select a weekday (Monday-Friday)',
        messageKey: 'validation.date.weekdaysOnly',
        description: 'No weekends allowed',
        priority: 15,
        sortOrder: 5,
        isActive: true,
        pros: [
            'Ensures business day selection',
            'Avoids weekend bookings',
        ],
        cons: [
            'Excludes weekend events',
            'Cultural considerations (different weekends globally)',
        ],
        bestFor: 'Business appointments, deliveries',
        warning: 'Some countries have different weekend days (Fri-Sat in Middle East)',
        canAutoFix: false,
        autoFixDefault: false,
    },

    // ─────────────────────────────────────────────────────────────────────
    // SELECTION RULES
    // ─────────────────────────────────────────────────────────────────────
    {
        ruleKey: 'minSelections',
        ruleTypeId: 6,
        ruleTypeCode: 'selection',
        validationMessage: 'Please select at least {min} options',
        messageKey: 'validation.selection.minSelections',
        description: 'Minimum number of selections required',
        priority: 10,
        sortOrder: 1,
        isActive: true,
        pros: [
            'Ensures meaningful checkbox responses',
            'Gathers required preference data',
        ],
        cons: [
            'May force users to select unwanted options',
            'Can frustrate users who only want one choice',
        ],
        bestFor: 'Interest surveys, topic selection',
        canAutoFix: false,
        autoFixDefault: false,
    },
    {
        ruleKey: 'maxSelections',
        ruleTypeId: 6,
        ruleTypeCode: 'selection',
        validationMessage: 'Please select no more than {max} options',
        messageKey: 'validation.selection.maxSelections',
        description: 'Maximum number of selections allowed',
        priority: 10,
        sortOrder: 2,
        isActive: true,
        pros: [
            'Limits choices to manageable number',
            'Useful for "pick your top 3" scenarios',
        ],
        cons: [
            'May frustrate users who want more options',
        ],
        bestFor: 'Priority ranking, limited choice surveys',
        canAutoFix: false,
        autoFixDefault: false,
    },
];

// ═══════════════════════════════════════════════════════════════════════════
// HELPER FUNCTIONS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Get educational info for a specific rule
 */
export function getRuleEducationalInfo(ruleKey: string): RuleEducationalInfo | undefined {
    const rule = VALIDATION_RULES.find(r => r.ruleKey === ruleKey);
    if (!rule) return undefined;
    
    return {
        ruleKey: rule.ruleKey,
        displayName: rule.description,
        description: rule.description,
        pros: rule.pros,
        cons: rule.cons,
        bestFor: rule.bestFor,
        warning: rule.warning,
        canAutoFix: rule.canAutoFix,
        autoFixDescription: rule.autoFixDescription,
        example: rule.example,
    };
}

/**
 * Get educational info for domain-related fields
 */
export function getDomainFieldInfo(fieldType: 'whitelist' | 'blacklist'): RuleEducationalInfo {
    if (fieldType === 'whitelist') {
        return {
            ruleKey: 'domainWhitelist',
            displayName: 'Allowed Domains',
            description: 'Only accept emails from these specific domains. Enter domain names separated by commas.',
            pros: [
                'Restrict to specific companies or partners',
                'Useful for internal forms',
                'High data quality for targeted audiences',
            ],
            cons: [
                'Users outside allowed domains cannot submit',
                'May need frequent updates as partners change',
            ],
            bestFor: 'Internal company forms, partner-only registrations',
            example: 'company.com, partner.org → Only these domains allowed',
            canAutoFix: false,
        };
    }
    return {
        ruleKey: 'domainBlacklist',
        displayName: 'Blocked Domains',
        description: 'Reject emails from these specific domains. Enter domain names separated by commas.',
        pros: [
            'Block known spam or competitor domains',
            'Prevent specific organizations from registering',
        ],
        cons: [
            'Must know domains to block in advance',
            'Determined users can use other emails',
        ],
        bestFor: 'Blocking known problematic domains',
        example: 'spam.com, fake.org → These domains rejected',
        canAutoFix: false,
    };
}

/**
 * Get educational info for Must Match Field
 */
export function getMustMatchFieldInfo(): RuleEducationalInfo {
    return {
        ruleKey: 'mustMatchField',
        displayName: 'Confirmation Field',
        description: 'Requires this field\'s value to exactly match another field. Use the Export Name of the field you want to match.',
        pros: [
            'Prevents typos in critical fields (email, password)',
            'Common UX pattern users understand',
            'Extra verification for important data',
        ],
        cons: [
            'Extra typing effort for users',
            'Annoying if overused',
        ],
        bestFor: 'Email confirmation, password confirmation',
        example: 'Field "Confirm Email" must match field "Email" (use Email\'s Export Name)',
        canAutoFix: false,
    };
}

/**
 * Get educational info for Blocked Characters field
 */
export function getBlockedCharactersInfo(): RuleEducationalInfo {
    return {
        ruleKey: 'blockedCharacters',
        displayName: 'Blocked Characters',
        description: 'Type characters directly without any separator. Each character you type will be blocked.',
        pros: [
            'Block specific problematic characters',
            'Prevent data formatting issues',
            'Custom character restrictions',
        ],
        cons: [
            'May confuse users if common characters blocked',
            'Error message should explain what\'s blocked',
        ],
        bestFor: 'Preventing special characters that cause export/database issues',
        example: '<>{}[]\\/ → Blocks each of these 8 characters individually',
        canAutoFix: false,
    };
}

/**
 * Get educational info for Export Name field
 */
export function getExportNameInfo(): RuleEducationalInfo {
    return {
        ruleKey: 'exportName',
        displayName: 'Export Field Name',
        description: 'The column header name when exporting form submissions to CSV. Must be unique and contain only letters, numbers, and underscores.',
        pros: [
            'Clear, consistent column names in exports',
            'Prevents CSV formatting issues',
            'Easy to identify data in spreadsheets',
        ],
        cons: [
            'Must be unique across all form fields',
            'Cannot contain spaces or special characters',
        ],
        bestFor: 'All fields that collect data',
        example: 'Label "First Name" → Export Name "FirstName" or "first_name"',
        warning: 'Changing this after collecting data may affect report consistency',
        canAutoFix: false,
    };
}

/**
 * Get all rule educational info as a map
 */
export function getRuleEducationalMap(): RuleEducationalMap {
    const map = new Map<string, RuleEducationalInfo>();
    
    for (const rule of VALIDATION_RULES) {
        map.set(rule.ruleKey, {
            ruleKey: rule.ruleKey,
            displayName: rule.description,
            description: rule.description,
            pros: rule.pros,
            cons: rule.cons,
            bestFor: rule.bestFor,
            warning: rule.warning,
            canAutoFix: rule.canAutoFix,
            autoFixDescription: rule.autoFixDescription,
        });
    }
    
    return map;
}

/**
 * Get country config by country code
 */
export function getCountryConfig(countryCode: string): CountryValidationConfig | undefined {
    return COUNTRY_CONFIGS.find(c => c.countryCode === countryCode);
}

/**
 * Get all country configs for dropdown
 */
export function getCountryOptions(): { value: string; label: string }[] {
    return COUNTRY_CONFIGS.map(c => ({
        value: c.countryCode,
        label: `${c.countryName} (${c.phonePrefix})`,
    }));
}

/**
 * Get rules that support auto-fix
 */
export function getAutoFixableRules(): ValidationRuleDefinition[] {
    return VALIDATION_RULES.filter(r => r.canAutoFix);
}

export default {
    COUNTRY_CONFIGS,
    VALIDATION_RULES,
    getRuleEducationalInfo,
    getRuleEducationalMap,
    getCountryConfig,
    getCountryOptions,
    getAutoFixableRules,
};

