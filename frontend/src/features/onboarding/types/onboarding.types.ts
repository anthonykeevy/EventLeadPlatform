/**
 * Onboarding Types - Story 1.14
 * Type definitions for onboarding flow
 */

export interface OnboardingStep1Data {
  firstName: string
  lastName: string
  phone?: string
  roleTitle?: string
  countryId?: number  // Story 1.20: User's selected country
}

export interface OnboardingStep2Data {
  companyName: string
  abn: string
  gstRegistered: boolean
  billingAddress: string
  billingSuburb: string
  billingState: string
  billingPostcode: string
  billingCountry: string
}

export interface OnboardingState {
  currentStep: number
  step1Data: OnboardingStep1Data | null
  step2Data: OnboardingStep2Data | null
  isSubmitting: boolean
  error: string | null
}

export interface OnboardingModalProps {
  isOpen: boolean
  onComplete: () => void
}



