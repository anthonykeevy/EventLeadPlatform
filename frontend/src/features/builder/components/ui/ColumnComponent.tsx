import React from 'react';
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable';
import { useDroppable } from '@dnd-kit/core';
import { FormComponent } from '../../types/builder.types';
import { SortableComponent } from '../SortableComponent';

interface ColumnComponentProps {
    component: FormComponent;
}

export const ColumnComponent: React.FC<ColumnComponentProps> = ({ component }) => {
    const { setNodeRef, isOver } = useDroppable({
        id: component.id,
        data: {
            type: 'container'
        }
    });

    const children = component.children || [];

    return (
        <div 
            ref={setNodeRef}
            className={`
                flex-1 flex flex-col gap-3 p-3 min-h-[80px] rounded h-full
                border-2 border-dashed transition-colors
                ${isOver ? 'border-blue-400 bg-blue-50' : 'border-gray-200'}
            `}
        >
            <SortableContext 
                items={children.map(c => c.id)} 
                strategy={verticalListSortingStrategy}
            >
                 {children.length === 0 ? (
                    <div className="w-full text-center text-xs text-gray-400 py-4 select-none flex-1 flex items-center justify-center">
                        Drop Components Here
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
