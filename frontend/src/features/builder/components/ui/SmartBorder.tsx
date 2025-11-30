import React, { useLayoutEffect, useRef, useState } from 'react';

interface SmartBorderProps {
  children: React.ReactNode[]; 
  padding?: number; 
  dragListeners?: any; // Listeners from dnd-kit
  dragAttributes?: any; // Attributes from dnd-kit
}

export const SmartBorder: React.FC<SmartBorderProps> = ({ children, padding = 5, dragListeners, dragAttributes }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [pathD, setPathD] = useState('');
  
  const calculatePath = () => {
    if (!containerRef.current) return;

    const contentWrapper = containerRef.current.querySelector('[data-smart-content]');
    if (!contentWrapper) return;

    const childNodes = Array.from(contentWrapper.children) as HTMLElement[];
    if (childNodes.length === 0) return;

    const parentRect = contentWrapper.getBoundingClientRect();

    const profiles: { y: number; h: number; w: number; r: number; b: number }[] = childNodes.map(el => {
        const rect = el.getBoundingClientRect();
        return {
            y: rect.top - parentRect.top,
            h: rect.height,
            w: rect.width,
            r: rect.right - parentRect.left,
            b: rect.bottom - parentRect.top
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

  useLayoutEffect(() => {
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
  }, [children]);

  return (
    <div className="relative inline-block group" ref={containerRef}>
        {/* SVG Overlay */}
        <svg 
            className="absolute top-0 left-0 overflow-visible transition-all duration-300"
            style={{ zIndex: 0 }}
        >
            <path 
                d={pathD} 
                fill="transparent" 
                stroke="currentColor" // Use currentColor for easy theming
                strokeWidth="1.5" 
                strokeDasharray="4 4"
                strokeLinejoin="round"
                // Light: stroke-slate-400, Dark: stroke-slate-500
                className="text-slate-400 dark:text-slate-500 transition-colors duration-300 group-hover:text-teal-400 dark:group-hover:text-teal-500 cursor-grab active:cursor-grabbing"
                style={{ pointerEvents: 'auto' }} 
                // ATTACH DRAG LISTENERS TO THE SVG PATH HITBOX
                {...dragListeners}
                {...dragAttributes}
            />
        </svg>

        {/* Content Wrapper */}
        <div 
            data-smart-content 
            className="relative z-10 flex flex-col items-start pointer-events-none [&_*]:pointer-events-none"
        >
            {children}
        </div>
    </div>
  );
};
