/**
 * TypographyColorsSection Component
 * 
 * Properties Panel section for configuring typography and colors per object type.
 * Shows collapsible sections for each object type (Label, Input, Validation, etc.)
 * with "Apply to All Components" functionality.
 */

import React from 'react';
import { Type, Tag, MessageSquare, Zap, Loader2, Palette, Wand2, Minus, type LucideIcon } from 'lucide-react';
import { ComponentStructure, StyleOverrides, GlobalStyles, ObjectType } from '../../types/builder.types';
import { TypographyCard } from './inputs';
import { devLogger } from '../../utils/devLogger';

interface TypographyColorsSectionProps {
    structure: ComponentStructure;
    globalStyles: GlobalStyles;
    styleOverrides?: StyleOverrides;
    onGlobalStylesChange: (updates: Partial<GlobalStyles>) => void;
    onStyleOverridesChange: (updates: Partial<StyleOverrides>) => void;
}

/**
 * Map object types to display labels and icons
 */
const OBJECT_TYPE_CONFIG: Record<ObjectType, { label: string; icon: LucideIcon; iconColor: string }> = {
    label: { label: 'Label Text', icon: Tag, iconColor: 'text-blue-500' },
    input: { label: 'Input Text', icon: Type, iconColor: 'text-green-500' },
    validation: { label: 'Help & Validation', icon: MessageSquare, iconColor: 'text-orange-500' },
    action: { label: 'Button Text', icon: Zap, iconColor: 'text-purple-500' },
    status: { label: 'Status Text', icon: Loader2, iconColor: 'text-gray-500' },
    divider: { label: 'Divider', icon: Minus, iconColor: 'text-gray-400' },
    custom: { label: 'Custom', icon: Type, iconColor: 'text-gray-500' },
};

/**
 * Map object types to StyleOverrides keys
 */
function getOverrideKeysForObjectType(objectType: ObjectType): {
    fontFamily: keyof StyleOverrides;
    fontSize: keyof StyleOverrides;
    fontWeight: keyof StyleOverrides;
    fontStyle: keyof StyleOverrides;
    color: keyof StyleOverrides;
    backgroundColor: keyof StyleOverrides;
    borderColor: keyof StyleOverrides;
    borderWidth: keyof StyleOverrides;
    borderRadius: keyof StyleOverrides;
} {
    switch (objectType) {
        case 'label':
            return {
                fontFamily: 'labelFontFamily',
                fontSize: 'labelFontSize',
                fontWeight: 'labelFontWeight',
                fontStyle: 'labelFontStyle',
                color: 'labelColor',
                backgroundColor: 'labelBackgroundColor',
                borderColor: 'labelBorderColor',
                borderWidth: 'labelBorderWidth',
                borderRadius: 'labelBorderRadius',
            };
        case 'input':
            return {
                fontFamily: 'fontFamily',
                fontSize: 'fontSize',
                fontWeight: 'fontWeight',
                fontStyle: 'fontStyle',
                color: 'textColor',
                backgroundColor: 'textBackgroundColor',
                borderColor: 'textBorderColor',
                borderWidth: 'textBorderWidth',
                borderRadius: 'textBorderRadius',
            };
        case 'validation':
            return {
                fontFamily: 'helpTextFontFamily',
                fontSize: 'helpTextFontSize',
                fontWeight: 'helpTextFontWeight',
                fontStyle: 'helpTextFontStyle',
                color: 'helpTextColor',
                backgroundColor: 'helpTextBackgroundColor',
                borderColor: 'helpTextBorderColor',
                borderWidth: 'helpTextBorderWidth',
                borderRadius: 'helpTextBorderRadius',
            };
        case 'action':
            // Button uses label styles
            return {
                fontFamily: 'labelFontFamily',
                fontSize: 'labelFontSize',
                fontWeight: 'labelFontWeight',
                fontStyle: 'labelFontStyle',
                color: 'labelColor',
                backgroundColor: 'labelBackgroundColor',
                borderColor: 'labelBorderColor',
                borderWidth: 'labelBorderWidth',
                borderRadius: 'labelBorderRadius',
            };
        case 'divider':
            return {
                fontFamily: 'fontFamily',
                fontSize: 'fontSize',
                fontWeight: 'fontWeight',
                fontStyle: 'fontStyle',
                color: 'dividerBorderColor',
                backgroundColor: 'backgroundColor',
                borderColor: 'dividerBorderColor',
                borderWidth: 'dividerBorderWidth',
                borderRadius: 'borderRadius',
            };
        default:
            // Fallback to input styles
            return {
                fontFamily: 'fontFamily',
                fontSize: 'fontSize',
                fontWeight: 'fontWeight',
                fontStyle: 'fontStyle',
                color: 'textColor',
                backgroundColor: 'textBackgroundColor',
                borderColor: 'textBorderColor',
                borderWidth: 'textBorderWidth',
                borderRadius: 'textBorderRadius',
            };
    }
}

