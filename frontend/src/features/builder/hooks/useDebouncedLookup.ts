import { useCallback, useEffect, useRef, useState } from 'react';

interface UseDebouncedLookupOptions<T> {
  debounceMs?: number;
  minQueryLength?: number;
  fetcher: (query: string) => Promise<T>;
}

export function useDebouncedLookup<T>({
  debounceMs = 300,
  minQueryLength = 2,
  fetcher,
}: UseDebouncedLookupOptions<T>) {
  const [query, setQuery] = useState('');
  const [data, setData] = useState<T | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const requestIdRef = useRef(0);

  const search = useCallback((value: string) => {
    setQuery(value);
  }, []);

  const clear = useCallback(() => {
    setQuery('');
    setData(null);
    setError(null);
    setIsLoading(false);
  }, []);

  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current);

    if (query.trim().length < minQueryLength) {
      setData(null);
      setError(null);
      setIsLoading(false);
      return;
    }

    debounceRef.current = setTimeout(async () => {
      const requestId = ++requestIdRef.current;
      setIsLoading(true);
      setError(null);
      try {
        const result = await fetcher(query.trim());
        if (requestId !== requestIdRef.current) return;
        setData(result);
      } catch (err) {
        if (requestId !== requestIdRef.current) return;
        const message =
          err instanceof Error
            ? err.message
            : typeof err === 'object' && err !== null && 'message' in err
              ? String((err as { message: unknown }).message)
              : 'Search failed';
        setError(message);
        setData(null);
      } finally {
        if (requestId === requestIdRef.current) setIsLoading(false);
      }
    }, debounceMs);

    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current);
    };
  }, [query, debounceMs, minQueryLength, fetcher]);

  return { query, search, data, isLoading, error, clear };
}
