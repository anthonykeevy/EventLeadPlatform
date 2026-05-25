import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Loader2 } from 'lucide-react';
import type { RuntimeComponentProps } from '../../registry/ComponentRegistry';
import {
  displayTextFromFieldValue,
  resolveAddressAu,
  searchAddressAu,
  type AddressAuResolvedValue,
  type AddressAuSuggestion,
} from '../../api/externalFeedApi';
import { computeFieldStyles } from '../../utils/styleUtils';
import { DEFAULT_GLOBAL_STYLES } from '../../types/builder.types';
import { useDebouncedLookup } from '../../hooks/useDebouncedLookup';
import { EdfLookupResultsPanel } from './EdfLookupResultsPanel';
import { EdfAnchorPortal } from './EdfAnchorPortal';

export const AddressLookupAuRuntime: React.FC<RuntimeComponentProps> = ({
  component,
  value,
  onChange,
  disabled,
  required,
  error,
  tabIndex,
  primaryColor,
  inputRef,
  styleOverrides,
  globalStyles,
  artboardScale = 1,
}) => {
  const anchorRef = useRef<HTMLDivElement>(null);

  const resolved = useMemo((): AddressAuResolvedValue | null => {
    if (value && typeof value === 'object' && 'displayText' in (value as object)) {
      return value as AddressAuResolvedValue;
    }
    return null;
  }, [value]);

  const [inputText, setInputText] = useState(() =>
    resolved?.displayText ?? displayTextFromFieldValue(value)
  );
  const [resolvingId, setResolvingId] = useState<string | null>(null);

  const fetcher = useCallback(
    async (query: string) => searchAddressAu(query, 8),
    []
  );

  const { search, data, isLoading, error: searchError, clear } = useDebouncedLookup({
    fetcher,
    debounceMs: 350,
    minQueryLength: 2,
  });

  // Keep visible text in sync when parent clears value (e.g. submit-and-reset / kiosk reset).
  useEffect(() => {
    const externalText = resolved?.displayText ?? displayTextFromFieldValue(value);
    setInputText(externalText);
    if (!externalText && !resolved) {
      clear();
      setResolvingId(null);
    }
  }, [value, resolved, clear]);

  const fieldStyles = computeFieldStyles(
    globalStyles ?? DEFAULT_GLOBAL_STYLES,
    styleOverrides,
    component.props.componentScale ?? 100
  );

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const next = e.target.value;
    setInputText(next);
    search(next);
    if (!next.trim()) onChange(undefined);
  };

  const handleSelect = async (item: AddressAuSuggestion) => {
    const selectedLabel = item.label.trim();
    if (!item.id) {
      onChange({
        displayText: selectedLabel,
        psmaAddressId: null,
        validationSource: 'manual',
      } satisfies AddressAuResolvedValue);
      setInputText(selectedLabel);
      return;
    }
    setInputText(selectedLabel);
    setResolvingId(item.id);
    try {
      const payload = await resolveAddressAu(item.id, selectedLabel);
      onChange(payload);
      setInputText(payload.displayText || selectedLabel);
    } catch {
      onChange({
        displayText: selectedLabel,
        psmaAddressId: item.id,
        validationSource: 'geoscape',
        resolvedFields: { formattedAddress: selectedLabel, psmaAddressId: item.id },
      } satisfies AddressAuResolvedValue);
      setInputText(selectedLabel);
    } finally {
      setResolvingId(null);
    }
  };

  const suggestions = data?.items ?? [];
  const hasActiveSelection =
    !!resolved?.psmaAddressId &&
    inputText.trim() === (resolved.displayText ?? '').trim();
  const showResults =
    !disabled &&
    !hasActiveSelection &&
    inputText.trim().length >= 2 &&
    (isLoading || !!searchError || suggestions.length > 0);

  const label = component.props.label || 'Address';
  const placeholder = component.props.placeholder || 'Start typing your address…';
  const displayError = error;

  const resultsPanel = showResults ? (
    <EdfLookupResultsPanel
      isLoading={isLoading}
      error={searchError}
      showEmpty={!isLoading && !searchError && suggestions.length === 0}
      emptyMessage="No addresses found. Try a different search or use manual entry if enabled."
      resultCountLabel={
        suggestions.length > 0 ? `${suggestions.length} addresses` : undefined
      }
    >
      {suggestions.map((item) => (
        <button
          key={`${item.id}-${item.label}`}
          type="button"
          disabled={disabled || !!resolvingId}
          onClick={() => handleSelect(item)}
          className="w-full text-left px-3 py-2 text-sm leading-snug border-b border-gray-100 dark:border-gray-800 last:border-0 hover:bg-teal-50 dark:hover:bg-teal-900/20 focus:outline-none focus:bg-teal-50 dark:focus:bg-teal-900/20 truncate"
          title={item.label}
        >
          {item.label}
        </button>
      ))}
    </EdfLookupResultsPanel>
  ) : null;

  return (
    <div style={fieldStyles.containerStyle} className="w-full">
      <label style={fieldStyles.labelStyle}>
        {label}
        {required && <span className="text-red-500 ml-0.5">*</span>}
      </label>
      <div ref={anchorRef} className="relative">
        <input
          ref={inputRef as React.RefObject<HTMLInputElement>}
          type="text"
          value={inputText}
          onChange={handleInputChange}
          disabled={disabled || !!resolvingId}
          placeholder={placeholder}
          tabIndex={tabIndex}
          autoComplete="off"
          className="w-full"
          style={{
            ...fieldStyles.inputStyle,
            ...(primaryColor
              ? ({ ['--tw-ring-color' as string]: primaryColor } as React.CSSProperties)
              : {}),
          }}
          aria-invalid={!!displayError}
          aria-describedby={displayError ? `${component.id}-error` : undefined}
        />
        {resolvingId && (
          <Loader2 className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 animate-spin text-gray-400 pointer-events-none" />
        )}
      </div>

      <EdfAnchorPortal open={showResults} anchorRef={anchorRef} contentScale={artboardScale}>
        {resultsPanel}
      </EdfAnchorPortal>

      {resolved?.resolvedFields?.formattedAddress && resolved.psmaAddressId && (
        <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Validated address selected
        </p>
      )}

      {displayError && (
        <p id={`${component.id}-error`} style={fieldStyles.errorTextStyle} role="alert">
          {displayError}
        </p>
      )}
    </div>
  );
};
