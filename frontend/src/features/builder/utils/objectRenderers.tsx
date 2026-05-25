/**
 * Object Renderer Utilities
 * 
 * Type-safe renderer utilities for common object types (label, input, validation, action, status).
 * These can be reused across components.
 */

import React from 'react';
import { AlertCircle, ExternalLink, Loader2, Send, Star } from 'lucide-react';
import { ComponentObject, FormComponent, ObjectLayoutType, ComponentProps, FontWeightValue } from '../types/builder.types';
import { ComputedFieldStyles } from '../utils/styleUtils';
import { StyledInput, StyledSelect, StyledTextarea } from '../components/styled';
import { TextLengthOverlay } from '../components/ui/TextLengthOverlay';
import { devLogger } from '../utils/devLogger';
import { measureTextWidth } from '../utils/widthCalculator';
import { getComponentCapabilities } from './componentCapabilities';
import { getComponentSurfaceCapabilities, type ComponentSurface } from './componentSurfaceCapabilities';

/** Placeholder inside the URL field is host/path only when a prefix (e.g. https://) is shown beside it. */
function effectiveUrlInputPlaceholder(placeholder: string | undefined, prefix: string | undefined): string {
    const fallback = 'example.com';
    let text = (placeholder ?? '').trim() || fallback;
    const pref = (prefix ?? '').trim();
    if (pref && text.toLowerCase().startsWith(pref.toLowerCase())) {
        text = text.slice(pref.length).trim() || fallback;
    }
    return text;
}

/**
 * When true, strip label/input vertical margins so flex row alignment or same-row grid cells stay aligned.
 * Grid + one object per row keeps margins so Typography "Label ↓ Input" still affects canvas/runtime.
 */
function suppressVerticalFieldMargins(
    layout: ObjectLayoutType,
    isGridLayout?: boolean,
    inRowGroup?: boolean
): boolean {
    if (layout === 'horizontal') return true;
    if (inRowGroup && (isGridLayout || layout === 'mixed')) return true;
    return false;
}

