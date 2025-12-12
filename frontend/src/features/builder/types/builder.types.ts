/**
 * Builder Types - Story 3.3, 3.4 & 3.5
 * Based on JSON Schema from Story 3.2
 * 
 * i18n Note: All string properties support full Unicode (UTF-16).
 * This enables international character sets for labels, placeholders, etc.
 */

export type ComponentType = 
  // Input Fields
  | 'text' 
  | 'number' 
  | 'email' 
  | 'phone'           // Phone number input
  | 'textarea' 
  | 'select' 
  | 'radio' 
  | 'checkbox' 
  | 'date'
  | 'address'         // Address with autocomplete (placeholder for future)
  | 'first-name'      // POC component
  // Action/Legal Components
  | 'terms'           // Terms & Conditions checkbox
  | 'submit-button'   // Form submission button
  // Display/Layout
  | 'header'
  | 'paragraph'
  | 'divider';        // Visual separator

export type DeviceType = 'desktop' | 'tablet' | 'mobile';

/**
 * Layout orientation for form components.
 * - vertical: Label above input (default)
 * - horizontal: Label to the left of input
 */
export type LayoutType = 'vertical' | 'horizontal';

/**
 * Text alignment options
 */
export type AlignType = 'left' | 'center' | 'right';

/**
 * Available font weight values
 * Not all fonts support all weights - check font.weights array
 */
export type FontWeightValue = 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900;

/**
 * Font weight options for UI (legacy support)
 */
export type FontWeightType = 300 | 400 | 500 | 600 | 700;

/**
 * Font weight label mapping
 */
export const FONT_WEIGHT_LABELS: Record<FontWeightValue, string> = {
    100: 'Thin',
    200: 'Extra Light',
    300: 'Light',
    400: 'Regular',
    500: 'Medium',
    600: 'Semi-Bold',
    700: 'Bold',
    800: 'Extra-Bold',
    900: 'Black',
};

/**
 * Font category types for filtering/grouping
 */
export type FontCategory = 
    | 'sans-serif'      // Clean, modern - ideal for digital interfaces
    | 'serif'           // Traditional, elegant - great for formal content
    | 'display'         // Bold, attention-grabbing - headers/titles
    | 'handwriting'     // Personal, creative - signatures, accents
    | 'monospace';      // Technical, code-like - forms, data entry

/**
 * Font family definition with category, weights, and i18n support
 */
export interface FontFamily {
    value: string;              // CSS font-family value
    label: string;              // Display name
    category: FontCategory;
    weights: FontWeightValue[]; // Available font weights
    i18nSupport?: boolean;      // Has broad Unicode coverage
    googleFont?: boolean;       // Available via Google Fonts
    hasItalic?: boolean;        // Has italic variants
}

// ═══════════════════════════════════════════════════════════════════════════
// FONT DATA - Now fetched from /api/fonts backend
// The hardcoded FONT_FAMILIES array has been removed in favor of the 
// Google Fonts API. See:
// - frontend/src/features/builder/api/fontsApi.ts (API client)
// - frontend/src/features/builder/hooks/useFonts.ts (React Query hooks)
// - frontend/src/features/builder/api/fontTypes.ts (TypeScript types)
// ═══════════════════════════════════════════════════════════════════════════

export const DEVICE_DIMENSIONS: Record<DeviceType, { width: number; height: number; label: string }> = {
    desktop: { width: 1920, height: 980, label: 'Desktop (1920 x 980)' },
    tablet: { width: 768, height: 1024, label: 'Tablet (768 x 1024)' },
    mobile: { width: 375, height: 667, label: 'Mobile (375 x 667)' }
};

/**
 * Validation rules for form components.
 * Pattern uses Unicode-aware regex (apply with /u flag).
 * 
 * These rules are organized by category and component type.
 * Some rules may conflict with others - see validationConflicts.ts
 */
export interface ValidationRules {
    // ═══════════════════════════════════════════════════════════════
    // GENERAL RULES (All components)
    // ═══════════════════════════════════════════════════════════════
    /** Field is required */
    required?: boolean;
    /** Custom error message (Unicode string) */
    customError?: string;
    
