/**
 * BackgroundImageCanvas - Story 5.1 T06 WYSIWYG
 * Background image as a draggable/resizable canvas component when in Background mode.
 * Uses @dnd-kit useDraggable and ResizeHandles (corner + optional edge handles).
 * Live resize preview via onResize; lock aspect ratio controls handle set.
 */

import React, { useCallback, useState, useRef, useEffect } from 'react';
import { useDraggable } from '@dnd-kit/core';
import { ResizeHandles, HandlePosition } from './ui/ResizeHandles';
import { useBuilderStore } from '../stores/useBuilderStore';
import { createDefaultPlacement, isBackgroundFullyOffCanvas } from '../utils/backgroundPlacementUtils';
import type { BackgroundPlacement, BackgroundDefinition } from '../types/builder.types';

const PAGE_BACKGROUND_ID = 'page-background';

export interface BackgroundImageCanvasProps {
  /** Resolved image URL */
  imageUrl: string | null;
  /** Background definition (placement, crop, etc.) */
  background: NonNullable<BackgroundDefinition>;
  /** Canvas dimensions (base px) */
  canvasWidth: number;
  canvasHeight: number;
  /** Canvas scale (0.2–1) for screen→canvas conversion */
  scale: number;
  /** Whether we're in Background layer mode (interactive) */
  isBackgroundMode: boolean;
  /** Whether image is loading */
  isLoading?: boolean;
}

