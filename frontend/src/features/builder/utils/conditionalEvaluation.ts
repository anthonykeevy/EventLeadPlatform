/**
 * Conditional Evaluation Utilities
 * 
 * Utilities for evaluating conditional rules to determine object visibility.
 */

import { ConditionalRule, ConditionalContext, ComponentObject } from '../types/builder.types';

/**
 * Evaluate a single conditional rule against a context.
 * Returns true if the object should be visible.
 */
export function evaluateConditionalRule(
    rule: ConditionalRule,
    context: ConditionalContext
): boolean {
    switch (rule.type) {
        case 'always':
            return true;
            
        case 'prop':
            if (!rule.prop) {
                return true; // No prop specified, show by default
            }
            // Check if property exists and is truthy
            const propValue = context.componentProps[rule.prop];
            return Boolean(propValue);
            
        case 'state':
            // In builder mode, always show state-based objects so SmartBorder accounts for their space
            if (context.builderMode) {
                return true;
            }
            if (rule.condition) {
                // Use custom condition function
                return rule.condition(context);
            }
            // No condition function, show by default
            return true;
            
        case 'validation':
            // In builder mode, always show validation objects so SmartBorder accounts for their space
            if (context.builderMode) {
                return true;
            }
            // Show if there are validation errors
            // Check multiple sources: direct error prop, validationErrors map, or allFormErrors map
            const hasDirectError = Boolean(context.error);
            const hasErrors = context.validationErrors && Object.keys(context.validationErrors).length > 0;
            const hasFormErrors = context.allFormErrors && Object.keys(context.allFormErrors).length > 0;
            return hasDirectError || hasErrors || hasFormErrors;
            
        default:
            // Unknown rule type, show by default for safety
            return true;
    }
}

/**
 * Filter objects based on conditional rules.
 * Returns only objects that should be visible given the current context.
 */
export function filterConditionalObjects(
    objects: ComponentObject[],
    context: ConditionalContext
): ComponentObject[] {
    return objects.filter(obj => {
        // Required objects always show
        if (obj.required) {
            return true;
        }
        
        // Objects without conditional rules always show
        if (!obj.conditional) {
            return true;
        }
        
        // Evaluate conditional rule
        return evaluateConditionalRule(obj.conditional, context);
    });
}

/**
 * Check if an object should be visible in the Properties Panel.
 * Uses progressive disclosure: only show if condition is met OR showInProperties is false.
 */
export function shouldShowInProperties(
    obj: ComponentObject,
    context: ConditionalContext
): boolean {
    // Required objects always show
    if (obj.required) {
        return true;
    }
    
    // Objects without conditional rules always show
    if (!obj.conditional) {
        return true;
    }
    
    // If showInProperties is false, hide from properties panel (but may show at runtime)
    if (obj.conditional.showInProperties === false) {
        return false;
    }
    
    // Evaluate conditional rule
    return evaluateConditionalRule(obj.conditional, context);
}



