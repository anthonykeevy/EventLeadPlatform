/**
 * Structure Validation Utilities
 * 
 * Validates component structure definitions to ensure they are well-formed.
 */

import { ComponentStructure, ComponentObject } from '../types/builder.types';

export interface StructureValidationResult {
    valid: boolean;
    errors: string[];
}

/**
 * Validate a component structure definition.
 * Checks for:
 * - Unique object IDs
 * - Valid layout group references
 * - Sequential order numbers
 * - Required objects present
 */
export function validateStructure(structure: ComponentStructure): StructureValidationResult {
    const errors: string[] = [];
    
    // Check objects array exists and is not empty
    if (!structure.objects || structure.objects.length === 0) {
        errors.push('Structure must have at least one object');
        return { valid: false, errors };
    }
    
    // Check for unique object IDs
    const objectIds = structure.objects.map(obj => obj.id);
    const uniqueIds = new Set(objectIds);
    if (objectIds.length !== uniqueIds.size) {
        const duplicates = objectIds.filter((id, index) => objectIds.indexOf(id) !== index);
        errors.push(`Duplicate object IDs found: ${Array.from(new Set(duplicates)).join(', ')}`);
    }
    
    // Check order numbers are sequential starting from 1
    const orders = structure.objects.map(obj => obj.order).sort((a, b) => a - b);
    for (let i = 0; i < orders.length; i++) {
        if (orders[i] !== i + 1) {
            errors.push(`Order numbers must be sequential starting from 1. Found: ${orders.join(', ')}`);
            break;
        }
    }
    
    // Validate layoutGroups if present
    if (structure.layoutGroups) {
        const allObjectIds = new Set(objectIds);
        const groupObjectIds = new Set<string>();
        
        // Collect all object IDs referenced in groups
        Object.values(structure.layoutGroups).forEach(group => {
            if (!Array.isArray(group)) {
                errors.push(`Layout groups must be arrays of object IDs`);
                return;
            }
            group.forEach(objId => {
                groupObjectIds.add(objId);
                if (!allObjectIds.has(objId)) {
                    errors.push(`Layout group references non-existent object ID: ${objId}`);
                }
            });
        });
        
        // Check that all objects are included in groups (for mixed layout)
        if (structure.defaultLayout === 'mixed') {
            const missingObjects = objectIds.filter(id => !groupObjectIds.has(id));
            if (missingObjects.length > 0) {
                errors.push(`Mixed layout requires all objects to be in layoutGroups. Missing: ${missingObjects.join(', ')}`);
            }
        }
    } else if (structure.defaultLayout === 'mixed') {
        errors.push('Mixed layout requires layoutGroups to be defined');
    }
    
    // Validate each object
    structure.objects.forEach((obj, index) => {
        if (!obj.id || obj.id.trim() === '') {
            errors.push(`Object at index ${index} has empty or missing ID`);
        }
        if (!obj.type) {
            errors.push(`Object '${obj.id}' has missing type`);
        }
        if (obj.order < 1) {
            errors.push(`Object '${obj.id}' has invalid order: ${obj.order} (must be >= 1)`);
        }
    });
    
    return {
        valid: errors.length === 0,
        errors
    };
}

/**
 * Validate a single component object.
 */
export function validateComponentObject(obj: ComponentObject, _allObjectIds: string[]): StructureValidationResult {
    const errors: string[] = [];
    
    if (!obj.id || obj.id.trim() === '') {
        errors.push('Object ID is required');
    }
    
    if (!obj.type) {
        errors.push(`Object '${obj.id}' has missing type`);
    }
    
    if (obj.order < 1) {
        errors.push(`Object '${obj.id}' has invalid order: ${obj.order} (must be >= 1)`);
    }
    
    if (obj.conditional && !obj.conditional.type) {
        errors.push(`Object '${obj.id}' has conditional rule without type`);
    }
    
    return {
        valid: errors.length === 0,
        errors
    };
}



