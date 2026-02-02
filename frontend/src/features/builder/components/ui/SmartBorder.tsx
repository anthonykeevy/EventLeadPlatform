import React, { useLayoutEffect, useRef, useState, useEffect, useCallback } from 'react';
import { devLogger } from '../../utils/devLogger';

interface SmartBorderProps {
    children: React.ReactNode | React.ReactNode[]; 
    padding?: number; 
    dragListeners?: unknown;
    dragAttributes?: unknown;
    isSelected?: boolean;
    isDragging?: boolean; // Track drag state for logging
    isResizing?: boolean; // Disable transitions during resize for smoother visual feedback
    componentId?: string; // For collision detection identification
    /** Default is shrink-to-content. Use "fill" when children need to respect parent width (e.g. divider with 100%). */
    layout?: 'shrink' | 'fill';
    /** Preview width (in px) for E/W resize - forces border to draw at this width regardless of content */
    previewWidth?: number;
}

export const SmartBorder = React.forwardRef<HTMLDivElement, SmartBorderProps>(({ 
    children, 
    padding = 5, 
    dragListeners, 
    dragAttributes,
    isSelected = false,
    isDragging: _isDragging = false,
    isResizing = false,
    componentId,
    layout = 'shrink',
    previewWidth,
}, ref) => {
    void _isDragging;
    const containerRef = useRef<HTMLDivElement | null>(null);
    
    // Merge forwarded ref with internal ref
    const mergedRef = useCallback((node: HTMLDivElement | null) => {
        containerRef.current = node;
        if (typeof ref === 'function') {
            ref(node);
        } else if (ref) {
            ref.current = node;
        }
    }, [ref]);
    const [pathD, setPathD] = useState('');
    const svgRef = useRef<SVGSVGElement | null>(null);
    const pathRef = useRef<SVGPathElement | null>(null);
    
    const calculatePath = () => {
        if (!containerRef.current) {
            devLogger.debug('smartborder.calculate.skip', {
                componentId,
                reason: 'no-container',
                layout,
                padding,
                isSelected,
                isResizing,
                hasDragListeners: !!dragListeners,
            });
            return;
        }

        const contentWrapper = containerRef.current.querySelector('[data-smart-content]') as HTMLElement;
        if (!contentWrapper) {
            devLogger.debug('smartborder.calculate.skip', {
                componentId,
                reason: 'no-content-wrapper',
                layout,
                padding,
                isSelected,
                isResizing,
                hasDragListeners: !!dragListeners,
            });
            return;
        }

        // Note: contentWrapper children are usually layout GROUPS (divs).
        // To wrap the actual content tightly, we must look inside these groups 
        // to find the individual leaf elements (Label, Input, etc.)
        const groupNodes = Array.from(contentWrapper.children) as HTMLElement[];
        if (groupNodes.length === 0) {
            devLogger.debug('smartborder.calculate.skip', {
                componentId,
                reason: 'no-groups',
                layout,
                padding,
                isSelected,
                isResizing,
                hasDragListeners: !!dragListeners,
            });
            return;
        }

        // Use offsetWidth/offsetHeight for UNSCALED dimensions
        // During E/W resize, use previewWidth to force border to follow the preview
        const measuredWidth = contentWrapper.offsetWidth;
        const parentWidth = previewWidth !== undefined ? previewWidth : measuredWidth;
        const parentHeight = contentWrapper.offsetHeight;
        
        if (parentWidth === 0 || parentHeight === 0) {
            devLogger.debug('smartborder.calculate.skip', {
                componentId,
                reason: 'zero-size',
                layout,
                padding,
                isSelected,
                isResizing,
                hasDragListeners: !!dragListeners,
                parentWidth,
                parentHeight,
            });
            return;
        }

        // ============================================================
        // ROBUST GEOMETRIC UNION APPROACH (Dual Skyline Algorithm)
        // ============================================================

        const p = padding;
        const wrapperRect = contentWrapper.getBoundingClientRect();
        const containerRect = containerRef.current.getBoundingClientRect();
        
        const contentStyles = window.getComputedStyle(contentWrapper);
        const gridContainer = contentWrapper.querySelector('[data-layout-type="grid"]') as HTMLElement | null;
        const gridWidth = gridContainer ? Math.round(gridContainer.getBoundingClientRect().width) : null;
        const paddingLeftPx = parseFloat(contentStyles.paddingLeft || '0');
        const paddingRightPx = parseFloat(contentStyles.paddingRight || '0');
        const paddingTotal = paddingLeftPx + paddingRightPx;
        const widthBudget = gridWidth !== null
            ? {
                parentWidth,
                gridWidth,
                paddingLeftPx,
                paddingRightPx,
                paddingTotal,
                remainder: Math.round(parentWidth - (gridWidth + paddingTotal)),
            }
            : null;
        // Correct for potential scaling transform on the container
        // If the wrapper is scaled, getBoundingClientRect returns scaled values,
        // but the SVG coordinate system is local to the container (before scale).
        // We calculate scale factor by comparing BoundingRect to offsetWidth.
        const scaleX = parentWidth > 0 ? wrapperRect.width / parentWidth : 1;
        const scaleY = parentHeight > 0 ? wrapperRect.height / parentHeight : 1;

        // Safety check for degenerate scale
        if (scaleX === 0 || scaleY === 0) {
            devLogger.debug('smartborder.calculate.skip', {
                componentId,
                reason: 'degenerate-scale',
                layout,
                padding,
                isSelected,
                isResizing,
                hasDragListeners: !!dragListeners,
                scaleX,
                scaleY,
            });
            return;
        }

        // Calculate offsets relative to container, UN-SCALED
        const wrapperOffsetX = (wrapperRect.left - containerRect.left) / scaleX;
        const wrapperOffsetY = (wrapperRect.top - containerRect.top) / scaleY;

        devLogger.debug('smartborder.calculate.start', {
            componentId,
            layout,
            padding,
            isSelected,
            isResizing,
            hasDragListeners: !!dragListeners,
            parent: {
                width: parentWidth,
                height: parentHeight,
            },
            wrapperRect: {
                width: wrapperRect.width,
                height: wrapperRect.height,
            },
            containerRect: {
                width: containerRect.width,
                height: containerRect.height,
            },
            wrapperOffset: {
                x: wrapperOffsetX,
                y: wrapperOffsetY,
            },
            scale: {
                x: scaleX,
                y: scaleY,
            },
            contentPadding: {
                left: contentStyles.paddingLeft,
                right: contentStyles.paddingRight,
                top: contentStyles.paddingTop,
                bottom: contentStyles.paddingBottom,
                boxSizing: contentStyles.boxSizing,
            },
            gridWidth,
            widthBudget,
            groupCount: groupNodes.length,
            groupChildCounts: groupNodes.map(group => group.children.length),
        });

        if (isResizing && widthBudget && widthBudget.remainder < -2) {
            devLogger.debug('smartborder.calculate.defer', {
                componentId,
                reason: 'width-budget-negative',
                widthBudget,
                parentWidth,
                gridWidth,
            });
            return;
        }

        // 1. Convert children to Padded Segments
        interface Segment {
            yStart: number;
            yEnd: number;
            xLeft: number;
            xRight: number;
            source?: {
                tag: string;
                className?: string;
                dataGridObject?: string | null;
                dataLayoutGroup?: string | null;
                dataComponentId?: string | null;
                role?: string | null;
            };
        }

        const segments: Segment[] = [];
        
        const getMeasurementTarget = (node: HTMLElement): HTMLElement => {
            if (typeof window === 'undefined') return node;
            const style = window.getComputedStyle(node);
            if (style?.display === 'contents' && node.firstElementChild instanceof HTMLElement) {
                return node.firstElementChild;
            }
            return node;
        };

        // Helper to process an element into a segment
        const createSegment = (el: HTMLElement, sourceEl?: HTMLElement): Segment | null => {
            if (!el) return null;
            const elRect = el.getBoundingClientRect();
            if (elRect.width === 0 || elRect.height === 0) {
                const sourceNode = sourceEl || el;
                devLogger.debug('smartborder.segment.skipped', {
                    componentId,
                    reason: 'zero-size',
                    source: {
                        tag: sourceNode.tagName.toLowerCase(),
                        dataGridObject: sourceNode.getAttribute('data-grid-object'),
                        dataLayoutGroup: sourceNode.getAttribute('data-layout-group'),
                        dataComponentId: sourceNode.getAttribute('data-component-id'),
                        role: sourceNode.getAttribute('role'),
                    },
                    rect: {
                        width: elRect.width,
                        height: elRect.height,
                    },
                });
                return null;
            }

            // Calculate coordinates relative to wrapper using getBoundingClientRect for accuracy
            // UN-SCALE the delta to get local coordinates
            const top = (elRect.top - wrapperRect.top) / scaleY;
            const left = (elRect.left - wrapperRect.left) / scaleX;
            const width = elRect.width / scaleX;
            const height = elRect.height / scaleY;
            
            // We use the full visual height. 
            // Previous logic subtracted marginBottom which caused labels to be cut off.
            // getBoundingClientRect().height includes padding+border but NOT margin.
            // So we want the full height.
            const visualHeight = height;
            const bottom = top + visualHeight;

            // Create padded segment
            const yStart = (wrapperOffsetY + top) - p;
            const yEnd = (wrapperOffsetY + bottom) + p;
            const xLeft = (wrapperOffsetX + left) - p;
            const xRight = (wrapperOffsetX + left + width) + p;
            
            // Log segment creation details
            const sourceNode = sourceEl || el;
            devLogger.debug('smartborder.segment.created', {
                componentId,
                objectId: sourceNode.getAttribute('data-grid-object'),
                rawRect: {
                    top: elRect.top,
                    left: elRect.left,
                    width: elRect.width,
                    height: elRect.height,
                },
                wrapperRect: {
                    top: wrapperRect.top,
                    left: wrapperRect.left,
                },
                scale: { x: scaleX, y: scaleY },
                unscaled: {
                    top,
                    left,
                    width,
                    height,
                    bottom,
                },
                wrapperOffset: { x: wrapperOffsetX, y: wrapperOffsetY },
                padding: p,
                segment: {
                    yStart,
                    yEnd,
                    xLeft,
                    xRight,
                    segmentHeight: yEnd - yStart,
                },
            });
            
            return {
                yStart,
                yEnd,
                xLeft,
                xRight,
                source: {
                    tag: sourceNode.tagName.toLowerCase(),
                    className: sourceNode.className || undefined,
                    dataGridObject: sourceNode.getAttribute('data-grid-object'),
                    dataLayoutGroup: sourceNode.getAttribute('data-layout-group'),
                    dataComponentId: sourceNode.getAttribute('data-component-id'),
                    role: sourceNode.getAttribute('role'),
                },
            };
        };

        const gridObjectNodes = Array.from(
            contentWrapper.querySelectorAll('[data-grid-object]')
        ) as HTMLElement[];
        const componentRoot = contentWrapper.closest('[data-component-id]') as HTMLElement | null;
        const fallbackGridObjectNodes = gridObjectNodes.length === 0 && componentRoot
            ? (Array.from(componentRoot.querySelectorAll('[data-grid-object]')) as HTMLElement[])
            : [];
        const activeGridNodes = gridObjectNodes.length > 0 ? gridObjectNodes : fallbackGridObjectNodes;
        devLogger.debug('smartborder.calculate.gridObjects', {
            componentId,
            gridObjectCount: activeGridNodes.length,
            gridObjectIds: activeGridNodes.map(node => node.getAttribute('data-grid-object')).filter(Boolean),
            gridObjectMetrics: activeGridNodes.map(node => {
                const rect = node.getBoundingClientRect();
                const target = getMeasurementTarget(node);
                const targetRect = target.getBoundingClientRect();
                return {
                    id: node.getAttribute('data-grid-object'),
                    display: window.getComputedStyle(node).display,
                    width: rect.width,
                    height: rect.height,
                    targetTag: target.tagName.toLowerCase(),
                    targetWidth: targetRect.width,
                    targetHeight: targetRect.height,
                };
            }),
        });

        if (activeGridNodes.length > 0) {
            activeGridNodes.forEach(node => {
                const target = getMeasurementTarget(node);
                const seg = createSegment(target, node);
                if (seg) segments.push(seg);
            });
        } else {
            // Iterate groups and their children
            groupNodes.forEach(group => {
                // Layout detection via data attribute (preferred) or style fallback
                const _groupLayout = group.getAttribute('data-layout-group');
                void _groupLayout;
                // We don't need special "Row Alignment" logic if we trust the Skyline algorithm
                // and correct height measurements. The user requested we respect height variations.
                
                const children = Array.from(group.children) as HTMLElement[];
                if (children.length > 0) {
                    children.forEach(child => {
                        const seg = createSegment(child);
                        if (seg) segments.push(seg);
                    });
                } else {
                    const seg = createSegment(group);
                    if (seg) segments.push(seg);
                }
            });
        }

        // During E/W resize preview, add a synthetic segment that spans the full previewWidth
        // This forces the border to extend to the preview width even if children are smaller
        if (previewWidth !== undefined && segments.length > 0) {
            // Find the Y bounds of existing segments
            const minY = Math.min(...segments.map(s => s.yStart));
            const maxY = Math.max(...segments.map(s => s.yEnd));
            // Find the left edge of existing segments
            const minX = Math.min(...segments.map(s => s.xLeft));
            
            // Find the rightmost segment to determine where to place synthetic preview
            // We want the synthetic preview to only extend as tall as needed
            const rightmostSegments = segments.filter(s => {
                const segRight = s.xRight;
                return segments.every(other => other.xRight <= segRight + 1); // Within 1px
            });
            
            // Use the Y bounds of only the rightmost segments, not all segments
            const previewMinY = Math.min(...rightmostSegments.map(s => s.yStart));
            const previewMaxY = Math.max(...rightmostSegments.map(s => s.yEnd));
            
            // Create synthetic right-edge segment at previewWidth
            // The segment is 1px wide at the right edge, spanning only the rightmost segments' height
            const syntheticRightX = wrapperOffsetX + previewWidth + p;
            segments.push({
                yStart: previewMinY,
                yEnd: previewMaxY,
                xLeft: syntheticRightX - 1,  // 1px wide segment at right edge
                xRight: syntheticRightX,
                source: {
                    tag: 'synthetic-preview',
                    className: 'preview-right-edge',
                },
            });
            devLogger.debug('smartborder.preview.synthetic-segment', {
                componentId,
                previewWidth,
                syntheticRightX,
                yBounds: { min: previewMinY, max: previewMaxY },
                originalBounds: { min: minY, max: maxY },
                rightmostSegmentCount: rightmostSegments.length,
                existingMinX: minX,
            });
        }

        if (segments.length === 0) {
            devLogger.debug('smartborder.calculate.skip', {
                componentId,
                reason: 'no-segments',
                layout,
                padding,
                isSelected,
                isResizing,
                hasDragListeners: !!dragListeners,
            });
            return;
        }
        devLogger.debug('smartborder.segments.final', {
            componentId,
            segmentCount: segments.length,
            segmentSources: segments.map(seg => seg.source?.dataGridObject ?? seg.source?.tag ?? 'unknown'),
            bounds: {
                minX: Math.min(...segments.map(seg => seg.xLeft)),
                maxX: Math.max(...segments.map(seg => seg.xRight)),
                minY: Math.min(...segments.map(seg => seg.yStart)),
                maxY: Math.max(...segments.map(seg => seg.yEnd)),
            },
        });

        // 2. Generate Unique Ys
        const uniqueYs = new Set<number>();
        
        segments.forEach(seg => {
            uniqueYs.add(seg.yStart);
            uniqueYs.add(seg.yEnd);
        });
        
        const sortedYs = Array.from(uniqueYs).sort((a, b) => a - b);
        
        // Helper to generate a profile (Left or Right)
        const generateProfile = (side: 'left' | 'right') => {
            const points: {x: number, y: number}[] = [];
            const isRight = side === 'right';
            const defaultX = isRight ? wrapperOffsetX - p : wrapperOffsetX + parentWidth + p;

            // We do NOT initialize with defaultX to avoid spurious "ears"
            // The first iteration will set the start point.

            for (let i = 0; i < sortedYs.length - 1; i++) {
                const y1 = sortedYs[i];
                const y2 = sortedYs[i+1];
                const midY = (y1 + y2) / 2;
                
                let bestX = isRight ? -Infinity : Infinity;
                let hasSegment = false;

                segments.forEach(seg => {
                    if (seg.yStart <= midY && seg.yEnd >= midY) {
                        hasSegment = true;
                        if (isRight) {
                            bestX = Math.max(bestX, seg.xRight);
                        } else {
                            bestX = Math.min(bestX, seg.xLeft);
                        }
                    }
                });

                if (!hasSegment) {
                    // Gap Logic
                    const prevSeg = segments.find(s => Math.abs(s.yEnd - y1) < 0.1);
                    const nextSeg = segments.find(s => Math.abs(s.yStart - y2) < 0.1);

                    if (prevSeg && nextSeg) {
                        // Bridge Gap
                        const prevX = isRight ? prevSeg.xRight : prevSeg.xLeft;
                        const nextX = isRight ? nextSeg.xRight : nextSeg.xLeft;
                        
                        let stepY;
                        const useNext = isRight ? (nextX < prevX) : (nextX > prevX);
                        devLogger.debug('smartborder.profile.bridge', {
                            componentId,
                            side,
                            y1,
                            y2,
                            prevX,
                            nextX,
                            useNext,
                        });
                        
                        if (useNext) {
                            stepY = y1;
                        } else {
                            stepY = y2;
                        }

                        // Ensure start point / vertical continuity
                        if (points.length === 0) {
                             points.push({ x: prevX, y: y1 });
                        } else {
                             const lastPoint = points[points.length - 1];
                             if (Math.abs(lastPoint.y - stepY) > 0.1) {
                                  points.push({ x: prevX, y: stepY });
                             }
                        }
                        
                        points.push({ x: nextX, y: stepY });

                    } else if (prevSeg) {
                        // Trailing Gap: Extend Prev
                        const prevX = isRight ? prevSeg.xRight : prevSeg.xLeft;
                        if (points.length === 0) points.push({ x: prevX, y: y1 });
                        points.push({ x: prevX, y: y2 }); 
                        devLogger.debug('smartborder.profile.gap.trailing', {
                            componentId,
                            side,
                            y1,
                            y2,
                            prevX,
                        });
                    } else if (nextSeg) {
                        // Leading Gap: Extend Next (Backwards)
                        const nextX = isRight ? nextSeg.xRight : nextSeg.xLeft;
                        points.push({ x: nextX, y: y1 });
                        devLogger.debug('smartborder.profile.gap.leading', {
                            componentId,
                            side,
                            y1,
                            y2,
                            nextX,
                        });
                    } else {
                        // Full Gap
                        if (points.length === 0) points.push({ x: defaultX, y: y1 });
                        // We need to extend to y2 to cover the height
                         const lastPoint = points[points.length - 1];
                         points.push({ x: lastPoint.x, y: y2 });
                        devLogger.debug('smartborder.profile.gap.full', {
                            componentId,
                            side,
                            y1,
                            y2,
                            defaultX,
                        });
                    }
                } else {
                    // Content Logic
                    if (points.length === 0) {
                        points.push({ x: bestX, y: y1 });
                    } else {
                        const lastPoint = points[points.length - 1];
                        if (Math.abs(lastPoint.x - bestX) > 1) {
                            if (Math.abs(lastPoint.y - y1) > 0.1) {
                                points.push({ x: lastPoint.x, y: y1 });
                            }
                            points.push({ x: bestX, y: y1 });
                        }
                    }
                }
            }
            
            // Final point at bottom
            const lastY = sortedYs[sortedYs.length - 1];
            if (points.length > 0) {
                const lastX = points[points.length - 1].x;
                points.push({ x: lastX, y: lastY });
            }
            
            return points;
        };

        const rightPoints = generateProfile('right');
        const leftPoints = generateProfile('left');

        // Combine Points
        const finalPoints: {x: number, y: number}[] = [];
        
        if (leftPoints.length > 0 && rightPoints.length > 0) {
            // Add Left[0]
            finalPoints.push(leftPoints[0]);
            // Add Right Points
            rightPoints.forEach(pt => finalPoints.push(pt));
            // Add Left Points Reversed
            for (let i = leftPoints.length - 1; i >= 0; i--) {
                finalPoints.push(leftPoints[i]);
            }
        }

        const pathString = finalPoints.map((pt, i) => 
            (i === 0 ? 'M' : 'L') + ` ${pt.x} ${pt.y}`
        ).join(' ') + ' Z';
        const bounds = finalPoints.reduce(
            (acc, pt) => ({
                minX: Math.min(acc.minX, pt.x),
                minY: Math.min(acc.minY, pt.y),
                maxX: Math.max(acc.maxX, pt.x),
                maxY: Math.max(acc.maxY, pt.y),
            }),
            { minX: Number.POSITIVE_INFINITY, minY: Number.POSITIVE_INFINITY, maxX: Number.NEGATIVE_INFINITY, maxY: Number.NEGATIVE_INFINITY }
        );
        const boundsSummary = finalPoints.length
            ? {
                minX: Math.round(bounds.minX * 1000) / 1000,
                minY: Math.round(bounds.minY * 1000) / 1000,
                maxX: Math.round(bounds.maxX * 1000) / 1000,
                maxY: Math.round(bounds.maxY * 1000) / 1000,
                width: Math.round((bounds.maxX - bounds.minX) * 1000) / 1000,
                height: Math.round((bounds.maxY - bounds.minY) * 1000) / 1000,
            }
            : null;
        let pathHash = 0;
        finalPoints.forEach(pt => {
            const x = Math.round(pt.x * 10);
            const y = Math.round(pt.y * 10);
            pathHash = (pathHash * 31 + x + y) % 1000000007;
        });

        setPathD(pathString);
        
        if (componentId) {
            devLogger.debug('smartborder.path.calculated', {
                componentId,
                algorithm: 'DualSkyline',
                segments,
                sortedYs,
                hasDragListeners: !!dragListeners,
                pathDLength: pathString.length,
                pointCount: finalPoints.length,
                pathHash,
                bounds: boundsSummary,
                parent: { width: parentWidth, height: parentHeight },
                wrapperOffset: { x: wrapperOffsetX, y: wrapperOffsetY },
                scale: { x: scaleX, y: scaleY },
            });
        }
    };

    // Initial calculation after mount
    useEffect(() => {
        const timer = setTimeout(() => {
            calculatePath();
        }, 50);
        return () => clearTimeout(timer);
    }, []);

    useLayoutEffect(() => {
        let rafId: number | null = null;
        let isScheduled = false;
        
        const scheduleCalculation = () => {
            if (isScheduled) return; // Already scheduled, skip
            isScheduled = true;
            rafId = requestAnimationFrame(() => {
                isScheduled = false;
                calculatePath();
            });
        };
        
        scheduleCalculation();
        
        if (!containerRef.current) {
            return () => {
                if (rafId !== null) {
                    cancelAnimationFrame(rafId);
                }
            };
        }
        
        const observer = new ResizeObserver(() => {
            scheduleCalculation(); // Batch via RAF, prevent multiple rapid calls
        });
        
        const contentWrapper = containerRef.current.querySelector('[data-smart-content]');
        if (contentWrapper) {
            observer.observe(contentWrapper);
            Array.from(contentWrapper.children).forEach(c => observer.observe(c));
        }
        
        return () => {
            if (rafId !== null) {
                cancelAnimationFrame(rafId);
            }
            observer.disconnect();
        };
    }, [children, padding, previewWidth]);

    useLayoutEffect(() => {
        if (!pathD || !pathRef.current || !svgRef.current || !componentId) return;
        const rafId = requestAnimationFrame(() => {
            try {
                const pathBox = pathRef.current?.getBBox();
                const svgBox = svgRef.current?.getBoundingClientRect();
                if (!pathBox || !svgBox) return;
                devLogger.debug('smartborder.rendered.bbox', {
                    componentId,
                    isResizing,
                    pathDLength: pathD.length,
                    pathBBox: {
                        x: pathBox.x,
                        y: pathBox.y,
                        width: pathBox.width,
                        height: pathBox.height,
                    },
                    svgRect: {
                        width: svgBox.width,
                        height: svgBox.height,
                    },
                });
            } catch (error) {
                devLogger.debug('smartborder.rendered.bbox', {
                    componentId,
                    isResizing,
                    error: (error as Error)?.message ?? 'unknown-error',
                });
            }
        });
        return () => cancelAnimationFrame(rafId);
    }, [pathD, componentId, isResizing]);

    // Border styles based on selection state
    const borderClasses = isSelected 
        ? 'text-blue-500 dark:text-blue-400'
        : 'text-slate-400 dark:text-slate-500 group-hover:text-teal-400 dark:group-hover:text-teal-500';

    const strokeWidth = isSelected ? 2.5 : 1.5;
    const strokeDasharray = isSelected ? 'none' : '4 4';
    const hasDragHandlers = !!dragListeners;
    const cursorClasses = hasDragHandlers ? 'cursor-grab active:cursor-grabbing' : '';
    const wrapperClassName = layout === 'fill' ? 'relative block w-full group' : 'relative inline-block group';
    const contentClassName =
        layout === 'fill'
            ? 'relative z-10 flex flex-col items-stretch pointer-events-none w-full'
            : 'relative z-10 inline-flex flex-col items-start pointer-events-none';

    return (
        <div 
            className={wrapperClassName} 
            ref={mergedRef}
            data-component-id={componentId}
        >
            {pathD && (
                <svg 
                    className={`absolute top-0 left-0 overflow-visible pointer-events-none ${isResizing ? '' : 'transition-all duration-300'}`}
                    style={{ zIndex: 20 }}
                    ref={svgRef}
                >
                    <path 
                        d={pathD} 
                        fill="transparent" 
                        stroke="currentColor"
                        ref={pathRef}
                        strokeWidth={strokeWidth}
                        strokeDasharray={strokeDasharray}
                        strokeLinejoin="round"
                        vectorEffect="non-scaling-stroke"
                        className={`${isResizing ? '' : 'transition-colors duration-300'} ${cursorClasses} ${borderClasses}`}
                        style={{ 
                            pointerEvents: hasDragHandlers ? 'auto' : 'none',
                            outline: 'none',
                        }} 
                        {...(dragListeners as React.SVGProps<SVGPathElement>)}
                        {...(dragAttributes as React.SVGProps<SVGPathElement>)}
                    />
                </svg>
            )}

            <div 
                data-smart-content 
                className={contentClassName}
                style={{ padding: `${padding}px` }}
            >
                {children}
            </div>
        </div>
    );
});
