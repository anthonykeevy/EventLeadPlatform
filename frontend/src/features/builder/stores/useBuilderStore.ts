/**
 * Builder Store - Story 3.3, 3.4 & 3.5
 * Manages the state of the Form Builder (FormDefinition)
 */

import { create } from 'zustand';
import { FormDefinition, FormComponent, GlobalStyles, DEFAULT_GLOBAL_STYLES, StyleOverrides, LogicRule, FormPage, BackgroundDefinition } from '../types/builder.types';
import { hasStyleOverrides, getOverriddenProperties } from '../utils/styleUtils';
import type { RuntimeRuleWarning } from '../../logic-engine/types';
import { createDraftVersion, formatFormVersionError, listFormVersions, updateDraftVersion } from '../api/formVersionsApi';
import { hashDefinition } from '../utils/hashUtils';
import { devLogger } from '../utils/devLogger';
import { ComponentRegistry } from '../registry/ComponentRegistry';
import { buildDefaultGridLayoutsByComponent } from '../utils/gridLayoutUtils';

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
    description: string;  // Human-readable action description for undo/redo UI
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
    isSaving: boolean;
    isDirty: boolean;
    lastSavedHash: string | null;
    loadError: string | null;
    saveError: string | null;
    loadedVersionNumber: number | null;
    loadedVersionStatus: string | null;
    hasNoVersions: boolean;
    
    // Canvas Viewport State
    scale: number;
    showGrid: boolean;
    activeLayer: 0 | 1; // 0 = Background, 1 = Functional
    
    // Live drag position (for real-time position display)
    dragPosition: { x: number; y: number } | null;
    setDragPosition: (position: { x: number; y: number } | null) => void;
    
    // Track if a component is currently being resized (to prevent drag end from interfering)
    resizingComponentId: string | null;
    setResizingComponentId: (id: string | null) => void;

    // Story 3.7: runtime warnings from evaluation (non-blocking)
    runtimeWarnings: RuntimeRuleWarning[];
    setRuntimeWarnings: (warnings: RuntimeRuleWarning[]) => void;
    clearRuntimeWarnings: () => void;
    
    // Undo/Redo History
    historyPast: FormSnapshot[];
    historyFuture: FormSnapshot[];
    
    // Actions
    initializeForm: (formId: string) => Promise<void>;
    /** Returns true if a network save occurred, false if skipped (no changes). */
    saveDraft: (formId: string, versionComment?: string) => Promise<boolean>;
    setActiveId: (id: string | null) => void;
    selectComponent: (id: string | null, additive?: boolean) => void; // Story 3.5 - additive = Ctrl+Click
    clearSelection: () => void; // Clear all selections
    setScale: (scale: number) => void;
    setShowGrid: (show: boolean) => void;
    setActiveLayer: (layer: 0 | 1) => void;
    moveComponent: (activeId: string, overId: string) => void;
    updateComponent: (id: string, updates: Partial<FormComponent>) => void;
    updateComponentProps: (id: string, props: Partial<FormComponent['props']>) => void; // Story 3.5
    updateComponentPositionAndProps: (id: string, position: { x: number; y: number }, props: Partial<FormComponent['props']>) => void; // Atomic position+props update
    updateMultipleComponentProps: (props: Partial<FormComponent['props']>) => void; // Multi-select bulk update
    addComponent: (component: FormComponent, parentId?: string, index?: number) => void;
    deleteSelectedComponents: () => void; // Delete key support (Story 3.7+)
    updateGlobalStyles: (updates: Partial<GlobalStyles>) => void; // Story 3.5
    getSelectedComponent: () => FormComponent | null; // Story 3.5 helper - returns first/primary
    getSelectedComponents: () => FormComponent[]; // Multi-select helper - returns all selected
    
    // Undo/Redo Actions
    undo: () => void;
    redo: () => void;
    canUndo: () => boolean;
    canRedo: () => boolean;
    pushToHistory: (description: string) => void; // Save current state with action description
    getNextUndoDescription: () => string | null; // Get description of next undo action
    getNextRedoDescription: () => string | null; // Get description of next redo action

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

