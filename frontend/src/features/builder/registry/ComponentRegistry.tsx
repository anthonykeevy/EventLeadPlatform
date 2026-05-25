import React from 'react';
import { 
  Type, 
  Hash, 
  AlignLeft, 
  Box, 
  CheckSquare, 
  List, 
  Calendar, 
  Link,
  Heading, 
  FileText,
  User,
  Phone,
  MapPin,
  FileCheck,
  Send,
  Star,
  Minus,
  Upload,
} from 'lucide-react';
import { uploadPublicFormAttachment } from '../../renderer/api/publicSubmissionApi';
import { ComponentType, FormComponent, StyleOverrides, GlobalStyles, LayoutType, ComponentStructure, ObjectLayoutType } from '../types/builder.types';
import { getDefaultStructure } from '../utils/structureDefaults';
import { UniversalFieldShell } from '../components/UniversalFieldShell';
import { getRenderersForComponent } from '../utils/componentRenderers';
import { ObjectRenderers } from '../utils/objectRenderers';
import { AddressLookupAuRuntime } from '../components/edf/AddressLookupAuRuntime';
import { CompanyLookupAbrRuntime } from '../components/edf/CompanyLookupAbrRuntime';

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

interface ToolboxPreviewProps {
  globalStyles?: GlobalStyles;
  /** When true, render input object with focus styling (e.g. Focus Color cycling) */
  simulateFocus?: boolean;
}

