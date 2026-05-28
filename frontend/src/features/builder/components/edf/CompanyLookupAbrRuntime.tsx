import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import type { RuntimeComponentProps } from '../../registry/ComponentRegistry';
import {
  displayTextFromFieldValue,
  searchCompanyAbr,
  type CompanyAbrResolvedValue,
  type CompanySearchResponse,
} from '../../api/externalFeedApi';
import type { CompanySearchResult } from '../../../companies/api/companiesApi';
import { computeFieldStyles } from '../../utils/styleUtils';
import { DEFAULT_GLOBAL_STYLES } from '../../types/builder.types';
import { useDebouncedLookup } from '../../hooks/useDebouncedLookup';
import { EdfLookupResultsPanel } from './EdfLookupResultsPanel';
import { CompactCompanyLookupResults } from './CompactCompanyLookupResults';
import { EdfAnchorPortal } from './EdfAnchorPortal';
import { useEdfOverlayRegister } from './EdfOverlayContext';
import { buildManualCompanyValue, CompanyManualEntryPanel } from './CompanyManualEntryPanel';
import { isInactiveAbnStatus } from './abnStatusUtils';

function toResolvedValue(result: CompanySearchResult): CompanyAbrResolvedValue {
  const abnDisplay = result.abnFormatted || result.abn;
  const displayText = abnDisplay
    ? `${result.companyName} (${abnDisplay})`
    : result.companyName;

  return {
    displayText,
    validationSource: 'abr',
    legalEntityName: result.companyName,
    abn: result.abn,
    acn: result.acn,
    entityType: result.entityType,
    abnStatus: result.status,
    gstRegistered: result.gstRegistered,
    matchType: result.matchType ?? 'abr',
  };
}

const MANUAL_FALLBACK_LABEL = "Can't find your company? Enter details manually →";

function initialInputText(resolved: CompanyAbrResolvedValue | null, value: unknown): string {
  if (resolved?.displayText) return resolved.displayText;
  return displayTextFromFieldValue(value);
}

