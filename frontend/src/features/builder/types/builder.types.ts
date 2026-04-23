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
  | 'url'             // Website URL input
  | 'textarea'
  | 'dropdown'        // Dropdown/Select field (canonical)
  | 'select'          // Alias for dropdown (runtime/legacy)
  | 'radio'
  | 'checkbox'
  | 'date'
  | 'address'         // Address with autocomplete (placeholder for future)
  | 'rating'          // Rating selector (stars, numbers, emoji)
  | 'file-upload'     // File attachment(s) via public upload API (Story 6.2.2)
  | 'first-name'      // POC component
  // Action/Legal Components
  | 'terms'           // Terms & Conditions checkbox
  | 'submit-button'   // Form submission button
  // Display/Layout
  | 'header'
  | 'paragraph'       // Display text block
  | 'divider'         // Visual separator
  // Layout containers (canvas row/column)
  | 'row'
  | 'column';

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
    /** Verify URL hostname resolves via DNS (online submit only) */
    urlDnsCheck?: boolean;
    
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

    // ═══════════════════════════════════════════════════════════════
    // SELECTION RULES (dropdown, checkbox, radio)
    // ═══════════════════════════════════════════════════════════════
    /** Minimum number of options that must be selected */
    minSelections?: number;
    /** Maximum number of options that can be selected */
    maxSelections?: number;
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

    // Action/Button typography & colors
    actionFontFamily?: string;
    actionFontSize?: number;
    actionFontWeight?: FontWeightValue;
    actionFontStyle?: FontStyleType;
    actionTextColor?: string;
    actionBackgroundColor?: string;
    actionBorderColor?: string;
    actionBorderWidth?: number;
    actionBorderRadius?: number;
    
    // Divider styles
    dividerBorderColor?: string;
    dividerBorderWidth?: number;
    
    // Legacy colors (for backward compatibility)
    placeholderColor?: string;
    backgroundColor?: string;
    borderColor?: string;
    
    // Rating Styles
    ratingColor?: string;
    ratingBackgroundColor?: string;
    
    // Borders & Spacing
    borderRadius?: number;
    borderWidth?: number;
    inputHeight?: number;
    
    // Spacing overrides
    labelGap?: number;
    inputHelpGap?: number;
}

/**
 * Spacing overrides for preview during resize operations.
 * Used to temporarily override spacing values while resizing.
 */
