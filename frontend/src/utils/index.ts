/**
 * Utility Exports - Global utilities
 * 
 * Makes utilities available globally for testing in browser console
 */

import { unsavedWorkTracker } from './unsavedWorkTracker'
import { offlineQueue } from './offlineQueue'

export { unsavedWorkTracker, useUnsavedWork } from './unsavedWorkTracker'
export { offlineQueue } from './offlineQueue'

// Make available on window for testing in browser console
if (typeof window !== 'undefined') {
  (window as any).unsavedWorkTracker = unsavedWorkTracker;
  (window as any).offlineQueue = offlineQueue
}

