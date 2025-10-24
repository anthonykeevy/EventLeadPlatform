/**
 * Onboarding Modal - Story 1.14
 * AC-1.14.1: Modal overlay on dashboard (cannot dismiss)
 */

import React, { useState, useEffect } from 'react'
import { OnboardingStep1 } from './OnboardingStep1'
import { OnboardingStep2 } from './OnboardingStep2'
import { ProgressIndicator } from './ProgressIndicator'
import { useAuth } from '../../auth'
import type { OnboardingStep1Data, OnboardingStep2Data } from '../types/onboarding.types'

interface OnboardingModalProps {
  isOpen: boolean
  onComplete: () => void
}

export function OnboardingModal({ isOpen, onComplete }: OnboardingModalProps) {
  const { user } = useAuth()
  const [currentStep, setCurrentStep] = useState(1)
  const [step1Data, setStep1Data] = useState<OnboardingStep1Data | null>(null)
  const [step2Data, setStep2Data] = useState<OnboardingStep2Data | null>(null)

  // Auto-save to localStorage - AC-1.14.7
  useEffect(() => {
    if (!user) return
    
    const draftKey = `onboarding_draft_${user.user_id}`
    const draft = {
      currentStep,
      step1Data,
      step2Data
    }
    localStorage.setItem(draftKey, JSON.stringify(draft))
  }, [currentStep, step1Data, step2Data, user])

  // Restore draft on mount
  useEffect(() => {
    if (!user) return
    
    const draftKey = `onboarding_draft_${user.user_id}`
    const savedDraft = localStorage.getItem(draftKey)
    
    if (savedDraft) {
      try {
        const draft = JSON.parse(savedDraft)
        setCurrentStep(draft.currentStep || 1)
        setStep1Data(draft.step1Data)
        setStep2Data(draft.step2Data)
      } catch (error) {
        console.error('Failed to restore onboarding draft:', error)
      }
    }
  }, [user])

  const handleStep1Complete = (data: OnboardingStep1Data) => {
    setStep1Data(data)
    setCurrentStep(2)
  }

  const handleStep2Complete = (data: OnboardingStep2Data) => {
    setStep2Data(data)
    
    // Clear draft from localStorage
    if (user) {
      localStorage.removeItem(`onboarding_draft_${user.user_id}`)
    }
    
    // Notify parent (dashboard) that onboarding is complete
    onComplete()
  }

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1)
    }
  }

  if (!isOpen) return null

  return (
    <>
      {/* Backdrop - AC-1.14.1: Semi-transparent, dashboard visible but dimmed */}
      <div
        className="fixed inset-0 bg-black bg-opacity-60 z-50"
        onClick={(e) => e.preventDefault()} // Prevent dismiss on click outside
      />

      {/* Modal - AC-1.14.1: Cannot dismiss, large size */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none">
        <div
          className="bg-white rounded-xl shadow-2xl w-full max-w-3xl max-h-[90vh] overflow-y-auto pointer-events-auto"
          role="dialog"
          aria-modal="true"
          aria-labelledby="onboarding-title"
        >
          {/* Header */}
          <div className="bg-gradient-to-r from-teal-600 to-teal-500 text-white p-8">
            <h2 id="onboarding-title" className="text-3xl font-bold mb-2">
              Welcome to EventLead! 👋
            </h2>
            <p className="text-teal-100">
              Let's get you set up - this will only take a few minutes
            </p>
          </div>

          {/* Progress Indicator - AC-1.14.6 */}
          <div className="px-8 pt-6">
            <ProgressIndicator currentStep={currentStep} totalSteps={2} />
          </div>

          {/* Step Content */}
          <div className="p-8">
            {currentStep === 1 && (
              <OnboardingStep1
                initialData={step1Data}
                onComplete={handleStep1Complete}
                user={user}
              />
            )}

            {currentStep === 2 && (
              <OnboardingStep2
                initialData={step2Data}
                onComplete={handleStep2Complete}
                onBack={handleBack}
                initialCountryId={step1Data?.countryId}
              />
            )}
          </div>
        </div>
      </div>
    </>
  )
}



