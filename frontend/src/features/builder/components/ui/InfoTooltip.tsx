import React, { useState, useRef, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { HelpCircle, CheckCircle, XCircle, AlertTriangle, Lightbulb, Sparkles } from 'lucide-react';
import { RuleEducationalInfo } from '../../types/validationRule.types';

interface InfoTooltipProps {
    /** Educational info to display */
    info: RuleEducationalInfo;
    /** Size of the help icon */
    size?: number;
    /** Custom className for the container */
    className?: string;
}

/**
 * InfoTooltip - Educational tooltip with pros/cons for validation rules
 * 
 * Features:
 * - HelpCircle icon that triggers tooltip
 * - Click to show (mobile-friendly)
 * - Hover to show (desktop)
 * - Structured layout for pros/cons lists
 * - Dark theme, smart positioning
 * - Auto-fix indicator when applicable
 * - Uses portal to escape parent overflow constraints
 */
export const InfoTooltip: React.FC<InfoTooltipProps> = ({
    info,
    size = 14,
    className = '',
}) => {
    const [isVisible, setIsVisible] = useState(false);
    const [tooltipStyle, setTooltipStyle] = useState<React.CSSProperties>({});
    const containerRef = useRef<HTMLDivElement>(null);
    const tooltipRef = useRef<HTMLDivElement>(null);

    // Calculate optimal position using fixed positioning (relative to viewport)
    useEffect(() => {
        if (isVisible && containerRef.current) {
            const iconRect = containerRef.current.getBoundingClientRect();
            const viewportHeight = window.innerHeight;
            const viewportWidth = window.innerWidth;
            
            // Tooltip dimensions (estimate if not yet rendered)
            const tooltipWidth = 280; // Fixed width
            const tooltipHeight = tooltipRef.current?.offsetHeight || 200;
            
            // Calculate position - prefer to show to the right of the icon
            let left = iconRect.right + 8;
            let top = iconRect.top;
            
            // If tooltip would overflow right edge, show to left of icon
            if (left + tooltipWidth > viewportWidth - 16) {
                left = iconRect.left - tooltipWidth - 8;
            }
            
            // If still overflows left, center horizontally and show below
            if (left < 16) {
                left = Math.max(16, (viewportWidth - tooltipWidth) / 2);
                top = iconRect.bottom + 8;
            }
            
            // Vertical positioning - keep within viewport
            if (top + tooltipHeight > viewportHeight - 16) {
                top = viewportHeight - tooltipHeight - 16;
            }
            if (top < 16) {
                top = 16;
            }
            
            setTooltipStyle({
                position: 'fixed',
                left: `${left}px`,
                top: `${top}px`,
                width: `${tooltipWidth}px`,
                zIndex: 9999,
            });
        }
    }, [isVisible]);

    // Close tooltip when clicking outside
    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
                setIsVisible(false);
            }
        };

        const handleScroll = () => {
            setIsVisible(false);
        };

        if (isVisible) {
            document.addEventListener('mousedown', handleClickOutside);
            document.addEventListener('scroll', handleScroll, true);
        }

        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
            document.removeEventListener('scroll', handleScroll, true);
        };
    }, [isVisible]);

    const handleClick = (e: React.MouseEvent) => {
        e.stopPropagation();
        setIsVisible(!isVisible);
    };

    const handleMouseEnter = () => {
        setIsVisible(true);
    };

    const handleMouseLeave = () => {
        setIsVisible(false);
    };

    const hasPros = info.pros && info.pros.length > 0;
    const hasCons = info.cons && info.cons.length > 0;

    // Render tooltip in a portal to escape parent overflow constraints
    const tooltipContent = isVisible && (
        <div
            ref={tooltipRef}
            style={tooltipStyle}
            className="p-3 rounded-lg shadow-xl bg-gray-900 dark:bg-gray-800 text-white text-xs border border-gray-700"
            role="tooltip"
            onMouseEnter={() => setIsVisible(true)}
            onMouseLeave={() => setIsVisible(false)}
        >
            {/* Content */}
            <div className="space-y-2.5 max-h-[60vh] overflow-y-auto">
                {/* Example - shown first for context */}
                {info.example && (
                    <div className="bg-gray-800 dark:bg-gray-700 p-2 rounded font-mono text-xs">
                        <div className="text-gray-400 mb-1">Example:</div>
                        <div className="text-cyan-300">{info.example}</div>
                    </div>
                )}

                {/* Pros */}
                {hasPros && (
                    <div>
                        <div className="flex items-center gap-1.5 text-green-400 font-medium mb-1.5">
                            <CheckCircle size={12} />
                            <span>Benefits</span>
                        </div>
                        <ul className="space-y-1 text-gray-300 ml-4">
                            {info.pros.map((pro, i) => (
                                <li key={i} className="flex items-start gap-1.5">
                                    <span className="text-green-400 mt-0.5">•</span>
                                    <span>{pro}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                )}

                {/* Cons */}
                {hasCons && (
                    <div>
                        <div className="flex items-center gap-1.5 text-amber-400 font-medium mb-1.5">
                            <XCircle size={12} />
                            <span>Considerations</span>
                        </div>
                        <ul className="space-y-1 text-gray-300 ml-4">
                            {info.cons.map((con, i) => (
                                <li key={i} className="flex items-start gap-1.5">
                                    <span className="text-amber-400 mt-0.5">•</span>
                                    <span>{con}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                )}

                {/* Best For */}
                {info.bestFor && (
                    <div className="flex items-start gap-1.5 text-blue-300 bg-blue-900/30 p-2 rounded">
                        <Lightbulb size={12} className="mt-0.5 flex-shrink-0" />
                        <span><strong>Best for:</strong> {info.bestFor}</span>
                    </div>
                )}

                {/* Warning */}
                {info.warning && (
                    <div className="flex items-start gap-1.5 text-orange-300 bg-orange-900/30 p-2 rounded">
                        <AlertTriangle size={12} className="mt-0.5 flex-shrink-0" />
                        <span>{info.warning}</span>
                    </div>
                )}

                {/* Auto-Fix Indicator */}
                {info.canAutoFix && info.autoFixDescription && (
                    <div className="flex items-start gap-1.5 text-purple-300 bg-purple-900/30 p-2 rounded">
                        <Sparkles size={12} className="mt-0.5 flex-shrink-0" />
                        <span><strong>Auto-fix:</strong> {info.autoFixDescription}</span>
                    </div>
                )}
            </div>
        </div>
    );

    return (
        <div 
            ref={containerRef}
            className={`relative inline-flex items-center ${className}`}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
        >
            {/* Help Icon */}
            <button
                type="button"
                onClick={handleClick}
                className="text-gray-400 hover:text-blue-500 dark:text-gray-500 dark:hover:text-blue-400 
                    transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-1 
                    rounded-full p-0.5"
                aria-label="More information"
            >
                <HelpCircle size={size} />
            </button>

            {/* Tooltip rendered via portal to escape overflow constraints */}
            {tooltipContent && createPortal(tooltipContent, document.body)}
        </div>
    );
};

/**
 * Compact version of InfoTooltip - just shows the icon with a simple tooltip
 */
interface SimpleTooltipProps {
    text: string;
    size?: number;
    className?: string;
}

export const SimpleTooltip: React.FC<SimpleTooltipProps> = ({
    text,
    size = 14,
    className = '',
}) => {
    const [isVisible, setIsVisible] = useState(false);

    return (
        <div 
            className={`relative inline-flex items-center ${className}`}
            onMouseEnter={() => setIsVisible(true)}
            onMouseLeave={() => setIsVisible(false)}
        >
            <HelpCircle 
                size={size} 
                className="text-gray-400 hover:text-blue-500 dark:text-gray-500 dark:hover:text-blue-400 
                    transition-colors cursor-help"
            />

            {isVisible && (
                <div
                    className="absolute z-50 px-2 py-1 rounded shadow-lg 
                        bg-gray-900 dark:bg-gray-800 text-white text-xs
                        whitespace-nowrap
                        bottom-full mb-2 left-1/2 -translate-x-1/2"
                >
                    {text}
                    <div 
                        className="absolute left-1/2 -translate-x-1/2 bottom-[-4px] 
                            w-2 h-2 bg-gray-900 dark:bg-gray-800 rotate-45"
                    />
                </div>
            )}
        </div>
    );
};

export default InfoTooltip;
