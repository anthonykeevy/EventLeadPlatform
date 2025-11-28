import React from 'react';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { FormComponent } from '../types/builder.types';
import { GripVertical } from 'lucide-react';

interface SortableComponentProps {
  component: FormComponent;
}

export const SortableComponent: React.FC<SortableComponentProps> = ({ component }) => {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: component.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={`
        relative group bg-white border border-gray-200 rounded-md p-4 mb-3 shadow-sm 
        hover:border-teal-400 hover:shadow-md transition-all
        ${isDragging ? 'ring-2 ring-teal-500 z-50' : ''}
      `}
    >
      {/* Drag Handle */}
      <div 
        {...attributes} 
        {...listeners}
        className="absolute left-2 top-1/2 -translate-y-1/2 p-2 cursor-grab text-gray-400 hover:text-teal-600 active:cursor-grabbing"
        aria-label="Drag to reorder"
      >
        <GripVertical size={20} />
      </div>

      {/* Content Area */}
      <div className="ml-8">
        <div className="mb-2">
          <label className="block text-sm font-medium text-gray-700">
            {component.props.label}
            {component.props.required && <span className="text-red-500 ml-1">*</span>}
          </label>
          {component.props.helpText && (
             <p className="text-xs text-gray-500 mb-1">{component.props.helpText}</p>
          )}
        </div>

        {/* Visual Placeholder of the Input */}
        <div className="pointer-events-none"> 
          {renderInputPlaceholder(component)}
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
    default: // text, email, number, date
      return <div className={baseClasses}>{component.props.placeholder || 'Input text'}</div>;
  }
};

