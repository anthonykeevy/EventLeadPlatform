/**
 * Font Loader Utility - Story 3.5
 * 
 * Dynamically loads Google Fonts as they are selected in the builder.
 * This ensures fonts render correctly without pre-loading all 1,900+ fonts.
 * 
 * Supports both:
 * - Variable fonts: Load weight range (e.g., wght@100..900)
 * - Static fonts: Load specific weights (e.g., wght@400;500;700)
 */

// Track which fonts have already been loaded
const loadedFonts = new Map<string, string>(); // fontFamily -> loadedConfig

/**
 * Load a Google Font dynamically by injecting a link tag
 * 
 * @param fontFamily - Font family name (e.g., "Inter", "Playfair Display")
 * @param isVariable - Whether this is a variable font
 * @param minWeight - Minimum weight for variable fonts (default 100)
 * @param maxWeight - Maximum weight for variable fonts (default 900)
 * @param specificWeights - Specific weights to load for static fonts
 */
export function loadGoogleFont(
    fontFamily: string,
    isVariable: boolean = false,
    minWeight: number | null = null,
    maxWeight: number | null = null,
    specificWeights?: number[]
): void {
    // Format font name for Google Fonts URL (replace spaces with +)
    const formattedFontName = fontFamily.replace(/\s+/g, '+');
    
    // Build the weights parameter
    let weightsParam: string;
    
    if (isVariable && minWeight !== null && maxWeight !== null) {
        // Variable font: use range syntax (e.g., "wght@100..900")
        weightsParam = `${minWeight}..${maxWeight}`;
    } else if (specificWeights && specificWeights.length > 0) {
        // Static font with specific weights
        weightsParam = specificWeights.sort((a, b) => a - b).join(';');
    } else {
        // Default: load common weights
        weightsParam = '300;400;500;600;700';
    }
    
    // Create a unique key for this font configuration
    const fontKey = `${formattedFontName}:${weightsParam}`;
    
    // Skip if already loaded with same or superset config
    if (loadedFonts.has(fontFamily)) {
        const existingConfig = loadedFonts.get(fontFamily)!;
        // If existing config includes this one, skip
        if (existingConfig === weightsParam || existingConfig.includes('..')) {
            return;
        }
    }
    
    // Create the Google Fonts URL
    const fontUrl = `https://fonts.googleapis.com/css2?family=${formattedFontName}:wght@${weightsParam}&display=swap`;
    
    // Check if this exact link already exists
    const existingLink = document.querySelector(`link[data-font-key="${fontKey}"]`);
    if (existingLink) {
        loadedFonts.set(fontFamily, weightsParam);
        return;
    }
    
    // Remove any previous link for this font (we're loading a better config)
    const oldLinks = document.querySelectorAll(`link[data-font="${formattedFontName}"]`);
    oldLinks.forEach(link => link.remove());
    
    // Create and inject the link tag
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = fontUrl;
    link.setAttribute('data-font', formattedFontName);
    link.setAttribute('data-font-key', fontKey);
    document.head.appendChild(link);
    
    // Mark as loaded
    loadedFonts.set(fontFamily, weightsParam);
    
    console.log(`[FontLoader] Loaded: ${fontFamily} (${isVariable ? 'variable' : 'static'}: ${weightsParam})`);
}

/**
 * Load multiple fonts at once
 */
export function loadGoogleFonts(fonts: Array<{
    family: string;
    isVariable?: boolean;
    minWeight?: number | null;
    maxWeight?: number | null;
    weights?: number[];
}>): void {
    fonts.forEach(font => {
        loadGoogleFont(
            font.family,
            font.isVariable ?? false,
            font.minWeight ?? null,
            font.maxWeight ?? null,
            font.weights
        );
    });
}

/**
 * Preload common fonts used as defaults
 */
export function preloadDefaultFonts(): void {
    // Load Inter as primary default (variable font)
    loadGoogleFont('Inter', true, 100, 900);
    
    // Load a few other common fonts
    loadGoogleFonts([
        { family: 'Roboto', weights: [300, 400, 500, 700] },
        { family: 'Open Sans', weights: [300, 400, 600, 700] },
        { family: 'Noto Sans', isVariable: true, minWeight: 100, maxWeight: 900 },
    ]);
}

/**
 * Check if a font is already loaded
 */
export function isFontLoaded(fontFamily: string): boolean {
    return loadedFonts.has(fontFamily);
}

/**
 * Get the loaded configuration for a font
 */
export function getFontLoadedConfig(fontFamily: string): string | null {
    return loadedFonts.get(fontFamily) ?? null;
}

/**
 * Clear all loaded fonts (for testing)
 */
export function clearLoadedFonts(): void {
    const fontLinks = document.querySelectorAll('link[data-font]');
    fontLinks.forEach(link => link.remove());
    loadedFonts.clear();
}

export default {
    loadGoogleFont,
    loadGoogleFonts,
    preloadDefaultFonts,
    isFontLoaded,
    getFontLoadedConfig,
    clearLoadedFonts,
};