function makeToolboxPreview(args: {
  type: ComponentType;
  structure: ComponentStructure;
  props: FormComponent['props'];
  renderersOverride?: (base: ObjectRenderers) => ObjectRenderers;
}): React.ReactNode {
  const ToolboxPreview: React.FC<ToolboxPreviewProps> = ({ globalStyles, simulateFocus }) => {
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
        simulateFocus={simulateFocus}
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
  /** Public form only: token + session for attachment upload (Story 6.2.2) */
  publicFormUploadContext?: {
    token: string;
    clientSessionId: string;
  };
  /** Preview/production artboard CSS scale (portaled EDF UI must match). */
  artboardScale?: number;
}

const FileUploadRuntimeComponent: React.FC<RuntimeComponentProps> = ({
  component,
  value,
  onChange,
  disabled,
  required,
  error,
  tabIndex,
  primaryColor,
  publicFormUploadContext,
}) => {
  const allowMulti = Boolean(component.props.allowMultiple);
  const maxFiles =
    typeof component.props.maxFiles === 'number' && component.props.maxFiles > 0
      ? component.props.maxFiles
      : 8;
  const maxBytes =
    typeof component.props.maxFileSizeBytes === 'number' && component.props.maxFileSizeBytes > 0
      ? component.props.maxFileSizeBytes
      : typeof component.props.maxFileSizeMb === 'number' && component.props.maxFileSizeMb > 0
        ? Math.round(component.props.maxFileSizeMb * 1024 * 1024)
        : 10 * 1024 * 1024;

  const accept =
    component.props.accept ||
    (Array.isArray(component.props.acceptedFileTypes)
      ? component.props.acceptedFileTypes.join(',')
      : undefined);

  const ids: string[] = allowMulti
    ? Array.isArray(value)
      ? (value as string[]).filter(Boolean)
      : []
    : typeof value === 'string' && value
      ? [value]
      : [];

  const [busy, setBusy] = React.useState(false);
  const [localError, setLocalError] = React.useState<string | null>(null);
  /** Display names keyed by attachmentId (form value stays UUID-only for submit). */
  const [fileLabelById, setFileLabelById] = React.useState<Record<string, string>>({});
  const displayError = error || localError;
  const label = component.props.label || 'File upload';
  const help = component.props.helpText;

  const onPick: React.ChangeEventHandler<HTMLInputElement> = async (e) => {
    const files = e.target.files;
    if (!files?.length) return;
    setLocalError(null);
    const ctx = publicFormUploadContext;
    if (!ctx?.token) {
      setLocalError('Upload is available on the published form only.');
      e.target.value = '';
      return;
    }
    const picked = Array.from(files);
    if (!allowMulti && picked.length > 1) {
      setLocalError('Only one file is allowed.');
      e.target.value = '';
      return;
    }
    const room = allowMulti ? Math.max(0, maxFiles - ids.length) : 1;
    if (room <= 0) {
      setLocalError(`Maximum ${maxFiles} file(s).`);
      e.target.value = '';
      return;
    }
    const slice = picked.slice(0, room);
    setBusy(true);
    try {
      if (allowMulti) {
        const next = [...ids];
        for (const file of slice) {
          if (file.size > maxBytes) {
            setLocalError(`File exceeds ${Math.round(maxBytes / (1024 * 1024))} MB.`);
            continue;
          }
          const res = await uploadPublicFormAttachment(ctx.token, {
            file,
            componentId: component.id,
            clientSessionId: ctx.clientSessionId,
          });
          next.push(res.attachmentId);
          setFileLabelById((prev) => ({ ...prev, [res.attachmentId]: file.name }));
        }
        onChange(next);
      } else {
        const file = slice[0];
        if (file.size > maxBytes) {
          setLocalError(`File exceeds ${Math.round(maxBytes / (1024 * 1024))} MB.`);
        } else {
          const res = await uploadPublicFormAttachment(ctx.token, {
            file,
            componentId: component.id,
            clientSessionId: ctx.clientSessionId,
          });
          onChange(res.attachmentId);
          setFileLabelById({ [res.attachmentId]: file.name });
        }
      }
    } catch {
      setLocalError('Upload failed. Check connection and try again.');
    } finally {
      setBusy(false);
      e.target.value = '';
    }
  };

  const accent = primaryColor ?? '#0055FF';

  return (
    <div className="space-y-1 w-full">
      <label className="block text-sm font-medium text-gray-800">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      {help ? <p className="text-xs text-gray-500">{help}</p> : null}
      <label
        className={`inline-flex items-center gap-2 rounded-md border border-dashed px-3 py-2 text-sm cursor-pointer select-none ${
          disabled || busy ? 'opacity-50 pointer-events-none' : 'hover:bg-gray-50'
        }`}
        style={{ borderColor: accent }}
      >
        <Upload size={16} style={{ color: accent }} />
        <span>{busy ? 'Uploading…' : 'Choose file'}</span>
        <input
          type="file"
          className="sr-only"
          accept={accept}
          disabled={disabled || busy}
          multiple={allowMulti}
          tabIndex={tabIndex}
          onChange={onPick}
        />
      </label>
      {ids.length > 0 && (
        <ul className="text-xs text-gray-600 space-y-1 mt-1">
          {ids.map((id) => {
            const displayName = fileLabelById[id] || 'Uploaded file';
            return (
              <li key={id} className="flex items-center justify-between gap-2">
                <span className="truncate min-w-0" title={`${displayName} (${id})`}>
                  {displayName}
                </span>
                <button
                  type="button"
                  className="text-red-600 hover:underline shrink-0"
                  disabled={disabled || busy}
                  onClick={() => {
                    if (allowMulti) {
                      setFileLabelById((prev) => {
                        const next = { ...prev };
                        delete next[id];
                        return next;
                      });
                      onChange(ids.filter((x) => x !== id));
                    } else {
                      setFileLabelById({});
                      onChange('');
                    }
                  }}
                >
                  Remove
                </button>
              </li>
            );
          })}
        </ul>
      )}
      {displayError ? <p className="text-xs text-red-600 mt-1">{displayError}</p> : null}
    </div>
  );
};

const SubmitButtonRuntimeComponent: React.FC<RuntimeComponentProps> = ({
  component,
  disabled,
  onSubmit,
  error,
  allFormErrors,
  formValidationContext,
  styleOverrides,
  globalStyles,
  required,
}) => {
  const structure = ComponentRegistry['submit-button']?.structure || getDefaultStructure('submit-button');
  const renderers = getRenderersForComponent('submit-button', structure, component);

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
};

export interface ComponentDefinition {
  type: ComponentType;
  label: string;
  icon: React.ReactNode;
  category: 'layout' | 'input' | 'display';
  defaultProps: Record<string, unknown>;
  defaultChildren?: FormComponent[];
  previewComponent?: React.ReactNode; 
  runtimeComponent?: React.FC<RuntimeComponentProps>;
  
  // NEW: Component structure definition
  structure: ComponentStructure;
  
  // NEW: For custom components stored in database
  isCustom?: boolean;
  customComponentId?: string; // Reference to database record
}

export const ComponentRegistry: Partial<Record<ComponentType, ComponentDefinition>> = {
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
      const structure = ComponentRegistry[component.type]?.structure || getDefaultStructure(component.type);
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
      const structure = ComponentRegistry[component.type]?.structure || getDefaultStructure(component.type);
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
      const structure = ComponentRegistry[component.type]?.structure || getDefaultStructure(component.type);
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
      const structure = ComponentRegistry[component.type]?.structure || getDefaultStructure(component.type);
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
  url: {
    type: 'url',
    label: 'Website URL',
    icon: <Link size={18} />,
    category: 'input',
    defaultProps: {
      label: 'Website URL',
      placeholder: 'example.com',
      required: false,
      urlPrefix: 'https://',
      validation: { url: true, maxLength: 2048 },
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
      type: 'url',
      structure: {
        objects: [
          { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
          { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2, features: { textLengthIndicator: {} } },
          { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } },
        ],
        defaultLayout: 'vertical',
      },
      props: {
        label: 'Website URL',
        placeholder: 'example.com',
        required: false,
        urlPrefix: 'https://',
        validation: { url: true, maxLength: 2048 },
      },
    }),
    runtimeComponent: ({ component, value, onChange, disabled, required, error, tabIndex, primaryColor, inputRef, styleOverrides, globalStyles }) => {
      const structure = ComponentRegistry[component.type]?.structure || getDefaultStructure(component.type);
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
      const structure = ComponentRegistry[component.type]?.structure || getDefaultStructure(component.type);
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
      const structure = ComponentRegistry[component.type]?.structure || getDefaultStructure(component.type);
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
      const structure = ComponentRegistry[component.type]?.structure || getDefaultStructure(component.type);
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
      const structure = ComponentRegistry[component.type]?.structure || getDefaultStructure(component.type);
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
      const structure = ComponentRegistry[component.type]?.structure || getDefaultStructure(component.type);
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
      const structure = ComponentRegistry[component.type]?.structure || getDefaultStructure(component.type);
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

  'address-lookup-au': {
    type: 'address-lookup-au',
    label: 'Address Lookup (AU)',
    icon: <MapPin size={18} />,
    category: 'input',
    defaultProps: {
      label: 'Address',
      placeholder: 'Start typing your address...',
      required: false,
      exportName: 'address',
      deliveryMode: 'decomposed',
      concatenationTemplate: '{{line1}}, {{suburb}} {{state}} {{postcode}}',
      enabledOutputFields: ['line1', 'suburb', 'state', 'postcode'],
      allowManualFallback: true,
      requireValidatedAddress: false,
      editableAfterResolve: true,
      showUnitField: true,
      allowDeliveryInstructions: false,
      requireDeliveryInstructions: false,
      deliveryInstructionsLabel: 'Delivery instructions',
      deliveryInstructionsExportName: 'address_instructions',
      showPoBoxHelperText: true,
      validation: { maxLength: 120 },
    },
    structure: {
      objects: [
        { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
        { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2, features: { textLengthIndicator: {} } },
        { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } },
      ],
      defaultLayout: 'vertical',
    },
    previewComponent: makeToolboxPreview({
      type: 'address-lookup-au',
      structure: {
        objects: [
          { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
          { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2, features: { textLengthIndicator: {} } },
          { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } },
        ],
        defaultLayout: 'vertical',
      },
      props: {
        label: 'Address (AU lookup)',
        placeholder: 'Search address…',
        exportName: 'address',
        validation: { maxLength: 120 },
      },
    }),
    runtimeComponent: AddressLookupAuRuntime,
  },

  'company-lookup-abr': {
    type: 'company-lookup-abr',
    label: 'Company Lookup (ABR)',
    icon: <MapPin size={18} />,
    category: 'input',
    defaultProps: {
      label: 'Company',
      placeholder: 'Search by ABN, ACN, or name…',
      required: false,
      exportName: 'company',
      deliveryMode: 'decomposed',
      enabledOutputFields: ['legalEntityName', 'abn', 'entityType'],
      allowManualFallback: true,
      requireAbn: false,
      requireAbnWhenManual: false,
      autoSelectSingleResult: true,
      allowTradingAs: true,
      tradingAsLabel: 'Trading as (optional)',
      tradingAsExportName: 'company_tradingAs',
      showBusinessNamesInResults: true,
      editableLegalNameAfterResolve: false,
      warnOnInactiveAbn: true,
      blockOnInactiveAbn: false,
      validation: { maxLength: 200 },
    },
    structure: {
      objects: [
        { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
        { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2, features: { textLengthIndicator: {} } },
        { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } },
      ],
      defaultLayout: 'vertical',
    },
    previewComponent: makeToolboxPreview({
      type: 'company-lookup-abr',
      structure: {
        objects: [
          { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
          { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2, features: { textLengthIndicator: {} } },
          { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } },
        ],
        defaultLayout: 'vertical',
      },
      props: {
        label: 'Company (ABR)',
        placeholder: 'Search company…',
        exportName: 'company',
        validation: { maxLength: 200 },
      },
    }),
    runtimeComponent: CompanyLookupAbrRuntime,
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
      const structure = ComponentRegistry[component.type]?.structure || getDefaultStructure(component.type);
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
      const structure = ComponentRegistry[component.type]?.structure || getDefaultStructure(component.type);
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

  rating: {
    type: 'rating',
    label: 'Rating',
    icon: <Star size={18} />,
    category: 'input',
    defaultProps: {
      label: 'Rating',
      required: false,
      ratingMax: 5,
      ratingStyle: 'stars',
      ratingLabels: { low: '', high: '' },
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
      type: 'rating',
      structure: {
        objects: [
          { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
          { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2 },
          { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } },
        ],
        defaultLayout: 'vertical',
      },
      props: {
        label: 'Rating',
        required: false,
        ratingMax: 5,
        ratingStyle: 'stars',
      },
    }),
    runtimeComponent: ({ component, value, onChange, disabled, required, error, tabIndex, primaryColor, inputRef, styleOverrides, globalStyles }) => {
      const structure = ComponentRegistry[component.type]?.structure || getDefaultStructure(component.type);
      const renderers = getRenderersForComponent(component.type, structure, component);
      const ratingValue = typeof value === 'number' ? value : Number(value ?? 0);

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
            value: Number.isFinite(ratingValue) ? ratingValue : 0,
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

  'file-upload': {
    type: 'file-upload',
    label: 'File upload',
    icon: <Upload size={18} />,
    category: 'input',
    defaultProps: {
      label: 'Upload a file',
      required: false,
      helpText: '',
      allowMultiple: false,
      maxFileSizeMb: 10,
      maxFileSizeBytes: 10 * 1024 * 1024,
      accept: '',
    },
    structure: {
      objects: [
        { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
        { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2 },
        { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } },
      ],
      defaultLayout: 'vertical',
    },
    previewComponent: makeToolboxPreview({
      type: 'file-upload',
      structure: {
        objects: [
          { id: 'label', type: 'label', archetype: 'PrimaryLabel', required: true, order: 1 },
          { id: 'input', type: 'input', archetype: 'InputControl', required: true, order: 2 },
          { id: 'validation', type: 'validation', archetype: 'HelperText', required: false, order: 3, conditional: { type: 'validation' } },
        ],
        defaultLayout: 'vertical',
      },
      props: {
        label: 'Upload a file',
        required: false,
      },
    }),
    runtimeComponent: FileUploadRuntimeComponent,
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
    runtimeComponent: SubmitButtonRuntimeComponent,
  },

  // Display
  header: {
    type: 'header',
    label: 'Header',
    icon: <Heading size={18} />,
    category: 'display',
    defaultProps: { label: 'Header', width: '100%' },
    structure: {
      objects: [
        { id: 'content', type: 'display', archetype: 'DisplayBlock', required: true, order: 1 }
      ],
      defaultLayout: 'vertical'
    },
    previewComponent: makeToolboxPreview({
      type: 'header',
      structure: {
        objects: [{ id: 'content', type: 'display', archetype: 'DisplayBlock', required: true, order: 1 }],
        defaultLayout: 'vertical',
      },
      props: { label: 'Header' },
    }),
    runtimeComponent: ({ component, styleOverrides, globalStyles }) => {
      const structure = ComponentRegistry[component.type]?.structure || getDefaultStructure(component.type);
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
  },
  paragraph: {
    type: 'paragraph',
    label: 'Paragraph',
    icon: <FileText size={18} />,
    category: 'display',
    defaultProps: {
      label: 'Paragraph text goes here.',
      text: 'Paragraph text goes here.',
      width: '100%'
    },
    structure: {
      objects: [
        { id: 'content', type: 'display', archetype: 'DisplayBlock', required: true, order: 1 }
      ],
      defaultLayout: 'vertical'
    },
    previewComponent: makeToolboxPreview({
      type: 'paragraph',
      structure: {
        objects: [{ id: 'content', type: 'display', archetype: 'DisplayBlock', required: true, order: 1 }],
        defaultLayout: 'vertical',
      },
      props: { label: 'Paragraph text goes here.', text: 'Paragraph text goes here.' },
    }),
    runtimeComponent: ({ component, styleOverrides, globalStyles }) => {
      const structure = ComponentRegistry[component.type]?.structure || getDefaultStructure(component.type);
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
      const structure = ComponentRegistry[component.type]?.structure || getDefaultStructure(component.type);
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
} as Partial<Record<ComponentType, ComponentDefinition>>;

export const generateComponent = (type: ComponentType, globalStyles?: GlobalStyles): FormComponent => {
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
  const props: Record<string, unknown> = { ...def.defaultProps };
  
  // Snapshot current form Global Object Layout onto the new instance so:
  // - Toolbox previews still follow *live* global defaults (via ComponentSidebar).
  // - Canvas instances do not "drift" when the user later changes Global → Default Object Layout.
  // Only seed vertical/horizontal (mixed needs explicit layoutGroups).
  const seed: ObjectLayoutType | undefined =
    globalStyles?.defaultObjectLayout ?? (globalStyles?.defaultLayout as LayoutType | undefined);
  if (seed === 'vertical' || seed === 'horizontal') {
    props.objectLayout = seed;
  }

  void structure;
  
  return {
    id: `${type}-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
    type,
    props,
    children: def.defaultChildren ? [...def.defaultChildren] : undefined
  };
};
