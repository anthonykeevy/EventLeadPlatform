import { useEffect } from 'react';
import { ArrowLeft, Settings, Save, Eye, Undo2, Redo2, Download } from 'lucide-react';
import { Link } from 'react-router-dom';
import { ResizablePanel } from './ResizablePanel';
import { useBuilderStore } from '../stores/useBuilderStore';
import { devLogger } from '../utils/devLogger';

interface BuilderLayoutProps {
    children: React.ReactNode;
    sidebar: React.ReactNode;
    propertiesPanel?: React.ReactNode; // Story 3.5
    title?: string;
    formId?: string;
    onToggleInlinePreview?: () => void;
    isInlinePreviewOpen?: boolean;
    isInlinePreviewLoading?: boolean;
    onOpenPreview?: () => void;
    isPreviewLoading?: boolean;
    /** Story 5.6: Optional header action (e.g. Request Publish / Publish button) */
    headerAction?: React.ReactNode;
    /** Story 5.6: Optional status badge (replaces hardcoded Draft with actual form status) */
    formStatusBadge?: React.ReactNode;
}

// Default panel widths
const DEFAULT_TOOLBOX_WIDTH = 320;
const DEFAULT_PROPERTIES_WIDTH = 320;
const MIN_PANEL_WIDTH = 260;
const MAX_PANEL_WIDTH = 480;

