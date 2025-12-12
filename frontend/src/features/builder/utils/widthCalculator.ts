/**
 * Width Calculator Utility - Story 3.5
 * 
 * Design-time utility for calculating optimal input widths based on:
 * - Font properties (family, size, weight)
 * - Content (placeholder, options)
 * - Coverage percentage (how much of average content should fit)
 * 
 * Uses canvas measureText API for accurate font-aware measurement.
 */

export interface FontProperties {
    fontFamily: string;
    fontSize: number;
    fontWeight: number;
}

// Cache for font metrics to avoid repeated canvas operations
const fontMetricsCache = new Map<string, number>();

/**
 * Get a canvas context for text measurement
 */
function getCanvas(): CanvasRenderingContext2D {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    if (!ctx) {
        throw new Error('Failed to get canvas context');
    }
    return ctx;
}

/**
 * Generate cache key for font properties
 */
function getFontCacheKey(fontProps: FontProperties, text: string): string {
    return `${fontProps.fontFamily}-${fontProps.fontSize}-${fontProps.fontWeight}-${text}`;
}

/**
 * Measure the pixel width of text using a specific font
 * 
 * @param text - The text to measure
 * @param fontFamily - CSS font-family value
 * @param fontSize - Font size in pixels
 * @param fontWeight - Font weight (100-900)
 * @returns Width in pixels
 */
export function measureTextWidth(
    text: string,
    fontFamily: string,
    fontSize: number,
    fontWeight: number
): number {
    const fontProps: FontProperties = { fontFamily, fontSize, fontWeight };
    const cacheKey = getFontCacheKey(fontProps, text);
    
    // Check cache first
    const cached = fontMetricsCache.get(cacheKey);
    if (cached !== undefined) {
        return cached;
    }
    
    try {
        const ctx = getCanvas();
        ctx.font = `${fontWeight} ${fontSize}px ${fontFamily}`;
        const metrics = ctx.measureText(text);
        const width = Math.ceil(metrics.width);
        
        // Cache the result (limit cache size to prevent memory issues)
        if (fontMetricsCache.size > 1000) {
            // Clear oldest entries (simple FIFO)
            const firstKey = fontMetricsCache.keys().next().value;
            if (firstKey) fontMetricsCache.delete(firstKey);
        }
        fontMetricsCache.set(cacheKey, width);
        
        return width;
    } catch (error) {
        // Fallback: estimate based on average character width
        console.warn('Canvas text measurement failed, using fallback:', error);
        return text.length * (fontSize * 0.6);
    }
}

/**
 * Calculate optimal input width based on placeholder and/or options
 * 
 * For inputs: Uses placeholder text
 * For dropdowns: Uses longest option label
 * 
 * @param placeholder - Placeholder text
 * @param options - Array of options (for select/dropdown)
 * @param fontProps - Font properties
 * @param minWidth - Minimum width (default: 100)
 * @param maxWidth - Maximum width (default: 500)
 * @returns Optimal width in pixels
 */
export function calculateInputWidth(
    placeholder: string | undefined,
    options: Array<{ label: string; value: string }> | undefined,
    fontProps: FontProperties,
    minWidth: number = 100,
    maxWidth: number = 500
): number {
    let longestText = placeholder || '';
    
    // For dropdowns, find the longest option
    if (options && options.length > 0) {
        for (const option of options) {
            if (option.label.length > longestText.length) {
                longestText = option.label;
            }
        }
    }
    
    // Measure the text
    const textWidth = measureTextWidth(
        longestText,
        fontProps.fontFamily,
        fontProps.fontSize,
        fontProps.fontWeight
    );
    
    // Add padding for input borders, icons, etc.
    const padding = 40; // ~20px on each side
    const calculatedWidth = textWidth + padding;
    
    // Clamp to min/max
    return Math.max(minWidth, Math.min(calculatedWidth, maxWidth));
}

/**
 * Estimate width needed for N characters at a given coverage percentage
 * 
 * Uses a reference character set to estimate average character width.
 * The coverage percentage determines how much of the estimated content
 * should fit without scrolling.
 * 
 * @param charCount - Number of characters to fit
 * @param fontProps - Font properties
 * @param coveragePercent - Percentage of average content to fit (0.0 - 1.0, default: 0.9)
 * @returns Estimated width in pixels
 */
export function estimateCharacterWidth(
    charCount: number,
    fontProps: FontProperties,
    coveragePercent: number = 0.9
): number {
    // Use a representative sample of characters for measurement
    // This string contains a mix of narrow and wide characters
    const sampleText = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    
    const sampleWidth = measureTextWidth(
        sampleText,
        fontProps.fontFamily,
        fontProps.fontSize,
        fontProps.fontWeight
    );
    
    // Average character width
    const avgCharWidth = sampleWidth / sampleText.length;
    
    // Calculate width for N characters at the coverage percentage
    const estimatedWidth = charCount * avgCharWidth * coveragePercent;
    
    // Add padding
    const padding = 40;
    
    return Math.ceil(estimatedWidth + padding);
}

/**
 * Calculate dropdown width with a maximum limit
 * Dropdowns are single-line only, so we don't need multiline consideration.
 * 
 * @param options - Dropdown options
 * @param fontProps - Font properties
 * @param maxWidth - Maximum allowed width (default: 400)
 * @returns Optimal dropdown width
 */
export function calculateDropdownWidth(
    options: Array<{ label: string; value: string }>,
    fontProps: FontProperties,
    maxWidth: number = 400
): number {
    if (!options || options.length === 0) {
        return 200; // Default width
    }
    
    // Find longest option
    let longestLabel = '';
    for (const option of options) {
        if (option.label.length > longestLabel.length) {
            longestLabel = option.label;
        }
    }
    
    const textWidth = measureTextWidth(
        longestLabel,
        fontProps.fontFamily,
        fontProps.fontSize,
        fontProps.fontWeight
    );
    
    // Add space for dropdown arrow and padding
    const dropdownChrome = 60; // Arrow + padding
    const calculatedWidth = textWidth + dropdownChrome;
    
    // Clamp to max width
    return Math.min(calculatedWidth, maxWidth);
}

/**
 * Clear the font metrics cache
 * Useful when fonts are dynamically loaded
 */
export function clearFontMetricsCache(): void {
    fontMetricsCache.clear();
}

