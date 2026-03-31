/**
 * AppearanceSection - Story 3.5
 * 
 * Combines typography/spacing overrides with dimensions settings.
 * Renamed from StyleOverridesSection for clarity.
 * 
 * Order matches visual component layout:
 * 1. Dimensions (Width, Height, Alignment)
 * 2. Label Text
 * 3. [Label Gap spacing]
 * 4. Input Text  
 * 5. [Input-to-Help spacing]
 * 6. Help & Validation
 */

import React, { useState, useRef } from 'react';
import { 
    ChevronDown, Link, Unlink, Tag, Type, MessageSquare, 
    ArrowUpDown, Palette, Maximize2, Wand2, LayoutGrid, RotateCcw, Star 
} from 'lucide-react';
import { TypographyCard, PropertySelect, PropertyNumberInput } from './inputs';
import { StyleOverrides, GlobalStyles, FontWeightValue, FontStyleType, ComponentProps, AlignType, ComponentStructure, ObjectLayoutType } from '../../types/builder.types';
import { SpacingSection } from './SpacingSection';
import { ScaleAnchor } from '../../utils/scaleUtils';
import { devLogger } from '../../utils/devLogger';
import { getRatingMarksTypographyInfo } from '../../data/validationRuleSeed';

// Interface for sticky anchor during slider drag
interface StickyAnchor {
    x: number;
    y: number;
    anchor: ScaleAnchor;
    // Base dimensions at 100% scale - used to calculate size at any scale
    baseWidth: number;
    baseHeight: number;
}

interface AppearanceSectionProps {
    overrides: StyleOverrides | undefined;
    globalStyles: GlobalStyles;
    onOverridesChange: (updates: Partial<StyleOverrides>) => void;
    /** Current layout for spacing control direction */
    currentLayout?: 'vertical' | 'horizontal' | 'mixed';
    /** Component props for dimensions */
    props?: ComponentProps;
    /** Handler for component props changes */
    onPropsChange?: (updates: Partial<ComponentProps>) => void;
    /** Component type for conditional rendering */
    componentType?: string;
    /** NEW: Component structure for Universal FieldShell */
    structure?: ComponentStructure;
    /** NEW: Handler for global styles changes */
    onGlobalStylesChange?: (updates: Partial<GlobalStyles>) => void;
    /** Component position for anchor-based scaling */
    componentPosition?: { x: number; y: number };
    /** Handler for position changes (for anchor-based scaling) */
    onPositionChange?: (position: { x: number; y: number }) => void;
    /** Atomic update for position AND props in single render (for smooth anchor scaling) */
    onAtomicScaleChange?: (position: { x: number; y: number }, props: Partial<ComponentProps>) => void;
    /** Component ID for DOM lookup */
    componentId?: string;
}

const WIDTH_PRESET_OPTIONS = [
    { value: 'auto', label: 'Auto' },
    { value: '25%', label: '25%' },
    { value: '33%', label: '33%' },
    { value: '50%', label: '50%' },
    { value: '66%', label: '66%' },
    { value: '75%', label: '75%' },
    { value: '90%', label: '90%' },
    { value: '100%', label: '100%' },
    { value: 'custom', label: 'Custom (px)' },
];

const ALIGN_OPTIONS = [
    { value: 'left', label: 'Left' },
    { value: 'center', label: 'Center' },
    { value: 'right', label: 'Right' },
];

// Object width mode options for individual object width overrides
const OBJECT_WIDTH_OPTIONS = [
    { value: 'auto', label: 'Auto (fit content)' },
    { value: 'fill', label: 'Fill (remaining space)' },
    { value: 'custom', label: 'Custom (px)' },
];

/**
 * Chain link indicator component - shows global/override status
 */
const ChainIndicator: React.FC<{
    isOverridden: boolean;
    onReset: () => void;
    overrideCount?: number;
}> = ({ isOverridden, onReset, overrideCount = 0 }) => (
    <button
        onClick={(e) => {
            e.stopPropagation();
            if (isOverridden) onReset();
        }}
        className={`flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] transition-colors ${
            isOverridden 
                ? 'text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-900/20 hover:bg-amber-100 dark:hover:bg-amber-900/30 cursor-pointer' 
                : 'text-gray-400 bg-gray-50 dark:bg-gray-800 cursor-default'
        }`}
        title={isOverridden ? 'Custom overrides - click to reset to global' : 'Using global values'}
    >
        {isOverridden ? (
            <>
                <Unlink size={10} />
                <span>{overrideCount} override{overrideCount !== 1 ? 's' : ''}</span>
            </>
        ) : (
            <>
                <Link size={10} />
                <span>global</span>
            </>
        )}
    </button>
);

/**
 * Inline spacing control with chain indicator
 */
const SpacingOverride: React.FC<{
    label: string;
    value: number;
    globalValue: number;
    baseSpacing: number;
    onChange: (value: number) => void;
    onReset: () => void;
    isOverridden: boolean;
}> = ({ label, value, globalValue: _globalValue, baseSpacing, onChange, onReset, isOverridden }) => (
    <div className="flex items-center gap-2 py-2 px-3 bg-gray-50 dark:bg-gray-800/50 rounded-lg border border-dashed border-gray-200 dark:border-gray-700">
        <ArrowUpDown size={12} className="text-gray-400" />
        <span className="text-[10px] text-gray-500 dark:text-gray-400 flex-1">{label}</span>
        <div className="flex items-center gap-1">
            <input
                type="range"
                min={0}
                max={4}
                step={0.5}
                value={value}
                onChange={(e) => onChange(parseFloat(e.target.value))}
                className="w-16 h-1 accent-blue-500"
            />
            <span className="text-[10px] font-mono text-gray-600 dark:text-gray-300 w-8 text-right">
                {Math.round(value * baseSpacing)}px
            </span>
        </div>
        <ChainIndicator 
            isOverridden={isOverridden} 
            onReset={onReset}
            overrideCount={1}
        />
    </div>
);

