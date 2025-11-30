/**
 * Builder Types - Story 3.3 & 3.4
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
  | 'paragraph'
  | 'first-name'; // Added for POC

export type DeviceType = 'desktop' | 'tablet' | 'mobile';

export const DEVICE_DIMENSIONS: Record<DeviceType, { width: number; height: number; label: string }> = {
    desktop: { width: 1920, height: 980, label: 'Desktop (1920 x 980)' },
    tablet: { width: 768, height: 1024, label: 'Tablet (768 x 1024)' },
    mobile: { width: 375, height: 667, label: 'Mobile (375 x 667)' }
};

export interface ComponentProps {
  label?: string; 
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
  // Canvas Refactor: Absolute Positioning
  position?: {
    x: number;
    y: number;
  };
  style?: {
      zIndex?: number;
      width?: number; // Optional override
      height?: number; // Optional override
  };
  children?: FormComponent[]; 
}

export interface FormPage {
  id: string;
  title: string;
  components: FormComponent[];
  // Canvas Refactor: Background Settings per page
  background?: {
      type: 'color' | 'image';
      value: string; // Hex code or URL
      opacity?: number;
      scale?: number;
      position?: { x: number, y: number };
  };
}

export interface GlobalStyles {
    fontFamily: string;
    fontSize: number; // Base size (e.g. 14)
    primaryColor: string;
    textColor: string;
    borderRadius: number;
    spacing: number; // Base spacing unit
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
  // Canvas Refactor: Global Styles (The Master Theme)
  globalStyles?: GlobalStyles;
  // Canvas Refactor: Global Canvas Settings
  canvasSettings?: {
      width: number; // e.g. 1920
      height: number; // e.g. 1080
      gridSize: number; // e.g. 8
  };
  pages: FormPage[];
}
