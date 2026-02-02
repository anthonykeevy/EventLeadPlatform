/**
 * Spacing Calculation Utilities
 * 
 * Utilities for calculating spacing based on layout type and rules.
 */

import { ObjectLayoutType, GlobalStyles } from '../types/builder.types';

export interface SpacingRules {
    horizontalGap?: number;      // Gap between objects in same row
    verticalSpacing?: number;     // Spacing between rows
    objectGap?: number;          // Generic gap (fallback)
}

export interface SpacingResult {
    groupStyle: React.CSSProperties;
    objectGap: number;
    /** Vertical gap between stacked groups/rows (px) */
    rowGap: number;
    /** Horizontal gap between objects within a row (px) */
    columnGap: number;
}

/**
 * Calculate spacing based on layout type, layout groups, and spacing rules.
 * Returns CSS properties for groups and gap values.
 */
export function calculateSpacing(
    layout: ObjectLayoutType,
    _layoutGroups: Record<string, string[]> | undefined,
    spacingRules: SpacingRules | undefined,
    globalStyles: GlobalStyles | undefined
): SpacingResult {
    // layoutGroups is currently only used by UniversalFieldShell to determine grouping;
    // spacing itself is layout-type driven (vertical/horizontal/mixed).
    void _layoutGroups;

    const baseSpacing = globalStyles?.baseSpacing ?? 8;
    const defaultColumnGap = globalStyles?.objectColumnGapPx ?? baseSpacing;
    // NOTE: Row gap is additive with Layer 2 (labelGap/inputHelpGap). To preserve legacy spacing,
    // treat "unset" as 0 rather than inheriting baseSpacing.
    const defaultRowGap = globalStyles?.objectRowGapPx ?? 0;
    
    // Extract spacing values from rules or use defaults
    const horizontalGap = spacingRules?.horizontalGap ?? defaultColumnGap;
    const verticalSpacing = spacingRules?.verticalSpacing ?? defaultRowGap;
    const objectGap = spacingRules?.objectGap ?? defaultColumnGap;
    
    switch (layout) {
        case 'vertical':
            // Vertical layout: stack objects with vertical spacing
            return {
                groupStyle: {
                    display: 'flex',
                    flexDirection: 'column',
                    gap: `${verticalSpacing}px`
                },
                objectGap: verticalSpacing,
                rowGap: verticalSpacing,
                columnGap: horizontalGap,
            };
            
        case 'horizontal':
            // Horizontal layout: arrange objects in a row with horizontal gap
            return {
                groupStyle: {
                    display: 'flex',
                    flexDirection: 'row',
                    gap: `${horizontalGap}px`,
                    alignItems: 'center'
                },
                objectGap: horizontalGap,
                rowGap: verticalSpacing,
                columnGap: horizontalGap,
            };
            
        case 'mixed':
            // Mixed layout: use layoutGroups to determine spacing
            // Each group is a row, with vertical spacing between rows
            // Objects within a row use horizontal gap
            return {
                groupStyle: {
                    display: 'flex',
                    flexDirection: 'column',
                    gap: `${verticalSpacing}px`
                },
                objectGap: horizontalGap, // Used for objects within same row
                rowGap: verticalSpacing,
                columnGap: horizontalGap,
            };
            
        default:
            // Fallback to vertical
            return {
                groupStyle: {
                    display: 'flex',
                    flexDirection: 'column',
                    gap: `${objectGap}px`
                },
                objectGap,
                rowGap: objectGap,
                columnGap: objectGap,
            };
    }
}

/**
 * Calculate spacing for a specific row in a mixed layout.
 */
export function calculateRowSpacing(
    spacingRules: SpacingRules | undefined,
    globalStyles: GlobalStyles | undefined
): React.CSSProperties {
    const baseSpacing = globalStyles?.baseSpacing ?? 8;
    const horizontalGap = spacingRules?.horizontalGap ?? (globalStyles?.objectColumnGapPx ?? baseSpacing);
    
    return {
        display: 'flex',
        flexDirection: 'row',
        gap: `${horizontalGap}px`,
        alignItems: 'center'
    };
}



