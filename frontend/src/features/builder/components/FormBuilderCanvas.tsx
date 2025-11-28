import React from 'react';
import { 
  DndContext, 
  closestCenter, 
  KeyboardSensor, 
  PointerSensor, 
  useSensor, 
  useSensors,
  DragOverlay,
  DragStartEvent,
  DragEndEvent
} from '@dnd-kit/core';
import { 
  arrayMove, 
  SortableContext, 
  sortableKeyboardCoordinates, 
  verticalListSortingStrategy 
} from '@dnd-kit/sortable';
import { useBuilderStore } from '../stores/useBuilderStore';
import { SortableComponent } from './SortableComponent';
import { FormComponent } from '../types/builder.types';

export const FormBuilderCanvas: React.FC = () => {
  const { formDefinition, activePageId, moveComponent, activeId, setActiveId } = useBuilderStore();
  
  const activePage = formDefinition?.pages.find(p => p.id === activePageId);
  const components = activePage?.components || [];
  
  const sensors = useSensors(
    useSensor(PointerSensor, {
        activationConstraint: {
            distance: 5, // Avoid accidental drags on click
        }
    }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  const handleDragStart = (event: DragStartEvent) => {
    setActiveId(event.active.id as string);
  };

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;

    if (active.id !== over?.id && over) {
      moveComponent(active.id as string, over.id as string);
    }
    
    setActiveId(null);
  };

  // Find the component object for the DragOverlay
  const activeComponent = activeId 
    ? components.find(c => c.id === activeId) 
    : null;

  if (!formDefinition) return <div>Loading Canvas...</div>;

  return (
    <div className="max-w-3xl mx-auto min-h-[800px] bg-white shadow-lg rounded-lg p-8 my-8">
        <div className="mb-8 border-b pb-4">
            <h2 className="text-2xl font-bold text-gray-800">{activePage?.title || 'Form Page'}</h2>
            <p className="text-gray-500">Drag and drop components to reorder.</p>
        </div>

      <DndContext 
        sensors={sensors} 
        collisionDetection={closestCenter} 
        onDragStart={handleDragStart}
        onDragEnd={handleDragEnd}
      >
        <SortableContext 
          items={components.map(c => c.id)} 
          strategy={verticalListSortingStrategy}
        >
          <div className="space-y-3 min-h-[200px]">
            {components.length === 0 ? (
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center text-gray-400">
                    Drop components here
                </div>
            ) : (
                components.map((component) => (
                <SortableComponent key={component.id} component={component} />
                ))
            )}
          </div>
        </SortableContext>

        <DragOverlay>
          {activeComponent ? (
             <div className="opacity-90 rotate-2 scale-105 cursor-grabbing">
                <SortableComponent component={activeComponent} />
             </div>
          ) : null}
        </DragOverlay>
      </DndContext>
    </div>
  );
};

