import React from 'react';

type HandleSide = 'e';

export interface InputWidthHandlesProps {
  /** Whether handles should render at all (selection + not locked) */
  enabled: boolean;
  /** Builder canvas scale (0.2-1). Used to convert screen px to canvas px for positioning. */
  canvasScale: number;
  /** Outer component container (the `relative` wrapper in SortableComponent) */
  outerRef: React.RefObject<HTMLElement | null>;
  /** Input element id (e.g. `${componentId}-input`) */
  inputElementId: string;
  /** Called once when user starts dragging */
  onResizeStart?: () => void;
  /** Called during drag with the next width (canvas px) */
  onResizePreview?: (nextWidthPx: number) => void;
  /** Called on pointer up with final width (canvas px) */
  onResizeCommit?: (finalWidthPx: number) => void;
  /** Min width clamp in px */
  minWidthPx?: number;
  /** Max width clamp in px */
  maxWidthPx?: number;
}

function clamp(n: number, min: number, max: number) {
  return Math.max(min, Math.min(max, n));
}

/**
 * InputWidthHandles
 *
 * Renders a small "E" handle on the input object itself so the user can
 * set `props.inputWidthOverride` without affecting label/help widths.
 *
 * Note: This is builder/canvas-only UI; it relies on DOM measurement.
 */
export const InputWidthHandles: React.FC<InputWidthHandlesProps> = ({
  enabled,
  canvasScale,
  outerRef,
  inputElementId,
  onResizeStart,
  onResizePreview,
  onResizeCommit,
  minWidthPx = 40,
  maxWidthPx = 2000,
}) => {
  const [overlay, setOverlay] = React.useState<{ left: number; top: number; width: number; height: number } | null>(
    null
  );
  const dragRef = React.useRef<{
    side: HandleSide;
    startX: number;
    startWidth: number;
  } | null>(null);

  // Measure the input element and project it into outer-container coordinates (unscaled).
  const measure = React.useCallback(() => {
    if (!enabled) return;
    const outer = outerRef.current;
    if (!outer) return;
    const inputEl = document.getElementById(inputElementId);
    if (!inputEl) return;

    const outerRect = outer.getBoundingClientRect();
    const inputRect = inputEl.getBoundingClientRect();

    const scale = canvasScale || 1;
    const left = (inputRect.left - outerRect.left) / scale;
    const top = (inputRect.top - outerRect.top) / scale;
    const width = inputRect.width / scale;
    const height = inputRect.height / scale;

    // Hide if degenerate (e.g., not yet laid out)
    if (width <= 1 || height <= 1) return;
    setOverlay({ left, top, width, height });
  }, [enabled, outerRef, inputElementId, canvasScale]);

  React.useEffect(() => {
    if (!enabled) {
      setOverlay(null);
      return;
    }

    let raf = 0;
    const schedule = () => {
      if (raf) return;
      raf = window.requestAnimationFrame(() => {
        raf = 0;
        measure();
      });
    };

    schedule(); // initial measure

    const outer = outerRef.current;
    if (!outer) return () => window.cancelAnimationFrame(raf);

    const ro = new ResizeObserver(schedule);
    ro.observe(outer);

    let observedInput: HTMLElement | null = null;

    const tryObserveInput = () => {
      const el = document.getElementById(inputElementId) as HTMLElement | null;
      if (el && el !== observedInput) {
        observedInput = el;
        ro.observe(el);
      }
    };

    // Input may be mounted/unmounted as component switches. Observe DOM mutations to re-hook.
    const mo = new MutationObserver(() => {
      tryObserveInput();
      schedule();
    });
    mo.observe(outer, { childList: true, subtree: true });

    // Window resize/scroll can change bounding rects even if element sizes don't.
    window.addEventListener('resize', schedule);
    window.addEventListener('scroll', schedule, true);

    tryObserveInput();

    return () => {
      window.cancelAnimationFrame(raf);
      window.removeEventListener('resize', schedule);
      window.removeEventListener('scroll', schedule, true);
      mo.disconnect();
      ro.disconnect();
    };
  }, [enabled, measure]);

  const onPointerMove = React.useCallback(
    (e: PointerEvent) => {
      const drag = dragRef.current;
      if (!drag) return;
      const scale = canvasScale || 1;
      const delta = (e.clientX - drag.startX) / scale;
      const next = clamp(drag.startWidth + delta, minWidthPx, maxWidthPx);
      onResizePreview?.(Math.round(next));
    },
    [canvasScale, minWidthPx, maxWidthPx, onResizePreview]
  );

  const onPointerUp = React.useCallback(
    (e: PointerEvent) => {
      const drag = dragRef.current;
      if (!drag) return;
      dragRef.current = null;
      window.removeEventListener('pointermove', onPointerMove);
      window.removeEventListener('pointerup', onPointerUp);

      const scale = canvasScale || 1;
      const delta = (e.clientX - drag.startX) / scale;
      const final = clamp(drag.startWidth + delta, minWidthPx, maxWidthPx);
      onResizeCommit?.(Math.round(final));
    },
    [canvasScale, minWidthPx, maxWidthPx, onPointerMove, onResizeCommit]
  );

  const handlePointerDown = React.useCallback(
    (e: React.PointerEvent) => {
      if (!enabled) return;
      e.stopPropagation();
      e.preventDefault();

      const inputEl = document.getElementById(inputElementId);
      if (!inputEl) return;
      const scale = canvasScale || 1;
      const inputRect = inputEl.getBoundingClientRect();
      const startWidth = inputRect.width / scale;

      dragRef.current = {
        side: 'e',
        startX: e.clientX,
        startWidth,
      };

      onResizeStart?.();
      window.addEventListener('pointermove', onPointerMove);
      window.addEventListener('pointerup', onPointerUp);
    },
    [enabled, inputElementId, canvasScale, onResizeStart, onPointerMove, onPointerUp]
  );

  if (!enabled || !overlay) return null;

  return (
    <div
      style={{
        position: 'absolute',
        left: overlay.left,
        top: overlay.top,
        width: overlay.width,
        height: overlay.height,
        pointerEvents: 'none',
        zIndex: 60,
      }}
      aria-hidden="true"
    >
      {/* Right (E) handle */}
      <div
        onPointerDown={handlePointerDown}
        style={{
          position: 'absolute',
          right: -4,
          top: '50%',
          transform: 'translateY(-50%)',
          width: 8,
          height: 8,
          backgroundColor: '#10B981', // emerald-500
          border: '1px solid #FFFFFF',
          borderRadius: 2,
          cursor: 'ew-resize',
          boxShadow: '0 1px 2px rgba(0,0,0,0.2)',
          pointerEvents: 'auto',
          touchAction: 'none',
        }}
        title="Adjust input width"
      />
    </div>
  );
};


