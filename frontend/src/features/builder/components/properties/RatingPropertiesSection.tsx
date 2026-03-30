import React from 'react';
import { ChevronDown, Star } from 'lucide-react';
import { PropertyNumberInput, PropertySelect, PropertyTextInput } from './inputs';
import { ComponentProps } from '../../types/builder.types';

interface RatingPropertiesSectionProps {
    props: ComponentProps;
    onPropsChange: (updates: Partial<ComponentProps>) => void;
}

const RATING_STYLE_OPTIONS = [
    { value: 'stars', label: 'Stars' },
    { value: 'numbers', label: 'Numbers' },
    { value: 'emoji', label: 'Emoji' },
];

export const RatingPropertiesSection: React.FC<RatingPropertiesSectionProps> = ({ props, onPropsChange }) => {
    const [isExpanded, setIsExpanded] = React.useState(true);
    const ratingLabels = props.ratingLabels || {};

    return (
        <div className="border-b border-gray-200 dark:border-gray-700">
            <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="w-full flex items-center justify-between px-4 py-3 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
            >
                <div className="flex items-center gap-2">
                    <Star size={14} className="text-amber-500" />
                    <span>Rating Settings</span>
                </div>
                <ChevronDown
                    size={16}
                    className={`transform transition-transform ${isExpanded ? 'rotate-180' : ''}`}
                />
            </button>

            {isExpanded && (
                <div className="px-4 pb-4 space-y-3">
                    <PropertyNumberInput
                        label="Maximum Rating"
                        value={props.ratingMax || 5}
                        min={1}
                        max={10}
                        step={1}
                        onChange={(value) => onPropsChange({ ratingMax: value })}
                        helpText="Set the highest selectable rating value."
                    />
                    <PropertySelect
                        label="Rating Style"
                        value={props.ratingStyle || 'stars'}
                        onChange={(value) => onPropsChange({ ratingStyle: value as ComponentProps['ratingStyle'] })}
                        options={RATING_STYLE_OPTIONS}
                        helpText="Choose how rating options are rendered."
                    />
                    <PropertyTextInput
                        label="Low Label"
                        value={ratingLabels.low || ''}
                        onChange={(value) =>
                            onPropsChange({
                                ratingLabels: {
                                    ...ratingLabels,
                                    low: value || undefined,
                                },
                            })
                        }
                        placeholder="Not likely"
                    />
                    <PropertyTextInput
                        label="High Label"
                        value={ratingLabels.high || ''}
                        onChange={(value) =>
                            onPropsChange({
                                ratingLabels: {
                                    ...ratingLabels,
                                    high: value || undefined,
                                },
                            })
                        }
                        placeholder="Very likely"
                    />
                </div>
            )}
        </div>
    );
};