export interface SpacingOverrides {
    labelGapOverride?: number;
    inputHelpGapOverride?: number;
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
 * Row alignment options for horizontal/mixed layouts.
 * - top: Align items to the top (flex-start)
 * - center: Align items to the center (center) - Default for inputs
 * - bottom: Align items to the bottom (flex-end)
 * - stretch: Stretch items to fill height (stretch)
 */
export type RowAlignment = 'top' | 'center' | 'bottom' | 'stretch';

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
        /** Group/section name (visual only; dropdown may render as <optgroup>) */
        group?: string;
        /** If true, selecting this option enables an adjacent free-text input */
        hasExtraText?: boolean;
        /** Placeholder for the option's extra text input */
        extraPlaceholder?: string;
    }>;
    /** Layout orientation */
    layout?: LayoutType;
    /** Row alignment for horizontal layouts */
    rowAlignment?: RowAlignment;
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
    // INITIAL STATE PROPERTIES
    // ═══════════════════════════════════════════════════════════════
    /**
     * Initial visibility state for this component.
     * Logic rules can override via show/hide actions.
     * @default 'visible'
     */
    initialVisibility?: 'visible' | 'hidden';
    /**
     * Initial enabled state for this component.
     * Logic rules can override via enable/disable actions.
     * @default 'enabled'
     */
    initialEnabled?: 'enabled' | 'disabled';
    
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
    /**
     * Anchor point for component scaling (nw, ne, se, sw).
     * Determines which corner stays fixed during scaling.
     * Default: 'nw' (top-left stays fixed, component grows toward bottom-right).
     */
    componentScaleAnchor?: 'nw' | 'ne' | 'se' | 'sw';
    
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
    // OBJECT WIDTH OVERRIDES (for E/W resize affecting internal objects)
    // ═══════════════════════════════════════════════════════════════
    /** Override label object width in pixels */
    labelWidthOverride?: number;
    /** Override input object width in pixels */
    inputWidthOverride?: number;
    /** Override help/validation object width in pixels */
    helpWidthOverride?: number;
    /** Override action/button object width in pixels */
    actionWidthOverride?: number;

    // ═══════════════════════════════════════════════════════════════
    // SPACING OVERRIDES (for resize handles)
    // ═══════════════════════════════════════════════════════════════
    /** Override for gap between label and input (in pixels, not multiplier) */
    labelGapOverride?: number;
    /** Override for gap between input and help text (in pixels, not multiplier) */
    inputHelpGapOverride?: number;
    
    // ═══════════════════════════════════════════════════════════════
    // UNIVERSAL FIELDSHELL - Per-instance layout overrides
    // ═══════════════════════════════════════════════════════════════
    /** Override structure.defaultLayout (per-instance layout configuration) */
    objectLayout?: ObjectLayoutType;
    /** Override structure.layoutGroups (per-instance group configuration) */
    layoutGroups?: Record<string, string[]>;
    
    /** Object-specific spacing overrides */
    objectSpacing?: {
        horizontalGap?: number;      // Gap between objects in same row
        verticalSpacing?: number;      // Spacing between rows
        objectGap?: number;           // Generic gap (fallback)
    };
    
    /**
     * Grid layout configuration (alternative to objectLayout).
     * When set, this takes precedence over objectLayout for rendering.
     * - undefined: inherit from global defaults (if available) or use object layout
     * - null: explicitly opt out of grid mode, use object layout
     * - GridLayoutConfig: explicit grid layout override
     * See docs/GRID-LAYOUT-GUIDE.md for full specification.
     */
    gridLayout?: GridLayoutConfig | null;
    
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
    /** Validation rules for the "Other" text input (when allowOther is enabled and Other is selected) */
    otherValidation?: ValidationRules;
    /** Optional validation message override for the "Other" text input */
    otherValidationMessage?: string;
    // Unified selection extra text (new; replaces allowOther for new configs)
    /** Shared validation rules for option extra text inputs */
    extraTextValidation?: ValidationRules;
    /** Optional message override for option extra text validation failures */
    extraTextValidationMessage?: string;
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
    // URL-SPECIFIC
    // ═══════════════════════════════════════════════════════════════
    /** Optional URL prefix helper shown in UI (e.g., https://) */
    urlPrefix?: string;
    /** Custom URL regex pattern */
    urlPattern?: string;

    // ═══════════════════════════════════════════════════════════════
    // RATING-SPECIFIC
    // ═══════════════════════════════════════════════════════════════
    /** Maximum rating value (common: 5 or 10) */
    ratingMax?: number;
    /** Rating display style */
    ratingStyle?: 'stars' | 'numbers' | 'emoji';
    /** Optional low/high labels for rating scale */
    ratingLabels?: {
        low?: string;
        high?: string;
    };

    // ═══════════════════════════════════════════════════════════════
    // FILE UPLOAD (Story 6.2.2)
    // ═══════════════════════════════════════════════════════════════
    /** HTML input accept string or MIME/extension list */
    accept?: string;
    /** Allowed types (MIME or leading-dot extension), alternative to accept */
    acceptedFileTypes?: string[];
    /** Max upload size in bytes (server enforces on upload) */
    maxFileSizeBytes?: number;
    /** Max size in megabytes (converted to bytes for API) */
    maxFileSizeMb?: number;
    /** Allow more than one file in this control */
    allowMultiple?: boolean;
    /** Cap when allowMultiple is true */
    maxFiles?: number;
    
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
    /** Show icon in button */
    showIcon?: boolean;
    
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

// ═══════════════════════════════════════════════════════════════════════════
// BACKGROUND ASSET CONTRACTS (Story 5.1)
// Field names intentionally match backend asset_schemas.py
// Data URL guard: background values must NOT be persisted if value starts with "data:".
// ═══════════════════════════════════════════════════════════════════════════

