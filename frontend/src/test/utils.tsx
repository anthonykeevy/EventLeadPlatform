/**
 * Test utilities for EventLead Platform Frontend
 */
import React from 'react'
import { render, RenderOptions } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { vi } from 'vitest'

// Test wrapper component
interface TestWrapperProps {
  children: React.ReactNode
}

const TestWrapper: React.FC<TestWrapperProps> = ({ children }) => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
        gcTime: 0,
      },
      mutations: {
        retry: false,
      },
    },
  })

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        {children}
      </BrowserRouter>
    </QueryClientProvider>
  )
}

// Custom render function with providers
const customRender = (
  ui: React.ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) => render(ui, { wrapper: TestWrapper, ...options })

// Re-export everything
export * from '@testing-library/react'
export { customRender as render }

// Mock data factories
export const createMockUser = (overrides = {}) => ({
  user_id: '123',
  email: 'test@example.com',
  first_name: 'Test',
  last_name: 'User',
  email_verified: false,
  created_date: '2024-01-01T00:00:00Z',
  ...overrides,
})

export const createMockCompany = (overrides = {}) => ({
  company_id: '456',
  company_name: 'Test Company Pty Ltd',
  abn: '12345678901',
  industry: 'Technology',
  address: '123 Test Street, Test City, NSW 2000',
  phone: '+61234567890',
  website: 'https://testcompany.com',
  ...overrides,
})

export const createMockEvent = (overrides = {}) => ({
  event_id: '789',
  event_name: 'Test Event',
  description: 'Test event description',
  start_date: '2024-12-01T09:00:00Z',
  end_date: '2024-12-01T17:00:00Z',
  location: 'Test Venue, Test City',
  max_attendees: 100,
  ...overrides,
})

// Mock API responses
export const createMockApiResponse = <T,>(data: T, status = 200) => ({
  data,
  status,
  statusText: 'OK',
  headers: {},
  config: {},
})

export const createMockErrorResponse = (message: string, status = 400) => ({
  response: {
    data: { detail: message },
    status,
    statusText: 'Bad Request',
    headers: {},
    config: {},
  },
})

// Mock fetch responses
export const mockFetchSuccess = <T,>(data: T, status = 200) => {
  return vi.fn().mockResolvedValue({
    ok: true,
    status,
    json: () => Promise.resolve(data),
    text: () => Promise.resolve(JSON.stringify(data)),
  })
}

export const mockFetchError = (message: string, status = 400) => {
  return vi.fn().mockResolvedValue({
    ok: false,
    status,
    json: () => Promise.resolve({ detail: message }),
    text: () => Promise.resolve(JSON.stringify({ detail: message })),
  })
}

// Test constants
export const TEST_CONSTANTS = {
  VALID_EMAIL: 'test@example.com',
  INVALID_EMAIL: 'invalid-email',
  VALID_PASSWORD: 'TestPassword123!',
  WEAK_PASSWORD: '123',
  VALID_ABN: '12345678901',
  INVALID_ABN: '1234567890',
  
  API_ENDPOINTS: {
    SIGNUP: '/api/auth/signup',
    LOGIN: '/api/auth/login',
    VERIFY_EMAIL: '/api/auth/verify-email',
    RESET_PASSWORD: '/api/auth/reset-password',
    REFRESH_TOKEN: '/api/auth/refresh',
    USER_PROFILE: '/api/auth/me',
  },
  
  HTTP_STATUS: {
    OK: 200,
    CREATED: 201,
    BAD_REQUEST: 400,
    UNAUTHORIZED: 401,
    FORBIDDEN: 403,
    NOT_FOUND: 404,
    CONFLICT: 409,
    UNPROCESSABLE_ENTITY: 422,
    TOO_MANY_REQUESTS: 429,
    INTERNAL_SERVER_ERROR: 500,
  },
  
  TEST_TIMEOUTS: {
    DEFAULT: 5000,
    LONG: 10000,
  },
} as const

// Form testing utilities
export const fillFormField = async (
  getByLabelText: (text: string) => HTMLElement,
  label: string,
  value: string
) => {
  const field = getByLabelText(label)
  await userEvent.type(field, value)
  return field
}

export const submitForm = async (
  getByRole: (role: string, options?: any) => HTMLElement
) => {
  const submitButton = getByRole('button', { name: /submit|sign up|log in|verify/i })
  await userEvent.click(submitButton)
  return submitButton
}

// Wait utilities
export const waitForApiCall = async (mockFn: any) => {
  await waitFor(() => {
    expect(mockFn).toHaveBeenCalled()
  })
}

export const waitForErrorMessage = async (getByText: (text: RegExp | string) => HTMLElement) => {
  await waitFor(() => {
    expect(getByText(/error|invalid|required/i)).toBeInTheDocument()
  })
}

export const waitForSuccessMessage = async (getByText: (text: RegExp | string) => HTMLElement) => {
  await waitFor(() => {
    expect(getByText(/success|verified|sent/i)).toBeInTheDocument()
  })
}

// Import userEvent for form testing
import userEvent from '@testing-library/user-event'
import { waitFor } from '@testing-library/react'
