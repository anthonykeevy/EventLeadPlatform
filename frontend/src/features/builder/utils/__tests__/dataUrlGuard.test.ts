/**
 * Data URL Guard Tests - Story 5.1 Task T07
 */
import { describe, it, expect } from 'vitest';
import {
  isDataUrl,
  stripDataUrlFromBackground,
  DATA_URL_ERROR_MESSAGE,
} from '../dataUrlGuard';

describe('dataUrlGuard', () => {
  describe('isDataUrl', () => {
    it('returns true for data: URLs', () => {
      expect(isDataUrl('data:image/png;base64,abc')).toBe(true);
      expect(isDataUrl('data:image/jpeg;base64,xyz')).toBe(true);
      expect(isDataUrl('DATA:image/png;base64,x')).toBe(true);
      expect(isDataUrl('  data:image/svg+xml,<svg/>')).toBe(true);
    });
    it('returns false for non-Data URLs', () => {
      expect(isDataUrl('https://example.com/image.png')).toBe(false);
      expect(isDataUrl('')).toBe(false);
      expect(isDataUrl(undefined)).toBe(false);
      expect(isDataUrl('/api/assets/1/content')).toBe(false);
    });
  });

  describe('stripDataUrlFromBackground', () => {
    it('removes background when value is Data URL and no asset', () => {
      const result = stripDataUrlFromBackground({
        type: 'image',
        value: 'data:image/png;base64,abc',
      });
      expect(result).toBeUndefined();
    });
    it('clears value but keeps asset when Data URL with asset ref', () => {
      const result = stripDataUrlFromBackground({
        type: 'image',
        value: 'data:image/png;base64,abc',
        asset: { assetId: 'a1', displayName: 'x', originalFilename: 'y.png' },
      });
      expect(result).toBeDefined();
      expect(result!.value).toBe('');
      expect(result!.asset?.assetId).toBe('a1');
    });
    it('returns background unchanged when value is external URL', () => {
      const bg = {
        type: 'image' as const,
        value: 'https://example.com/img.png',
      };
      const result = stripDataUrlFromBackground(bg);
      expect(result).toEqual(bg);
    });
    it('returns undefined for undefined input', () => {
      expect(stripDataUrlFromBackground(undefined)).toBeUndefined();
    });
  });

  describe('DATA_URL_ERROR_MESSAGE', () => {
    it('is a non-empty user-facing string', () => {
      expect(DATA_URL_ERROR_MESSAGE).toBeTruthy();
      expect(DATA_URL_ERROR_MESSAGE.length).toBeGreaterThan(20);
      expect(DATA_URL_ERROR_MESSAGE).toContain('Data URL');
    });
  });
});
