/**
 * Default Structure Generator
 * 
 * Generates default component structures for components without explicit definitions.
 * Ensures backward compatibility during migration.
 */

import { ComponentType, ComponentStructure } from '../types/builder.types';

/**
 * Generate default structure for a component type.
 * Returns a basic structure based on component type patterns.
 */
export function getDefaultStructure(componentType: ComponentType): ComponentStructure {
    // Input field components (text, email, phone, etc.)
    if (isInputFieldType(componentType)) {
        return {
            objects: [
                { id: 'label', type: 'label', required: true, order: 1 },
                { id: 'input', type: 'input', required: true, order: 2 },
                { id: 'validation', type: 'validation', required: false, order: 3, conditional: { type: 'validation' } }
            ],
            defaultLayout: 'vertical'
        };
    }
    
    // Button/action components
    if (componentType === 'submit-button') {
        return {
            objects: [
                { id: 'button', type: 'action', required: true, order: 1 },
                { id: 'loading', type: 'status', required: false, order: 2, conditional: { type: 'prop', prop: 'showLoadingState' } },
                { id: 'validation', type: 'validation', required: false, order: 3, conditional: { type: 'validation' } }
            ],
            defaultLayout: 'vertical'
        };
    }
    
    // Display components (header, divider)
    if (isDisplayType(componentType)) {
        return {
            objects: [
                { id: 'content', type: 'custom', required: true, order: 1, customType: componentType }
            ],
            defaultLayout: 'vertical'
        };
    }
    
    // Terms checkbox
    if (componentType === 'terms') {
        return {
            objects: [
                { id: 'checkbox', type: 'input', required: true, order: 1 },
                { id: 'label', type: 'label', required: true, order: 2 },
                { id: 'validation', type: 'validation', required: false, order: 3, conditional: { type: 'validation' } }
            ],
            defaultLayout: 'horizontal'
        };
    }
    
    // Default fallback: single object
    return {
        objects: [
            { id: 'content', type: 'input', required: true, order: 1 }
        ],
        defaultLayout: 'vertical'
    };
}

/**
 * Check if component type is an input field
 */
function isInputFieldType(type: ComponentType): boolean {
    return [
        'text',
        'number',
        'email',
        'phone',
        'url',
        'textarea',
        'dropdown',
        'radio',
        'checkbox',
        'date',
        'address',
        'rating',
        'file-upload',
        'first-name'
    ].includes(type);
}

/**
 * Check if component type is a display component
 */
function isDisplayType(type: ComponentType): boolean {
    return ['header', 'paragraph', 'divider'].includes(type);
}