function buildDefaultGlobalStyles(): GlobalStyles {
    const base = { ...DEFAULT_GLOBAL_STYLES };
    const components = Object.values(ComponentRegistry).map((component) => ({
        type: component.type,
        structure: component.structure,
    }));
    const defaultGridLayoutsByComponent = buildDefaultGridLayoutsByComponent(components, 'mixed');

    return {
        ...base,
        defaultGridLayoutsByComponent,
    };
}

function createEmptyFormDefinition(formId: string): FormDefinition {
    const globalStyles = buildDefaultGlobalStyles();

    return {
        schemaVersion: '1.0',
        formId,
        theme: {
            primaryColor: '#0055FF',
            backgroundColor: '#FFFFFF',
            fontFamily: 'Inter',
        },
        globalStyles,
        logic: { rules: [] },
        canvasSettings: {
            width: 1920,
            height: 980,
            gridSize: 8,
        },
        pages: [
            {
                id: 'page-1',
                title: 'Page 1',
                components: [],
            },
        ],
    };
}

function selectAuthoredPages(def: FormDefinition): FormPage[] {
    if (def.desktopPages && def.desktopPages.length > 0) return def.desktopPages;
    return def.pages ?? [];
}

function writeAuthoredPages(def: FormDefinition, pages: FormPage[]): FormDefinition {
    if (def.desktopPages && def.desktopPages.length > 0) {
        return { ...def, desktopPages: pages };
    }
    return { ...def, pages };
}

function selectAuthoredPagesForState(state: { formDefinition: FormDefinition | null }): FormPage[] {
    if (!state.formDefinition) return [];
    return selectAuthoredPages(state.formDefinition);
}

function writeAuthoredPagesForState(def: FormDefinition, pages: FormPage[]): FormDefinition {
    return writeAuthoredPages(def, pages);
}

function normalizeDefinitionForSave(def: FormDefinition): FormDefinition {
    const clone = JSON.parse(JSON.stringify(def)) as FormDefinition;
    const pages = selectAuthoredPages(clone);

    const normalizeComponents = (components: FormComponent[]): FormComponent[] => {
        return components.map((component) => {
            const next = { ...component };
            if (next.type === 'email') {
                const validation = { ...(next.props?.validation ?? {}) };
                if (validation.email === undefined) {
                    validation.email = true;
                }
                next.props = { ...next.props, validation };
            }
            if (next.children?.length) {
                next.children = normalizeComponents(next.children);
            }
            return next;
        });
    };

    // Normalize background definitions: strip Data URLs (Story 5.1 Task T04)
    const normalizeBackground = (background?: BackgroundDefinition): BackgroundDefinition | undefined => {
        if (!background) return undefined;
        
        // If background value is a Data URL, clear it (asset reference should be used instead)
        if (background.value && background.value.startsWith('data:')) {
            // If we have an asset reference, keep it and clear the Data URL value
            if (background.asset) {
                return {
                    ...background,
                    value: '', // Clear Data URL, asset reference is the source of truth
                };
            } else {
                // No asset reference and Data URL - remove background entirely
                return undefined;
            }
        }
        
        return background;
    };

    const normalizedPages = pages.map((page) => ({
        ...page,
        components: normalizeComponents(page.components),
        background: normalizeBackground(page.background),
    }));

    return writeAuthoredPages(clone, normalizedPages);
}

function withSafeDefaults(def: FormDefinition, formId: string): FormDefinition {
    const pages = def.pages && def.pages.length > 0 ? def.pages : [{ id: 'page-1', title: 'Page 1', components: [] }];
    const baseGlobalStyles = def.globalStyles || buildDefaultGlobalStyles();
    const components = Object.values(ComponentRegistry).map((component) => ({
        type: component.type,
        structure: component.structure,
    }));
    const defaultGridLayoutsByComponent =
        baseGlobalStyles.defaultGridLayoutsByComponent ??
        buildDefaultGridLayoutsByComponent(components, 'mixed');

    return {
        ...def,
        formId,
        theme: def.theme || {
            primaryColor: '#0055FF',
            backgroundColor: '#FFFFFF',
            fontFamily: 'Inter',
        },
        globalStyles: {
            ...baseGlobalStyles,
            defaultGridLayoutsByComponent,
        },
        logic: def.logic || { rules: [] },
        pages,
    };
}

