/**
 * Builder Store - Story 3.3
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
  
  // Actions
  initializeForm: (formId: string) => void;
  setActiveId: (id: string | null) => void;
  moveComponent: (activeId: string, overId: string) => void;
  addComponent: (component: FormComponent) => void; // Placeholder for future
}

// Mock Initial Data (as per UAT requirements)
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
        {
          id: 'comp-1',
          type: 'text',
          props: { label: 'First Name', placeholder: 'Enter your first name', required: true },
        },
        {
          id: 'comp-2',
          type: 'email',
          props: { label: 'Email Address', placeholder: 'name@example.com', required: true },
        },
        {
          id: 'comp-3',
          type: 'checkbox',
          props: { label: 'I agree to terms', required: true },
        },
        {
          id: 'comp-4',
          type: 'textarea',
          props: { label: 'Comments', placeholder: 'Any additional details...' },
        }
      ],
    },
  ],
};

export const useBuilderStore = create<BuilderState>((set, get) => ({
  formDefinition: null,
  activeId: null,
  activePageId: 'page-1',
  isLoading: false,

  initializeForm: (formId: string) => {
    set({ isLoading: true });
    
    // In a real app, we would fetch from API here.
    // For now, we hydrate with mock data and override the ID.
    setTimeout(() => {
      set({
        formDefinition: { ...MOCK_INITIAL_FORM, formId },
        activePageId: MOCK_INITIAL_FORM.pages[0].id,
        isLoading: false,
      });
    }, 500); // Simulate network delay
  },

  setActiveId: (id) => set({ activeId: id }),

  moveComponent: (activeId, overId) => {
    set((state) => {
      if (!state.formDefinition) return state;

      const currentPageIndex = state.formDefinition.pages.findIndex(p => p.id === state.activePageId);
      if (currentPageIndex === -1) return state;

      const components = [...state.formDefinition.pages[currentPageIndex].components];
      const oldIndex = components.findIndex((c) => c.id === activeId);
      const newIndex = components.findIndex((c) => c.id === overId);

      if (oldIndex === -1 || newIndex === -1) return state;

      const newComponents = arrayMove(components, oldIndex, newIndex);
      
      // Create new immutable state
      const newPages = [...state.formDefinition.pages];
      newPages[currentPageIndex] = {
        ...newPages[currentPageIndex],
        components: newComponents
      };

      return {
        formDefinition: {
          ...state.formDefinition,
          pages: newPages
        }
      };
    });
  },

  addComponent: (component) => {
      // Placeholder for Story 3.4
      console.log('Adding component', component);
  }
}));

