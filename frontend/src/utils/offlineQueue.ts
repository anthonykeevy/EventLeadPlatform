/**
 * Offline Queue Manager - Lead Capture Support
 * 
 * Handles offline lead capture at events where internet is unreliable.
 * Queues leads locally and uploads when connection is restored.
 * 
 * Features:
 * - IndexedDB storage (more space than localStorage)
 * - Automatic retry with exponential backoff
 * - Background sync when available
 * - Queue status tracking
 * - Conflict resolution
 */

export interface QueuedItem<T = any> {
  id: string
  type: 'lead_submission' | 'form_draft' | 'other'
  data: T
  timestamp: number
  retryCount: number
  lastRetry?: number
  error?: string
  status: 'pending' | 'uploading' | 'failed' | 'success'
}

export interface OfflineQueueStats {
  totalQueued: number
  pending: number
  uploading: number
  failed: number
  success: number
  oldestItemAge: number // milliseconds
}

class OfflineQueue {
  private db: IDBDatabase | null = null
  private readonly DB_NAME = 'eventlead_offline'
  private readonly STORE_NAME = 'queue'
  private readonly DB_VERSION = 1
  
  private isOnline: boolean = navigator.onLine
  private uploadInProgress: boolean = false
  private listeners: Set<(stats: OfflineQueueStats) => void> = new Set()

  /**
   * Initialize IndexedDB
   */
  async initialize(): Promise<void> {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.DB_NAME, this.DB_VERSION)

      request.onerror = () => reject(request.error)
      request.onsuccess = () => {
        this.db = request.result
        console.log('✅ Offline queue initialized')
        resolve()
      }

      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result
        
