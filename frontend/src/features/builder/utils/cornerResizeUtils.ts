/**
 * Corner resize utilities
 *
 * Corner handles are non-proportional 2-axis resize:
 * - NW = W + N
 * - NE = E + N
 * - SE = E + S
 * - SW = W + S
 */
export type CornerHandle = 'nw' | 'ne' | 'se' | 'sw';

export function isCornerHandle(handle: string): handle is CornerHandle {
    return handle === 'nw' || handle === 'ne' || handle === 'se' || handle === 'sw';
}

export function cornerToEdges(handle: CornerHandle): { horizontal: 'e' | 'w'; vertical: 'n' | 's' } {
    switch (handle) {
        case 'nw':
            return { horizontal: 'w', vertical: 'n' };
        case 'ne':
            return { horizontal: 'e', vertical: 'n' };
        case 'se':
            return { horizontal: 'e', vertical: 's' };
        case 'sw':
            return { horizontal: 'w', vertical: 's' };
        default: {
            // Exhaustive check
            const _exhaustive: never = handle;
            return _exhaustive;
        }
    }
}

