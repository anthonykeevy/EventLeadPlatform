import type { ComponentType } from '../types/builder.types';

/**
 * Component surface capabilities:
 * A single source of truth for how a component should behave/render on:
 * - toolbox (compact preview card)
 * - canvas  (builder WYSIWYG with builder aids)
 * - runtime (preview/production renderer)
 *
 * Goals:
 * - Make surface differences explicit and easy to edit
 * - Avoid scattered ad-hoc checks (e.g. previewContext === 'toolbox')
 * - Provide a stable "parity contract" for toolbox/canvas/runtime
 */

export type ComponentSurface = 'toolbox' | 'canvas' | 'runtime';

export type DropdownDisplayMode = 'placeholder' | 'longest-option' | 'selected-value';

export type DragConstraintMode = 'slide';
export type ResizeConstraintMode = 'autoAdjustSlide';

export interface ComponentSurfaceCapabilities {
  /** Design-time helper for text-based components */
  textLengthIndicator: {
    enabled: boolean;
    showBar: boolean;
    showLabel: boolean;
    /** Only relevant for textarea */
    showTextareaLineEstimate: boolean;
  };

  /**
   * Builder-only canvas drag constraints (applied while dragging).
   * Declared here so new components inherit sane defaults without scattered ad-hoc checks.
   */
  dragConstraints: {
    enabled: boolean;
    /** Prevent leaving the canvas bounds. */
    canvasBoundary: boolean;
    /** Prevent overlap with other components (uses SmartBorder bounds). */
    collisionAvoidance: boolean;
    /** How to respond when a constraint is hit. */
    mode: DragConstraintMode;
    boundaryPaddingPx: number;
    collisionPaddingPx: number;
  };

  /**
   * Builder-only resize/panel constraints (applied while previewing and on commit).
   * Policy: keep requested size, then auto-adjust position to avoid overlap; otherwise revert.
   */
  resizeConstraints: {
    enabled: boolean;
    canvasBoundary: boolean;
    collisionAvoidance: boolean;
    mode: ResizeConstraintMode;
    boundaryPaddingPx: number;
    collisionPaddingPx: number;
  };

  /** Dropdown-specific behavior differences */
  dropdown: {
    displayMode: DropdownDisplayMode;
  };

  /** Submit button behavior differences */
  submitButton: {
    /**
     * - never: never show status indicator (toolbox/canvas)
     * - while-submitting: show only during submit (runtime)
     */
    showStatus: 'never' | 'while-submitting';
    showIcon: boolean;
    /**
     * Builder-only (canvas). Runtime doesn't show resize handles; this flag is still useful
     * to keep a single place where "should be resizable" intent is declared.
     */
    allowResizeHandles: boolean;
  };

  /**
   * Builder-only object-level resize handles (canvas).
   * These are separate from the component-level SmartBorder resize handles.
   */
  objectResizeHandles: {
    /** Allow the input-object-only width handle (updates `ComponentProps.inputWidthOverride`). */
    inputWidthHandle: boolean;
  };

  /**
   * Surface-specific style application rules.
   * Ensures WYSIWYG parity between canvas and runtime.
   */
  surfaceStyles: {
    /** Apply component.props.width to container */
    applyComponentWidth: boolean;
    /** Apply component.props.buttonWidth/buttonAlign to action objects */
    applyButtonStyling: boolean;
    /** Apply component.props.labelWidthOverride to label objects */
    applyLabelWidth: boolean;
    /** Apply component.props.inputWidthOverride to input objects */
    applyInputWidthOverride: boolean;
  };

  /**
   * Drag preview configuration for this component on canvas.
   * Used by DragOverlay to render visual feedback during drag.
   */
  dragPreview: {
    /** Show visual preview during drag */
    enabled: boolean;
    /** Type of preview: 'snapshot' uses component visual, 'placeholder' uses simple shape */
    type: 'snapshot' | 'placeholder';
  };
}

type SurfaceOverride = Partial<{
  [K in keyof ComponentSurfaceCapabilities]: Partial<ComponentSurfaceCapabilities[K]>;
}>;

