/**
 * Builder Store - Story 3.3, 3.4 & 3.5
 * Manages the state of the Form Builder (FormDefinition)
 */

import { create } from 'zustand';
import { FormDefinition, FormComponent, GlobalStyles, DEFAULT_GLOBAL_STYLES, StyleOverrides, LogicRule } from '../types/builder.types';
import { hasStyleOverrides, getOverriddenProperties } from '../utils/styleUtils';

/**
 * Info about a component with style overrides
 */
export interface ComponentWithOverrides {
    id: string;
    label: string;
    overriddenProperties: string[];
}

/**
 * Snapshot of form state for undo/redo history
 */
interface FormSnapshot {
    formDefinition: FormDefinition;
    timestamp: number;
}

/**
 * Maximum number of undo/redo steps to keep
 */
const MAX_HISTORY_SIZE = 50;

function getStorageKey(formId: string) {
    return `builder-formDefinition-${formId}`;
}

function persistToStorage(def: FormDefinition | null) {
    if (!def?.formId) return;
    try {
        localStorage.setItem(getStorageKey(def.formId), JSON.stringify(def));
    } catch {
        // Ignore persistence failures (storage full/disabled)
    }
}

interface BuilderState {
    formDefinition: FormDefinition | null;
    activeId: string | null; // ID of the component currently being dragged
    selectedComponentId: string | null; // ID of the PRIMARY selected component (for single select mode)
    selectedComponentIds: string[]; // IDs of ALL selected components (for multi-select mode)
    activePageId: string; // Currently selected page
    isLoading: boolean;
    
    // Canvas Viewport State
    scale: number;
    showGrid: boolean;
    activeLayer: 0 | 1; // 0 = Background, 1 = Functional
    
    // Undo/Redo History
    historyPast: FormSnapshot[];
    historyFuture: FormSnapshot[];
    
    // Actions
    initializeForm: (formId: string) => void;
    setActiveId: (id: string | null) => void;
    selectComponent: (id: string | null, additive?: boolean) => void; // Story 3.5 - additive = Ctrl+Click
    clearSelection: () => void; // Clear all selections
    setScale: (scale: number) => void;
    setShowGrid: (show: boolean) => void;
    setActiveLayer: (layer: 0 | 1) => void;
    moveComponent: (activeId: string, overId: string) => void;
    updateComponent: (id: string, updates: Partial<FormComponent>) => void;
    updateComponentProps: (id: string, props: Partial<FormComponent['props']>) => void; // Story 3.5
    updateMultipleComponentProps: (props: Partial<FormComponent['props']>) => void; // Multi-select bulk update
    addComponent: (component: FormComponent, parentId?: string, index?: number) => void;
    updateGlobalStyles: (updates: Partial<GlobalStyles>) => void; // Story 3.5
    getSelectedComponent: () => FormComponent | null; // Story 3.5 helper - returns first/primary
    getSelectedComponents: () => FormComponent[]; // Multi-select helper - returns all selected
    
    // Undo/Redo Actions
    undo: () => void;
    redo: () => void;
    canUndo: () => boolean;
    canRedo: () => boolean;
    pushToHistory: () => void; // Internal: save current state before changes

    // Logic Rules (Story 3.6) - authoring + persistence only
    addRule: (rule: LogicRule) => void;
    updateRule: (ruleId: string, updates: Partial<LogicRule>) => void;
    removeRule: (ruleId: string) => void;
    moveRule: (ruleId: string, direction: 'up' | 'down') => void;
    /** Swap two rules by id (used by filtered UI reordering) */
    swapRules: (ruleIdA: string, ruleIdB: string) => void;
    toggleRuleEnabled: (ruleId: string, enabled: boolean) => void;
    
    // Override tracking helpers
    getComponentsWithOverrides: () => ComponentWithOverrides[];
    getComponentsAffectedByGlobalChange: (propertyKey: keyof StyleOverrides) => ComponentWithOverrides[];
    clearAllOverrides: () => void;
    clearOverridesForProperty: (propertyKey: keyof StyleOverrides) => void;
}

