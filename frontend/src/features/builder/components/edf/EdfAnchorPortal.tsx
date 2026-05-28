import React, { useLayoutEffect, useState } from 'react';
import { createPortal } from 'react-dom';

/** Dedicated root for all EDF overlays (above absolute-positioned artboard fields). */
export const EDF_OVERLAY_ROOT_ID = 'edf-overlay-root';

/** z-index for portaled EDF surfaces — must exceed artboard field wrappers (incl. lifted fields). */
export const EDF_OVERLAY_Z_INDEX = 2147483000;

function getOrCreateOverlayRoot(): HTMLElement {
  if (typeof document === 'undefined') {
    throw new Error('EdfAnchorPortal requires document');
  }
  let root = document.getElementById(EDF_OVERLAY_ROOT_ID);
  if (!root) {
    root = document.createElement('div');
    root.id = EDF_OVERLAY_ROOT_ID;
    root.setAttribute('data-edf-overlay-root', 'true');
    Object.assign(root.style, {
      position: 'fixed',
      inset: '0',
      pointerEvents: 'none',
      zIndex: String(EDF_OVERLAY_Z_INDEX),
      isolation: 'isolate',
    });
    document.body.appendChild(root);
  }
  return root;
}

interface EdfAnchorPortalProps {
  open: boolean;
  anchorRef: React.RefObject<HTMLElement | null>;
  children: React.ReactNode;
  /** When set, portal is at least this wide (visual px). Omit to match anchor width exactly. */
  minWidth?: number;
  /**
   * Optional artboard CSS scale hint. Prefer auto-detection from the anchor element
   * (layout width vs getBoundingClientRect) because portals render outside the scaled canvas.
   */
  contentScale?: number;
}

/** Detect effective CSS scale on an element (e.g. ancestor transform: scale). */
function detectAnchorScale(el: HTMLElement): number {
  const layoutWidth = el.offsetWidth;
  const visualWidth = el.getBoundingClientRect().width;
  if (layoutWidth <= 0 || visualWidth <= 0) return 1;
  const ratio = visualWidth / layoutWidth;
  if (!Number.isFinite(ratio) || ratio <= 0) return 1;
  if (Math.abs(ratio - 1) < 0.02) return 1;
  return ratio;
}

function resolveContentScale(anchor: HTMLElement | null, contentScale?: number): number {
  const detected = anchor ? detectAnchorScale(anchor) : 1;
  if (detected !== 1) return detected;
  if (
    contentScale != null &&
    Number.isFinite(contentScale) &&
    contentScale > 0 &&
    contentScale !== 1
  ) {
    return contentScale;
  }
  return 1;
}

/**
 * Renders EDF floating UI in a fixed portal above the artboard.
 */
export const EdfAnchorPortal: React.FC<EdfAnchorPortalProps> = ({
  open,
  anchorRef,
  children,
  minWidth,
  contentScale,
}) => {
  const [position, setPosition] = useState<{
    top: number;
    left: number;
    width: number;
    scale: number;
  } | null>(null);

  useLayoutEffect(() => {
    if (!open) {
      setPosition(null);
      return;
    }

    const update = () => {
      const el = anchorRef.current;
      if (!el) return;
      const rect = el.getBoundingClientRect();
      const scale = resolveContentScale(el, contentScale);
      const width =
        minWidth != null ? Math.max(rect.width, minWidth) : Math.max(rect.width, 1);
      setPosition({
        top: rect.bottom + 4,
        left: rect.left,
        width,
        scale,
      });
    };

    update();
    window.addEventListener('scroll', update, true);
    window.addEventListener('resize', update);
    return () => {
      window.removeEventListener('scroll', update, true);
      window.removeEventListener('resize', update);
    };
  }, [open, anchorRef, minWidth, contentScale]);

  if (!open || !position) return null;

  const { scale, width, top, left } = position;
  const innerWidth = scale !== 1 ? width / scale : width;
  const overlayRoot = getOrCreateOverlayRoot();

  return createPortal(
    <div
      className="pointer-events-auto"
      style={{
        position: 'fixed',
        top,
        left,
        width,
        maxWidth: width,
        pointerEvents: 'auto',
        overflow: 'visible',
      }}
    >
      <div
        style={{
          width: innerWidth,
          transform: scale !== 1 ? `scale(${scale})` : undefined,
          transformOrigin: 'top left',
        }}
      >
        {children}
      </div>
    </div>,
    overlayRoot
  );
};