export interface BackgroundAssetMetadata {
    assetId: number;
    assetKey: string;
    displayName?: string;
    originalFilename: string;
    mimeType: string;
    byteSize: number;
    widthPx?: number;
    heightPx?: number;
    checksumSha256?: string;
    createdAt?: string; // ISO timestamp
    updatedAt?: string; // ISO timestamp
}

export interface BackgroundPosition {
    /** Canvas coordinates in pixels; negative offsets allowed. */
    x: number;
    y: number;
}

export interface BackgroundSize {
    width: number;
    height: number;
}

export interface BackgroundCrop {
    x: number;
    y: number;
    width: number;
    height: number;
}

export interface BackgroundPlacement {
    position: BackgroundPosition;
    size: BackgroundSize;
    crop?: BackgroundCrop;
}

export type BackgroundType = 'color' | 'image';

/** True if string looks like a hex colour (e.g. #RRGGBB). */
export function isHexColor(s: string | undefined): boolean {
    return !!s && /^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/.test(s);
}

export interface BackgroundDefinition {
    type: BackgroundType;
    /** Hex color or legacy URL (Data URLs are NOT allowed). Active value for current type. */
    value: string;
    /** Stored colour when type is image so switching back to Colour restores it. */
    colorValue?: string;
    /** Preferred asset reference for background images. */
    asset?: BackgroundAssetMetadata;
    /** Placement metadata for image backgrounds. */
    placement?: BackgroundPlacement;
    /** How image fills placement frame. cover=fill+crop, contain=fit, fill=stretch, tile=repeat. */
    imageSize?: 'cover' | 'contain' | 'tile' | 'auto' | 'fill';
    /** Lock aspect ratio during resize. true=corner handles only; false=all 8 handles. */
    lockAspectRatio?: boolean;
    /** Legacy positioning (CSS-style). */
    imagePosition?: string;
    /** Overlay tint (hex). */
    overlayColor?: string;
    /** Overlay opacity (0-1). */
    overlayOpacity?: number;
    /** Background opacity (0-1). */
    opacity?: number;
    /** Legacy scale factor. */
    scale?: number;
    /** Legacy position (use placement.position instead). */
    position?: BackgroundPosition;
}

export interface BackgroundAssetResolver {
    /** Resolve an asset reference into a runtime URL. */
    resolveUrl: (asset: BackgroundAssetMetadata, placement?: BackgroundPlacement) => string | Promise<string>;
}

export interface FormPage {
    id: string;
    title: string;
    components: FormComponent[];
    // Canvas Refactor: Background Settings per page (T04: asset ref + image/overlay options)
    background?: BackgroundDefinition;
}

// ═══════════════════════════════════════════════════════════════════════════
// LOGIC ENGINE (Story 3.6 - Authoring + Persistence Only)
// Runtime evaluation is explicitly deferred to Story 3.7.
// ═══════════════════════════════════════════════════════════════════════════

