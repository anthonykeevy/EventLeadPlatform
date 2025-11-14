/**
 * Utility Exports - Global utilities
 * 
 * Makes utilities available globally for testing in browser console
 */

import { unsavedWorkTracker } from './unsavedWorkTracker'
import { offlineQueue } from './offlineQueue'
import { formAutoSave } from './formAutoSave'

export { unsavedWorkTracker, useUnsavedWork } from './unsavedWorkTracker'
export { offlineQueue } from './offlineQueue'
export { formAutoSave } from './formAutoSave'

// Make available on window for testing in browser console
if (typeof window !== 'undefined') {
  (window as any).unsavedWorkTracker = unsavedWorkTracker;
  (window as any).offlineQueue = offlineQueue
  ;(window as any).formAutoSave = formAutoSave
}