/**
 * Collapsible sub-section within Appearance
 */
const SubSection: React.FC<{
    title: string;
    icon: React.ElementType;
    iconColor: string;
    isExpanded: boolean;
    onToggle: () => void;
    children: React.ReactNode;
    badge?: React.ReactNode;
}> = ({ title, icon: Icon, iconColor, isExpanded, onToggle, children, badge }) => (
    <div className="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
        <button
            onClick={onToggle}
            className="w-full flex items-center justify-between px-3 py-2 text-xs font-medium text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800"
        >
            <div className="flex items-center gap-2">
                <Icon size={12} className={iconColor} />
                <span>{title}</span>
                {badge}
            </div>
            <ChevronDown 
                size={14} 
                className={`transform transition-transform ${isExpanded ? 'rotate-180' : ''}`} 
            />
        </button>
        {isExpanded && (
            <div className="px-3 pb-3 pt-1 border-t border-gray-100 dark:border-gray-800">
                {children}
            </div>
        )}
    </div>
);

export const AppearanceSection: React.FC<AppearanceSectionProps> = ({
    overrides = {},
    globalStyles,
    onOverridesChange,
    currentLayout = 'vertical',
    props,
    onPropsChange,
    componentType = 'text',
    structure,
    onGlobalStylesChange,
    componentPosition,
    onPositionChange,
    onAtomicScaleChange,
    componentId,
}) => {
    const [isExpanded, setIsExpanded] = React.useState(false);
    const [isDimensionsExpanded, setIsDimensionsExpanded] = React.useState(true);
    const [isTypographyExpanded, setIsTypographyExpanded] = React.useState(false);
    const [customWidth, setCustomWidth] = React.useState<number>(300);
    // Anchor point for slider-based scaling (default: NW = component grows toward SE)
    // Initialize from props if available, otherwise default to 'nw'
    const [scaleAnchor, setScaleAnchor] = useState<ScaleAnchor>(props?.componentScaleAnchor ?? 'nw');
    
    // Sync anchor state with props when component changes (e.g., different component selected)
    React.useEffect(() => {
        if (props?.componentScaleAnchor !== undefined) {
            setScaleAnchor(props.componentScaleAnchor);
        } else {
            setScaleAnchor('nw'); // Default to NW if not set
        }
    }, [props?.componentScaleAnchor]);
    
    // Sticky anchor ref - persists across slider drag to prevent drift
    // Stores the EXACT anchor position captured at drag start
    const stickyAnchorRef = useRef<StickyAnchor | null>(null);

    // Dimensions logic
    const isCustomWidth = props?.width?.endsWith('px');
    const currentPreset = isCustomWidth ? 'custom' : (props?.width || 'auto');
    const supportsHeight = ['textarea'].includes(componentType);
    const supportsAutoFit = ['text', 'email', 'number', 'dropdown', 'phone'].includes(componentType);
    
    // Components that support object width overrides (most input types with label/input/validation objects)
    const supportsObjectWidthOverrides = [
        'text', 'email', 'number', 'phone', 'textarea', 'dropdown', 
        'checkbox', 'radio', 'date', 'address', 'first-name', 'terms'
    ].includes(componentType);
    
    // Check if any object width override is set
    const hasAnyObjectWidthOverride = props && (
        props.labelWidthOverride !== undefined || 
        props.inputWidthOverride !== undefined || 
        props.helpWidthOverride !== undefined
    );
    
    // Object width mode helpers
    const getLabelWidthMode = (): string => {
        if (props?.labelWidthOverride !== undefined) return 'custom';
        return 'auto';
    };
    
    const getInputWidthMode = (): string => {
        if (props?.inputWidthOverride !== undefined) return 'custom';
        if (props?.inputWidthMode === 'fill') return 'fill';
        return 'auto';
    };
    
    const getHelpWidthMode = (): string => {
        if (props?.helpWidthOverride !== undefined) return 'custom';
        return 'auto';
    };
    
    const handleLabelWidthModeChange = (mode: string) => {
        if (!onPropsChange) return;
        if (mode === 'auto') {
            onPropsChange({ labelWidthOverride: undefined });
        } else if (mode === 'fill') {
            onPropsChange({ labelWidthOverride: undefined });
        } else if (mode === 'custom') {
            onPropsChange({ labelWidthOverride: 120 });
        }
    };
    
    const handleInputWidthModeChange = (mode: string) => {
        if (!onPropsChange) return;
        if (mode === 'auto') {
            onPropsChange({ inputWidthOverride: undefined, inputWidthMode: undefined });
        } else if (mode === 'fill') {
            onPropsChange({ inputWidthOverride: undefined, inputWidthMode: 'fill' });
        } else if (mode === 'custom') {
            onPropsChange({ inputWidthOverride: 200 });
        }
    };
    
    const handleHelpWidthModeChange = (mode: string) => {
        if (!onPropsChange) return;
        if (mode === 'auto') {
            onPropsChange({ helpWidthOverride: undefined });
        } else if (mode === 'fill') {
            onPropsChange({ helpWidthOverride: undefined });
        } else if (mode === 'custom') {
            onPropsChange({ helpWidthOverride: 200 });
        }
    };

    const handleWidthPresetChange = (value: string) => {
        if (!onPropsChange) return;
        
        const isSubmitButton = componentType === 'submit-button';
        
        // ═══════════════════════════════════════════════════════════════
        // BUTTON WIDTH CHANGE LOGGING (for debugging panel changes)
        // ═══════════════════════════════════════════════════════════════
        if (isSubmitButton) {
            const currentWidth = props?.width;
            const currentActionWidthOverride = props?.actionWidthOverride;
            
            devLogger.info('panel.button.width.preset.changed', {
                componentId: componentId,
                componentType: componentType,
                BEFORE: {
                    width: currentWidth,
                    actionWidthOverride: currentActionWidthOverride,
                },
                NEW_VALUE: value,
                IS_CUSTOM: value === 'custom',
                IS_AUTO: value === 'auto',
            });
        }
        
        if (value === 'custom') {
            const updates: Partial<ComponentProps> = { width: `${customWidth}px` };
            if (isSubmitButton) {
                updates.actionWidthOverride = customWidth;
            }
            
            if (isSubmitButton) {
                devLogger.info('panel.button.width.custom.applied', {
                    componentId: componentId,
                    customWidth,
                    updates,
                });
            }
            
            onPropsChange(updates);
        } else if (value === 'auto') {
            // Clear width to allow auto-sizing (undefined is the true "auto" state)
            const updates: Partial<ComponentProps> = { width: undefined };
            if (isSubmitButton) {
                updates.actionWidthOverride = undefined;
            }
            
            if (isSubmitButton) {
                devLogger.info('panel.button.width.auto.applied', {
                    componentId: componentId,
                    updates,
                });
            }
            
            onPropsChange(updates);
        } else {
            // For buttons: set both width (for container) and actionWidthOverride (for button element)
            const updates: Partial<ComponentProps> = { width: value };
            
            if (isSubmitButton) {
                if (value.endsWith('%')) {
                    // For percentage widths: keep width as percentage (for container/SmartBorder)
                    // and set actionWidthOverride to undefined so button fills container (100%)
                    // CRITICAL: Store uses Object.keys() which includes keys with undefined values
                    // We must explicitly set the key so store can delete it
                    (updates as Record<string, unknown>).actionWidthOverride = undefined;
                } else if (value.endsWith('px')) {
                    // For pixel widths: set both width and actionWidthOverride to the same value
                    const widthPx = parseInt(value, 10);
                    updates.width = `${widthPx}px`;
                    updates.actionWidthOverride = widthPx;
                }
            }
            
            if (isSubmitButton) {
                // Create a log-safe version that shows undefined values
                const logUpdates: Record<string, unknown> = { ...updates };
                if (value.endsWith('%')) {
                    logUpdates.actionWidthOverride = undefined; // Explicitly show undefined
                }
                devLogger.info('panel.button.width.preset.applied', {
                    componentId: componentId,
                    value,
                    updates: logUpdates,
                    actualUpdatesKeys: Object.keys(updates),
                    hasActionWidthOverrideKey: 'actionWidthOverride' in updates,
                    actionWidthOverrideValue: (updates as Record<string, unknown>).actionWidthOverride,
                    parsedPx: value.endsWith('px') ? parseInt(value, 10) : undefined,
                    isPercentage: value.endsWith('%'),
                });
            }
            
            onPropsChange(updates);
        }
    };

    const handleCustomWidthChange = (value: number) => {
        if (!onPropsChange) return;
        setCustomWidth(value);
        const updates: Partial<ComponentProps> = { width: `${value}px` };
        // For buttons: also set actionWidthOverride
        if (componentType === 'submit-button') {
            updates.actionWidthOverride = value;
            
            devLogger.info('panel.button.width.custom.changed', {
                componentId: componentId,
                BEFORE: {
                    width: props?.width,
                    actionWidthOverride: props?.actionWidthOverride,
                },
                NEW_VALUE: value,
                updates,
            });
        }
        onPropsChange(updates);
    };

    // Count overrides for each category
    const labelOverrides = ['labelFontFamily', 'labelFontSize', 'labelFontWeight', 'labelFontStyle', 'labelColor', 'labelBackgroundColor', 'labelBorderColor', 'labelBorderWidth', 'labelBorderRadius']
        .filter(key => key in overrides).length;
    
    const inputOverrides = [
        'fontFamily', 'fontSize', 'fontWeight', 'fontStyle', 'textColor', 'textBackgroundColor',
        'textBorderColor', 'textBorderWidth', 'textBorderRadius', 'inputHeight',
        'ratingColor', 'ratingBackgroundColor',
    ].filter(key => key in overrides).length;
    
    const helpOverrides = ['helpTextFontFamily', 'helpTextFontSize', 'helpTextFontWeight', 'helpTextFontStyle', 'helpTextColor', 'helpTextBackgroundColor', 'helpTextBorderColor', 'helpTextBorderWidth', 'helpTextBorderRadius']
        .filter(key => key in overrides).length;

    const totalOverrides = Object.keys(overrides).length;

    // Helper to get effective value
    const getEffective = <K extends keyof StyleOverrides>(key: K, fallbackKey?: keyof GlobalStyles): NonNullable<StyleOverrides[K]> => {
        if (key in overrides) return overrides[key] as NonNullable<StyleOverrides[K]>;
        const gKey = fallbackKey || (key as keyof GlobalStyles);
        return globalStyles[gKey] as NonNullable<StyleOverrides[K]>;
    };
    
    const getDisplayValue = <K extends keyof StyleOverrides>(key: K, fallbackKey?: keyof GlobalStyles): StyleOverrides[K] | undefined => {
        if (key in overrides) return overrides[key];
        const gKey = fallbackKey || (key as keyof GlobalStyles);
        return globalStyles[gKey] as StyleOverrides[K];
    };

    // Reset helpers
    const resetLabelStyles = () => {
        const updates = { ...overrides };
        ['labelFontFamily', 'labelFontSize', 'labelFontWeight', 'labelFontStyle', 'labelColor', 'labelBackgroundColor', 'labelBorderColor', 'labelBorderWidth', 'labelBorderRadius']
            .forEach(key => delete updates[key as keyof StyleOverrides]);
        onOverridesChange(updates);
    };

    const resetInputStyles = () => {
        const updates = { ...overrides };
        [
            'fontFamily', 'fontSize', 'fontWeight', 'fontStyle', 'textColor', 'textBackgroundColor',
            'textBorderColor', 'textBorderWidth', 'textBorderRadius', 'inputHeight',
            'ratingColor', 'ratingBackgroundColor',
        ].forEach(key => delete updates[key as keyof StyleOverrides]);
        onOverridesChange(updates);
    };

    const resetHelpStyles = () => {
        const updates = { ...overrides };
        ['helpTextFontFamily', 'helpTextFontSize', 'helpTextFontWeight', 'helpTextFontStyle', 'helpTextColor', 'helpTextBackgroundColor', 'helpTextBorderColor', 'helpTextBorderWidth', 'helpTextBorderRadius']
            .forEach(key => delete updates[key as keyof StyleOverrides]);
        onOverridesChange(updates);
    };

    // Border change handlers
    const handleBorderChange = (
        colorKey: keyof StyleOverrides,
        widthKey: keyof StyleOverrides,
        radiusKey: keyof StyleOverrides
    ) => ({
        onColorChange: (v: string | undefined) => {
            onOverridesChange({ [colorKey]: v } as Partial<StyleOverrides>);
        },
        onWidthChange: (v: number | undefined) => {
            onOverridesChange({ [widthKey]: v } as Partial<StyleOverrides>);
        },
        onRadiusChange: (v: number | undefined) => {
            onOverridesChange({ [radiusKey]: v } as Partial<StyleOverrides>);
        },
    });

    const labelBorderHandlers = handleBorderChange('labelBorderColor', 'labelBorderWidth', 'labelBorderRadius');
    const inputBorderHandlers = handleBorderChange('textBorderColor', 'textBorderWidth', 'textBorderRadius');
    const helpBorderHandlers = handleBorderChange('helpTextBorderColor', 'helpTextBorderWidth', 'helpTextBorderRadius');

    return (
        <div className="border-b border-gray-200 dark:border-gray-700">
            {/* Section Header */}
            <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="w-full flex items-center justify-between px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
            >
                <div className="flex items-center gap-2">
                    <Palette size={14} className="text-purple-500" />
                    <span>Appearance</span>
                    {totalOverrides > 0 && (
                        <span className="text-xs bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400 px-1.5 py-0.5 rounded">
                            {totalOverrides} custom
                        </span>
                    )}
                </div>
                <ChevronDown 
                    size={16} 
                    className={`transform transition-transform ${isExpanded ? 'rotate-180' : ''}`} 
                />
            </button>

            {/* Section Content */}
            {isExpanded && (
                <div className="px-4 pb-4 space-y-3">
                    {/* ═══════════════════════════════════════════════════════════════ */}
                    {/* DIMENSIONS SUB-SECTION */}
                    {/* ═══════════════════════════════════════════════════════════════ */}
                    {props && onPropsChange && (
                        <SubSection
                            title="Dimensions"
                            icon={Maximize2}
                            iconColor="text-blue-500"
                            isExpanded={isDimensionsExpanded}
                            onToggle={() => setIsDimensionsExpanded(!isDimensionsExpanded)}
                        >
                            <div className="space-y-3">
                                {/* Width Preset */}
                                <PropertySelect
                                    label="Width"
                                    value={currentPreset}
                                    onChange={handleWidthPresetChange}
                                    options={WIDTH_PRESET_OPTIONS}
                                    helpText="Component width"
                                />

                                {/* Custom Width Input */}
                                {isCustomWidth && (
                                    <PropertyNumberInput
                                        label="Custom Width"
                                        value={parseInt(props.width || '300')}
                                        onChange={handleCustomWidthChange}
                                        min={50}
                                        max={2000}
                                        step={10}
                                        unit="px"
                                    />
                                )}

                                {/* Auto-fit to Content */}
                                {supportsAutoFit && (
                                    <div className="p-2 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                                        <div className="flex items-center justify-between">
                                            <div className="flex items-center gap-2">
                                                <Wand2 size={12} className="text-blue-500" />
                                                <span className="text-xs text-blue-700 dark:text-blue-300">
                                                    Auto-fit Width
                                                </span>
                                            </div>
                                            <button
                                                type="button"
                                                onClick={() => {
                                                    onPropsChange({ width: '90%', inputWidthMode: 'fill' });
                                                }}
                                                className="px-2 py-1 text-[10px] bg-blue-600 text-white rounded hover:bg-blue-700"
                                            >
                                                Calculate
                                            </button>
                                        </div>
                                    </div>
                                )}

                                {/* Height (for textarea) */}
                                {supportsHeight && (
                                    <PropertyNumberInput
                                        label="Height"
                                        value={props.styleOverrides?.inputHeight ?? props.height ?? 40}
                                        onChange={(value) =>
                                            onPropsChange({
                                                styleOverrides: { ...(props.styleOverrides || {}), inputHeight: value },
                                                height: undefined,
                                            })
                                        }
                                        min={40}
                                        max={500}
                                        step={10}
                                        unit="px"
                                    />
                                )}

                                {/* Text Alignment */}
                                <PropertySelect
                                    label={componentType === 'submit-button' ? "Container Alignment (Canvas)" : "Text Alignment"}
                                    value={props.textAlign || 'left'}
                                    onChange={(value) => onPropsChange({ textAlign: value as AlignType })}
                                    options={ALIGN_OPTIONS}
                                    helpText={componentType === 'submit-button' 
                                        ? "Alignment of the component container on the canvas (use Button Settings for button alignment)"
                                        : undefined}
                                />

                                {/* Component Scale - Proportional scaling with anchor selection
                                    Uses shared scaleUtils for unified scaling logic.
                                    Anchor determines which corner stays fixed during scaling. */}
                                <div className="space-y-2 pt-2 border-t border-gray-100 dark:border-gray-700">
                                    <div className="flex items-center justify-between">
                                        <span className="text-xs font-medium text-gray-700 dark:text-gray-300">
                                            Component Scale
                                        </span>
                                        <span className="text-sm font-bold font-mono text-gray-500 dark:text-gray-400">
                                            {props.componentScale ?? 100}%
                                        </span>
                                    </div>
                                    
                                    {/* Anchor Point Selection - 2x2 grid */}
                                    <div className="flex items-center gap-2">
                                        <span className="text-[10px] text-gray-500 dark:text-gray-400">Anchor:</span>
                                        <div className="grid grid-cols-2 gap-0.5 p-1 bg-gray-100 dark:bg-gray-800 rounded">
                                            {(['nw', 'ne', 'sw', 'se'] as ScaleAnchor[]).map((anchor) => (
                                                <button
                                                    key={anchor}
                                                    type="button"
                                                    onClick={() => {
                                                        setScaleAnchor(anchor);
                                                        // Save anchor to component props so SortableComponent can use it for transform-origin
                                                        onPropsChange?.({ componentScaleAnchor: anchor });
                                                    }}
                                                    className={`w-5 h-5 text-[8px] font-bold rounded transition-colors ${
                                                        scaleAnchor === anchor
                                                            ? 'bg-blue-500 text-white'
                                                            : 'bg-white dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-blue-100 dark:hover:bg-blue-900/30'
                                                    }`}
                                                    title={`Anchor ${anchor.toUpperCase()} corner (${anchor === 'nw' ? 'top-left' : anchor === 'ne' ? 'top-right' : anchor === 'sw' ? 'bottom-left' : 'bottom-right'})`}
                                                >
                                                    {anchor.toUpperCase()}
                                                </button>
                                            ))}
                                        </div>
                                        <span className="text-[9px] text-gray-400">{scaleAnchor === 'nw' ? '↘' : scaleAnchor === 'ne' ? '↙' : scaleAnchor === 'sw' ? '↗' : '↖'}</span>
                                    </div>
                                    
                                    <input
                                        type="range"
                                        min={50}
                                        max={200}
                                        step={5}
                                        value={props.componentScale ?? 100}
                                        onMouseDown={() => {
                                            // Capture sticky anchor AND base dimensions at START of drag
                                            if (scaleAnchor === 'nw' || !componentPosition || !componentId) {
                                                stickyAnchorRef.current = null;
                                                return;
                                            }
                                            
                                            const el = document.querySelector(`[data-component-id="${componentId}"]`) as HTMLElement;
                                            const rect = el?.getBoundingClientRect();
                                            if (!rect) {
                                                stickyAnchorRef.current = null;
                                                return;
                                            }
                                            
                                            const canvasContainer = document.querySelector('[data-canvas-container]') as HTMLElement;
                                            const canvasScale = canvasContainer ? 
                                                parseFloat(canvasContainer.style.transform?.match(/scale\(([^)]+)\)/)?.[1] || '1') : 1;
                                            
                                            const currentScale = props?.componentScale ?? 100;
                                            const canvasWidth = rect.width / canvasScale;
                                            const canvasHeight = rect.height / canvasScale;
                                            
                                            // Calculate BASE dimensions at 100% scale
                                            const baseWidth = canvasWidth * (100 / currentScale);
                                            const baseHeight = canvasHeight * (100 / currentScale);
                                            
                                            let anchorX = componentPosition.x;
                                            let anchorY = componentPosition.y;
                                            
                                            if (scaleAnchor === 'ne' || scaleAnchor === 'se') {
                                                anchorX = componentPosition.x + canvasWidth;
                                            }
                                            if (scaleAnchor === 'se' || scaleAnchor === 'sw') {
                                                anchorY = componentPosition.y + canvasHeight;
                                            }
                                            
                                            stickyAnchorRef.current = { 
                                                x: anchorX, 
                                                y: anchorY, 
                                                anchor: scaleAnchor,
                                                baseWidth,
                                                baseHeight,
                                            };
                                            
                                            devLogger.info('scale.slider.start', {
                                                componentId,
                                                anchor: scaleAnchor,
                                                currentScale,
                                                stickyAnchor: stickyAnchorRef.current,
                                                componentPosition,
                                                dimensions: { width: canvasWidth, height: canvasHeight },
                                                baseDimensions: { width: baseWidth, height: baseHeight },
                                            });
                                        }}
                                        onMouseUp={() => {
                                            // Clear sticky anchor at END of drag
                                            if (stickyAnchorRef.current) {
                                                devLogger.info('scale.slider.end', {
                                                    componentId,
                                                    stickyAnchor: stickyAnchorRef.current,
                                                });
                                            }
                                            stickyAnchorRef.current = null;
                                        }}
                                        onChange={(e) => {
                                            const newScale = parseInt(e.target.value);
                                            
                                            // If anchor is NW or no sticky anchor, just update scale
                                            if (scaleAnchor === 'nw' || !stickyAnchorRef.current) {
                                                onPropsChange?.({ componentScale: newScale });
                                                return;
                                            }
                                            
                                            const sticky = stickyAnchorRef.current;
                                            
                                            // Calculate new dimensions from BASE dimensions (no DOM measurement needed!)
                                            const newWidth = sticky.baseWidth * (newScale / 100);
                                            const newHeight = sticky.baseHeight * (newScale / 100);
                                            
                                            // Calculate position using the STICKY anchor
                                            let newX: number;
                                            let newY: number;
                                            
                                            // For NE/SE: right edge is fixed, so x = anchorX - width
                                            if (sticky.anchor === 'ne' || sticky.anchor === 'se') {
                                                newX = sticky.x - newWidth;
                                            } else {
                                                newX = sticky.x; // NW/SW: left edge is fixed
                                            }
                                            
                                            // For SE/SW: bottom edge is fixed, so y = anchorY - height
                                            if (sticky.anchor === 'se' || sticky.anchor === 'sw') {
                                                newY = sticky.y - newHeight;
                                            } else {
                                                newY = sticky.y; // NW/NE: top edge is fixed
                                            }
                                            
                                            devLogger.info('scale.slider.change', {
                                                componentId,
                                                newScale,
                                                stickyAnchor: sticky,
                                                calculatedSize: { width: newWidth, height: newHeight },
                                                newPosition: { x: newX, y: newY },
                                                mode: onAtomicScaleChange ? 'atomic' : 'separate',
                                            });
                                            
                                            // Use atomic update if available (single render), otherwise fallback to separate calls
                                            if (onAtomicScaleChange) {
                                                onAtomicScaleChange({ x: newX, y: newY }, { componentScale: newScale });
                                            } else {
                                                onPositionChange?.({ x: newX, y: newY });
                                                onPropsChange?.({ componentScale: newScale });
                                            }
                                        }}
                                        className="w-full h-1.5 accent-blue-500"
                                    />
                                    <div className="flex justify-between text-[9px] text-gray-400">
                                        <span>50%</span>
                                        <span className="text-blue-500">100%</span>
                                        <span>200%</span>
                                    </div>
                                    <p className="text-[10px] text-gray-400 dark:text-gray-500">
                                        Scales proportionally. Anchor = fixed corner.
                                    </p>
                                    {(props.componentScale ?? 100) !== 100 && (
                                        <button
                                            type="button"
                                            onClick={() => onPropsChange?.({ componentScale: 100 })}
                                            className="w-full mt-1 py-1 text-[10px] text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded border border-blue-200 dark:border-blue-800"
                                        >
                                            Reset to 100%
                                        </button>
                                    )}
                                </div>

                                {/* Object Width Overrides - for horizontal/mixed layouts */}
                                {supportsObjectWidthOverrides && (
                                    <div className="pt-3 border-t border-gray-100 dark:border-gray-700">
                                        <div className="flex items-center justify-between mb-2">
                                            <div className="flex items-center gap-2">
                                                <LayoutGrid size={12} className="text-purple-500" />
                                                <span className="text-xs font-medium text-gray-700 dark:text-gray-300">
                                                    Object Widths
                                                </span>
                                            </div>
                                            {hasAnyObjectWidthOverride && (
                                                <button
                                                    type="button"
                                                    onClick={() => onPropsChange({
                                                        labelWidthOverride: undefined,
                                                        inputWidthOverride: undefined,
                                                        helpWidthOverride: undefined,
                                                    })}
                                                    className="flex items-center gap-1 px-1.5 py-0.5 text-[10px] text-gray-500 hover:text-gray-700 dark:hover:text-gray-300"
                                                    title="Reset all object widths to auto"
                                                >
                                                    <RotateCcw size={10} />
                                                    Reset
                                                </button>
                                            )}
                                        </div>
                                        <p className="text-[10px] text-gray-500 dark:text-gray-400 mb-2">
                                            Set individual widths for Label, Input, and Validation objects in horizontal layouts.
                                        </p>

                                        <div className="space-y-2">
                                            {/* Label Width */}
                                            <PropertySelect
                                                label="Label Width"
                                                value={getLabelWidthMode()}
                                                onChange={handleLabelWidthModeChange}
                                                options={OBJECT_WIDTH_OPTIONS}
                                                helpText="Width of the label object"
                                            />
                                            {props.labelWidthOverride !== undefined && (
                                                <PropertyNumberInput
                                                    label="Label Width (px)"
                                                    value={props.labelWidthOverride}
                                                    onChange={(value) => onPropsChange({ labelWidthOverride: value })}
                                                    min={30}
                                                    max={800}
                                                    step={10}
                                                    unit="px"
                                                />
                                            )}

                                            {/* Input Width */}
                                            <PropertySelect
                                                label="Input Width"
                                                value={getInputWidthMode()}
                                                onChange={handleInputWidthModeChange}
                                                options={OBJECT_WIDTH_OPTIONS}
                                                helpText="Width of the input control"
                                            />
                                            {props.inputWidthOverride !== undefined && (
                                                <PropertyNumberInput
                                                    label="Input Width (px)"
                                                    value={props.inputWidthOverride}
                                                    onChange={(value) => onPropsChange({ inputWidthOverride: value })}
                                                    min={50}
                                                    max={1200}
                                                    step={10}
                                                    unit="px"
                                                />
                                            )}

                                            {/* Validation Width */}
                                            <PropertySelect
                                                label="Validation Width"
                                                value={getHelpWidthMode()}
                                                onChange={handleHelpWidthModeChange}
                                                options={OBJECT_WIDTH_OPTIONS}
                                                helpText="Width of validation/help text"
                                            />
                                            {props.helpWidthOverride !== undefined && (
                                                <PropertyNumberInput
                                                    label="Validation Width (px)"
                                                    value={props.helpWidthOverride}
                                                    onChange={(value) => onPropsChange({ helpWidthOverride: value })}
                                                    min={50}
                                                    max={1200}
                                                    step={10}
                                                    unit="px"
                                                />
                                            )}
                                        </div>
                                    </div>
                                )}
                            </div>
                        </SubSection>
                    )}

                    {/* ═══════════════════════════════════════════════════════════════ */}
                    {/* TYPOGRAPHY SUB-SECTION */}
                    {/* ═══════════════════════════════════════════════════════════════ */}
                    <SubSection
                        title="Typography & Colors"
                        icon={Type}
                        iconColor="text-orange-500"
                        isExpanded={isTypographyExpanded}
                        onToggle={() => setIsTypographyExpanded(!isTypographyExpanded)}
                        badge={totalOverrides > 0 ? (
                            <span className="text-[10px] bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400 px-1 py-0.5 rounded">
                                {totalOverrides}
                            </span>
                        ) : undefined}
                    >
                        <div className="space-y-2">
                            {/* Info Banner */}
                            <div className="text-[10px] text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-800 p-2 rounded mb-2">
                                <Link size={8} className="inline text-gray-400" /> global | 
                                <Unlink size={8} className="inline text-amber-500 ml-1" /> custom (click to reset)
                            </div>

                            {/* 1. Label Text Card */}
                            {!['paragraph'].includes(componentType) && (
                                <div className="relative">
                                    <div className="absolute -top-1 right-2 z-10">
                                        <ChainIndicator 
                                            isOverridden={labelOverrides > 0} 
                                            onReset={resetLabelStyles}
                                            overrideCount={labelOverrides}
                                        />
                                    </div>
                                    <TypographyCard
                                        title={componentType === 'header' ? "Header Text" : "Label Text"}
                                        icon={Tag}
                                        iconColor="text-green-500"
                                        fontFamily={getEffective('labelFontFamily', 'labelFontFamily')}
                                        fontSize={getEffective('labelFontSize', 'labelFontSize') ?? 14}
                                        fontWeight={getEffective('labelFontWeight', 'labelFontWeight') ?? '500'}
                                        fontStyle={getEffective('labelFontStyle', 'labelFontStyle') ?? 'normal'}
                                        color={getEffective('labelColor', 'labelColor')}
                                        backgroundColor={getDisplayValue('labelBackgroundColor', 'labelBackgroundColor')}
                                        borderColor={getDisplayValue('labelBorderColor', 'labelBorderColor')}
                                        borderWidth={getDisplayValue('labelBorderWidth', 'labelBorderWidth')}
                                        borderRadius={getDisplayValue('labelBorderRadius', 'labelBorderRadius')}
                                        showBorderOptions={true}
                                        onFontFamilyChange={(v) => onOverridesChange({ labelFontFamily: v })}
                                        onFontSizeChange={(v) => onOverridesChange({ labelFontSize: v })}
                                        onFontWeightChange={(v) => onOverridesChange({ labelFontWeight: v as FontWeightValue })}
                                        onFontStyleChange={(v) => onOverridesChange({ labelFontStyle: v as FontStyleType })}
                                        onColorChange={(v) => onOverridesChange({ labelColor: v })}
                                        onBackgroundColorChange={(v) => onOverridesChange({ labelBackgroundColor: v })}
                                        onBorderColorChange={labelBorderHandlers.onColorChange}
                                        onBorderWidthChange={labelBorderHandlers.onWidthChange}
                                        onBorderRadiusChange={labelBorderHandlers.onRadiusChange}
                                        minSize={10}
                                        maxSize={64}
                                    />
                                </div>
                            )}

                            {/* Spacing: Label to Input */}
                            {!['header', 'paragraph'].includes(componentType) && (
                                <SpacingOverride
                                    label={(currentLayout === 'horizontal' || currentLayout === 'mixed') ? 'Label → Input' : 'Label ↓ Input'}
                                    value={'labelGap' in overrides ? overrides.labelGap! : globalStyles.labelGap}
                                    globalValue={globalStyles.labelGap}
                                    baseSpacing={globalStyles.baseSpacing}
                                    onChange={(v) => onOverridesChange({ labelGap: v })}
                                    onReset={() => {
                                        const updates = { ...overrides };
                                        delete updates.labelGap;
                                        onOverridesChange(updates);
                                    }}
                                    isOverridden={'labelGap' in overrides}
                                />
                            )}

                            {/* 2. Input Text Card — rating uses same controls for marks row (stars / numbers / emoji cells) */}
                            {!['submit-button', 'header', 'paragraph'].includes(componentType) && (
                                <>
                                    <div className="relative">
                                        <div className="absolute -top-1 right-2 z-10">
                                            <ChainIndicator 
                                                isOverridden={inputOverrides > 0} 
                                                onReset={resetInputStyles}
                                                overrideCount={inputOverrides}
                                            />
                                        </div>
                                        <TypographyCard
                                            title={componentType === 'rating' ? 'Rating marks' : 'Input Text'}
                                            titleInfo={
                                                componentType === 'rating'
                                                    ? getRatingMarksTypographyInfo()
                                                    : undefined
                                            }
                                            icon={componentType === 'rating' ? Star : Type}
                                            iconColor={componentType === 'rating' ? 'text-amber-500' : 'text-blue-500'}
                                            fontFamily={getEffective('fontFamily', 'fontFamily')}
                                            fontSize={getEffective('fontSize', 'fontSize') ?? 14}
                                            fontWeight={getEffective('fontWeight', 'fontWeight') ?? '400'}
                                            fontStyle={getEffective('fontStyle', 'fontStyle') ?? 'normal'}
                                            color={getEffective('textColor', 'textColor')}
                                            backgroundColor={getDisplayValue('textBackgroundColor', 'textBackgroundColor')}
                                            borderColor={getDisplayValue('textBorderColor', 'textBorderColor')}
                                            borderWidth={getDisplayValue('textBorderWidth', 'textBorderWidth')}
                                            borderRadius={getDisplayValue('textBorderRadius', 'textBorderRadius')}
                                            showBorderOptions={true}
                                            inputHeight={overrides.inputHeight ?? globalStyles.inputHeight}
                                            onFontFamilyChange={(v) => onOverridesChange({ fontFamily: v })}
                                            onFontSizeChange={(v) => onOverridesChange({ fontSize: v })}
                                            onFontWeightChange={(v) => onOverridesChange({ fontWeight: v as FontWeightValue })}
                                            onFontStyleChange={(v) => onOverridesChange({ fontStyle: v as FontStyleType })}
                                            onColorChange={(v) => onOverridesChange({ textColor: v })}
                                            onBackgroundColorChange={(v) => onOverridesChange({ textBackgroundColor: v })}
                                            onBorderColorChange={inputBorderHandlers.onColorChange}
                                            onBorderWidthChange={inputBorderHandlers.onWidthChange}
                                            onBorderRadiusChange={inputBorderHandlers.onRadiusChange}
                                            onInputHeightChange={(v) => onOverridesChange({ inputHeight: v })}
                                            minSize={10}
                                            maxSize={32}
                                        />
                                    </div>

                                    {/* Spacing: Input to Help */}
                                    <SpacingOverride
                                        label="Input ↓ Help text"
                                        value={'inputHelpGap' in overrides ? overrides.inputHelpGap! : globalStyles.inputHelpGap}
                                        globalValue={globalStyles.inputHelpGap}
                                        baseSpacing={globalStyles.baseSpacing}
                                        onChange={(v) => onOverridesChange({ inputHelpGap: v })}
                                        onReset={() => {
                                            const updates = { ...overrides };
                                            delete updates.inputHelpGap;
                                            onOverridesChange(updates);
                                        }}
                                        isOverridden={'inputHelpGap' in overrides}
                                    />
                                </>
                            )}

                            {/* 3. Help & Validation Card (also acts as main typography for Paragraph) */}
                            {!['header'].includes(componentType) && (
                                <div className="relative">
                                    <div className="absolute -top-1 right-2 z-10">
                                        <ChainIndicator 
                                            isOverridden={helpOverrides > 0} 
                                            onReset={resetHelpStyles}
                                            overrideCount={helpOverrides}
                                        />
                                    </div>
                                    <TypographyCard
                                        title={componentType === 'paragraph' ? "Paragraph Text" : "Help & Validation"}
                                        icon={componentType === 'paragraph' ? Type : MessageSquare}
                                        iconColor={componentType === 'paragraph' ? "text-green-500" : "text-orange-500"}
                                        fontFamily={getEffective('helpTextFontFamily', 'helpTextFontFamily')}
                                        fontSize={getEffective('helpTextFontSize', 'helpTextFontSize') ?? 12}
                                        fontWeight={getEffective('helpTextFontWeight', 'helpTextFontWeight') ?? '400'}
                                        fontStyle={getEffective('helpTextFontStyle', 'helpTextFontStyle') ?? 'normal'}
                                        color={getEffective('helpTextColor', 'helpTextColor')}
                                        backgroundColor={getDisplayValue('helpTextBackgroundColor', 'helpTextBackgroundColor')}
                                        borderColor={getDisplayValue('helpTextBorderColor', 'helpTextBorderColor')}
                                        borderWidth={getDisplayValue('helpTextBorderWidth', 'helpTextBorderWidth')}
                                        borderRadius={getDisplayValue('helpTextBorderRadius', 'helpTextBorderRadius')}
                                        showBorderOptions={true}
                                        onFontFamilyChange={(v) => onOverridesChange({ helpTextFontFamily: v })}
                                        onFontSizeChange={(v) => onOverridesChange({ helpTextFontSize: v })}
                                        onFontWeightChange={(v) => onOverridesChange({ helpTextFontWeight: v as FontWeightValue })}
                                        onFontStyleChange={(v) => onOverridesChange({ helpTextFontStyle: v as FontStyleType })}
                                        onColorChange={(v) => onOverridesChange({ helpTextColor: v })}
                                        onBackgroundColorChange={(v) => onOverridesChange({ helpTextBackgroundColor: v })}
                                        onBorderColorChange={helpBorderHandlers.onColorChange}
                                        onBorderWidthChange={helpBorderHandlers.onWidthChange}
                                        onBorderRadiusChange={helpBorderHandlers.onRadiusChange}
                                        minSize={8}
                                        maxSize={64}
                                    />
                                </div>
                            )}

                            {/* Reset All Button */}
                            {totalOverrides > 0 && (
                                <button
                                    onClick={() => onOverridesChange({})}
                                    className="w-full mt-2 py-1.5 text-[10px] text-amber-600 dark:text-amber-400 hover:bg-amber-50 dark:hover:bg-amber-900/20 rounded border border-amber-200 dark:border-amber-800 transition-colors"
                                >
                                    Reset All Typography to Global
                                </button>
                            )}
                        </div>
                    </SubSection>
                    
                    {/* ═══════════════════════════════════════════════════════════════ */}
                    {/* SPACING SUB-SECTION (NEW) */}
                    {/* ═══════════════════════════════════════════════════════════════ */}
                    {structure && props && onPropsChange && (
                        <SubSection
                            title="Spacing"
                            icon={ArrowUpDown}
                            iconColor="text-purple-500"
                            isExpanded={true}
                            onToggle={() => {}}
                        >
                            <SpacingSection
                                structure={structure}
                                currentLayout={(props.objectLayout || structure.defaultLayout || 'vertical') as ObjectLayoutType}
                                globalStyles={globalStyles}
                                objectSpacing={props.objectSpacing}
                                onGlobalStylesChange={onGlobalStylesChange || (() => {})}
                                onPropsChange={onPropsChange}
                            />
                        </SubSection>
                    )}
                </div>
            )}
        </div>
    );
};

// Also export as StyleOverridesSection for backwards compatibility
export const StyleOverridesSection = AppearanceSection;