const TermsLinkComponent: React.FC<{
    component: FormComponent;
    primaryColor?: string;
    linkText: string;
    isCanvas: boolean;
}> = ({ component, primaryColor, linkText, isCanvas }) => {
    const [showModal, setShowModal] = React.useState(false);
    const url = component.props.termsUrl;
    const content = component.props.termsContent;
    const displayMode = component.props.termsDisplayMode || 'popup';
    const displayWidth = component.props.termsDisplayWidth || 720;
    const displayHeight = component.props.termsDisplayHeight || 600;

    return (
        <>
            <span
                onClick={(e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    if (isCanvas) return;
                    if (content) {
                        setShowModal(true);
                    } else if (url) {
                        if (displayMode === 'new_tab') {
                            const parsedUrl = new URL(url, window.location.origin);
                            parsedUrl.searchParams.set('viewer', 'inline');
                            window.open(parsedUrl.toString(), '_blank', 'noopener,noreferrer');
                        } else {
                            setShowModal(true);
                        }
                    }
                }}
                style={{
                    color: primaryColor,
                    textDecoration: 'underline',
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: 4,
                    cursor: isCanvas ? 'default' : 'pointer',
                    pointerEvents: isCanvas ? 'none' : 'auto',
                }}
            >
                {linkText}
                <ExternalLink size={12} />
            </span>
            {showModal && (content || url) && (
                <div 
                    className="fixed inset-0 flex items-center justify-center z-[9999]"
                    style={{ backgroundColor: 'rgba(0, 0, 0, 0.5)' }}
                    onClick={(e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        setShowModal(false);
                    }}
                >
                    <div 
                        className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[80vh] flex flex-col"
                        onClick={(e) => e.stopPropagation()}
                        style={{
                            maxWidth: url && !content ? displayWidth : undefined,
                            height: url && !content ? displayHeight : undefined
                        }}
                    >
                        <div className="flex items-center justify-between px-6 py-4 border-b">
                            <h3 className="text-lg font-semibold text-gray-800 m-0">
                                {linkText}
                            </h3>
                            <button
                                type="button"
                                onClick={(e) => {
                                    e.preventDefault();
                                    e.stopPropagation();
                                    setShowModal(false);
                                }}
                                className="text-gray-400 hover:text-gray-600 text-xl font-bold p-2 leading-none cursor-pointer"
                            >
                                &times;
                            </button>
                        </div>
                        <div className="flex-1 overflow-hidden flex flex-col min-h-0">
                            {content ? (
                                <div className="flex-1 overflow-y-auto px-6 py-4">
                                    <div 
                                        className="prose prose-sm max-w-none"
                                        dangerouslySetInnerHTML={{ __html: content }}
                                    />
                                </div>
                            ) : (
                                <iframe 
                                    src={url + (url?.includes('?') ? '&' : '?') + 'viewer=inline'} 
                                    className="w-full h-full min-h-[300px] border-0"
                                    title={linkText}
                                />
                            )}
                        </div>
                        <div className="px-6 py-4 border-t bg-gray-50 rounded-b-lg flex justify-end flex-shrink-0">
                            <button
                                type="button"
                                onClick={(e) => {
                                    e.preventDefault();
                                    e.stopPropagation();
                                    setShowModal(false);
                                }}
                                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium cursor-pointer"
                            >
                                Close
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
};

/**
 * ValidationArea component for displaying validation errors.
 * In builder mode, shows a placeholder message so SmartBorder accounts for full validation space.
 */
const ValidationArea: React.FC<{ 
    error?: string; 
    helpTextStyle?: React.CSSProperties;
    componentId: string;
    builderMode?: boolean;
    placeholderMessage?: string;
}> = ({ error, helpTextStyle, componentId, builderMode, placeholderMessage }) => {
    const baseColor =
        (helpTextStyle?.color as string | undefined) ??
        '#DC2626';
    const displayColor = builderMode && !error ? '#9CA3AF' : baseColor;

    const typographyOnly = (s?: React.CSSProperties): React.CSSProperties => ({
        fontFamily: s?.fontFamily,
        fontSize: s?.fontSize,
        fontWeight: s?.fontWeight,
        fontStyle: s?.fontStyle,
        lineHeight: s?.lineHeight,
        letterSpacing: s?.letterSpacing,
    });

    // IMPORTANT:
    // - HelpText styles may include `display: inline-block` (when borders enabled).
    // - If applied to the message row, it overrides `display:flex` and forces icon/text to stack.
    // So: keep typography, but force a flex row for the message.
    const messageStyle: React.CSSProperties = {
        ...typographyOnly(helpTextStyle),
        color: displayColor,
        display: 'flex',
        alignItems: 'flex-start',
        gap: 6,
    };

    // In builder mode, show placeholder if no error (so SmartBorder accounts for space)
    const displayMessage = error || (builderMode && placeholderMessage ? placeholderMessage : null);

    // Avoid rendering an "empty bordered box" when there is no message in runtime.
    // Preserve vertical spacing via marginTop when configured.
    const outerStyle: React.CSSProperties = displayMessage
        ? { minHeight: 18, ...helpTextStyle }
        : {
            minHeight: 18,
            ...(helpTextStyle?.marginTop !== undefined ? { marginTop: helpTextStyle.marginTop } : {}),
        };

    return (
        <div 
            id={`${componentId}-error`}
            className="text-sm"
            style={outerStyle}
            role="alert"
            aria-live="polite"
            aria-atomic="true"
        >
            {displayMessage ? (
                <div className="flex items-start gap-1.5" style={messageStyle}>
                    <AlertCircle 
                        className="h-4 w-4 mt-0.5 flex-shrink-0" 
                        aria-hidden="true"
                        style={{ color: displayColor }}
                    />
                    <span style={{ color: displayColor }}>
                        {displayMessage}
                    </span>
                </div>
            ) : null}
        </div>
    );
};

export interface ObjectRendererProps {
    object: ComponentObject;
    component: FormComponent;
    styles: ComputedFieldStyles;
    layout: ObjectLayoutType;
    componentId?: string;
    /**
     * Rendering surface (toolbox/canvas/runtime). When undefined, renderer falls back to:
     * - 'canvas' if builderMode is true
     * - 'runtime' otherwise
     */
    surface?: ComponentSurface;
    /** Optional override for primary color (some styled components support it) */
    primaryColor?: string;
    tabIndex?: number;
    inputRef?: React.RefObject<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement | null>;
    // Additional context based on object type
    value?: unknown;
    onChange?: (value: unknown) => void;
    error?: string;
    disabled?: boolean;
    required?: boolean;
    // For action/button objects
    buttonText?: string;
    onClick?: () => void;
    isLoading?: boolean;
    // For validation objects (runtime may pass string[] or Record<string, string[]>)
    validationErrors?: Record<string, string> | string[];
    allFormErrors?: Record<string, string> | Record<string, string[]>;
    // Form-level validation context for submit button
    formValidationContext?: {
        errors: Record<string, string>;
        errorsByPriority: Array<{ componentId: string; error: string; tabOrder: number; label: string }>;
        firstError?: string;
        errorCount: number;
    };
    // Builder mode flag (for showing placeholders)
    builderMode?: boolean;
    /**
     * True when this object is being rendered alongside other objects in the same horizontal row.
     * Used to avoid per-object margin offsets that would defeat rowAlignment (flex align-items).
     */
    inRowGroup?: boolean;
    // Width overrides for object categories (from E/W resize)
    labelWidthOverride?: number;
    inputWidthOverride?: number;
    helpWidthOverride?: number;
    actionWidthOverride?: number; // For button action objects
    // Height override for action/button objects (used by submit button resize)
    actionHeightOverride?: number;
    // Height override for display objects (used by paragraph/header resize)
    displayHeightOverride?: number;
    // True when rendering inside a Grid Layout cell
    isGridLayout?: boolean;
    /** When true, render with focus styling (e.g. Focus Color cycling in Form Branding Defaults) */
    simulateFocus?: boolean;
}

export type ObjectRenderer = (props: ObjectRendererProps) => React.ReactNode;

export interface ObjectRenderers {
    [objectId: string]: ObjectRenderer;
}

/**
 * Create a standard label renderer with Required * support.
 */
export function createLabelRenderer(): ObjectRenderer {
    return ({ component, styles, required, componentId, labelWidthOverride, layout, inRowGroup, surface, builderMode, isGridLayout }) => {
        const label = component.props.label;
        if (!label && !required) {
            return null;
        }
        
        const labelId = componentId ? `${componentId}-label` : undefined;
        const effectiveSurface = surface ?? (builderMode ? 'canvas' : 'runtime');
        const isCanvas = effectiveSurface === 'canvas';
        
        // Apply width override if set (from E/W resize)
        const labelStyle: React.CSSProperties = {
            ...styles.labelStyle,
            // Parity: In vertical layouts, the label should visually behave like "shrink-to-text"
            // (avoid flex-column default `align-items: stretch`).
            //
            // In horizontal/mixed rows, do NOT override alignSelf, otherwise the label will
            // ignore rowAlignment (flex align-items) and appear stuck to the top.
            ...(inRowGroup ? {} : { alignSelf: 'flex-start' }),
            // Remove vertical margins when objects share one flex/grid row; keep for vertical stacks (incl. grid rows).
            marginTop: suppressVerticalFieldMargins(layout, isGridLayout, inRowGroup) ? 0 : styles.labelStyle.marginTop,
            marginBottom: suppressVerticalFieldMargins(layout, isGridLayout, inRowGroup) ? 0 : styles.labelStyle.marginBottom,
            ...(labelWidthOverride && {
                maxWidth: labelWidthOverride,
                // Allow wrapping when width is constrained
                whiteSpace: 'normal',
                wordWrap: 'break-word',
            }),
        };
        
        return (
            <label
                id={labelId}
                htmlFor={componentId ? `${componentId}-input` : undefined}
                style={labelStyle}
            >
                {component.type === 'terms' ? (
                    <>
                        {label}{' '}
                        <TermsLinkComponent 
                            component={component} 
                            primaryColor={styles.computed.primaryColor} 
                            linkText={String(component.props.termsLinkText ?? 'Terms')} 
                            isCanvas={isCanvas}
                        />
                        {required && <span className="text-red-600"> *</span>}
                    </>
                ) : (
                    <>
                        {label}
                        {required && <span className="text-red-600"> *</span>}
                    </>
                )}
            </label>
        );
    };
}

/**
 * Create a standard input renderer with StyledInput.
 */
export function createInputRenderer(): ObjectRenderer {
    return ({ component, styles, value, onChange, disabled, required, error, componentId, primaryColor, inputRef, tabIndex, inputWidthOverride, builderMode, layout, surface, isGridLayout, inRowGroup, simulateFocus }) => {
        const inputId = componentId ? `${componentId}-input` : undefined;
        const placeholder = component.props.placeholder;
        
        const effectiveSurface: ComponentSurface = surface ?? (builderMode ? 'canvas' : 'runtime');
        const surfaceCaps = getComponentSurfaceCapabilities(component.type, effectiveSurface);

        const showTextLengthIndicator =
            getComponentCapabilities(component.type).supportsTextLengthIndicator &&
            surfaceCaps.textLengthIndicator.enabled;

        // Get maxLength from validation, or use a default ONLY for indicator-enabled types (builder mode).
        let maxLength = component.props.validation?.maxLength;
        if (effectiveSurface !== 'runtime' && showTextLengthIndicator && !maxLength) {
            const defaultMaxLengthMap: Record<string, number> = {
                'first-name': 30,
                'text': 50,
                'email': 254,
                'textarea': 500,
                // Address is variable; pick a conservative default for design-time guidance.
                'address': 120,
                'address-lookup-au': 120,
                'company-lookup-abr': 200,
            };
            maxLength = defaultMaxLengthMap[component.type];
        }
        
        // Apply width override if set (from E/W resize)
        // Input does NOT wrap - it maintains a fixed width
        // Ensure no vertical margins in horizontal layouts to prevent alignment issues
        
        // Normalize inputWidthOverride to a pixel string for CSS consistency
        // Handle both number (e.g., 578) and string (e.g., "578px") formats
        const normalizedInputWidth = inputWidthOverride != null && inputWidthOverride !== 0
            ? (typeof inputWidthOverride === 'number' 
                ? `${inputWidthOverride}px` 
                : String(inputWidthOverride).endsWith('px') 
                    ? inputWidthOverride 
                    : `${parseInt(String(inputWidthOverride), 10)}px`)
            : undefined;

        const inputWidthMode = component.props.inputWidthMode;
        const hasPercentWidth = component.props.width?.endsWith('%');
        const allowInputWidthOverride =
            !hasPercentWidth &&
            (inputWidthMode === 'fixed' || inputWidthMode == null);
        
        const inputStyle: React.CSSProperties = {
            ...styles.inputStyle,
            marginTop: suppressVerticalFieldMargins(layout, isGridLayout, inRowGroup) ? 0 : styles.inputStyle.marginTop,
            marginBottom: suppressVerticalFieldMargins(layout, isGridLayout, inRowGroup) ? 0 : styles.inputStyle.marginBottom,
            ...(normalizedInputWidth && allowInputWidthOverride && {
                width: normalizedInputWidth,
                maxWidth: normalizedInputWidth,
                minWidth: normalizedInputWidth, // Ensure minimum width is also respected
            }),
        };
        
        // Determine input type based on component type
        const inputType = component.type === 'date'
            ? getDateInputType(component.props.dateType)
            : getInputType(component.type);

        const dateBounds =
            component.type === 'date' && inputType === 'date'
                ? getDateBoundsForInput(component.props.validation)
                : undefined;
        
        // Terms (canvas/builder): checkbox input (single option)
        if (component.type === 'file-upload') {
            return (
                <div
                    style={{
                        ...inputStyle,
                        display: 'flex',
                        alignItems: 'center',
                        gap: 8,
                        color: styles.computed.helpTextColor || '#6b7280',
                    }}
                >
                    <span aria-hidden>📎</span>
                    <span>File upload</span>
                </div>
            );
        }

        if (component.type === 'terms') {
            const primary = primaryColor || styles.computed.primaryColor;
            return (
                <input
                    id={inputId}
                    type="checkbox"
                    disabled={builderMode ? true : disabled}
                    checked={Boolean(value)}
                    onChange={(e) => onChange?.(e.target.checked)}
                    aria-invalid={!!error}
                    aria-describedby={error && componentId ? `${componentId}-error` : undefined}
                    aria-required={required}
                    style={{
                        width: 16,
                        height: 16,
                        marginTop: 0,
                        accentColor: primary,
                        ...(simulateFocus && primary && {
                            outline: `2px solid ${primary}`,
                            outlineOffset: '2px',
                            boxShadow: `0 0 0 2px ${primary}33`,
                        }),
                    }}
                />
            );
        }

        if (component.type === 'url') {
            const isRuntime = effectiveSurface === 'runtime';
            const runtimeValue = typeof value === 'string' ? value : '';
            const prefix = component.props.urlPrefix;
            const urlPlaceholder = effectiveUrlInputPlaceholder(placeholder, prefix);

            // When prefix is active, we render a flex container with the prefix and a borderless input
            if (prefix) {
                return (
                    <div style={{
                        ...inputStyle,
                        width: normalizedInputWidth || inputStyle.width || '100%',
                        maxWidth: '100%',
                        minWidth: 0,
                        display: 'flex',
                        alignItems: 'center',
                        overflow: 'hidden',
                        padding: 0, // Remove padding from container, apply to input
                        ...(simulateFocus && primaryColor && {
                            outline: `2px solid ${primaryColor}`,
                            outlineOffset: '2px',
                            boxShadow: `0 0 0 2px ${primaryColor}33`,
                        }),
                        ...(error && {
                            borderColor: '#ef4444',
                        })
                    }}>
                        <div style={{
                            padding: `0 ${styles.computed.inputPaddingX}px`,
                            color: styles.computed.helpTextColor || '#6b7280',
                            backgroundColor: 'rgba(0,0,0,0.02)',
                            borderRight: `1px solid ${styles.computed.inputBorderColor || '#e5e7eb'}`,
                            display: 'flex',
                            alignItems: 'center',
                            height: '100%',
                            whiteSpace: 'nowrap',
                            userSelect: 'none'
                        }}>
                            {prefix}
                        </div>
                        <input
                            ref={inputRef as React.RefObject<HTMLInputElement>}
                            id={inputId}
                            type="url"
                            disabled={disabled}
                            required={required}
                            tabIndex={tabIndex}
                            maxLength={maxLength}
                            placeholder={urlPlaceholder}
                            value={isRuntime ? runtimeValue : ''}
                            onChange={e => onChange?.(e.target.value)}
                            style={{
                                flex: 1,
                                height: '100%',
                                border: 'none',
                                outline: 'none',
                                background: 'transparent',
                                padding: `0 ${styles.computed.inputPaddingX}px`,
                                color: styles.computed.textColor,
                                minWidth: 0,
                            }}
                            onBlur={e => {
                                if (!isRuntime) return;
                                const raw = e.target.value.trim();
                                if (raw.length === 0) return;
                                // If the prefix provides the scheme, we don't need to auto-append one
                                const hasScheme = /^[a-zA-Z][a-zA-Z\d+\-.]*:\/\//.test(raw);
                                const prefixHasScheme = /^[a-zA-Z][a-zA-Z\d+\-.]*:\/\//.test(prefix);
                                if (!hasScheme && !prefixHasScheme) {
                                    onChange?.(`https://${raw}`);
                                }
                            }}
                        />
                    </div>
                );
            }

            return (
                <StyledInput
                    ref={inputRef as React.RefObject<HTMLInputElement>}
                    id={inputId}
                    styles={{
                        ...inputStyle,
                        width: normalizedInputWidth || inputStyle.width || '100%',
                        maxWidth: '100%',
                        minWidth: 0,
                    }}
                    primaryColor={primaryColor || styles.computed.primaryColor}
                    simulateFocus={simulateFocus}
                    disabled={disabled}
                    error={error}
                    componentId={componentId}
                    type="url"
                    placeholder={urlPlaceholder}
                    value={isRuntime ? runtimeValue : ''}
                    onChange={e => onChange?.(e.target.value)}
                    maxLength={maxLength}
                    tabIndex={tabIndex}
                    required={required}
                    onBlur={e => {
                        if (!isRuntime) return;
                        const raw = e.target.value.trim();
                        if (raw.length === 0) return;
                        const hasScheme = /^[a-zA-Z][a-zA-Z\d+\-.]*:\/\//.test(raw);
                        if (!hasScheme) {
                            onChange?.(`https://${raw}`);
                        }
                    }}
                />
            );
        }

        if (component.type === 'rating') {
            const ratingMax = Math.max(1, Math.min(10, Number(component.props.ratingMax ?? 5)));
            const ratingStyle = component.props.ratingStyle ?? 'stars';
            const isRuntime = effectiveSurface === 'runtime';
            const currentValueRaw = typeof value === 'number' ? value : Number(value ?? 0);
            const currentValue = Number.isFinite(currentValueRaw) ? currentValueRaw : 0;
            const so = component.props.styleOverrides;
            const hasTextColorOverride = Boolean(so && 'textColor' in so && so.textColor !== undefined);
            const hasRatingColorOverride = Boolean(so && 'ratingColor' in so && so.ratingColor !== undefined);
            // Typography "Input Text" colour drives marks; legacy ratingColor if only that was set.
            const markColor = hasTextColorOverride
                ? styles.computed.textColor
                : hasRatingColorOverride
                  ? String(so!.ratingColor)
                  : styles.computed.ratingColor || styles.computed.textColor || styles.computed.primaryColor || '#2563EB';
            const hasTextBgOverride = Boolean(so && 'textBackgroundColor' in so && so.textBackgroundColor !== undefined);
            const hasRatingBgOverride = Boolean(so && 'ratingBackgroundColor' in so && so.ratingBackgroundColor !== undefined);
            const cellBg = hasTextBgOverride
                ? (styles.computed.textBackgroundColor ?? 'transparent')
                : hasRatingBgOverride
                  ? String(so!.ratingBackgroundColor)
                  : styles.computed.ratingBackgroundColor ?? styles.computed.textBackgroundColor ?? 'transparent';
            const fontSz = styles.computed.fontSize ?? 14;
            const starSize = Math.max(14, Math.round(fontSz * 1.25));
            const numberSide = Math.max(28, Math.round(fontSz * 2), Math.min(styles.computed.inputHeight, 50));
            // Match resolved input border (same rules as Typography → Input, including per-component textBorder*).
            const resolvedBorderW = styles.inputStyle.borderWidth;
            const useTypographyBorder =
                (typeof resolvedBorderW === 'string' && resolvedBorderW !== '0px') ||
                (typeof resolvedBorderW === 'number' && resolvedBorderW > 0);
            const borderCol = (styles.inputStyle.borderColor as string | undefined) ?? '#D1D5DB';
            const borderW = useTypographyBorder
                ? Math.max(
                      1,
                      typeof resolvedBorderW === 'string'
                          ? Number.parseFloat(resolvedBorderW) || 1
                          : Number(resolvedBorderW) || 1
                  )
                : 1;
            const cellBorderRadius: React.CSSProperties['borderRadius'] = useTypographyBorder
                ? (styles.inputStyle.borderRadius as React.CSSProperties['borderRadius'])
                : ratingStyle === 'numbers'
                  ? 6
                  : 0;

            const renderMark = (index: number) => {
                if (ratingStyle === 'numbers') {
                    return String(index + 1);
                }
                if (ratingStyle === 'emoji') {
                    return index < Math.ceil(ratingMax / 3) ? '😞' : index < Math.ceil((ratingMax * 2) / 3) ? '😐' : '😄';
                }
                return (
                    <Star
                        size={starSize}
                        fill={index + 1 <= currentValue ? markColor : 'none'}
                        color={markColor}
                    />
                );
            };

            return (
                <div style={{ 
                    display: 'flex', 
                    flexDirection: 'column', 
                    gap: 8,
                    minHeight: styles.computed.inputHeight ? `${styles.computed.inputHeight}px` : undefined,
                    justifyContent: 'center'
                }}>
                    {/* Story 6.3.1 (UAT round 10) — rating no-wrap policy.
                       *
                       * Previously this row used ``flexWrap: 'wrap'`` which
                       * masked an underlying width-budget mismatch: in canvas
                       * the ``ValidationArea`` placeholder ("Validation error
                       * message") gives the validation grid track a
                       * ``max-content`` width of ~170 px, leaving the input
                       * track too narrow for >5 stars and wrapping the row.
                       * In runtime the placeholder is absent so the same
                       * rating renders cleanly on one line. The result was a
                       * designer/runtime parity break — UAT round 10 #2 / #7.
                       *
                       * Resolution: pin ``flexWrap: 'nowrap'`` so the rating
                       * always renders on a single line in BOTH surfaces. If
                       * the user adds stars beyond the AI-reserved bounding
                       * box the rating extends past the box edge instead of
                       * silently wrapping — which is the right visual cue
                       * that the component needs more horizontal room (the
                       * AI generation snapshot reserved space for the
                       * stars-at-compile-time count, not for later edits). */}
                    <div style={{ display: 'flex', alignItems: 'center', gap: 6, flexWrap: 'nowrap' }}>
                        {Array.from({ length: ratingMax }).map((_, index) => {
                            const selected = index + 1 <= currentValue;
                            const defaultNumberBorder = `${borderW}px solid ${selected ? markColor : borderCol}`;
                            const cellBorder = useTypographyBorder
                                ? `${borderW}px solid ${borderCol}`
                                : ratingStyle === 'numbers'
                                  ? defaultNumberBorder
                                  : 'none';
                            const numberBg =
                                ratingStyle === 'numbers' && !useTypographyBorder
                                    ? selected
                                        ? `${markColor}20`
                                        : cellBg
                                    : cellBg;
                            const starEmojiBg = cellBg;

                            return (
                                <button
                                    key={`rating-${index}`}
                                    type="button"
                                    disabled={!isRuntime || disabled}
                                    onClick={() => {
                                        if (!isRuntime || disabled) return;
                                        onChange?.(index + 1);
                                    }}
                                    style={{
                                        fontFamily: styles.computed.fontFamily,
                                        fontSize: ratingStyle === 'emoji' ? `${Math.round(fontSz * 1.1)}px` : `${fontSz}px`,
                                        fontWeight: styles.computed.fontWeight,
                                        fontStyle: styles.computed.fontStyle,
                                        width: ratingStyle === 'numbers' ? numberSide : undefined,
                                        height: ratingStyle === 'numbers' ? numberSide : undefined,
                                        minWidth: ratingStyle === 'stars' || ratingStyle === 'emoji' ? starSize + 8 : undefined,
                                        minHeight: ratingStyle === 'stars' || ratingStyle === 'emoji' ? starSize + 8 : undefined,
                                        border: cellBorder,
                                        borderRadius: cellBorderRadius,
                                        background:
                                            ratingStyle === 'numbers'
                                                ? numberBg
                                                : starEmojiBg,
                                        color: markColor,
                                        cursor: !isRuntime || disabled ? 'default' : 'pointer',
                                        padding: ratingStyle === 'numbers' ? 0 : 4,
                                        display: 'inline-flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        boxSizing: 'border-box',
                                    }}
                                >
                                    {renderMark(index)}
                                </button>
                            );
                        })}
                    </div>
                    {(component.props.ratingLabels?.low || component.props.ratingLabels?.high) && (
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, color: '#6B7280' }}>
                            <span>{component.props.ratingLabels?.low || ''}</span>
                            <span>{component.props.ratingLabels?.high || ''}</span>
                        </div>
                    )}
                </div>
            );
        }

        // Checkbox/Radio: per-option extra text inputs + universal grouping (Option B).
        if (component.type === 'checkbox' || component.type === 'radio') {
            const options = Array.isArray(component.props.options) ? component.props.options : [];
            const direction = component.props.optionsDirection || 'vertical';

            const previewOptions =
                options.length > 0
                    ? options
                    : [
                        { label: 'Option 1', value: 'option_1' },
                        { label: 'Option 2', value: 'option_2' },
                        { label: 'Option 3', value: 'option_3' },
                      ];

            const containerWidthPx = inputWidthOverride
                ? inputWidthOverride
                : (component.props.width?.endsWith('px')
                    ? parseInt(component.props.width, 10)
                    : undefined);

            const boxWidthStyle: React.CSSProperties = {};
            if (containerWidthPx) {
                boxWidthStyle.width = `${containerWidthPx}px`;
                boxWidthStyle.maxWidth = `${containerWidthPx}px`;
            }
            if (isGridLayout) {
                boxWidthStyle.maxWidth = '100%';
                if (!containerWidthPx) {
                    boxWidthStyle.width = '100%';
                }
            }

            const boxStyle: React.CSSProperties = {
                fontFamily: styles.computed.fontFamily,
                fontSize: `${styles.computed.fontSize ?? 14}px`,
                fontWeight: styles.computed.fontWeight ?? 400,
                fontStyle: styles.computed.fontStyle,
                color: styles.computed.textColor || '#1F2937',
                backgroundColor: styles.computed.textBackgroundColor ?? styles.computed.backgroundColor ?? '#FFFFFF',
                border: `${styles.computed.borderWidth ?? 1}px solid ${styles.computed.borderColor || '#D1D5DB'}`,
                borderRadius: `${styles.computed.borderRadius ?? 6}px`,
                padding: `${styles.computed.paddingY ?? 8}px ${styles.computed.paddingX ?? 12}px`,
                minHeight: styles.computed.inputHeight ? `${styles.computed.inputHeight}px` : undefined,
                ...boxWidthStyle,
            };

            const controlStyle: React.CSSProperties = {
                width: 14,
                height: 14,
                flexShrink: 0,
                marginTop: 0,
            };

            const isRuntime = effectiveSurface === 'runtime';
            const valueObj = isRuntime && value && typeof value === 'object' ? (value as Record<string, unknown>) : null;

            const selectedValues: string[] =
                isRuntime
                    ? (Array.isArray(value) ? (value as string[]) : (Array.isArray(valueObj?.values) ? (valueObj.values as string[]) : []))
                    : [];
            const selectedRadio: string =
                isRuntime
                    ? (typeof value === 'string' ? (value as string) : (typeof valueObj?.value === 'string' ? (valueObj.value as string) : ''))
                    : '';
            const extraTextByValue: Record<string, string> =
                isRuntime && valueObj && valueObj.extraTextByValue && typeof valueObj.extraTextByValue === 'object'
                    ? (valueObj.extraTextByValue as Record<string, string>)
                    : {};

            const setSelection = (next: { values?: string[]; value?: string }) => {
                if (!isRuntime) return;
                if (component.type === 'checkbox') {
                    onChange?.({ values: next.values ?? [], extraTextByValue });
                } else {
                    onChange?.({ value: next.value ?? '', extraTextByValue });
                }
            };

            const setExtraText = (optValue: string, txt: string, baseSel?: { values?: string[]; value?: string }) => {
                if (!isRuntime) return;
                const nextMap = { ...extraTextByValue, [optValue]: txt };
                if (component.type === 'checkbox') {
                    onChange?.({ values: baseSel?.values ?? selectedValues, extraTextByValue: nextMap });
                } else {
                    onChange?.({ value: baseSel?.value ?? selectedRadio, extraTextByValue: nextMap });
                }
            };

            const grouped = (() => {
                const out: Array<{ group?: string; items: unknown[] }> = [];
                const seen = new Map<string, number>();
                for (const opt of previewOptions) {
                    const g = opt.group && String(opt.group).trim().length > 0 ? String(opt.group).trim() : '';
                    const idx = seen.get(g);
                    if (idx === undefined) {
                        seen.set(g, out.length);
                        out.push({ group: g || undefined, items: [opt] });
                    } else {
                        out[idx].items.push(opt);
                    }
                }
                return out;
            })();

            const listStyle: React.CSSProperties =
                direction === 'horizontal'
                    ? { display: 'flex', flexWrap: 'wrap', gap: '12px' }
                    : { display: 'flex', flexDirection: 'column', gap: '8px' };

            const extraMaxLength =
                (component.props.extraTextValidation?.maxLength ?? component.props.otherValidation?.maxLength) as
                    | number
                    | undefined;
            // Align all extra inputs to the longest option label width (Vegetarian sets the start, etc.).
            // Then ensure the input fills the remaining width (flush to the component border) without overflowing.
            const optionLabelWidths = previewOptions.map((opt: { label?: string; value?: string }) =>
                measureTextWidth(
                    String(opt?.label ?? opt?.value ?? ''),
                    styles.computed.fontFamily,
                    styles.computed.fontSize,
                    styles.computed.fontWeight
                )
            );
            const maxLabelTextW = optionLabelWidths.length ? Math.max(...optionLabelWidths) : 0;
            const controlW = 14;
            const controlGap = 8;
            const rowGap = 10;
            const labelColumnW = Math.round(controlW + controlGap + maxLabelTextW);

            // Available inner width of the box (roughly): containerWidthPx - padding*2.
            // If we can't compute it (no fixed width), we still keep alignment via labelColumnW.
            const paddingX = styles.computed.paddingX ?? 12;
            const innerW = containerWidthPx ? Math.max(0, containerWidthPx - paddingX * 2) : undefined;
            const minInputW = 160;
            const clampedLabelColW =
                innerW != null ? Math.min(labelColumnW, Math.max(0, innerW - rowGap - minInputW)) : labelColumnW;

            const showExtraTextLengthIndicator =
                effectiveSurface === 'canvas' && surfaceCaps.textLengthIndicator.enabled;

            return (
                <div className="relative" style={{ marginTop: (layout === 'horizontal' || layout === 'mixed') ? 0 : undefined }}>
                    <div style={boxStyle} aria-describedby={error && componentId ? `${componentId}-error` : undefined}>
                        {grouped.map((g, gi) => (
                            <div key={`g-${g.group ?? 'ungrouped'}-${gi}`} style={{ marginTop: gi === 0 ? 0 : 10 }}>
                                {g.group && (
                                    <div style={{ fontSize: 11, fontWeight: 600, opacity: 0.75, marginBottom: 8 }}>
                                        {g.group}
                                    </div>
                                )}
                                <div style={listStyle}>
                                    {g.items.slice(0, 50).map((opt: { label?: string; value?: string; disabled?: boolean; hasExtraText?: boolean; extraPlaceholder?: string }, idx: number) => {
                                        const optValue = String(opt.value ?? opt.label ?? idx);
                                        const optLabel = String(opt.label ?? opt.value ?? '');
                                        const optDisabled = Boolean(opt.disabled);
                                        const checked =
                                            component.type === 'checkbox'
                                                ? selectedValues.includes(optValue)
                                                : selectedRadio === optValue;
                                        const isDisabled = isRuntime ? (disabled || optDisabled) : false;

                                        const hasExtra = Boolean(opt.hasExtraText);
                                        const showExtra = hasExtra && (effectiveSurface !== 'runtime' || checked);
                                        const extraPlaceholder = String(opt.extraPlaceholder || 'Please specify…');
                                        const extraVal = extraTextByValue[optValue] ?? '';

                                        // For vertical option lists, align extra inputs based on the longest option label.
                                        // For horizontal lists, we keep the simpler wrap behavior.
                                        const useAlignedColumns = direction !== 'horizontal';

                                        return (
                                            <div
                                                key={`${optValue}-${idx}`}
                                                style={{
                                                    display: 'flex',
                                                    alignItems: 'center',
                                                    gap: rowGap,
                                                    // In horizontal layout, let items shrink to content; in vertical, take full width
                                                    width: direction === 'horizontal' ? 'auto' : '100%',
                                                    flexWrap: direction === 'horizontal' ? 'wrap' : 'nowrap',
                                                }}
                                            >
                                                <label
                                                    style={{
                                                        display: 'flex',
                                                        alignItems: 'center',
                                                        gap: controlGap,
                                                        opacity: isDisabled ? 0.5 : 1,
                                                        cursor: isRuntime ? (isDisabled ? 'not-allowed' : 'pointer') : 'default',
                                                        userSelect: 'none',
                                                        ...(useAlignedColumns
                                                            ? { width: clampedLabelColW, minWidth: clampedLabelColW, flexShrink: 0 }
                                                            : {}),
                                                    }}
                                                >
                                                    <input
                                                        ref={(idx === 0 ? (inputRef as React.RefObject<HTMLInputElement>) : undefined)}
                                                        tabIndex={tabIndex}
                                                        type={component.type === 'radio' ? 'radio' : 'checkbox'}
                                                        name={component.type === 'radio' ? (componentId || 'radio') : undefined}
                                                        disabled={isDisabled}
                                                        checked={checked}
                                                        readOnly={!isRuntime}
                                                        onChange={() => {
                                                            if (!isRuntime || isDisabled) return;
                                                            if (component.type === 'checkbox') {
                                                                const set = new Set(selectedValues);
                                                                if (set.has(optValue)) set.delete(optValue);
                                                                else set.add(optValue);
                                                                setSelection({ values: Array.from(set) });
                                                            } else {
                                                                setSelection({ value: optValue });
                                                            }
                                                        }}
                                                        aria-invalid={!!error}
                                                        aria-required={required}
                                                        style={{
                                                            ...controlStyle,
                                                            ...(idx === 0 && simulateFocus && (primaryColor || styles.computed.primaryColor) && {
                                                                outline: `2px solid ${primaryColor || styles.computed.primaryColor}`,
                                                                outlineOffset: '2px',
                                                                boxShadow: `0 0 0 2px ${(primaryColor || styles.computed.primaryColor)}33`,
                                                            }),
                                                        }}
                                                    />
                                                    <div style={{ lineHeight: '1.3', maxWidth: direction === 'horizontal' ? 240 : undefined }}>
                                                        {optLabel}
                                                    </div>
                                                </label>

                                                {showExtra && (
                                                    <TextLengthOverlay
                                                        enabled={Boolean(showExtraTextLengthIndicator && extraMaxLength)}
                                                        maxLength={extraMaxLength}
                                                        fontFamily={styles.computed.fontFamily}
                                                        fontSize={styles.computed.fontSize}
                                                        fontWeight={(styles.computed.fontWeight ?? 400) as FontWeightValue}
                                                        componentId={componentId ? `${componentId}:${optValue}:extra` : undefined}
                                                        borderWidth={styles.computed.borderWidth ?? 1}
                                                        paddingY={styles.computed.paddingY ?? 8}
                                                        componentType={'text'}
                                                        showBar={surfaceCaps.textLengthIndicator.showBar}
                                                        showLabel={surfaceCaps.textLengthIndicator.showLabel}
                                                        style={{
                                                            display: 'block',
                                                            flex: useAlignedColumns ? 1 : undefined,
                                                            minWidth: useAlignedColumns ? 0 : minInputW,
                                                            width: useAlignedColumns ? undefined : minInputW,
                                                        }}
                                                    >
                                                        <StyledInput
                                                            id={`${inputId}-${optValue}-extra`}
                                                            styles={{
                                                                ...inputStyle,
                                                                width: useAlignedColumns ? '100%' : inputStyle.width,
                                                                minWidth: useAlignedColumns ? '0' : undefined,
                                                                maxWidth: useAlignedColumns ? '100%' : undefined,
                                                            }}
                                                            primaryColor={primaryColor || styles.computed.primaryColor}
                                                            disabled={effectiveSurface === 'runtime' ? disabled : false}
                                                            error={error}
                                                            componentId={componentId}
                                                            type="text"
                                                            placeholder={extraPlaceholder}
                                                            value={effectiveSurface === 'runtime' ? extraVal : ''}
                                                            maxLength={extraMaxLength}
                                                            onChange={(e) => {
                                                                if (!isRuntime) return;
                                                                // Ensure selection is set if the user types.
                                                                if (component.type === 'radio') {
                                                                    const baseSel = { value: optValue };
                                                                    setSelection(baseSel);
                                                                    setExtraText(optValue, e.target.value, baseSel);
                                                                } else {
                                                                    const set = new Set(selectedValues);
                                                                    set.add(optValue);
                                                                    const baseSel = { values: Array.from(set) };
                                                                    setSelection(baseSel);
                                                                    setExtraText(optValue, e.target.value, baseSel);
                                                                }
                                                            }}
                                                            tabIndex={tabIndex != null ? tabIndex + 1 : undefined}
                                                            required={false}
                                                        />
                                                    </TextLengthOverlay>
                                                )}
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            );
        }

        if (component.type === 'textarea') {
            // Textarea height source-of-truth:
            // - Render height comes from computed `inputHeight` (global + styleOverrides, scaled by componentScale).
            // - Older/legacy data may have `props.height` (documented as px). We honor it ONLY when
            //   there is no explicit styleOverrides.inputHeight, to avoid conflicting sources.
            const scaleFactor = Math.max(0.5, Math.min(2, (component.props.componentScale ?? 100) / 100));
            const legacyHeightPx =
                component.props.styleOverrides?.inputHeight === undefined && component.props.height !== undefined
                    ? Math.round(component.props.height * scaleFactor)
                    : undefined;
            const textareaInputStyle: React.CSSProperties = {
                ...inputStyle,
                ...(legacyHeightPx !== undefined ? { height: `${legacyHeightPx}px` } : {}),
            };
            const valueStr = (value as string) ?? '';
            const maxLength = component.props.validation?.maxLength;
            const showCharacterCount = Boolean(
                effectiveSurface === 'runtime' && component.props.showCharacterCount && maxLength !== undefined
            );
            const resizeMode = component.props.resizeMode ?? 'vertical';
            const shouldAutoGrow = resizeMode === 'auto-grow';
            const textareaElement = (
                <div style={{ display: 'flex', flexDirection: 'column', gap: 4, width: '100%' }}>
                    <StyledTextarea
                        ref={inputRef as React.RefObject<HTMLTextAreaElement>}
                        id={inputId}
                        styles={textareaInputStyle}
                        primaryColor={primaryColor || styles.computed.primaryColor}
                        simulateFocus={simulateFocus}
                        disabled={disabled}
                        error={error}
                        componentId={componentId}
                        placeholder={placeholder}
                        value={valueStr}
                        onChange={e => onChange?.(e.target.value)}
                        maxLength={maxLength}
                        rows={4}
                        tabIndex={tabIndex}
                        required={required}
                        autoGrow={shouldAutoGrow}
                        resizeMode={resizeMode}
                    />
                    {showCharacterCount && (
                        <div
                            style={{
                                ...styles.helpTextStyle,
                                color: styles.helpTextStyle?.color ?? '#6B7280',
                                alignSelf: 'flex-end',
                            }}
                        >
                            {valueStr.length} / {maxLength} characters
                        </div>
                    )}
                </div>
            );
            return textareaElement;
        }

        if (component.type === 'date' && component.props.pickerStyle === 'dropdown' && (component.props.dateType ?? 'date') === 'date') {
            const dateValue = typeof value === 'string' ? value : '';
            const valueParts = value && typeof value === 'object'
                ? (value as { year?: string; month?: string; day?: string })
                : {};
            const [yearFromString, monthFromString, dayFromString] = dateValue.split('-');
            const yearPart = yearFromString || valueParts.year || '';
            const monthPart = monthFromString || valueParts.month || '';
            const dayPart = dayFromString || valueParts.day || '';
            const dateParts = component.props.dateParts ?? { year: true, month: true, day: true };
            const showYear = dateParts.year !== false;
            const showMonth = dateParts.month !== false;
            const showDay = dateParts.day !== false;
            const partOrder = getDatePartOrder(component.props.dateFormat);
            const validation = component.props.validation ?? {};

            const yearOptions = (() => {
                const currentYear = new Date().getFullYear();
                const start = currentYear - 100;
                const end = currentYear + 20;
                return Array.from({ length: end - start + 1 }, (_, idx) => {
                    const year = start + idx;
                    return { label: String(year), value: String(year) };
                });
            })();
            const monthOptions = Array.from({ length: 12 }, (_, idx) => {
                const month = String(idx + 1).padStart(2, '0');
                return { label: String(idx + 1), value: month };
            });
            const dayOptions = Array.from({ length: 31 }, (_, idx) => {
                const day = String(idx + 1).padStart(2, '0');
                return { label: String(idx + 1), value: day };
            });

            const today = (() => {
                const d = new Date();
                d.setHours(0, 0, 0, 0);
                return d;
            })();

            const parseRuleDate = (rule?: string): Date | undefined => {
                if (!rule) return undefined;
                if (rule === 'today') return new Date(today);
                const parsed = new Date(rule);
                if (Number.isNaN(parsed.getTime())) return undefined;
                parsed.setHours(0, 0, 0, 0);
                return parsed;
            };

            const minRule = parseRuleDate(validation.minDate);
            const maxRule = parseRuleDate(validation.maxDate);
            const minFromFuture = validation.futureOnly ? (() => {
                const d = new Date(today);
                d.setDate(d.getDate() + 1);
                return d;
            })() : undefined;
            const maxFromPast = validation.pastOnly ? (() => {
                const d = new Date(today);
                d.setDate(d.getDate() - 1);
                return d;
            })() : undefined;

            const minAllowed = [minRule, minFromFuture].filter(Boolean).sort((a, b) => (a!.getTime() - b!.getTime())).pop();
            const maxAllowed = [maxRule, maxFromPast].filter(Boolean).sort((a, b) => (a!.getTime() - b!.getTime()))[0];

            const isDateAllowed = (date: Date) => {
                if (minAllowed && date < minAllowed) return false;
                if (maxAllowed && date > maxAllowed) return false;
                if (validation.weekdaysOnly) {
                    const dayOfWeek = date.getDay();
                    if (dayOfWeek === 0 || dayOfWeek === 6) return false;
                }
                return true;
            };

            const daysInMonth = (year: number, month: number) => new Date(year, month, 0).getDate();

            const selectedYear = yearPart ? parseInt(yearPart, 10) : undefined;
            const selectedMonth = monthPart ? parseInt(monthPart, 10) : undefined;
            const selectedDay = dayPart ? parseInt(dayPart, 10) : undefined;

            const hasValidDateForYear = (year: number) => {
                if (showMonth && selectedMonth && showDay && selectedDay) {
                    if (selectedDay > daysInMonth(year, selectedMonth)) return false;
                    return isDateAllowed(new Date(year, selectedMonth - 1, selectedDay));
                }

                if (showMonth && selectedMonth) {
                    const maxDay = daysInMonth(year, selectedMonth);
                    for (let d = 1; d <= maxDay; d += 1) {
                        if (isDateAllowed(new Date(year, selectedMonth - 1, d))) return true;
                    }
                    return false;
                }

                if (showDay && selectedDay) {
                    for (let m = 1; m <= 12; m += 1) {
                        if (selectedDay > daysInMonth(year, m)) continue;
                        if (isDateAllowed(new Date(year, m - 1, selectedDay))) return true;
                    }
                    return false;
                }

                if (minAllowed || maxAllowed) {
                    const yearStart = new Date(year, 0, 1);
                    const yearEnd = new Date(year, 11, 31);
                    if (minAllowed && yearEnd < minAllowed) return false;
                    if (maxAllowed && yearStart > maxAllowed) return false;
                }

                return true;
            };

            const yearOptionsWithDisabled = yearOptions.map(option => {
                const year = parseInt(option.value, 10);
                return { ...option, disabled: showYear ? !hasValidDateForYear(year) : false };
            });

            const candidateYears = showYear
                ? yearOptionsWithDisabled.filter(option => !option.disabled).map(option => parseInt(option.value, 10))
                : (selectedYear ? [selectedYear] : yearOptions.map(option => parseInt(option.value, 10)));

            const hasValidDateForMonth = (month: number) => {
                const yearsToCheck = selectedYear ? [selectedYear] : candidateYears;
                for (const year of yearsToCheck) {
                    const maxDay = daysInMonth(year, month);
                    if (showDay && selectedDay) {
                        if (selectedDay > maxDay) continue;
                        if (isDateAllowed(new Date(year, month - 1, selectedDay))) return true;
                        continue;
                    }
                    for (let d = 1; d <= maxDay; d += 1) {
                        if (isDateAllowed(new Date(year, month - 1, d))) return true;
                    }
                }
                return false;
            };

            const monthOptionsWithDisabled = monthOptions.map(option => {
                const month = parseInt(option.value, 10);
                return { ...option, disabled: showMonth ? !hasValidDateForMonth(month) : false };
            });

            const hasValidDateForDay = (day: number) => {
                const monthsToCheck = selectedMonth ? [selectedMonth] : (showMonth ? monthOptions.map(opt => parseInt(opt.value, 10)) : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]);
                const yearsToCheck = selectedYear ? [selectedYear] : candidateYears;
                for (const year of yearsToCheck) {
                    for (const month of monthsToCheck) {
                        if (day > daysInMonth(year, month)) continue;
                        if (isDateAllowed(new Date(year, month - 1, day))) return true;
                    }
                }
                return false;
            };

            const dayOptionsWithDisabled = dayOptions.map(option => {
                const day = parseInt(option.value, 10);
                return { ...option, disabled: showDay ? !hasValidDateForDay(day) : false };
            });

            const buildDateValue = (parts: { year?: string; month?: string; day?: string }) => {
                if (!showYear) return '';
                const year = parts.year ?? '';
                if (!year) return '';
                const month = showMonth ? (parts.month ?? '') : '01';
                const day = showDay ? (parts.day ?? '') : '01';
                if ((showMonth && !month) || (showDay && !day)) return '';
                return `${year}-${month}-${day}`;
            };

            const updatePart = (part: 'year' | 'month' | 'day', nextValue: string) => {
                const next = {
                    year: part === 'year' ? nextValue : (yearPart || ''),
                    month: part === 'month' ? nextValue : (monthPart || ''),
                    day: part === 'day' ? nextValue : (dayPart || ''),
                };
                const nextDate = buildDateValue(next);
                onChange?.(nextDate || next);
            };

            const orderedParts = partOrder.filter((part) => {
                if (part === 'day') return showDay;
                if (part === 'month') return showMonth;
                return showYear;
            });

            const renderPart = (part: 'day' | 'month' | 'year') => {
                if (part === 'day') {
                    return (
                        <StyledSelect
                            key="date-part-day"
                            id={`${inputId}-day`}
                            styles={{ ...inputStyle, flex: 1, minWidth: 0 }}
                            primaryColor={primaryColor || styles.computed.primaryColor}
                            simulateFocus={simulateFocus}
                            disabled={disabled}
                            error={error}
                            componentId={componentId}
                            options={dayOptionsWithDisabled}
                            placeholder="Day"
                            value={dayPart || ''}
                            onChange={e => updatePart('day', e.target.value)}
                            tabIndex={tabIndex}
                            required={required}
                        />
                    );
                }

                if (part === 'month') {
                    return (
                        <StyledSelect
                            key="date-part-month"
                            id={`${inputId}-month`}
                            styles={{ ...inputStyle, flex: 1, minWidth: 0 }}
                            primaryColor={primaryColor || styles.computed.primaryColor}
                            simulateFocus={simulateFocus}
                            disabled={disabled}
                            error={error}
                            componentId={componentId}
                            options={monthOptionsWithDisabled}
                            placeholder="Month"
                            value={monthPart || ''}
                            onChange={e => updatePart('month', e.target.value)}
                            tabIndex={tabIndex}
                            required={required}
                        />
                    );
                }

                return (
                    <StyledSelect
                        key="date-part-year"
                        id={`${inputId}-year`}
                        styles={{ ...inputStyle, flex: 1.2, minWidth: 0 }}
                        primaryColor={primaryColor || styles.computed.primaryColor}
                        simulateFocus={simulateFocus}
                        disabled={disabled}
                        error={error}
                        componentId={componentId}
                        options={yearOptionsWithDisabled}
                        placeholder="Year"
                        value={yearPart || ''}
                        onChange={e => updatePart('year', e.target.value)}
                        tabIndex={tabIndex}
                        required={required}
                    />
                );
            };

            return (
                <div style={{ display: 'flex', gap: 8, width: '100%' }}>
                    {orderedParts.map(renderPart)}
                </div>
            );
        }
        
        if (component.type === 'dropdown') {
            const options = component.props.options || [];
            
            // Calculate width based on longest option (or default 200px if no options)
            let calculatedWidth: number | undefined;
            let longestLabel = '';
            let longestValue: string | undefined;
            if (options.length > 0) {
                // Find longest option label (use label if available, otherwise value)
                let best = options[0];
                for (const opt of options) {
                    const a = String(opt?.label ?? opt?.value ?? '');
                    const b = String(best?.label ?? best?.value ?? '');
                    if (a.length > b.length) best = opt;
                }
                longestLabel = String(best?.label ?? best?.value ?? '');
                longestValue = String(best?.value ?? best?.label ?? '');
                
                // Measure actual width of longest option text using Canvas API
                // Use Input category font properties (from styles.computed which includes component overrides)
                const fontFamily = styles.computed.fontFamily;
                const fontSize = styles.computed.fontSize;
                const fontWeight = styles.computed.fontWeight;
                
                // Measure the actual text width using Canvas measureText API
                const textWidth = measureTextWidth(
                    longestLabel,
                    fontFamily,
                    fontSize,
                    fontWeight
                );
                
                // Add padding, border, and space for dropdown arrow (~40px)
                const paddingX = styles.computed.paddingX ?? 12;
                const borderWidth = styles.computed.borderWidth ?? 1;
                calculatedWidth = textWidth + (paddingX * 2) + (borderWidth * 2) + 40; // +40 for arrow
                
                devLogger.debug('canvas.dropdown.width.calculated', {
                    componentId: componentId || 'unknown',
                    optionsCount: options.length,
                    longestLabel,
                    longestLabelLength: longestLabel.length,
                    // Font properties used for calculation (Input category, includes component overrides)
                    fontFamily,
                    fontSize,
                    fontWeight,
                    textWidth, // Actual measured width
                    calculatedWidth,
                    paddingX,
                    borderWidth,
                    calculationBreakdown: {
                        textWidth, // Actual measured width from Canvas API
                        padding: paddingX * 2,
                        border: borderWidth * 2,
                        arrowSpace: 40,
                        total: calculatedWidth
                    },
                    measurementMethod: 'canvas.measureText' // Indicates we're using actual measurement
                });
            } else {
                // Default width when no options
                calculatedWidth = 200;
                devLogger.debug('canvas.dropdown.width.default', {
                    componentId: componentId || 'unknown',
                    calculatedWidth,
                    reason: 'no options available',
                });
            }
            
            // Use inputWidthOverride if explicitly set, otherwise use calculated width
            // For dropdown, we want calculated width to be the default
            const finalWidth = inputWidthOverride || calculatedWidth;

            // Enforce minimum widths:
            // - dropdown control min: 10 characters (plus chrome/arrow)
            // - extra input min: 10 characters
            const fontFamily = styles.computed.fontFamily;
            const fontSize = styles.computed.fontSize;
            const fontWeight = styles.computed.fontWeight;
            const paddingX = styles.computed.paddingX ?? 12;
            const borderWidthPx = styles.computed.borderWidth ?? 1;
            const minExtraWidthPx =
                measureTextWidth('W'.repeat(10), fontFamily, fontSize, fontWeight) + (paddingX * 2) + (borderWidthPx * 2);
            const minDropdownWidthPx =
                Math.max(
                    Number(calculatedWidth ?? 0),
                    measureTextWidth('W'.repeat(10), fontFamily, fontSize, fontWeight) + (paddingX * 2) + (borderWidthPx * 2) + 40
                );
            // If the overall component has an explicit width, use it so the extra input can "fill to the border".
            const componentWidthPx =
                component.props.width?.endsWith('px') ? parseInt(component.props.width, 10) : undefined;

            const normalizedOptions = options.map((opt: Record<string, unknown>) => ({
                label: String(opt.label ?? opt.value ?? ''),
                value: String(opt.value ?? opt.label ?? ''),
                disabled: Boolean(opt.disabled),
                group: opt.group ? String(opt.group) : undefined,
                hasExtraText: Boolean(opt.hasExtraText),
                extraPlaceholder: opt.extraPlaceholder ? String(opt.extraPlaceholder) : undefined,
            }));

            const anyExtra = normalizedOptions.some(o => o.hasExtraText);
            const extraMaxLength =
                (component.props.extraTextValidation?.maxLength ?? component.props.otherValidation?.maxLength) as
                    | number
                    | undefined;
            const gap = 8;

            // Clamp dropdown width so:
            // - It never shrinks below the anchored min (longest option / 10 chars)
            // - If extra input exists and component width is fixed, the dropdown won't steal the extra input's minimum.
            const maxAllowedDropdownWidthPx =
                anyExtra && componentWidthPx
                    ? Math.max(minDropdownWidthPx, componentWidthPx - gap - minExtraWidthPx)
                    : undefined;
            const dropdownWidthPx = Math.max(
                minDropdownWidthPx,
                Math.min(
                    Number(finalWidth ?? minDropdownWidthPx),
                    maxAllowedDropdownWidthPx ?? Number.POSITIVE_INFINITY
                )
            );
            const dropdownStyle: React.CSSProperties = {
                ...inputStyle,
                // Ensure StyledSelect receives full border/background info.
                // (If borderColor is missing, browsers can fall back to a default black border.)
                borderColor: (inputStyle.borderColor as string | undefined) ?? (styles.computed.borderColor || '#D1D5DB'),
                borderWidth: (inputStyle.borderWidth as string | undefined) ?? `${styles.computed.borderWidth ?? 1}px`,
                borderStyle: (inputStyle.borderStyle as string | undefined) ?? 'solid',
                borderRadius: (inputStyle.borderRadius as string | undefined) ?? `${styles.computed.borderRadius ?? 6}px`,
                backgroundColor: (styles.computed.textBackgroundColor ?? styles.computed.backgroundColor ?? '#FFFFFF') as string,
                color: (styles.computed.textColor || (styles.computed as Record<string, unknown>).fontColor || '#1F2937') as string,
                width: `${dropdownWidthPx}px`,
                minWidth: `${dropdownWidthPx}px`,
            };
            const showExtraTextLengthIndicator =
                effectiveSurface === 'canvas' && surfaceCaps.textLengthIndicator.enabled;

            // Non-runtime surfaces: render a real <select> (enabled styles) so it matches runtime visuals.
            if (effectiveSurface !== 'runtime') {
                const displayMode = surfaceCaps.dropdown.displayMode;
                const valueForSurface =
                    displayMode === 'longest-option'
                        ? (options.length > 0 ? (longestValue ?? '') : '')
                        : '';

                const placeholderText = String(component.props.emptyPlaceholder || component.props.placeholder || 'Select...');

                const samplePlaceholder = normalizedOptions.find(o => o.hasExtraText)?.extraPlaceholder || 'Please specify…';

                return (
                    <div
                        className="relative"
                        style={{
                            marginTop: (layout === 'horizontal' || layout === 'mixed') ? 0 : undefined,
                            width: componentWidthPx ? `${componentWidthPx}px` : undefined,
                        }}
                    >
                        <div style={{ display: 'flex', gap, alignItems: 'center', width: '100%' }}>
                            <StyledSelect
                                ref={inputRef as React.RefObject<HTMLSelectElement>}
                                id={inputId}
                                styles={dropdownStyle}
                                primaryColor={primaryColor || styles.computed.primaryColor}
                                simulateFocus={simulateFocus}
                                disabled={false}
                                error={error}
                                componentId={componentId}
                                value={valueForSurface}
                                onChange={() => undefined}
                                required={required}
                                placeholder={placeholderText}
                                options={normalizedOptions}
                                tabIndex={tabIndex}
                            />
                            {anyExtra && (
                                <TextLengthOverlay
                                    enabled={Boolean(showExtraTextLengthIndicator && extraMaxLength)}
                                    maxLength={extraMaxLength}
                                    fontFamily={styles.computed.fontFamily}
                                    fontSize={styles.computed.fontSize}
                                    fontWeight={(styles.computed.fontWeight ?? 400) as FontWeightValue}
                                    componentId={componentId ? `${componentId}:dropdownExtra` : undefined}
                                    borderWidth={styles.computed.borderWidth ?? 1}
                                    paddingY={styles.computed.paddingY ?? 8}
                                    componentType={'text'}
                                    showBar={surfaceCaps.textLengthIndicator.showBar}
                                    showLabel={surfaceCaps.textLengthIndicator.showLabel}
                                    style={{ display: 'block', flex: 1, minWidth: 0 }}
                                >
                                    <StyledInput
                                        id={`${inputId}-extra`}
                                        styles={{
                                            ...inputStyle,
                                            width: '100%',
                                            minWidth: '0',
                                        }}
                                        primaryColor={primaryColor || styles.computed.primaryColor}
                                        disabled={false}
                                        error={error}
                                        componentId={componentId}
                                        type="text"
                                        placeholder={String(samplePlaceholder)}
                                        value={''}
                                        maxLength={extraMaxLength}
                                        onChange={() => undefined}
                                        tabIndex={-1}
                                        required={false}
                                    />
                                </TextLengthOverlay>
                            )}
                        </div>
                    </div>
                );
            }
            
            // Runtime mode: render actual select with placeholder + options (same API as other surfaces)
            const placeholderText = String(component.props.emptyPlaceholder || component.props.placeholder || 'Select...');
            const current = (value as Record<string, unknown>) ?? {};
            const selectedValue = typeof current === 'object' && current && current.value !== undefined
                ? String(current.value ?? '')
                : String(current ?? '');
            const extraTextByValue = typeof current === 'object' && current && current.extraTextByValue && typeof current.extraTextByValue === 'object'
                ? (current.extraTextByValue as Record<string, string>)
                : {};

            const selectedOpt = normalizedOptions.find(o => String(o.value) === selectedValue);
            const selectedNeedsExtra = !!selectedOpt?.hasExtraText;
            const selectedExtraPlaceholder = selectedOpt?.extraPlaceholder || 'Please specify…';
            const selectedExtraText = extraTextByValue[selectedValue] ?? '';

            return (
                <div
                    style={{
                        display: 'flex',
                        gap,
                        alignItems: 'center',
                        width: componentWidthPx ? `${componentWidthPx}px` : undefined,
                    }}
                >
                    <StyledSelect
                        ref={inputRef as React.RefObject<HTMLSelectElement>}
                        id={inputId}
                        styles={dropdownStyle}
                        primaryColor={primaryColor || styles.computed.primaryColor}
                        simulateFocus={simulateFocus}
                        disabled={disabled}
                        error={error}
                        componentId={componentId}
                        value={selectedValue}
                        onChange={e => {
                            const nextVal = e.target.value;
                            onChange?.({ value: nextVal, extraTextByValue });
                        }}
                        required={required}
                        placeholder={placeholderText}
                        options={normalizedOptions}
                        tabIndex={tabIndex}
                    />
                    {selectedNeedsExtra && (
                        <TextLengthOverlay
                            enabled={Boolean(showExtraTextLengthIndicator && extraMaxLength)}
                            maxLength={extraMaxLength}
                            fontFamily={styles.computed.fontFamily}
                            fontSize={styles.computed.fontSize}
                            fontWeight={(styles.computed.fontWeight ?? 400) as FontWeightValue}
                            componentId={componentId ? `${componentId}:dropdownExtraSelected` : undefined}
                            borderWidth={styles.computed.borderWidth ?? 1}
                            paddingY={styles.computed.paddingY ?? 8}
                            componentType={'text'}
                            showBar={surfaceCaps.textLengthIndicator.showBar}
                            showLabel={surfaceCaps.textLengthIndicator.showLabel}
                            style={{ display: 'block', flex: 1, minWidth: 0 }}
                        >
                            <StyledInput
                                id={`${inputId}-extra`}
                                styles={{
                                    ...inputStyle,
                                    width: '100%',
                                    minWidth: '0',
                                }}
                                primaryColor={primaryColor || styles.computed.primaryColor}
                                disabled={disabled}
                                error={error}
                                componentId={componentId}
                                type="text"
                                placeholder={String(selectedExtraPlaceholder)}
                                value={selectedExtraText}
                                maxLength={extraMaxLength}
                                onChange={e => {
                                    const txt = e.target.value;
                                    onChange?.({
                                        value: selectedValue,
                                        extraTextByValue: { ...extraTextByValue, [selectedValue]: txt },
                                    });
                                }}
                                tabIndex={tabIndex != null ? tabIndex + 1 : undefined}
                                required={false}
                            />
                        </TextLengthOverlay>
                    )}
                </div>
            );
        }
        
        const inputElement = (
            <StyledInput
                ref={inputRef as React.RefObject<HTMLInputElement>}
                id={inputId}
                styles={inputStyle}
                primaryColor={primaryColor || styles.computed.primaryColor}
                simulateFocus={simulateFocus}
                disabled={disabled}
                error={error}
                componentId={componentId}
                type={inputType}
                placeholder={placeholder}
                value={(value as string) ?? ''}
                onChange={e => onChange?.(e.target.value)}
                maxLength={maxLength}
                min={dateBounds?.min}
                max={dateBounds?.max}
                tabIndex={tabIndex}
                required={required}
            />
        );
        
        // Note: TextLengthIndicator is now applied via ObjectFeatureHost (object-level features),
        // and via TextLengthOverlay for selection extra-text sub-controls.
        return inputElement;
    };
}

/**
 * Create a standard validation renderer with ValidationArea.
 * In builder mode, shows placeholder message so SmartBorder accounts for full validation space.
 */
export function createValidationRenderer(): ObjectRenderer {
    return ({ component, styles, error, validationErrors, allFormErrors, componentId, builderMode, helpWidthOverride, inRowGroup }) => {
        // Get maxLength to generate realistic placeholder message
        const maxLength = component.props.validation?.maxLength;
        const placeholderMessage = maxLength
            ? `We only allow a max of ${maxLength} Characters`
            : 'Validation error message';

        // Use the builderMode prop passed from renderObjectGroup
        // Fallback to heuristic only if builderMode is not explicitly set
        const isBuilderMode = builderMode ?? (!error && !validationErrors && !allFormErrors);

        // Apply width override if set (from E/W resize)
        // Help text wraps when width is constrained
        const helpTextStyle: React.CSSProperties = {
            ...styles.helpTextStyle,
            ...(helpWidthOverride && {
                maxWidth: helpWidthOverride,
                // Allow wrapping when width is constrained
                whiteSpace: 'normal',
                wordWrap: 'break-word',
            }),
            // When validation is placed in the same horizontal row as label/input,
            // vertical spacing must be controlled by the row's alignItems (rowAlignment),
            // not by a fixed top margin on the validation object.
            ...(inRowGroup ? { marginTop: 0 } : {}),
        };

        // ValidationArea always renders (with minHeight: 18) even when there's no error
        // In builder mode, shows placeholder so SmartBorder accounts for full validation space
        return (
            <ValidationArea
                error={error}
                helpTextStyle={helpTextStyle}
                componentId={componentId || 'field'}
                builderMode={isBuilderMode}
                placeholderMessage={placeholderMessage}
            />
        );
    };
}

/**
 * Create a standard action/button renderer.
 */
export function createActionRenderer(): ObjectRenderer {
    return ({ component, styles, buttonText, onClick, disabled, isLoading, componentId, surface, builderMode, formValidationContext, actionWidthOverride, actionHeightOverride }) => {
        const effectiveSurface: ComponentSurface = surface ?? (builderMode ? 'canvas' : 'runtime');
        const caps = getComponentSurfaceCapabilities(component.type, effectiveSurface);

        // Default action renderer for non-submit-button components
        if (component.type !== 'submit-button') {
            const text = buttonText || component.props.buttonText || 'Submit';
            const buttonId = componentId ? `${componentId}-button` : undefined;

            return (
                <button
                    id={buttonId}
                    type="button"
                    onClick={onClick}
                    disabled={disabled || isLoading}
                    style={{
                        ...styles.inputStyle,
                        cursor: disabled || isLoading ? 'not-allowed' : 'pointer',
                        opacity: disabled || isLoading ? 0.6 : 1,
                    }}
                >
                    {isLoading && <span>Loading...</span>}
                    {!isLoading && text}
                </button>
            );
        }

        // Submit button rendering (surface-driven)
        const text = String(component.props.buttonText || 'Submit');
        const buttonId = componentId ? `${componentId}-button` : undefined;

        const showIcon = caps.submitButton.showIcon && component.props.showIcon !== false;
        const showSpinnerOnButton = isLoading && caps.submitButton.showStatus === 'while-submitting';
        const Icon = showSpinnerOnButton ? Loader2 : Send;

        // Non-runtime surfaces should never be interactive (parity: WYSIWYG but no submission)
        const effectiveDisabled = effectiveSurface !== 'runtime' ? true : Boolean(disabled);

        const align: NonNullable<ComponentProps['buttonAlign']> = component.props.buttonAlign ?? 'left';
        const explicitButtonWidth = component.props.buttonWidth;
        
        // Determine button width with clear priority chain:
        // 1. Percentage width → always use 100% (fill container)
        // 2. actionWidthOverride (preview or committed) → use pixel value
        // 3. buttonWidth === 'full' → use 100%
        // 4. component.props.width (pixel) → button fills container (100%)
        // 5. Default → 'auto' (content-sized)
        let buttonWidthValue: string | number = 'auto';
        
        // Use preview override if provided (during resize preview), otherwise use props
        const effectiveActionWidthOverride = actionWidthOverride !== undefined 
            ? actionWidthOverride 
            : component.props.actionWidthOverride;
        const isPercentageWidth = component.props.width?.endsWith('%');
        const effectiveActionHeightOverride =
            actionHeightOverride !== undefined ? actionHeightOverride : component.props.height;
        
        if (isPercentageWidth) {
            // Percentage widths: button always fills container
            buttonWidthValue = '100%';
        } else if (effectiveActionWidthOverride !== undefined) {
            // Explicit pixel override from preset calculations or resize
            buttonWidthValue = effectiveActionWidthOverride;
        } else if (explicitButtonWidth === 'full') {
            // Button Settings "Full Width" option
            buttonWidthValue = '100%';
        } else if (component.props.width) {
            // Explicit width set (px): button fills container to match user intent
            buttonWidthValue = '100%';
        }
        // else: 'auto' (content-sized)
        
        // Debug logging for button width calculation
        if (componentId && builderMode) {
            devLogger.info('button.width.calculated', {
                componentId,
                PROPS: {
                    actionWidthOverrideProp: actionWidthOverride, // Preview override from renderer prop
                    actionWidthOverrideFromProps: component.props.actionWidthOverride, // Committed value from component props
                    buttonWidth: explicitButtonWidth,
                    componentWidth: component.props.width,
                },
                CALCULATION: {
                    isPercentageWidth,
                    effectiveActionWidthOverride,
                    buttonWidthValue,
                    priority: isPercentageWidth ? '1-percentage-width (100%)' :
                             effectiveActionWidthOverride !== undefined ? '2-actionWidthOverride' : 
                             explicitButtonWidth === 'full' ? '3-buttonWidth:full' :
                             component.props.width ? '4-componentWidth' : '5-auto',
                },
                RESULT: {
                    finalWidth: buttonWidthValue,
                    type: typeof buttonWidthValue,
                },
            });
        }
        
        const contentAlignment =
            align === 'center' ? 'center' : align === 'right' ? 'flex-end' : 'flex-start';

        const alignmentClass =
            align === 'center' ? 'justify-center' : align === 'right' ? 'justify-end' : 'justify-start';

        const buttonStyle: React.CSSProperties = {
            backgroundColor: styles.computed.labelColor || styles.computed.primaryColor || '#0055FF',
            color: '#FFFFFF',
            fontFamily: styles.computed.labelFontFamily || styles.computed.fontFamily || 'Inter',
            fontSize: `${styles.computed.labelFontSize || styles.computed.fontSize || 14}px`,
            fontWeight: styles.computed.labelFontWeight || styles.computed.fontWeight || 500,
            borderRadius: `${styles.computed.borderRadius || 6}px`,
            border:
                styles.computed.textBorderWidth && styles.computed.textBorderColor
                    ? `${styles.computed.textBorderWidth}px solid ${styles.computed.textBorderColor}`
                    : 'none',
            padding: `${styles.computed.paddingY || 10}px ${styles.computed.paddingX || 24}px`,
            cursor: effectiveDisabled ? 'not-allowed' : 'pointer',
            opacity: effectiveDisabled ? 0.6 : 1,
            transition: 'all 0.2s',
            display: 'inline-flex',
            alignItems: 'center',
            gap: 8,
            width: typeof buttonWidthValue === 'number' ? `${buttonWidthValue}px` : buttonWidthValue,
            ...(effectiveActionHeightOverride !== undefined
                ? {
                      height: `${effectiveActionHeightOverride}px`,
                      boxSizing: 'border-box',
                  }
                : {}),
            justifyContent: (buttonWidthValue === '100%' || typeof buttonWidthValue === 'number') ? contentAlignment : undefined,
            textAlign: (buttonWidthValue === '100%' || typeof buttonWidthValue === 'number') ? align : undefined,
        };

        // Display first validation error if present (runtime only)
        const showValidationError = effectiveSurface === 'runtime' && formValidationContext?.firstError;

        return (
            <div style={{ width: '100%' }}>
                <div className={`flex ${alignmentClass}`} style={{ width: '100%' }}>
                    <button
                        id={buttonId}
                        type="button"
                        onClick={effectiveSurface === 'runtime' ? onClick : undefined}
                        disabled={effectiveDisabled}
                        style={buttonStyle}
                    >
                        {showIcon ? (
                            <Icon
                                size={16}
                                className={showSpinnerOnButton ? 'animate-spin' : undefined}
                                color="#FFFFFF"
                            />
                        ) : null}
                        {text}
                    </button>
                </div>
                {showValidationError && (
                    <div 
                        style={{
                            marginTop: 8,
                            fontSize: styles.computed.helpTextFontSize || 12,
                            color: styles.computed.helpTextColor || '#DC2626',
                            fontFamily: styles.computed.helpTextFontFamily || styles.computed.fontFamily || 'Inter',
                        }}
                    >
                        {formValidationContext.firstError}
                    </div>
                )}
            </div>
        );
    };
}

/**
 * Create a standard status renderer (loading, etc.).
 */
export function createStatusRenderer(): ObjectRenderer {
    return ({ component, isLoading, surface, builderMode }) => {
        const effectiveSurface: ComponentSurface = surface ?? (builderMode ? 'canvas' : 'runtime');

        if (!isLoading) return null;

        // Submit button status object is surface-driven
        if (component.type === 'submit-button') {
            const caps = getComponentSurfaceCapabilities(component.type, effectiveSurface);
            if (caps.submitButton.showStatus === 'never') return null;
            return <Loader2 className="animate-spin" size={16} style={{ marginTop: 8 }} />;
        }

        // Generic status renderer
        return (
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <div
                    className="animate-spin"
                    style={{
                        width: '16px',
                        height: '16px',
                        border: '2px solid currentColor',
                        borderTopColor: 'transparent',
                        borderRadius: '50%',
                    }}
                />
                <span>Loading...</span>
            </div>
        );
    };
}

/**
 * Create a divider/separator renderer.
 * Renders a horizontal line with configurable thickness and color from styles.
 */
export function createDividerRenderer(): ObjectRenderer {
    return ({ component, styles, componentId, builderMode, inputWidthOverride }) => {
        // Divider uses Divider & Lines settings (GlobalStyles / styleOverrides):
        // dividerBorderColor + dividerBorderWidth
        const borderWidth = styles.computed.dividerBorderWidth ?? 1;
        const borderColor = styles.computed.dividerBorderColor || '#E5E7EB';
        
        // Use inputWidthOverride if provided (during resize preview), otherwise fallback to component props
        const componentWidth = inputWidthOverride ? `${inputWidthOverride}px` : component.props.width;
        const dividerWidth = componentWidth ?? styles.computed.dividerWidth ?? '100%';
        
        const dividerStyle: React.CSSProperties = {
            borderTopWidth: `${borderWidth}px`,
            borderTopColor: borderColor,
            borderTopStyle: 'solid',
            width: dividerWidth,
            margin: '0',
        };
        
        return (
            <div
                // In builder mode SmartBorder already adds selection padding; keep divider content tight
                // so its border padding matches other components.
                className={builderMode ? undefined : "py-2"}
                style={{ 
                    width: dividerWidth, 
                    paddingTop: builderMode ? 0 : undefined, 
                    paddingBottom: builderMode ? 0 : undefined, 
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'center'
                }}
            >
                <hr 
                    id={componentId ? `${componentId}-divider` : undefined}
                    style={dividerStyle} 
                    aria-hidden="true"
                />
            </div>
        );
    };
}

/**
 * Create a display renderer (e.g., for paragraph, header).
 * Renders read-only display text mapping to the component's dimension overrides.
 */
export function createDisplayRenderer(): ObjectRenderer {
    return ({ component, styles, componentId, builderMode, surface, inputWidthOverride, displayHeightOverride }) => {
        // We use inputWidthOverride for the main display content block, as display objects map to "input" sizing rules.
        const effectiveHeight = displayHeightOverride !== undefined ? displayHeightOverride : styles.computed?.inputHeight;
        const isCanvas = surface === 'canvas' || builderMode;
        
        let contentNode = null;
        if (component.type === 'header') {
            contentNode = (
                <h3 id={componentId ? `${componentId}-content` : undefined} style={{...styles.labelStyle, margin: 0, width: '100%', height: '100%', minHeight: effectiveHeight ? `${effectiveHeight}px` : undefined, display: 'block', whiteSpace: 'pre-wrap', wordBreak: 'break-word'}}>
                    {String(component.props.text ?? component.props.label ?? 'Header')}
                </h3>
            );
        } else {
            contentNode = (
                <p id={componentId ? `${componentId}-content` : undefined} style={{...styles.helpTextStyle, margin: 0, width: '100%', height: '100%', minHeight: effectiveHeight ? `${effectiveHeight}px` : undefined, display: 'block', whiteSpace: 'pre-wrap', wordBreak: 'break-word'}}>
                    {String(component.props.text ?? component.props.label ?? 'Paragraph text goes here.')}
                </p>
            );
        }

        return (
            <div style={{ 
                width: inputWidthOverride ? `${inputWidthOverride}px` : '100%',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'flex-start',
                border: isCanvas ? '1px dashed rgba(0,0,0,0.1)' : undefined
            }}>
                {contentNode}
            </div>
        );
    };
}

/**
 * Get input type based on component type.
 */
function getInputType(componentType: string): string {
    const typeMap: Record<string, string> = {
        'text': 'text',
        'email': 'email',
        'phone': 'tel',
        'url': 'url',
        'number': 'number',
        'first-name': 'text',
    };
    
    return typeMap[componentType] || 'text';
}

function getDateInputType(dateType?: 'date' | 'datetime' | 'time'): string {
    if (dateType === 'datetime') return 'datetime-local';
    if (dateType === 'time') return 'time';
    return 'date';
}

function getDatePartOrder(dateFormat?: string): Array<'day' | 'month' | 'year'> {
    const format = dateFormat || 'DD/MM/YYYY';
    const tokens = Array.from(format.matchAll(/Y+|M+|D+/g)).map(match => match[0]);
    const order: Array<'day' | 'month' | 'year'> = [];

    for (const token of tokens) {
        if (token.startsWith('Y') && !order.includes('year')) order.push('year');
        if (token.startsWith('M') && !order.includes('month')) order.push('month');
        if (token.startsWith('D') && !order.includes('day')) order.push('day');
    }

    if (!order.includes('day')) order.push('day');
    if (!order.includes('month')) order.push('month');
    if (!order.includes('year')) order.push('year');

    return order;
}

function getDateBoundsForInput(validation?: ComponentProps['validation']): { min?: string; max?: string } | undefined {
    if (!validation) return undefined;

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const parseRuleDate = (rule?: string): Date | undefined => {
        if (!rule) return undefined;
        if (rule === 'today') return new Date(today);
        const parsed = new Date(rule);
        if (Number.isNaN(parsed.getTime())) return undefined;
        parsed.setHours(0, 0, 0, 0);
        return parsed;
    };

    const minRule = parseRuleDate(validation.minDate);
    const maxRule = parseRuleDate(validation.maxDate);
    const minFromFuture = validation.futureOnly ? (() => {
        const d = new Date(today);
        d.setDate(d.getDate() + 1);
        return d;
    })() : undefined;
    const maxFromPast = validation.pastOnly ? (() => {
        const d = new Date(today);
        d.setDate(d.getDate() - 1);
        return d;
    })() : undefined;

    const minAllowed = [minRule, minFromFuture].filter(Boolean).sort((a, b) => (a!.getTime() - b!.getTime())).pop();
    const maxAllowed = [maxRule, maxFromPast].filter(Boolean).sort((a, b) => (a!.getTime() - b!.getTime()))[0];

    if (minAllowed && maxAllowed && minAllowed > maxAllowed) {
        return undefined;
    }

    return {
        min: minAllowed ? toDateInputString(minAllowed) : undefined,
        max: maxAllowed ? toDateInputString(maxAllowed) : undefined,
    };
}

function toDateInputString(date: Date): string {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

/**
 * Get default renderers for common object types.
 */
export function getDefaultRenderers(): ObjectRenderers {
    return {
        label: createLabelRenderer(),
        input: createInputRenderer(),
        validation: createValidationRenderer(),
        action: createActionRenderer(),
        status: createStatusRenderer(),
        divider: createDividerRenderer(),
        display: createDisplayRenderer(),
        line: createDividerRenderer(), // Alias for divider components that use 'line' as object id
        content: createDisplayRenderer(), // Alias for display components that use 'content' as object id
    };
}


