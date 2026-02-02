import React, { useRef, useState, useEffect } from 'react';
import { 
  Type, 
  Hash, 
  AlignLeft, 
  Box, 
  CheckSquare, 
  List, 
  Calendar, 
  Heading, 
  User,
  Phone,
  MapPin,
  FileCheck,
  Send,
  Minus,
  Loader2,
} from 'lucide-react';
import { ComponentType, FormComponent, StyleOverrides, GlobalStyles, LayoutType, ComponentStructure } from '../types/builder.types';
import { getDefaultStructure } from '../utils/structureDefaults';
import { UniversalFieldShell } from '../components/UniversalFieldShell';
import { getRenderersForComponent } from '../utils/componentRenderers';
import { ObjectRenderers } from '../utils/objectRenderers';

// ---------- Toolbox preview helpers (no hooks) ----------
const FIRST_NAME_STRUCTURE: ComponentStructure = {
  objects: [
    { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
    { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2, features: { textLengthIndicator: {} } },
    { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } },
  ],
  defaultLayout: 'vertical',
  defaultRowAlignment: 'center',
};

const TOOLBOX_FIRST_NAME_COMPONENT: FormComponent = {
  id: 'toolbox-first-name',
  type: 'first-name',
  props: {
    label: 'First Name',
    placeholder: 'Enter your first name',
    required: true,
    validation: { maxLength: 30 },
  },
};

const TOOLBOX_FIRST_NAME_RENDERERS = getRenderersForComponent(
  'first-name',
  FIRST_NAME_STRUCTURE,
  TOOLBOX_FIRST_NAME_COMPONENT
);

interface ToolboxPreviewProps {
  globalStyles?: GlobalStyles;
}

function makeToolboxPreview(args: {
  type: ComponentType;
  structure: ComponentStructure;
  props: FormComponent['props'];
  renderersOverride?: (base: ObjectRenderers) => ObjectRenderers;
}): React.ReactNode {
  const ToolboxPreview: React.FC<ToolboxPreviewProps> = ({ globalStyles }) => {
    const component: FormComponent = {
      id: `toolbox-${args.type}`,
      type: args.type,
      props: {
        ...(args.props ?? {}),
      },
    };
    const baseRenderers = getRenderersForComponent(args.type, args.structure, component);
    const renderers = args.renderersOverride ? args.renderersOverride(baseRenderers) : baseRenderers;

    return (
      <UniversalFieldShell
        structure={args.structure}
        renderers={renderers}
        surface="toolbox"
        componentId={component.id}
        component={component}
        globalStyles={globalStyles}
        objectLayout={globalStyles?.defaultObjectLayout}
        layoutGroups={globalStyles?.defaultLayoutGroups}
        // Enable builder-mode branches (placeholder validation, sizing guides) AND show SmartBorder
        // so toolbox previews match canvas behavior.
        builderMode={{ showBorder: true, borderPadding: 5 }}
      />
    );
  };

  return <ToolboxPreview />;
}

export interface RuntimeComponentProps {
  component: FormComponent;
  value: unknown;
  onChange: (value: unknown) => void;
  disabled: boolean;
  required: boolean;
  error?: string;
  /** For submit buttons: all form validation errors */
  allFormErrors?: Record<string, string>;
  /** For submit buttons: structured validation context with priority sorting */
  formValidationContext?: {
    errors: Record<string, string>;
    errorsByPriority: Array<{ componentId: string; error: string; tabOrder: number; label: string }>;
    firstError?: string;
    errorCount: number;
  };
  /** For submit buttons / validation triggers */
  onSubmit?: () => void;
  /** Tab order index for keyboard navigation */
  tabIndex?: number;
  /** Primary color for focus styling */
  primaryColor?: string;
  /** Ref for initial focus (tabOrder: 1) */
  inputRef?: React.RefObject<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>;
  /** Component-level style overrides */
  styleOverrides?: StyleOverrides;
  /** Global styles (fallback when styleOverrides not set) */
  globalStyles?: GlobalStyles;
  /** Layout orientation */
  layout?: LayoutType;
}

