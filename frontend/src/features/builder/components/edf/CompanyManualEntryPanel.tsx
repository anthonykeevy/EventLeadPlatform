import React from 'react';

import type { CompanyAbrResolvedValue } from '../../api/externalFeedApi';



function formatAbnDisplay(abn: string): string {

  const digits = abn.replace(/\D/g, '');

  if (digits.length !== 11) return abn.trim();

  return `${digits.slice(0, 2)} ${digits.slice(2, 5)} ${digits.slice(5, 8)} ${digits.slice(8, 11)}`;

}



export function buildManualCompanyValue(params: {

  legalEntityName: string;

  abn?: string;

  tradingAs?: string;

}): CompanyAbrResolvedValue | undefined {

  const legalEntityName = params.legalEntityName.trim();

  if (!legalEntityName) return undefined;



  const abnDigits = params.abn?.replace(/\D/g, '') ?? '';

  const abn = abnDigits.length > 0 ? abnDigits : null;

  const tradingAs = params.tradingAs?.trim() || null;

  const abnDisplay = abn ? formatAbnDisplay(abn) : null;

  const displayText = abnDisplay ? `${legalEntityName} (${abnDisplay})` : legalEntityName;



  return {

    displayText,

    validationSource: 'manual',

    legalEntityName,

    abn,

    matchType: 'manual',

    tradingAs,

  };

}



interface CompanyManualEntryPanelProps {

  legalEntityName: string;

  abn: string;

  tradingAs: string;

  requireAbn: boolean;

  allowTradingAs: boolean;

  tradingAsLabel: string;

  canConfirm: boolean;

  disabled?: boolean;

  onLegalEntityNameChange: (value: string) => void;

  onAbnChange: (value: string) => void;

  onTradingAsChange: (value: string) => void;

  onConfirm: () => void;

  onBackToSearch: () => void;

  panelStyle?: React.CSSProperties;

  helpTextStyle?: React.CSSProperties;

  fieldLabelStyle: React.CSSProperties;

  inputStyle: React.CSSProperties;

  primaryColor?: string;

}



export const CompanyManualEntryPanel: React.FC<CompanyManualEntryPanelProps> = ({

  legalEntityName,

  abn,

  tradingAs,

  requireAbn,

  allowTradingAs,

  tradingAsLabel,

  canConfirm,

  disabled,

  onLegalEntityNameChange,

  onAbnChange,

  onTradingAsChange,

  onConfirm,

  onBackToSearch,

  panelStyle,

  helpTextStyle,

  fieldLabelStyle,

  inputStyle,

  primaryColor,

}) => {

  const gapPx =

    typeof helpTextStyle?.marginTop === 'string'

      ? parseInt(helpTextStyle.marginTop, 10) || 4

      : 4;



  const linkStyle: React.CSSProperties = {

    ...helpTextStyle,

    margin: 0,

    background: 'none',

    border: 'none',

    padding: 0,

    cursor: disabled ? 'not-allowed' : 'pointer',

    textAlign: 'left',

    opacity: disabled ? 0.6 : 1,

    textDecoration: 'underline',

  };



  const confirmStyle: React.CSSProperties = {

    ...inputStyle,

    height: 'auto',

    minHeight: inputStyle.height,

    paddingTop: inputStyle.paddingTop,

    paddingBottom: inputStyle.paddingBottom,

    cursor: disabled || !canConfirm ? 'not-allowed' : 'pointer',

    opacity: disabled || !canConfirm ? 0.55 : 1,

    backgroundColor: primaryColor || '#0d9488',

    color: '#fff',

    borderColor: primaryColor || '#0d9488',

    fontWeight: 500,

  };



  const fieldBlockStyle: React.CSSProperties = {

    display: 'flex',

    flexDirection: 'column',

    gap: Math.max(2, Math.round(gapPx * 0.5)),

  };



  return (

    <div

      style={{

        ...panelStyle,

        boxSizing: 'border-box',

        display: 'flex',

        flexDirection: 'column',

        gap: gapPx,

        padding: gapPx,

        borderRadius: inputStyle.borderRadius,

        borderWidth: inputStyle.borderWidth ?? 1,

        borderStyle: 'solid',

        borderColor: inputStyle.borderColor ?? '#e5e7eb',

        backgroundColor: '#fff',

        boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',

      }}

    >

      <p style={{ ...helpTextStyle, margin: 0 }}>

        Enter details manually (not verified against ABR). Use &ldquo;Use this company&rdquo; when

        done.

      </p>



      <div style={fieldBlockStyle}>

        <label style={fieldLabelStyle}>

          Legal entity name

          <span style={{ color: '#ef4444', marginLeft: 2 }}>*</span>

        </label>

        <input

          type="text"

          value={legalEntityName}

          onChange={(e) => onLegalEntityNameChange(e.target.value)}

          disabled={disabled}

          autoComplete="organization"

          style={inputStyle}

          placeholder="Registered company name"

        />

      </div>



      <div style={fieldBlockStyle}>

        <label style={fieldLabelStyle}>

          ABN

          {requireAbn && <span style={{ color: '#ef4444', marginLeft: 2 }}>*</span>}

        </label>

        <input

          type="text"

          inputMode="numeric"

          value={abn}

          onChange={(e) => onAbnChange(e.target.value)}

          disabled={disabled}

          autoComplete="off"

          style={inputStyle}

          placeholder={requireAbn ? '11-digit ABN' : 'Optional — 11-digit ABN'}

        />

      </div>



      {allowTradingAs && (

        <div style={fieldBlockStyle}>

          <label style={fieldLabelStyle}>{tradingAsLabel}</label>

          <input

            type="text"

            value={tradingAs}

            onChange={(e) => onTradingAsChange(e.target.value)}

            disabled={disabled}

            autoComplete="off"

            style={inputStyle}

          />

        </div>

      )}



      <div style={{ display: 'flex', flexDirection: 'column', gap: gapPx, paddingTop: Math.round(gapPx * 0.25) }}>

        <button type="button" onClick={onConfirm} disabled={disabled || !canConfirm} style={confirmStyle}>

          Use this company

        </button>

        <button type="button" onClick={onBackToSearch} disabled={disabled} style={linkStyle}>

          Back to ABR search

        </button>

      </div>

    </div>

  );

};