export const BuilderLayout: React.FC<BuilderLayoutProps> = ({ 
    children, 
    sidebar, 
    propertiesPanel,
    title,
    formId,
    onToggleInlinePreview,
    isInlinePreviewOpen,
    isInlinePreviewLoading,
    onOpenPreview,
    isPreviewLoading,
    headerAction,
    formStatusBadge,
}) => {
    const {
        undo,
        redo,
        canUndo,
        canRedo,
        runtimeWarnings,
        deleteSelectedComponents,
        selectedComponentIds,
        activeLayer,
        saveDraft,
        isSaving,
        isDirty,
    } = useBuilderStore();
    const canSave = Boolean(formId) && !isSaving;
    const saveLabel = isSaving ? 'Saving...' : 'Save';

    const handleSave = async () => {
        if (!formId) {
            devLogger.warn('form.save.missingFormId');
            return;
        }
        try {
            await saveDraft(formId);
        } catch (err) {
            devLogger.error('form.save.failed', {
                formId,
                error: err instanceof Error ? err.message : String(err),
            });
        }
    };
    
    // Keyboard shortcuts for undo/redo
    useEffect(() => {
        const handleKeyDown = (e: KeyboardEvent) => {
            // Don't trigger global shortcuts while typing in inputs/textareas/contenteditable
            const target = e.target as HTMLElement | null;
            const isTypingTarget =
                !!target &&
                (target.tagName === 'INPUT' ||
                    target.tagName === 'TEXTAREA' ||
                    (target as any).isContentEditable);

            // Check for Ctrl+Z (Windows) or Cmd+Z (Mac)
            if (!isTypingTarget && (e.ctrlKey || e.metaKey) && e.key === 'z' && !e.shiftKey) {
                e.preventDefault();
                if (canUndo()) {
                    undo();
                }
            }
            // Check for Ctrl+Y (Windows) or Cmd+Shift+Z (Mac)
            if (!isTypingTarget && (e.ctrlKey || e.metaKey) && (e.key === 'y' || (e.key === 'z' && e.shiftKey))) {
                e.preventDefault();
                if (canRedo()) {
                    redo();
                }
            }

            // Delete selected component(s) (edit mode only)
            if (!isTypingTarget && activeLayer === 1 && selectedComponentIds.length > 0) {
                if (e.key === 'Delete' || e.key === 'Backspace') {
                    e.preventDefault();
                    deleteSelectedComponents();
                }
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [undo, redo, canUndo, canRedo, deleteSelectedComponents, selectedComponentIds, activeLayer]);

    return (
        <div className="flex flex-col h-screen bg-gray-100 overflow-hidden">
            {/* Header */}
            <header className="bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between flex-shrink-0 z-10 shadow-sm">
                <div className="flex items-center gap-4">
                    <Link to="/dashboard" className="text-gray-500 hover:text-gray-800 transition-colors">
                        <ArrowLeft size={20} />
                    </Link>
                    <div className="h-6 w-px bg-gray-200"></div>
                    <h1 className="font-semibold text-gray-800 text-lg">{title || 'Untitled Form'}</h1>
                    {formStatusBadge ?? (
                      <span className="bg-yellow-100 text-yellow-800 text-xs px-2 py-0.5 rounded-full font-medium">Draft</span>
                    )}
                </div>

                <div className="flex items-center gap-3">
                    {/* Undo/Redo Buttons */}
                    <div className="flex items-center gap-1 border-r border-gray-200 pr-3 mr-1">
                        <button 
                            onClick={() => canUndo() && undo()}
                            disabled={!canUndo()}
                            className="p-1.5 rounded hover:bg-gray-100 text-gray-500 hover:text-gray-700 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                            title="Undo (Ctrl+Z)"
                        >
                            <Undo2 size={18} />
                        </button>
                        <button 
                            onClick={() => canRedo() && redo()}
                            disabled={!canRedo()}
                            className="p-1.5 rounded hover:bg-gray-100 text-gray-500 hover:text-gray-700 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                            title="Redo (Ctrl+Y)"
                        >
                            <Redo2 size={18} />
                        </button>
                    </div>
                    {devLogger.isEnabled() && (
                        <button
                            className="btn-secondary text-sm py-1.5 px-3 flex items-center gap-2"
                            onClick={() => devLogger.download()}
                            title="Download dev logs (dev only)"
                        >
                            <Download size={16} /> Dev Logs
                        </button>
                    )}
                    <button
                        className={`btn-secondary text-sm py-1.5 px-3 flex items-center gap-2 ${isInlinePreviewOpen ? 'ring-2 ring-teal-400' : ''}`}
                        onClick={onToggleInlinePreview}
                        title="Toggle inline preview"
                        disabled={!onToggleInlinePreview || isInlinePreviewLoading}
                    >
                        <Eye size={16} /> {isInlinePreviewLoading ? 'Opening...' : (isInlinePreviewOpen ? 'Editing' : 'Preview')}
                    </button>
                    <button
                        className="btn-secondary text-sm py-1.5 px-3 flex items-center gap-2"
                        onClick={onOpenPreview}
                        title="Open runtime preview in a new tab"
                        disabled={!onOpenPreview || isPreviewLoading}
                    >
                        <Eye size={16} /> {isPreviewLoading ? 'Opening...' : 'Open Preview'}
                    </button>
                    {runtimeWarnings.length > 0 && (
                        <span
                            className="bg-yellow-100 text-yellow-800 text-xs px-2 py-0.5 rounded-full font-medium"
                            title={`${runtimeWarnings.length} runtime warning(s) (rules ignored safely)`}
                        >
                            Warnings: {runtimeWarnings.length}
                        </span>
                    )}
                    <button className="btn-secondary text-sm py-1.5 px-3 flex items-center gap-2">
                        <Settings size={16} /> Settings
                    </button>
                    {headerAction}
                    <button
                        className="btn-primary text-sm py-1.5 px-4 flex items-center gap-2"
                        onClick={handleSave}
                        disabled={!canSave}
                        title={!formId ? 'Cannot save: missing form id' : (isDirty ? 'Save draft' : 'No changes to save')}
                    >
                        <Save size={16} /> {saveLabel}
                    </button>
                </div>
            </header>

            {/* Main Workspace */}
            <div className="flex flex-1 overflow-hidden">
                {/* Left Sidebar (Toolbox) - Resizable */}
                <ResizablePanel
                    resizeFrom="right"
                    defaultWidth={DEFAULT_TOOLBOX_WIDTH}
                    minWidth={MIN_PANEL_WIDTH}
                    maxWidth={MAX_PANEL_WIDTH}
                    storageKey="builder-toolbox-width"
                    className="h-full hidden lg:block"
                >
                    {sidebar}
                </ResizablePanel>

                {/* Center Canvas */}
                <main className="flex-1 overflow-y-auto bg-gray-100 relative">
                    {children}
                </main>

                {/* Right Sidebar (Properties Panel) - Resizable - Story 3.5 */}
                {propertiesPanel && (
                    <ResizablePanel
                        resizeFrom="left"
                        defaultWidth={DEFAULT_PROPERTIES_WIDTH}
                        minWidth={MIN_PANEL_WIDTH}
                        maxWidth={MAX_PANEL_WIDTH}
                        storageKey="builder-properties-width"
                        className="h-full hidden lg:block"
                    >
                        {propertiesPanel}
                    </ResizablePanel>
                )}
            </div>
        </div>
    );
};