export interface ComponentDefinition {
  type: ComponentType;
  label: string;
  icon: React.ReactNode;
  category: 'layout' | 'input' | 'display';
  defaultProps: Record<string, any>;
  defaultChildren?: FormComponent[];
  previewComponent?: React.ReactNode; 
  runtimeComponent?: React.FC<RuntimeComponentProps>;
  
  // NEW: Component structure definition
  structure: ComponentStructure;
  
  // NEW: For custom components stored in database
  isCustom?: boolean;
  customComponentId?: string; // Reference to database record
}

export const ComponentRegistry: Record<ComponentType, ComponentDefinition> = {
  // POC: First Name
  'first-name': {
    type: 'first-name',
    label: 'First Name',
    icon: <User size={18} />,
    category: 'input',
    defaultProps: {
      label: 'First Name',
      placeholder: 'Enter your first name',
      required: true,
      validation: { maxLength: 30 },
    },
    structure: FIRST_NAME_STRUCTURE,
    previewComponent: makeToolboxPreview({
      type: 'first-name',
      structure: FIRST_NAME_STRUCTURE,
      props: TOOLBOX_FIRST_NAME_COMPONENT.props,
    }),
    runtimeComponent: ({ component, value, onChange, disabled, required, error, tabIndex, primaryColor, inputRef, styleOverrides, globalStyles }) => {
      const structure = ComponentRegistry[component.type].structure || getDefaultStructure(component.type);
      const renderers = getRenderersForComponent(component.type, structure, component);
      const valueStr = (value as string) ?? '';

      return (
        <UniversalFieldShell
          structure={structure}
          renderers={renderers}
          surface="runtime"
          objectLayout={component.props.objectLayout}
          layoutGroups={component.props.layoutGroups}
          styleOverrides={styleOverrides}
          globalStyles={globalStyles}
          componentId={component.id}
          component={component}
          runtimeMode={{
            value: valueStr,
            onChange,
            disabled,
            required,
            error,
            primaryColor,
            tabIndex,
            inputRef,
          }}
        />
      );
    },
  },

  // Standard Inputs - Now using Gold Standard visual
  text: {
    type: 'text',
    label: 'Text Input',
    icon: <Type size={18} />,
    category: 'input',
    defaultProps: {
      label: 'Text Field',
      placeholder: 'Enter text...',
      required: false,
      validation: { maxLength: 50 },
    },
    structure: {
      objects: [
        { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
        { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2, features: { textLengthIndicator: {} } },
        { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } }
      ],
      defaultLayout: 'vertical'
    },
    previewComponent: makeToolboxPreview({
      type: 'text',
      structure: {
        objects: [
          { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
          { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2, features: { textLengthIndicator: {} } },
          { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } },
        ],
        defaultLayout: 'vertical',
      },
      props: {
        label: 'Text Field',
        placeholder: 'Enter text...',
        required: false,
        validation: { maxLength: 50 },
      },
    }),
    runtimeComponent: ({ component, value, onChange, disabled, required, error, tabIndex, primaryColor, inputRef, styleOverrides, globalStyles }) => {
      const structure = ComponentRegistry[component.type].structure || getDefaultStructure(component.type);
      const renderers = getRenderersForComponent(component.type, structure, component);
      const valueStr = (value as string) ?? ''
      
      return (
        <UniversalFieldShell
          structure={structure}
          renderers={renderers}
          surface="runtime"
          objectLayout={component.props.objectLayout}
          layoutGroups={component.props.layoutGroups}
          styleOverrides={styleOverrides}
          globalStyles={globalStyles}
          componentId={component.id}
          component={component}
          runtimeMode={{
            value: valueStr,
            onChange,
            disabled,
            required,
            error,
            primaryColor,
            tabIndex,
            inputRef,
          }}
        />
      )
    },
  },
  number: {
    type: 'number',
    label: 'Number',
    icon: <Hash size={18} />,
    category: 'input',
    defaultProps: {
      label: 'Number Field',
      placeholder: '0',
      required: false,
      validation: { maxLength: 12 },
    },
    structure: {
      objects: [
        { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
        { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2 },
        { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } }
      ],
      defaultLayout: 'vertical'
    },
    previewComponent: makeToolboxPreview({
      type: 'number',
      structure: {
        objects: [
          { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
          { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2 },
          { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } },
        ],
        defaultLayout: 'vertical',
      },
      props: {
        label: 'Number Field',
        placeholder: '0',
        required: false,
        validation: { maxLength: 12 },
      },
    }),
    runtimeComponent: ({ component, value, onChange, disabled, required, error, tabIndex, primaryColor, inputRef, styleOverrides, globalStyles }) => {
      const structure = ComponentRegistry[component.type].structure || getDefaultStructure(component.type);
      const renderers = getRenderersForComponent(component.type, structure, component);
      const valueStr = String(value ?? '')
      
      return (
        <UniversalFieldShell
          structure={structure}
          renderers={renderers}
          surface="runtime"
          objectLayout={component.props.objectLayout}
          layoutGroups={component.props.layoutGroups}
          styleOverrides={styleOverrides}
          globalStyles={globalStyles}
          componentId={component.id}
          component={component}
          runtimeMode={{
            value: valueStr,
            onChange,
            disabled,
            required,
            error,
            primaryColor,
            tabIndex,
            inputRef,
          }}
        />
      )
    },
  },
  email: {
    type: 'email',
    label: 'Email',
    icon: <Box size={18} />,
    category: 'input',
    defaultProps: {
      label: 'Email Address',
      placeholder: 'example@email.com',
      required: false,
      validation: { maxLength: 254, email: true },
    },
    structure: {
      objects: [
        { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
        { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2, features: { textLengthIndicator: {} } },
        { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } }
      ],
      defaultLayout: 'vertical'
    },
    previewComponent: makeToolboxPreview({
      type: 'email',
      structure: {
        objects: [
          { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
          { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2, features: { textLengthIndicator: {} } },
          { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } },
        ],
        defaultLayout: 'vertical',
      },
      props: {
        label: 'Email Address',
        placeholder: 'name@example.com',
        required: false,
        validation: { maxLength: 254, email: true },
      },
    }),
    runtimeComponent: ({ component, value, onChange, disabled, required, error, tabIndex, primaryColor, inputRef, styleOverrides, globalStyles }) => {
      const structure = ComponentRegistry[component.type].structure || getDefaultStructure(component.type);
      const renderers = getRenderersForComponent(component.type, structure, component);
      const valueStr = (value as string) ?? ''
      
      return (
        <UniversalFieldShell
          structure={structure}
          renderers={renderers}
          surface="runtime"
          objectLayout={component.props.objectLayout}
          layoutGroups={component.props.layoutGroups}
          styleOverrides={styleOverrides}
          globalStyles={globalStyles}
          componentId={component.id}
          component={component}
          runtimeMode={{
            value: valueStr,
            onChange,
            disabled,
            required,
            error,
            primaryColor,
            tabIndex,
            inputRef,
          }}
        />
      )
    },
  },
  textarea: {
    type: 'textarea',
    label: 'Text Area',
    icon: <AlignLeft size={18} />,
    category: 'input',
    defaultProps: {
      label: 'Long Text',
      placeholder: 'Enter details...',
      required: false,
      validation: { maxLength: 500 },
    },
    structure: {
      objects: [
        { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
        { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2, features: { textLengthIndicator: {} } },
        { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } }
      ],
      defaultLayout: 'vertical'
    },
    previewComponent: makeToolboxPreview({
      type: 'textarea',
      structure: {
        objects: [
          { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
          { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2 },
          { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } },
        ],
        defaultLayout: 'vertical',
      },
      props: {
        label: 'Long Text',
        placeholder: 'Enter details...',
        required: false,
        validation: { maxLength: 500 },
        // A reasonable tall default so toolbox previews resemble a textarea.
        styleOverrides: { inputHeight: 120 },
      },
    }),
    runtimeComponent: ({ component, value, onChange, disabled, required, error, tabIndex, primaryColor, inputRef, styleOverrides, globalStyles }) => {
      const structure = ComponentRegistry[component.type].structure || getDefaultStructure(component.type);
      const renderers = getRenderersForComponent(component.type, structure, component);
      const valueStr = (value as string) ?? ''
      
      return (
        <UniversalFieldShell
          structure={structure}
          renderers={renderers}
          surface="runtime"
          objectLayout={component.props.objectLayout}
          layoutGroups={component.props.layoutGroups}
          styleOverrides={styleOverrides}
          globalStyles={globalStyles}
          componentId={component.id}
          component={component}
          runtimeMode={{
            value: valueStr,
            onChange,
            disabled,
            required,
            error,
            primaryColor,
            tabIndex,
            inputRef,
          }}
        />
      )
    },
  },
  dropdown: {
    type: 'dropdown',
    label: 'Dropdown',
    icon: <List size={18} />,
    category: 'input',
    defaultProps: {
      label: 'Dropdown',
      placeholder: 'Select an option',
      options: [],
      required: false
    },
    structure: {
      objects: [
        { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
        { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2 },
        { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } }
      ],
      defaultLayout: 'vertical'
    },
    previewComponent: makeToolboxPreview({
      type: 'dropdown',
      structure: {
        objects: [
          { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
          { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2 },
          { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } },
        ],
        defaultLayout: 'vertical',
      },
      props: {
        label: 'Dropdown',
        placeholder: 'Select option',
        required: false,
        options: [
          { label: 'Option 1', value: 'option_1' },
          { label: 'Option 2', value: 'option_2' },
          { label: 'Option 3', value: 'option_3' },
        ],
      },
    }),
    runtimeComponent: ({ component, value, onChange, disabled, required, error, tabIndex, primaryColor, inputRef, styleOverrides, globalStyles }) => {
      const structure = ComponentRegistry[component.type].structure || getDefaultStructure(component.type);
      const renderers = getRenderersForComponent(component.type, structure, component);
      const valueStr = (value as string) ?? '';

      return (
        <UniversalFieldShell
          structure={structure}
          renderers={renderers}
          surface="runtime"
          objectLayout={component.props.objectLayout}
          layoutGroups={component.props.layoutGroups}
          styleOverrides={styleOverrides}
          globalStyles={globalStyles}
          componentId={component.id}
          component={component}
          runtimeMode={{
            value: valueStr,
            onChange,
            disabled,
            required,
            error,
            primaryColor,
            tabIndex,
            inputRef,
          }}
        />
      );
    },
  },
  date: {
    type: 'date',
    label: 'Date Picker',
    icon: <Calendar size={18} />,
    category: 'input',
    defaultProps: {
      label: 'Select Date',
      required: false
    },
    structure: {
      objects: [
        { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
        { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2 },
        { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } }
      ],
      defaultLayout: 'vertical'
    },
    previewComponent: makeToolboxPreview({
      type: 'date',
      structure: {
        objects: [
          { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
          { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2 },
          { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } },
        ],
        defaultLayout: 'vertical',
      },
      props: {
        label: 'Select Date',
        placeholder: 'DD/MM/YYYY',
        required: false,
      },
    }),
    runtimeComponent: ({ component, value, onChange, disabled, required, error, tabIndex, primaryColor, inputRef, styleOverrides, globalStyles }) => {
      const structure = ComponentRegistry[component.type].structure || getDefaultStructure(component.type);
      const renderers = getRenderersForComponent(component.type, structure, component);
      const valueStr = (value as string) ?? '';

      return (
        <UniversalFieldShell
          structure={structure}
          renderers={renderers}
          surface="runtime"
          objectLayout={component.props.objectLayout}
          layoutGroups={component.props.layoutGroups}
          styleOverrides={styleOverrides}
          globalStyles={globalStyles}
          componentId={component.id}
          component={component}
          runtimeMode={{
            value: valueStr,
            onChange,
            disabled,
            required,
            error,
            primaryColor,
            tabIndex,
            inputRef,
          }}
        />
      );
    },
  },

  checkbox: {
    type: 'checkbox',
    label: 'Checkbox',
    icon: <CheckSquare size={18} />,
    category: 'input',
    defaultProps: { label: 'Checkbox', required: false },
    structure: {
      objects: [
        // Keep canonical object order consistent across components: label → input → validation.
        // NOTE: Visual placement (e.g. checkbox control beside option labels) is handled inside the input renderer.
        { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
        { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2 },
        { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } }
      ],
      defaultLayout: 'horizontal',
      layoutGroups: { row1: ['input', 'label'], row2: ['validation'] },
      // Parity: align checkbox + label to top so SmartBorder stays level.
      defaultRowAlignment: 'top'
    },
    previewComponent: makeToolboxPreview({
      type: 'checkbox',
      structure: {
        objects: [
          { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
          { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2 },
          { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } },
        ],
        defaultLayout: 'horizontal',
        layoutGroups: { row1: ['input', 'label'], row2: ['validation'] },
        defaultRowAlignment: 'top',
      },
      props: {
        label: 'Checkbox',
        required: false,
        options: [
          { label: 'Option 1', value: 'option_1' },
          { label: 'Option 2', value: 'option_2' },
        ],
      },
    }),
    runtimeComponent: ({ component, value, onChange, disabled, required, error, tabIndex, primaryColor, inputRef, styleOverrides, globalStyles }) => {
      const structure = ComponentRegistry[component.type].structure || getDefaultStructure(component.type);
      const renderers = getRenderersForComponent(component.type, structure, component);

      return (
        <UniversalFieldShell
          structure={structure}
          renderers={renderers}
          surface="runtime"
          objectLayout={component.props.objectLayout}
          layoutGroups={component.props.layoutGroups}
          styleOverrides={styleOverrides}
          globalStyles={globalStyles}
          componentId={component.id}
          component={component}
          runtimeMode={{
            value,
            onChange,
            disabled,
            required,
            error,
            primaryColor,
            tabIndex,
            inputRef,
          }}
        />
      );
    },
  },
  radio: {
    type: 'radio',
    label: 'Radio',
    icon: <Box size={18} />,
    category: 'input',
    defaultProps: { label: 'Radio Group', required: false },
    structure: {
      objects: [
        { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
        { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2 },
        { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } }
      ],
      defaultLayout: 'vertical'
    },
    previewComponent: makeToolboxPreview({
      type: 'radio',
      structure: {
        objects: [
          { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
          { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2 },
          { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } },
        ],
        defaultLayout: 'vertical',
      },
      props: {
        label: 'Radio Group',
        required: false,
        options: [
          { label: 'Option 1', value: 'option_1' },
          { label: 'Option 2', value: 'option_2' },
        ],
      },
    }),
    runtimeComponent: ({ component, value, onChange, disabled, required, error, tabIndex, primaryColor, inputRef, styleOverrides, globalStyles }) => {
      const structure = ComponentRegistry[component.type].structure || getDefaultStructure(component.type);
      const renderers = getRenderersForComponent(component.type, structure, component);

      return (
        <UniversalFieldShell
          structure={structure}
          renderers={renderers}
          surface="runtime"
          objectLayout={component.props.objectLayout}
          layoutGroups={component.props.layoutGroups}
          styleOverrides={styleOverrides}
          globalStyles={globalStyles}
          componentId={component.id}
          component={component}
          runtimeMode={{
            value,
            onChange,
            disabled,
            required,
            error,
            primaryColor,
            tabIndex,
            inputRef,
          }}
        />
      );
    },
  },

  // Layout (Row/Column removed per user request)

  // Phone Input
  phone: {
    type: 'phone',
    label: 'Phone Number',
    icon: <Phone size={18} />,
    category: 'input',
    defaultProps: {
      label: 'Phone Number',
      placeholder: '+61 400 000 000',
      required: false,
      exportName: 'phone',
      validation: { maxLength: 20 },
    },
    structure: {
      objects: [
        { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
        { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2 },
        { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } }
      ],
      defaultLayout: 'vertical'
    },
    previewComponent: makeToolboxPreview({
      type: 'phone',
      structure: {
        objects: [
          { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
          { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2 },
          { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } },
        ],
        defaultLayout: 'vertical',
      },
      props: {
        label: 'Phone Number',
        placeholder: '+61 400 000 000',
        required: false,
        validation: { maxLength: 20 },
      },
    }),
    runtimeComponent: ({ component, value, onChange, disabled, required, error, tabIndex, primaryColor, inputRef, styleOverrides, globalStyles }) => {
      const structure = ComponentRegistry[component.type].structure || getDefaultStructure(component.type);
      const renderers = getRenderersForComponent(component.type, structure, component);
      const valueStr = (value as string) ?? ''
      
      return (
        <UniversalFieldShell
          structure={structure}
          renderers={renderers}
          surface="runtime"
          objectLayout={component.props.objectLayout}
          layoutGroups={component.props.layoutGroups}
          styleOverrides={styleOverrides}
          globalStyles={globalStyles}
          componentId={component.id}
          component={component}
          runtimeMode={{
            value: valueStr,
            onChange,
            disabled,
            required,
            error,
            primaryColor,
            tabIndex,
            inputRef,
          }}
        />
      )
    },
  },

  // Address Field (Placeholder for future autocomplete)
  address: {
    type: 'address',
    label: 'Address',
    icon: <MapPin size={18} />,
    category: 'input',
    defaultProps: {
      label: 'Address',
      placeholder: 'Start typing your address...',
      required: false,
      enableAutocomplete: true,
      exportName: 'address',
    },
    structure: {
      objects: [
        { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
        { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2, features: { textLengthIndicator: {} } },
        { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } }
      ],
      defaultLayout: 'vertical'
    },
    previewComponent: makeToolboxPreview({
      type: 'address',
      structure: {
        objects: [
          { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
          { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2, features: { textLengthIndicator: {} } },
          { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } },
        ],
        defaultLayout: 'vertical',
      },
      props: {
        label: 'Address',
        placeholder: 'Start typing your address...',
        required: false,
        enableAutocomplete: true,
        exportName: 'address',
        validation: { maxLength: 120 },
      },
    }),
    runtimeComponent: ({ component, value, onChange, disabled, required, error, tabIndex, primaryColor, inputRef, styleOverrides, globalStyles }) => {
      const structure = ComponentRegistry[component.type].structure || getDefaultStructure(component.type);
      const renderers = getRenderersForComponent(component.type, structure, component);
      const valueStr = (value as string) ?? '';

      return (
        <UniversalFieldShell
          structure={structure}
          renderers={renderers}
          surface="runtime"
          objectLayout={component.props.objectLayout}
          layoutGroups={component.props.layoutGroups}
          styleOverrides={styleOverrides}
          globalStyles={globalStyles}
          componentId={component.id}
          component={component}
          runtimeMode={{
            value: valueStr,
            onChange,
            disabled,
            required,
            error,
            primaryColor,
            tabIndex,
            inputRef,
          }}
        />
      );
    },
  },

  // Terms & Conditions
  terms: {
    type: 'terms',
    label: 'Terms & Conditions',
    icon: <FileCheck size={18} />,
    category: 'input',
    defaultProps: {
      label: 'I agree to the',
      termsLinkText: 'Terms of Service',
      termsUrl: '',
      termsContent: '',
      required: true,
      exportName: 'terms_accepted',
    },
    structure: {
      objects: [
        { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 1 },
        { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 2 },
        { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } }
      ],
      defaultLayout: 'horizontal',
      layoutGroups: { row1: ['input', 'label'], row2: ['validation'] },
      // Allow users to change vertical alignment via Object Layout panel.
      defaultRowAlignment: 'top'
    },
    previewComponent: makeToolboxPreview({
      type: 'terms',
      structure: {
        objects: [
          { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 1 },
          { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 2 },
          { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } },
        ],
        defaultLayout: 'horizontal',
        layoutGroups: { row1: ['input', 'label'], row2: ['validation'] },
        defaultRowAlignment: 'top',
      },
      props: {
        label: 'I agree to the',
        termsLinkText: 'Terms of Service',
        termsUrl: '',
        termsContent: '',
        required: true,
        exportName: 'terms_accepted',
      },
    }),
    runtimeComponent: ({ component, value, onChange, disabled, required, error, tabIndex, primaryColor, inputRef, styleOverrides, globalStyles }) => {
      const structure = ComponentRegistry[component.type].structure || getDefaultStructure(component.type);
      const renderers = getRenderersForComponent(component.type, structure, component);

      return (
        <UniversalFieldShell
          structure={structure}
          renderers={renderers}
          surface="runtime"
          objectLayout={component.props.objectLayout}
          layoutGroups={component.props.layoutGroups}
          styleOverrides={styleOverrides}
          globalStyles={globalStyles}
          componentId={component.id}
          component={component}
          runtimeMode={{
            value: Boolean(value),
            onChange,
            disabled,
            required,
            error,
            primaryColor,
            tabIndex,
            inputRef,
          }}
        />
      );
    },
  },

  // Submit Button
  'submit-button': {
    type: 'submit-button',
    label: 'Submit Button',
    icon: <Send size={18} />,
    category: 'input',
    defaultProps: {
      buttonText: 'Submit',
      buttonAction: 'submit',
      buttonWidth: 'auto',
      buttonAlign: 'left',
      showLoadingState: true,
      disableUntilValid: true,
      showIcon: true,
    },
    structure: {
      objects: [
        { id: 'button', type: 'action', archetype: 'Action', required: true, order: 1 },
        { id: 'loading', type: 'status', archetype: 'HelperText', required: false, order: 2, conditional: { type: 'prop', prop: 'showLoadingState', showInProperties: false } },
        { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'state', condition: (ctx) => ctx.componentState?.hasFocus && ctx.allFormErrors && Object.keys(ctx.allFormErrors).length > 0 } }
      ],
      defaultLayout: 'vertical'
    },
    previewComponent: makeToolboxPreview({
      type: 'submit-button',
      structure: {
        objects: [
          { id: 'button', type: 'action', archetype: 'Action', required: true, order: 1 },
          { id: 'loading', type: 'status', archetype: 'HelperText', required: false, order: 2, conditional: { type: 'prop', prop: 'showLoadingState', showInProperties: false } },
          { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'state', condition: (ctx) => ctx.componentState?.hasFocus && ctx.allFormErrors && Object.keys(ctx.allFormErrors).length > 0 } },
        ],
        defaultLayout: 'vertical',
      },
      props: {
        buttonText: 'Submit',
        buttonAction: 'submit',
        buttonWidth: 'auto',
        buttonAlign: 'left',
        showLoadingState: true,
        disableUntilValid: true,
        showIcon: true,
      },
    }),
    runtimeComponent: ({ component, disabled, onSubmit, error, allFormErrors, formValidationContext, styleOverrides, globalStyles, required }) => {
      const structure = ComponentRegistry[component.type].structure || getDefaultStructure(component.type);
      const renderers = getRenderersForComponent(component.type, structure, component);

      const [hasFocus, setHasFocus] = React.useState(false);
      const [isSubmitting, setIsSubmitting] = React.useState(false);

      return (
        <UniversalFieldShell
          structure={structure}
          renderers={renderers}
          surface="runtime"
          objectLayout={component.props.objectLayout}
          layoutGroups={component.props.layoutGroups}
          styleOverrides={styleOverrides}
          globalStyles={globalStyles}
          componentId={component.id}
          component={component}
          runtimeMode={{
            componentState: { hasFocus },
            allFormErrors,
            formValidationContext,
            validationErrors: error ? { [component.id]: error } : undefined,
            required,
            disabled,
            isLoading: isSubmitting,
            onClick: () => {
              if (!onSubmit || disabled) return;
              void (async () => {
                try {
                  setHasFocus(true);
                  setIsSubmitting(true);
                  await onSubmit();
                } finally {
                  setIsSubmitting(false);
                  setHasFocus(false);
                }
              })();
            },
          }}
        />
      );
    },
  },

  // Display
  header: {
    type: 'header',
    label: 'Header',
    icon: <Heading size={18} />,
    category: 'display',
    defaultProps: { label: 'Header' },
    structure: {
      objects: [
        { id: 'content', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 }
      ],
      defaultLayout: 'vertical'
    },
    previewComponent: makeToolboxPreview({
      type: 'header',
      structure: {
        objects: [{ id: 'content', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 }],
        defaultLayout: 'vertical',
      },
      props: { label: 'Header' },
      renderersOverride: (base) => ({
        ...base,
        content: ({ styles, componentId }) => (
          <h3 id={componentId ? `${componentId}-content` : undefined} style={styles.labelStyle}>
            Header
          </h3>
        ),
      }),
    }),
    runtimeComponent: ({ component, styleOverrides, globalStyles }) => {
      const structure = ComponentRegistry[component.type].structure || getDefaultStructure(component.type);
      const baseRenderers = getRenderersForComponent(component.type, structure, component);
      const renderers: ObjectRenderers = {
        ...baseRenderers,
        // Header uses its 'content' object but should render as a heading, not a <label>.
        content: ({ styles, componentId }) => (
          <div>
            <h3 id={componentId ? `${componentId}-content` : undefined} style={styles.labelStyle}>
              {String(component.props.label ?? '')}
            </h3>
            <div style={{ minHeight: 18 }} />
          </div>
        ),
      };

      return (
        <UniversalFieldShell
          structure={structure}
          renderers={renderers}
          surface="runtime"
          objectLayout={component.props.objectLayout}
          layoutGroups={component.props.layoutGroups}
          styleOverrides={styleOverrides}
          globalStyles={globalStyles}
          componentId={component.id}
          component={component}
        />
      );
    },
  },
  // Divider - Uses UniversalFieldShell with SmartBorder for collision detection
  divider: {
    type: 'divider',
    label: 'Divider',
    icon: <Minus size={18} />,
    category: 'display',
    defaultProps: {
      // Leave undefined so it falls back to GlobalStyles.dividerWidth.
    },
    structure: {
      objects: [
        { id: 'line', type: 'divider', archetype: 'Divider', required: true, order: 1 }
      ],
      defaultLayout: 'vertical'
    },
    previewComponent: makeToolboxPreview({
      type: 'divider',
      structure: {
        objects: [{ id: 'line', type: 'divider', archetype: 'Divider', required: true, order: 1 }],
        defaultLayout: 'vertical',
      },
      props: {},
    }),
    runtimeComponent: ({ component, styleOverrides, globalStyles }) => {
      const structure = ComponentRegistry[component.type].structure || getDefaultStructure(component.type);
      const renderers = getRenderersForComponent(component.type, structure, component);
      return (
        <UniversalFieldShell
          structure={structure}
          renderers={renderers}
          surface="runtime"
          objectLayout={component.props.objectLayout}
          layoutGroups={component.props.layoutGroups}
          styleOverrides={styleOverrides}
          globalStyles={globalStyles}
          componentId={component.id}
          component={component}
        />
      );
    },
  }
} as Record<ComponentType, ComponentDefinition>;

export const generateComponent = (type: ComponentType): FormComponent => {
  const def = ComponentRegistry[type];
  if (!def) {
      // Fallback or error if type is legacy but not in registry
      console.warn(`Component type ${type} not found in registry.`);
      return {
          id: `${type}-${Date.now()}`,
          type,
          props: {},
          children: []
      };
  }
  
  // Initialize structure-related props from structure definition
  const structure = def.structure;
  const props: any = { ...def.defaultProps };
  
  // IMPORTANT:
  // Components should follow Global Defaults by default.
  //
  // - Toolbox previews receive `globalStyles` from `ComponentSidebar`, so they naturally render with
  //   `globalStyles.defaultObjectLayout` unless a component has an explicit override.
  // - When adding a component to the canvas, we intentionally do NOT seed `props.objectLayout` /
  //   `props.layoutGroups` from the structure, otherwise the component would override Global Defaults
  //   immediately (this is exactly what caused first-name to switch from toolbox-vertical → canvas-mixed).
  void structure;
  
  return {
    id: `${type}-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
    type,
    props,
    children: def.defaultChildren ? [...def.defaultChildren] : undefined
  };
};