export const useBuilderStore = create<BuilderState>((set, get) => ({
    formDefinition: null,
    activeId: null,
    selectedComponentId: null, // Story 3.5 - primary selection
    selectedComponentIds: [], // Story 3.5 - all selections (multi-select)
    activePageId: 'page-1',
    isLoading: false,
    isSaving: false,
    isDirty: false,
    lastSavedHash: null,
    loadError: null,
    saveError: null,
    loadedVersionNumber: null,
    loadedVersionStatus: null,
    hasNoVersions: false,
    scale: 1,
    showGrid: true,
    activeLayer: 1,
    dragPosition: null,
    setDragPosition: (position) => set({ dragPosition: position }),
    resizingComponentId: null,
    setResizingComponentId: (id) => set({ resizingComponentId: id }),

    runtimeWarnings: [],
    setRuntimeWarnings: (warnings) => set({ runtimeWarnings: warnings }),
    clearRuntimeWarnings: () => set({ runtimeWarnings: [] }),
    
    // Undo/Redo history stacks
    historyPast: [],
    historyFuture: [],

    initializeForm: async (formId: string) => {
        set({ isLoading: true, loadError: null, hasNoVersions: false });

        try {
            const versions = await listFormVersions(formId);
            if (!versions || versions.length === 0) {
                const empty = createEmptyFormDefinition(formId);
                set({
                    formDefinition: empty,
                    activePageId: empty.pages[0].id,
                    isLoading: false,
                    selectedComponentId: null,
                    selectedComponentIds: [],
                    historyPast: [],
                    historyFuture: [],
                    loadedVersionNumber: null,
                    loadedVersionStatus: null,
                    hasNoVersions: true,
                    isDirty: false,
                    lastSavedHash: hashDefinition(empty),
                });
                persistToStorage(empty);
                return;
            }

            // Prefer latest DRAFT; otherwise latest version.
            const preferred = versions.find(v => v.status === 'DRAFT') || versions[0];
            const loaded = withSafeDefaults(preferred.definition as unknown as FormDefinition, formId);
            
            // Migrate components in authored pages (prefer desktopPages when present)
            const authoredPages = selectAuthoredPages(loaded);
            const migratedAuthoredPages = authoredPages;
            const migratedLoaded = writeAuthoredPages(loaded, migratedAuthoredPages);
            const firstPageId = migratedAuthoredPages[0]?.id || 'page-1';

            set({
                formDefinition: migratedLoaded,
                activePageId: firstPageId,
                isLoading: false,
                selectedComponentId: null,
                selectedComponentIds: [],
                historyPast: [],
                historyFuture: [],
                loadedVersionNumber: preferred.versionNumber,
                loadedVersionStatus: preferred.status,
                hasNoVersions: false,
                isDirty: false,
                lastSavedHash: hashDefinition(migratedLoaded),
            });
            persistToStorage(migratedLoaded);
        } catch (err: unknown) {
            // Check HTTP status code to determine appropriate handling
            const axiosError = err as { response?: { status?: number }; code?: string };
            const httpStatus = axiosError?.response?.status;
            const isNetworkError = axiosError?.code === 'ERR_NETWORK' || !axiosError?.response;
            
            // 403 Forbidden - User doesn't have access to this form
            // Do NOT fall back to localStorage - block access for this user
            // BUT preserve localStorage - another user with access may need it later
            if (httpStatus === 403) {
                devLogger.warn('form.access.denied', { formId, httpStatus });
                set({
                    formDefinition: null,
                    isLoading: false,
                    loadError: 'Access Denied: You do not have permission to view this form.',
                    selectedComponentId: null,
                    selectedComponentIds: [],
                    historyPast: [],
                    historyFuture: [],
                    loadedVersionNumber: null,
                    loadedVersionStatus: null,
                    hasNoVersions: false,
                    isDirty: false,
                    lastSavedHash: null,
                });
                // NOTE: Do NOT clear localStorage - it may belong to another user
                // who has proper access and needs their unsaved work preserved.
                // The version system handles conflicts when they next open the form.
                return;
            }
            
            // 404 Not Found - Form doesn't exist
            // Do NOT fall back to localStorage - form was deleted or never existed
            // BUT preserve localStorage - could be network glitch, or form may be restored
            if (httpStatus === 404) {
                devLogger.warn('form.not.found', { formId, httpStatus });
                set({
                    formDefinition: null,
                    isLoading: false,
                    loadError: 'Form Not Found: This form does not exist or has been deleted.',
                    selectedComponentId: null,
                    selectedComponentIds: [],
                    historyPast: [],
                    historyFuture: [],
                    loadedVersionNumber: null,
                    loadedVersionStatus: null,
                    hasNoVersions: false,
                    isDirty: false,
                    lastSavedHash: null,
                });
                // NOTE: Do NOT clear localStorage - could be temporary issue
                // or form may be restored by admin. Let version system handle conflicts.
                return;
            }
            
            // Network error (offline) or server error (5xx) - allow localStorage fallback
            // This supports offline editing scenarios
            if (isNetworkError || (httpStatus && httpStatus >= 500)) {
                devLogger.info('form.load.fallback', { 
                    formId, 
                    httpStatus, 
                    isNetworkError,
                    reason: isNetworkError ? 'network-error' : 'server-error'
                });
                
                let loaded: FormDefinition | null = null;
                try {
                    const raw = localStorage.getItem(getStorageKey(formId));
                    if (raw) loaded = JSON.parse(raw) as FormDefinition;
                } catch {
                    loaded = null;
                }

                const fallback = withSafeDefaults(loaded || createEmptyFormDefinition(formId), formId);
                const authoredPages = selectAuthoredPages(fallback);
                const migratedAuthoredPages = authoredPages;
                const migratedFallback = writeAuthoredPages(fallback, migratedAuthoredPages);
                const firstPageId = migratedAuthoredPages[0]?.id || 'page-1';
                
                set({
                    formDefinition: migratedFallback,
                    activePageId: firstPageId,
                    isLoading: false,
                    loadError: isNetworkError 
                        ? 'Offline: Working with locally saved data. Changes will sync when connection is restored.'
                        : `Server Error: Working with locally saved data. (${formatFormVersionError(err)})`,
                    selectedComponentId: null,
                    selectedComponentIds: [],
                    historyPast: [],
                    historyFuture: [],
                    loadedVersionNumber: null,
                    loadedVersionStatus: null,
                    hasNoVersions: loaded ? false : true,
                    isDirty: true,
                    lastSavedHash: hashDefinition(fallback),
                });
                persistToStorage(migratedFallback);
                return;
            }
            
            // Other errors (e.g., 400, 401) - show error, don't fall back
            devLogger.error('form.load.error', { formId, httpStatus, error: formatFormVersionError(err) });
            set({
                formDefinition: null,
                isLoading: false,
                loadError: formatFormVersionError(err),
                selectedComponentId: null,
                selectedComponentIds: [],
                historyPast: [],
                historyFuture: [],
                loadedVersionNumber: null,
                loadedVersionStatus: null,
                hasNoVersions: false,
                isDirty: false,
                lastSavedHash: null,
            });
        }
    },

    saveDraft: async (formId: string, versionComment?: string) => {
        const state = get();
        const def = state.formDefinition;
        if (!def) {
            set({ saveError: 'Nothing to save (formDefinition is empty).' });
            throw new Error('Nothing to save');
        }

        const normalizedDef = normalizeDefinitionForSave(def);
        const normalizedHash = hashDefinition(normalizedDef);
        if (normalizedHash !== hashDefinition(def)) {
            set({ formDefinition: normalizedDef });
            persistToStorage(normalizedDef);
        }

        if (state.lastSavedHash && normalizedHash === state.lastSavedHash) {
            set({ isDirty: false, saveError: null });
            persistToStorage(normalizedDef);
            return false;
        }

        set({ isSaving: true, saveError: null });
        try {
            // Deterministic strategy:
            // - If currently loaded version is a DRAFT, update it
            // - Otherwise, create a new DRAFT version
            if (state.loadedVersionStatus === 'DRAFT' && state.loadedVersionNumber) {
                const res = await updateDraftVersion(formId, state.loadedVersionNumber, normalizedDef as unknown as Record<string, unknown>, versionComment);
                set({
                    isSaving: false,
                    loadedVersionNumber: res.versionNumber,
                    loadedVersionStatus: res.status,
                    hasNoVersions: false,
                    isDirty: false,
                    lastSavedHash: normalizedHash,
                });
                persistToStorage(normalizedDef);
                return true;
            }

            const res = await createDraftVersion(formId, normalizedDef as unknown as Record<string, unknown>, versionComment);
            set({
                isSaving: false,
                loadedVersionNumber: res.versionNumber,
                loadedVersionStatus: res.status,
                hasNoVersions: false,
                isDirty: false,
                lastSavedHash: normalizedHash,
            });
            persistToStorage(normalizedDef);
            return true;
        } catch (err: unknown) {
            set({ isSaving: false, saveError: formatFormVersionError(err) });
            throw err;
        }
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
        
        const pages = selectAuthoredPages(state.formDefinition);
        const activePage = pages.find(p => p.id === state.activePageId);
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
        
        const pages = selectAuthoredPages(state.formDefinition);
        const activePage = pages.find(p => p.id === state.activePageId);
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
     * @param description - Human-readable description of the action about to be performed
     */
    pushToHistory: (description: string) => {
        const state = get();
        if (!state.formDefinition) return;
        
        const snapshot: FormSnapshot = {
            formDefinition: JSON.parse(JSON.stringify(state.formDefinition)),
            timestamp: Date.now(),
            description,
        };
        
        set((s) => ({
            historyPast: [...s.historyPast.slice(-MAX_HISTORY_SIZE + 1), snapshot],
            historyFuture: [], // Clear redo stack on new change
        }));
        
        // Log history push event
        devLogger.info('history.push', {
            description,
            stackSize: get().historyPast.length,
        });
    },
    
    /**
     * Get the description of the next undo action (if available)
     */
    getNextUndoDescription: () => {
        const state = get();
        if (state.historyPast.length === 0) return null;
        return state.historyPast[state.historyPast.length - 1].description;
    },
    
    /**
     * Get the description of the next redo action (if available)
     */
    getNextRedoDescription: () => {
        const state = get();
        if (state.historyFuture.length === 0) return null;
        return state.historyFuture[0].description;
    },

    /**
     * Undo the last change
     */
    undo: () => {
        const state = get();
        if (state.historyPast.length === 0 || !state.formDefinition) return;
        
        // Pop the last state from history
        const newPast = [...state.historyPast];
        const previousSnapshot = newPast.pop()!;
        
        // Save current state to future (redo) stack with the description of what was undone
        const currentSnapshot: FormSnapshot = {
            formDefinition: JSON.parse(JSON.stringify(state.formDefinition)),
            timestamp: Date.now(),
            description: previousSnapshot.description, // Use the description of the undone action
        };
        
        set({
            formDefinition: previousSnapshot.formDefinition,
            historyPast: newPast,
            historyFuture: [currentSnapshot, ...state.historyFuture].slice(0, MAX_HISTORY_SIZE),
        });
        persistToStorage(get().formDefinition);
        const def = get().formDefinition;
        if (def) {
            const h = hashDefinition(def);
            set({ isDirty: !(get().lastSavedHash && h === get().lastSavedHash) });
        }
        
        // Log undo event
        devLogger.info('history.undo', {
            description: previousSnapshot.description,
        });
    },

    /**
     * Redo the last undone change
     */
    redo: () => {
        const state = get();
        if (state.historyFuture.length === 0 || !state.formDefinition) return;
        
        // Pop the first state from future
        const newFuture = [...state.historyFuture];
        const nextSnapshot = newFuture.shift()!;
        
        // Save current state to past (undo) stack with the description of what will be redone
        const currentSnapshot: FormSnapshot = {
            formDefinition: JSON.parse(JSON.stringify(state.formDefinition)),
            timestamp: Date.now(),
            description: nextSnapshot.description, // Use the description of the action being redone
        };
        
        set({
            formDefinition: nextSnapshot.formDefinition,
            historyPast: [...state.historyPast, currentSnapshot].slice(-MAX_HISTORY_SIZE),
            historyFuture: newFuture,
        });
        persistToStorage(get().formDefinition);
        const def = get().formDefinition;
        if (def) {
            const h = hashDefinition(def);
            set({ isDirty: !(get().lastSavedHash && h === get().lastSavedHash) });
        }
        
        // Log redo event
        devLogger.info('history.redo', {
            description: nextSnapshot.description,
        });
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
        // Generate description based on what's being updated
        const component = get().getSelectedComponent();
        const componentLabel = component?.props.label || component?.type || 'component';
        let description = `Update ${componentLabel}`;
        if (updates.position) {
            description = `Move ${componentLabel} to (${updates.position.x}, ${updates.position.y})`;
        }
        get().pushToHistory(description);
        set((state) => {
            if (!state.formDefinition) return state;
            const pages = selectAuthoredPages(state.formDefinition);
            const activePage = pages.find(p => p.id === state.activePageId);
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

            const newPages = pages.map(p => 
                p.id === state.activePageId ? { ...p, components: newComponents } : p
            );

            return { formDefinition: writeAuthoredPagesForState(state.formDefinition, newPages) };
        });
        persistToStorage(get().formDefinition);
        set({ isDirty: true });
    },

    // Story 3.5: Update just the props of a component (for property panel)
    updateComponentProps: (id, propUpdates) => {
        // Generate description based on property being updated
        const component = get().getSelectedComponent();
        const componentLabel = component?.props.label || component?.type || 'component';
        const propKeys = Object.keys(propUpdates);
        const propName = propKeys.length === 1 ? propKeys[0] : `${propKeys.length} properties`;
        const description = `Update ${propName} on ${componentLabel}`;
        get().pushToHistory(description);
        set((state) => {
            if (!state.formDefinition) return state;
            const pages = selectAuthoredPages(state.formDefinition);
            const activePage = pages.find(p => p.id === state.activePageId);
            if (!activePage) return state;

            // Deep clone components
            const newComponents = JSON.parse(JSON.stringify(activePage.components)) as FormComponent[];

            // Recursive find and update props
            const updateRecursive = (list: FormComponent[]): boolean => {
                for (let i = 0; i < list.length; i++) {
                    if (list[i].id === id) {
                        // Handle undefined/null values explicitly - Object.entries() omits undefined values!
                        // So we need to use Object.keys() and access the value directly
                        const updatedProps = { ...list[i].props };
                        for (const key of Object.keys(propUpdates)) {
                            const value = (propUpdates as any)[key];
                            if (value === undefined) {
                                // For undefined, delete the property to allow inheritance
                                delete updatedProps[key as keyof typeof updatedProps];
                            } else {
                                // For null or other values, explicitly set it
                                // This is important for gridLayout: null (opt-out) and gridLayout: undefined (inherit)
                                updatedProps[key as keyof typeof updatedProps] = value;
                            }
                        }
                        // Create a new component object to ensure React detects the change
                        list[i] = { ...list[i], props: updatedProps };
                        return true;
                    }
                    if (list[i].children && updateRecursive(list[i].children!)) {
                        return true;
                    }
                }
                return false;
            };

            updateRecursive(newComponents);

            const newPages = pages.map(p => 
                p.id === state.activePageId ? { ...p, components: newComponents } : p
            );

            return { formDefinition: writeAuthoredPagesForState(state.formDefinition, newPages) };
        });
        persistToStorage(get().formDefinition);
        set({ isDirty: true });
    },

    // Atomic update of position AND props in a single render (for anchored scaling)
    updateComponentPositionAndProps: (id, position, propUpdates) => {
        const component = get().getSelectedComponent();
        const componentLabel = component?.props.label || component?.type || 'component';
        const description = `Scale ${componentLabel}`;
        get().pushToHistory(description);
        set((state) => {
            if (!state.formDefinition) return state;
            const pages = selectAuthoredPages(state.formDefinition);
            const activePage = pages.find(p => p.id === state.activePageId);
            if (!activePage) return state;

            const newComponents = JSON.parse(JSON.stringify(activePage.components)) as FormComponent[];

            const updateRecursive = (list: FormComponent[]): boolean => {
                for (let i = 0; i < list.length; i++) {
                    if (list[i].id === id) {
                        // Update position
                        list[i] = { ...list[i], position };
                        // Merge props
                        const updatedProps = { ...list[i].props };
                        for (const key of Object.keys(propUpdates)) {
                            const value = (propUpdates as any)[key];
                            if (value === undefined) {
                                delete updatedProps[key as keyof typeof updatedProps];
                            } else {
                                updatedProps[key as keyof typeof updatedProps] = value;
                            }
                        }
                        list[i] = { ...list[i], props: updatedProps };
                        return true;
                    }
                    if (list[i].children && updateRecursive(list[i].children!)) {
                        return true;
                    }
                }
                return false;
            };

            updateRecursive(newComponents);

            const newPages = pages.map(p => 
                p.id === state.activePageId ? { ...p, components: newComponents } : p
            );

            return { formDefinition: writeAuthoredPagesForState(state.formDefinition, newPages) };
        });
        persistToStorage(get().formDefinition);
        set({ isDirty: true });
    },

    // Multi-select: Update props on ALL selected components
    updateMultipleComponentProps: (propUpdates) => {
        // Generate description for bulk update
        const count = get().selectedComponentIds.length;
        const propKeys = Object.keys(propUpdates);
        const propName = propKeys.length === 1 ? propKeys[0] : `${propKeys.length} properties`;
        const description = `Bulk update ${propName} on ${count} component(s)`;
        get().pushToHistory(description);
        set((state) => {
            if (!state.formDefinition) return state;
            if (state.selectedComponentIds.length === 0) return state;
            
            const pages = selectAuthoredPages(state.formDefinition);
            const activePage = pages.find(p => p.id === state.activePageId);
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

            const newPages = pages.map(p => 
                p.id === state.activePageId ? { ...p, components: newComponents } : p
            );

            return { formDefinition: writeAuthoredPagesForState(state.formDefinition, newPages) };
        });
        persistToStorage(get().formDefinition);
        set({ isDirty: true });
    },

    // Story 3.5: Update global styles
    updateGlobalStyles: (updates) => {
        // Generate description for global style update
        const styleKeys = Object.keys(updates);
        const styleName = styleKeys.length === 1 ? styleKeys[0] : `${styleKeys.length} styles`;
        const description = `Update global ${styleName}`;
        get().pushToHistory(description);
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
        set({ isDirty: true });
    },

    // Deprecated for Free-Form Canvas but kept for safety
    moveComponent: (_activeId, _overId) => {
        return;
    },

    addComponent: (component, _parentId, _index) => {
        const componentLabel = component.props?.label || component.type;
        const description = `Add ${componentLabel}`;
        get().pushToHistory(description);
        set((state) => {
            if (!state.formDefinition) return state;
            const pages = selectAuthoredPages(state.formDefinition);
            const activePage = pages.find(p => p.id === state.activePageId);
            if (!activePage) return state;

            const newComponents = JSON.parse(JSON.stringify(activePage.components)) as FormComponent[];

            // Simplified: Only adding to root for Free-Form Canvas
            newComponents.push(component);

            const newPages = pages.map(p => 
                p.id === state.activePageId ? { ...p, components: newComponents } : p
            );

            return {
                formDefinition: {
                    ...writeAuthoredPagesForState(state.formDefinition, newPages)
                }
            };
        });
        persistToStorage(get().formDefinition);
        set({ isDirty: true });
    },

    /**
     * Delete currently selected component(s) (supports multi-select).
     * Integrated with undo/redo by pushing state before mutation.
     */
    deleteSelectedComponents: () => {
        const state = get();
        if (!state.formDefinition) return;
        if (state.selectedComponentIds.length === 0) return;

        const count = state.selectedComponentIds.length;
        const description = `Delete ${count} component(s)`;
        get().pushToHistory(description);

        set((s) => {
            if (!s.formDefinition) return s;
            const pages = selectAuthoredPages(s.formDefinition);
            const activePage = pages.find(p => p.id === s.activePageId);
            if (!activePage) return s;

            const idsToDelete = new Set(s.selectedComponentIds);

            const removeRecursive = (list: FormComponent[]): FormComponent[] => {
                const next: FormComponent[] = [];
                for (const c of list) {
                    if (idsToDelete.has(c.id)) {
                        continue;
                    }
                    if (c.children?.length) {
                        next.push({ ...c, children: removeRecursive(c.children) });
                    } else {
                        next.push(c);
                    }
                }
                return next;
            };

            const newComponents = removeRecursive(activePage.components);
            const newPages = pages.map(p =>
                p.id === s.activePageId ? { ...p, components: newComponents } : p
            );

            return {
                formDefinition: writeAuthoredPagesForState(s.formDefinition, newPages),
                selectedComponentId: null,
                selectedComponentIds: [],
                activeId: null,
            };
        });

        persistToStorage(get().formDefinition);
        set({ isDirty: true });
    },

    // ═══════════════════════════════════════════════════════════════
    // LOGIC RULES (Story 3.6) - Authoring + Persistence Only
    // ═══════════════════════════════════════════════════════════════

    addRule: (rule) => {
        const description = `Add logic rule "${rule.name || rule.id}"`;
        get().pushToHistory(description);
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
        set({ isDirty: true });
    },

    updateRule: (ruleId, updates) => {
        const currentState = get();
        const currentRule = currentState.formDefinition?.logic?.rules?.find(r => r.id === ruleId);
        const ruleName = currentRule?.name || ruleId;
        const description = `Update logic rule "${ruleName}"`;
        get().pushToHistory(description);
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
        set({ isDirty: true });
    },

    removeRule: (ruleId) => {
        const currentState = get();
        const currentRule = currentState.formDefinition?.logic?.rules?.find(r => r.id === ruleId);
        const ruleName = currentRule?.name || ruleId;
        const description = `Remove logic rule "${ruleName}"`;
        get().pushToHistory(description);
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
        set({ isDirty: true });
    },

    moveRule: (ruleId, direction) => {
        const currentState = get();
        const currentRule = currentState.formDefinition?.logic?.rules?.find(r => r.id === ruleId);
        const ruleName = currentRule?.name || ruleId;
        const description = `Move logic rule "${ruleName}" ${direction}`;
        get().pushToHistory(description);
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
        set({ isDirty: true });
    },

    swapRules: (ruleIdA, ruleIdB) => {
        if (ruleIdA === ruleIdB) return;
        const description = `Swap logic rules`;
        get().pushToHistory(description);
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
        set({ isDirty: true });
    },

    toggleRuleEnabled: (ruleId, enabled) => {
        const currentState = get();
        const currentRule = currentState.formDefinition?.logic?.rules?.find(r => r.id === ruleId);
        const ruleName = currentRule?.name || ruleId;
        const description = `${enabled ? 'Enable' : 'Disable'} logic rule "${ruleName}"`;
        get().pushToHistory(description);
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
        set({ isDirty: true });
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
        set({ isDirty: true });
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
        set({ isDirty: true });
    },
}));
