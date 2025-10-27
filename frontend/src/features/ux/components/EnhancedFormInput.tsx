import React, { useState, useRef, forwardRef } from 'react';
import { Eye, EyeOff, X, Check } from 'lucide-react';

export interface EnhancedFormInputProps {
  type?: 'text' | 'email' | 'password' | 'tel' | 'url' | 'search' | 'textarea';
  label: string;
  name: string;
  value: string;
  onChange: (value: string) => void;
  onBlur?: () => void;
  placeholder?: string;
  error?: string;
  success?: boolean;
  disabled?: boolean;
  required?: boolean;
  autoComplete?: string;
  maxLength?: number;
  showCharacterCount?: boolean;
  showPasswordToggle?: boolean;
  showClearButton?: boolean;
  floatingLabel?: boolean;
  className?: string;
  inputClassName?: string;
  'aria-describedby'?: string;
}

export const EnhancedFormInput = forwardRef<HTMLInputElement | HTMLTextAreaElement, EnhancedFormInputProps>(
  ({
    type = 'text',
    label,
    name,
    value,
    onChange,
    onBlur,
    placeholder,
    error,
    success = false,
    disabled = false,
    required = false,
    autoComplete,
    maxLength,
    showCharacterCount = false,
    showPasswordToggle = false,
    showClearButton = false,
    floatingLabel = true,
    className = '',
    inputClassName = '',
    'aria-describedby': ariaDescribedby,
  }, ref) => {
    const [isFocused, setIsFocused] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const inputRef = useRef<HTMLInputElement | HTMLTextAreaElement>(null);

    const isTextArea = type === 'textarea';
    const isPassword = type === 'password';
    const hasValue = value.length > 0;
    const shouldFloatLabel = floatingLabel && (isFocused || hasValue);
    const currentType = isPassword && showPassword ? 'text' : type;

    const handleFocus = () => {
      setIsFocused(true);
    };

    const handleBlur = () => {
      setIsFocused(false);
      onBlur?.();
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
      onChange(e.target.value);
    };

    const handleClear = () => {
      onChange('');
      if (inputRef.current) {
        inputRef.current.focus();
      }
    };

    const togglePasswordVisibility = () => {
      setShowPassword(!showPassword);
    };

    const getInputId = () => `input-${name}`;
    const getErrorId = () => `error-${name}`;
    const getHelpId = () => `help-${name}`;

    const inputClasses = `
      w-full px-3 py-2 border rounded-md transition-all duration-200 ease-in-out
      focus:outline-none focus:ring-2 focus:ring-offset-0
      disabled:bg-gray-50 disabled:text-gray-500 disabled:cursor-not-allowed
      ${error
        ? 'border-red-300 focus:border-red-500 focus:ring-red-500'
        : success
        ? 'border-green-300 focus:border-green-500 focus:ring-green-500'
        : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'
      }
      ${floatingLabel ? 'pt-6 pb-2' : ''}
      ${inputClassName}
    `.trim();

    const labelClasses = `
      absolute left-3 transition-all duration-200 ease-in-out pointer-events-none
      ${shouldFloatLabel
        ? 'top-1 text-xs text-gray-500'
        : 'top-2 text-sm text-gray-700'
      }
      ${error ? 'text-red-600' : success ? 'text-green-600' : ''}
    `.trim();

    const InputComponent = isTextArea ? 'textarea' : 'input';

    return (
      <div className={`relative ${className}`}>
        <div className="relative">
          <InputComponent
            ref={(node: any) => {
              if (ref) {
                if (typeof ref === 'function') {
                  ref(node);
                } else if (ref && 'current' in ref) {
                  (ref as any).current = node;
                }
              }
              if (inputRef) {
                (inputRef as any).current = node;
              }
            }}
            type={currentType}
            id={getInputId()}
            name={name}
            value={value}
            onChange={handleChange}
            onFocus={handleFocus}
            onBlur={handleBlur}
            placeholder={floatingLabel ? '' : placeholder}
            disabled={disabled}
            required={required}
            autoComplete={autoComplete}
            maxLength={maxLength}
            className={inputClasses}
            aria-invalid={error ? 'true' : 'false'}
            aria-describedby={[
              error ? getErrorId() : '',
              showCharacterCount ? getHelpId() : '',
              ariaDescribedby || '',
            ].filter(Boolean).join(' ') || undefined}
          />

          {floatingLabel && (
            <label
              htmlFor={getInputId()}
              className={labelClasses}
            >
              {label}
              {required && <span className="text-red-500 ml-1">*</span>}
            </label>
          )}

          {!floatingLabel && (
            <label
              htmlFor={getInputId()}
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              {label}
              {required && <span className="text-red-500 ml-1">*</span>}
            </label>
          )}

          {/* Action buttons */}
          <div className="absolute right-3 top-1/2 transform -translate-y-1/2 flex items-center space-x-1">
            {isPassword && showPasswordToggle && (
              <button
                type="button"
                onClick={togglePasswordVisibility}
                className="p-1 text-gray-400 hover:text-gray-600 focus:outline-none focus:text-gray-600"
                aria-label={showPassword ? 'Hide password' : 'Show password'}
                tabIndex={-1}
              >
                {showPassword ? (
                  <EyeOff className="h-4 w-4" />
                ) : (
                  <Eye className="h-4 w-4" />
                )}
              </button>
            )}

            {showClearButton && hasValue && !disabled && (
              <button
                type="button"
                onClick={handleClear}
                className="p-1 text-gray-400 hover:text-gray-600 focus:outline-none focus:text-gray-600"
                aria-label="Clear input"
                tabIndex={-1}
              >
                <X className="h-4 w-4" />
              </button>
            )}

            {success && (
              <Check className="h-4 w-4 text-green-500" aria-hidden="true" />
            )}
          </div>
        </div>

        {/* Error message */}
        {error && (
          <p
            id={getErrorId()}
            className="mt-1 text-sm text-red-600"
            role="alert"
            aria-live="polite"
          >
            {error}
          </p>
        )}

        {/* Character count */}
        {showCharacterCount && maxLength && (
          <p
            id={getHelpId()}
            className="mt-1 text-sm text-gray-500"
          >
            {value.length}/{maxLength} characters
          </p>
        )}

        {/* Success message */}
        {success && !error && (
          <p className="mt-1 text-sm text-green-600">
            Looks good!
          </p>
        )}
      </div>
    );
  }
);

EnhancedFormInput.displayName = 'EnhancedFormInput';

export default EnhancedFormInput;