export const CompanyLookupAbrRuntime: React.FC<RuntimeComponentProps> = ({
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
  const skipAutoSelectRef = useRef(false);
  const skipExternalSyncRef = useRef(false);

  const resolved = useMemo((): CompanyAbrResolvedValue | null => {
    if (value && typeof value === 'object' && 'displayText' in (value as object)) {
      return value as CompanyAbrResolvedValue;
    }
    return null;
  }, [value]);

  const allowManualFallback = component.props.allowManualFallback !== false;
  const requireAbnWhenManual = Boolean(component.props.requireAbnWhenManual);
  const requireAbn = Boolean(component.props.requireAbn);
  const allowTradingAs = component.props.allowTradingAs !== false;
  const showBusinessNames = component.props.showBusinessNamesInResults !== false;
  const warnOnInactiveAbn = component.props.warnOnInactiveAbn !== false;
  const tradingAsLabel =
    (component.props.tradingAsLabel as string | undefined) || 'Trading as (optional)';

  const [inputText, setInputText] = useState(() => initialInputText(resolved, value));
  const [manualMode, setManualMode] = useState(false);
  const [manualLegalName, setManualLegalName] = useState('');
  const [manualAbn, setManualAbn] = useState('');
  const [manualTradingAs, setManualTradingAs] = useState('');

  const fetcher = useCallback(async (query: string) => searchCompanyAbr(query, 10), []);

  const { search, data, isLoading, error: searchError, clear } =
    useDebouncedLookup<CompanySearchResponse>({
      fetcher,
      debounceMs: 300,
      minQueryLength: 2,
    });

  const autoSelect = component.props.autoSelectSingleResult !== false;
  const manualAbnRequired = requireAbnWhenManual || requireAbn;

  const draftManualValue = useMemo(
    () => buildManualCompanyValue({ legalEntityName: manualLegalName, abn: manualAbn, tradingAs: manualTradingAs }),
    [manualLegalName, manualAbn, manualTradingAs],
  );

  const canConfirmManual =
    !!draftManualValue &&
    (!manualAbnRequired || (manualAbn.replace(/\D/g, '').length === 11));

  const publishManualValue = useCallback(
    (legalEntityName: string, abn: string, tradingAs: string) => {
      const abnDigits = abn.replace(/\D/g, '');
      skipExternalSyncRef.current = true;

      if (manualAbnRequired && abnDigits.length !== 11) {
        onChange(undefined);
        return;
      }

      onChange(buildManualCompanyValue({ legalEntityName, abn, tradingAs }) ?? undefined);
    },
    [manualAbnRequired, onChange],
  );

  const handleManualLegalNameChange = useCallback(
    (next: string) => {
      setManualLegalName(next);
      publishManualValue(next, manualAbn, manualTradingAs);
    },
    [manualAbn, manualTradingAs, publishManualValue],
  );

  const handleManualAbnChange = useCallback(
    (next: string) => {
      setManualAbn(next);
      publishManualValue(manualLegalName, next, manualTradingAs);
    },
    [manualLegalName, manualTradingAs, publishManualValue],
  );

  const handleManualTradingAsChange = useCallback(
    (next: string) => {
      setManualTradingAs(next);
      publishManualValue(manualLegalName, manualAbn, next);
    },
    [manualAbn, manualLegalName, publishManualValue],
  );

  const commitManualEntry = useCallback(() => {
    if (!canConfirmManual || !draftManualValue) return false;
    setManualMode(false);
    clear();
    skipExternalSyncRef.current = true;
    onChange(draftManualValue);
    setInputText(draftManualValue.displayText);
    return true;
  }, [canConfirmManual, clear, draftManualValue, onChange]);

  const enterManualMode = useCallback(
    (seedName?: string) => {
      if (!allowManualFallback) return;
      const fromResolved =
        resolved?.validationSource === 'manual'
          ? {
              legal: resolved.legalEntityName ?? '',
              abn: resolved.abn ?? '',
              trading: resolved.tradingAs ?? '',
            }
          : null;
      const seed = (seedName ?? inputText).trim();
      setManualLegalName(fromResolved?.legal || seed);
      setManualAbn(fromResolved?.abn || '');
      setManualTradingAs(fromResolved?.trading || '');
      setManualMode(true);
      clear();
      publishManualValue(
        fromResolved?.legal || seed,
        fromResolved?.abn || '',
        fromResolved?.trading || '',
      );
    },
    [allowManualFallback, clear, inputText, publishManualValue, resolved],
  );

  const exitManualMode = useCallback(() => {
    if (commitManualEntry()) return;
    setManualMode(false);
    setManualLegalName('');
    setManualAbn('');
    setManualTradingAs('');
    skipExternalSyncRef.current = true;
    onChange(undefined);
    setInputText('');
    clear();
  }, [clear, commitManualEntry, onChange]);

  useEffect(() => {
    if (skipExternalSyncRef.current) {
      skipExternalSyncRef.current = false;
      return;
    }

    if (!value && !resolved) {
      skipAutoSelectRef.current = true;
      clear();
      setManualMode(false);
      setManualLegalName('');
      setManualAbn('');
      setManualTradingAs('');
      setInputText('');
      return;
    }

    if (manualMode) {
      if (resolved?.validationSource === 'manual') {
        setManualLegalName(resolved.legalEntityName ?? '');
        setManualAbn(resolved.abn ?? '');
        setManualTradingAs(resolved.tradingAs ?? '');
      }
      return;
    }

    setInputText(initialInputText(resolved, value));
  }, [value, resolved, clear, manualMode]);

  useEffect(() => {
    if (skipAutoSelectRef.current) {
      skipAutoSelectRef.current = false;
      return;
    }
    if (manualMode) return;
    if (resolved?.legalEntityName) return;
    if (
      autoSelect &&
      data &&
      data.results.length === 1 &&
      !disabled &&
      inputText.trim().length >= 2
    ) {
      const picked = toResolvedValue(data.results[0]);
      onChange(picked);
      setInputText(picked.displayText);
    }
  }, [
    autoSelect,
    data,
    disabled,
    inputText,
    manualMode,
    onChange,
    resolved?.legalEntityName,
  ]);

  const fieldStyles = computeFieldStyles(
    globalStyles ?? DEFAULT_GLOBAL_STYLES,
    styleOverrides,
    component.props.componentScale ?? 100,
  );

  const fieldLabelStyle: React.CSSProperties = {
    ...fieldStyles.labelStyle,
    display: 'block',
    marginBottom: 0,
  };

  const panelStyle: React.CSSProperties = {
    fontFamily: fieldStyles.computed.fontFamily,
    fontSize: fieldStyles.computed.helpTextFontSize,
    color: fieldStyles.computed.textColor,
  };

  const resultRowStyle: React.CSSProperties = {
    fontFamily: fieldStyles.computed.fontFamily,
    fontSize: fieldStyles.computed.fontSize,
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const next = e.target.value;
    setInputText(next);
    search(next);
    if (!next.trim()) onChange(undefined);
  };

  const handleSelect = (result: CompanySearchResult) => {
    const picked = toResolvedValue(result);
    onChange(picked);
    setInputText(picked.displayText);
  };

  const hasActiveSelection =
    !manualMode &&
    !!resolved &&
    !!resolved.displayText &&
    inputText.trim() === (resolved.displayText ?? '').trim();

  const hasSearchFinished = data !== null || !!searchError;
  const showResults =
    !disabled &&
    !manualMode &&
    !hasActiveSelection &&
    inputText.trim().length >= 2 &&
    (isLoading || !!searchError || hasSearchFinished);

  const manualFallbackAction = allowManualFallback
    ? { label: MANUAL_FALLBACK_LABEL, onActivate: () => enterManualMode(inputText) }
    : undefined;

  const label = component.props.label || 'Company';
  const placeholder = component.props.placeholder || 'Search by ABN, ACN, or name…';
  const displayError = error;
  const accent = primaryColor || fieldStyles.computed.primaryColor;

  const showInactiveWarning =
    warnOnInactiveAbn &&
    !manualMode &&
    resolved?.validationSource === 'abr' &&
    isInactiveAbnStatus(resolved.abnStatus);

  const showManualCommittedHint =
    !manualMode && resolved?.validationSource === 'manual' && hasActiveSelection;

  useEdfOverlayRegister(component.id, showResults || manualMode);

  const resultsPanel = showResults ? (
    <EdfLookupResultsPanel
      isLoading={isLoading}
      error={searchError}
      showEmpty={!isLoading && !searchError && !!data && data.results.length === 0}
      emptyMessage={`No companies found for "${inputText.trim()}". Check ABN/ACN or try the company legal name.`}
      manualFallback={manualFallbackAction}
      resultCountLabel={
        data && data.results.length > 0
          ? `${data.results.length} ${data.results.length === 1 ? 'company' : 'companies'}`
          : undefined
      }
    >
      {data && data.results.length > 0 && (
        <CompactCompanyLookupResults
          results={data.results}
          onSelect={handleSelect}
          showBusinessNames={showBusinessNames}
          showStatusBadge={warnOnInactiveAbn}
          resultStyle={resultRowStyle}
        />
      )}
    </EdfLookupResultsPanel>
  ) : null;

  return (
    <div style={fieldStyles.containerStyle} className="w-full">
      <div ref={anchorRef} className="relative w-full">
      <label style={fieldStyles.labelStyle}>
        {label}
        {required && <span className="text-red-500 ml-0.5">*</span>}
      </label>

      <div className="relative w-full">
        {manualMode ? (
          <p style={{ ...fieldStyles.helpTextStyle, margin: 0 }}>
            Manual entry open — fill in below, then choose &ldquo;Use this company&rdquo;.
          </p>
        ) : (
          <>
            <input
              ref={inputRef as React.RefObject<HTMLInputElement>}
              type="text"
              value={inputText}
              onChange={handleInputChange}
              disabled={disabled}
              placeholder={placeholder}
              tabIndex={tabIndex}
              autoComplete="off"
              className="w-full"
              style={fieldStyles.inputStyle}
              aria-invalid={!!displayError}
              aria-describedby={displayError ? `${component.id}-error` : undefined}
            />
            {showManualCommittedHint && (
              <p style={{ ...fieldStyles.helpTextStyle, margin: 0, marginTop: 4 }}>
                Manual company entry (not ABR verified).
                {allowManualFallback && (
                  <>
                    {' '}
                    <button
                      type="button"
                      onClick={() => enterManualMode()}
                      disabled={disabled}
                      style={{
                        ...fieldStyles.helpTextStyle,
                        margin: 0,
                        padding: 0,
                        background: 'none',
                        border: 'none',
                        cursor: disabled ? 'not-allowed' : 'pointer',
                        textDecoration: 'underline',
                      }}
                    >
                      Edit
                    </button>
                  </>
                )}
              </p>
            )}
            {allowManualFallback && !hasActiveSelection && inputText.trim().length < 2 && (
              <button
                type="button"
                onClick={() => enterManualMode()}
                disabled={disabled}
                style={{
                  ...fieldStyles.helpTextStyle,
                  marginTop: fieldStyles.helpTextStyle.marginTop,
                  background: 'none',
                  border: 'none',
                  padding: 0,
                  cursor: disabled ? 'not-allowed' : 'pointer',
                  textAlign: 'left',
                  textDecoration: 'underline',
                }}
              >
                {MANUAL_FALLBACK_LABEL}
              </button>
            )}
          </>
        )}
      </div>
      </div>

      <EdfAnchorPortal open={showResults} anchorRef={anchorRef} minWidth={240} contentScale={artboardScale}>
        {resultsPanel}
      </EdfAnchorPortal>

      <EdfAnchorPortal open={manualMode} anchorRef={anchorRef} contentScale={artboardScale}>
        <CompanyManualEntryPanel
          legalEntityName={manualLegalName}
          abn={manualAbn}
          tradingAs={manualTradingAs}
          requireAbn={manualAbnRequired}
          allowTradingAs={allowTradingAs}
          tradingAsLabel={tradingAsLabel}
          canConfirm={canConfirmManual}
          disabled={disabled}
          onLegalEntityNameChange={handleManualLegalNameChange}
          onAbnChange={handleManualAbnChange}
          onTradingAsChange={handleManualTradingAsChange}
          onConfirm={commitManualEntry}
          onBackToSearch={exitManualMode}
          panelStyle={panelStyle}
          helpTextStyle={fieldStyles.helpTextStyle}
          fieldLabelStyle={fieldLabelStyle}
          inputStyle={fieldStyles.inputStyle}
          primaryColor={accent}
        />
      </EdfAnchorPortal>

      {showInactiveWarning && (
        <p
          className="rounded border border-amber-200 bg-amber-50 px-2 py-1 text-amber-900 dark:border-amber-800 dark:bg-amber-900/20 dark:text-amber-100"
          style={{ ...fieldStyles.helpTextStyle, marginTop: 4 }}
          role="status"
        >
          This ABN is <strong>{resolved?.abnStatus}</strong> on the Australian Business Register.
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
