/**
 * Form Auto-Save Service
 * 
 * Handles automatic saving and restoration of form state.
 * Prevents data loss when users go offline or reload the page.
 * 
 * Features:
 * - Auto-save form state to IndexedDB every 30 seconds
 * - Restore form state on page reload
 * - Clear saved state after successful submission
 * - Handle multiple forms (event creation, event edit, lead forms)
 * 
 * Storage Key Format: form_draft_{formType}_{formId}_{userId}
 */

import { offlineQueue as _offlineQueue } from './offlineQueue'

export type FormType = 'event_create' | 'event_edit' | 'lead_form' | 'invitation' | 'other'

interface FormDraft {
  formType: FormType
  formId?: string // Optional: for edit forms
  userId: number
  data: Record<string, unknown> // Form data (validated before saving)
  timestamp: number
  version: number // For conflict detection
}

class FormAutoSave {
  private readonly DB_NAME = 'eventlead_form_drafts'
  private readonly STORE_NAME = 'drafts'
  private readonly DB_VERSION = 1
  private db: IDBDatabase | null = null
  private saveIntervals: Map<string, NodeJS.Timeout> = new Map()
  private firstSaveFlags: Map<string, boolean> = new Map()

  /**
   * Initialize IndexedDB
   */
  async initialize(): Promise<void> {
    if (this.db) return

    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.DB_NAME, this.DB_VERSION)

      request.onerror = () => reject(request.error)
      request.onsuccess = () => {
        this.db = request.result
        console.log('✅ Form auto-save initialized')
        resolve()
      }

      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result

