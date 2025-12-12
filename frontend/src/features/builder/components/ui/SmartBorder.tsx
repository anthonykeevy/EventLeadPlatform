import React, { useLayoutEffect, useRef, useState, useEffect } from 'react';

interface SmartBorderProps {
    children: React.ReactNode | React.ReactNode[]; 
    padding?: number; 
    dragListeners?: unknown;
    dragAttributes?: unknown;
    isSelected?: boolean;
}

export const SmartBorder: React.FC<SmartBorderProps> = ({ 
    children, 
    padding = 5, 
    dragListeners, 
    dragAttributes,
    isSelected = false 
}) => {
    const containerRef = useRef<HTMLDivElement>(null);
    const [pathD, setPathD] = useState('');
    
    const calculatePath = () => {
        if (!containerRef.current) return;

        const contentWrapper = containerRef.current.querySelector('[data-smart-content]') as HTMLElement;
        if (!contentWrapper) return;

        const childNodes = Array.from(contentWrapper.children) as HTMLElement[];
        if (childNodes.length === 0) return;

        // Use offsetWidth/offsetHeight for UNSCALED dimensions (not affected by CSS transforms)
        // This prevents double-scaling when parent has transform: scale()
        const parentWidth = contentWrapper.offsetWidth;
        const parentHeight = contentWrapper.offsetHeight;
        
        // Early exit if not laid out yet
        if (parentWidth === 0 || parentHeight === 0) return;

        // Calculate profiles using offset properties (unscaled CSS dimensions)
        const profiles: { y: number; h: number; w: number; b: number }[] = childNodes.map(el => {
            return {
                y: el.offsetTop,
                h: el.offsetHeight,
                w: el.offsetWidth,
                b: el.offsetTop + el.offsetHeight
            };
        });

        profiles.sort((a, b) => a.y - b.y);

        const p = padding;
        const points: {x: number, y: number}[] = [];
        
        points.push({ x: -p, y: -p });
        points.push({ x: profiles[0].w + p, y: -p });

        for (let i = 0; i < profiles.length; i++) {
            const curr = profiles[i];
            const next = profiles[i + 1];

            const rightX = curr.w + p;
            const segmentEndY = next 
                ? curr.b + (next.y - curr.b) / 2 
                : curr.b + p; 

            points.push({ x: rightX, y: segmentEndY });

            if (next) {
                const nextRightX = next.w + p;
                if (Math.abs(nextRightX - rightX) > 1) {
                    points.push({ x: nextRightX, y: segmentEndY });
                }
            }
        }

        const last = profiles[profiles.length - 1];
        points.push({ x: -p, y: last.b + p });
        points.push({ x: -p, y: -p });

        const pathString = points.map((pt, i) => 
            (i === 0 ? 'M' : 'L') + ` ${pt.x} ${pt.y}`
        ).join(' ') + ' Z';

        setPathD(pathString);
    };

    // Initial calculation after mount with a small delay to ensure DOM is ready
    useEffect(() => {
        const timer = setTimeout(() => {
            calculatePath();
        }, 50);
        return () => clearTimeout(timer);
    }, []);

    useLayoutEffect(() => {
        // Calculate on children change
        requestAnimationFrame(calculatePath);
        
        if (!containerRef.current) return;
        
        const observer = new ResizeObserver(() => {
            requestAnimationFrame(calculatePath);
        });
        
        const contentWrapper = containerRef.current.querySelector('[data-smart-content]');
        if (contentWrapper) {
            observer.observe(contentWrapper);
            Array.from(contentWrapper.children).forEach(c => observer.observe(c));
        }
        
        return () => observer.disconnect();
    }, [children, padding]);

    // Border styles based on selection state
    const borderClasses = isSelected 
        ? 'text-blue-500 dark:text-blue-400' // Selected: blue
        : 'text-slate-400 dark:text-slate-500 group-hover:text-teal-400 dark:group-hover:text-teal-500'; // Default with hover

    const strokeWidth = isSelected ? 2.5 : 1.5;
    const strokeDasharray = isSelected ? 'none' : '4 4';

    // Determine if we have drag handlers (for cursor style)
    const hasDragHandlers = !!dragListeners;
    const cursorClasses = hasDragHandlers ? 'cursor-grab active:cursor-grabbing' : '';

    return (
        <div className="relative inline-block group" ref={containerRef}>
            {/* SVG Overlay with smart path - only shows when path is calculated */}
            {pathD && (
                <svg 
                    className="absolute top-0 left-0 overflow-visible transition-all duration-300"
                    style={{ zIndex: 0 }}
                >
                    <path 
                        d={pathD} 
                        fill="transparent" 
                        stroke="currentColor"
                        strokeWidth={strokeWidth}
                        strokeDasharray={strokeDasharray}
                        strokeLinejoin="round"
                        className={`transition-colors duration-300 ${cursorClasses} ${borderClasses}`}
                        style={{ 
                            pointerEvents: hasDragHandlers ? 'auto' : 'none',
                            outline: 'none', // Remove browser's rectangular focus outline
                        }} 
                        {...(dragListeners as React.SVGProps<SVGPathElement>)}
                        {...(dragAttributes as React.SVGProps<SVGPathElement>)}
                    />
                </svg>
            )}

            {/* Content Wrapper */}
            <div 
                data-smart-content 
                className="relative z-10 inline-flex flex-col items-start pointer-events-none"
            >
                {children}
            </div>
        </div>
    );
};
