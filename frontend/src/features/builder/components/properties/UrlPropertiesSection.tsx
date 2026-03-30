import React from 'react';
import { ChevronDown, Link as LinkIcon } from 'lucide-react';
import { PropertyTextInput } from './inputs';
import { ComponentProps } from '../../types/builder.types';

interface UrlPropertiesSectionProps {
    props: ComponentProps;
    onPropsChange: (updates: Partial<ComponentProps>) => void;
}

export const UrlPropertiesSection: React.FC<UrlPropertiesSectionProps> = ({ props, onPropsChange }) => {
    const [isExpanded, setIsExpanded] = React.useState(true);
    const migratedLegacyPatternRef = React.useRef(false);

    React.useEffect(() => {
        if (migratedLegacyPatternRef.current) return;
        const legacyPattern = props.urlPattern?.trim();
        if (!legacyPattern || props.validation?.pattern) return;

        migratedLegacyPatternRef.current = true;
        onPropsChange({
            validation: {
                ...props.validation,
                pattern: legacyPattern,
            },
            urlPattern: undefined,
        });
    }, [props.urlPattern, props.validation, onPropsChange]);

    return (
        <div className="border-b border-gray-200 dark:border-gray-700">
            <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="w-full flex items-center justify-between px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
            >
                <div className="flex items-center gap-2">
                    <LinkIcon size={14} className="text-blue-500" />
                    <span>URL Settings</span>
                </div>
                <ChevronDown
                    size={16}
                    className={`transform transition-transform ${isExpanded ? 'rotate-180' : ''}`}
                />
            </button>

            {isExpanded && (
                <div className="px-4 pb-4 space-y-3">
                    <PropertyTextInput
                        label="URL Prefix"
                        value={props.urlPrefix || ''}
                        onChange={(value) => onPropsChange({ urlPrefix: value || undefined })}
                        placeholder="https://"
                        helpText="Fixed text shown inside the input before user entry."
                    />
                </div>
            )}
        </div>
    );
};
