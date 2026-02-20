/**
 * Text Length Estimator Utility
 * 
 * Estimates the visual width of text based on character count and font properties.
 * Used for calculating input field widths and displaying text length indicators.
 */

import { FontWeightValue } from '../types/builder.types';

/**
 * Estimate the visual width of text based on character count and font properties
 * 
 * @param charCount - Number of characters
 * @param fontProps - Font properties (family, size, weight)
 * @returns Estimated width in pixels
 */
export function estimateTextWidth(
    charCount: number,
    fontProps: { fontFamily: string; fontSize: number; fontWeight: FontWeightValue }
): number {
    // Base character width multiplier
    // Based on actual measurements with longest option displayed:
    // - Ubuntu 14px weight 500, 62 chars = 401px text width needed (467px total - 66px overhead)
    // - That's 6.47px per char = 0.462 multiplier (6.47 / 14)
    // - For weight 500: base * 1.02 = 0.462, so base ≈ 0.453
    // Using 0.453 as base multiplier (precise match to actual rendered width)
    const baseMultiplier = 0.453;
    
    // Adjust for font weight (heavier weights are slightly wider)
    // Based on measurements: Weight 500 adds ~2-3% width vs 400
    // Weight 400 (normal) = 1.0, Weight 500 (medium) = 1.02, Weight 600+ = 1.03
    const weightMultiplier = fontProps.fontWeight >= 600 ? 1.03 : 
                            fontProps.fontWeight >= 500 ? 1.02 : 1.0;
    
    // Adjust for font family (some fonts have different character widths)
    // Condensed fonts (like Roboto Condensed) are narrower - typically 15-20% narrower
    // Regular fonts use 1.0 multiplier
    let familyMultiplier = 1.0;
    
    const fontFamilyLower = fontProps.fontFamily.toLowerCase();
    
    if (fontFamilyLower.includes('condensed')) {
        // Condensed fonts are narrower - reduce width by ~17% (0.83 multiplier)
        familyMultiplier = 0.83;
    } else if (fontFamilyLower.includes('ubuntu')) {
        // Ubuntu matches the base calculation well
        familyMultiplier = 1.0;
    }
    // Other fonts default to 1.0
    
    // Calculate average character width with adjustments
    const avgCharWidth = fontProps.fontSize * baseMultiplier * weightMultiplier * familyMultiplier;
    
    // Calculate estimated width
    const estimatedWidth = charCount * avgCharWidth;
    
    // Round to nearest pixel
    return Math.round(estimatedWidth);
}