export type LogicOperator =
  | 'equals'
  | 'notEquals'
  | 'contains'
  | 'greaterThan'
  | 'greaterThanOrEqual'
  | 'lessThan'
  | 'lessThanOrEqual'
  | 'isEmpty';
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
    
    // Action/Button styles
    actionFontFamily: string;
    actionFontSize: number;
    actionFontWeight: FontWeightValue;
    actionFontStyle: FontStyleType;
    actionTextColor: string;
    actionBackgroundColor: string;
    actionBorderColor?: string;
    actionBorderWidth?: number;
    actionBorderRadius?: number;

    // Divider styles
    dividerBorderColor: string;
    dividerBorderWidth: number;
    /** Default divider length/width (e.g. '100%' or '380px') */
    dividerWidth: string;

    // Rating styles
    ratingColor?: string;
    ratingBackgroundColor?: string;

    // ═══════════════════════════════════════════════════════════════
    // TEXT BORDERS (per text type - optional)
    // ═══════════════════════════════════════════════════════════════
    // Input text borders (in addition to input field border)
    textHasBorder?: boolean;          // Explicit border toggle for Input category
    textBorderColor?: string;
    textBorderWidth?: number;
    textBorderRadius?: number;
    
    // Label borders
    labelHasBorder?: boolean;          // Explicit border toggle for Label category
    labelBorderColor?: string;
    labelBorderWidth?: number;
    labelBorderRadius?: number;
    
    // Help text borders
    helpTextHasBorder?: boolean;       // Explicit border toggle for Help category
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
    // OBJECT LAYOUT SPACING DEFAULTS (Layer 3, explicit pixels)
    // Used by UniversalFieldShell's Object Layout engine when a component does not
    // provide per-instance `component.props.objectSpacing` overrides.
    // ═══════════════════════════════════════════════════════════════
    /** Default vertical gap between Object Layout rows (px) */
    objectRowGapPx: number;
    /** Default horizontal gap between objects within a row (px) */
    objectColumnGapPx: number;
    
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
    
    // ═══════════════════════════════════════════════════════════════
    // UNIVERSAL FIELDSHELL - Global object layout defaults
    // These serve as the global defaults that components inherit unless overridden
    // ═══════════════════════════════════════════════════════════════
    /** Default object layout for all components (vertical/horizontal/mixed) */
    defaultObjectLayout?: ObjectLayoutType;
    /** Default layout groups for mixed layouts */
    defaultLayoutGroups?: Record<string, string[]>;
    
    // ═══════════════════════════════════════════════════════════════
    // GRID LAYOUT DEFAULTS (GLOBAL)
    // Alternative to Object Layout - uses CSS Grid for object arrangement
    // ═══════════════════════════════════════════════════════════════
    
    /**
     * Default grid layout configuration (form-wide defaults).
     * Applied to all components when component doesn't have gridLayout override.
     * Components can override individual properties or the entire configuration.
     * 
     * When both defaultGridLayout and defaultObjectLayout are defined,
     * Grid Layout takes precedence if component.props.gridLayout is set.
     */
    defaultGridLayout?: Partial<GridLayoutConfig>;

    /**
     * Story 6.3.1 (UAT round 6) — form-wide horizontal label band.
     *
     * When set, every component rendered in horizontal-stacked grid mode uses
     * this pixel value as the width of its label column, giving the whole form
     * a consistent left-edge for inputs even when individual labels are very
     * short or very long. This is the form-wide alignment knob that sits
     * between component-level `props.labelWidthOverride` (per-component) and
     * the renderer's `'auto'` fallback (browser-determined).
     *
     * Resolution order in `UniversalFieldShell` for the label grid column:
     *   `gridLayout.columnGaps[c]` is for inter-column gaps (separate concern).
     *   For label column WIDTH:
     *     1. `props.labelWidthOverride` (per-component, from Appearance →
     *        Dimensions slider)
     *     2. `globalStyles.horizontalLabelBandPx` (this property — form-wide)
     *     3. `'auto'` (content-sized — original behaviour)
     *
     * The AI compiler computes a sensible default by measuring the longest
     * label in the semantic plan and clamping to a canvas-aware band, then
     * stamps it on the form when `defaultObjectLayout === 'horizontal'`.
     * Users can still override per-component via Appearance → Dimensions.
     */
    horizontalLabelBandPx?: number;

    /**
     * Story 6.3.1 (UAT round 6) — Fix D: form-wide input-band density preset
     * for horizontal-stacked grid mode.
     *
     * Scales the per-type comfortable character counts (in
     * `INPUT_COMFORTABLE_CHARS` on the backend) by a multiplier:
     *   - 'compact'  → 0.80x (denser inputs, more components fit per row)
     *   - 'standard' → 1.00x (default; Baymard P95-ish content widths)
     *   - 'spacious' → 1.25x (roomier inputs, marketing-style forms)
     *
     * Per-component `inputWidthOverride` always wins. Tier min/max still
     * clamp the result so the preset never produces a degenerate width.
     */
    horizontalInputBandPreset?: HorizontalInputBandPreset;

    /**
     * Per-component grid defaults (form-wide). Used when a component does not
     * define a gridLayout override, enabling Grid layout as the primary layout mode.
     */
    defaultGridLayoutsByComponent?: Partial<Record<ComponentType, Partial<GridLayoutConfig>>>;
}

