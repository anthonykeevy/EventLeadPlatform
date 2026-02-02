/**
 * TextLengthIndicator Component
 * 
 * Displays estimated text length for input fields based on maxLength and font properties.
 * Shows format: "~{maxLength} chars ({estimatedWidth}px)"
 */

import React, { useMemo, useEffect } from 'react';
import { FontWeightValue } from '../../types/builder.types';
import { estimateCharacterWidth } from '../../utils/widthCalculator';
import { devLogger } from '../../utils/devLogger';

interface TextLengthIndicatorProps {
    /** Maximum character length for the input */
    maxLength?: number;
    /** Font family */
    fontFamily: string;
    /** Font size in pixels */
    fontSize: number;
    /** Font weight */
    fontWeight: FontWeightValue;
    /** Whether the indicator should be visible */
    visible?: boolean;
    /** Component ID for logging */
    componentId?: string;
    /** Container width in pixels (for green bar width calculation) */
    containerWidth?: number;
    /** Border width of the input (for positioning) */
    borderWidth?: number;
    /** Padding Y of the input (for positioning) */
    paddingY?: number;
    /** Line estimate for textarea (shows how many lines needed) */
    lineEstimate?: { needed: number; fits: number };
    /** Component type (to determine if textarea) */
    componentType?: string;
    /** Whether to show the green bar */
    showBar?: boolean;
    /** Whether to show the text label (~500 chars ...) */
    showLabel?: boolean;
}

export const TextLengthIndicator: React.FC<TextLengthIndicatorProps> = ({
    maxLength,
    fontFamily,
    fontSize,
    fontWeight,
    visible = true,
    componentId,
    containerWidth,
    borderWidth = 1,
    lineEstimate,
    componentType,
    showBar = true,
    showLabel = true,
}) => {
    const estimatedWidth = useMemo(() => {
        if (!maxLength) return 0;
        // Use actual measurement: measure 100 random characters to get per-character width
        // Then multiply by maxLength to estimate total width needed
        return estimateCharacterWidth(maxLength, { fontFamily, fontSize, fontWeight }, 1.0);
    }, [maxLength, fontFamily, fontSize, fontWeight]);
    
    // Calculate guide bar width (clamped to container width if provided)
    const guideDisplayWidth = containerWidth
        ? Math.min(estimatedWidth, containerWidth)
        : estimatedWidth;
    
    // Guide bar colors
    const guideFill = 'rgba(34, 197, 94, 0.6)'; // green-500 with opacity
    const guideBorder = 'rgba(0, 0, 0, 0.35)';
    
    // Log text length calculation
    useEffect(() => {
        if (visible && maxLength) {
            devLogger.info('canvas.textlength.calculated', {
                componentId: componentId || 'unknown',
                maxLength,
                estimatedWidth,
                guideDisplayWidth,
                containerWidth,
                fontFamily,
                fontSize,
                fontWeight,
            });
        }
    }, [visible, maxLength, estimatedWidth, guideDisplayWidth, containerWidth, fontFamily, fontSize, fontWeight, componentId]);
    
    if (!visible || !maxLength) {
        devLogger.debug('canvas.textlength.indicator.hidden', {
            componentId: componentId || 'unknown',
            reason: !visible ? 'visible=false' : 'maxLength missing',
            maxLength,
            visible
        });
        return null;
    }
    
    // Log when indicator is actually rendered
    devLogger.debug('canvas.textlength.indicator.rendered', {
        componentId: componentId || 'unknown',
        maxLength,
        estimatedWidth,
        guideDisplayWidth,
        hasGreenBar: true
    });
    
    const barHeight = 8;
    const gap = 2;
    const labelHeight = 18; // approximate (px) used only for stacking offsets

    const baseBottom = borderWidth;
    const labelBottom = baseBottom + (showBar ? barHeight + gap : 0);
    const lineBadgeBottom = labelBottom + (showLabel ? labelHeight + gap : 0);

    return (
        <>
            {/* Green bar indicator (anchored to the inner bottom edge of the input). */}
            {showBar && (
                <div
                    style={{
                        position: 'absolute',
                        left: `${borderWidth}px`,
                        right: `${borderWidth}px`,
                        // Align with the bottom border of the input object (inside the border).
                        bottom: `${baseBottom}px`,
                        pointerEvents: 'none',
                        height: barHeight,
                        border: `1px solid ${guideBorder}`,
                        borderRadius: 4,
                        overflow: 'hidden',
                        backgroundColor: 'transparent',
                        zIndex: 10, // Above input but below text
                    }}
                >
                    <div
                        style={{
                            height: '100%',
                            width: `${guideDisplayWidth}px`,
                            maxWidth: '100%',
                            backgroundColor: guideFill,
                        }}
                    />
                </div>
            )}

            {/* Text indicator */}
            {showLabel && (
                <div
                    className="text-length-indicator absolute right-1 text-xs text-gray-400 dark:text-gray-500 pointer-events-none z-50"
                    style={{
                        bottom: `${labelBottom}px`,
                        backgroundColor: 'rgba(255, 255, 255, 0.9)',
                        border: '1px solid rgba(0, 0, 0, 0.15)',
                        borderRadius: 4,
                        padding: '2px 6px',
                    }}
                >
                    ~{maxLength} chars ({estimatedWidth}px)
                </div>
            )}

            {/* Line estimate badge for textarea */}
            {componentType === 'textarea' && lineEstimate && (
                <div
                    style={{
                        position: 'absolute',
                        right: 6,
                        bottom: `${lineBadgeBottom}px`,
                        fontSize: Math.max(10, fontSize - 2),
                        color: lineEstimate.fits >= lineEstimate.needed ? '#166534' : '#0f172a',
                        backgroundColor:
                            lineEstimate.fits >= lineEstimate.needed ? 'rgba(34,197,94,0.15)' : 'rgba(255,255,255,0.9)',
                        border:
                            lineEstimate.fits >= lineEstimate.needed
                                ? '1px solid rgba(34,197,94,0.45)'
                                : '1px solid rgba(0,0,0,0.15)',
                        borderRadius: 6,
                        padding: '2px 6px',
                        pointerEvents: 'none',
                        zIndex: 15, // Above green bar and text indicator
                    }}
                >
                    ≈ {lineEstimate.needed} lines for max length
                    {lineEstimate.fits > 0 ? ` (fits ~${lineEstimate.fits})` : ''}
                </div>
            )}
        </>
    );
};
