import React from 'react';
import { FormComponent } from '../types/builder.types';
import { AlertCircle } from 'lucide-react';
import { RowComponent } from './ui/RowComponent';
import { ColumnComponent } from './ui/ColumnComponent';

interface ComponentPreviewProps {
  component: FormComponent;
  isOverlay?: boolean; // If true, we force card width
}

export const ComponentPreview: React.FC<ComponentPreviewProps> = ({ component, isOverlay = false }) => {
  // Handle Layout Containers specifically
  // For overlay of layout containers, we might want a simplified view, 
  // but for now reusing the component is fine.
  if (component.type === 'row') {
      return (
          <div className="relative group mb-4 w-full border-2 border-dashed border-gray-300 p-4 bg-gray-50 rounded">
             <div className="text-xs text-gray-400 mb-2 uppercase tracking-wider font-bold">Row Container</div>
             {/* We don't render children in drag preview to keep it clean, or we could? */}
             {/* For now, just a placeholder for the row drag */}
          </div>
      );
  }

  if (component.type === 'column') {
      return (
        <div className="relative group h-full flex-1 border-2 border-dashed border-gray-300 p-4 bg-gray-50 rounded">
             <div className="text-xs text-gray-400 mb-2 uppercase tracking-wider font-bold">Column</div>
        </div>
      );
  }

  // Standard Input/Display Components
  // If it's overlay, constrain width to 280px (Card look). If on canvas, w-full.
  const widthClass = isOverlay ? 'w-[280px]' : 'w-full';

  return (
    <div
      className={`
        relative bg-white border border-gray-200 rounded-md p-4 shadow-sm 
        ${widthClass} cursor-grabbing
      `}
    >
      {/* Content Area (Standard 3-Part Structure) */}
      <div className="ml-2">
        {/* Part 1: Label */}
        <div className="mb-2 flex justify-between">
          <label className="block text-sm font-medium text-gray-700 truncate pr-2">
            {component.props.label}
            {component.props.required && <span className="text-red-500 ml-1">*</span>}
          </label>
          {/* Component Type Badge (Helper) */}
          <span className="text-[10px] uppercase text-gray-300 font-mono flex-shrink-0">{component.type}</span>
        </div>

        {/* Part 2: Input Control */}
        <div className="pointer-events-none"> 
          {renderInputPlaceholder(component)}
        </div>
        
        {/* Part 3: Validation Message (Placeholder/Preview) */}
        <div className="mt-1 min-h-[16px]">
             <div className="flex items-center text-xs text-gray-400 border-l-2 border-gray-300 pl-2">
                <AlertCircle size={12} className="mr-1" />
                Validation message area
             </div>
        </div>
      </div>
    </div>
  );
};

const renderInputPlaceholder = (component: FormComponent) => {
  const baseClasses = "block w-full rounded-md border-gray-300 shadow-sm bg-gray-50 px-3 py-2 text-sm text-gray-500";
  
  switch (component.type) {
    case 'textarea':
      return <div className={`${baseClasses} h-20`}>{component.props.placeholder || 'Text Area'}</div>;
    case 'checkbox':
      return (
        <div className="flex items-center">
          <div className="h-4 w-4 rounded border-gray-300 bg-gray-50"></div>
          <span className="ml-2 text-sm text-gray-500">{component.props.label}</span>
        </div>
      );
    case 'radio':
        return (
            <div className="space-y-2">
                <div className="flex items-center">
                    <div className="h-4 w-4 rounded-full border-gray-300 bg-gray-50"></div>
                    <span className="ml-2 text-sm text-gray-500">Option 1</span>
                </div>
                <div className="flex items-center">
                    <div className="h-4 w-4 rounded-full border-gray-300 bg-gray-50"></div>
                    <span className="ml-2 text-sm text-gray-500">Option 2</span>
                </div>
            </div>
        );
    case 'select':
       return (
         <div className={`${baseClasses} flex justify-between items-center`}>
            <span>{component.props.placeholder || 'Select an option'}</span>
            <span>▼</span>
         </div>
       );
    case 'header':
        return <h3 className="text-lg font-bold text-gray-800 border-b pb-2">{component.props.label}</h3>;
    case 'paragraph':
        return <p className="text-gray-600">{component.props.label}</p>;
    default: // text, email, number, date
      return <div className={baseClasses}>{component.props.placeholder || 'Input text'}</div>;
  }
};

