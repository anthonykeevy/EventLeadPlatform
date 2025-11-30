import React from 'react';
import { useDraggable } from '@dnd-kit/core';
import { CSS } from '@dnd-kit/utilities';
import { FormComponent } from '../types/builder.types';
import { FirstNameField } from './fields/FirstNameField';
import { StandardInput } from './fields/StandardInput';
import { ComponentRegistry } from '../registry/ComponentRegistry';
import { useBuilderStore } from '../stores/useBuilderStore';

interface SortableComponentProps {
  component: FormComponent;
}

// Renamed to DraggableComponent since we aren't sorting anymore
export const SortableComponent: React.FC<SortableComponentProps> = ({ component }) => {
  // Get the current Canvas Scale and Layer from store
  const { scale, activeLayer } = useBuilderStore(state => ({ 
      scale: state.scale, 
      activeLayer: state.activeLayer 
  }));

  // Determine if interaction should be disabled
  // For now, all components are on Layer 1 (Elements)
  // If Active Layer is 0 (Background), then Layer 1 is locked.
  const isLocked = activeLayer === 0; 

  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    isDragging,
  } = useDraggable({ 
      id: component.id,
      data: {
        type: component.type,
        component 
      },
      disabled: isLocked // Disable drag if locked
  });

  // Inverse-Scale the Transform
  const scaledTransform = transform ? {
      ...transform,
      x: transform.x / scale,
      y: transform.y / scale
  } : null;

  // Absolute Positioning Logic
  const style: React.CSSProperties = {
    transform: scaledTransform ? CSS.Translate.toString(scaledTransform) : undefined,
    position: 'absolute',
    left: component.position?.x ?? 0,
    top: component.position?.y ?? 0,
    zIndex: isDragging ? 100 : (component.style?.zIndex ?? 10),
    opacity: isDragging ? 0.5 : 1,
    // Visual feedback for locked state
    cursor: isLocked ? 'not-allowed' : undefined 
  };

  // 1. First Name (POC)
  if (component.type === 'first-name') {
      return (
        <div
            ref={setNodeRef} 
            style={style}
            className="group touch-none" 
        >
            <FirstNameField 
                dragListeners={listeners} 
                dragAttributes={attributes} 
            />
        </div>
      );
  }

  // 2. Standard Inputs (Gold Standard)
  const def = ComponentRegistry[component.type];
  
  return (
    <div
      ref={setNodeRef}
      style={style}
      className="group touch-none"
    >
      <StandardInput 
          label={component.props.label || 'Unknown'}
          icon={def?.icon}
          placeholder={component.props.placeholder}
          validationMessage={component.props.validationMessage || "Validation message here"}
          required={component.props.required}
          type={component.type as any}
          options={component.props.options}
          dragListeners={listeners}
          dragAttributes={attributes}
      />
    </div>
  );
};