/**
 * Map object types to GlobalStyles keys
 */
function getGlobalKeysForObjectType(objectType: ObjectType): {
    fontFamily: keyof GlobalStyles;
    fontSize: keyof GlobalStyles;
    fontWeight: keyof GlobalStyles;
    fontStyle: keyof GlobalStyles;
    color: keyof GlobalStyles;
    backgroundColor?: keyof GlobalStyles;
    borderColor?: keyof GlobalStyles;
    borderWidth?: keyof GlobalStyles;
    borderRadius?: keyof GlobalStyles;
} {
    switch (objectType) {
        case 'label':
            return {
                fontFamily: 'labelFontFamily',
                fontSize: 'labelFontSize',
                fontWeight: 'labelFontWeight',
                fontStyle: 'labelFontStyle',
                color: 'labelColor',
                backgroundColor: 'labelBackgroundColor',
                borderColor: 'labelBorderColor',
                borderWidth: 'labelBorderWidth',
                borderRadius: 'labelBorderRadius',
            };
        case 'input':
            return {
                fontFamily: 'fontFamily',
                fontSize: 'fontSize',
                fontWeight: 'fontWeight',
                fontStyle: 'fontStyle',
                color: 'textColor',
                backgroundColor: 'textBackgroundColor',
                borderColor: 'textBorderColor',
                borderWidth: 'textBorderWidth',
                borderRadius: 'textBorderRadius',
            };
        case 'validation':
            return {
                fontFamily: 'helpTextFontFamily',
                fontSize: 'helpTextFontSize',
                fontWeight: 'helpTextFontWeight',
                fontStyle: 'helpTextFontStyle',
                color: 'helpTextColor',
                backgroundColor: 'helpTextBackgroundColor',
                borderColor: 'helpTextBorderColor',
                borderWidth: 'helpTextBorderWidth',
                borderRadius: 'helpTextBorderRadius',
            };
        case 'action':
            return {
                fontFamily: 'labelFontFamily',
                fontSize: 'labelFontSize',
                fontWeight: 'labelFontWeight',
                fontStyle: 'labelFontStyle',
                color: 'labelColor',
                backgroundColor: 'labelBackgroundColor',
                borderColor: 'labelBorderColor',
                borderWidth: 'labelBorderWidth',
                borderRadius: 'labelBorderRadius',
            };
        case 'divider':
            return {
                fontFamily: 'fontFamily',
                fontSize: 'fontSize',
                fontWeight: 'fontWeight',
                fontStyle: 'fontStyle',
                color: 'dividerBorderColor',
                backgroundColor: 'backgroundColor',
                borderColor: 'dividerBorderColor',
                borderWidth: 'dividerBorderWidth',
                borderRadius: 'borderRadius',
            };
        default:
            return {
                fontFamily: 'fontFamily',
                fontSize: 'fontSize',
                fontWeight: 'fontWeight',
                fontStyle: 'fontStyle',
                color: 'textColor',
            };
    }
}

