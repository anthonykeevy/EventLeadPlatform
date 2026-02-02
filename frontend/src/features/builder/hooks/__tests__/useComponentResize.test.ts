/**
 * Tests for useComponentResize pure calculation functions
 * 
 * Run with: npm test -- --testPathPattern="useComponentResize"
 */

import { 
    calculatePreviewWidths, 
    willColumnsFit, 
    screenToBasePx,
    CapturedObjectWidths 
} from '../useComponentResize';

describe('calculatePreviewWidths', () => {
    const baseCapturedWidths: CapturedObjectWidths = {
        labelWidth: 70,
        inputWidth: 200,
        helpWidth: 100,
        columnGapPx: 8,
        totalExtras: 26, // 2 gaps (16) + SmartBorder padding (10)
    };

    it('keeps label and help fixed, adjusts input for expansion', () => {
        // Expanding component: 500px total
        const result = calculatePreviewWidths(500, baseCapturedWidths);
        
        expect(result.labelWidthOverride).toBe(70);  // unchanged
        expect(result.helpWidthOverride).toBe(100);  // unchanged
        // Available: 500 - 70 - 100 - 26 = 304
        expect(result.inputWidthOverride).toBe(304);
    });

    it('clamps input to minimum when shrinking significantly', () => {
        // Shrinking to very narrow: input would be negative
        const result = calculatePreviewWidths(200, baseCapturedWidths);
        
        expect(result.labelWidthOverride).toBe(70);
        expect(result.helpWidthOverride).toBe(100);
        // Available: 200 - 70 - 100 - 26 = 4 (less than min 60)
        expect(result.inputWidthOverride).toBe(60); // clamped to minimum
    });

    it('handles exact fit scenario', () => {
        // Component width that exactly fits min input
        // 70 + 60 + 100 + 26 = 256
        const result = calculatePreviewWidths(256, baseCapturedWidths);
        
        expect(result.labelWidthOverride).toBe(70);
        expect(result.helpWidthOverride).toBe(100);
        expect(result.inputWidthOverride).toBe(60);
    });

    it('respects custom minimum input width', () => {
        const result = calculatePreviewWidths(200, baseCapturedWidths, 100);
        
        // With min 100, should clamp to 100
        expect(result.inputWidthOverride).toBe(100);
    });
});

describe('willColumnsFit', () => {
    it('returns true when columns fit within container', () => {
        // 70 + 150 + 100 + 16 = 336, container = 400
        const result = willColumnsFit(400, 70, 150, 100, 8);
        expect(result).toBe(true);
    });

    it('returns false when columns exceed container', () => {
        // 70 + 150 + 100 + 16 = 336, container = 300
        const result = willColumnsFit(300, 70, 150, 100, 8);
        expect(result).toBe(false);
    });

    it('returns true for exact fit', () => {
        // 70 + 150 + 100 + 16 = 336, container = 336
        const result = willColumnsFit(336, 70, 150, 100, 8);
        expect(result).toBe(true);
    });

    it('handles zero gap', () => {
        // 70 + 150 + 100 + 0 = 320, container = 320
        const result = willColumnsFit(320, 70, 150, 100, 0);
        expect(result).toBe(true);
    });
});

describe('screenToBasePx', () => {
    it('converts screen pixels to base pixels at 100% scale', () => {
        // 100% component scale, 1.0 canvas scale
        const result = screenToBasePx(200, 100, 1.0);
        expect(result).toBe(200);
    });

    it('converts screen pixels to base pixels at 50% canvas zoom', () => {
        // 100% component scale, 0.5 canvas scale (zoomed out)
        const result = screenToBasePx(100, 100, 0.5);
        expect(result).toBe(200); // 100 / (1.0 * 0.5) = 200
    });

    it('converts screen pixels to base pixels at 150% component scale', () => {
        // 150% component scale, 1.0 canvas scale
        const result = screenToBasePx(150, 150, 1.0);
        expect(result).toBe(100); // 150 / (1.5 * 1.0) = 100
    });

    it('handles combined scaling', () => {
        // 150% component scale, 0.5 canvas scale
        const result = screenToBasePx(150, 150, 0.5);
        expect(result).toBe(200); // 150 / (1.5 * 0.5) = 200
    });

    it('handles zero scale by returning input unchanged', () => {
        const result = screenToBasePx(100, 0, 1.0);
        expect(result).toBe(100);
    });
});
