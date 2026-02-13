import React from 'react';
import { Settings, X, Layers, Users, GitBranch, SlidersHorizontal } from 'lucide-react';
import { useBuilderStore } from '../stores/useBuilderStore';
import { ComponentRegistry } from '../registry/ComponentRegistry';
import { DEFAULT_GLOBAL_STYLES, FormPage, FormComponent, StyleOverrides } from '../types/builder.types';
import { GeneralSection } from './properties/GeneralSection';
import { ValidationSection } from './properties/ValidationSection';
import { AppearanceSection } from './properties/AppearanceSection';
import { GlobalStylesPanel } from './properties/GlobalStylesPanel';
import { BackgroundPropertiesPanel } from './properties/BackgroundPropertiesPanel';
import { DataExportSection } from './properties/DataExportSection';
import { ButtonPropertiesSection } from './properties/ButtonPropertiesSection';
import { TermsPropertiesSection } from './properties/TermsPropertiesSection';
import { TextareaPropertiesSection } from './properties/TextareaPropertiesSection';
import { OptionsSection } from './properties/OptionsSection';
import { DatePropertiesSection } from './properties/DatePropertiesSection';
import GridLayoutSection from './properties/GridLayoutSection';
import { ObjectLayoutSection } from './properties/ObjectLayoutSection';
import { LogicPanel } from './logic/LogicPanel';

/**
 * Type compatibility map for Must Match Field filtering
 * Defines which component types can match with each other
 */
const TYPE_COMPATIBILITY: Record<string, string[]> = {
    'text': ['text', 'email', 'phone', 'first-name', 'textarea'],
    'email': ['email', 'text'],
    'phone': ['phone', 'text'],
    'first-name': ['first-name', 'text'],
    'textarea': ['textarea', 'text'],
    'number': ['number'],
    'date': ['date'],
    'checkbox': ['checkbox'],
    'radio': ['radio'],
    'select': ['select'],
};

