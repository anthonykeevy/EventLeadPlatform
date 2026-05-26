import React, { createContext, useCallback, useContext, useMemo, useState } from 'react';

interface EdfOverlayContextValue {
  /** True when this component has an open EDF floating surface (dropdown, manual panel, error). */
  isLifted: (componentId: string) => boolean;
  /** Call from EDF runtimes when overlay open state changes. */
  setOverlayOpen: (componentId: string, open: boolean) => void;
}

const EdfOverlayContext = createContext<EdfOverlayContextValue | null>(null);

/** z-index for the field wrapper while its EDF overlay is open (above default artboard siblings). */
export const EDF_FIELD_LIFT_Z_INDEX = 10002;

export const EdfOverlayProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [openIds, setOpenIds] = useState<Set<string>>(() => new Set());

  const setOverlayOpen = useCallback((componentId: string, open: boolean) => {
    setOpenIds((prev) => {
      const has = prev.has(componentId);
      if ((open && has) || (!open && !has)) return prev;
      const next = new Set(prev);
      if (open) next.add(componentId);
      else next.delete(componentId);
      return next;
    });
  }, []);

  const value = useMemo(
    () => ({
      isLifted: (componentId: string) => openIds.has(componentId),
      setOverlayOpen,
    }),
    [openIds, setOverlayOpen],
  );

  return <EdfOverlayContext.Provider value={value}>{children}</EdfOverlayContext.Provider>;
};

export function useEdfOverlayRegister(componentId: string, open: boolean): void {
  const ctx = useContext(EdfOverlayContext);
  React.useEffect(() => {
    if (!ctx) return;
    ctx.setOverlayOpen(componentId, open);
    return () => ctx.setOverlayOpen(componentId, false);
  }, [ctx, componentId, open]);
}

export function useEdfFieldLifted(componentId: string): boolean {
  const ctx = useContext(EdfOverlayContext);
  return ctx?.isLifted(componentId) ?? false;
}
