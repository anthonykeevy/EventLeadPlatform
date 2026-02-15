import React from 'react';
import { useDraggable } from '@dnd-kit/core';
import { ComponentRegistry, ComponentDefinition } from '../registry/ComponentRegistry';
import { useBuilderStore } from '../stores/useBuilderStore';
import type { GlobalStyles } from '../types/builder.types';

export const ComponentSidebar: React.FC = () => {
  // Story 5.2 T05: Use Init API components when available, else full ComponentRegistry
  const initComponents = useBuilderStore(state => state.initComponents);
  const baseComponents = Object.values(ComponentRegistry);
  const allowedTypes = initComponents?.map(c => c.componentCode) ?? null;
  const components = allowedTypes
    ? baseComponents.filter(c => allowedTypes.includes(c.type))
    : baseComponents;
  
  // Get global styles from the store to pass to preview components
  const globalStyles = useBuilderStore(state => state.formDefinition?.globalStyles);
  
  const inputComponents = components.filter(c => c.category === 'input');
  const displayComponents = components.filter(c => c.category === 'display');
  
  // Panel styling - width is controlled by ResizablePanel parent
  // Using overflow-y: scroll to always reserve scrollbar space and prevent layout shift
  return (
    <aside className="w-full h-full bg-white border-r border-gray-200 overflow-y-scroll">
      <div className="p-4 border-b border-gray-100">
        <h3 className="font-semibold text-gray-700">Toolbox</h3>
        <p className="text-xs text-gray-400 mt-1">Drag components to canvas</p>
      </div>
      
      <div className="p-4 space-y-8">
        {/* Inputs */}
        <div>
            <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">Input Fields</h4>
            <div className="space-y-4">
                {inputComponents.map(item => (
                    <DraggableRichItem
                        key={item.type}
                        item={item}
                        globalStyles={globalStyles}
                    />
                ))}
            </div>
        </div>

        {/* Display */}
        <div>
            <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">Display</h4>
            <div className="space-y-4">
                {displayComponents.map(item => (
                    <DraggableRichItem
                        key={item.type}
                        item={item}
                        globalStyles={globalStyles}
                    />
                ))}
            </div>
        </div>
      </div>
    </aside>
  );
};

interface DraggableRichItemProps {
    item: ComponentDefinition;
    globalStyles?: GlobalStyles;
}

const DraggableRichItem: React.FC<DraggableRichItemProps> = ({ item, globalStyles }) => {
    const { attributes, listeners, setNodeRef, isDragging } = useDraggable({
        id: `toolbox-${item.type}`,
        data: {
            type: item.type,
            isToolboxItem: true
        }
    });

    // Check if preview is a React component (not a plain DOM element like <div>)
    // Only pass custom props to actual components, not to DOM elements
    const isReactComponent = React.isValidElement(item.previewComponent) && 
        typeof item.previewComponent.type !== 'string';

    // Props to pass to component-based previews
    const componentProps = isReactComponent ? { globalStyles } : {};

    return (
        <div 
            ref={setNodeRef}
            {...listeners}
            {...attributes}
            className={`transition-all duration-200 cursor-grab active:cursor-grabbing ${isDragging ? 'opacity-40' : 'hover:translate-x-1'}`}
        >
            {/* Clone the preview component to inject global styles if it's a React component */}
            {React.isValidElement(item.previewComponent) 
                ? React.cloneElement(item.previewComponent as React.ReactElement, componentProps)
                : item.previewComponent
            }
        </div>
    );
};

// Removed SidebarSection and DraggableSidebarItem as they were primarily for Layout components
