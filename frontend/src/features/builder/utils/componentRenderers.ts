/**
 * Component Renderer Utilities
 * 
 * Utilities to create renderers for components based on their structure.
 */

import React from 'react';
import { ComponentType, ComponentStructure, FormComponent } from '../types/builder.types';
import { ObjectRenderers, getDefaultRenderers, createLabelRenderer, createInputRenderer, createValidationRenderer, createActionRenderer, createStatusRenderer, createDividerRenderer } from './objectRenderers';

/**
 * Get renderers for a component based on its structure.
 * Creates renderers for each object in the structure.
 */
export function getRenderersForComponent(
    componentType: ComponentType,
    structure: ComponentStructure,
    component?: FormComponent
): ObjectRenderers {
    const defaultRenderers = getDefaultRenderers();
    const renderers: ObjectRenderers = {};
    
    // Create renderers for each object in the structure
    for (const obj of structure.objects) {
        switch (obj.type) {
            case 'label':
                renderers[obj.id] = createLabelRenderer();
                break;
            case 'input':
                renderers[obj.id] = createInputRenderer();
                break;
            case 'validation':
                renderers[obj.id] = createValidationRenderer();
                break;
            case 'action':
                renderers[obj.id] = createActionRenderer();
                break;
            case 'status':
                renderers[obj.id] = createStatusRenderer();
                break;
            case 'divider':
                renderers[obj.id] = createDividerRenderer();
                break;
            case 'custom':
                // For custom types, try to use default renderer or create a basic one
                if (defaultRenderers[obj.id]) {
                    renderers[obj.id] = defaultRenderers[obj.id];
                } else {
                    // Fallback: create a simple div renderer
                    renderers[obj.id] = () => React.createElement('div', null, `Custom: ${obj.id}`);
                }
                break;
            default:
                // Fallback to default renderer if available
                if (defaultRenderers[obj.id]) {
                    renderers[obj.id] = defaultRenderers[obj.id];
                } else {
                    console.warn(`No renderer found for object type: ${obj.type}, id: ${obj.id}`);
                }
        }
    }
    
    return renderers;
}

/**
 * Get runtime renderers for a component.
 * Similar to getRenderersForComponent but includes form state handlers.
 */
export function getRuntimeRenderers(
    componentType: ComponentType,
    structure: ComponentStructure,
    handlers: {
        value?: unknown;
        onChange?: (value: unknown) => void;
        disabled?: boolean;
        required?: boolean;
        error?: string;
        buttonText?: string;
        onClick?: () => void;
        isLoading?: boolean;
        validationErrors?: Record<string, string>;
        allFormErrors?: Record<string, string>;
    }
): ObjectRenderers {
    const renderers = getRenderersForComponent(componentType, structure);
    
    // Enhance renderers with runtime handlers
    // This is a simplified version - in practice, you'd wrap each renderer
    // to inject the handlers
    
    return renderers;
}



