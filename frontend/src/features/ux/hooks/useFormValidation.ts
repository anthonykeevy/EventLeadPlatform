import { useState, useCallback, useMemo, useEffect } from 'react';

export interface ValidationRule {
  required?: boolean;
  minLength?: number;
  maxLength?: number;
  pattern?: RegExp;
  email?: boolean;
  url?: boolean;
  phone?: boolean;
  custom?: (value: string) => string | null;
}

export interface ValidationRules {
  [key: string]: ValidationRule;
}

export interface ValidationErrors {
  [key: string]: string | null;
}

export interface UseFormValidationOptions {
  rules: ValidationRules;
  debounceMs?: number;
  validateOnChange?: boolean;
  validateOnBlur?: boolean;
}

export interface UseFormValidationReturn {
  errors: ValidationErrors;
  isValid: boolean;
  validateField: (field: string, value: string) => string | null;
  validateForm: (values: Record<string, string>) => ValidationErrors;
  clearError: (field: string) => void;
  clearAllErrors: () => void;
  setError: (field: string, error: string) => void;
}

// Built-in validators
const validators = {
  required: (value: string): string | null => {
    if (!value || value.trim().length === 0) {
      return 'This field is required';
    }
    return null;
  },

  minLength: (value: string, min: number): string | null => {
    if (value.length < min) {
      return `Must be at least ${min} characters`;
    }
    return null;
  },

  maxLength: (value: string, max: number): string | null => {
    if (value.length > max) {
      return `Must be no more than ${max} characters`;
    }
    return null;
  },

  pattern: (value: string, pattern: RegExp): string | null => {
    if (!pattern.test(value)) {
      return 'Invalid format';
    }
    return null;
  },

  email: (value: string): string | null => {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (value && !emailPattern.test(value)) {
      return 'Please enter a valid email address';
    }
    return null;
  },

  url: (value: string): string | null => {
    try {
      if (value) {
        new URL(value);
      }
      return null;
    } catch {
      return 'Please enter a valid URL';
    }
  },

  phone: (value: string): string | null => {
    const phonePattern = /^[\+]?[1-9][\d]{0,15}$/;
    if (value && !phonePattern.test(value.replace(/[\s\-\(\)]/g, ''))) {
      return 'Please enter a valid phone number';
    }
    return null;
  },
};

export const useFormValidation = ({
  rules,
  debounceMs = 300,
  validateOnChange = true,
  validateOnBlur = true,
}: UseFormValidationOptions): UseFormValidationReturn => {
  const [errors, setErrors] = useState<ValidationErrors>({});

  const validateField = useCallback((field: string, value: string): string | null => {
    const rule = rules[field];
    if (!rule) return null;

    // Required validation
    if (rule.required) {
      const requiredError = validators.required(value);
      if (requiredError) return requiredError;
    }

    // Skip other validations if value is empty and not required
    if (!value && !rule.required) return null;

    // Min length validation
    if (rule.minLength !== undefined) {
      const minLengthError = validators.minLength(value, rule.minLength);
      if (minLengthError) return minLengthError;
    }

    // Max length validation
    if (rule.maxLength !== undefined) {
      const maxLengthError = validators.maxLength(value, rule.maxLength);
      if (maxLengthError) return maxLengthError;
    }

    // Pattern validation
    if (rule.pattern) {
      const patternError = validators.pattern(value, rule.pattern);
      if (patternError) return patternError;
    }

    // Email validation
    if (rule.email) {
      const emailError = validators.email(value);
      if (emailError) return emailError;
    }

    // URL validation
    if (rule.url) {
      const urlError = validators.url(value);
      if (urlError) return urlError;
    }

    // Phone validation
    if (rule.phone) {
      const phoneError = validators.phone(value);
      if (phoneError) return phoneError;
    }

    // Custom validation
    if (rule.custom) {
      return rule.custom(value);
    }

    return null;
  }, [rules]);

  const validateForm = useCallback((values: Record<string, string>): ValidationErrors => {
    const newErrors: ValidationErrors = {};
    
    Object.keys(rules).forEach(field => {
      const error = validateField(field, values[field] || '');
      if (error) {
        newErrors[field] = error;
      }
    });

    return newErrors;
  }, [rules, validateField]);

  const debouncedValidateField = useMemo(() => {
    let timeoutId: NodeJS.Timeout;
    
    return (field: string, value: string) => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => {
        const error = validateField(field, value);
        setErrors(prev => ({
          ...prev,
          [field]: error,
        }));
      }, debounceMs);
    };
  }, [validateField, debounceMs]);

  const clearError = useCallback((field: string) => {
    setErrors(prev => {
      const newErrors = { ...prev };
      delete newErrors[field];
      return newErrors;
    });
  }, []);

  const clearAllErrors = useCallback(() => {
    setErrors({});
  }, []);

  const setError = useCallback((field: string, error: string) => {
    setErrors(prev => ({
      ...prev,
      [field]: error,
    }));
  }, []);

  const isValid = useMemo(() => {
    return Object.values(errors).every(error => error === null);
  }, [errors]);

  return {
    errors,
    isValid,
    validateField,
    validateForm,
    clearError,
    clearAllErrors,
    setError,
  };
};