    // ═══════════════════════════════════════════════════════════════
    // TEXT RULES (text, textarea, first-name)
    // ═══════════════════════════════════════════════════════════════
    /** Minimum character length (Unicode graphemes) */
    minLength?: number;
    /** Maximum character length (Unicode graphemes) */
    maxLength?: number;
    /** Regex pattern - use /u flag for Unicode support */
    pattern?: string;
    /** Alpha only (letters) */
    alpha?: boolean;
    /** Alphanumeric (letters and digits) */
    alphanumeric?: boolean;
    /** Block HTML tags and script content (XSS prevention) */
    noHtmlScript?: boolean;
    /** Automatically trim leading/trailing whitespace */
    trimWhitespace?: boolean;
    /** Prevent multiple consecutive spaces */
    noConsecutiveSpaces?: boolean;
    /** Auto-transform text case */
    caseTransform?: 'uppercase' | 'lowercase' | 'titlecase';
    /** Characters that are not allowed */
    blockedCharacters?: string;
    /** Field ID that this value must match (for confirmation fields) */
    mustMatchField?: string;
    
    // ═══════════════════════════════════════════════════════════════
    // NUMBER RULES
    // ═══════════════════════════════════════════════════════════════
    /** Numeric only (digits) */
    numeric?: boolean;
    /** Minimum numeric value */
    minValue?: number;
    /** Maximum numeric value */
    maxValue?: number;
    /** No decimal values allowed */
    integerOnly?: boolean;
    /** Maximum number of decimal places */
    decimalPrecision?: number;
    /** Value must be a multiple of this number */
    stepIncrement?: number;
    /** Must be greater than zero */
    positiveOnly?: boolean;
    /** Zero or positive only (no negatives) */
    nonNegative?: boolean;
    /** Cannot be exactly zero */
    nonZero?: boolean;
    /** Only odd numbers allowed */
    oddOnly?: boolean;
    /** Only even numbers allowed */
    evenOnly?: boolean;
    /** Only these specific numbers are valid */
    allowedValues?: number[];
    
    // ═══════════════════════════════════════════════════════════════
    // EMAIL RULES
    // ═══════════════════════════════════════════════════════════════
    /** Email format validation */
    email?: boolean;
    /** Block free email providers (gmail, yahoo, hotmail, etc.) */
    businessEmailOnly?: boolean;
    /** Only accept emails from these domains */
    domainWhitelist?: string[];
    /** Reject emails from these domains */
    domainBlacklist?: string[];
    /** Block known disposable/temporary email providers */
    noDisposableEmail?: boolean;
    /** Block email+tag@domain format */
    noPlusAddressing?: boolean;
    
    // ═══════════════════════════════════════════════════════════════
    // PHONE RULES
    // ═══════════════════════════════════════════════════════════════
    /** Phone number validation */
    phone?: boolean;
    /** Must include country code (+XX) */
    countryCodeRequired?: boolean;
    /** Only accept phone numbers from these countries (ISO codes) */
    allowedCountries?: string[];
    /** Only accept mobile numbers (reject landlines) */
    mobileOnly?: boolean;
    
    // ═══════════════════════════════════════════════════════════════
    // URL RULES
    // ═══════════════════════════════════════════════════════════════
    /** URL format validation */
    url?: boolean;
    
    // ═══════════════════════════════════════════════════════════════
    // DATE RULES
    // ═══════════════════════════════════════════════════════════════
    /** Earliest allowed date (YYYY-MM-DD or "today") */
    minDate?: string;
    /** Latest allowed date (YYYY-MM-DD or "today") */
    maxDate?: string;
    /** Date must be in the future */
    futureOnly?: boolean;
    /** Date must be in the past */
    pastOnly?: boolean;
    /** User must be at least N years old */
    minimumAge?: number;
    /** User cannot be older than N years */
    maximumAge?: number;
    /** Only weekdays allowed (no Saturday/Sunday) */
    weekdaysOnly?: boolean;
    /** Enable date range selection (start + end dates) */
    isDateRange?: boolean;
    /** Maximum days between start and end date (for date range) */
    maxDateRangeSpan?: number;
    /** Minimum days between start and end date (for date range) */
    minDateRangeSpan?: number;
}

/**
 * Font style options
 */
export type FontStyleType = 'normal' | 'italic';

/**
 * Style overrides for individual components.
 * Properties set here override global styles.
 * Use `undefined` to inherit from global.
 * 
 * Each property that is `undefined` will inherit from GlobalStyles.
 * Only set properties you want to override.
 */
export interface StyleOverrides {
    // Input text typography
    fontFamily?: string;
    fontSize?: number;
    fontWeight?: FontWeightValue;
    fontStyle?: FontStyleType;
    textColor?: string;
    textBackgroundColor?: string;
    textBorderColor?: string;
    textBorderWidth?: number;
    textBorderRadius?: number;
    
