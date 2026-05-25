import React from 'react';
import { ChevronDown, Globe, AlertTriangle } from 'lucide-react';
import { PropertyTextInput, PropertyToggle } from './inputs';
import { ComponentProps } from '../../types/builder.types';

type ExternalFeedVariant = 'address-lookup-au' | 'company-lookup-abr';

interface ExternalFeedPropertiesSectionProps {
    variant: ExternalFeedVariant;
    props: ComponentProps;
    onPropsChange: (updates: Partial<ComponentProps>) => void;
}

const ADDRESS_OUTPUT_FIELDS = [
    { key: 'line1', label: 'Line 1' },
    { key: 'line2', label: 'Line 2' },
    { key: 'suburb', label: 'Suburb' },
    { key: 'state', label: 'State' },
    { key: 'postcode', label: 'Postcode' },
] as const;

const COMPANY_OUTPUT_FIELDS = [
    { key: 'legalEntityName', label: 'Legal entity name' },
    { key: 'abn', label: 'ABN' },
    { key: 'acn', label: 'ACN' },
    { key: 'entityType', label: 'Entity type' },
    { key: 'abnStatus', label: 'ABN status' },
    { key: 'gstRegistered', label: 'GST registered' },
] as const;

export const ExternalFeedPropertiesSection: React.FC<ExternalFeedPropertiesSectionProps> = ({
    variant,
    props,
    onPropsChange,
}) => {
    const [isExpanded, setIsExpanded] = React.useState(true);
    const isAddress = variant === 'address-lookup-au';
    const title = isAddress ? 'Address lookup (AU / GeoScape)' : 'Company lookup (ABR)';
    const providerHelp = isAddress
        ? 'Requires internet at the event. Respondents search AU addresses via GeoScape/PSMA (platform proxy).'
        : 'Requires internet at the event. Respondents search companies via ABR (platform proxy).';

    const requireValidated = Boolean(props.requireValidatedAddress);
    const allowManual = props.allowManualFallback !== false;
    const allowDelivery = Boolean(props.allowDeliveryInstructions);
    const blockInactive = Boolean(props.blockOnInactiveAbn);

    const enabledFields = (props.enabledOutputFields as string[] | undefined) ?? [];
    const toggleOutputField = (key: string, checked: boolean) => {
        const next = checked
            ? [...new Set([...enabledFields, key])]
            : enabledFields.filter((f) => f !== key);
        onPropsChange({ enabledOutputFields: next.length ? next : undefined });
    };

    return (
        <div className="border-b border-gray-200 dark:border-gray-700">
            <button
                type="button"
                onClick={() => setIsExpanded(!isExpanded)}
                className="w-full flex items-center justify-between px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
            >
                <div className="flex items-center gap-2">
                    <Globe size={14} className="text-sky-500" />
                    <span>{title}</span>
                </div>
                <ChevronDown
                    size={16}
                    className={`transform transition-transform ${isExpanded ? 'rotate-180' : ''}`}
                />
            </button>

            {isExpanded && (
                <div className="px-4 pb-4 space-y-3">
                    <p className="text-xs text-gray-500 dark:text-gray-400 leading-relaxed">{providerHelp}</p>

                    <PropertyToggle
                        label="Allow manual entry fallback"
                        checked={allowManual}
                        onChange={(checked) => onPropsChange({ allowManualFallback: checked })}
                        helpText={
                            isAddress
                                ? 'Show “Can’t find your address?” manual fields when lookup fails.'
                                : 'Show “Can’t find your company?” manual entry when ABR search fails.'
                        }
                    />

                    {isAddress ? (
                        <>
                            <PropertyToggle
                                label="Require validated address (PSMA)"
                                checked={requireValidated}
                                onChange={(checked) =>
                                    onPropsChange({
                                        requireValidatedAddress: checked || undefined,
                                        ...(checked ? { allowManualFallback: false } : {}),
                                    })
                                }
                                helpText="Submit blocked unless a PSMA suggestion was selected."
                            />
                            {requireValidated && allowManual && (
                                <div className="flex items-start gap-2 text-xs text-amber-700 dark:text-amber-300 bg-amber-50 dark:bg-amber-900/20 rounded p-2">
                                    <AlertTriangle size={12} className="mt-0.5 shrink-0" />
                                    <span>
                                        Strict mode: manual fallback was turned off because validated-only
                                        conflicts with manual entry.
                                    </span>
                                </div>
                            )}
                            <PropertyToggle
                                label="Allow editing after autocomplete"
                                checked={props.editableAfterResolve !== false}
                                onChange={(checked) =>
                                    onPropsChange({ editableAfterResolve: checked || undefined })
                                }
                            />
                            <PropertyToggle
                                label="Show unit / address line 2"
                                checked={props.showUnitField !== false}
                                onChange={(checked) => onPropsChange({ showUnitField: checked || undefined })}
                            />
                            <PropertyToggle
                                label="Show delivery instructions field"
                                checked={allowDelivery}
                                onChange={(checked) =>
                                    onPropsChange({
                                        allowDeliveryInstructions: checked || undefined,
                                        ...(checked ? {} : { requireDeliveryInstructions: undefined }),
                                    })
                                }
                            />
                            {allowDelivery && (
                                <>
                                    <PropertyToggle
                                        label="Require delivery instructions"
                                        checked={Boolean(props.requireDeliveryInstructions)}
                                        onChange={(checked) =>
                                            onPropsChange({
                                                requireDeliveryInstructions: checked || undefined,
                                            })
                                        }
                                    />
                                    <PropertyTextInput
                                        label="Delivery instructions label"
                                        value={(props.deliveryInstructionsLabel as string) || 'Delivery instructions'}
                                        onChange={(value) =>
                                            onPropsChange({
                                                deliveryInstructionsLabel: value || undefined,
                                            })
                                        }
                                    />
                                    <PropertyTextInput
                                        label="Export name for instructions"
                                        value={
                                            (props.deliveryInstructionsExportName as string) ||
                                            `${props.exportName || 'address'}_instructions`
                                        }
                                        onChange={(value) =>
                                            onPropsChange({
                                                deliveryInstructionsExportName: value || undefined,
                                            })
                                        }
                                    />
                                </>
                            )}
                            {allowManual && (
                                <PropertyToggle
                                    label="Show PO Box / parcel locker hint"
                                    checked={props.showPoBoxHelperText !== false}
                                    onChange={(checked) =>
                                        onPropsChange({ showPoBoxHelperText: checked || undefined })
                                    }
                                />
                            )}
                            <PropertyTextInput
                                label="Concatenation template"
                                value={(props.concatenationTemplate as string) || ''}
                                onChange={(value) =>
                                    onPropsChange({ concatenationTemplate: value || undefined })
                                }
                                placeholder="{{line1}}, {{suburb}} {{state}} {{postcode}}"
                                helpText="Used when delivery mode is single concatenated export."
                            />
                        </>
                    ) : (
                        <>
                            <PropertyToggle
                                label="Require ABN on submission"
                                checked={Boolean(props.requireAbn)}
                                onChange={(checked) => onPropsChange({ requireAbn: checked || undefined })}
                            />
                            {allowManual && (
                                <PropertyToggle
                                    label="Require ABN when entering manually"
                                    checked={Boolean(props.requireAbnWhenManual)}
                                    onChange={(checked) =>
                                        onPropsChange({ requireAbnWhenManual: checked || undefined })
                                    }
                                />
                            )}
                            <PropertyToggle
                                label="Auto-select single search result"
                                checked={props.autoSelectSingleResult !== false}
                                onChange={(checked) =>
                                    onPropsChange({ autoSelectSingleResult: checked || undefined })
                                }
                            />
                            <PropertyToggle
                                label="Show “Trading as” field"
                                checked={props.allowTradingAs !== false}
                                onChange={(checked) =>
                                    onPropsChange({
                                        allowTradingAs: checked || undefined,
                                        ...(checked ? {} : { tradingAsLabel: undefined }),
                                    })
                                }
                            />
                            {props.allowTradingAs !== false && (
                                <>
                                    <PropertyTextInput
                                        label="Trading as label"
                                        value={(props.tradingAsLabel as string) || 'Trading as (optional)'}
                                        onChange={(value) =>
                                            onPropsChange({ tradingAsLabel: value || undefined })
                                        }
                                    />
                                    <PropertyTextInput
                                        label="Export name for trading as"
                                        value={
                                            (props.tradingAsExportName as string) ||
                                            `${props.exportName || 'company'}_tradingAs`
                                        }
                                        onChange={(value) =>
                                            onPropsChange({ tradingAsExportName: value || undefined })
                                        }
                                    />
                                </>
                            )}
                            <PropertyToggle
                                label="Show business names in results"
                                checked={props.showBusinessNamesInResults !== false}
                                onChange={(checked) =>
                                    onPropsChange({ showBusinessNamesInResults: checked || undefined })
                                }
                            />
                            <PropertyToggle
                                label="Allow editing legal name after lookup"
                                checked={Boolean(props.editableLegalNameAfterResolve)}
                                onChange={(checked) =>
                                    onPropsChange({
                                        editableLegalNameAfterResolve: checked || undefined,
                                    })
                                }
                            />
                            <PropertyToggle
                                label="Warn when ABN is not Active"
                                checked={props.warnOnInactiveAbn !== false}
                                onChange={(checked) =>
                                    onPropsChange({ warnOnInactiveAbn: checked || undefined })
                                }
                            />
                            <PropertyToggle
                                label="Block submission for inactive ABN"
                                checked={blockInactive}
                                onChange={(checked) =>
                                    onPropsChange({ blockOnInactiveAbn: checked || undefined })
                                }
                            />
                            {blockInactive && allowManual && (
                                <div className="flex items-start gap-2 text-xs text-amber-700 dark:text-amber-300 bg-amber-50 dark:bg-amber-900/20 rounded p-2">
                                    <AlertTriangle size={12} className="mt-0.5 shrink-0" />
                                    <span>
                                        Manual fallback lets respondents bypass ABN status checks.
                                    </span>
                                </div>
                            )}
                        </>
                    )}

                    <div className="space-y-2 pt-1 border-t border-gray-100 dark:border-gray-800">
                        <span className="text-xs font-medium text-gray-600 dark:text-gray-400">
                            Delivery mode
                        </span>
                        <select
                            value={(props.deliveryMode as string) || 'decomposed'}
                            onChange={(e) =>
                                onPropsChange({
                                    deliveryMode: e.target.value as 'decomposed' | 'concatenated',
                                })
                            }
                            className="w-full px-2 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800"
                        >
                            <option value="decomposed">Decomposed (separate export columns)</option>
                            <option value="concatenated">Concatenated (single field)</option>
                        </select>
                    </div>

                    <div className="space-y-2">
                        <span className="text-xs font-medium text-gray-600 dark:text-gray-400">
                            Enabled output fields
                        </span>
                        <div className="space-y-1">
                            {(isAddress ? ADDRESS_OUTPUT_FIELDS : COMPANY_OUTPUT_FIELDS).map((field) => (
                                <label
                                    key={field.key}
                                    className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300"
                                >
                                    <input
                                        type="checkbox"
                                        checked={enabledFields.includes(field.key)}
                                        onChange={(e) => toggleOutputField(field.key, e.target.checked)}
                                    />
                                    {field.label}
                                </label>
                            ))}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};
