import React from 'react';
import { SortableContext, horizontalListSortingStrategy } from '@dnd-kit/sortable';
import { useDroppable } from '@dnd-kit/core';
import { FormComponent } from '../../types/builder.types';
// Circular dependency note: SortableComponent will be imported from parent index or directly.
// We will assume it works or fix with React.lazy if needed.
import { SortableComponent } from '../SortableComponent';

interface RowComponentProps {
    component: FormComponent;
}

export const RowComponent: React.FC<RowComponentProps> = ({ component }) => {
    // We need useDroppable to allow dropping into an empty row
    const { setNodeRef, isOver } = useDroppable({
        id: component.id,
        data: {
            type: 'container',
            accepts: ['column'] // Optional constraint logic
        }
    });

    const children = component.children || [];

    return (
        <div 
            ref={setNodeRef}
            className={`
                flex flex-row flex-wrap gap-4 p-4 min-h-[80px] rounded
                border-2 border-dashed transition-colors
                ${isOver ? 'border-blue-400 bg-blue-50' : 'border-gray-200 bg-gray-50'}
            `}
        >
            <SortableContext 
                items={children.map(c => c.id)} 
                strategy={horizontalListSortingStrategy}
            >
                {children.length === 0 ? (
                    <div className="w-full text-center text-xs text-gray-400 py-4 select-none">
                        Drop Columns Here
                    </div>
                ) : (
                    children.map((child) => (
                        <SortableComponent key={child.id} component={child} />
                    ))
                )}
            </SortableContext>
        </div>
    );
};