    // Label typography (separate from input)
    labelFontFamily?: string;
    labelFontSize?: number;
    labelFontWeight?: FontWeightValue;
    labelFontStyle?: FontStyleType;
    labelColor?: string;
    labelBackgroundColor?: string;
    labelBorderColor?: string;
    labelBorderWidth?: number;
    labelBorderRadius?: number;
    
    // Help/validation text typography
    helpTextFontFamily?: string;
    helpTextFontSize?: number;
    helpTextFontWeight?: FontWeightValue;
    helpTextFontStyle?: FontStyleType;
    helpTextColor?: string;
    helpTextBackgroundColor?: string;
    helpTextBorderColor?: string;
    helpTextBorderWidth?: number;
    helpTextBorderRadius?: number;
    
    // Legacy colors (for backward compatibility)
    placeholderColor?: string;
    backgroundColor?: string;
    borderColor?: string;
    
    // Borders & Spacing
    borderRadius?: number;
    borderWidth?: number;
    inputHeight?: number;
    
    // Spacing overrides
    labelGap?: number;
    inputHelpGap?: number;
}

/**
 * Textarea resize mode options
 */
export type ResizeMode = 'none' | 'vertical' | 'horizontal' | 'both' | 'auto-grow';

/**
 * Button action types
 */
export type ButtonAction = 'submit' | 'submit-and-reset' | 'next-page';

/**
 * Button width options
 */
export type ButtonWidth = 'auto' | 'full';

/**
 * Export mode for checkboxes
 */
export type ExportMode = 'single-value' | 'multi-column';

/**
 * Address export mapping for decomposed address fields
 */
export interface AddressExportMapping {
    streetNumber?: string;
    streetName?: string;
    unit?: string;
    suburb?: string;
    state?: string;
    postcode?: string;
    country?: string;
}

/**
 * Component properties - supports Unicode text for all string fields.
 */
export interface ComponentProps {
    // ═══════════════════════════════════════════════════════════════
    // GENERAL PROPERTIES
    // ═══════════════════════════════════════════════════════════════
    /** Field label (Unicode string) */
    label?: string;
    /** Is field required? */
    required?: boolean;
    /** Placeholder text (Unicode string) */
    placeholder?: string;
    /** Help text below field (Unicode string) */
    helpText?: string;
    /** Options for select/radio/checkbox */
    options?: Array<{ 
        label: string; 
        value: string;
        /** Option is disabled (greyed out) */
        disabled?: boolean;
        /** Group name for optgroup (select only) */
        group?: string;
    }>;
    /** Layout orientation */
    layout?: LayoutType;
    /** Label text alignment */
    labelAlign?: AlignType;
    /** Text alignment within input */
    textAlign?: AlignType;
    /** Validation rules */
    validation?: ValidationRules;
    /** Style overrides (undefined = use global) */
    styleOverrides?: StyleOverrides;
    /** Validation message shown in builder preview */
    validationMessage?: string;
    
    // ═══════════════════════════════════════════════════════════════
    // EXPORT & DATA PROPERTIES
    // ═══════════════════════════════════════════════════════════════
    /** Export field name for data integration (camelCase, no spaces) */
    exportName?: string;
    /** Tab order for keyboard navigation (1-based) */
    tabOrder?: number;
    /** Checkbox export mode */
    exportMode?: ExportMode;
    
    // ═══════════════════════════════════════════════════════════════
    // DIMENSION PROPERTIES
    // ═══════════════════════════════════════════════════════════════
    /** Width (e.g., "100%", "300px", "auto") */
    width?: string;
    /** Height in pixels (for textarea) */
    height?: number;
    /** 
     * Proportional scale factor (50-200%). Default 100.
     * Scales: font sizes, input height, padding, border radius.
     */
    componentScale?: number;
    
    // ═══════════════════════════════════════════════════════════════
    // INPUT WIDTH & RESPONSIVE BEHAVIOR
    // ═══════════════════════════════════════════════════════════════
    /**
     * How the input field width is determined.
     * - 'fill': Input stretches to fill container width (default)
     * - 'fixed': Use explicit inputWidth value
     * - 'auto': Calculate from maxLength validation
     */
    inputWidthMode?: 'fill' | 'fixed' | 'auto';
    /** Explicit input width in pixels (used when inputWidthMode = 'fixed') */
    inputWidth?: number;
    /** Allow label text to wrap to multiple lines (default: true) */
    labelWrap?: boolean;
    