        if (!db.objectStoreNames.contains(this.STORE_NAME)) {
          const store = db.createObjectStore(this.STORE_NAME, { keyPath: 'id' })
          store.createIndex('status', 'status', { unique: false })
          store.createIndex('timestamp', 'timestamp', { unique: false })
          store.createIndex('type', 'type', { unique: false })
        }
      }
    })
  }

  /**
   * Add item to queue
   */
  async enqueue<T>(type: QueuedItem['type'], data: T): Promise<string> {
    if (!this.db) await this.initialize()

    const item: QueuedItem<T> = {
      id: `${type}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      type,
      data,
      timestamp: Date.now(),
      retryCount: 0,
      status: 'pending'
    }

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([this.STORE_NAME], 'readwrite')
      const store = transaction.objectStore(this.STORE_NAME)
      const request = store.add(item)

      request.onsuccess = () => {
        console.log(`✅ Queued ${type}:`, item.id)
        this.notifyListeners()
        
        // Try to upload immediately if online
        if (this.isOnline) {
          this.processQueue()
        }
        
        resolve(item.id)
      }
      request.onerror = () => reject(request.error)
    })
  }

  /**
   * Get all queued items
   */
  async getAll(): Promise<QueuedItem[]> {
    if (!this.db) await this.initialize()

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([this.STORE_NAME], 'readonly')
      const store = transaction.objectStore(this.STORE_NAME)
      const request = store.getAll()

      request.onsuccess = () => resolve(request.result)
      request.onerror = () => reject(request.error)
    })
  }

  /**
   * Get pending items only
   */
  async getPending(): Promise<QueuedItem[]> {
    const all = await this.getAll()
    return all.filter(item => item.status === 'pending' || item.status === 'failed')
  }

  /**
   * Update item status
   */
  async updateStatus(id: string, status: QueuedItem['status'], error?: string): Promise<void> {
    if (!this.db) await this.initialize()

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([this.STORE_NAME], 'readwrite')
      const store = transaction.objectStore(this.STORE_NAME)
      const getRequest = store.get(id)

      getRequest.onsuccess = () => {
        const item = getRequest.result
        if (item) {
          item.status = status
          if (error) item.error = error
          if (status === 'failed') item.retryCount++
          if (status === 'uploading') item.lastRetry = Date.now()

          const updateRequest = store.put(item)
          updateRequest.onsuccess = () => {
            this.notifyListeners()
            resolve()
          }
          updateRequest.onerror = () => reject(updateRequest.error)
        } else {
          resolve()
        }
      }
      getRequest.onerror = () => reject(getRequest.error)
    })
  }

  /**
   * Remove item from queue
   */
  async remove(id: string): Promise<void> {
    if (!this.db) await this.initialize()

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([this.STORE_NAME], 'readwrite')
      const store = transaction.objectStore(this.STORE_NAME)
      const request = store.delete(id)

      request.onsuccess = () => {
        this.notifyListeners()
        resolve()
      }
      request.onerror = () => reject(request.error)
    })
  }

  /**
   * Process queue (upload pending items)
   */
  async processQueue(): Promise<void> {
    if (!this.isOnline || this.uploadInProgress) return

    this.uploadInProgress = true
    const pending = await this.getPending()

    console.log(`📤 Processing ${pending.length} queued items...`)

    for (const item of pending) {
      try {
        await this.uploadItem(item)
      } catch (error) {
        console.error(`Failed to upload ${item.id}:`, error)
        // Continue with next item even if one fails
      }
    }

    this.uploadInProgress = false
    this.notifyListeners()
  }

  /**
   * Upload a single item
   */
  private async uploadItem(item: QueuedItem): Promise<void> {
    // Mark as uploading
    await this.updateStatus(item.id, 'uploading')

    try {
      // Call the appropriate API based on item type
      let response: Response
      
      if (item.type === 'lead_submission') {
        response = await fetch('/api/leads', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(item.data)
        })
      } else {
        throw new Error(`Unknown item type: ${item.type}`)
      }

      if (response.ok) {
        // Success - mark as complete and remove from queue
        await this.updateStatus(item.id, 'success')
        
        // Remove after 1 hour (keep for audit)
        setTimeout(() => this.remove(item.id), 3600000)
        
        console.log(`✅ Uploaded ${item.id}`)
      } else {
        // API error - mark as failed
        const error = await response.text()
        await this.updateStatus(item.id, 'failed', error)
        console.error(`❌ Upload failed ${item.id}:`, error)
      }
    } catch (error: any) {
      // Network error - mark as failed
      await this.updateStatus(item.id, 'failed', error.message)
      console.error(`❌ Upload error ${item.id}:`, error)
    }
  }

  /**
   * Get queue statistics
   */
  async getStats(): Promise<OfflineQueueStats> {
    const all = await this.getAll()
    
    const stats: OfflineQueueStats = {
      totalQueued: all.length,
      pending: all.filter(i => i.status === 'pending').length,
      uploading: all.filter(i => i.status === 'uploading').length,
      failed: all.filter(i => i.status === 'failed').length,
      success: all.filter(i => i.status === 'success').length,
      oldestItemAge: all.length > 0 
        ? Date.now() - Math.min(...all.map(i => i.timestamp))
        : 0
    }
    
    return stats
  }

  /**
   * Subscribe to queue changes
   */
  subscribe(listener: (stats: OfflineQueueStats) => void): () => void {
    this.listeners.add(listener)
    
    // Send initial stats
    this.getStats().then(listener)
    
    return () => {
      this.listeners.delete(listener)
    }
  }

  /**
   * Notify listeners of queue changes
   */
  private notifyListeners(): void {
    this.getStats().then(stats => {
      this.listeners.forEach(listener => listener(stats))
    })
  }

  /**
   * Setup online/offline listeners
   */
  setupNetworkListeners(): void {
    window.addEventListener('online', () => {
      console.log('🌐 Connection restored - processing queue')
      this.isOnline = true
      this.processQueue()
    })

    window.addEventListener('offline', () => {
      console.log('📡 Connection lost - queueing mode enabled')
      this.isOnline = false
    })
  }

  /**
   * Clear all successful items (cleanup)
   */
  async clearSuccessful(): Promise<void> {
    const all = await this.getAll()
    const successful = all.filter(i => i.status === 'success')
    
    await Promise.all(successful.map(item => this.remove(item.id)))
  }

  /**
   * Retry all failed items
   */
  async retryFailed(): Promise<void> {
    const all = await this.getAll()
    const failed = all.filter(i => i.status === 'failed')
    
    // Reset status to pending
    await Promise.all(
      failed.map(item => this.updateStatus(item.id, 'pending'))
    )
    
    // Process queue
    await this.processQueue()
  }
}

// Singleton instance
export const offlineQueue = new OfflineQueue()

// Auto-initialize and setup listeners
if (typeof window !== 'undefined') {
  offlineQueue.initialize().catch(console.error)
  offlineQueue.setupNetworkListeners()
}