        if (!db.objectStoreNames.contains(this.STORE_NAME)) {
          const store = db.createObjectStore(this.STORE_NAME, { keyPath: 'key' })
          store.createIndex('formType', 'formType', { unique: false })
          store.createIndex('userId', 'userId', { unique: false })
          store.createIndex('timestamp', 'timestamp', { unique: false })
        }
      }
    })
  }

  /**
   * Generate storage key
   */
  private getStorageKey(formType: FormType, formId: string | undefined, userId: number): string {
    const idPart = formId ? `_${formId}` : ''
    return `form_draft_${formType}${idPart}_${userId}`
  }

  /**
   * Start auto-saving a form
   * 
   * @param formType - Type of form (event_create, event_edit, etc.)
   * @param formId - Optional form ID (for edit forms)
   * @param userId - Current user ID
   * @param getFormData - Function that returns current form data
   * @param onFirstSave - Optional callback for first save notification
   */
  startAutoSave(
    formType: FormType,
    formId: string | undefined,
    userId: number,
    getFormData: () => Record<string, unknown>,
    onFirstSave?: () => void
  ): () => void {
    const key = this.getStorageKey(formType, formId, userId)

    // Clear any existing interval
    this.stopAutoSave(formType, formId, userId)

    // Initialize first save flag
    if (!this.firstSaveFlags.has(key)) {
      this.firstSaveFlags.set(key, true)
    }

    // Auto-save every 30 seconds
    const interval = setInterval(async () => {
      const formData = getFormData()

      // Only save if form has meaningful data
      if (this.hasFormData(formData)) {
        await this.save(formType, formId, userId, formData)

        // Show notification on first save only
        const isFirstSave = this.firstSaveFlags.get(key)
        if (isFirstSave && onFirstSave) {
          onFirstSave()
          this.firstSaveFlags.set(key, false)
        }
      }
    }, 30000) // 30 seconds

    this.saveIntervals.set(key, interval)

    // Return cleanup function
    return () => this.stopAutoSave(formType, formId, userId)
  }

  /**
   * Stop auto-saving a form
   */
  stopAutoSave(formType: FormType, formId: string | undefined, userId: number): void {
    const key = this.getStorageKey(formType, formId, userId)
    const interval = this.saveIntervals.get(key)

    if (interval) {
      clearInterval(interval)
      this.saveIntervals.delete(key)
    }
  }

  /**
   * Check if form has meaningful data
   */
  private hasFormData(data: unknown): boolean {
    if (!data || typeof data !== 'object') return false

    const d = data as Record<string, unknown>
    // Check for common form fields
    const hasName = typeof d.name === 'string' && d.name.trim().length > 0
    const hasStartDate = d.startDatetime || d.startDateTime
    const hasDescription = d.description || d.shortDescription

    return hasName || !!hasStartDate || !!hasDescription
  }

  /**
   * Save form draft
   */
  async save(
    formType: FormType,
    formId: string | undefined,
    userId: number,
    data: Record<string, unknown>
  ): Promise<void> {
    if (!this.db) await this.initialize()

    const key = this.getStorageKey(formType, formId, userId)

    // Get existing draft to increment version
    const existing = await this.get(formType, formId, userId)
    const version = existing ? existing.version + 1 : 1

    const draft: FormDraft = {
      formType,
      formId,
      userId,
      data,
      timestamp: Date.now(),
      version,
    }

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([this.STORE_NAME], 'readwrite')
      const store = transaction.objectStore(this.STORE_NAME)
      const request = store.put({ key, ...draft })

      request.onsuccess = () => {
        console.log(`💾 Draft saved: ${key}`)
        resolve()
      }
      request.onerror = () => reject(request.error)
    })
  }

  /**
   * Get form draft
   */
  async get(
    formType: FormType,
    formId: string | undefined,
    userId: number
  ): Promise<FormDraft | null> {
    if (!this.db) await this.initialize()

    const key = this.getStorageKey(formType, formId, userId)

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([this.STORE_NAME], 'readonly')
      const store = transaction.objectStore(this.STORE_NAME)
      const request = store.get(key)

      request.onsuccess = () => {
        const result = request.result
        if (result) {
          // Remove the 'key' property before returning
          const { key: _, ...draft } = result
          resolve(draft as FormDraft)
        } else {
          resolve(null)
        }
      }
      request.onerror = () => reject(request.error)
    })
  }

  /**
   * Restore form draft
   * Returns the form data if a draft exists
   */
  async restore(
    formType: FormType,
    formId: string | undefined,
    userId: number
  ): Promise<Record<string, unknown> | null> {
    const draft = await this.get(formType, formId, userId)
    return draft ? draft.data : null
  }

  /**
   * Clear form draft (after successful submission)
   */
  async clear(
    formType: FormType,
    formId: string | undefined,
    userId: number
  ): Promise<void> {
    if (!this.db) await this.initialize()

    const key = this.getStorageKey(formType, formId, userId)

    // Stop auto-save
    this.stopAutoSave(formType, formId, userId)

    // Clear first save flag
    this.firstSaveFlags.delete(key)

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([this.STORE_NAME], 'readwrite')
      const store = transaction.objectStore(this.STORE_NAME)
      const request = store.delete(key)

      request.onsuccess = () => {
        console.log(`🗑️ Draft cleared: ${key}`)
        resolve()
      }
      request.onerror = () => reject(request.error)
    })
  }

  /**
   * Clear all drafts for a user (cleanup)
   */
  async clearAllForUser(userId: number): Promise<void> {
    if (!this.db) await this.initialize()

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([this.STORE_NAME], 'readwrite')
      const store = transaction.objectStore(this.STORE_NAME)
      const index = store.index('userId')
      const request = index.openCursor(IDBKeyRange.only(userId))

      request.onsuccess = (event) => {
        const cursor = (event.target as IDBRequest<IDBCursorWithValue>).result
        if (cursor) {
          cursor.delete()
          cursor.continue()
        } else {
          resolve()
        }
      }
      request.onerror = () => reject(request.error)
    })
  }

  /**
   * Clean up old drafts (older than 7 days)
   */
  async cleanupOldDrafts(): Promise<void> {
    if (!this.db) await this.initialize()

    const sevenDaysAgo = Date.now() - 7 * 24 * 60 * 60 * 1000

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([this.STORE_NAME], 'readwrite')
      const store = transaction.objectStore(this.STORE_NAME)
      const index = store.index('timestamp')
      const request = index.openCursor(IDBKeyRange.upperBound(sevenDaysAgo))

      request.onsuccess = (event) => {
        const cursor = (event.target as IDBRequest<IDBCursorWithValue>).result
        if (cursor) {
          cursor.delete()
          cursor.continue()
        } else {
          resolve()
        }
      }
      request.onerror = () => reject(request.error)
    })
  }
}

// Singleton instance
export const formAutoSave = new FormAutoSave()

// Auto-initialize
if (typeof window !== 'undefined') {
  formAutoSave.initialize().catch(console.error)
  
  // Cleanup old drafts on startup
  formAutoSave.cleanupOldDrafts().catch(console.error)
}