export const TypographyColorsSection: React.FC<TypographyColorsSectionProps> = ({
    structure,
    globalStyles,
    styleOverrides,
    onGlobalStylesChange,
    onStyleOverridesChange,
}) => {
    // Get unique object types from structure
    const objectTypes = Array.from(new Set(structure.objects.map(obj => obj.type)));
    
    // Helper to get effective value
    const getEffective = <K extends keyof StyleOverrides>(
        overrideKey: K,
        globalKey: keyof GlobalStyles
    ): any => {
        if (styleOverrides && overrideKey in styleOverrides) {
            return styleOverrides[overrideKey];
        }
        return globalStyles[globalKey];
    };
    
    // Handle "Apply to All" for a specific object type
    const handleApplyToAll = (objectType: ObjectType) => {
        const overrideKeys = getOverrideKeysForObjectType(objectType);
        const globalKeys = getGlobalKeysForObjectType(objectType);
        
        // Get current override values
        const currentOverrides: Partial<GlobalStyles> = {};
        if (styleOverrides) {
            Object.entries(overrideKeys).forEach(([prop, overrideKey]) => {
                if (overrideKey in styleOverrides) {
                    const globalKey = globalKeys[prop as keyof typeof globalKeys];
                    if (globalKey) {
                        currentOverrides[globalKey] = styleOverrides[overrideKey] as any;
                    }
                }
            });
        }
        
        // Apply to global styles
        if (Object.keys(currentOverrides).length > 0) {
            devLogger.info('fieldshell.properties.styling.changed', {
                componentId: 'global',
                section: 'typography',
                property: objectType,
                oldValue: globalStyles,
                newValue: { ...globalStyles, ...currentOverrides },
                scope: 'global'
            });
            
            onGlobalStylesChange(currentOverrides);
        }
    };
    
    return (
        <div className="space-y-3">
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <Palette size={14} className="text-purple-500" />
                    <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300">
                        Typography & Colors
                    </h4>
                </div>
            </div>
            
            {/* Render TypographyCard for each object type */}
            {objectTypes.map(objectType => {
                const config = OBJECT_TYPE_CONFIG[objectType] || OBJECT_TYPE_CONFIG.custom;
                const overrideKeys = getOverrideKeysForObjectType(objectType);
                const globalKeys = getGlobalKeysForObjectType(objectType);
                
                return (
                    <TypographyCard
                        key={objectType}
                        title={config.label}
                        icon={config.icon}
                        iconColor={config.iconColor}
                        fontFamily={getEffective(overrideKeys.fontFamily, globalKeys.fontFamily)}
                        fontSize={getEffective(overrideKeys.fontSize, globalKeys.fontSize)}
                        fontWeight={getEffective(overrideKeys.fontWeight, globalKeys.fontWeight)}
                        fontStyle={getEffective(overrideKeys.fontStyle, globalKeys.fontStyle)}
                        color={getEffective(overrideKeys.color, globalKeys.color)}
                        backgroundColor={globalKeys.backgroundColor != null ? getEffective(overrideKeys.backgroundColor, globalKeys.backgroundColor) : undefined}
                        borderColor={globalKeys.borderColor != null ? getEffective(overrideKeys.borderColor, globalKeys.borderColor) : undefined}
                        borderWidth={globalKeys.borderWidth != null ? getEffective(overrideKeys.borderWidth, globalKeys.borderWidth) : undefined}
                        borderRadius={globalKeys.borderRadius != null ? getEffective(overrideKeys.borderRadius, globalKeys.borderRadius) : undefined}
                        showBorderOptions={true}
                        onFontFamilyChange={(value) => {
                            onStyleOverridesChange({ [overrideKeys.fontFamily]: value } as Partial<StyleOverrides>);
                        }}
                        onFontSizeChange={(value) => {
                            onStyleOverridesChange({ [overrideKeys.fontSize]: value } as Partial<StyleOverrides>);
                        }}
                        onFontWeightChange={(value) => {
                            onStyleOverridesChange({ [overrideKeys.fontWeight]: value } as Partial<StyleOverrides>);
                        }}
                        onFontStyleChange={(value) => {
                            onStyleOverridesChange({ [overrideKeys.fontStyle]: value } as Partial<StyleOverrides>);
                        }}
                        onColorChange={(value) => {
                            onStyleOverridesChange({ [overrideKeys.color]: value } as Partial<StyleOverrides>);
                        }}
                        onBackgroundColorChange={(value) => {
                            onStyleOverridesChange({ [overrideKeys.backgroundColor]: value } as Partial<StyleOverrides>);
                        }}
                        onBorderColorChange={(value) => {
                            onStyleOverridesChange({ [overrideKeys.borderColor]: value } as Partial<StyleOverrides>);
                        }}
                        onBorderWidthChange={(value) => {
                            onStyleOverridesChange({ [overrideKeys.borderWidth]: value } as Partial<StyleOverrides>);
                        }}
                        onBorderRadiusChange={(value) => {
                            onStyleOverridesChange({ [overrideKeys.borderRadius]: value } as Partial<StyleOverrides>);
                        }}
                    />
                );
            })}
            
            {/* Apply to All Button */}
            {objectTypes.length > 0 && (
                <div className="pt-2 border-t border-gray-200 dark:border-gray-700">
                    <button
                        onClick={() => {
                            // Apply all current overrides to global
                            objectTypes.forEach(type => handleApplyToAll(type));
                        }}
                        className="w-full px-3 py-2 text-xs font-medium text-purple-600 dark:text-purple-400 bg-purple-50 dark:bg-purple-900/20 rounded hover:bg-purple-100 dark:hover:bg-purple-900/30 transition-colors flex items-center justify-center gap-2"
                    >
                        <Wand2 size={12} />
                        Apply to All Components
                    </button>
                </div>
            )}
        </div>
    );
};