export const PropertiesPanel: React.FC = () => {
    const { 
        selectedComponentId, 
        selectedComponentIds,
        selectComponent,
        clearSelection,
        formDefinition,
        updateComponentProps,
        updateMultipleComponentProps,
        updateGlobalStyles,
        updatePageBackground,
        getSelectedComponent,
        getSelectedComponents,
        activeLayer,
        activePageId,
    } = useBuilderStore();

    const selectedComponent = getSelectedComponent();
    const selectedComponents = getSelectedComponents();
    const isMultiSelect = selectedComponentIds.length > 1;
    const globalStyles = formDefinition?.globalStyles || DEFAULT_GLOBAL_STYLES;
    const [bulkStyleOverrides, setBulkStyleOverrides] = React.useState<StyleOverrides>({});
    
    // Use same authored pages as canvas (desktopPages when present, else pages)
    const authoredPages = formDefinition?.desktopPages?.length
        ? formDefinition.desktopPages
        : formDefinition?.pages ?? [];
    const currentPage = authoredPages.find(p => p.id === activePageId);
    const pageBackground = currentPage?.background;

    // Right panel tabs (Inspector/Logic). Logic is form-level and works without selection.
    const [activeTab, setActiveTab] = React.useState<'inspector' | 'logic'>(() => {
        try {
            const raw = localStorage.getItem('builder-right-panel-tab');
            if (raw === 'logic' || raw === 'inspector') return raw;
        } catch {
            // ignore
        }
        return 'inspector';
    });

    React.useEffect(() => {
        try {
            localStorage.setItem('builder-right-panel-tab', activeTab);
        } catch {
            // ignore
        }
    }, [activeTab]);
    
    // ═══════════════════════════════════════════════════════════════════════════════
    // ALL HOOKS MUST BE CALLED BEFORE ANY EARLY RETURNS
    // ═══════════════════════════════════════════════════════════════════════════════
    
    // Get all components on current page for Must Match Field dropdown
    // Exclude the currently selected component and filter by type compatibility
    // NOTE: This must be called unconditionally (before early returns)
    const availableFieldsForMatch = React.useMemo(() => {
        if (!currentPage || !selectedComponent) return [];
        
        const currentType = selectedComponent.type;
        const compatibleTypes = TYPE_COMPATIBILITY[currentType] || [currentType];
        
        return currentPage.components
            .filter(c => c.id !== selectedComponentId)
            .filter(c => !['submit-button', 'divider', 'header', 'paragraph'].includes(c.type))
            .filter(c => compatibleTypes.includes(c.type))
            .map(c => ({
                id: c.id,
                label: c.props.label || c.type,
                exportName: c.props.exportName,
                type: c.type,
            }));
    }, [currentPage, selectedComponentId, selectedComponent]);

    // Handler for updating page background (uses store action for undo + persist)
    const handleBackgroundChange = React.useCallback((updates: Partial<NonNullable<FormPage['background']>>) => {
        updatePageBackground(updates);
    }, [updatePageBackground]);

    // Handle property updates
    const handlePropsChange = React.useCallback((updates: Partial<NonNullable<typeof selectedComponent>['props']>) => {
        if (!selectedComponentId) return;
        updateComponentProps(selectedComponentId, updates);
    }, [selectedComponentId, updateComponentProps]);

    // Handle validation updates - uses functional state update to avoid race conditions
    const handleValidationChange = React.useCallback((updates: Partial<NonNullable<NonNullable<typeof selectedComponent>['props']['validation']>>) => {
        if (!selectedComponentId) return;
        
        useBuilderStore.setState((state) => {
            if (!state.formDefinition) return state;
            
            const activePage = state.formDefinition.pages.find(p => p.id === state.activePageId);
            if (!activePage) return state;
            
            // Find the component
            const findComponent = (components: typeof activePage.components): typeof activePage.components[0] | null => {
                for (const comp of components) {
                    if (comp.id === selectedComponentId) return comp;
                    if (comp.children) {
                        const found = findComponent(comp.children);
                        if (found) return found;
                    }
                }
                return null;
            };
            
            const currentComponent = findComponent(activePage.components);
            if (!currentComponent) return state;
            
            // Get current validation from STATE (not from closure)
            const currentValidation = currentComponent.props.validation || {};
            
            // Update the component in the state tree
            const updateComponentInList = (components: typeof activePage.components): typeof activePage.components => {
                return components.map(comp => {
                    if (comp.id === selectedComponentId) {
                        return {
                            ...comp,
                            props: {
                                ...comp.props,
                                validation: { ...currentValidation, ...updates },
                            },
                        };
                    }
                    if (comp.children) {
                        return {
                            ...comp,
                            children: updateComponentInList(comp.children),
                        };
                    }
                    return comp;
                });
            };
            
            const newComponents = updateComponentInList(activePage.components);
            const newPages = state.formDefinition.pages.map(p =>
                p.id === state.activePageId ? { ...p, components: newComponents } : p
            );
            
            return {
                formDefinition: {
                    ...state.formDefinition,
                    pages: newPages,
                },
            };
        });
    }, [selectedComponentId]);

    // Merge helper that removes keys when value is undefined/null
    const mergeStyleOverrides = React.useCallback((base: StyleOverrides, updates: Partial<StyleOverrides>) => {
        const next: StyleOverrides = { ...base };
        Object.entries(updates).forEach(([k, v]) => {
            if (v === undefined || v === null) {
                delete next[k as keyof StyleOverrides];
            } else {
                next[k as keyof StyleOverrides] = v as any;
            }
        });
        return next;
    }, []);

    // Reset bulk overrides whenever selection changes (must run before any early returns)
    React.useEffect(() => {
        setBulkStyleOverrides({});
    }, [selectedComponentIds]);

    // Handle style overrides updates - uses functional state update to avoid race conditions
    const handleStyleOverridesChange = React.useCallback((updates: Partial<NonNullable<NonNullable<typeof selectedComponent>['props']['styleOverrides']>> | undefined) => {
        if (!selectedComponentId) return;
        
        useBuilderStore.setState((state) => {
            if (!state.formDefinition) return state;
            
            const activePage = state.formDefinition.pages.find(p => p.id === state.activePageId);
            if (!activePage) return state;
            
            // Find the component and get its CURRENT overrides from state (not from closure)
            const findComponent = (components: typeof activePage.components): typeof activePage.components[0] | null => {
                for (const comp of components) {
                    if (comp.id === selectedComponentId) return comp;
                    if (comp.children) {
                        const found = findComponent(comp.children);
                        if (found) return found;
                    }
                }
                return null;
            };
            
            const currentComponent = findComponent(activePage.components);
            if (!currentComponent) return state;
            
            // Get current overrides from STATE (not from closure)
            const currentOverrides = currentComponent.props.styleOverrides || {};
            
            // Determine new overrides
            let newOverrides: StyleOverrides | undefined;
            if (!updates || Object.keys(updates).length === 0) {
                // Clear all overrides
                newOverrides = undefined;
            } else {
                // Merge with current overrides
                newOverrides = mergeStyleOverrides(currentOverrides, updates);
            }
            
            // Update the component in the state tree
            const updateComponentInList = (components: typeof activePage.components): typeof activePage.components => {
                return components.map(comp => {
                    if (comp.id === selectedComponentId) {
                        return {
                            ...comp,
                            props: {
                                ...comp.props,
                                styleOverrides: newOverrides,
                            },
                        };
                    }
                    if (comp.children) {
                        return {
                            ...comp,
                            children: updateComponentInList(comp.children),
                        };
                    }
                    return comp;
                });
            };
            
            const newComponents = updateComponentInList(activePage.components);
            const newPages = state.formDefinition.pages.map(p =>
                p.id === state.activePageId ? { ...p, components: newComponents } : p
            );
            
            return {
                formDefinition: {
                    ...state.formDefinition,
                    pages: newPages,
                },
            };
        });
    }, [selectedComponentId]);

    // ═══════════════════════════════════════════════════════════════════════════════
    // EARLY RETURNS - AFTER ALL HOOKS
    // ═══════════════════════════════════════════════════════════════════════════════

    // Panel styling - width is controlled by ResizablePanel parent
    const panelClassName = "w-full h-full bg-white dark:bg-gray-900 border-l border-gray-200 dark:border-gray-700 flex flex-col overflow-hidden";

    const TabsHeader = () => (
        <div className="flex items-center border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/40">
            <button
                onClick={() => setActiveTab('inspector')}
                className={`flex-1 px-3 py-2 text-xs font-medium flex items-center justify-center gap-2 transition-colors ${
                    activeTab === 'inspector'
                        ? 'text-gray-900 dark:text-gray-100 bg-white dark:bg-gray-900 border-b-2 border-teal-500'
                        : 'text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200'
                }`}
                title="Inspector"
            >
                <SlidersHorizontal size={14} />
                Inspector
            </button>
            <button
                onClick={() => setActiveTab('logic')}
                className={`flex-1 px-3 py-2 text-xs font-medium flex items-center justify-center gap-2 transition-colors ${
                    activeTab === 'logic'
                        ? 'text-gray-900 dark:text-gray-100 bg-white dark:bg-gray-900 border-b-2 border-indigo-500'
                        : 'text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200'
                }`}
                title="Logic"
            >
                <GitBranch size={14} />
                Logic
            </button>
        </div>
    );

    if (activeTab === 'logic') {
        return (
            <aside className={panelClassName}>
                <TabsHeader />
                <LogicPanel />
            </aside>
        );
    }

    // If in Background mode (activeLayer === 0), show Background Properties
    if (activeLayer === 0) {
        return (
            <aside className={panelClassName}>
                <TabsHeader />
                <BackgroundPropertiesPanel 
                    pageBackground={pageBackground}
                    onBackgroundChange={handleBackgroundChange}
                    canvasWidth={formDefinition?.canvasSettings?.width ?? 1920}
                    canvasHeight={formDefinition?.canvasSettings?.height ?? 980}
                />
            </aside>
        );
    }

    // If no component selected, show Global Styles
    if (!selectedComponentId || !selectedComponent) {
        return (
            <aside className={panelClassName}>
                <TabsHeader />
                <GlobalStylesPanel 
                    globalStyles={globalStyles}
                    onGlobalStylesChange={updateGlobalStyles}
                />
            </aside>
        );
    }

    // Handler for bulk property updates (multi-select)
    const handleMultiPropsChange = (updates: Partial<FormComponent['props']>) => {
        updateMultipleComponentProps(updates);
    };

    // Get component definition from registry
    const componentDef = ComponentRegistry[selectedComponent.type];
    const componentLabel = componentDef?.label || selectedComponent.type;

    // ═══════════════════════════════════════════════════════════════════════════════
    // MULTI-SELECT MODE
    // ═══════════════════════════════════════════════════════════════════════════════
    if (isMultiSelect) {
        // Get component type breakdown
        const typeBreakdown = selectedComponents.reduce((acc, comp) => {
            acc[comp.type] = (acc[comp.type] || 0) + 1;
            return acc;
        }, {} as Record<string, number>);
        
        return (
            <aside className={panelClassName}>
                <TabsHeader />
                {/* Multi-Select Header */}
                <div className="p-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between bg-gradient-to-r from-purple-50 to-indigo-50 dark:from-purple-900/20 dark:to-indigo-900/20">
                    <div className="flex items-center gap-2">
                        <Users className="text-purple-500" size={18} />
                        <div>
                            <h3 className="font-semibold text-gray-800 dark:text-gray-200 text-sm">
                                {selectedComponentIds.length} Components Selected
                            </h3>
                            <p className="text-xs text-gray-500 dark:text-gray-400">
                                Ctrl+Click to add/remove
                            </p>
                        </div>
                    </div>
                    <button
                        onClick={() => clearSelection()}
                        className="p-1.5 rounded hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                        title="Clear Selection (Esc)"
                    >
                        <X size={16} />
                    </button>
                </div>

                <div className="flex-1 overflow-y-scroll">
                    {/* Type Breakdown */}
                    <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                        <div className="text-xs text-gray-500 dark:text-gray-400 mb-2">Selection breakdown:</div>
                        <div className="flex flex-wrap gap-1">
                            {Object.entries(typeBreakdown).map(([type, count]) => (
                                <span 
                                    key={type}
                                    className="px-2 py-0.5 text-xs bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 rounded"
                                >
                                    {ComponentRegistry[type as keyof typeof ComponentRegistry]?.label || type} × {count}
                                </span>
                            ))}
                        </div>
                    </div>

                    {/* Shared Properties Section */}
                    <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                        <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3 flex items-center gap-2">
                            <Layers size={14} className="text-purple-500" />
                            Bulk Edit (applies to all)
                        </h4>
                        
                        <div className="space-y-3">
                            {/* Required Toggle */}
                            <div className="flex items-center justify-between">
                                <span className="text-xs text-gray-600 dark:text-gray-400">Required</span>
                                <label className="relative inline-flex items-center cursor-pointer">
                                    <input
                                        type="checkbox"
                                        className="sr-only peer"
                                        onChange={(e) => handleMultiPropsChange({ required: e.target.checked })}
                                    />
                                    <div className="w-8 h-4 bg-gray-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-purple-300 dark:peer-focus:ring-purple-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-3 after:w-3 after:transition-all dark:border-gray-600 peer-checked:bg-purple-600"></div>
                                    <span className="ml-1 text-[10px] text-gray-400">Set all</span>
                                </label>
                            </div>

                            {/* Layout Toggle */}
                            <div className="flex items-center justify-between">
                                <span className="text-xs text-gray-600 dark:text-gray-400">Layout</span>
                                <div className="flex gap-1">
                                    <button
                                        onClick={() => handleMultiPropsChange({ layout: 'vertical' })}
                                        className="px-2 py-1 text-[10px] rounded bg-gray-100 hover:bg-purple-100 dark:bg-gray-700 dark:hover:bg-purple-900/30"
                                    >
                                        Vertical
                                    </button>
                                    <button
                                        onClick={() => handleMultiPropsChange({ layout: 'horizontal' })}
                                        className="px-2 py-1 text-[10px] rounded bg-gray-100 hover:bg-purple-100 dark:bg-gray-700 dark:hover:bg-purple-900/30"
                                    >
                                        Horizontal
                                    </button>
                                </div>
                            </div>

                            {/* Component Scale */}
                            <div className="space-y-1">
                                <div className="flex items-center justify-between">
                                    <span className="text-xs text-gray-600 dark:text-gray-400">Component Scale</span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <input
                                        type="range"
                                        min={50}
                                        max={200}
                                        step={5}
                                        defaultValue={100}
                                        onChange={(e) => handleMultiPropsChange({ componentScale: parseInt(e.target.value) })}
                                        className="flex-1 h-1.5 accent-purple-500"
                                    />
                                    <button
                                        onClick={() => handleMultiPropsChange({ componentScale: 100 })}
                                        className="px-2 py-0.5 text-[10px] rounded bg-gray-100 hover:bg-purple-100 dark:bg-gray-700 dark:hover:bg-purple-900/30"
                                    >
                                        Reset
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Appearance Section (shared styling) */}
                    <AppearanceSection
                        overrides={bulkStyleOverrides}
                        globalStyles={globalStyles}
                        onOverridesChange={(updates) => {
                            const nextBulk = updates ? mergeStyleOverrides(bulkStyleOverrides, updates) : {};
                            setBulkStyleOverrides(nextBulk);

                            const state = useBuilderStore.getState();
                            const selected = state.getSelectedComponents();

                            selected.forEach(comp => {
                                const existing = comp.props.styleOverrides || {};
                                const merged = updates ? mergeStyleOverrides(existing, updates) : {};
                                state.updateComponentProps(comp.id, { styleOverrides: Object.keys(merged).length ? merged : undefined });
                            });
                        }}
                        currentLayout="vertical"
                    />

                    {/* Info Note */}
                    <div className="p-4">
                        <div className="text-xs text-gray-400 dark:text-gray-500 bg-gray-50 dark:bg-gray-800 p-3 rounded-lg">
                            <strong>Multi-select mode:</strong> Changes apply to all {selectedComponentIds.length} selected components.
                            Click a component without Ctrl to select only that one.
                        </div>
                    </div>
                </div>
            </aside>
        );
    }

    // ═══════════════════════════════════════════════════════════════════════════════
    // SINGLE-SELECT MODE (original behavior)
    // ═══════════════════════════════════════════════════════════════════════════════
    const selectedStructure = selectedComponent ? ComponentRegistry[selectedComponent.type]?.structure : undefined;
    const canShowObjectGridLayout =
        Boolean(selectedStructure?.objects?.length) && !['divider', 'header', 'paragraph'].includes(selectedComponent?.type || '');
    const isGridMode =
        !!selectedComponent &&
        selectedComponent.props.gridLayout !== null &&
        (selectedComponent.props.gridLayout !== undefined || Boolean(globalStyles.defaultGridLayout));

    return (
        <aside className={panelClassName}>
            <TabsHeader />
            {/* Panel Header */}
            <div className="p-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between bg-gradient-to-r from-teal-50 to-cyan-50 dark:from-teal-900/20 dark:to-cyan-900/20">
                <div className="flex items-center gap-2">
                    <Settings className="text-teal-500" size={18} />
                    <div>
                        <h3 className="font-semibold text-gray-800 dark:text-gray-200 text-sm">
                            {componentLabel}
                        </h3>
                        <p className="text-xs text-gray-500 dark:text-gray-400">
                            Properties
                        </p>
                    </div>
                </div>
                <button
                    onClick={() => selectComponent(null)}
                    className="p-1.5 rounded hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                    title="Deselect (Esc)"
                >
                    <X size={16} />
                </button>
            </div>

            {/* Scrollable Content - using scroll to always reserve scrollbar space */}
            <div className="flex-1 overflow-y-scroll">
                {/* ═══════════════════════════════════════════════════════════════ */}
                {/* COMPONENT-SPECIFIC SECTIONS (shown first for relevant types) */}
                {/* ═══════════════════════════════════════════════════════════════ */}
                
                {/* Button Properties (for submit-button) */}
                {selectedComponent.type === 'submit-button' && (
                    <ButtonPropertiesSection
                        props={selectedComponent.props}
                        onPropsChange={handlePropsChange}
                    />
                )}

                {/* Terms Properties (for terms) */}
                {selectedComponent.type === 'terms' && (
                    <TermsPropertiesSection
                        props={selectedComponent.props}
                        onPropsChange={handlePropsChange}
                    />
                )}

                {/* Textarea Properties (for textarea) */}
                {selectedComponent.type === 'textarea' && (
                    <TextareaPropertiesSection
                        props={selectedComponent.props}
                        onPropsChange={handlePropsChange}
                    />
                )}

                {/* Options Section - for dropdown/select, checkbox, radio */}
                {['select', 'dropdown', 'checkbox', 'radio'].includes(selectedComponent.type) && (
                    <OptionsSection
                        props={selectedComponent.props}
                        onPropsChange={handlePropsChange}
                        componentType={selectedComponent.type}
                    />
                )}

                {/* Date Properties Section - for date component */}
                {selectedComponent.type === 'date' && (
                    <DatePropertiesSection
                        props={selectedComponent.props}
                        onPropsChange={handlePropsChange}
                    />
                )}

                {/* ═══════════════════════════════════════════════════════════════ */}
                {/* IDENTITY & BEHAVIOR + DATA COLLECTION (from GeneralSection) */}
                {/* ═══════════════════════════════════════════════════════════════ */}
                {!['submit-button', 'divider'].includes(selectedComponent.type) && (
                    <GeneralSection
                        props={selectedComponent.props}
                        onPropsChange={handlePropsChange}
                        componentType={selectedComponent.type}
                        globalDefaultLayout={globalStyles.defaultLayout}
                    />
                )}

                {/* ═══════════════════════════════════════════════════════════════ */}
                {/* LAYOUT MODE (Object Layout vs Grid Layout) */}
                {/* ═══════════════════════════════════════════════════════════════ */}
                {canShowObjectGridLayout && selectedStructure && (
                    <>
                        <GridLayoutSection
                            component={selectedComponent}
                            structure={selectedStructure}
                            onPropsChange={handlePropsChange}
                            globalStyles={globalStyles}
                        />
                        {/* Only show Object Layout editor when in Object mode */}
                        {!isGridMode && (
                            <ObjectLayoutSection
                                component={selectedComponent}
                                structure={selectedStructure}
                                onPropsChange={handlePropsChange}
                                globalStyles={{
                                    defaultObjectLayout: globalStyles.defaultObjectLayout,
                                    defaultLayoutGroups: globalStyles.defaultLayoutGroups,
                                }}
                            />
                        )}
                    </>
                )}

                {/* ═══════════════════════════════════════════════════════════════ */}
                {/* VALIDATION RULES */}
                {/* ═══════════════════════════════════════════════════════════════ */}
                {!['submit-button', 'divider', 'header', 'paragraph'].includes(selectedComponent.type) && (
                    <ValidationSection
                        validation={selectedComponent.props.validation}
                        onValidationChange={handleValidationChange}
                        componentType={selectedComponent.type}
                        componentId={selectedComponent.id}
                        availableFields={availableFieldsForMatch}
                    />
                )}

                {/* Data Export Section - for checkbox/terms */}
                {['checkbox', 'terms'].includes(selectedComponent.type) && (
                    <DataExportSection
                        props={selectedComponent.props}
                        onPropsChange={handlePropsChange}
                        componentType={selectedComponent.type}
                    />
                )}

                {/* ═══════════════════════════════════════════════════════════════ */}
                {/* APPEARANCE (Dimensions + Typography/Spacing) */}
                {/* ═══════════════════════════════════════════════════════════════ */}
                {!['divider'].includes(selectedComponent.type) && (
                    <AppearanceSection
                        overrides={selectedComponent.props.styleOverrides}
                        globalStyles={globalStyles}
                        onOverridesChange={handleStyleOverridesChange}
                        currentLayout={selectedComponent.props.layout || globalStyles.defaultLayout}
                        props={selectedComponent.props}
                        onPropsChange={handlePropsChange}
                        componentType={selectedComponent.type}
                    />
                )}

                {/* Component ID (Debug Info) */}
                <div className="p-4 border-t border-gray-100 dark:border-gray-800">
                    <div className="text-xs text-gray-400 dark:text-gray-500 space-y-1">
                        <div className="flex justify-between">
                            <span>ID:</span>
                            <span className="font-mono truncate max-w-[180px]" title={selectedComponent.id}>
                                {selectedComponent.id}
                            </span>
                        </div>
                        {selectedComponent.position && (
                            <div className="flex justify-between">
                                <span>Position:</span>
                                <span className="font-mono">
                                    x:{selectedComponent.position.x}, y:{selectedComponent.position.y}
                                </span>
                            </div>
                        )}
                        {selectedComponent.props.exportName && (
                            <div className="flex justify-between">
                                <span>Export:</span>
                                <span className="font-mono text-green-600 dark:text-green-400">
                                    {selectedComponent.props.exportName}
                                </span>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </aside>
    );
};
