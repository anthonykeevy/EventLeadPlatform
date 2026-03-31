import React from 'react';
import { ChevronDown, Paperclip } from 'lucide-react';
import { PropertyTextInput } from './inputs';
import { ComponentProps } from '../../types/builder.types';

interface FileUploadPropertiesSectionProps {
    props: ComponentProps;
    onPropsChange: (updates: Partial<ComponentProps>) => void;
}

export const FileUploadPropertiesSection: React.FC<FileUploadPropertiesSectionProps> = ({
    props,
    onPropsChange,
}) => {
    const [isExpanded, setIsExpanded] = React.useState(true);

    return (
        <div className="border-b border-gray-200 dark:border-gray-700">
            <button
                type="button"
                onClick={() => setIsExpanded(!isExpanded)}
                className="w-full flex items-center justify-between px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
            >
                <div className="flex items-center gap-2">
                    <Paperclip size={14} className="text-teal-500" />
                    <span>File upload</span>
                </div>
                <ChevronDown
                    size={16}
                    className={`transform transition-transform ${isExpanded ? 'rotate-180' : ''}`}
                />
            </button>

            {isExpanded && (
                <div className="px-4 pb-4 space-y-3">
                    <div className="space-y-1">
                        <PropertyTextInput
                            label="Allowed file types"
                            value={props.accept || ''}
                            onChange={(value) => onPropsChange({ accept: value || undefined })}
                            placeholder="Leave empty for any type, or e.g. .pdf, .png"
                            helpText={undefined}
                        />
                        <p className="text-xs text-gray-500 dark:text-gray-400 leading-relaxed">
                            <strong className="font-medium text-gray-600 dark:text-gray-300">
                                Leave blank
                            </strong>{' '}
                            if visitors may upload any file type (the max size below still applies).
                        </p>
                        <p className="text-xs text-gray-500 dark:text-gray-400 leading-relaxed">
                            To limit types, use a comma-separated list. Examples:{' '}
                            <span className="font-mono text-gray-600 dark:text-gray-300">.pdf</span> for PDFs only;{' '}
                            <span className="font-mono text-gray-600 dark:text-gray-300">.pdf, .png</span> for those
                            two; <span className="font-mono text-gray-600 dark:text-gray-300">image/*</span> for any
                            image.
                        </p>
                    </div>
                    <label className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
                        <input
                            type="checkbox"
                            checked={Boolean(props.allowMultiple)}
                            onChange={(e) =>
                                onPropsChange({
                                    allowMultiple: e.target.checked,
                                    maxFiles: e.target.checked ? props.maxFiles ?? 3 : undefined,
                                })
                            }
                        />
                        Allow multiple files
                    </label>
                    {props.allowMultiple && (
                        <PropertyTextInput
                            label="Max files"
                            value={String(props.maxFiles ?? 3)}
                            onChange={(value) => {
                                const n = parseInt(value, 10);
                                onPropsChange({
                                    maxFiles: Number.isFinite(n) && n > 0 ? n : 3,
                                });
                            }}
                        />
                    )}
                    <PropertyTextInput
                        label="Max size (MB)"
                        value={
                            props.maxFileSizeMb != null
                                ? String(props.maxFileSizeMb)
                                : props.maxFileSizeBytes
                                  ? String(Math.round(props.maxFileSizeBytes / (1024 * 1024)))
                                  : '10'
                        }
                        onChange={(value) => {
                            const n = parseFloat(value);
                            if (!Number.isFinite(n) || n <= 0) {
                                onPropsChange({ maxFileSizeMb: 10, maxFileSizeBytes: undefined });
                                return;
                            }
                            onPropsChange({
                                maxFileSizeMb: n,
                                maxFileSizeBytes: Math.round(n * 1024 * 1024),
                            });
                        }}
                        helpText="Enforced on upload. Default 10 MB."
                    />
                </div>
            )}
        </div>
    );
};
