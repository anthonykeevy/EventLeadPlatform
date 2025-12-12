/**
 * Export Service - Story 3.5
 * 
 * Handles the export schema generation and field mapping for forms.
 * Ensures consistent data export regardless of which device layout was used.
 */

import { FormComponent, FormDefinition, FormPage, ExportMode, AddressExportMapping } from '../types/builder.types';

/**
 * Field export configuration derived from component
 */
export interface FieldExportConfig {
    fieldId: string;
    exportName: string;
    type: string;
    required: boolean;
    exportMode?: ExportMode;
    validation?: {
        minLength?: number;
        maxLength?: number;
        pattern?: string;
    };
}

/**
 * Address export field mappings
 */
export interface AddressExportFields {
    fullAddress: string;
    streetNumber?: string;
    streetName?: string;
    unit?: string;
    suburb?: string;
    state?: string;
    postcode?: string;
    country?: string;
}

/**
 * Complete form export schema
 */
export interface FormExportSchema {
    formId: string;
    version: string;
    generatedAt: string;
    fields: FieldExportConfig[];
    deviceLayouts: {
        desktop: boolean;
        tablet: boolean;
        mobile: boolean;
    };
}

/**
 * Generate an export name from a label
 * Converts to camelCase with only alphanumeric characters
 */
export function labelToExportName(label: string): string {
    if (!label) return 'field';
    
    return label
        .toLowerCase()
        // Remove non-alphanumeric except spaces
        .replace(/[^a-zA-Z0-9\s]/g, '')
        // Split on spaces
        .split(/\s+/)
        // Convert to camelCase
        .map((word, index) => 
            index === 0 ? word : word.charAt(0).toUpperCase() + word.slice(1)
        )
        .join('')
        // Ensure starts with letter
        .replace(/^[0-9]/, '_$&');
}

/**
 * Validate export name format
 * Must be alphanumeric with underscores, starting with letter or underscore
 */
export function isValidExportName(name: string): boolean {
    return /^[a-zA-Z_][a-zA-Z0-9_]*$/.test(name);
}

/**
 * Extract field export config from a component
 */
export function extractFieldConfig(component: FormComponent): FieldExportConfig | null {
    // Skip non-input components
    const nonInputTypes = ['header', 'paragraph', 'divider'];
    if (nonInputTypes.includes(component.type)) {
        return null;
    }

    // Skip submit button (action, not data)
    if (component.type === 'submit-button') {
        return null;
    }

    // Determine export name
    const exportName = component.props.exportName || 
        labelToExportName(component.props.label || component.type);

    return {
        fieldId: component.id,
        exportName,
        type: component.type,
        required: component.props.required || false,
        exportMode: component.props.exportMode,
        validation: component.props.validation ? {
            minLength: component.props.validation.minLength,
            maxLength: component.props.validation.maxLength,
            pattern: component.props.validation.pattern,
        } : undefined,
    };
}

/**
 * Collect all field configs from a page
 */
export function collectPageFields(page: FormPage): FieldExportConfig[] {
    const fields: FieldExportConfig[] = [];
    
    for (const component of page.components) {
        const config = extractFieldConfig(component);
        if (config) {
            fields.push(config);
        }
        
        // Handle nested components
        if (component.children) {
            for (const child of component.children) {
                const childConfig = extractFieldConfig(child);
                if (childConfig) {
                    fields.push(childConfig);
                }
            }
        }
    }
    
    return fields;
}

/**
 * Generate complete export schema for a form
 * Validates that all device layouts export the same fields
 */
export function generateExportSchema(formDef: FormDefinition): FormExportSchema {
    // Collect fields from primary layout (prefer desktop, then tablet, then mobile)
    const primaryPages = formDef.desktopPages || formDef.tabletPages || formDef.mobilePages || formDef.pages;
    
    const allFields: FieldExportConfig[] = [];
    for (const page of primaryPages) {
        allFields.push(...collectPageFields(page));
    }
    
    // Deduplicate by exportName (in case same field is on multiple pages)
    const fieldMap = new Map<string, FieldExportConfig>();
    for (const field of allFields) {
        if (!fieldMap.has(field.exportName)) {
            fieldMap.set(field.exportName, field);
        }
    }
    
    return {
        formId: formDef.formId,
        version: formDef.schemaVersion,
        generatedAt: new Date().toISOString(),
        fields: Array.from(fieldMap.values()),
        deviceLayouts: {
            desktop: !!(formDef.desktopPages && formDef.desktopPages.length > 0),
            tablet: !!(formDef.tabletPages && formDef.tabletPages.length > 0),
            mobile: !!(formDef.mobilePages && formDef.mobilePages.length > 0),
        },
    };
}

/**
 * Validate that field export names are unique within a form
 * Returns array of duplicate field names
 */
export function findDuplicateExportNames(formDef: FormDefinition): string[] {
    const schema = generateExportSchema(formDef);
    const seen = new Set<string>();
    const duplicates: string[] = [];
    
    for (const field of schema.fields) {
        if (seen.has(field.exportName)) {
            duplicates.push(field.exportName);
        } else {
            seen.add(field.exportName);
        }
    }
    
    return duplicates;
}

/**
 * Generate address field mappings
 */
export function getAddressExportFields(
    baseExportName: string,
    decompose: boolean,
    customMapping?: AddressExportMapping
): AddressExportFields {
    if (!decompose) {
        return { fullAddress: baseExportName };
    }
    
    // Default decomposition mapping
    const defaultMapping: AddressExportFields = {
        fullAddress: `${baseExportName}_full`,
        streetNumber: `${baseExportName}_streetNumber`,
        streetName: `${baseExportName}_streetName`,
        unit: `${baseExportName}_unit`,
        suburb: `${baseExportName}_suburb`,
        state: `${baseExportName}_state`,
        postcode: `${baseExportName}_postcode`,
        country: `${baseExportName}_country`,
    };
    
    // Apply custom mappings if provided
    if (customMapping) {
        return {
            fullAddress: defaultMapping.fullAddress,
            streetNumber: customMapping.streetNumber || defaultMapping.streetNumber,
            streetName: customMapping.streetName || defaultMapping.streetName,
            unit: customMapping.unit || defaultMapping.unit,
            suburb: customMapping.suburb || defaultMapping.suburb,
            state: customMapping.state || defaultMapping.state,
            postcode: customMapping.postcode || defaultMapping.postcode,
            country: customMapping.country || defaultMapping.country,
        };
    }
    
    return defaultMapping;
}

/**
 * Serialize export schema to JSON for API/storage
 */
export function serializeExportSchema(schema: FormExportSchema): string {
    return JSON.stringify(schema, null, 2);
}

