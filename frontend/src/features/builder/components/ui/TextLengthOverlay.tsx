import React from 'react';
import type { FontWeightValue } from '../../types/builder.types';
import { TextLengthIndicator } from './TextLengthIndicator';
import { useMeasuredSize } from '../../hooks/useMeasuredSize';
import type { MeasuredSize } from '../../hooks/useMeasuredSize';

export interface TextLengthOverlayProps {
    enabled: boolean;
    maxLength?: number;
    fontFamily: string;
    fontSize: number;
    fontWeight: FontWeightValue;
    borderWidth?: number;
    paddingY?: number;
    componentId?: string;
    componentType?: string;
    lineEstimate?: { needed: number; fits: number };
    /** Compute a line estimate from measured size (used for textarea) */
    computeLineEstimate?: (size: MeasuredSize) => { needed: number; fits: number } | undefined;
    showBar?: boolean;
    showLabel?: boolean;
    /** Optional wrapper style (keeps layout contracts stable) */
    style?: React.CSSProperties;
    children: React.ReactNode;
}

/**
 * TextLengthOverlay
 * Wraps a control and renders TextLengthIndicator as an overlay using real DOM measurement.
 * This is used both for top-level objects (via ObjectFeatureHost) and for sub-controls
 * (e.g. selection “extra text” inputs).
 */
export const TextLengthOverlay: React.FC<TextLengthOverlayProps> = ({
    enabled,
    maxLength,
    fontFamily,
    fontSize,
    fontWeight,
    borderWidth,
    paddingY,
    componentId,
    componentType,
    lineEstimate,
    computeLineEstimate,
    showBar = true,
    showLabel = true,
    style,
    children,
}) => {
    const { ref, size } = useMeasuredSize<HTMLDivElement>();

    if (!enabled || !maxLength) return <>{children}</>;

    const effectiveLineEstimate = lineEstimate ?? computeLineEstimate?.(size);

    return (
        <div
            ref={ref}
            style={{
                position: 'relative',
                // Preserve shrink-to-content by default; callers can override with `style`.
                display: 'inline-block',
                maxWidth: '100%',
                ...style,
            }}
        >
            {children}
            <TextLengthIndicator
                maxLength={maxLength}
                fontFamily={fontFamily}
                fontSize={fontSize}
                fontWeight={fontWeight}
                visible={true}
                componentId={componentId}
                containerWidth={size.width || undefined}
                borderWidth={borderWidth}
                paddingY={paddingY}
                lineEstimate={effectiveLineEstimate}
                componentType={componentType}
                showBar={showBar}
                showLabel={showLabel}
            />
        </div>
    );
};