// Hook for real-time validation with debouncing
export const useFieldValidation = (
  field: string,
  value: string,
  rules: ValidationRules,
  options: { debounceMs?: number; validateOnChange?: boolean; validateOnBlur?: boolean } = {}
) => {
  const { debounceMs = 300, validateOnChange = true, validateOnBlur = true } = options;
  const [error, setError] = useState<string | null>(null);
  const [isValidating, setIsValidating] = useState(false);

  const validate = useCallback((val: string) => {
    setIsValidating(true);
    const rule = rules[field];
    if (!rule) {
      setError(null);
      setIsValidating(false);
      return;
    }

    // Required validation
    if (rule.required) {
      const requiredError = validators.required(val);
      if (requiredError) {
        setError(requiredError);
        setIsValidating(false);
        return;
      }
    }

    // Skip other validations if value is empty and not required
    if (!val && !rule.required) {
      setError(null);
      setIsValidating(false);
      return;
    }

    // Run other validations
    let fieldError: string | null = null;

    if (rule.minLength !== undefined) {
      fieldError = validators.minLength(val, rule.minLength);
      if (fieldError) {
        setError(fieldError);
        setIsValidating(false);
        return;
      }
    }

    if (rule.maxLength !== undefined) {
      fieldError = validators.maxLength(val, rule.maxLength);
      if (fieldError) {
        setError(fieldError);
        setIsValidating(false);
        return;
      }
    }

    if (rule.pattern) {
      fieldError = validators.pattern(val, rule.pattern);
      if (fieldError) {
        setError(fieldError);
        setIsValidating(false);
        return;
      }
    }

    if (rule.email) {
      fieldError = validators.email(val);
      if (fieldError) {
        setError(fieldError);
        setIsValidating(false);
        return;
      }
    }

    if (rule.url) {
      fieldError = validators.url(val);
      if (fieldError) {
        setError(fieldError);
        setIsValidating(false);
        return;
      }
    }

    if (rule.phone) {
      fieldError = validators.phone(val);
      if (fieldError) {
        setError(fieldError);
        setIsValidating(false);
        return;
      }
    }

    if (rule.custom) {
      fieldError = rule.custom(val);
      if (fieldError) {
        setError(fieldError);
        setIsValidating(false);
        return;
      }
    }

    setError(null);
    setIsValidating(false);
  }, [field, rules]);

  // Debounced validation
  const debouncedValidate = useMemo(() => {
    let timeoutId: NodeJS.Timeout;
    
    return (val: string) => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => validate(val), debounceMs);
    };
  }, [validate, debounceMs]);

  // Validate on value change
  useEffect(() => {
    if (validateOnChange) {
      debouncedValidate(value);
    }
  }, [value, debouncedValidate, validateOnChange]);

  return {
    error,
    isValidating,
    validate: (val: string) => {
      if (validateOnChange) {
        debouncedValidate(val);
      } else {
        validate(val);
      }
    },
    clearError: () => setError(null),
  };
};

export default useFormValidation;