const MOCK_INITIAL_FORM: FormDefinition = {
    schemaVersion: '1.0',
    formId: 'mock-form-1',
    theme: {
        primaryColor: '#0055FF',
        backgroundColor: '#FFFFFF',
        fontFamily: 'Inter',
    },
    globalStyles: { ...DEFAULT_GLOBAL_STYLES },
    logic: { rules: [] },
    pages: [
        {
            id: 'page-1',
            title: 'Page 1',
            components: [
                // Pre-populated for UAT Testing (Story 3.5)
                // Note: No explicit 'layout' property - uses global default
                {
                    id: 'comp-1',
                    type: 'first-name',
                    props: {
                        label: 'First Name',
                        placeholder: 'Enter your first name',
                        required: true,
                    },
                    position: { x: 100, y: 100 },
                },
                {
                    id: 'comp-2',
                    type: 'text',
                    props: {
                        label: 'Company Name',
                        placeholder: 'Enter company name',
                        required: false,
                    },
                    position: { x: 100, y: 200 },
                },
                {
                    id: 'comp-3',
                    type: 'email',
                    props: {
                        label: 'Email Address',
                        placeholder: 'name@example.com',
                        required: true,
                    },
                    position: { x: 100, y: 300 },
                },
            ],
        },
    ],
};

