import React, { useState } from 'react';
import { FileCheck, ExternalLink, X } from 'lucide-react';
import { ComputedFieldStyles } from '../../utils/styleUtils';

interface TermsFieldProps {
    label?: string;
    termsLinkText?: string;
    termsUrl?: string;
    termsContent?: string;
    termsDisplayMode?: 'popup' | 'new_tab';
    termsDisplayWidth?: number;
    termsDisplayHeight?: number;
    required?: boolean;
    fieldStyles?: ComputedFieldStyles;
}

/**
 * Terms & Conditions Field Component
 * 
 * Displays a checkbox with a clickable link to view terms.
 * - If termsUrl is provided, link opens in new tab
 * - If termsContent is provided, opens modal with content
 * - If both provided, modal takes precedence
 */
export const TermsField: React.FC<TermsFieldProps> = ({
    label = 'I agree to the',
    termsLinkText = 'Terms of Service',
    termsUrl,
    termsContent,
    termsDisplayMode = 'popup',
    termsDisplayWidth = 720,
    termsDisplayHeight = 600,
    required = true,
    fieldStyles,
}) => {
    const [showModal, setShowModal] = useState(false);

    const handleLinkClick = (e: React.MouseEvent) => {
        e.preventDefault();
        e.stopPropagation();
        
        if (termsContent) {
            setShowModal(true);
        } else if (termsUrl) {
            if (termsDisplayMode === 'new_tab') {
                const parsedUrl = new URL(termsUrl, window.location.origin);
                parsedUrl.searchParams.set('viewer', 'inline');
                window.open(parsedUrl.toString(), '_blank', 'noopener,noreferrer');
            } else {
                setShowModal(true);
            }
        }
    };

    const labelStyle = fieldStyles?.labelStyle || {};
    const helpTextStyle = fieldStyles?.helpTextStyle || {};

    return (
        <>
            <div
                className="border border-dashed border-gray-300 rounded-lg p-3 bg-white hover:border-blue-400 
                    transition-colors group relative"
            >
                {/* Drag Handle */}
                <div className="absolute -left-1 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <FileCheck size={14} className="text-gray-400" />
                </div>

                {/* Terms Checkbox */}
                <div className="flex items-start gap-3">
                    <div className="flex items-center h-5 mt-0.5">
                        <input
                            type="checkbox"
                            disabled
                            className="w-4 h-4 border-2 border-gray-300 rounded text-blue-500 
                                focus:ring-blue-500 cursor-not-allowed"
                        />
                    </div>
                    <div className="flex-1">
                        <label 
                            className="text-sm text-gray-700"
                            style={labelStyle}
                        >
                            {label}{' '}
                            <button
                                type="button"
                                onClick={handleLinkClick}
                                className="text-blue-600 hover:text-blue-800 underline inline-flex items-center gap-1"
                            >
                                {termsLinkText}
                                <ExternalLink size={12} />
                            </button>
                            {required && <span className="text-red-500 ml-0.5">*</span>}
                        </label>
                        
                        {/* Help text / validation message */}
                        <p 
                            className="text-xs mt-1 flex items-center gap-1"
                            style={{
                                ...helpTextStyle,
                                color: '#DC2626', // Error color for required
                            }}
                        >
                            <FileCheck size={10} />
                            Required to proceed
                        </p>
                    </div>
                </div>

                {/* Preview badge */}
                <div className="absolute top-1 right-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <span className="text-[9px] bg-purple-100 text-purple-600 px-1.5 py-0.5 rounded font-medium">
                        TERMS
                    </span>
                </div>
            </div>

            {/* Terms Modal */}
            {showModal && (termsContent || termsUrl) && (
                <div 
                    className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
                    onClick={() => setShowModal(false)}
                >
                    <div 
                        className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[80vh] flex flex-col"
                        onClick={(e) => e.stopPropagation()}
                        style={{
                            maxWidth: termsUrl && !termsContent ? termsDisplayWidth : undefined,
                            height: termsUrl && !termsContent ? termsDisplayHeight : undefined
                        }}
                    >
                        {/* Modal Header */}
                        <div className="flex items-center justify-between px-6 py-4 border-b">
                            <h3 className="text-lg font-semibold text-gray-800">
                                {termsLinkText}
                            </h3>
                            <button
                                onClick={() => setShowModal(false)}
                                className="p-1 hover:bg-gray-100 rounded-full transition-colors"
                            >
                                <X size={20} className="text-gray-500" />
                            </button>
                        </div>
                        
                        {/* Modal Content */}
                        <div className="flex-1 overflow-hidden flex flex-col min-h-0">
                            {termsContent ? (
                                <div className="flex-1 overflow-y-auto px-6 py-4">
                                    <div 
                                        className="prose prose-sm max-w-none"
                                        dangerouslySetInnerHTML={{ __html: termsContent }}
                                    />
                                </div>
                            ) : (
                                <iframe 
                                    src={termsUrl + (termsUrl.includes('?') ? '&' : '?') + 'viewer=inline'} 
                                    className="w-full h-full min-h-[300px] border-0"
                                    title={termsLinkText}
                                />
                            )}
                        </div>
                        
                        {/* Modal Footer */}
                        <div className="px-6 py-4 border-t bg-gray-50 rounded-b-lg flex-shrink-0">
                            <button
                                onClick={() => setShowModal(false)}
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

export default TermsField;