/**
 * Story 6.3.1 (UAT round 6) — Fix D: input-band density presets for
 * horizontal-stacked grid mode. See `GlobalStyles.horizontalInputBandPreset`.
 */
export type HorizontalInputBandPreset = 'compact' | 'standard' | 'spacious';

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
    // Default to red so validation/help is easy to spot in builder.
    // Users can change this via Global Styles → Help & Validation text color.
    helpTextColor: '#DC2626',
    helpTextBackgroundColor: undefined,  // No background by default
    
    // Action/Button Styles (Defaults to Label font + Primary color)
    actionFontFamily: 'Inter',
    actionFontSize: 14,
    actionFontWeight: 500,
    actionFontStyle: 'normal',
    actionTextColor: '#FFFFFF',          // White text
    actionBackgroundColor: '#0055FF',    // Primary color (matches primaryColor below)
    actionBorderColor: undefined,
    actionBorderWidth: undefined,
    actionBorderRadius: 6,

    // Divider Styles
    dividerBorderColor: '#E5E7EB',       // Light gray
    dividerBorderWidth: 1,
    // Divider default length (kept as px by default for stable toolbox drag overlay)
    dividerWidth: '380px',

    // Rating Styles
    ratingColor: '#F59E0B',              // Amber-500
    ratingBackgroundColor: 'transparent',

    // Text Borders (optional)
    textHasBorder: false,              // Default: no border for Input category
    textBorderColor: undefined,
    textBorderWidth: undefined,
    textBorderRadius: undefined,
    labelHasBorder: false,             // Default: no border for Label category
    labelBorderColor: undefined,
    labelBorderWidth: undefined,
    labelBorderRadius: undefined,
    helpTextHasBorder: false,          // Default: no border for Help category
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

    // Object Layout spacing defaults (Layer 3)
    objectRowGapPx: 0,
    objectColumnGapPx: 8,
    
    // Borders
    borderRadius: 6,
    borderWidth: 1,
    
    // Sizing
    inputHeight: 40,
    
    // Layout
    defaultLayout: 'vertical',
    defaultObjectLayout: 'vertical',
    defaultLayoutGroups: undefined,
    
    // Grid Layout (opt-in, undefined by default)
    defaultGridLayout: undefined,
    defaultGridLayoutsByComponent: undefined,
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
    /**
     * Canvas/artboard background color (builder + renderer).
     * Note: Page-level backgrounds may also exist on `FormPage.background`; when both are present,
     * page background wins.
     */
    backgroundColor?: string;
}

/**
 * Form Definition - supports multi-device layouts
 * 
 * Architecture: One form = Three device-specific page arrays
 * - Same fields (exportName, label, validation) across all devices
 * - Different layouts (position, size) per device
 * - Single export schema regardless of which device was used
 */
/** Last AI Agent prompt + options; persisted with the form definition (Story 6.3 UAT). */
export interface AiAgentSettings {
    lastPrompt?: string;
    includeEventInformation?: boolean;
    maxSystemCorrectionAttempts?: number;
    globalStylesLocked?: boolean;
    sectionedPromptProfileVersion?: string;
}

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

    /** Builder AI Agent panel; saved with draft so prompts survive reload (optional). */
    aiAgentSettings?: AiAgentSettings;
    
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

// ═══════════════════════════════════════════════════════════════════════════
// GRID LAYOUT TYPES
// Provides CSS Grid-based layout as an alternative to Object Layout.
// See docs/GRID-LAYOUT-GUIDE.md for full specification.
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Grid layout configuration for component objects.
 * Enables CSS Grid-based arrangement of label, input, validation, etc.
 * Alternative to the Object Layout system (vertical/horizontal/mixed).
 */
