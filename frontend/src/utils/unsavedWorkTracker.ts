/**
 * Unsaved Work Tracker - Story 1.16 Enhanced
 * 
 * Central utility for tracking unsaved work across the application.
 * Prevents data loss when auth changes occur in other tabs.
 * 
 * Used by:
 * - Form Builder (drafts, unsaved changes)
 * - Lead Forms (offline captures, pending uploads)
 * - Dashboard (unsaved settings)
 * - Any component with stateful unsaved data
 */

export interface UnsavedWorkSource {
  id: string
  type: 'form_builder' | 'lead_capture' | 'settings' | 'other'
  description: string
  isDirty: boolean
  autoSaveEnabled: boolean
  lastSaved?: Date
  onSave?: () => Promise<void>
}

class UnsavedWorkTracker {
  private sources: Map<string, UnsavedWorkSource> = new Map()
  private listeners: Set<(hasUnsavedWork: boolean) => void> = new Set()

  /**
   * Register a source of unsaved work
   */
  register(source: UnsavedWorkSource): void {
    this.sources.set(source.id, source)
    this.notifyListeners()
  }

  /**
   * Unregister a source (component unmounted or work saved)
   */
  unregister(sourceId: string): void {
    this.sources.delete(sourceId)
    this.notifyListeners()
  }

  /**
   * Update an existing source
   */
  update(sourceId: string, updates: Partial<UnsavedWorkSource>): void {
    const existing = this.sources.get(sourceId)
    if (existing) {
      this.sources.set(sourceId, { ...existing, ...updates })
      this.notifyListeners()
    }
  }

  /**
   * Mark a source as dirty (has unsaved changes)
   */
  markDirty(sourceId: string): void {
    this.update(sourceId, { isDirty: true })
  }

  /**
   * Mark a source as clean (saved)
   */
  markClean(sourceId: string): void {
    this.update(sourceId, { isDirty: false, lastSaved: new Date() })
  }

  /**
   * Check if ANY source has unsaved work
   */
  hasUnsavedWork(): boolean {
    return Array.from(this.sources.values()).some(source => source.isDirty)
  }

  /**
   * Get all sources with unsaved work
   */
  getUnsavedSources(): UnsavedWorkSource[] {
    return Array.from(this.sources.values()).filter(source => source.isDirty)
  }

  /**
   * Get count of unsaved sources
   */
  getUnsavedCount(): number {
    return this.getUnsavedSources().length
  }

  /**
   * Save all dirty sources
   */
  async saveAll(): Promise<void> {
    const unsavedSources = this.getUnsavedSources()
    
    await Promise.all(
      unsavedSources.map(async (source) => {
        if (source.onSave) {
          try {
            await source.onSave()
            this.markClean(source.id)
          } catch (error) {
            console.error(`Failed to save ${source.id}:`, error)
            throw error
          }
        }
      })
    )
  }

  /**
   * Subscribe to unsaved work changes
   */
  subscribe(listener: (hasUnsavedWork: boolean) => void): () => void {
    this.listeners.add(listener)
    
    // Return unsubscribe function
    return () => {
      this.listeners.delete(listener)
    }
  }

  /**
   * Notify all listeners of unsaved work state change
   */
  private notifyListeners(): void {
    const hasUnsaved = this.hasUnsavedWork()
    this.listeners.forEach(listener => listener(hasUnsaved))
  }

  /**
   * Get summary of unsaved work for display
   */
  getSummary(): string {
    const sources = this.getUnsavedSources()
    
    if (sources.length === 0) {
      return 'No unsaved work'
    }
    
    if (sources.length === 1) {
      return sources[0].description
    }
    
    return `${sources.length} items with unsaved changes`
  }

  /**
   * Check for browser beforeunload handlers
   * (Some components may set their own)
   */
  hasBeforeUnloadHandler(): boolean {
    return window.onbeforeunload !== null
  }

  /**
   * Clear all sources (use on logout/session end)
   */
  clear(): void {
    this.sources.clear()
    this.notifyListeners()
  }
}

// Singleton instance
export const unsavedWorkTracker = new UnsavedWorkTracker()

/**
 * React hook for tracking unsaved work in a component
 */
export function useUnsavedWork(
  id: string,
  type: UnsavedWorkSource['type'],
  description: string,
  onSave?: () => Promise<void>
) {
  const [isDirty, setIsDirty] = React.useState(false)

  React.useEffect(() => {
    // Register this component as a source
    unsavedWorkTracker.register({
      id,
      type,
      description,
      isDirty,
      autoSaveEnabled: false,
      onSave
    })

    return () => {
      // Unregister on unmount
      unsavedWorkTracker.unregister(id)
    }
  }, [id, type, description, onSave])

  React.useEffect(() => {
    // Update dirty state
    if (isDirty) {
      unsavedWorkTracker.markDirty(id)
    } else {
      unsavedWorkTracker.markClean(id)
    }
  }, [id, isDirty])

  return {
    isDirty,
    setIsDirty,
    markDirty: () => setIsDirty(true),
    markClean: () => setIsDirty(false)
  }
}

// Add React import for the hook
import React from 'react'


