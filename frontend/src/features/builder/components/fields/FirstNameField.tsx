import React from 'react';
import { AlertCircle, User } from 'lucide-react';
import { SmartBorder } from '../ui/SmartBorder';

interface FirstNameFieldProps {
  // Drag props passed from dnd-kit
  dragListeners?: any;
  dragAttributes?: any;
  setNodeRef?: (node: HTMLElement | null) => void;
}

export const FirstNameField: React.FC<FirstNameFieldProps> = ({ dragListeners, dragAttributes, setNodeRef }) => {
  // Validation Messages
  const validationMessages = [
      "We only accept names less than 30 Characters",
      "Numbers and Special characters are not allowed"
  ];

  const longestMessage = validationMessages.reduce((a, b) => a.length > b.length ? a : b);

  return (
    <div ref={setNodeRef ? (node) => setNodeRef(node as any) : undefined} style={{display: 'inline-block'}}> 
      {/* We wrap in a div to receive the setNodeRef so dnd-kit knows what element moves 
          BUT we don't attach listeners here. We pass them to SmartBorder. */}
      
      <SmartBorder padding={5} dragListeners={dragListeners} dragAttributes={dragAttributes}>
        
        {/* 1. Label Area */}
        <div className="mb-1 pr-2 w-max">
          <label className="block text-sm font-medium text-slate-900 dark:text-gray-200 whitespace-nowrap">
            First Name <span className="text-red-500">*</span>
          </label>
        </div>

        {/* 2. Input Area */}
        <div className="relative rounded-md shadow-sm w-80">
          <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
            <User className="h-4 w-4 text-gray-400" aria-hidden="true" />
          </div>
          <input
            type="text"
            name="first-name"
            className="block w-full rounded-md border border-gray-300 dark:border-gray-600 pl-10 py-2 text-sm text-slate-900 dark:text-gray-200 bg-white dark:bg-gray-800 focus:border-teal-500 focus:outline-none placeholder-gray-400 dark:placeholder-gray-500"
            placeholder="Enter your first name"
            disabled
            readOnly
          />
        </div>

        {/* 3. Validation Area */}
        <div className="mt-1 w-max max-w-[320px]">
          <div className="flex items-start text-xs text-gray-500 dark:text-gray-400 opacity-70">
              <AlertCircle size={14} className="mr-1 mt-0.5 flex-shrink-0" />
              <span>{longestMessage}</span>
          </div>
        </div>

      </SmartBorder>
    </div>
  );
};
