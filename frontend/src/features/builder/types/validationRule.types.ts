/**
 * Validation Rule Types - Phase 2
 * 
 * TypeScript interfaces that mirror the database schema for seamless future integration.
 * These types are designed to match:
 * - config.ValidationRule table
 * - ref.Country table
 * - ref.RuleType table
 * 
 * @see docs/database-schema.md for database structure
 */

/**
 * Rule type categories - mirrors ref.RuleType
 */
export type RuleTypeCode = 
    | 'text'        // Text length, pattern, characters
    | 'number'      // Numeric range, precision
    | 'email'       // Email format, domain rules
    | 'phone'       // Phone format, country-specific
    | 'date'        // Date range, age validation
    | 'selection'   // Checkbox/radio constraints
    | 'security'    // XSS prevention, blocked content
    | 'formatting'; // Case transform, whitespace

/**
 * Character set categories for international name validation
 */
export type CharacterSet = 
    | 'latin'      // Western European (A-Za-z with accents)
    | 'cjk'        // Chinese, Japanese, Korean
    | 'arabic'     // Arabic script (RTL)
    | 'cyrillic'   // Russian, Ukrainian, etc.
    | 'devanagari' // Hindi, Sanskrit
    | 'mixed';     // Allow multiple scripts

/**
 * Validation Rule Definition - mirrors config.ValidationRule table
 * 
 * This is the complete definition of a validation rule as it would
 * be stored in the database.
 */
export interface ValidationRuleDefinition {
    /** Primary key - ValidationRuleID */
    id?: number;
    
    /** Unique rule identifier - e.g., 'minLength', 'phone_au' */
    ruleKey: string;
    
    /** FK to ref.RuleType */
    ruleTypeId: number;
    
    /** Rule type code for easier lookup */
    ruleTypeCode: RuleTypeCode;
    
    /** FK to ref.Country (null = global rule) */
    countryId?: number;
    
    /** Country code for easier lookup (e.g., 'AU', 'US') */
    countryCode?: string;
    
    /** Regex pattern for validation */
    validationPattern?: string;
    
    /** User-facing error message (supports placeholders: {min}, {max}) */
    validationMessage: string;
    
    /** i18n message key for future translation */
    messageKey?: string;
    
    /** Admin/developer description */
    description: string;
    
    /** Minimum length/value constraint */
    minLength?: number;
    
    /** Maximum length/value constraint */
    maxLength?: number;
    
    /** Display format hint (e.g., 'DD/MM/YYYY') */
    displayFormat?: string;
    
    /** Example value (e.g., '+61 412 345 678') */
    exampleValue?: string;
    
    /** Display example for user (formatted) */
    displayExample?: string;
    
    /** Priority for rule ordering */
    priority: number;
    
    /** Sort order for UI display */
    sortOrder: number;
    
    /** Is this rule active? */
    isActive: boolean;
    
    // ═══════════════════════════════════════════════════════════════
    // EDUCATIONAL CONTENT
    // ═══════════════════════════════════════════════════════════════
    
    /** Benefits of using this rule */
    pros: string[];
    
    /** Drawbacks or limitations */
    cons: string[];
    
    /** Best use case hint */
    bestFor?: string;
    
    /** Warning message for potential issues */
    warning?: string;
    
    /** Concrete example to help users understand */
    example?: string;
    
    // ═══════════════════════════════════════════════════════════════
    // AUTO-SANITIZATION CONFIG
    // ═══════════════════════════════════════════════════════════════
    
    /** Can this rule auto-fix issues instead of showing errors? */
    canAutoFix: boolean;
    
    /** Is auto-fix enabled by default? */
    autoFixDefault: boolean;
    
    /** Description of what auto-fix does */
    autoFixDescription?: string;
}

/**
 * Country Validation Config - mirrors ref.Country validation-related fields
 */
export interface CountryValidationConfig {
    /** Primary key - CountryID */
    countryId: number;
    
    /** ISO 3166-1 alpha-2 code (e.g., 'AU', 'US', 'GB') */
    countryCode: string;
    
    /** Country name for display */
    countryName: string;
    
    /** Phone prefix (e.g., '+61', '+1', '+44') */
    phonePrefix: string;
    
    /** Preferred date format */
    dateFormat: 'DD/MM/YYYY' | 'MM/DD/YYYY' | 'YYYY-MM-DD';
    
    /** Currency code (e.g., 'AUD', 'USD', 'GBP') */
    currencyCode: string;
    
    /** Primary character set for names */
    nameCharacterSet: CharacterSet;
    
    /** Minimum valid name length (e.g., 2 for CJK, 1 for some cultures) */
    minNameLength: number;
    
    /** Is RTL text direction? */
    isRtl: boolean;
    
    /** Phone number format pattern for display */
    phoneDisplayFormat?: string;
    
    /** Example phone number */
    phoneExample?: string;
    
    /** Postal code pattern */
    postalCodePattern?: string;
    
    /** Postal code example */
    postalCodeExample?: string;
}

/**
 * Validation context passed to the validation engine
 */
export interface ValidationContext {
    /** User's country code (from form settings or browser) */
    countryCode?: string;
    
    /** User's language code (e.g., 'en', 'zh', 'ar') */
    languageCode?: string;
    
    /** Form's target locale */
    formLocale?: string;
    
    /** Date format for date field validation (e.g. component dateFormat) */
    dateFormat?: string;
    
    /** Country config for country-specific validation */
    countryConfig?: CountryValidationConfig;
}

/**
 * Result of validation with auto-fix support
 */
export interface ValidationResult {
    /** Did validation pass? */
    isValid: boolean;
    
    /** Error messages (empty if valid) */
    errors: ValidationError[];
    
    /** Warning messages (validation passed but has issues) */
    warnings?: string[];
    
    /** Sanitized/auto-fixed value (if different from input) */
    sanitizedValue?: unknown;
    
    /** List of auto-fixes that were applied */
    autoFixesApplied?: AutoFixResult[];
}

/**
 * Detailed validation error
 */
export interface ValidationError {
    /** Rule key that failed */
    ruleKey: string;
    
    /** User-facing error message */
    message: string;
    
    /** i18n message key */
    messageKey?: string;
    
    /** Message placeholders for i18n */
    params?: Record<string, string | number>;
}

/**
 * Auto-fix result
 */
export interface AutoFixResult {
    /** What was fixed */
    fixType: 'trim' | 'consecutive_spaces' | 'lowercase' | 'titlecase' | 'phone_format';
    
    /** Original value */
    originalValue: string;
    
    /** Fixed value */
    fixedValue: string;
    
    /** Human-readable description */
    description: string;
}

/**
 * Rule info for educational tooltips
 */
export interface RuleEducationalInfo {
    ruleKey: string;
    displayName: string;
    description: string;
    pros: string[];
    cons: string[];
    bestFor?: string;
    warning?: string;
    canAutoFix: boolean;
    autoFixDescription?: string;
    /** Concrete example to help users understand */
    example?: string;
}

/**
 * Map of rule keys to their educational info
 */
export type RuleEducationalMap = Map<string, RuleEducationalInfo>;

export default {
    // Type exports are handled by the interface/type declarations above
};

