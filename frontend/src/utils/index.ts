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
declare global {
  interface Window {
    unsavedWorkTracker?: typeof unsavedWorkTracker;
    offlineQueue?: typeof offlineQueue;
    formAutoSave?: typeof formAutoSave;
  }
}
if (typeof window !== 'undefined') {
  window.unsavedWorkTracker = unsavedWorkTracker;
  window.offlineQueue = offlineQueue;
  window.formAutoSave = formAutoSave;
}