export interface GridLayoutConfig {
    /**
     * Number of rows in the grid (1-12)
     * @default 3
     */
    rows: number;

    /**
     * Number of columns in the grid (1-12)
     * @default 1
     */
    columns: number;

    /**
     * Horizontal gap between grid cells in pixels (default for all columns)
     * @default 8
     */
    columnGap: number;

    /**
     * Vertical gap between grid cells in pixels (default for all rows)
     * @default 8
     */
    rowGap: number;

    /**
     * Per-column spacing overrides: allows individual column gaps.
     * Format: colIndex → gapInPixels
     * Example: { 0: 16, 1: 8 } - Column 0 has 16px gap to the right
     * Note: Gap applies TO THE RIGHT of the specified column
     */
    columnGaps?: Record<number, number>;

    /**
     * Per-row spacing overrides: allows individual row gaps.
     * Format: rowIndex → gapInPixels
     * Example: { 0: 12, 2: 16 } - Row 0 has 12px gap below
     * Note: Gap applies BELOW the specified row
     */
    rowGaps?: Record<number, number>;

    /**
     * Grid cell assignments: maps cell coordinates to object IDs.
     * Format: "row-col" → objectId
     * Example: { "0-0": "label", "1-0": "input", "2-0": "validation" }
     */
    cellAssignments: Record<string, string>;

    /**
     * Merged cell groups: defines which cells are merged together.
     * Format: "merged-group-id" → { cells: string[], objectId: string }
     * Example: { "merge-1": { cells: ["0-0", "0-1"], objectId: "label" } }
     */
    mergedCells?: Record<string, { cells: string[]; objectId: string }>;

    /**
     * Object span configuration: allows objects to span multiple cells.
     * Format: objectId → { rowSpan?: number, colSpan?: number }
     * Example: { "input": { rowSpan: 1, colSpan: 2 } }
     */
    objectSpans?: Record<string, { rowSpan?: number; colSpan?: number }>;

    /**
     * Grid alignment: how objects align within their grid cells.
     * @default 'stretch'
     */
    cellAlignment?: 'start' | 'center' | 'end' | 'stretch';

    /**
     * Grid justification: how grid cells align within the container.
     * @default 'start'
     */
    gridJustification?: 'start' | 'center' | 'end' | 'stretch' | 'space-between' | 'space-around' | 'space-evenly';

    /**
     * Row track sizing mode for gridTemplateRows.
     * - 'fr' uses 1fr tracks (default)
     * - 'auto' uses content-sized tracks
     */
    rowSizing?: 'fr' | 'auto';

    /**
     * Column track sizing mode for gridTemplateColumns.
     * - 'fr' uses 1fr tracks (default)
     * - 'auto' uses content-sized tracks
     */
    columnSizing?: 'fr' | 'auto';
}

// ═══════════════════════════════════════════════════════════════════════════
// UNIVERSAL FIELDSHELL ARCHITECTURE - Conditional Context & Rules
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Context for evaluating conditional rules for object visibility.
 * Used to determine when objects should be shown/hidden based on component state.
 */
export interface ConditionalContext {
    component: FormComponent;
    componentProps: ComponentProps;
    componentState?: Record<string, unknown>; // Runtime state (e.g., hasFocus, isLoading)
    /** Direct error for this component (simpler than validationErrors map) */
    error?: string;
    validationErrors?: Record<string, string>;
    allFormErrors?: Record<string, string>;
    /** If true, always show conditional objects (for builder mode) */
    builderMode?: boolean;
}

/**
 * Form-level validation context for action objects (submit button).
 * Provides aggregated validation state for all components.
 */
export interface FormValidationContext {
    /** All form validation errors, keyed by component ID */
    errors: Record<string, string>;
    /** Components sorted by tabOrder for priority display */
    errorsByPriority: Array<{
        componentId: string;
        error: string;
        tabOrder: number;
        label: string;
    }>;
    /** First error by priority (for single-line display), includes label prefix */
    firstError?: string;
    /** Total count of components with errors */
    errorCount: number;
}

