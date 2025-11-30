import React from 'react';
import { 
  Type, 
  Hash, 
  AlignLeft, 
  Box, 
  CheckSquare, 
  List, 
  Calendar, 
  Heading, 
  Pilcrow,
  User 
} from 'lucide-react';
import { ComponentType, FormComponent } from '../types/builder.types';
import { FirstNameField } from '../components/fields/FirstNameField';
import { StandardInput } from '../components/fields/StandardInput';

export interface ComponentDefinition {
  type: ComponentType;
  label: string;
  icon: React.ReactNode;
  category: 'layout' | 'input' | 'display';
  defaultProps: Record<string, any>;
  defaultChildren?: FormComponent[];
  previewComponent?: React.ReactNode; 
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
      required: true
    },
    previewComponent: <FirstNameField />
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
      required: false
    },
    previewComponent: <StandardInput 
        label="Text Field" 
        icon={Type} 
        placeholder="Enter text..." 
        validationMessage="Validation error example"
    />
  },
  number: {
    type: 'number',
    label: 'Number',
    icon: <Hash size={18} />,
    category: 'input',
    defaultProps: {
      label: 'Number Field',
      placeholder: '0',
      required: false
    },
    previewComponent: <StandardInput 
        label="Number Field" 
        icon={Hash} 
        placeholder="0" 
        type="number"
        validationMessage="Must be a valid number"
    />
  },
  email: {
    type: 'email',
    label: 'Email',
    icon: <Box size={18} />,
    category: 'input',
    defaultProps: {
      label: 'Email Address',
      placeholder: 'example@email.com',
      required: false
    },
    previewComponent: <StandardInput 
        label="Email Address" 
        icon={Box} 
        placeholder="name@example.com" 
        validationMessage="Invalid email format"
    />
  },
  textarea: {
    type: 'textarea',
    label: 'Text Area',
    icon: <AlignLeft size={18} />,
    category: 'input',
    defaultProps: {
      label: 'Long Text',
      placeholder: 'Enter details...',
      required: false
    },
    previewComponent: <StandardInput 
        label="Long Text" 
        icon={AlignLeft} 
        placeholder="Enter details..." 
        type="textarea"
        validationMessage="Maximum 500 characters"
    />
  },
  select: {
    type: 'select',
    label: 'Select',
    icon: <List size={18} />,
    category: 'input',
    defaultProps: {
      label: 'Dropdown',
      placeholder: 'Select an option',
      options: [],
      required: false
    },
    previewComponent: <StandardInput 
        label="Dropdown" 
        icon={List} 
        placeholder="Select option" 
        type="select"
        validationMessage="Selection required"
    />
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
    previewComponent: <StandardInput 
        label="Select Date" 
        icon={Calendar} 
        placeholder="DD/MM/YYYY" 
        type="date"
        validationMessage="Invalid date"
    />
  },

  checkbox: {
    type: 'checkbox',
    label: 'Checkbox',
    icon: <CheckSquare size={18} />,
    category: 'input',
    defaultProps: { label: 'Checkbox', required: false },
    previewComponent: <StandardInput label="Checkbox" icon={CheckSquare} placeholder="[ ] Checkbox Option" validationMessage="Required" />
  },
  radio: {
    type: 'radio',
    label: 'Radio',
    icon: <Box size={18} />,
    category: 'input',
    defaultProps: { label: 'Radio Group', required: false },
    previewComponent: <StandardInput label="Radio Group" icon={Box} placeholder="(o) Option 1" validationMessage="Selection required" />
  },

  // Layout (Row/Column removed per user request)

  // Display
  header: {
    type: 'header',
    label: 'Header',
    icon: <Heading size={18} />,
    category: 'display',
    defaultProps: { label: 'Header' }
  },
  paragraph: {
    type: 'paragraph',
    label: 'Paragraph',
    icon: <Pilcrow size={18} />,
    category: 'display',
    defaultProps: { label: 'Paragraph' }
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
  return {
    id: `${type}-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
    type,
    props: { ...def.defaultProps },
    children: def.defaultChildren ? [...def.defaultChildren] : undefined
  };
};