    // ═══════════════════════════════════════════════════════════════
    // SPACING OVERRIDES (for resize handles)
    // ═══════════════════════════════════════════════════════════════
    /** Override for gap between label and input (in pixels, not multiplier) */
    labelGapOverride?: number;
    /** Override for gap between input and help text (in pixels, not multiplier) */
    inputHelpGapOverride?: number;
    
    // ═══════════════════════════════════════════════════════════════
    // TEXTAREA-SPECIFIC
    // ═══════════════════════════════════════════════════════════════
    /** Resize behavior for textarea */
    resizeMode?: ResizeMode;
    /** Show character count */
    showCharacterCount?: boolean;
    
    // ═══════════════════════════════════════════════════════════════
    // SELECT/DROPDOWN-SPECIFIC
    // ═══════════════════════════════════════════════════════════════
    /** Allow "Other" option with free text */
    allowOther?: boolean;
    /** Placeholder for "Other" input */
    otherPlaceholder?: string;
    /** Default selected value */
    defaultValue?: string;
    /** Allow empty selection (show "Select..." placeholder) */
    allowEmpty?: boolean;
    /** Placeholder text for empty selection */
    emptyPlaceholder?: string;
    /** Enable search/filter in dropdown */
    searchable?: boolean;
    
    // ═══════════════════════════════════════════════════════════════
    // CHECKBOX/RADIO SPECIFIC
    // ═══════════════════════════════════════════════════════════════
    /** Default checked values (for checkbox groups) */
    defaultChecked?: string[];
    /** Minimum number of selections required (checkbox) */
    minSelections?: number;
    /** Maximum number of selections allowed (checkbox) */
    maxSelections?: number;
    /** Custom separator for combined export mode */
    exportSeparator?: string;
    /** Layout direction for checkbox/radio options */
    optionsDirection?: 'horizontal' | 'vertical';
    
    // ═══════════════════════════════════════════════════════════════
    // DATE-SPECIFIC
    // ═══════════════════════════════════════════════════════════════
    /** Type of date/time input */
    dateType?: 'date' | 'datetime' | 'time';
    /** Style of date picker UI */
    pickerStyle?: 'calendar' | 'dropdown' | 'native';
    /** Display format for the date (e.g., "DD/MM/YYYY") */
    dateFormat?: string;
    /** Which date parts to include */
    dateParts?: {
        year?: boolean;
        month?: boolean;
        day?: boolean;
        hour?: boolean;
        minute?: boolean;
    };
    /** Labels for date range fields */
    dateRangeLabels?: {
        start?: string;
        end?: string;
    };
    
    // ═══════════════════════════════════════════════════════════════
    // TERMS & CONDITIONS SPECIFIC
    // ═══════════════════════════════════════════════════════════════
    /** URL to terms document */
    termsUrl?: string;
    /** Terms document content (for modal display) */
    termsContent?: string;
    /** Link text (e.g., "Terms of Service") */
    termsLinkText?: string;
    
    // ═══════════════════════════════════════════════════════════════
    // BUTTON SPECIFIC
    // ═══════════════════════════════════════════════════════════════
    /** Button text */
    buttonText?: string;
    /** Button behavior */
    buttonAction?: ButtonAction;
    /** Button width */
    buttonWidth?: ButtonWidth;
    /** Button alignment */
    buttonAlign?: AlignType;
    /** Show loading indicator on submit */
    showLoadingState?: boolean;
    /** Disable until form is valid */
    disableUntilValid?: boolean;
    
    // ═══════════════════════════════════════════════════════════════
    // ADDRESS SPECIFIC (Placeholder for future)
    // ═══════════════════════════════════════════════════════════════
    /** Enable Google Places autocomplete */
    enableAutocomplete?: boolean;
    /** Export decomposed address fields */
    decomposeAddress?: boolean;
    /** Address subfield mappings for export */
    addressExportMapping?: AddressExportMapping;
    
    /** Allow additional properties for extensibility */
    [key: string]: unknown;
}

export interface FormComponent {
    id: string;
    type: ComponentType;
    props: ComponentProps;
    // Canvas Refactor: Absolute Positioning
    position?: {
        x: number;
        y: number;
    };
    style?: {
        zIndex?: number;
        width?: number; // Optional override
        height?: number; // Optional override
    };
    children?: FormComponent[]; 
}

export interface FormPage {
    id: string;
    title: string;
    components: FormComponent[];
    // Canvas Refactor: Background Settings per page
    background?: {
        type: 'color' | 'image';
        value: string; // Hex code or URL
        opacity?: number;
        scale?: number;
        position?: { x: number, y: number };
    };
}

