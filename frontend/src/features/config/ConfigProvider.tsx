/**
 * Configuration Provider Component - Story 1.13
 * Provides global application configuration context
 * AC-1.13.9: ConfigProvider Context
 */
import React, { createContext, useContext, ReactNode } from 'react'
import { useAppConfig, AppConfig } from '../../lib/config'

// Context type
interface ConfigContextType {
  config: AppConfig | undefined
  isLoading: boolean
  error: Error | null
  isError: boolean
}

// Create context with undefined as default (will be provided by ConfigProvider)
const ConfigContext = createContext<ConfigContextType | undefined>(undefined)

// Provider Props
interface ConfigProviderProps {
  children: ReactNode
}

/**
 * ConfigProvider Component
 * 
 * Wraps the application to provide configuration context to all child components.
 * Fetches configuration from the backend API and caches it with React Query.
 * 
 * Features:
 * - Automatic configuration fetching on mount
 * - 5-minute cache with React Query
 * - Global access to configuration via useConfig hook
 * - Loading and error states
 * 
 * Usage:
 * ```tsx
 * // In main.tsx or App.tsx:
 * <ConfigProvider>
 *   <App />
 * </ConfigProvider>
 * 
 * // In any component:
 * function SignupForm() {
 *   const { config, isLoading } = useConfig();
 *   
 *   if (isLoading) return <LoadingSpinner />;
 *   
 *   return (
 *     <input 
 *       type="password"
 *       minLength={config?.password_min_length || 8}
 *       placeholder={`Password (min ${config?.password_min_length || 8} characters)`}
 *     />
 *   );
 * }
 * ```
 */
export function ConfigProvider({ children }: ConfigProviderProps) {
  const { config, isLoading, error, isError } = useAppConfig()

  const value: ConfigContextType = {
    config,
    isLoading,
    error,
    isError,
  }

  return <ConfigContext.Provider value={value}>{children}</ConfigContext.Provider>
}

/**
 * useConfig Hook
 * 
 * Access application configuration from any component within ConfigProvider.
 * 
 * @throws {Error} If used outside of ConfigProvider
 * @returns {ConfigContextType} Configuration context with config, loading, and error states
 * 
 * Usage:
 * ```tsx
 * function MyComponent() {
 *   const { config, isLoading, error, isError } = useConfig();
 *   
 *   if (isLoading) return <div>Loading configuration...</div>;
 *   if (isError) return <div>Error: {error?.message}</div>;
 *   
 *   return <div>Min password length: {config?.password_min_length}</div>;
 * }
 * ```
 */
export function useConfig(): ConfigContextType {
  const context = useContext(ConfigContext)

  if (context === undefined) {
    throw new Error('useConfig must be used within a ConfigProvider')
  }

  return context
}

/**
 * Export ConfigContext for testing purposes
 */
export { ConfigContext }

