/**
 * Builder Store - Story 3.3 & 3.4
 * Manages the state of the Form Builder (FormDefinition)
 */

import { create } from 'zustand';
import { arrayMove } from '@dnd-kit/sortable';
import { FormDefinition, FormComponent } from '../types/builder.types';

interface BuilderState {
  formDefinition: FormDefinition | null;
  activeId: string | null; // ID of the component currently being dragged
  activePageId: string; // Currently selected page
  isLoading: boolean;
  
  // Canvas Viewport State
  scale: number;
  showGrid: boolean;
  activeLayer: 0 | 1; // 0 = Background, 1 = Functional
  
  // Actions
  initializeForm: (formId: string) => void;
  setActiveId: (id: string | null) => void;
  setScale: (scale: number) => void;
  setShowGrid: (show: boolean) => void;
  setActiveLayer: (layer: 0 | 1) => void;
  moveComponent: (activeId: string, overId: string) => void; // Legacy Sortable Move (Deprecated for Canvas)
  updateComponent: (id: string, updates: Partial<FormComponent>) => void; // New Generic Update (for Position)
  addComponent: (component: FormComponent, parentId?: string, index?: number) => void;
}

const MOCK_INITIAL_FORM: FormDefinition = {
  schemaVersion: '1.0',
  formId: 'mock-form-1',
  theme: {
    primaryColor: '#0055FF',
    backgroundColor: '#FFFFFF',
    fontFamily: 'Inter',
  },
  pages: [
    {
      id: 'page-1',
      title: 'Page 1',
      components: [
        // Blank Canvas - No Components Initially
      ],
    },
  ],
};

export const useBuilderStore = create<BuilderState>((set, get) => ({
  formDefinition: null,
  activeId: null,
  activePageId: 'page-1',
  isLoading: false,
  scale: 1, // Default scale
  showGrid: true, // Default grid on
  activeLayer: 1, // Default to Elements layer

  initializeForm: (formId: string) => {
    set({ isLoading: true });
    setTimeout(() => {
      set({
        formDefinition: { ...MOCK_INITIAL_FORM, formId },
        activePageId: MOCK_INITIAL_FORM.pages[0].id,
        isLoading: false,
      });
    }, 500);
  },

  setActiveId: (id) => set({ activeId: id }),
  
  setScale: (scale) => set({ scale }),
  setShowGrid: (show) => set({ showGrid: show }),
  setActiveLayer: (layer) => set({ activeLayer: layer }),

  // Generic Update Action (Crucial for Absolute Positioning)
  updateComponent: (id, updates) => {
      set((state) => {
          if (!state.formDefinition) return state;
          const activePage = state.formDefinition.pages.find(p => p.id === state.activePageId);
          if (!activePage) return state;

          // Deep clone components
          const newComponents = JSON.parse(JSON.stringify(activePage.components)) as FormComponent[];

          // Recursive find and update
          const updateRecursive = (list: FormComponent[]): boolean => {
              for (let i = 0; i < list.length; i++) {
                  if (list[i].id === id) {
                      list[i] = { ...list[i], ...updates };
                      return true;
                  }
                  if (list[i].children && updateRecursive(list[i].children!)) {
                      return true;
                  }
              }
              return false;
          };

          updateRecursive(newComponents);

          const newPages = state.formDefinition.pages.map(p => 
            p.id === state.activePageId ? { ...p, components: newComponents } : p
          );

          return { formDefinition: { ...state.formDefinition, pages: newPages } };
      });
  },

  // Deprecated for Free-Form Canvas but kept for safety if we re-introduce lists later
  moveComponent: (activeId, overId) => {
      // ... existing logic ...
      return;
  },

  addComponent: (component, parentId, index) => {
    set((state) => {
        if (!state.formDefinition) return state;
        const activePage = state.formDefinition.pages.find(p => p.id === state.activePageId);
        if (!activePage) return state;

        let newComponents = JSON.parse(JSON.stringify(activePage.components)) as FormComponent[];

        // Simplified: Only adding to root for Free-Form Canvas for now
        newComponents.push(component);

        const newPages = state.formDefinition.pages.map(p => 
            p.id === state.activePageId ? { ...p, components: newComponents } : p
        );

        return {
            formDefinition: {
                ...state.formDefinition,
                pages: newPages
            }
        };
    });
  }
}));