// ═══════════════════════════════════════════════════════════════════════════
// LOGIC ENGINE (Story 3.6 - Authoring + Persistence Only)
// Runtime evaluation is explicitly deferred to Story 3.7.
// ═══════════════════════════════════════════════════════════════════════════

export type LogicOperator = 'equals' | 'notEquals' | 'contains' | 'isEmpty';
export type LogicAction = 'show' | 'hide' | 'require' | 'unrequire' | 'enable' | 'disable';

export interface LogicWhen {
    sourceComponentId: string;
    operator: LogicOperator;
    /** Required for equals/notEquals/contains; omitted for isEmpty */
    value?: string;
}

export interface LogicThen {
    targetComponentId: string;
    action: LogicAction;
}

export interface LogicRule {
    id: string;
    enabled: boolean;
    /** Optional user-friendly name for rule management (UX) */
    name?: string;
    when: LogicWhen;
    then: LogicThen;
}

export interface FormLogic {
    rules: LogicRule[];
}

/**
 * Global styles - the "Brand DNA" defaults for all components.
 * These cascade to all components unless overridden individually.
 * 
 * The cascade works as:
 * 1. GlobalStyles define the base "brand" settings
 * 2. Individual components can override ANY property via styleOverrides
 * 3. Toolbox always shows GlobalStyles (no overrides)
 * 4. Canvas components show effective style (global + overrides)
 */
export interface GlobalStyles {
    // ═══════════════════════════════════════════════════════════════
    // INPUT TEXT TYPOGRAPHY (Base font settings)
    // ═══════════════════════════════════════════════════════════════
    fontFamily: string;
    fontSize: number;
    fontWeight: FontWeightValue;
    fontStyle: FontStyleType;
    
    // ═══════════════════════════════════════════════════════════════
    // LABEL TYPOGRAPHY (Can differ from input text)
    // ═══════════════════════════════════════════════════════════════
    labelFontFamily: string;
    labelFontSize: number;
    labelFontWeight: FontWeightValue;
    labelFontStyle: FontStyleType;
    
    // ═══════════════════════════════════════════════════════════════
    // HELP/VALIDATION TEXT TYPOGRAPHY
    // ═══════════════════════════════════════════════════════════════
    helpTextFontFamily: string;
    helpTextFontSize: number;
    helpTextFontWeight: FontWeightValue;
    helpTextFontStyle: FontStyleType;
    
    // ═══════════════════════════════════════════════════════════════
    // TEXT COLORS & BACKGROUNDS (per text type)
    // ═══════════════════════════════════════════════════════════════
    // Input text
    textColor: string;
    textBackgroundColor?: string;        // Optional highlight/background
    
    // Label text
    labelColor: string;
    labelBackgroundColor?: string;       // Optional highlight/background
    
    // Help/validation text
    helpTextColor: string;
    helpTextBackgroundColor?: string;    // Optional highlight/background
    
    // ═══════════════════════════════════════════════════════════════
    // TEXT BORDERS (per text type - optional)
    // ═══════════════════════════════════════════════════════════════
    // Input text borders (in addition to input field border)
    textBorderColor?: string;
    textBorderWidth?: number;
    textBorderRadius?: number;
    
    // Label borders
    labelBorderColor?: string;
    labelBorderWidth?: number;
    labelBorderRadius?: number;
    
    // Help text borders
    helpTextBorderColor?: string;
    helpTextBorderWidth?: number;
    helpTextBorderRadius?: number;
    
    // ═══════════════════════════════════════════════════════════════
    // UI COLORS
    // ═══════════════════════════════════════════════════════════════
    primaryColor: string;
    placeholderColor: string;
    backgroundColor: string;             // Input field background
    borderColor: string;                 // Input field border
    errorColor: string;
    
    // ═══════════════════════════════════════════════════════════════
    // SPACING (Base unit system - all multipliers of baseSpacing)
    // ═══════════════════════════════════════════════════════════════
    baseSpacing: number;
    labelGap: number;       // Multiplier of baseSpacing - vertical/horizontal gap between label and input
    inputHelpGap: number;   // Multiplier of baseSpacing - gap between input and help text
    inputPaddingX: number;  // Multiplier of baseSpacing (internal padding)
    inputPaddingY: number;  // Multiplier of baseSpacing (internal padding)
    
    // ═══════════════════════════════════════════════════════════════
    // BORDERS
    // ═══════════════════════════════════════════════════════════════
    borderRadius: number;
    borderWidth: number;
    
