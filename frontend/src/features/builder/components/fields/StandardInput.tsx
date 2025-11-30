import React from 'react';
import { AlertCircle, LucideIcon } from 'lucide-react';
import { SmartBorder } from '../ui/SmartBorder';

interface StandardInputProps {
  label: string;
  icon?: LucideIcon | React.ReactNode;
  placeholder?: string;
  validationMessage?: string;
  required?: boolean;
  type?: 'text' | 'number' | 'email' | 'textarea' | 'select' | 'date'; // etc
  options?: { label: string; value: string }[]; // For select/radio
  // Drag props
  dragListeners?: any;
  dragAttributes?: any;
  setNodeRef?: (node: HTMLElement | null) => void;
}

export const StandardInput: React.FC<StandardInputProps> = ({ 
    label, 
    icon: Icon, 
    placeholder = "Input text...", 
    validationMessage = "Validation error message", 
    required = false,
    type = 'text',
    options,
    dragListeners,
    dragAttributes,
    setNodeRef
}) => {

  return (
    <div ref={setNodeRef ? (node) => setNodeRef(node as any) : undefined} style={{display: 'inline-block'}}> 
      <SmartBorder padding={5} dragListeners={dragListeners} dragAttributes={dragAttributes}>
        
        {/* 1. Label Area */}
        <div className="mb-1 pr-2 w-max">
          <label className="block text-sm font-medium text-slate-900 dark:text-gray-200 whitespace-nowrap flex items-center gap-2">
            {label}
            {required && <span className="text-red-500">*</span>}
          </label>
        </div>

        {/* 2. Input Area */}
        <div className="relative rounded-md shadow-sm w-80">
            {renderInputControl(type, placeholder, Icon, options)}
        </div>

        {/* 3. Validation Area */}
        <div className="mt-1 w-max max-w-[320px]">
          <div className="flex items-start text-xs text-gray-500 dark:text-gray-400 opacity-70">
              <AlertCircle size={14} className="mr-1 mt-0.5 flex-shrink-0" />
              <span>{validationMessage}</span>
          </div>
        </div>

      </SmartBorder>
    </div>
  );
};

// Helper to render different input types while keeping the "Gold Standard" look
const renderInputControl = (
    type: string, 
    placeholder: string, 
    Icon: any, 
    options?: { label: string; value: string }[]
) => {
    const baseInputClass = "block w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm text-slate-900 dark:text-gray-200 focus:border-teal-500 focus:outline-none placeholder-gray-400 dark:placeholder-gray-500";
    
    // Handle Icon rendering safely
    const iconElement = Icon && (React.isValidElement(Icon) ? Icon : <Icon className="h-4 w-4 text-gray-400" />);

    if (type === 'textarea') {
        return (
            <div className="relative">
                {iconElement && <div className="absolute top-3 left-3 pointer-events-none">{iconElement}</div>}
                <textarea
                    className={`${baseInputClass} py-2 ${iconElement ? 'pl-10' : 'pl-3'} h-20 resize-none`}
                    placeholder={placeholder}
                    readOnly
                    disabled
                />
            </div>
        );
    }

    if (type === 'select') {
        return (
            <div className="relative">
                {iconElement && <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">{iconElement}</div>}
                <div className={`${baseInputClass} py-2 ${iconElement ? 'pl-10' : 'pl-3'} flex justify-between items-center pr-3`}>
                    <span>{placeholder}</span>
                    <span className="text-gray-500">▼</span>
                </div>
            </div>
        );
    }

    // Default Text/Number/Date
    return (
        <div className="relative">
            {iconElement && <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">{iconElement}</div>}
            <input
                type={type === 'number' ? 'text' : type} // Use text for number preview to avoid spinners
                className={`${baseInputClass} py-2 ${iconElement ? 'pl-10' : 'pl-3'}`}
                placeholder={placeholder}
                readOnly
                disabled
            />
        </div>
    );
};