function mergeCaps(
  base: ComponentSurfaceCapabilities,
  override?: SurfaceOverride
): ComponentSurfaceCapabilities {
  if (!override) return base;
  return {
    textLengthIndicator: { ...base.textLengthIndicator, ...(override.textLengthIndicator ?? {}) },
    dragConstraints: { ...base.dragConstraints, ...(override.dragConstraints ?? {}) },
    resizeConstraints: { ...base.resizeConstraints, ...(override.resizeConstraints ?? {}) },
    dropdown: { ...base.dropdown, ...(override.dropdown ?? {}) },
    submitButton: { ...base.submitButton, ...(override.submitButton ?? {}) },
    objectResizeHandles: { ...base.objectResizeHandles, ...(override.objectResizeHandles ?? {}) },
    surfaceStyles: { ...base.surfaceStyles, ...(override.surfaceStyles ?? {}) },
    dragPreview: { ...base.dragPreview, ...(override.dragPreview ?? {}) },
  };
}

const BASE_BY_SURFACE: Record<ComponentSurface, ComponentSurfaceCapabilities> = {
  toolbox: {
    textLengthIndicator: {
      enabled: false,
      showBar: true,
      showLabel: true,
      showTextareaLineEstimate: false,
    },
    dragConstraints: {
      enabled: false,
      canvasBoundary: false,
      collisionAvoidance: false,
      mode: 'slide',
      boundaryPaddingPx: 0,
      collisionPaddingPx: 0,
    },
    resizeConstraints: {
      enabled: false,
      canvasBoundary: false,
      collisionAvoidance: false,
      mode: 'autoAdjustSlide',
      boundaryPaddingPx: 0,
      collisionPaddingPx: 0,
    },
    dropdown: {
      displayMode: 'placeholder',
    },
    submitButton: {
      showStatus: 'never',
      showIcon: true,
      allowResizeHandles: false,
    },
    objectResizeHandles: {
      inputWidthHandle: false,
    },
    // Toolbox uses compact rendering - doesn't apply component widths
    surfaceStyles: {
      applyComponentWidth: false,
      applyButtonStyling: true,
      applyLabelWidth: false,
      applyInputWidthOverride: false,
    },
    dragPreview: {
      enabled: true,
      type: 'snapshot',
    },
  },
  canvas: {
    textLengthIndicator: {
      enabled: false,
      showBar: true,
      showLabel: true,
      showTextareaLineEstimate: false,
    },
    dragConstraints: {
      enabled: true,
      canvasBoundary: true,
      collisionAvoidance: true,
      mode: 'slide',
      boundaryPaddingPx: 0,
      collisionPaddingPx: 0,
    },
    resizeConstraints: {
      enabled: true,
      canvasBoundary: true,
      collisionAvoidance: true,
      mode: 'autoAdjustSlide',
      boundaryPaddingPx: 0,
      collisionPaddingPx: 0,
    },
    dropdown: {
      // Canvas can use longest-option as a sizing guide.
      displayMode: 'longest-option',
    },
    submitButton: {
      showStatus: 'never',
      showIcon: true,
      allowResizeHandles: true,
    },
    objectResizeHandles: {
      inputWidthHandle: false,
    },
    // Canvas must match runtime for WYSIWYG parity
    surfaceStyles: {
      applyComponentWidth: true,
      applyButtonStyling: true,
      applyLabelWidth: true,
      applyInputWidthOverride: true,
    },
    dragPreview: {
      enabled: true,
      type: 'snapshot',
    },
  },
  runtime: {
    textLengthIndicator: {
      enabled: false,
      showBar: false,
      showLabel: false,
      showTextareaLineEstimate: false,
    },
    dragConstraints: {
      enabled: false,
      canvasBoundary: false,
      collisionAvoidance: false,
      mode: 'slide',
      boundaryPaddingPx: 0,
      collisionPaddingPx: 0,
    },
    resizeConstraints: {
      enabled: false,
      canvasBoundary: false,
      collisionAvoidance: false,
      mode: 'autoAdjustSlide',
      boundaryPaddingPx: 0,
      collisionPaddingPx: 0,
    },
    dropdown: {
      // Runtime should show placeholder unless user selected something.
      displayMode: 'placeholder',
    },
    submitButton: {
      showStatus: 'while-submitting',
      showIcon: true,
      allowResizeHandles: true,
    },
    objectResizeHandles: {
      inputWidthHandle: false,
    },
    // Runtime applies all styles for production rendering
    surfaceStyles: {
      applyComponentWidth: true,
      applyButtonStyling: true,
      applyLabelWidth: true,
      applyInputWidthOverride: true,
    },
    dragPreview: {
      enabled: false,
      type: 'snapshot',
    },
  },
};

