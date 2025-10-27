import { useState, useEffect, useCallback, useRef } from 'react';

export interface UseAutoSaveOptions {
  key: string;
  data: any;
  interval?: number; // in milliseconds
  onSave?: (data: any) => void;
  onRestore?: (data: any) => void;
  enabled?: boolean;
  debounceMs?: number;
}

export interface UseAutoSaveReturn {
  isSaving: boolean;
  lastSaved: Date | null;
  saveStatus: 'saving' | 'saved' | 'error' | 'idle';
  saveManually: () => void;
  clearSavedData: () => void;
  hasUnsavedChanges: boolean;
}

export const useAutoSave = ({
  key,
  data,
  interval = 30000, // 30 seconds
  onSave,
  onRestore,
  enabled = true,
  debounceMs = 1000,
}: UseAutoSaveOptions): UseAutoSaveReturn => {
  const [isSaving, setIsSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  const [saveStatus, setSaveStatus] = useState<'saving' | 'saved' | 'error' | 'idle'>('idle');
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);
  
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const debounceRef = useRef<NodeJS.Timeout | null>(null);
  const lastSavedDataRef = useRef<any>(null);

  // Check if data has changed
  const dataChanged = useCallback((currentData: any, lastData: any) => {
    return JSON.stringify(currentData) !== JSON.stringify(lastData);
  }, []);

  // Save data to localStorage
  const saveToStorage = useCallback((dataToSave: any) => {
    try {
      const saveData = {
        data: dataToSave,
        timestamp: new Date().toISOString(),
        version: '1.0',
      };
      
      localStorage.setItem(`autosave_${key}`, JSON.stringify(saveData));
      setLastSaved(new Date());
      setSaveStatus('saved');
      setHasUnsavedChanges(false);
      lastSavedDataRef.current = dataToSave;
      
      onSave?.(dataToSave);
    } catch (error) {
      console.error('Failed to save data to localStorage:', error);
      setSaveStatus('error');
    }
  }, [key, onSave]);

  // Load data from localStorage
  const loadFromStorage = useCallback(() => {
    try {
      const saved = localStorage.getItem(`autosave_${key}`);
      if (saved) {
        const { data: savedData, timestamp } = JSON.parse(saved);
        setLastSaved(new Date(timestamp));
        lastSavedDataRef.current = savedData;
        onRestore?.(savedData);
        return savedData;
      }
    } catch (error) {
      console.error('Failed to load data from localStorage:', error);
    }
    return null;
  }, [key, onRestore]);

  // Debounced save function
  const debouncedSave = useCallback((dataToSave: any) => {
    if (debounceRef.current) {
      clearTimeout(debounceRef.current);
    }
    
    debounceRef.current = setTimeout(() => {
      if (dataChanged(dataToSave, lastSavedDataRef.current)) {
        setIsSaving(true);
        setSaveStatus('saving');
        
        // Simulate async save operation
        setTimeout(() => {
          saveToStorage(dataToSave);
          setIsSaving(false);
        }, 500);
      }
    }, debounceMs);
  }, [dataChanged, saveToStorage, debounceMs]);

  // Manual save function
  const saveManually = useCallback(() => {
    if (dataChanged(data, lastSavedDataRef.current)) {
      setIsSaving(true);
      setSaveStatus('saving');
      
      setTimeout(() => {
        saveToStorage(data);
        setIsSaving(false);
      }, 500);
    }
  }, [data, dataChanged, saveToStorage]);

  // Clear saved data
  const clearSavedData = useCallback(() => {
    try {
      localStorage.removeItem(`autosave_${key}`);
      setLastSaved(null);
      setSaveStatus('idle');
      setHasUnsavedChanges(false);
      lastSavedDataRef.current = null;
    } catch (error) {
      console.error('Failed to clear saved data:', error);
    }
  }, [key]);

  // Set up auto-save interval
  useEffect(() => {
    if (enabled && interval > 0) {
      intervalRef.current = setInterval(() => {
        if (dataChanged(data, lastSavedDataRef.current)) {
          debouncedSave(data);
        }
      }, interval);

      return () => {
        if (intervalRef.current) {
          clearInterval(intervalRef.current);
        }
      };
    }
  }, [enabled, interval, data, dataChanged, debouncedSave]);

  // Track data changes
  useEffect(() => {
    if (enabled) {
      const changed = dataChanged(data, lastSavedDataRef.current);
      setHasUnsavedChanges(changed);
      
      if (changed) {
        debouncedSave(data);
      }
    }
  }, [data, enabled, dataChanged, debouncedSave]);

  // Load saved data on mount
  useEffect(() => {
    if (enabled) {
      loadFromStorage();
    }
  }, [enabled, loadFromStorage]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (debounceRef.current) {
        clearTimeout(debounceRef.current);
      }
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  return {
    isSaving,
    lastSaved,
    saveStatus,
    saveManually,
    clearSavedData,
    hasUnsavedChanges,
  };
};

// Hook for form auto-save with visual feedback
export const useFormAutoSave = (
  formData: Record<string, any>,
  formKey: string,
  options: Partial<UseAutoSaveOptions> = {}
) => {
  const autoSave = useAutoSave({
    key: formKey,
    data: formData,
    ...options,
  });

  const getStatusMessage = () => {
    switch (autoSave.saveStatus) {
      case 'saving':
        return 'Saving...';
      case 'saved':
        return autoSave.lastSaved 
          ? `Auto-saved at ${autoSave.lastSaved.toLocaleTimeString()}`
          : 'Saved';
      case 'error':
        return 'Save failed';
      default:
        return autoSave.hasUnsavedChanges ? 'Unsaved changes' : '';
    }
  };

  const getStatusColor = () => {
    switch (autoSave.saveStatus) {
      case 'saving':
        return 'text-blue-600';
      case 'saved':
        return 'text-green-600';
      case 'error':
        return 'text-red-600';
      default:
        return autoSave.hasUnsavedChanges ? 'text-yellow-600' : 'text-gray-500';
    }
  };

  return {
    ...autoSave,
    statusMessage: getStatusMessage(),
    statusColor: getStatusColor(),
  };
};

export default useAutoSave;

