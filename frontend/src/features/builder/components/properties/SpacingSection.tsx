/**
 * SpacingSection Component
 * 
 * Properties Panel section for configuring spacing between objects within components.
 * Layout-aware spacing controls (horizontal gap, vertical spacing, object gaps).
 */

import React from 'react';
import { ArrowUpDown, ArrowLeftRight, Maximize2 } from 'lucide-react';
import { ComponentStructure, ComponentProps, ObjectLayoutType, GlobalStyles } from '../../types/builder.types';
import { PropertyNumberInput } from './inputs';
import { devLogger } from '../../utils/devLogger';

interface SpacingSectionProps {
    structure: ComponentStructure;
    currentLayout: ObjectLayoutType;
    globalStyles: GlobalStyles;
    objectSpacing?: ComponentProps['objectSpacing'];
    onGlobalStylesChange: (updates: Partial<GlobalStyles>) => void;
    onPropsChange: (updates: Partial<ComponentProps>) => void;
}

export const SpacingSection: React.FC<SpacingSectionProps> = ({
    currentLayout,
    globalStyles,
    objectSpacing,
    onPropsChange,
}) => {
    const baseSpacing = globalStyles.baseSpacing;
    const defaultHorizontalGap = globalStyles.objectColumnGapPx ?? baseSpacing;
    const defaultVerticalSpacing = globalStyles.objectRowGapPx ?? 0;
    
    // Get spacing values from overrides or use defaults
    const horizontalGap = objectSpacing?.horizontalGap ?? defaultHorizontalGap;
    const verticalSpacing = objectSpacing?.verticalSpacing ?? defaultVerticalSpacing;
    const objectGap = objectSpacing?.objectGap ?? defaultHorizontalGap;

    const hasOverrides = Boolean(
        objectSpacing &&
        (objectSpacing.horizontalGap !== undefined ||
            objectSpacing.verticalSpacing !== undefined ||
            objectSpacing.objectGap !== undefined)
    );
    
    const handleHorizontalGapChange = (value: number) => {
        devLogger.info('fieldshell.properties.styling.changed', {
            componentId: 'current',
            section: 'spacing',
            property: 'horizontalGap',
            oldValue: horizontalGap,
            newValue: value,
            scope: 'component'
        });
        
        onPropsChange({
            objectSpacing: {
                ...objectSpacing,
                horizontalGap: value
            }
        });
    };
    
    const handleVerticalSpacingChange = (value: number) => {
        devLogger.info('fieldshell.properties.styling.changed', {
            componentId: 'current',
            section: 'spacing',
            property: 'verticalSpacing',
            oldValue: verticalSpacing,
            newValue: value,
            scope: 'component'
        });
        
        onPropsChange({
            objectSpacing: {
                ...objectSpacing,
                verticalSpacing: value
            }
        });
    };
    
    const handleObjectGapChange = (value: number) => {
        devLogger.info('fieldshell.properties.styling.changed', {
            componentId: 'current',
            section: 'spacing',
            property: 'objectGap',
            oldValue: objectGap,
            newValue: value,
            scope: 'component'
        });
        
        onPropsChange({
            objectSpacing: {
                ...objectSpacing,
                objectGap: value
            }
        });
    };
    
    return (
        <div className="space-y-3 pt-3 border-t border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-2">
                <Maximize2 size={14} className="text-purple-500" />
                <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    Spacing
                </h4>
                {hasOverrides && (
                    <button
                        type="button"
                        onClick={() => onPropsChange({ objectSpacing: undefined })}
                        className="ml-auto text-[10px] px-2 py-1 rounded border border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
                        title="Clear per-component spacing overrides and fall back to Global Styles defaults."
                    >
                        Reset to global
                    </button>
                )}
            </div>
            
            {/* Layout-aware spacing controls */}
            {currentLayout === 'horizontal' && (
                <div className="space-y-3">
                    <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
                        <ArrowLeftRight size={12} />
                        <span>Horizontal Gap (between objects in row)</span>
                    </div>
                    <PropertyNumberInput
                        label="Horizontal Gap"
                        value={horizontalGap}
                        onChange={handleHorizontalGapChange}
                        min={0}
                        max={100}
                        step={1}
                        unit="px"
                        helpText="Gap between objects in the same row"
                    />
                </div>
            )}
            
            {currentLayout === 'vertical' && (
                <div className="space-y-3">
                    <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
                        <ArrowUpDown size={12} />
                        <span>Vertical Spacing (between rows)</span>
                    </div>
                    <PropertyNumberInput
                        label="Vertical Spacing"
                        value={verticalSpacing}
                        onChange={handleVerticalSpacingChange}
                        min={0}
                        max={100}
                        step={1}
                        unit="px"
                        helpText="Spacing between vertically stacked objects"
                    />
                </div>
            )}
            
            {currentLayout === 'mixed' && (
                <div className="space-y-3">
                    <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
                        <ArrowLeftRight size={12} />
                        <span>Horizontal Gap (within rows)</span>
                    </div>
                    <PropertyNumberInput
                        label="Horizontal Gap"
                        value={horizontalGap}
                        onChange={handleHorizontalGapChange}
                        min={0}
                        max={100}
                        step={1}
                        unit="px"
                        helpText="Gap between objects in the same row"
                    />
                    
                    <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
                        <ArrowUpDown size={12} />
                        <span>Vertical Spacing (between rows)</span>
                    </div>
                    <PropertyNumberInput
                        label="Vertical Spacing"
                        value={verticalSpacing}
                        onChange={handleVerticalSpacingChange}
                        min={0}
                        max={100}
                        step={1}
                        unit="px"
                        helpText="Spacing between rows"
                    />
                </div>
            )}
            
            {/* Generic Object Gap (fallback) */}
            <div className="pt-2 border-t border-gray-100 dark:border-gray-700">
                <PropertyNumberInput
                    label="Object Gap (fallback)"
                    value={objectGap}
                    onChange={handleObjectGapChange}
                    min={0}
                    max={100}
                    step={1}
                    unit="px"
                    helpText="Generic gap used when specific spacing not set"
                />
            </div>
            
            {/* Visual Gap Indicator */}
            <div className="pt-2">
                <div className="text-xs text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-800 p-2 rounded">
                    <div className="font-medium mb-1">Current Spacing:</div>
                    <div className="space-y-1">
                        {currentLayout === 'horizontal' && (
                            <div>Horizontal: {horizontalGap}px</div>
                        )}
                        {currentLayout === 'vertical' && (
                            <div>Vertical: {verticalSpacing}px</div>
                        )}
                        {currentLayout === 'mixed' && (
                            <>
                                <div>Horizontal: {horizontalGap}px</div>
                                <div>Vertical: {verticalSpacing}px</div>
                            </>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};



