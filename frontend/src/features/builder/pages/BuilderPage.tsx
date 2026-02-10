import { useEffect, useRef } from 'react';
import { useLocation, useParams } from 'react-router-dom';
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
  DragMoveEvent,
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
import { FirstNameField } from '../components/fields/FirstNameField';
import { ComponentRegistry, generateComponent } from '../registry/ComponentRegistry';
import { LoadingSpinner } from '../../ux/components/LoadingSpinner';
import { ComponentType, FormComponent } from '../types/builder.types';
import { devLogger } from '../utils/devLogger';
import { captureComponentSnapshot } from '../utils/componentSnapshot';
import {
  buildCanvasRectsForComponents,
  checkCollision,
  checkCanvasBoundary,
  getComponentDimensions,
  resolveMoveConstraints,
} from '../utils/collisionDetection';
import { UniversalFieldShell } from '../components/UniversalFieldShell';
import { getRenderersForComponent } from '../utils/componentRenderers';
import { getDefaultStructure } from '../utils/structureDefaults';
import { apiClient } from '../../../lib/apiClient';
import { getComponentSurfaceCapabilities } from '../utils/componentSurfaceCapabilities';
import { PublicFormArtboard } from '../../renderer/components/PublicFormArtboard';

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
  const { formId: routeFormId } = useParams<{ formId: string }>();
  const location = useLocation();
  const queryFormId = React.useMemo(() => {
    const value = new URLSearchParams(location.search).get('formId');
    return value?.trim() || null;
  }, [location.search]);
  const formId = routeFormId ?? queryFormId ?? undefined;
  // Get scale and showGrid from store
  const { 
      initializeForm, 
      isLoading, 
      loadError,
      formDefinition, 
      activeId, 
      setActiveId, 
      updateComponent, 
      addComponent, 
      scale,
      showGrid,
      isDirty,
      setDragPosition,
      saveDraft,
  } = useBuilderStore();

  const [publicPreviewError, setPublicPreviewError] = React.useState<string | null>(null);
  const [isPublicPreviewLoading, setIsPublicPreviewLoading] = React.useState(false);
  const [isInlinePreviewOpen, setIsInlinePreviewOpen] = React.useState(false);
  const [isInlinePreviewLoading, setIsInlinePreviewLoading] = React.useState(false);
  const previewWindowRef = useRef<Window | null>(null);

  const canvasRef = useRef<HTMLDivElement>(null);

  const sensors = useSensors(
    useSensor(PointerSensor, {
        activationConstraint: {
            distance: 5, 
        }
    }),
    useSensor(KeyboardSensor, {})
  );

  /**
   * Toolbox drag overlay + drop placement must use the SAME assumed dimensions,
   * otherwise the pointer-ratio math can produce negative Y (clamped to 0),
   * which looks like the component "jumps to the top" after drop.
   */
  const getToolboxOverlayDimensions = React.useCallback((component: FormComponent) => {
    const estimate = getComponentDimensions(component, null, 100);
    let width = estimate.width;
    let height = estimate.height;

    // Percent widths don't have a meaningful pixel size in the overlay (no parent width),
    // so use a stable default.
    const widthProp = component.props?.width as string | undefined;
    if (typeof widthProp === 'string' && widthProp.endsWith('%')) {
      width = 380;
    }

    // Divider renderer has vertical padding, so height needs to be larger than the "line" itself
    // to keep pointer-ratio mapping stable.
    if (component.type === 'divider') {
      height = 32;
    }

    return {
      width: Math.max(50, width),
      height: Math.max(20, height),
    };
  }, []);

  useEffect(() => {
    if (formId) {
      initializeForm(formId);
    }
  }, [formId, initializeForm]);

  const buildPreviewToken = async () => {
    if (!formId) {
      throw new Error('Missing form id. Unable to open preview.');
    }

    try {
      // Ensure the renderer pulls exactly what the user just authored.
      await saveDraft(formId);

      const res = await apiClient.post(`/api/forms/${formId}/public-links`, { linkType: 'PREVIEW' });
      const token = res?.data?.link?.token as string | undefined;
      if (!token) {
        throw new Error('Preview link was created but no token was returned.');
      }

      return token;
    } catch (e: any) {
      const msg = e?.response?.data?.detail || e?.message || 'Failed to generate preview link.';
      throw new Error(String(msg));
    }
  };

  const handleToggleInlinePreview = async () => {
    if (isInlinePreviewOpen) {
      setIsInlinePreviewOpen(false);
      return;
    }

    setIsInlinePreviewLoading(true);
    setPublicPreviewError(null);
    try {
      setIsInlinePreviewOpen(true);
    } finally {
      setIsInlinePreviewLoading(false);
    }
  };

  const openPreviewInNewTab = async () => {
    if (isPublicPreviewLoading) return;
    setIsPublicPreviewLoading(true);
    setPublicPreviewError(null);

    let previewWindow: Window | null = null;
    try {
      // Open a new tab synchronously so popup blockers allow it.
      previewWindow = window.open('', '_blank');
      if (!previewWindow) {
        throw new Error('Popup blocked. Please allow popups for this site.');
      }
      // Reduce cross-window coupling after open.
      try {
        previewWindow.opener = null;
      } catch {
        // Ignore if browser blocks opener changes.
      }
      previewWindowRef.current = previewWindow;

      const token = await buildPreviewToken();
      const url = `${window.location.origin}/forms/${token}/preview`;
      if (previewWindow && !previewWindow.closed) {
        previewWindow.location.href = url;
      } else {
        window.open(url, '_blank');
      }
    } catch (err: any) {
      if (previewWindow && !previewWindow.closed) {
        previewWindow.close();
      }
      const msg = err?.message || 'Failed to generate preview link.';
      setPublicPreviewError(String(msg));
      devLogger.error('preview.open.failed', { formId, error: String(msg) });
    } finally {
      setIsPublicPreviewLoading(false);
    }
  };

  // Warn when leaving the builder with unsaved DB changes.
  // localStorage reduces data loss risk, but DB persistence is still important (collaboration, preview links, portability).
  useEffect(() => {
    const handler = (e: BeforeUnloadEvent) => {
      if (!isDirty) return;
      e.preventDefault();
      // Chrome requires returnValue to be set.
      e.returnValue = '';
    };
    window.addEventListener('beforeunload', handler);
    return () => window.removeEventListener('beforeunload', handler);
  }, [isDirty]);

  // Store drag snapshots ref for logging
  const dragSnapshotsRef = useRef<Map<string, { before: any; after: any }>>(new Map());
  
  // Ref to track drag interval for periodic snapshots
  const dragSnapshotIntervalRef = useRef<NodeJS.Timeout | null>(null);

  // Store component refs map for collision detection
  const componentRefsRef = useRef<Map<string, React.RefObject<HTMLDivElement>>>(new Map());
  
  // Track pointer offset within the dragged element (for accurate drop positioning)
  const pointerOffsetRef = useRef<{ x: number; y: number } | null>(null);
  
  // Track initial pointer position at drag start (screen coordinates)
  const initialPointerPositionRef = useRef<{ x: number; y: number } | null>(null);
  
  // Track the initial element dimensions (toolbox item size at 100%)
  const initialElementSizeRef = useRef<{ width: number; height: number } | null>(null);
  
  // Track last known pointer position (updated on every pointer move)
  const lastPointerRef = useRef<{ x: number; y: number }>({ x: 0, y: 0 });

  // Drag constraint helpers (existing components)
  const dragMoveRafRef = useRef<number | null>(null);
  const pendingDragMoveRef = useRef<{ activeId: string; delta: { x: number; y: number } } | null>(null);
  const dragActiveSizeRef = useRef<{ width: number; height: number } | null>(null);
  const dragOtherRectsRef = useRef<Array<{ id: string; rect: { x: number; y: number; width: number; height: number } }> | null>(null);
  const dragStartComponentPosRef = useRef<{ x: number; y: number } | null>(null);
  const lastConstraintLogRef = useRef<number>(0);
  const dragActivePolyLocalRef = useRef<Array<{ x: number; y: number }> | null>(null);
  
  // Set up global pointer tracking
  React.useEffect(() => {
    const handlePointerMove = (e: PointerEvent) => {
      lastPointerRef.current = { x: e.clientX, y: e.clientY };
    };
    
    window.addEventListener('pointermove', handlePointerMove);
    return () => window.removeEventListener('pointermove', handlePointerMove);
  }, []);

  const handleDragStart = (event: DragStartEvent) => {
    const activeId = event.active.id as string;
    setActiveId(activeId);
    setDragPosition(null); // Reset drag position
    dragStartComponentPosRef.current = null;
    
    // Clear any existing interval
    if (dragSnapshotIntervalRef.current) {
      clearInterval(dragSnapshotIntervalRef.current);
      dragSnapshotIntervalRef.current = null;
    }
    
    // Get element rect from dnd-kit or by querying the DOM
    let elementRect = event.active.rect?.current?.initial;
    
    // Fallback: query the DOM for the element
    if (!elementRect) {
      // Canvas components are identified by data-component-id; toolbox items sometimes use data-id.
      const element =
        (document.querySelector(`[data-component-id="${activeId}"]`) as HTMLElement | null) ??
        (document.querySelector(`[data-id="${activeId}"]`) as HTMLElement | null);
      if (element) {
        const rect = element.getBoundingClientRect();
        elementRect = { left: rect.left, top: rect.top, width: rect.width, height: rect.height };
      }
    }
    
    // Use the last known pointer position (from global tracking)
    const pointerX = lastPointerRef.current.x;
    const pointerY = lastPointerRef.current.y;
    
    if (elementRect && (pointerX !== 0 || pointerY !== 0)) {
      // Offset from element's top-left to pointer position
      pointerOffsetRef.current = {
        x: Math.max(0, Math.min(pointerX - elementRect.left, elementRect.width)),
        y: Math.max(0, Math.min(pointerY - elementRect.top, elementRect.height))
      };
      
      // Capture initial pointer position (screen coordinates)
      initialPointerPositionRef.current = { x: pointerX, y: pointerY };
      
      // Capture initial element size (toolbox item at 100%)
      initialElementSizeRef.current = { width: elementRect.width, height: elementRect.height };
      
      devLogger.debug('drag.pointer.offset', {
        activeId,
        elementRect,
        pointerPosition: { x: pointerX, y: pointerY },
        offset: pointerOffsetRef.current,
        initialSize: initialElementSizeRef.current
      });
    } else {
      // Use center of element as fallback
      if (elementRect) {
        pointerOffsetRef.current = { x: elementRect.width / 2, y: elementRect.height / 2 };
        initialPointerPositionRef.current = { 
          x: elementRect.left + elementRect.width / 2, 
          y: elementRect.top + elementRect.height / 2 
        };
        initialElementSizeRef.current = { width: elementRect.width, height: elementRect.height };
        
        devLogger.debug('drag.pointer.offset.fallback', {
          activeId,
          elementRect,
          offset: pointerOffsetRef.current,
          reason: 'using-element-center'
        });
      } else {
        devLogger.warn('drag.pointer.offset.failed', { activeId, reason: 'no-element-rect' });
        pointerOffsetRef.current = null;
        initialPointerPositionRef.current = null;
        initialElementSizeRef.current = null;
      }
    }
    
    // Log drag start (before grab) - only for existing components
    if (!activeId.toString().startsWith('toolbox-')) {
      const def = useBuilderStore.getState().formDefinition;
      const pages = def?.desktopPages && def.desktopPages.length > 0 ? def.desktopPages : (def?.pages ?? []);
      const activePage = pages.find(p => p.id === useBuilderStore.getState().activePageId);
      const component = activePage?.components.find(c => c.id === activeId);
      
      if (component) {
        // Preserve original grab point: compute proposed positions from initial position + delta (not incremental drift)
        dragStartComponentPosRef.current = {
          x: component.position?.x ?? 0,
          y: component.position?.y ?? 0,
        };

        // Precompute measured size + other component rects for live constraints (canvas coords)
        try {
          const el = document.querySelector(`[data-component-id="${component.id}"]`) as HTMLElement | null;
          dragActiveSizeRef.current = getComponentDimensions(component, el, scale * 100);
          // Capture SmartBorder local polygon points (from SVG path d) for true-shape collision during drag
          const pathEl = el?.querySelector('svg > path') as SVGPathElement | null;
          const d = pathEl?.getAttribute('d') || '';
          if (d) {
            // Parse SmartBorder `d` like: "M x y L x y ... Z"
            // NOTE: this regex must NOT be double-escaped; it runs in the browser at runtime.
            const nums = d.match(/-?\d*\.?\d+/g)?.map(n => Number(n)) || [];
            const local: Array<{ x: number; y: number }> = [];
            for (let i = 0; i + 1 < nums.length; i += 2) local.push({ x: nums[i], y: nums[i + 1] });
            dragActivePolyLocalRef.current = local.length >= 3 ? local : null;
          } else {
            dragActivePolyLocalRef.current = null;
          }
          const all = activePage.components;
          const ignore = new Set<string>([component.id]);
          const others = buildCanvasRectsForComponents(all, scale, ignore).map(o => ({ id: o.id, rect: o.rect, shape: o.shape }));
          dragOtherRectsRef.current = others;

          // Log shape capture so DB logs can prove whether we used SmartBorder polygon vs AABB.
          devLogger.info('fieldshell.collision.shape.capture', {
            componentId: component.id,
            hasSmartBorderPath: !!d,
            smartBorderPathDLength: d.length,
            activePolygonPointCount: dragActivePolyLocalRef.current?.length ?? 0,
            othersCount: others.length,
            othersWithShapeCount: others.filter(o => !!o.shape?.polygon?.length).length,
          });
        } catch {
          dragActiveSizeRef.current = null;
          dragOtherRectsRef.current = null;
          dragActivePolyLocalRef.current = null;
        }

        // Capture snapshot before grab (no ref available, use component data)
        const snapshot = captureComponentSnapshot(component, null);
        devLogger.info('fieldshell.drag.start', {
          component: snapshot,
          action: 'grab'
        });
        
        // Store initial snapshot
        dragSnapshotsRef.current.set(activeId, { before: snapshot, after: null });

        // Start periodic snapshots during drag (every 1 second)
        dragSnapshotIntervalRef.current = setInterval(() => {
          const def = useBuilderStore.getState().formDefinition;
          const currentPages = def?.desktopPages && def.desktopPages.length > 0 ? def.desktopPages : (def?.pages ?? []);
          const currentPage = currentPages.find(p => p.id === useBuilderStore.getState().activePageId);
          const currentComponent = currentPage?.components.find(c => c.id === activeId);
          const currentDragPosition = useBuilderStore.getState().dragPosition;
          
          if (currentComponent && currentDragPosition) {
            const dragSnapshot = captureComponentSnapshot({
              ...currentComponent,
              position: currentDragPosition
            }, null);
            
            devLogger.debug('fieldshell.drag.snapshot', {
              componentId: activeId,
              timestamp: Date.now(),
              component: dragSnapshot,
              dragPosition: currentDragPosition
            });
          }
        }, 1000); // Every 1 second
      }
    }
  };
  
  const handleDragMove = (event: DragMoveEvent) => {
    const { active, delta } = event;
    const activeId = active.id as string;
    pendingDragMoveRef.current = { activeId, delta: { x: delta.x, y: delta.y } };
    if (dragMoveRafRef.current != null) return;

    dragMoveRafRef.current = window.requestAnimationFrame(() => {
      dragMoveRafRef.current = null;
      const pending = pendingDragMoveRef.current;
      if (!pending) return;
      const { activeId: rafActiveId, delta: rafDelta } = pending;
    
      // Only track position for existing components (not toolbox items)
      if (rafActiveId.toString().startsWith('toolbox-')) return;

      const def = useBuilderStore.getState().formDefinition;
      const pages = def?.desktopPages && def.desktopPages.length > 0 ? def.desktopPages : (def?.pages ?? []);
      const activePage = pages.find(p => p.id === useBuilderStore.getState().activePageId);
      const component = activePage?.components.find(c => c.id === rafActiveId);
      
      if (component) {
        const startPos = dragStartComponentPosRef.current ?? { x: component.position?.x ?? 0, y: component.position?.y ?? 0 };
        const scaledDeltaX = rafDelta.x / scale;
        const scaledDeltaY = rafDelta.y / scale;
        let newX = startPos.x + scaledDeltaX;
        let newY = startPos.y + scaledDeltaY;

        // Snap to Grid Conditionally (same logic as drag end)
        if (showGrid) {
          newX = Math.round(newX / 8) * 8;
          newY = Math.round(newY / 8) * 8;
        } else {
          newX = Math.round(newX);
          newY = Math.round(newY);
        }
        
        // Log drag grabbed (after initial grab) - only once
        const snapshots = dragSnapshotsRef.current.get(component.id);
        if (snapshots && !snapshots.after) {
          const snapshotAfterGrab = captureComponentSnapshot(component, null);
          devLogger.info('fieldshell.drag.grabbed', {
            componentId: component.id,
            initialPosition: { x: startPos.x, y: startPos.y },
            positionAfterGrab: { x: newX, y: newY },
            delta: { x: scaledDeltaX, y: scaledDeltaY }
          });
          snapshots.after = snapshotAfterGrab;
        }
                
        // Apply live constraints (canvas boundary + collision slide), if enabled for this component type
        const caps = getComponentSurfaceCapabilities(component.type as any, 'canvas');
        if (caps.dragConstraints.enabled && (caps.dragConstraints.canvasBoundary || caps.dragConstraints.collisionAvoidance)) {
          const canvasSettings = useBuilderStore.getState().formDefinition?.canvasSettings;
          const canvasWidth = canvasSettings?.width || 1920;
          const canvasHeight = canvasSettings?.height || 980;

          const size =
            dragActiveSizeRef.current ??
            getComponentDimensions(
              component,
              document.querySelector(`[data-component-id="${component.id}"]`) as HTMLElement | null,
              scale * 100
            );

          const others =
            dragOtherRectsRef.current ??
            buildCanvasRectsForComponents(activePage.components, scale, new Set([component.id])).map(o => ({ id: o.id, rect: o.rect, shape: o.shape }));

          const resolved = resolveMoveConstraints({
            componentId: component.id,
            currentPosition: { x: component.position?.x ?? startPos.x, y: component.position?.y ?? startPos.y },
            proposedPosition: { x: newX, y: newY },
            size,
            canvas: { width: canvasWidth, height: canvasHeight },
            others,
            shapeLocal: dragActivePolyLocalRef.current ?? undefined,
            preferredPosition: useBuilderStore.getState().dragPosition ?? startPos,
            config: {
              boundaryPaddingPx: caps.dragConstraints.boundaryPaddingPx,
              collisionPaddingPx: caps.dragConstraints.collisionPaddingPx,
            },
            mode: caps.dragConstraints.mode,
            allowMoveOutOfExistingOverlap: true,
          });

          // Throttled high-signal logging (safe for DB): only when constraints change the move.
          const now = Date.now();
          const changed = resolved.position.x !== newX || resolved.position.y !== newY;
          if (changed && now - lastConstraintLogRef.current > 250) {
            lastConstraintLogRef.current = now;
            devLogger.info('fieldshell.collision.constrained', {
              componentId: component.id,
              reason: resolved.reason ?? 'collision',
              narrowPhase: dragActivePolyLocalRef.current ? 'smartborder-path' : 'aabb',
              proposed: { x: newX, y: newY },
              resolved: { x: resolved.position.x, y: resolved.position.y },
              collidingComponentIds: resolved.collidingComponentIds ?? [],
            });
          }

          newX = resolved.position.x;
          newY = resolved.position.y;
        }

        // Update live drag position (used by SortableComponent for visual positioning)
        setDragPosition({ x: newX, y: newY });
      }
    });
  };

  const handleDragEnd = (event: DragEndEvent) => {
    // Clear periodic snapshot interval
    if (dragSnapshotIntervalRef.current) {
      clearInterval(dragSnapshotIntervalRef.current);
      dragSnapshotIntervalRef.current = null;
    }

    try {
        const { active, over, delta } = event;
        
        setActiveId(null);
        // Always clear preview drag position after end
        const lastPreviewPos = useBuilderStore.getState().dragPosition;
        setDragPosition(null);

        // 1. Handle New Component from Toolbox
        // Toolbox drops require a valid droppable target (the canvas stage).
        if (active.id.toString().startsWith('toolbox-')) {
            if (!over) return;
            const type = active.data.current?.type as ComponentType;
            if (!type) return;

            const newComponent = generateComponent(type);
            
            if (canvasRef.current) {
                const canvasRect = canvasRef.current.getBoundingClientRect();
                
                // Use active.rect.current.translated for precise visual matching
                const ghostRect = active.rect.current.translated;

                // Use pointer position directly for accurate drop placement
                // This avoids issues with ghostRect not matching the DragOverlay position
                const initialPointer = initialPointerPositionRef.current;
                const pointerOffset = pointerOffsetRef.current;
                const initialSize = initialElementSizeRef.current;
                
                if (initialPointer && pointerOffset && initialSize) {
                    // Prefer live pointer position (client coords) because dnd-kit `delta`
                    // does NOT include scroll changes that can occur during a drag.
                    // When the container scrolls mid-drag, `initialPointer + delta` can even go negative,
                    // which leads to negative canvas Y that then gets clamped to 0 ("drops at top").
                    const deltaBasedPointer = {
                        x: initialPointer.x + delta.x,
                        y: initialPointer.y + delta.y,
                    };
                    const livePointer = lastPointerRef.current;

                    // Use live pointer when available; otherwise fall back to delta-based.
                    const currentPointerX =
                        Number.isFinite(livePointer?.x) ? livePointer.x : deltaBasedPointer.x;
                    const currentPointerY =
                        Number.isFinite(livePointer?.y) ? livePointer.y : deltaBasedPointer.y;

                    // Log when delta-based pointer drifts from live pointer (typically due to scroll during drag).
                    if (Number.isFinite(livePointer?.x) && Number.isFinite(livePointer?.y)) {
                        const drift = {
                            dx: livePointer.x - deltaBasedPointer.x,
                            dy: livePointer.y - deltaBasedPointer.y,
                        };
                        if (Math.abs(drift.dx) > 32 || Math.abs(drift.dy) > 32) {
                            devLogger.warn('toolbox.pointer.drift', {
                                componentType: newComponent.type,
                                componentId: newComponent.id,
                                initialPointer,
                                dragDelta: { x: delta.x, y: delta.y },
                                deltaBasedPointer,
                                livePointer,
                                drift,
                                note: 'Large drift usually means the page/container scrolled during drag; delta does not include scroll.',
                            });
                        }
                    }
                    
                    // Convert pointer position to canvas coordinates
                    const pointerCanvasX = (currentPointerX - canvasRect.left) / scale;
                    const pointerCanvasY = (currentPointerY - canvasRect.top) / scale;
                    
                    // Calculate pointer ratio within the original toolbox element
                    const pointerRatioX = pointerOffset.x / initialSize.width;
                    const pointerRatioY = pointerOffset.y / initialSize.height;
                    
                    // Canvas component dimensions (must match DragOverlay assumptions)
                    const overlayDims = getToolboxOverlayDimensions(newComponent);
                    const canvasComponentWidth = overlayDims.width;
                    const canvasComponentHeight = overlayDims.height;
                    
                    // The DragOverlay shows the canvas component with the pointer at the same ratio
                    // So the component's top-left should be positioned such that the pointer ratio is maintained
                    const scaledX = pointerCanvasX - (canvasComponentWidth * pointerRatioX);
                    const scaledY = pointerCanvasY - (canvasComponentHeight * pointerRatioY);

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

                    // ═══════════════════════════════════════════════════════════════
                    // CANVAS BOUNDARY CHECK - Ensure new components land within canvas
                    // ═══════════════════════════════════════════════════════════════
                    const canvasSettings = useBuilderStore.getState().formDefinition?.canvasSettings;
                    const canvasWidthNew = canvasSettings?.width || 1920;
                    const canvasHeightNew = canvasSettings?.height || 980;
                    
                    // Estimate component dimensions for new component.
                    // NOTE: getComponentDimensions() treats percentage widths as a generic default (300px),
                    // but for Divider we want reliable placement + visibility on drop. If width is percent,
                    // treat it as a percentage of the canvas width.
                    const baseEstimate = getComponentDimensions(newComponent, null, scale * 100);
                    let newCompWidth = baseEstimate.width;
                    let newCompHeight = baseEstimate.height;
                    const widthProp = newComponent.props?.width as string | undefined;
                    if (typeof widthProp === 'string' && widthProp.endsWith('%')) {
                        const pct = Number.parseFloat(widthProp);
                        if (Number.isFinite(pct) && pct > 0) {
                            newCompWidth = (pct / 100) * canvasWidthNew;
                        }
                    }
                    
                    // Check canvas boundary and constrain position
                    const newCompBoundary = checkCanvasBoundary(
                        droppedX,
                        droppedY,
                        newCompWidth,
                        newCompHeight,
                        canvasWidthNew,
                        canvasHeightNew,
                        0
                    );
                    
                    if (newCompBoundary.isOutOfBounds) {
                        droppedX = newCompBoundary.constrainedPosition.x;
                        droppedY = newCompBoundary.constrainedPosition.y;
                        
                        // Re-snap after constraint if grid is enabled
                        if (showGrid) {
                            droppedX = Math.round(droppedX / 8) * 8;
                            droppedY = Math.round(droppedY / 8) * 8;
                        }
                        
                        // Calculate edge positions and gaps
                        const originalEastEdge = scaledX + newCompWidth;
                        const finalEastEdge = droppedX + newCompWidth;
                        const canvasEastEdge = canvasWidthNew;
                        const gapFromEastEdge = canvasEastEdge - finalEastEdge;
                        
                        devLogger.info('collision.boundary.newComponent', {
                            componentType: newComponent.type,
                            componentId: newComponent.id,
                            originalPosition: { x: scaledX, y: scaledY },
                            constrainedPosition: { x: droppedX, y: droppedY },
                            violations: newCompBoundary.violations,
                            componentDimensions: { width: newCompWidth, height: newCompHeight },
                            canvasDimensions: { width: canvasWidthNew, height: canvasHeightNew },
                            edgePositions: {
                                original: {
                                    west: scaledX,
                                    east: originalEastEdge,
                                    north: scaledY,
                                    south: scaledY + newCompHeight
                                },
                                final: {
                                    west: droppedX,
                                    east: finalEastEdge,
                                    north: droppedY,
                                    south: droppedY + newCompHeight
                                },
                                canvas: {
                                    left: 0,
                                    right: canvasWidthNew,
                                    top: 0,
                                    bottom: canvasHeightNew
                                }
                            },
                            gapsFromCanvasEdges: {
                                left: droppedX,
                                right: gapFromEastEdge,
                                top: droppedY,
                                bottom: canvasHeightNew - (droppedY + newCompHeight)
                            }
                        });
                    }

                    const initialPosition = { x: scaledX, y: scaledY };
                    const finalPosition = { x: droppedX, y: droppedY };
                    const positionShift = {
                        deltaX: finalPosition.x - initialPosition.x,
                        deltaY: finalPosition.y - initialPosition.y
                    };
                    
                    newComponent.position = finalPosition;
                    
                    // Log component drop with position details
                    devLogger.info('component.dropped', {
                        componentId: newComponent.id,
                        componentType: newComponent.type,
                        strategy: 'canvas-component-matched',
                        dragDelta: { x: delta.x, y: delta.y },
                        initialPointer: initialPointer,
                        currentPointer: { x: currentPointerX, y: currentPointerY },
                        // Extra debugging to validate pointer math vs scroll drift
                        pointerSources: {
                            deltaBasedPointer,
                            livePointer,
                            used: Number.isFinite(livePointer?.x) && Number.isFinite(livePointer?.y) ? 'live' : 'delta',
                        },
                        canvasRect: {
                            left: canvasRect.left,
                            top: canvasRect.top
                        },
                        scale,
                        pointerInfo: {
                            offsetInToolbox: pointerOffset,
                            toolboxSize: initialSize,
                            pointerRatio: { x: pointerRatioX, y: pointerRatioY },
                            pointerCanvasPosition: { x: pointerCanvasX, y: pointerCanvasY }
                        },
                        canvasComponentSize: { width: canvasComponentWidth, height: canvasComponentHeight },
                        calculatedPosition: { x: scaledX, y: scaledY },
                        finalPosition,
                        positionShift,
                        reason: newCompBoundary.isOutOfBounds 
                            ? 'boundary-constraint' 
                            : (showGrid ? 'snap-to-grid' : 'none'),
                        gridSnap: showGrid,
                        boundaryViolations: newCompBoundary.isOutOfBounds ? newCompBoundary.violations : undefined
                    });

                    // Namespaced event for easier backend filtering (AGENT-LOGGING-GUIDE: toolbox.*)
                    devLogger.info('toolbox.component.dropped', {
                        componentId: newComponent.id,
                        componentType: newComponent.type,
                        finalPosition,
                        scale,
                        canvasRect: { left: canvasRect.left, top: canvasRect.top },
                        pointerCanvasPosition: { x: pointerCanvasX, y: pointerCanvasY },
                        pointerSources: {
                            deltaBasedPointer,
                            livePointer,
                            used: Number.isFinite(livePointer?.x) && Number.isFinite(livePointer?.y) ? 'live' : 'delta',
                        },
                        reason: newCompBoundary.isOutOfBounds
                            ? 'boundary-constraint'
                            : (showGrid ? 'snap-to-grid' : 'none'),
                    });
                    
                    addComponent(newComponent);
                } else {
                    const defaultPosition = { x: 50, y: 50 };
                    newComponent.position = defaultPosition;
                    
                    devLogger.info('component.dropped', {
                        componentId: newComponent.id,
                        componentType: newComponent.type,
                        dropCoordinates: null,
                        initialPosition: null,
                        finalPosition: defaultPosition,
                        positionShift: { deltaX: 0, deltaY: 0 },
                        reason: 'no-canvas-rect',
                        gridSnap: false
                    });
                    
                    addComponent(newComponent); 
                }
            } else {
                const defaultPosition = { x: 50, y: 50 };
                newComponent.position = defaultPosition;
                
                devLogger.info('component.dropped', {
                    componentId: newComponent.id,
                    componentType: newComponent.type,
                    dropCoordinates: null,
                    initialPosition: null,
                    finalPosition: defaultPosition,
                    positionShift: { deltaX: 0, deltaY: 0 },
                    reason: 'no-canvas-ref',
                    gridSnap: false
                });
                
                addComponent(newComponent); 
            }
            return;
        }

        // 2. Handle Moving Existing Component
        // Skip position update if this component is currently being resized
        if (active.id) {
            const def = useBuilderStore.getState().formDefinition;
            const pages = def?.desktopPages && def.desktopPages.length > 0 ? def.desktopPages : (def?.pages ?? []);
            const activePage = pages.find(p => p.id === useBuilderStore.getState().activePageId);
            const component = activePage?.components.find(c => c.id === active.id);
            const resizingComponentId = useBuilderStore.getState().resizingComponentId;

            if (component) {
                // Skip position update if this component is being resized (position is handled by resize handlers)
                if (resizingComponentId === component.id) {
                    devLogger.debug('drag.end.skipped.resizing', {
                        componentId: component.id,
                        componentType: component.type,
                        reason: 'component-being-resized'
                    });
                    return;
                }
                
                // Also check if this is a divider with very small delta (backup check)
                const scaledDeltaX = delta.x / scale;
                const scaledDeltaY = delta.y / scale;
                const deltaMagnitude = Math.sqrt(scaledDeltaX * scaledDeltaX + scaledDeltaY * scaledDeltaY);
                
                if (component.type === 'divider' && deltaMagnitude < 5) {
                    devLogger.debug('drag.end.skipped.divider', {
                        deltaMagnitude,
                        scaledDeltaX,
                        scaledDeltaY,
                        reason: 'small-delta-likely-resize'
                    });
                    return;
                }
                
                const currentX = component.position?.x || 0;
                const currentY = component.position?.y || 0;
                
                // Prefer the constrained live preview position (if available)
                let newX = lastPreviewPos?.x ?? (currentX + scaledDeltaX);
                let newY = lastPreviewPos?.y ?? (currentY + scaledDeltaY);

                // Snap to Grid Conditionally
                if (showGrid) {
                     newX = Math.round(newX / 8) * 8;
                     newY = Math.round(newY / 8) * 8;
                } else {
                     newX = Math.round(newX);
                     newY = Math.round(newY);
                }
                
                // ═══════════════════════════════════════════════════════════════
                // CANVAS BOUNDARY CHECK - Prevent components from leaving canvas
                // ═══════════════════════════════════════════════════════════════
                const canvasSettings = useBuilderStore.getState().formDefinition?.canvasSettings;
                const canvasWidth = canvasSettings?.width || 1920;
                const canvasHeight = canvasSettings?.height || 980;
                
                // Get component dimensions (try DOM first, then estimate)
                const componentElement = document.querySelector(`[data-component-id="${component.id}"]`) as HTMLElement;
                const { width: componentWidth, height: componentHeight } = getComponentDimensions(
                    component, 
                    componentElement, 
                    scale * 100
                );
                
                // Check canvas boundary and constrain position
                const boundaryResult = checkCanvasBoundary(
                    newX,
                    newY,
                    componentWidth,
                    componentHeight,
                    canvasWidth,
                    canvasHeight,
                    0 // No padding - components can touch the edge
                );
                
                // Apply constrained position if out of bounds
                if (boundaryResult.isOutOfBounds) {
                    // Capture original position BEFORE constraint
                    const originalPositionX = newX;
                    const originalPositionY = newY;
                    const originalEastEdge = newX + componentWidth;
                    const originalWestEdge = newX;
                    
                    newX = boundaryResult.constrainedPosition.x;
                    newY = boundaryResult.constrainedPosition.y;
                    
                    // Re-snap after constraint if grid is enabled
                    if (showGrid) {
                        newX = Math.round(newX / 8) * 8;
                        newY = Math.round(newY / 8) * 8;
                    }
                    
                    const finalEastEdge = newX + componentWidth;
                    const finalWestEdge = newX;
                    const gapFromEastEdge = canvasWidth - finalEastEdge;
                    const gapFromWestEdge = finalWestEdge;
                    
                    devLogger.info('collision.boundary.constrained', {
                        componentId: component.id,
                        componentType: component.type,
                        originalPosition: { x: originalPositionX, y: originalPositionY },
                        constrainedPosition: { x: newX, y: newY },
                        violations: boundaryResult.violations,
                        componentDimensions: { width: componentWidth, height: componentHeight },
                        canvasDimensions: { width: canvasWidth, height: canvasHeight },
                        edgePositions: {
                            original: {
                                west: originalWestEdge,
                                east: originalEastEdge,
                                north: newY,
                                south: newY + componentHeight
                            },
                            final: {
                                west: finalWestEdge,
                                east: finalEastEdge,
                                north: newY,
                                south: newY + componentHeight
                            },
                            canvas: {
                                left: 0,
                                right: canvasWidth,
                                top: 0,
                                bottom: canvasHeight
                            }
                        },
                        gapsFromCanvasEdges: {
                            left: gapFromWestEdge,
                            right: gapFromEastEdge,
                            top: newY,
                            bottom: canvasHeight - (newY + componentHeight)
                        }
                    });
                }
                
                // Log drag before drop
                const snapshots = dragSnapshotsRef.current.get(component.id) || { before: null, after: null };
                const snapshotBefore = snapshots.before || captureComponentSnapshot(component, null);
                
                devLogger.info('fieldshell.drag.beforeDrop', {
                  component: snapshotBefore,
                  action: 'beforeDrop'
                });

                // Check for collisions before updating position (currently logs only - doesn't block)
                const allComponents = activePage.components;
                const collisionResult = checkCollision(component, allComponents, componentRefsRef.current);
                if (collisionResult.hasCollision) {
                    devLogger.warn('fieldshell.collision.detected', {
                        draggedComponent: snapshotBefore,
                        collidingComponents: collisionResult.collidingComponents,
                        action: 'logged' // Changed from 'prevented' since we're not blocking yet
                    });
                }

                // Commit-time constraint enforcement (parity with live constraints)
                const caps = getComponentSurfaceCapabilities(component.type as any, 'canvas');
                if (caps.dragConstraints.enabled && (caps.dragConstraints.canvasBoundary || caps.dragConstraints.collisionAvoidance)) {
                    const ignore = new Set<string>([component.id]);
                    const others = buildCanvasRectsForComponents(allComponents, scale, ignore).map(o => ({ id: o.id, rect: o.rect, shape: o.shape }));
                    const resolved = resolveMoveConstraints({
                        componentId: component.id,
                        currentPosition: { x: currentX, y: currentY },
                        proposedPosition: { x: newX, y: newY },
                        size: { width: componentWidth, height: componentHeight },
                        canvas: { width: canvasWidth, height: canvasHeight },
                        others,
                        shapeLocal: dragActivePolyLocalRef.current ?? undefined,
                        config: {
                            boundaryPaddingPx: caps.dragConstraints.boundaryPaddingPx,
                            collisionPaddingPx: caps.dragConstraints.collisionPaddingPx,
                        },
                        mode: caps.dragConstraints.mode,
                        allowMoveOutOfExistingOverlap: true,
                    });
                    newX = resolved.position.x;
                    newY = resolved.position.y;
                }

                devLogger.info('fieldshell.drag.position.updated', {
                    componentId: component.id,
                    componentType: component.type,
                    from: { x: currentX, y: currentY },
                    to: { x: newX, y: newY },
                    delta: { x: scaledDeltaX, y: scaledDeltaY },
                    boundaryConstrained: boundaryResult.isOutOfBounds,
                });
                
                updateComponent(component.id, {
                    position: { x: newX, y: newY }
                });
                
                // Log drag drop (after update) - use setTimeout to ensure DOM is updated
                setTimeout(() => {
                    const updatedComponent = {
                        ...component,
                        position: { x: newX, y: newY }
                    };
                    const snapshotAfter = captureComponentSnapshot(updatedComponent, null);
                    
                    // Check collisions after drop
                    const updatedAllComponents = activePage.components.map(c => 
                        c.id === component.id ? updatedComponent : c
                    );
                    const collisionResultAfter = checkCollision(updatedComponent, updatedAllComponents, componentRefsRef.current);
                    
                    devLogger.info('fieldshell.drag.drop', {
                        componentBefore: snapshotBefore,
                        componentAfter: snapshotAfter,
                        delta: { x: scaledDeltaX, y: scaledDeltaY },
                        duration: 0, // TODO: Calculate actual duration from drag start
                        collisionDetected: collisionResultAfter.hasCollision,
                        collidingComponents: collisionResultAfter.collidingComponents
                    });
                    
                    // Clean up
                    dragSnapshotsRef.current.delete(component.id);
                }, 0);
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

  // Handle critical errors (403, 404) - don't show the builder
  if (loadError && !formDefinition) {
    const isAccessDenied = loadError.includes('Access Denied');
    const isNotFound = loadError.includes('Not Found');
    
    return (
      <div className="h-screen w-full flex items-center justify-center bg-gray-50 dark:bg-gray-900">
        <div className="max-w-md text-center p-8">
          <div className={`mx-auto w-16 h-16 rounded-full flex items-center justify-center mb-6 ${
            isAccessDenied ? 'bg-red-100 dark:bg-red-900/30' : 
            isNotFound ? 'bg-amber-100 dark:bg-amber-900/30' : 
            'bg-gray-100 dark:bg-gray-800'
          }`}>
            {isAccessDenied ? (
              <svg className="w-8 h-8 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
              </svg>
            ) : isNotFound ? (
              <svg className="w-8 h-8 text-amber-600 dark:text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            ) : (
              <svg className="w-8 h-8 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            )}
          </div>
          
          <h2 className={`text-xl font-semibold mb-2 ${
            isAccessDenied ? 'text-red-700 dark:text-red-400' : 
            isNotFound ? 'text-amber-700 dark:text-amber-400' : 
            'text-gray-700 dark:text-gray-300'
          }`}>
            {isAccessDenied ? 'Access Denied' : isNotFound ? 'Form Not Found' : 'Error Loading Form'}
          </h2>
          
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            {loadError}
          </p>
          
          <div className="flex flex-col gap-3">
            <a
              href="/dashboard"
              className="inline-flex items-center justify-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Go to Dashboard
            </a>
            {isAccessDenied && (
              <p className="text-sm text-gray-500 dark:text-gray-500">
                If you believe you should have access, please contact your administrator.
              </p>
            )}
          </div>
        </div>
      </div>
    );
  }

  const renderOverlayContent = (component: FormComponent | null) => {
      // DragOverlay is ONLY used for TOOLBOX items (new components being dragged to canvas)
      // For EXISTING canvas components, SmartBorder is the single source of truth - no overlay needed
      // Check if activeId starts with 'toolbox-' to determine if this is a toolbox drag
      if (!activeId?.toString().startsWith('toolbox-')) {
          // Canvas component drag - SmartBorder handles visualization
          return null;
      }
      
      // Toolbox drag - show a preview since the component doesn't exist on canvas yet
      if (!component) return null;

      // Show the ACTUAL canvas component in the DragOverlay
      // This ensures what you see during drag = what you get on drop
      const content = (() => {
        const componentDef = ComponentRegistry[component.type];
        
        // Use UniversalFieldShell - the same component that renders on canvas
        if (componentDef?.structure) {
          const structure = componentDef.structure;
          const renderers = getRenderersForComponent(component.type, structure, component);
          return (
            <UniversalFieldShell
              structure={structure}
              renderers={renderers}
              surface="toolbox"
              objectLayout={component.props.objectLayout}
              layoutGroups={component.props.layoutGroups}
              styleOverrides={component.props.styleOverrides}
              globalStyles={formDefinition?.globalStyles}
              componentId={component.id}
              component={component}
              builderMode={{
                showBorder: true,
                borderPadding: 5,
                isSelected: true,
                isDragging: true,
              }}
            />
          );
        }
        
        // Fallback: Use previewComponent if it exists
        if (componentDef?.previewComponent) {
            return componentDef.previewComponent;
        }
        
        // Final fallback
        return <ComponentPreview component={component} isOverlay={true} />;
      })();

      // The DragOverlay shows the canvas component (UniversalFieldShell)
      // We need to translate so the pointer stays at the correct position
      const pointerOffset = pointerOffsetRef.current || { x: 0, y: 0 };
      const initialSize = initialElementSizeRef.current || { width: 250, height: 101 };
      
      // Canvas component dimensions (must match drop placement assumptions)
      const overlayDims = component ? getToolboxOverlayDimensions(component) : { width: 380, height: 106 };
      const canvasComponentWidth = overlayDims.width;
      const canvasComponentHeight = overlayDims.height;
      
      // The pointer was at (pointerOffset.x, pointerOffset.y) within the toolbox item (initialSize)
      // In the canvas component, we want the pointer to be at the same RATIO
      const pointerRatioX = pointerOffset.x / initialSize.width;
      const pointerRatioY = pointerOffset.y / initialSize.height;
      
      // Position within the canvas component where the pointer should be
      const pointerInCanvasComponentX = canvasComponentWidth * pointerRatioX;
      const pointerInCanvasComponentY = canvasComponentHeight * pointerRatioY;
      
      // After scaling, the pointer position in screen coords relative to element top-left
      const pointerScreenOffsetX = pointerInCanvasComponentX * scale;
      const pointerScreenOffsetY = pointerInCanvasComponentY * scale;
      
      // dnd-kit positions the overlay so the cursor is at pointerOffset from the element's top-left
      // We need to translate so the cursor is at pointerScreenOffset instead
      const translateX = pointerOffset.x - pointerScreenOffsetX;
      const translateY = pointerOffset.y - pointerScreenOffsetY;
      
      return (
        <div style={{
          transform: `translate(${translateX}px, ${translateY}px) scale(${scale})`,
          transformOrigin: 'top left',
        }}>
          {content}
        </div>
      );
  };

  if (!formId) {
    return (
      <div className="h-screen w-full flex items-center justify-center bg-gray-50">
        <div className="max-w-md text-center p-6 bg-white rounded-lg shadow-sm border border-gray-200">
          <h2 className="text-lg font-semibold text-gray-800 mb-2">Missing form id</h2>
          <p className="text-sm text-gray-600 mb-4">
            Open the builder with a valid form id, for example:
          </p>
          <div className="text-xs text-gray-700 bg-gray-100 rounded px-3 py-2">
            /builder?formId=YOUR_FORM_ID
          </div>
        </div>
      </div>
    );
  }

  if (isInlinePreviewOpen) {
    return (
      <BuilderLayout
        sidebar={<ComponentSidebar />}
        propertiesPanel={<PropertiesPanel />}
        title={formDefinition?.formId ? `Form: ${formDefinition.formId}` : 'Form Builder'}
        formId={formId}
        onToggleInlinePreview={handleToggleInlinePreview}
        isInlinePreviewOpen={isInlinePreviewOpen}
        isInlinePreviewLoading={isInlinePreviewLoading}
        onOpenPreview={openPreviewInNewTab}
        isPreviewLoading={isPublicPreviewLoading}
      >
        <div className="flex flex-col h-full">
          {publicPreviewError && (
            <div className="bg-red-50 border-b border-red-200 px-4 py-2 text-sm text-red-900">
              {publicPreviewError}
            </div>
          )}
          <div className="flex-1 min-h-0 bg-gray-50">
            {isInlinePreviewLoading ? (
              <div className="p-6 text-sm text-gray-600">Preparing preview…</div>
            ) : formDefinition ? (
              <PublicFormArtboard
                definition={formDefinition}
                embed={true}
                layoutMode="builder"
                containerClassName="h-full"
                containerStyle={{ height: '100%' }}
              />
            ) : (
              <div className="p-6 text-sm text-gray-600">No definition available.</div>
            )}
          </div>
        </div>
      </BuilderLayout>
    );
  }

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCenter}
      onDragStart={handleDragStart}
      onDragMove={handleDragMove}
      onDragEnd={handleDragEnd}
      // Conditionally apply the snap modifier
      modifiers={showGrid ? [snapToGridModifier] : []}
    >
      <BuilderLayout
        sidebar={<ComponentSidebar />}
        propertiesPanel={<PropertiesPanel />}
        title={formDefinition?.formId ? `Form: ${formDefinition.formId}` : 'Form Builder'}
        formId={formId}
        onToggleInlinePreview={handleToggleInlinePreview}
        isInlinePreviewOpen={isInlinePreviewOpen}
        isInlinePreviewLoading={isInlinePreviewLoading}
        onOpenPreview={openPreviewInNewTab}
        isPreviewLoading={isPublicPreviewLoading}
      >
        <div className="flex flex-col h-full">
          {publicPreviewError && (
            <div className="bg-red-50 border-b border-red-200 px-4 py-2 text-sm text-red-900">
              {publicPreviewError}
            </div>
          )}
          <FormBuilderCanvas ref={canvasRef} />
        </div>
      </BuilderLayout>

      <DragOverlay dropAnimation={dropAnimationConfig}>
        {renderOverlayContent(activeComponent)}
      </DragOverlay>
    </DndContext>
  );
};
