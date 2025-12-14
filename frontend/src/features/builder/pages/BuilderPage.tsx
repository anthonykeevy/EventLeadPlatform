import React, { useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { 
  DndContext, 
  closestCenter, 
  KeyboardSensor, 
  PointerSensor, 
  useSensor, 
  useSensors,
  DragOverlay,
  DragStartEvent,
  DragEndEvent,
  defaultDropAnimationSideEffects,
  DropAnimation
} from '@dnd-kit/core';
import { createSnapModifier } from '@dnd-kit/modifiers';

import { useBuilderStore } from '../stores/useBuilderStore';
import { BuilderLayout } from '../components/BuilderLayout';
import { ComponentSidebar } from '../components/ComponentSidebar';
import { FormBuilderCanvas } from '../components/FormBuilderCanvas';
import { PropertiesPanel } from '../components/PropertiesPanel'; // Story 3.5
import { ComponentPreview } from '../components/ComponentPreview';
import { RuntimeFormView } from '../components/runtime/RuntimeFormView';
import { FirstNameField } from '../components/fields/FirstNameField';
import { StandardInput } from '../components/fields/StandardInput';
import { ComponentRegistry, generateComponent } from '../registry/ComponentRegistry';
import { LoadingSpinner } from '../../ux/components/LoadingSpinner';
import { ComponentType, FormComponent } from '../types/builder.types';

// 8px Grid Snap Modifier
const snapToGridModifier = createSnapModifier(8);

const dropAnimationConfig: DropAnimation = {
    sideEffects: defaultDropAnimationSideEffects({
      styles: {
        active: {
          opacity: '0.5',
        },
      },
    }),
  };

export const BuilderPage: React.FC = () => {
  const { formId } = useParams<{ formId: string }>();
  // Get scale and showGrid from store
  const { 
      initializeForm, 
      isLoading, 
      formDefinition, 
      activeId, 
      setActiveId, 
      updateComponent, 
      addComponent, 
      scale,
      showGrid,
      viewMode
  } = useBuilderStore();

  const canvasRef = useRef<HTMLDivElement>(null);

  const sensors = useSensors(
    useSensor(PointerSensor, {
        activationConstraint: {
            distance: 5, 
        }
    }),
    useSensor(KeyboardSensor, {})
  );

  useEffect(() => {
    if (formId) {
      initializeForm(formId);
    }
  }, [formId, initializeForm]);

  const handleDragStart = (event: DragStartEvent) => {
    setActiveId(event.active.id as string);
  };

  const handleDragEnd = (event: DragEndEvent) => {
    try {
        const { active, over, delta } = event;
        setActiveId(null);

        if (!over) return;

        // 1. Handle New Component from Toolbox
        if (active.id.toString().startsWith('toolbox-')) {
            const type = active.data.current?.type as ComponentType;
            if (!type) return;

            const newComponent = generateComponent(type);
            
            if (canvasRef.current) {
                const canvasRect = canvasRef.current.getBoundingClientRect();
                
                // Use active.rect.current.translated for precise visual matching
                const ghostRect = active.rect.current.translated;

                if (ghostRect) {
                    // Calculate relative position
                    const relativeX = ghostRect.left - canvasRect.left;
                    const relativeY = ghostRect.top - canvasRect.top;

                    // Apply Scale Correction:
                    const scaledX = relativeX / scale;
                    const scaledY = relativeY / scale;

                    // Snap to Grid Conditionally
                    let droppedX = scaledX;
                    let droppedY = scaledY;

                    if (showGrid) {
                        droppedX = Math.max(0, Math.round(scaledX / 8) * 8);
                        droppedY = Math.max(0, Math.round(scaledY / 8) * 8);
                    } else {
                        droppedX = Math.max(0, Math.round(scaledX));
                        droppedY = Math.max(0, Math.round(scaledY));
                    }

                    newComponent.position = { x: droppedX, y: droppedY };
                    addComponent(newComponent);
                } else {
                    newComponent.position = { x: 50, y: 50 };
                    addComponent(newComponent); 
                }
            } else {
                newComponent.position = { x: 50, y: 50 };
                addComponent(newComponent); 
            }
            return;
        }

        // 2. Handle Moving Existing Component
        if (active.id) {
            const pages = useBuilderStore.getState().formDefinition?.pages || [];
            const activePage = pages.find(p => p.id === useBuilderStore.getState().activePageId);
            const component = activePage?.components.find(c => c.id === active.id);

            if (component) {
                const currentX = component.position?.x || 0;
                const currentY = component.position?.y || 0;
                
                // Apply Scale to Delta
                const scaledDeltaX = delta.x / scale;
                const scaledDeltaY = delta.y / scale;
                
                let newX = currentX + scaledDeltaX;
                let newY = currentY + scaledDeltaY;

                // Snap to Grid Conditionally
                if (showGrid) {
                     newX = Math.round(newX / 8) * 8;
                     newY = Math.round(newY / 8) * 8;
                } else {
                     newX = Math.round(newX);
                     newY = Math.round(newY);
                }

                updateComponent(component.id, {
                    position: { x: newX, y: newY }
                });
            }
        }
    } catch (err) {
        console.error("Drag End Error:", err);
    }
  };

  let activeComponent: FormComponent | null = null;
  const components = formDefinition?.pages.find(p => p.id === useBuilderStore.getState().activePageId)?.components || [];

  if (activeId) {
      if (activeId.toString().startsWith('toolbox-')) {
          const type = activeId.toString().replace('toolbox-', '') as ComponentType;
          activeComponent = generateComponent(type);
      } else {
          const findRecursive = (list: FormComponent[]): FormComponent | null => {
              for(const c of list) {
                  if (c.id === activeId) return c;
                  if (c.children) {
                      const found = findRecursive(c.children);
                      if (found) return found;
                  }
              }
              return null;
          };
          activeComponent = findRecursive(components);
      }
  }

  if (isLoading) {
    return (
      <div className="h-screen w-full flex items-center justify-center bg-gray-50">
        <div className="text-center">
            <LoadingSpinner size="lg" />
            <p className="mt-4 text-gray-500">Loading Form Builder...</p>
        </div>
      </div>
    );
  }

  const renderOverlayContent = (component: FormComponent | null) => {
      if (!component) return null;
      
      // Show highlighted SmartBorder while dragging (isSelected=true)
      const content = (() => {
        if (component.type === 'first-name') return <FirstNameField isSelected={true} />;
        const def = ComponentRegistry[component.type];
        if (def?.category === 'input' || def?.category === 'display') {
            return <StandardInput 
                label={component.props.label || 'Field'}
                icon={def.icon}
                placeholder={component.props.placeholder}
                validationMessage={component.props.validationMessage || "Validation message here"}
                required={component.props.required}
                type={component.type as 'text' | 'number' | 'email' | 'textarea' | 'select' | 'date'}
                options={component.props.options}
                isSelected={true}
            />
        }
        return <ComponentPreview component={component} isOverlay={true} />;
      })();

      return (
          <div style={{ 
              transform: `scale(${scale})`, 
              transformOrigin: 'top left', 
          }}>
              {content}
          </div>
      );
  };

  if (viewMode === 'preview' && formDefinition) {
    return (
      <BuilderLayout
        sidebar={<ComponentSidebar />}
        propertiesPanel={<PropertiesPanel />}
        title={formDefinition?.formId ? `Form: ${formDefinition.formId}` : 'Form Builder'}
      >
        <RuntimeFormView definition={formDefinition} title="Builder Preview (Runtime)" />
      </BuilderLayout>
    );
  }

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCenter}
      onDragStart={handleDragStart}
      onDragEnd={handleDragEnd}
      // Conditionally apply the snap modifier
      modifiers={showGrid ? [snapToGridModifier] : []}
    >
      <BuilderLayout
        sidebar={<ComponentSidebar />}
        propertiesPanel={<PropertiesPanel />}
        title={formDefinition?.formId ? `Form: ${formDefinition.formId}` : 'Form Builder'}
      >
        <FormBuilderCanvas ref={canvasRef} />
      </BuilderLayout>

      <DragOverlay dropAnimation={dropAnimationConfig}>
        {renderOverlayContent(activeComponent)}
      </DragOverlay>
    </DndContext>
  );
};
