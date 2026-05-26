import React from 'react';
import type { CompanySearchResult } from '../../../companies/api/companiesApi';
import { abnStatusPresentation } from './abnStatusUtils';
import { EDF_LOOKUP_RESULT_ROW_CLASS } from './edfLookupStyles';

interface CompactCompanyLookupResultsProps {
  results: CompanySearchResult[];
  onSelect: (result: CompanySearchResult) => void;
  showBusinessNames?: boolean;
  showStatusBadge?: boolean;
  resultStyle?: React.CSSProperties;
}

function formatPrimaryLine(result: CompanySearchResult): string {
  const name = (result.companyName || '').trim() || 'Unknown company';
  const abn = (result.abnFormatted || result.abn || '').trim();
  return abn ? `${name} (${abn})` : name;
}

function businessSubtitle(result: CompanySearchResult, showBusinessNames: boolean): string | null {
  if (!showBusinessNames) return null;
  const matched = (result.matchedName || '').trim();
  if (matched && matched !== result.companyName) {
    return `Trading as: ${matched}`;
  }
  const names = result.businessNames?.filter(Boolean) ?? [];
  const extra = names.find((n) => n.trim() && n.trim() !== result.companyName);
  return extra ? `Also known as: ${extra}` : null;
}

export const CompactCompanyLookupResults: React.FC<CompactCompanyLookupResultsProps> = ({
  results,
  onSelect,
  showBusinessNames = true,
  showStatusBadge = true,
  resultStyle,
}) => {
  return (
    <>
      {results.map((result, index) => {
        const primary = formatPrimaryLine(result);
        const subtitle = businessSubtitle(result, showBusinessNames);
        const statusBadge = showStatusBadge ? abnStatusPresentation(result.status) : null;

        return (
          <button
            key={`${result.abn ?? 'na'}-${index}`}
            type="button"
            onClick={() => onSelect(result)}
            className={EDF_LOOKUP_RESULT_ROW_CLASS}
            style={resultStyle}
            title={primary}
          >
            <div className="flex items-start justify-between gap-2 min-w-0">
              <span className="truncate">{primary}</span>
              {statusBadge ? (
                <span className={`shrink-0 ${statusBadge.className}`}>{statusBadge.label}</span>
              ) : null}
            </div>
            {subtitle ? (
              <div
                className="truncate opacity-75 mt-0.5"
                style={{
                  fontSize: resultStyle?.fontSize
                    ? `calc(${typeof resultStyle.fontSize === 'number' ? `${resultStyle.fontSize}px` : resultStyle.fontSize} * 0.92)`
                    : undefined,
                }}
              >
                {subtitle}
              </div>
            ) : null}
          </button>
        );
      })}
    </>
  );
};
