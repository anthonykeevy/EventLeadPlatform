import React from 'react';
import { useDraggable } from '@dnd-kit/core';
import { ComponentRegistry, ComponentDefinition } from '../registry/ComponentRegistry';
import { FirstNameField } from './fields/FirstNameField';
import { StandardInput } from './fields/StandardInput';

export const ComponentSidebar: React.FC = () => {
  const components = Object.values(ComponentRegistry);
  
  const inputComponents = components.filter(c => c.category === 'input');
  const displayComponents = components.filter(c => c.category === 'display');
  
  return (
    <aside className="w-80 bg-white border-r border-gray-200 flex-shrink-0 h-full overflow-y-auto">
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
                    <DraggableRichItem key={item.type} item={item} />
                ))}
            </div>
        </div>

        {/* Display */}
        <div>
            <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">Display</h4>
            <div className="space-y-4">
                {displayComponents.map(item => (
                    <DraggableRichItem key={item.type} item={item} />
                ))}
            </div>
        </div>
      </div>
    </aside>
  );
};

const DraggableRichItem: React.FC<{ item: ComponentDefinition }> = ({ item }) => {
    const { attributes, listeners, setNodeRef, isDragging } = useDraggable({
        id: `toolbox-${item.type}`,
        data: {
            type: item.type,
            isToolboxItem: true
        }
    });

    // We need to inject drag props into the Gold Standard Components
    // so they use their internal SmartBorder as the drag handle
    
    const dragProps = { dragListeners: listeners, dragAttributes: attributes, setNodeRef };

    return (
        <div className={`transition-all duration-200 ${isDragging ? 'opacity-40' : 'hover:translate-x-1'}`}>
             {/* Clone the preview component to inject drag props */}
             {React.isValidElement(item.previewComponent) 
                ? React.cloneElement(item.previewComponent as React.ReactElement, dragProps)
                : null
             }
        </div>
    );
};

// Removed SidebarSection and DraggableSidebarItem as they were primarily for Layout components
