import { describe, expect, it } from 'vitest';
import { cornerToEdges, isCornerHandle } from '../cornerResizeUtils';

describe('cornerResizeUtils', () => {
    it('isCornerHandle identifies corner handles', () => {
        expect(isCornerHandle('nw')).toBe(true);
        expect(isCornerHandle('ne')).toBe(true);
        expect(isCornerHandle('se')).toBe(true);
        expect(isCornerHandle('sw')).toBe(true);

        expect(isCornerHandle('n')).toBe(false);
        expect(isCornerHandle('e')).toBe(false);
        expect(isCornerHandle('s')).toBe(false);
        expect(isCornerHandle('w')).toBe(false);
        expect(isCornerHandle('')).toBe(false);
        expect(isCornerHandle('nope')).toBe(false);
    });

    it('cornerToEdges maps corners to E/W + N/S', () => {
        expect(cornerToEdges('nw')).toEqual({ horizontal: 'w', vertical: 'n' });
        expect(cornerToEdges('ne')).toEqual({ horizontal: 'e', vertical: 'n' });
        expect(cornerToEdges('se')).toEqual({ horizontal: 'e', vertical: 's' });
        expect(cornerToEdges('sw')).toEqual({ horizontal: 'w', vertical: 's' });
    });
});

