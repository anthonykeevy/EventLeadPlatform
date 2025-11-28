/**
 * Builder Types - Story 3.3
 * Based on JSON Schema from Story 3.2
 */

export type ComponentType = 
  | 'text' 
  | 'number' 
  | 'email' 
  | 'textarea' 
  | 'select' 
  | 'radio' 
  | 'checkbox'
  | 'date'
  | 'header'
  | 'paragraph';

export interface ComponentProps {
  label: string;
  required?: boolean;
  placeholder?: string;
  helpText?: string;
  options?: Array<{ label: string; value: string }>;
  [key: string]: any;
}

export interface FormComponent {
  id: string;
  type: ComponentType;
  props: ComponentProps;
}

export interface FormPage {
  id: string;
  title: string;
  components: FormComponent[];
}

export interface FormTheme {
  primaryColor: string;
  backgroundColor: string;
  fontFamily: string;
}

export interface FormDefinition {
  schemaVersion: string;
  formId: string;
  theme: FormTheme;
  pages: FormPage[];
}