    // ═══════════════════════════════════════════════════════════════
    // SIZING
    // ═══════════════════════════════════════════════════════════════
    inputHeight: number;
    
    // ═══════════════════════════════════════════════════════════════
    // LAYOUT
    // ═══════════════════════════════════════════════════════════════
    defaultLayout: LayoutType;
}

/**
 * Default global styles - sensible defaults for new forms
 */
export const DEFAULT_GLOBAL_STYLES: GlobalStyles = {
    // Input Text Typography
    fontFamily: 'Inter',
    fontSize: 14,
    fontWeight: 400,
    fontStyle: 'normal',
    
    // Label Typography
    labelFontFamily: 'Inter',
    labelFontSize: 14,
    labelFontWeight: 500,
    labelFontStyle: 'normal',
    
    // Help Text Typography
    helpTextFontFamily: 'Inter',
    helpTextFontSize: 12,
    helpTextFontWeight: 400,
    helpTextFontStyle: 'normal',
    
    // Text Colors & Backgrounds
    textColor: '#1F2937',
    textBackgroundColor: '#FFFFFF',      // White background by default
    labelColor: '#374151',
    labelBackgroundColor: undefined,     // No background by default
    helpTextColor: '#6B7280',
    helpTextBackgroundColor: undefined,  // No background by default
    
    // Text Borders (optional)
    textBorderColor: undefined,
    textBorderWidth: undefined,
    textBorderRadius: undefined,
    labelBorderColor: undefined,
    labelBorderWidth: undefined,
    labelBorderRadius: undefined,
    helpTextBorderColor: undefined,
    helpTextBorderWidth: undefined,
    helpTextBorderRadius: undefined,
    
    // UI Colors
    primaryColor: '#0055FF',
    placeholderColor: '#9CA3AF',
    backgroundColor: '#FFFFFF',
    borderColor: '#D1D5DB',
    errorColor: '#DC2626',
    
    // Spacing (8px base unit)
    baseSpacing: 8,
    labelGap: 1,        // 8px - gap between label and input
    inputHelpGap: 0.5,  // 4px - gap between input and help text
    inputPaddingX: 1.5, // 12px - internal padding
    inputPaddingY: 1,   // 8px - internal padding
    
    // Borders
    borderRadius: 6,
    borderWidth: 1,
    
    // Sizing
    inputHeight: 40,
    
    // Layout
    defaultLayout: 'vertical',
};

export interface FormTheme {
    primaryColor: string;
    backgroundColor: string;
    fontFamily: string;
}

/**
 * Canvas settings per device type
 */
export interface CanvasSettings {
    width: number;   // e.g. 1920
    height: number;  // e.g. 1080
    gridSize: number; // e.g. 8
}

/**
 * Form Definition - supports multi-device layouts
 * 
 * Architecture: One form = Three device-specific page arrays
 * - Same fields (exportName, label, validation) across all devices
 * - Different layouts (position, size) per device
 * - Single export schema regardless of which device was used
 */
export interface FormDefinition {
    schemaVersion: string;
    formId: string;
    theme: FormTheme;
    
    // Global Styles (The Master Theme / Brand DNA)
    globalStyles?: GlobalStyles;

    // Logic Engine (Story 3.6) - persisted rule definitions
    logic?: FormLogic;
    
    // Canvas Settings
    canvasSettings?: CanvasSettings;
    
    // ═══════════════════════════════════════════════════════════════
    // DEVICE-SPECIFIC PAGE ARRAYS
    // Same fields, different visual layouts per device
    // ═══════════════════════════════════════════════════════════════
    /** Desktop layout pages */
    desktopPages?: FormPage[];
    /** Tablet layout pages */
    tabletPages?: FormPage[];
    /** Mobile layout pages */
    mobilePages?: FormPage[];
    
    // Legacy compatibility - will be migrated to desktopPages on load
    pages: FormPage[];
}

/**
 * Helper to resolve a component property with global fallback.
 * Returns component override if set, otherwise global value.
 */
export function resolveStyleProperty<K extends keyof StyleOverrides>(
    componentOverrides: StyleOverrides | undefined,
    globalStyles: GlobalStyles,
    property: K
): StyleOverrides[K] | GlobalStyles[keyof GlobalStyles] {
    if (componentOverrides && componentOverrides[property] !== undefined) {
        return componentOverrides[property];
    }
    // Map StyleOverrides keys to GlobalStyles keys
    const globalKey = property as keyof GlobalStyles;
    return globalStyles[globalKey];
}