/**
 * Rule for conditional object visibility (progressive disclosure).
 * Determines when an object should be visible based on component properties, state, or validation.
 */
export interface ConditionalRule {
    type: 'prop' | 'state' | 'validation' | 'always';
    prop?: string; // Property name to check (e.g., 'required', 'showLoadingState')
    condition?: (context: ConditionalContext) => boolean; // Custom evaluation function
    showInProperties?: boolean; // Progressive disclosure: show in Properties Panel only when condition met
}

// ═══════════════════════════════════════════════════════════════════════════
// UNIVERSAL FIELDSHELL ARCHITECTURE - Component Structure Types
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Layout type for component objects within FieldShell.
 * - vertical: Objects stacked vertically (default)
 * - horizontal: Objects arranged horizontally
 * - mixed: Custom grouping with layoutGroups
 */
export type ObjectLayoutType = 'vertical' | 'horizontal' | 'mixed';

/**
 * Type of object within a component structure.
 * - label: Text label for the field
 * - input: User input element (text, select, checkbox, etc.)
 * - action: Button or clickable action
 * - status: Loading/status indicator
 * - validation: Error/validation message
 * - divider: Visual separator line
 * - custom: Custom object type (specify with customType)
 */
export type ObjectType = 'label' | 'input' | 'action' | 'status' | 'validation' | 'divider' | 'display' | 'custom';

/**
 * Style archetype for an object.
 * Defines which category of global styles this object inherits from.
 */
export type StyleArchetype = 
    | 'PrimaryLabel'   // Inherits from GlobalStyles.Label (default for type='label')
    | 'InputControl'   // Inherits from GlobalStyles.Input (default for type='input')
    | 'HelperText'     // Inherits from GlobalStyles.HelpText (default for type='validation'/'status')
    | 'Action'         // Inherits from Button/Action styles
    | 'Divider'        // Inherits from divider styles
    | 'DisplayBlock';  // Inherits from nothing by default, acts as a display container

/**
 * Object-level feature configuration map.
 *
 * This enables “capabilities” to be attached to any top-level object in a component structure
 * (label/input/validation/divider/custom), independent of surface (toolbox/canvas/runtime).
 *
 * Surface gating (toolbox/canvas/runtime differences) remains in `componentSurfaceCapabilities.ts`.
 */
export type ObjectFeatures = {
    /**
     * Builder-only TextLengthIndicator overlay.
     * - Actual surface enablement still uses component surface capabilities.
     * - Presence here means “this object is eligible for the feature”.
     */
    textLengthIndicator?: {
        enabled?: boolean;
    };
    /** Allow future features without schema churn */
    [featureId: string]: unknown;
};

/**
 * Definition of a single object within a component structure.
 */
export interface ComponentObject {
    id: string;                    // Unique identifier within component (e.g., 'label', 'input')
    /** Optional display label for UI (grid/object layout panels); falls back to id when absent */
    label?: string;
    type: ObjectType;              // Type of object
    archetype?: StyleArchetype;    // Style archetype (optional, defaults based on type)
    required: boolean;              // Must always render?
    conditional?: ConditionalRule; // When to show/hide (progressive disclosure)
    order: number;                  // Display order (1, 2, 3...)
    customType?: string;            // For custom object types (e.g., 'icon', 'helper')
    /** Optional object-level capabilities/features (attachable by structure, independent of surface) */
    features?: ObjectFeatures;
}

/**
 * Structure definition for a component.
 * Defines how objects are arranged and when they should be visible.
 */
export interface ComponentStructure {
    objects: ComponentObject[];     // All objects this component contains (1-4+)
    defaultLayout: ObjectLayoutType; // Default layout (can be overridden per-instance)
    layoutGroups?: Record<string, string[]>; // For mixed layouts: { row1: ['label', 'input'], row2: ['validation'] }
    defaultRowAlignment?: RowAlignment; // Default vertical alignment for rows (e.g., 'top' for textarea, 'center' for inputs)
}
