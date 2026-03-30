import type { ComponentType } from '../types/builder.types';

/**
 * Central place to declare which features each component supports.
 *
 * Why:
 * - Prevents feature logic being scattered across many renderers/panels.
 * - Makes it explicit when a component intentionally deviates from defaults.
 */
export interface ComponentCapabilities {
  /** Shows Object Layout section + supports objectLayout/layoutGroups editing */
  supportsObjectLayout: boolean;
  /** Shows TextLengthIndicator (builder visual guide) */
  supportsTextLengthIndicator: boolean;
  /** Shows Export Name field in Properties Panel (for data collection) */
  supportsExportName: boolean;
  /** Shows Tab Order field in Properties Panel (for keyboard navigation) */
  supportsTabOrder: boolean;
  /** Shows Initial State controls (visibility/enabled) in Properties Panel */
  supportsInitialState: boolean;
}

/**
 * Default capabilities for data-collecting input components
 */
const INPUT_CAPABILITIES: ComponentCapabilities = {
  supportsObjectLayout: true,
  supportsTextLengthIndicator: false,
  supportsExportName: true,
  supportsTabOrder: true,
  supportsInitialState: true,
};

/**
 * Capabilities for text-based input components (adds TextLengthIndicator)
 */
const TEXT_INPUT_CAPABILITIES: ComponentCapabilities = {
  ...INPUT_CAPABILITIES,
  supportsTextLengthIndicator: true,
};

/**
 * Capabilities for non-data components (divider, header)
 */
const NON_DATA_CAPABILITIES: ComponentCapabilities = {
  supportsObjectLayout: false,
  supportsTextLengthIndicator: false,
  supportsExportName: false,
  supportsTabOrder: false,
  supportsInitialState: false,
};

/**
 * Capabilities for action components (submit button)
 */
const ACTION_CAPABILITIES: ComponentCapabilities = {
  supportsObjectLayout: true,
  supportsTextLengthIndicator: false,
  supportsExportName: false,
  supportsTabOrder: false,
  supportsInitialState: false,
};

export function getComponentCapabilities(type: ComponentType): ComponentCapabilities {
  switch (type) {
    case 'divider':
    case 'header':
    case 'paragraph':
      return NON_DATA_CAPABILITIES;
    case 'submit-button':
      return ACTION_CAPABILITIES;
    case 'checkbox':
    case 'radio':
    case 'dropdown':
    case 'date':
    case 'number':
    case 'phone':
    case 'terms':
      return INPUT_CAPABILITIES;
    case 'first-name':
    case 'email':
    case 'url':
    case 'address':
    case 'text':
    case 'textarea':
      return TEXT_INPUT_CAPABILITIES;
    default:
      return INPUT_CAPABILITIES;
  }
}