export const useBuilderStore = create<BuilderState>((set, get) => ({
    formDefinition: null,
    activeId: null,
    selectedComponentId: null, // Story 3.5 - primary selection
    selectedComponentIds: [], // Story 3.5 - all selections (multi-select)
    activePageId: 'page-1',
    isLoading: false,
    scale: 1,
    showGrid: true,
    activeLayer: 1,
    
    // Undo/Redo history stacks
    historyPast: [],
    historyFuture: [],

    initializeForm: (formId: string) => {
        set({ isLoading: true });
        setTimeout(() => {
            // Try to load persisted state first (UAT expects reload persistence)
            let loaded: FormDefinition | null = null;
            try {
                const raw = localStorage.getItem(getStorageKey(formId));
                if (raw) loaded = JSON.parse(raw) as FormDefinition;
            } catch {
                loaded = null;
            }

            const base = loaded || { ...MOCK_INITIAL_FORM, formId };
            const withLogic: FormDefinition = {
                ...base,
                logic: base.logic || { rules: [] },
            };

            set({
                formDefinition: withLogic,
                activePageId: withLogic.pages[0].id,
                isLoading: false,
                selectedComponentId: null, // Reset selection on form load
                selectedComponentIds: [], // Clear multi-selection
                historyPast: [], // Clear history on new form
                historyFuture: [],
            });
        }, 500);
    },

    setActiveId: (id) => set({ activeId: id }),
    
    // Story 3.5: Select component for property editing
    // additive = true means Ctrl+Click (add to selection or toggle)
    selectComponent: (id, additive = false) => {
        const state = get();
        
        if (id === null) {
            // Clear selection
            set({ selectedComponentId: null, selectedComponentIds: [] });
            return;
        }
        
        if (additive) {
            // Multi-select: toggle this component in the selection
            const currentIds = state.selectedComponentIds;
            const isAlreadySelected = currentIds.includes(id);
            
            if (isAlreadySelected) {
                // Remove from selection
                const newIds = currentIds.filter(cid => cid !== id);
                set({
                    selectedComponentIds: newIds,
                    selectedComponentId: newIds.length > 0 ? newIds[newIds.length - 1] : null,
                });
            } else {
                // Add to selection
                const newIds = [...currentIds, id];
                set({
                    selectedComponentIds: newIds,
                    selectedComponentId: id, // Make this the primary
                });
            }
        } else {
            // Single select: replace selection
            set({
                selectedComponentId: id,
                selectedComponentIds: [id],
            });
        }
    },

    // Clear all selections
    clearSelection: () => set({ selectedComponentId: null, selectedComponentIds: [] }),
    
    setScale: (scale) => set({ scale }),
    setShowGrid: (show) => set({ showGrid: show }),
    setActiveLayer: (layer) => set({ activeLayer: layer }),

    // Story 3.5: Helper to get the currently selected component (primary/first)
    getSelectedComponent: () => {
        const state = get();
        if (!state.selectedComponentId || !state.formDefinition) return null;
        
        const activePage = state.formDefinition.pages.find(p => p.id === state.activePageId);
        if (!activePage) return null;

        // Recursive find
        const findRecursive = (list: FormComponent[]): FormComponent | null => {
            for (const c of list) {
                if (c.id === state.selectedComponentId) return c;
                if (c.children) {
                    const found = findRecursive(c.children);
                    if (found) return found;
                }
            }
            return null;
        };

        return findRecursive(activePage.components);
    },

    // Multi-select helper: Get all selected components
    getSelectedComponents: () => {
        const state = get();
        if (state.selectedComponentIds.length === 0 || !state.formDefinition) return [];
        
        const activePage = state.formDefinition.pages.find(p => p.id === state.activePageId);
        if (!activePage) return [];

        const result: FormComponent[] = [];

        // Recursive find
        const findRecursive = (list: FormComponent[]) => {
            for (const c of list) {
                if (state.selectedComponentIds.includes(c.id)) {
                    result.push(c);
                }
                if (c.children) {
                    findRecursive(c.children);
                }
            }
        };

        findRecursive(activePage.components);
        return result;
    },

    // ═══════════════════════════════════════════════════════════════
    // UNDO/REDO HISTORY
    // ═══════════════════════════════════════════════════════════════

    /**
     * Save current form state to history (call before making changes)
     */
    pushToHistory: () => {
        const state = get();
        if (!state.formDefinition) return;
        
        const snapshot: FormSnapshot = {
            formDefinition: JSON.parse(JSON.stringify(state.formDefinition)),
            timestamp: Date.now(),
        };
        
        set((s) => ({
            historyPast: [...s.historyPast.slice(-MAX_HISTORY_SIZE + 1), snapshot],
            historyFuture: [], // Clear redo stack on new change
        }));
    },

    /**
     * Undo the last change
     */
    undo: () => {
        const state = get();
        if (state.historyPast.length === 0 || !state.formDefinition) return;
        
        // Save current state to future (redo) stack
        const currentSnapshot: FormSnapshot = {
            formDefinition: JSON.parse(JSON.stringify(state.formDefinition)),
            timestamp: Date.now(),
        };
        
        // Pop the last state from history
        const newPast = [...state.historyPast];
        const previousSnapshot = newPast.pop()!;
        
        set({
            formDefinition: previousSnapshot.formDefinition,
            historyPast: newPast,
            historyFuture: [currentSnapshot, ...state.historyFuture].slice(0, MAX_HISTORY_SIZE),
        });
        persistToStorage(get().formDefinition);
    },

    /**
     * Redo the last undone change
     */
    redo: () => {
        const state = get();
        if (state.historyFuture.length === 0 || !state.formDefinition) return;
        
        // Save current state to past (undo) stack
        const currentSnapshot: FormSnapshot = {
            formDefinition: JSON.parse(JSON.stringify(state.formDefinition)),
            timestamp: Date.now(),
        };
        
        // Pop the first state from future
        const newFuture = [...state.historyFuture];
        const nextSnapshot = newFuture.shift()!;
        
        set({
            formDefinition: nextSnapshot.formDefinition,
            historyPast: [...state.historyPast, currentSnapshot].slice(-MAX_HISTORY_SIZE),
            historyFuture: newFuture,
        });
        persistToStorage(get().formDefinition);
    },

    /**
     * Check if undo is available
     */
    canUndo: () => get().historyPast.length > 0,

    /**
     * Check if redo is available
     */
    canRedo: () => get().historyFuture.length > 0,

    // Generic Update Action (for Position, Style, etc.)
    updateComponent: (id, updates) => {
        get().pushToHistory(); // Save state before change
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
        persistToStorage(get().formDefinition);
    },

    // Story 3.5: Update just the props of a component (for property panel)
    updateComponentProps: (id, propUpdates) => {
        // Track property edits in undo/redo
        get().pushToHistory();
        set((state) => {
            if (!state.formDefinition) return state;
            const activePage = state.formDefinition.pages.find(p => p.id === state.activePageId);
            if (!activePage) return state;

            // Deep clone components
            const newComponents = JSON.parse(JSON.stringify(activePage.components)) as FormComponent[];

            // Recursive find and update props
            const updateRecursive = (list: FormComponent[]): boolean => {
                for (let i = 0; i < list.length; i++) {
                    if (list[i].id === id) {
                        list[i].props = { ...list[i].props, ...propUpdates };
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
        persistToStorage(get().formDefinition);
    },

    // Multi-select: Update props on ALL selected components
    updateMultipleComponentProps: (propUpdates) => {
        // Track bulk property edits in undo/redo
        get().pushToHistory();
        set((state) => {
            if (!state.formDefinition) return state;
            if (state.selectedComponentIds.length === 0) return state;
            
            const activePage = state.formDefinition.pages.find(p => p.id === state.activePageId);
            if (!activePage) return state;

            // Deep clone components
            const newComponents = JSON.parse(JSON.stringify(activePage.components)) as FormComponent[];
            const idsToUpdate = new Set(state.selectedComponentIds);

            // Recursive find and update props for all selected
            const updateRecursive = (list: FormComponent[]) => {
                for (let i = 0; i < list.length; i++) {
                    if (idsToUpdate.has(list[i].id)) {
                        list[i].props = { ...list[i].props, ...propUpdates };
                    }
                    if (list[i].children) {
                        updateRecursive(list[i].children!);
                    }
                }
            };

            updateRecursive(newComponents);

            const newPages = state.formDefinition.pages.map(p => 
                p.id === state.activePageId ? { ...p, components: newComponents } : p
            );

            return { formDefinition: { ...state.formDefinition, pages: newPages } };
        });
        persistToStorage(get().formDefinition);
    },

    // Story 3.5: Update global styles
    updateGlobalStyles: (updates) => {
        // Track global style edits in undo/redo
        get().pushToHistory();
        set((state) => {
            if (!state.formDefinition) return state;
            
            const currentGlobalStyles = state.formDefinition.globalStyles || DEFAULT_GLOBAL_STYLES;
            
            return {
                formDefinition: {
                    ...state.formDefinition,
                    globalStyles: {
                        ...currentGlobalStyles,
                        ...updates,
                    },
                },
            };
        });
        persistToStorage(get().formDefinition);
    },

    // Deprecated for Free-Form Canvas but kept for safety
    moveComponent: (_activeId, _overId) => {
        return;
    },

    addComponent: (component, _parentId, _index) => {
        get().pushToHistory(); // Save state before adding
        set((state) => {
            if (!state.formDefinition) return state;
            const activePage = state.formDefinition.pages.find(p => p.id === state.activePageId);
            if (!activePage) return state;

            const newComponents = JSON.parse(JSON.stringify(activePage.components)) as FormComponent[];

            // Simplified: Only adding to root for Free-Form Canvas
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
        persistToStorage(get().formDefinition);
    },

    // ═══════════════════════════════════════════════════════════════
    // LOGIC RULES (Story 3.6) - Authoring + Persistence Only
    // ═══════════════════════════════════════════════════════════════

    addRule: (rule) => {
        get().pushToHistory();
        set((state) => {
            if (!state.formDefinition) return state;
            const current = state.formDefinition.logic?.rules || [];
            return {
                formDefinition: {
                    ...state.formDefinition,
                    logic: {
                        rules: [...current, rule],
                    },
                },
            };
        });
        persistToStorage(get().formDefinition);
    },

    updateRule: (ruleId, updates) => {
        get().pushToHistory();
        set((state) => {
            if (!state.formDefinition) return state;
            const current = state.formDefinition.logic?.rules || [];
            return {
                formDefinition: {
                    ...state.formDefinition,
                    logic: {
                        rules: current.map(r => (r.id === ruleId ? { ...r, ...updates } : r)),
                    },
                },
            };
        });
        persistToStorage(get().formDefinition);
    },

    removeRule: (ruleId) => {
        get().pushToHistory();
        set((state) => {
            if (!state.formDefinition) return state;
            const current = state.formDefinition.logic?.rules || [];
            return {
                formDefinition: {
                    ...state.formDefinition,
                    logic: {
                        rules: current.filter(r => r.id !== ruleId),
                    },
                },
            };
        });
        persistToStorage(get().formDefinition);
    },

    moveRule: (ruleId, direction) => {
        get().pushToHistory();
        set((state) => {
            if (!state.formDefinition) return state;
            const current = [...(state.formDefinition.logic?.rules || [])];
            const idx = current.findIndex(r => r.id === ruleId);
            if (idx === -1) return state;

            const nextIdx = direction === 'up' ? idx - 1 : idx + 1;
            if (nextIdx < 0 || nextIdx >= current.length) return state;

            const tmp = current[idx];
            current[idx] = current[nextIdx];
            current[nextIdx] = tmp;

            return {
                formDefinition: {
                    ...state.formDefinition,
                    logic: { rules: current },
                },
            };
        });
        persistToStorage(get().formDefinition);
    },

    swapRules: (ruleIdA, ruleIdB) => {
        if (ruleIdA === ruleIdB) return;
        get().pushToHistory();
        set((state) => {
            if (!state.formDefinition) return state;
            const current = [...(state.formDefinition.logic?.rules || [])];
            const idxA = current.findIndex(r => r.id === ruleIdA);
            const idxB = current.findIndex(r => r.id === ruleIdB);
            if (idxA === -1 || idxB === -1) return state;

            const tmp = current[idxA];
            current[idxA] = current[idxB];
            current[idxB] = tmp;

            return {
                formDefinition: {
                    ...state.formDefinition,
                    logic: { rules: current },
                },
            };
        });
        persistToStorage(get().formDefinition);
    },

    toggleRuleEnabled: (ruleId, enabled) => {
        get().pushToHistory();
        set((state) => {
            if (!state.formDefinition) return state;
            const current = state.formDefinition.logic?.rules || [];
            return {
                formDefinition: {
                    ...state.formDefinition,
                    logic: {
                        rules: current.map(r => (r.id === ruleId ? { ...r, enabled } : r)),
                    },
                },
            };
        });
        persistToStorage(get().formDefinition);
    },

    // ═══════════════════════════════════════════════════════════════
    // OVERRIDE TRACKING HELPERS - For warning system
    // ═══════════════════════════════════════════════════════════════
    
    /**
     * Get all components that have any style overrides.
     * Used to warn users when making global changes.
     */
    getComponentsWithOverrides: () => {
        const state = get();
        if (!state.formDefinition) return [];
        
        const result: ComponentWithOverrides[] = [];
        
        // Recursive search through all pages and components
        const searchRecursive = (components: FormComponent[]) => {
            for (const comp of components) {
                if (hasStyleOverrides(comp.props.styleOverrides)) {
                    result.push({
                        id: comp.id,
                        label: comp.props.label || comp.type,
                        overriddenProperties: getOverriddenProperties(comp.props.styleOverrides),
                    });
                }
                if (comp.children) {
                    searchRecursive(comp.children);
                }
            }
        };
        
        for (const page of state.formDefinition.pages) {
            searchRecursive(page.components);
        }
        
        return result;
    },

    /**
     * Get components that would be affected by changing a specific global property.
     * Used to show targeted warnings.
     */
    getComponentsAffectedByGlobalChange: (propertyKey: keyof StyleOverrides) => {
        const state = get();
        if (!state.formDefinition) return [];
        
        const result: ComponentWithOverrides[] = [];
        
        const searchRecursive = (components: FormComponent[]) => {
            for (const comp of components) {
                const overrides = comp.props.styleOverrides;
                if (overrides && overrides[propertyKey] !== undefined) {
                    result.push({
                        id: comp.id,
                        label: comp.props.label || comp.type,
                        overriddenProperties: [propertyKey],
                    });
                }
                if (comp.children) {
                    searchRecursive(comp.children);
                }
            }
        };
        
        for (const page of state.formDefinition.pages) {
            searchRecursive(page.components);
        }
        
        return result;
    },

    /**
     * Clear all style overrides from all components.
     * Use when user confirms "Apply Global Style to All".
     */
    clearAllOverrides: () => {
        set((state) => {
            if (!state.formDefinition) return state;
            
            const clearRecursive = (components: FormComponent[]): FormComponent[] => {
                return components.map(comp => ({
                    ...comp,
                    props: {
                        ...comp.props,
                        styleOverrides: undefined,
                    },
                    children: comp.children ? clearRecursive(comp.children) : undefined,
                }));
            };
            
            const newPages = state.formDefinition.pages.map(page => ({
                ...page,
                components: clearRecursive(page.components),
            }));
            
            return {
                formDefinition: {
                    ...state.formDefinition,
                    pages: newPages,
                },
            };
        });
        persistToStorage(get().formDefinition);
    },

    /**
     * Clear a specific override property from all components.
     * Use when user wants to reset just one property globally.
     */
    clearOverridesForProperty: (propertyKey: keyof StyleOverrides) => {
        set((state) => {
            if (!state.formDefinition) return state;
            
            const clearRecursive = (components: FormComponent[]): FormComponent[] => {
                return components.map(comp => {
                    const overrides = comp.props.styleOverrides;
                    if (overrides && overrides[propertyKey] !== undefined) {
                        const newOverrides = { ...overrides };
                        delete newOverrides[propertyKey];
                        // If no overrides left, set to undefined
                        const hasRemaining = Object.values(newOverrides).some(v => v !== undefined);
                        return {
                            ...comp,
                            props: {
                                ...comp.props,
                                styleOverrides: hasRemaining ? newOverrides : undefined,
                            },
                            children: comp.children ? clearRecursive(comp.children) : undefined,
                        };
                    }
                    return {
                        ...comp,
                        children: comp.children ? clearRecursive(comp.children) : undefined,
                    };
                });
            };
            
            const newPages = state.formDefinition.pages.map(page => ({
                ...page,
                components: clearRecursive(page.components),
            }));
            
            return {
                formDefinition: {
                    ...state.formDefinition,
                    pages: newPages,
                },
            };
        });
        persistToStorage(get().formDefinition);
    },
}));
