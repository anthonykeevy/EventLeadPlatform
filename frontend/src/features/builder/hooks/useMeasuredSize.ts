import { useCallback, useEffect, useState } from 'react';

export type MeasuredSize = { width: number; height: number };

/**
 * Observe an element's rendered size (px) using ResizeObserver.
 * Returns a callback ref + the latest size.
 */
export function useMeasuredSize<T extends HTMLElement>(): {
    ref: (node: T | null) => void;
    size: MeasuredSize;
} {
    const [node, setNode] = useState<T | null>(null);
    const [size, setSize] = useState<MeasuredSize>({ width: 0, height: 0 });

    const ref = useCallback((node: T | null) => {
        setNode(node);
        if (node) {
            const r = node.getBoundingClientRect();
            setSize({ width: Math.round(r.width), height: Math.round(r.height) });
        }
    }, []);

    useEffect(() => {
        if (!node) return;
        if (typeof ResizeObserver === 'undefined') return;

        const ro = new ResizeObserver(entries => {
            const entry = entries[0];
            if (!entry) return;
            const cr = entry.contentRect;
            setSize({ width: Math.round(cr.width), height: Math.round(cr.height) });
        });
        ro.observe(node);
        return () => ro.disconnect();
    }, [node]);

    return { ref, size };
}