/**
 * Per-component overrides.
 * Keep this “table” small and obvious: only override what differs from BASE.
 */
const OVERRIDES: Partial<Record<ComponentType, Partial<Record<ComponentSurface, SurfaceOverride>>>> = {
  // Text-length indicator components
  'first-name': {
    toolbox: { textLengthIndicator: { enabled: true, showBar: true, showLabel: true } },
    canvas: {
      textLengthIndicator: { enabled: true, showBar: true, showLabel: true },
      objectResizeHandles: { inputWidthHandle: true },
    },
  },
  text: {
    toolbox: { textLengthIndicator: { enabled: true, showBar: true, showLabel: true } },
    canvas: {
      textLengthIndicator: { enabled: true, showBar: true, showLabel: true },
      objectResizeHandles: { inputWidthHandle: true },
    },
  },
  email: {
    toolbox: { textLengthIndicator: { enabled: true, showBar: true, showLabel: true } },
    canvas: {
      textLengthIndicator: { enabled: true, showBar: true, showLabel: true },
      objectResizeHandles: { inputWidthHandle: true },
    },
  },
  url: {
    toolbox: { textLengthIndicator: { enabled: true, showBar: true, showLabel: true } },
    canvas: {
      textLengthIndicator: { enabled: true, showBar: true, showLabel: true },
      objectResizeHandles: { inputWidthHandle: true },
    },
  },
  address: {
    toolbox: { textLengthIndicator: { enabled: true, showBar: true, showLabel: true } },
    canvas: {
      textLengthIndicator: { enabled: true, showBar: true, showLabel: true },
      objectResizeHandles: { inputWidthHandle: true },
    },
  },
  textarea: {
    // Toolbox: suppress crowded guides
    toolbox: { textLengthIndicator: { enabled: false, showBar: false, showLabel: false, showTextareaLineEstimate: false } },
    // Canvas: show both the indicator and the line estimate
    canvas: {
      textLengthIndicator: { enabled: true, showBar: true, showLabel: true, showTextareaLineEstimate: true },
      objectResizeHandles: { inputWidthHandle: true },
    },
  },
  radio: {
    canvas: { textLengthIndicator: { enabled: true, showBar: true, showLabel: true } },
  },
  checkbox: {
    canvas: { textLengthIndicator: { enabled: true, showBar: true, showLabel: true } },
  },

  // Input-only resize handle (canvas) for text-like inputs
  phone: {
    canvas: { objectResizeHandles: { inputWidthHandle: true } },
  },
  number: {
    canvas: { objectResizeHandles: { inputWidthHandle: true } },
  },
  date: {
    canvas: { objectResizeHandles: { inputWidthHandle: true } },
  },

  // Dropdown behavior
  dropdown: {
    toolbox: { dropdown: { displayMode: 'placeholder' } },
    // Also enables canvas-only TextLengthIndicator for per-option extra text inputs (selection "extra text" pattern).
    canvas: {
      dropdown: { displayMode: 'longest-option' },
      objectResizeHandles: { inputWidthHandle: true },
      textLengthIndicator: { enabled: true, showBar: true, showLabel: true },
    },
    runtime: { dropdown: { displayMode: 'placeholder' } },
  },

  // Submit button behavior
  'submit-button': {
    toolbox: { submitButton: { showStatus: 'never', showIcon: true, allowResizeHandles: false } },
    canvas: { submitButton: { showStatus: 'never', showIcon: true, allowResizeHandles: true } },
    runtime: { submitButton: { showStatus: 'while-submitting', showIcon: true, allowResizeHandles: true } },
  },

  // Divider uses placeholder drag preview since it's just a line
  divider: {
    canvas: { dragPreview: { enabled: true, type: 'placeholder' } },
  },
};

export function getComponentSurfaceCapabilities(
  type: ComponentType,
  surface: ComponentSurface
): ComponentSurfaceCapabilities {
  const base = BASE_BY_SURFACE[surface];
  const override = OVERRIDES[type]?.[surface];
  return mergeCaps(base, override);
}

