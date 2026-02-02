import React, { useMemo } from 'react';
import type { FontWeightValue, ComponentObject, FormComponent } from '../../types/builder.types';
import type { ComputedFieldStyles } from '../../utils/styleUtils';
import { getComponentCapabilities } from '../../utils/componentCapabilities';
import { getComponentSurfaceCapabilities, type ComponentSurface } from '../../utils/componentSurfaceCapabilities';
import { TextLengthOverlay } from './TextLengthOverlay';

export interface ObjectFeatureHostProps {
    object: ComponentObject;
    component: FormComponent;
    styles: ComputedFieldStyles;
    surface: ComponentSurface;
    builderMode: boolean;
    componentId?: string;
    /**
     * The rendered object content (label/input/validation/etc.)
     * The host will apply overlays without changing the object’s spacing contract.
     */
    children: React.ReactNode;
}

export const ObjectFeatureHost: React.FC<ObjectFeatureHostProps> = ({
    object,
    component,
    styles,
    surface,
    builderMode,
    componentId,
    children,
}) => {
    const surfaceCaps = useMemo(() => getComponentSurfaceCapabilities(component.type, surface), [component.type, surface]);

    // Object-level eligibility: prefer structure-attached features; fallback to legacy capability check for safety.
    const hasObjectFeatureFlag = Boolean(object.features?.textLengthIndicator);
    const eligibleByObject =
        object.features?.textLengthIndicator?.enabled !== false && hasObjectFeatureFlag;
    const eligibleByLegacy =
        !hasObjectFeatureFlag &&
        object.type === 'input' &&
        object.id === 'input' &&
        getComponentCapabilities(component.type).supportsTextLengthIndicator;

    const shouldShowTextLengthIndicator =
        (eligibleByObject || eligibleByLegacy) &&
        surface !== 'runtime' &&
        surfaceCaps.textLengthIndicator.enabled;

    const maxLength = useMemo(() => {
        if (!shouldShowTextLengthIndicator) return undefined;
        const configured = component.props.validation?.maxLength;
        if (configured) return configured;
        // Design-time defaults (builder/toolbox only) for indicator-enabled types.
        const defaults: Partial<Record<string, number>> = {
            'first-name': 30,
            text: 50,
            email: 254,
            textarea: 500,
            address: 120,
        };
        return defaults[component.type];
    }, [shouldShowTextLengthIndicator, component.props.validation?.maxLength, component.type]);

    const computeLineEstimate =
        shouldShowTextLengthIndicator &&
        component.type === 'textarea' &&
        surfaceCaps.textLengthIndicator.showTextareaLineEstimate &&
        maxLength
            ? (size: { width: number; height: number }) => {
                  const widthPx = Math.max(0, size.width);
                  const heightPx = Math.max(0, size.height);

                  const approximateCharWidth = (styles.computed.fontSize || 14) * 0.55;
                  const chromeWidth = ((styles.computed.paddingX ?? 0) + (styles.computed.borderWidth ?? 0)) * 2;
                  const usableWidth = Math.max(40, (widthPx || 320) - chromeWidth);
                  const charsPerLine = Math.max(1, Math.floor(usableWidth / approximateCharWidth));

                  const approximateLineHeight = (styles.computed.fontSize || 14) * 1.4;
                  const chromeHeight = ((styles.computed.paddingY ?? 0) + (styles.computed.borderWidth ?? 0)) * 2;
                  const usableHeight = Math.max(
                      1,
                      (heightPx || styles.computed.inputHeight || 100) - chromeHeight
                  );
                  const fitsLines = Math.max(1, Math.floor(usableHeight / approximateLineHeight));

                  return {
                      needed: Math.max(1, Math.ceil(maxLength / charsPerLine)),
                      fits: fitsLines,
                  };
              }
            : undefined;

    return (
        <TextLengthOverlay
            enabled={Boolean(builderMode && shouldShowTextLengthIndicator && maxLength)}
            maxLength={maxLength}
            fontFamily={styles.computed.fontFamily}
            fontSize={styles.computed.fontSize}
            fontWeight={(styles.computed.fontWeight ?? 400) as FontWeightValue}
            componentId={componentId ? `${componentId}:${object.id}` : undefined}
            borderWidth={styles.computed.borderWidth ?? 1}
            paddingY={styles.computed.paddingY ?? 8}
            componentType={component.type}
            computeLineEstimate={computeLineEstimate}
            showBar={surfaceCaps.textLengthIndicator.showBar}
            showLabel={surfaceCaps.textLengthIndicator.showLabel}
            style={{ display: 'inline-block' }}
        >
            {children}
        </TextLengthOverlay>
    );
};