export const BackgroundImageCanvas: React.FC<BackgroundImageCanvasProps> = ({
  imageUrl,
  background,
  canvasWidth,
  canvasHeight,
  scale,
  isBackgroundMode,
  isLoading,
}) => {
  const updatePageBackground = useBuilderStore((s) => s.updatePageBackground);
  const storePlacement: BackgroundPlacement =
    background.placement ?? createDefaultPlacement(canvasWidth, canvasHeight);
  const [previewPlacement, setPreviewPlacement] = useState<BackgroundPlacement | null>(null);
  const resizeStartRef = useRef<BackgroundPlacement | null>(null);
  const placement = previewPlacement ?? storePlacement;
  const { position: pos, size: sz, crop } = placement;
  const assetW = background.asset?.widthPx ?? 1;
  const assetH = background.asset?.heightPx ?? 1;
  const opacity = background.opacity ?? 1;
  const imagePosition = background.imagePosition || 'center';
  const rawSize = background.imageSize || 'contain';
  const objectFit = (rawSize === 'tile' || rawSize === 'auto') ? 'cover' : (rawSize === 'fill' ? 'fill' : rawSize);
  const lockAspectRatio = background.lockAspectRatio ?? (rawSize !== 'fill');

  useEffect(() => {
    if (!isBackgroundMode) setPreviewPlacement(null);
  }, [isBackgroundMode]);

  // When object-fit is contain, the visible image is letterboxed. Compute its rect so handles sit on visible corners.
  const visibleRect = React.useMemo(() => {
    if (rawSize !== 'contain' || !assetW || !assetH) return null;
    const fitScale = Math.min(sz.width / assetW, sz.height / assetH);
    const w = assetW * fitScale;
    const h = assetH * fitScale;
    const left = (sz.width - w) / 2;
    const top = (sz.height - h) / 2;
    return { left, top, width: w, height: h };
  }, [rawSize, sz.width, sz.height, assetW, assetH]);

  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    isDragging,
  } = useDraggable({
    id: PAGE_BACKGROUND_ID,
    data: { type: 'page-background' },
    disabled: !isBackgroundMode || !imageUrl,
  });

  const style: React.CSSProperties = {
    position: 'absolute',
    left: pos.x,
    top: pos.y,
    width: sz.width,
    height: sz.height,
    opacity,
    overflow: 'visible',
    // Live drag: dnd-kit transform is in screen px; convert to canvas px
    transform: transform
      ? `translate(${transform.x / scale}px, ${transform.y / scale}px)`
      : undefined,
    zIndex: 1,
    pointerEvents: isBackgroundMode && imageUrl ? 'auto' : 'none',
  };

  const applyResizeDelta = useCallback(
    (base: BackgroundPlacement, deltaWidth: number, deltaHeight: number, handle: HandlePosition): BackgroundPlacement => {
      const dx = deltaWidth / scale;
      const dy = deltaHeight / scale;
      const { position: p, size: s } = base;
      let newPos = { ...p };
      let newSize = { ...s };
      const minSize = 20;
      // ResizeHandles passes signed deltas: positive = expand in handle direction
      const cfg: Record<string, { px: number; py: number; dw: number; dh: number }> = {
        nw: { px: -dx, py: -dy, dw: dx, dh: dy },
        ne: { px: 0, py: -dy, dw: dx, dh: dy },
        se: { px: 0, py: 0, dw: dx, dh: dy },
        sw: { px: -dx, py: 0, dw: dx, dh: dy },
        e: { px: 0, py: 0, dw: dx, dh: 0 },
        w: { px: -dx, py: 0, dw: dx, dh: 0 },
        n: { px: 0, py: -dy, dw: 0, dh: dy },
        s: { px: 0, py: 0, dw: 0, dh: dy },
      };
      const c = cfg[handle];
      if (c) {
        newPos = { x: p.x + c.px, y: p.y + c.py };
        newSize = { width: Math.max(minSize, s.width + c.dw), height: Math.max(minSize, s.height + c.dh) };
      }
      return { ...base, position: newPos, size: newSize };
    },
    [scale]
  );

  const handleResizeStart = useCallback(() => {
    resizeStartRef.current = storePlacement;
    setPreviewPlacement(storePlacement);
  }, [storePlacement]);

  const handleResize = useCallback(
    (deltaWidth: number, deltaHeight: number, handle: HandlePosition) => {
      const base = resizeStartRef.current ?? storePlacement;
      const next = applyResizeDelta(base, deltaWidth, deltaHeight, handle);
      setPreviewPlacement(next);
    },
    [storePlacement, applyResizeDelta]
  );

  const clearPreview = useCallback(() => {
    resizeStartRef.current = null;
    setPreviewPlacement(null);
  }, []);

  const handleCornerResizeEnd = useCallback(
    (handle: HandlePosition, deltaX: number, deltaY: number) => {
      const base = resizeStartRef.current ?? storePlacement;
      const next = applyResizeDelta(base, deltaX, deltaY, handle);
      if (isBackgroundFullyOffCanvas(next, canvasWidth, canvasHeight)) {
        updatePageBackground({ asset: undefined, value: '', placement: undefined }, 'Remove background');
      } else {
        updatePageBackground({ placement: next }, 'Resize background');
      }
    },
    [storePlacement, applyResizeDelta, scale, canvasWidth, canvasHeight, updatePageBackground]
  );

  const handleWidthResizeEnd = useCallback(
    (handle: 'e' | 'w', newWidth: number) => {
      const base = resizeStartRef.current ?? storePlacement;
      const { position: p, size: s } = base;
      const minSize = 20;
      const w = Math.max(minSize, newWidth);
      let newPos = p;
      if (handle === 'w') {
        newPos = { x: p.x + s.width - w, y: p.y };
      }
      const next: BackgroundPlacement = { ...base, position: newPos, size: { ...s, width: w } };
      if (isBackgroundFullyOffCanvas(next, canvasWidth, canvasHeight)) {
        updatePageBackground({ asset: undefined, value: '', placement: undefined }, 'Remove background');
      } else {
        updatePageBackground({ placement: next }, 'Resize background');
      }
    },
    [storePlacement, canvasWidth, canvasHeight, updatePageBackground]
  );

  const handleVerticalResizeEnd = useCallback(
    (handle: 'n' | 's', deltaY: number) => {
      const dy = deltaY / scale;
      const base = resizeStartRef.current ?? storePlacement;
      const { position: p, size: s } = base;
      const minSize = 20;
      let newPos = p;
      let newH = s.height;
      if (handle === 'n') {
        newPos = { x: p.x, y: p.y - dy };
        newH = Math.max(minSize, s.height + dy);
      } else {
        newH = Math.max(minSize, s.height + dy);
      }
      const next: BackgroundPlacement = { ...base, position: newPos, size: { ...s, height: newH } };
      if (isBackgroundFullyOffCanvas(next, canvasWidth, canvasHeight)) {
        updatePageBackground({ asset: undefined, value: '', placement: undefined }, 'Remove background');
      } else {
        updatePageBackground({ placement: next }, 'Resize background');
      }
    },
    [storePlacement, scale, canvasWidth, canvasHeight, updatePageBackground]
  );

  const fullyOffCanvas = isBackgroundFullyOffCanvas(placement, canvasWidth, canvasHeight);
  if (fullyOffCanvas) return null;

  if (isLoading || !imageUrl) {
    return (
      <div
        className="absolute inset-0 z-0 bg-gray-100 animate-pulse"
        style={{ pointerEvents: 'none' }}
      />
    );
  }

  return (
    <div
      ref={setNodeRef}
      style={style}
      className="group"
      data-component-id={PAGE_BACKGROUND_ID}
      data-id={PAGE_BACKGROUND_ID}
      onClick={(e) => e.stopPropagation()}
      onPointerDown={(e) => e.stopPropagation()}
      {...(isBackgroundMode && imageUrl ? { ...attributes, ...listeners } : {})}
    >
      {crop && assetW > 0 && assetH > 0 ? (
        <div
          className="w-full h-full"
          style={{
            backgroundImage: `url(${imageUrl})`,
            backgroundSize: `${assetW * (sz.width / crop.width)}px ${assetH * (sz.height / crop.height)}px`,
            backgroundPosition: `${-crop.x * (sz.width / crop.width)}px ${-crop.y * (sz.height / crop.height)}px`,
          }}
        />
      ) : rawSize === 'tile' ? (
        <div
          className="w-full h-full"
          style={{
            backgroundImage: `url(${imageUrl})`,
            backgroundSize: `${assetW}px ${assetH}px`,
            backgroundRepeat: 'repeat',
            backgroundPosition: imagePosition,
          }}
        />
      ) : (
        <img
          src={imageUrl}
          alt="Background"
          className="w-full h-full"
          style={{
            objectFit: objectFit as React.CSSProperties['objectFit'],
            objectPosition: imagePosition,
          }}
          draggable={false}
        />
      )}

      {/* Resize handles - on visible image corners. When Fit (contain) letterboxes, use visible rect. */}
      {isBackgroundMode && imageUrl && (
        <div
          className="absolute"
          style={{
            ...(visibleRect
              ? { left: visibleRect.left, top: visibleRect.top, width: visibleRect.width, height: visibleRect.height }
              : { inset: 0 }),
            pointerEvents: 'none',
          }}
        >
          <ResizeHandles
              isSelected={true}
              currentWidth={`${sz.width}px`}
              currentHeight={sz.height}
              currentScale={scale * 100}
              componentId={PAGE_BACKGROUND_ID}
              hideCornerHandles={false}
              onResizeStart={handleResizeStart}
              onResize={handleResize}
              onResizeEnd={clearPreview}
              onCornerResizeEnd={handleCornerResizeEnd}
              onWidthChange={undefined}
              onWidthResizeEnd={lockAspectRatio ? undefined : handleWidthResizeEnd}
              onSpacingChange={undefined}
              onHeightChange={undefined}
              onVerticalResizeEnd={lockAspectRatio ? undefined : handleVerticalResizeEnd}
              minWidth={20}
              minHeight={20}
              cornerHandleSizePx={8}
            />
        </div>
      )}

      {isDragging && (
        <div
          className="absolute inset-0 bg-white/50"
          style={{ pointerEvents: 'none' }}
        />
      )}
    </div>
  );
};
