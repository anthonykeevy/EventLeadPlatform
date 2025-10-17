/**
 * Tests for ConfigProvider Component - Story 1.13
 * Testing AC-1.13.9: Frontend Configuration Hook
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen } from '../../../test/utils'
import { ConfigProvider, useConfig } from '../ConfigProvider'

// Mock the useAppConfig hook instead of axios directly
vi.mock('../../../lib/config', () => ({
  useAppConfig: vi.fn(),
  DEFAULT_CONFIG: {
    password_min_length: 8,
    password_require_uppercase: false,
    password_require_number: true,
    jwt_access_expiry_minutes: 15,
    email_verification_expiry_hours: 24,
    invitation_expiry_days: 7,
    company_name_min_length: 2,
    company_name_max_length: 200,
  },
}))

import { useAppConfig } from '../../../lib/config'
const mockedUseAppConfig = vi.mocked(useAppConfig)

// Test component that uses useConfig hook
function TestComponent() {
  const { config, isLoading, error, isError } = useConfig()

  if (isLoading) return <div>Loading...</div>
  if (isError && error) return <div>Error: {error.message}</div>

  return (
    <div>
      <div data-testid="password-min-length">{config?.password_min_length}</div>
      <div data-testid="password-require-uppercase">{config?.password_require_uppercase.toString()}</div>
      <div data-testid="password-require-number">{config?.password_require_number.toString()}</div>
      <div data-testid="jwt-expiry">{config?.jwt_access_expiry_minutes}</div>
      <div data-testid="email-verification-expiry">{config?.email_verification_expiry_hours}</div>
      <div data-testid="invitation-expiry">{config?.invitation_expiry_days}</div>
      <div data-testid="company-name-min">{config?.company_name_min_length}</div>
      <div data-testid="company-name-max">{config?.company_name_max_length}</div>
    </div>
  )
}

// Mock configuration response
const mockConfigResponse = {
  password_min_length: 10,
  password_require_uppercase: true,
  password_require_number: true,
  jwt_access_expiry_minutes: 30,
  email_verification_expiry_hours: 48,
  invitation_expiry_days: 14,
  company_name_min_length: 3,
  company_name_max_length: 150,
}

describe('ConfigProvider', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('AC-1.13.9: Configuration Provider Functionality', () => {
    it('should provide configuration to child components', () => {
      // Mock successful config load
      mockedUseAppConfig.mockReturnValue({
        config: mockConfigResponse,
        isLoading: false,
        error: null,
        isError: false,
        data: mockConfigResponse,
      } as any)

      render(
        <ConfigProvider>
          <TestComponent />
        </ConfigProvider>
      )

      // Verify all config values are rendered
      expect(screen.getByTestId('password-min-length')).toHaveTextContent('10')
      expect(screen.getByTestId('password-require-uppercase')).toHaveTextContent('true')
      expect(screen.getByTestId('password-require-number')).toHaveTextContent('true')
      expect(screen.getByTestId('jwt-expiry')).toHaveTextContent('30')
      expect(screen.getByTestId('email-verification-expiry')).toHaveTextContent('48')
      expect(screen.getByTestId('invitation-expiry')).toHaveTextContent('14')
      expect(screen.getByTestId('company-name-min')).toHaveTextContent('3')
      expect(screen.getByTestId('company-name-max')).toHaveTextContent('150')
    })

    it('should handle API errors gracefully', () => {
      // Mock API error
      mockedUseAppConfig.mockReturnValue({
        config: undefined,
        isLoading: false,
        error: new Error('Failed to fetch configuration'),
        isError: true,
        data: undefined,
      } as any)

      render(
        <ConfigProvider>
          <TestComponent />
        </ConfigProvider>
      )

      expect(screen.getByText(/Error:/)).toBeInTheDocument()
      expect(screen.getByText(/Failed to fetch configuration/)).toBeInTheDocument()
    })

    it('should show loading state while fetching configuration', () => {
      // Mock loading state
      mockedUseAppConfig.mockReturnValue({
        config: undefined,
        isLoading: true,
        error: null,
        isError: false,
        data: undefined,
      } as any)

      render(
        <ConfigProvider>
          <TestComponent />
        </ConfigProvider>
      )

      expect(screen.getByText('Loading...')).toBeInTheDocument()
    })
  })

  describe('useConfig Hook', () => {
    it('should throw error when used outside ConfigProvider', () => {
      // Suppress console.error for this test
      const originalError = console.error
      console.error = vi.fn()

      // Mock the hook for the test that doesn't use ConfigProvider
      mockedUseAppConfig.mockReturnValue({
        config: mockConfigResponse,
        isLoading: false,
        error: null,
        isError: false,
        data: mockConfigResponse,
      } as any)

      expect(() => {
        render(<TestComponent />)
      }).toThrow('useConfig must be used within a ConfigProvider')

      // Restore console.error
      console.error = originalError
    })

    it('should provide config context to nested components', () => {
      mockedUseAppConfig.mockReturnValue({
        config: mockConfigResponse,
        isLoading: false,
        error: null,
        isError: false,
        data: mockConfigResponse,
      } as any)

      function NestedComponent() {
        const { config } = useConfig()
        return <div data-testid="nested-config">{config?.password_min_length}</div>
      }

      render(
        <ConfigProvider>
          <div>
            <div>
              <NestedComponent />
            </div>
          </div>
        </ConfigProvider>
      )

      expect(screen.getByTestId('nested-config')).toHaveTextContent('10')
    })
  })

  describe('Configuration Values', () => {
    it('should handle all configuration fields correctly', () => {
      const customConfig = {
        password_min_length: 12,
        password_require_uppercase: false,
        password_require_number: false,
        jwt_access_expiry_minutes: 60,
        email_verification_expiry_hours: 24,
        invitation_expiry_days: 7,
        company_name_min_length: 2,
        company_name_max_length: 200,
      }

      mockedUseAppConfig.mockReturnValue({
        config: customConfig,
        isLoading: false,
        error: null,
        isError: false,
        data: customConfig,
      } as any)

      render(
        <ConfigProvider>
          <TestComponent />
        </ConfigProvider>
      )

      expect(screen.getByTestId('password-min-length')).toHaveTextContent('12')
      expect(screen.getByTestId('password-require-uppercase')).toHaveTextContent('false')
      expect(screen.getByTestId('password-require-number')).toHaveTextContent('false')
      expect(screen.getByTestId('jwt-expiry')).toHaveTextContent('60')
      expect(screen.getByTestId('email-verification-expiry')).toHaveTextContent('24')
      expect(screen.getByTestId('invitation-expiry')).toHaveTextContent('7')
      expect(screen.getByTestId('company-name-min')).toHaveTextContent('2')
      expect(screen.getByTestId('company-name-max')).toHaveTextContent('200')
    })
  })
})

