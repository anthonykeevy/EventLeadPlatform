import React, { useState, useEffect } from 'react';
import { ChevronDown, FileCheck, ExternalLink, Eye, Building2 } from 'lucide-react';
import { PropertyTextInput } from './inputs';
import { ComponentProps } from '../../types/builder.types';
import { getCompanyTermsAssets } from '../../../dashboard/api/companyAssetsApi';

interface TermsPropertiesSectionProps {
    props: ComponentProps;
    onPropsChange: (updates: Partial<ComponentProps>) => void;
    companyId?: number | null;
}

/**
 * TermsPropertiesSection - Properties specific to Terms & Conditions component
 * 
 * Includes:
 * - Checkbox label (e.g., "I agree to the")
 * - Link text (e.g., "Terms of Service")
 * - Terms URL (for external link)
 * - Terms Content (for modal display)
 * - Preview button
 */
export const TermsPropertiesSection: React.FC<TermsPropertiesSectionProps> = ({
    props,
    onPropsChange,
    companyId,
}) => {
    const [isExpanded, setIsExpanded] = useState(true);
    const [showPreview, setShowPreview] = useState(false);
    const [companyHasTerms, setCompanyHasTerms] = useState(false);
    const [termsCheckLoading, setTermsCheckLoading] = useState(false);

    useEffect(() => {
        if (!companyId || companyId <= 0) {
            setCompanyHasTerms(false);
            return;
        }
        let cancelled = false;
        setTermsCheckLoading(true);
        getCompanyTermsAssets(companyId)
            .then(({ assets }) => {
                if (!cancelled) setCompanyHasTerms((assets?.length ?? 0) > 0);
            })
            .catch(() => { if (!cancelled) setCompanyHasTerms(false); })
            .finally(() => { if (!cancelled) setTermsCheckLoading(false); });
        return () => { cancelled = true; };
    }, [companyId]);

    return (
        <>
            <div className="border-b border-gray-200 dark:border-gray-700">
                {/* Section Header */}
                <button
                    onClick={() => setIsExpanded(!isExpanded)}
                    className="w-full flex items-center justify-between px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
                >
                    <div className="flex items-center gap-2">
                        <FileCheck size={14} className="text-purple-500" />
                        <span>Terms Settings</span>
                    </div>
                    <ChevronDown 
                        size={16} 
                        className={`transform transition-transform ${isExpanded ? 'rotate-180' : ''}`} 
                    />
                </button>

                {/* Section Content */}
                {isExpanded && (
                    <div className="px-4 pb-4 space-y-4">
                        {/* Checkbox Label */}
                        <PropertyTextInput
                            label="Checkbox Label"
                            value={props.label || 'I agree to the'}
                            onChange={(value) => onPropsChange({ label: value })}
                            placeholder="I agree to the"
                            helpText="Text before the link"
                        />

                        {/* Link Text */}
                        <PropertyTextInput
                            label="Link Text"
                            value={props.termsLinkText || 'Terms of Service'}
                            onChange={(value) => onPropsChange({ termsLinkText: value })}
                            placeholder="Terms of Service"
                            helpText="Clickable link text"
                        />

                        {/* Terms Source */}
                        <div className="pt-3 border-t border-gray-100 dark:border-gray-700">
                            <div className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">
                                Terms Source
                            </div>
                            {termsCheckLoading ? (
                                <p className="text-xs text-gray-500 dark:text-gray-400 italic">Checking company settings…</p>
                            ) : companyHasTerms ? (
                                <div className="flex items-start gap-2 p-3 bg-teal-50 dark:bg-teal-900/20 rounded-lg border border-teal-200 dark:border-teal-800">
                                    <Building2 size={16} className="text-teal-600 dark:text-teal-400 mt-0.5 shrink-0" />
                                    <p className="text-sm text-teal-800 dark:text-teal-200">
                                        We will use your company terms
                                    </p>
                                </div>
                            ) : (
                                <>
                                    <p className="text-xs text-gray-500 dark:text-gray-400 mb-3">
                                        Provide either a URL (opens in new tab) or content (opens in modal).
                                        If both are provided, content takes precedence.
                                    </p>

                                    {/* Terms URL */}
                                    <div className="mb-3">
                                        <PropertyTextInput
                                            label="Terms URL"
                                            value={props.termsUrl || ''}
                                            onChange={(value) => onPropsChange({ termsUrl: value })}
                                            placeholder="https://example.com/terms"
                                            helpText="External link to terms page"
                                        />
                                        {props.termsUrl && (
                                            <a
                                                href={props.termsUrl}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="inline-flex items-center gap-1 text-xs text-blue-600 hover:text-blue-800 mt-1"
                                            >
                                                <ExternalLink size={10} />
                                                Open URL
                                            </a>
                                        )}
                                    </div>

                                    {/* Terms Content */}
                                    <div>
                                        <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">
                                            Terms Content (HTML)
                                        </label>
                                        <textarea
                                            value={props.termsContent || ''}
                                            onChange={(e) => onPropsChange({ termsContent: e.target.value })}
                                            placeholder="<h1>Terms of Service</h1><p>Your terms content here...</p>"
                                            className="w-full h-24 px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 
                                                rounded-md bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200
                                                focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none font-mono"
                                        />
                                        <p className="text-[10px] text-gray-400 mt-1">
                                            HTML content displayed in modal when link is clicked
                                        </p>
                                    </div>
                                </>
                            )}
                        </div>

                        {/* Preview Button (only when custom terms content is provided) */}
                        {!companyHasTerms && (props.termsContent || props.termsUrl) && (
                            <button
                                type="button"
                                onClick={() => setShowPreview(true)}
                                className="w-full flex items-center justify-center gap-2 px-4 py-2 
                                    bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 
                                    rounded-md hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                            >
                                <Eye size={14} />
                                Preview Terms
                            </button>
                        )}

                        {/* Component Preview */}
                        <div className="pt-3 border-t border-gray-100 dark:border-gray-700">
                            <div className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">
                                Preview
                            </div>
                            <div className="flex items-start gap-2 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                                <input type="checkbox" disabled className="mt-0.5" />
                                <span className="text-sm text-gray-700 dark:text-gray-300">
                                    {props.label || 'I agree to the'}{' '}
                                    <span className="text-blue-600 underline">
                                        {props.termsLinkText || 'Terms of Service'}
                                    </span>
                                    <span className="text-red-500">*</span>
                                </span>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* Preview Modal */}
            {showPreview && props.termsContent && (
                <div 
                    className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
                    onClick={() => setShowPreview(false)}
                >
                    <div 
                        className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[80vh] flex flex-col"
                        onClick={(e) => e.stopPropagation()}
                    >
                        <div className="flex items-center justify-between px-6 py-4 border-b">
                            <h3 className="text-lg font-semibold text-gray-800">
                                {props.termsLinkText || 'Terms of Service'}
                            </h3>
                            <button
                                onClick={() => setShowPreview(false)}
                                className="text-gray-400 hover:text-gray-600"
                            >
                                ✕
                            </button>
                        </div>
                        <div className="flex-1 overflow-y-auto px-6 py-4">
                            <div 
                                className="prose prose-sm max-w-none"
                                dangerouslySetInnerHTML={{ __html: props.termsContent }}
                            />
                        </div>
                        <div className="px-6 py-4 border-t bg-gray-50 rounded-b-lg">
                            <button
                                onClick={() => setShowPreview(false)}
                                className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg 
                                    hover:bg-blue-700 transition-colors font-medium"
                            >
                                Close
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
};

export default TermsPropertiesSection;

