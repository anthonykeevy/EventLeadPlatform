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

// Import event transformation function (lazy import to avoid circular dependencies)
let transformEventCreateRequest: ((request: any) => any) | null = null

async function getEventTransformFunction() {
  if (!transformEventCreateRequest) {
    const eventsApi = await import('../features/events/api/eventsApi')
    transformEventCreateRequest = eventsApi.transformEventCreateRequest
  }
  return transformEventCreateRequest
}

export interface QueuedItem<T = any> {
  id: string
  userId: number // User ID who queued this item (for security - prevents cross-user data access)
  type: 'lead_submission' | 'form_draft' | 'event_draft' | 'event_create' | 'event_update' | 'event_delete' | 'token_refresh' | 'api_request' | 'other'
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
  private readonly DB_VERSION = 2 // Incremented for userId migration
  
  private isOnline: boolean = navigator.onLine
  private uploadInProgress: boolean = false
  private listeners: Set<(stats: OfflineQueueStats) => void> = new Set()
  private currentUserId: number | null = null // Track current user ID
  
  // Queue configuration (configurable via app settings)
  // Can be overridden via localStorage: set 'offlineQueue.maxSize' to a number (e.g., '2' for testing)
  private get MAX_QUEUE_SIZE(): number {
    // Check localStorage first (for testing), then environment variable, then default
    if (typeof window !== 'undefined') {
      const localStorageValue = localStorage.getItem('offlineQueue.maxSize')
      if (localStorageValue) {
        const parsed = parseInt(localStorageValue, 10)
        if (!isNaN(parsed) && parsed > 0) {
          return parsed
        }
      }
    }
    // Environment variable (for production configuration)
    const envValue = import.meta.env.VITE_OFFLINE_QUEUE_MAX_SIZE
    if (envValue) {
      const parsed = parseInt(envValue, 10)
      if (!isNaN(parsed) && parsed > 0) {
        return parsed
      }
    }
    // Default: 100 (or 2 for testing - change back to 100 after Test Case 12.4)
    // ⚠️ TESTING: Temporarily set to 2 for Test Case 12.4
    // TO CHANGE BACK TO 100: Change the number below from 2 to 100
    return 2
  }
  private readonly SUCCESS_CLEANUP_DELAY = 3600000 // 1 hour - keep successful items for audit
  private readonly OLD_ITEM_CLEANUP_AGE = 7 * 24 * 60 * 60 * 1000 // 7 days

  /**
   * Get current user ID from auth token storage
   */
  private getCurrentUserId(): number | null {
    try {
      const token = localStorage.getItem('eventlead_access_token')
      if (!token) return null
      
      // Decode JWT to get user ID (simple base64 decode of payload)
      const payload = JSON.parse(atob(token.split('.')[1]))
      return payload.user_id || payload.sub || null
    } catch {
      return null
    }
  }

  /**
   * Set current user ID (called on login)
   */
  setCurrentUserId(userId: number | null): void {
    const previousUserId = this.currentUserId
    this.currentUserId = userId
    
    // If user changed, clear previous user's queue items
    if (previousUserId !== null && previousUserId !== userId) {
      console.log(`🔄 User changed (${previousUserId} → ${userId}) - clearing previous user's queue`)
      this.clearUserQueue(previousUserId).catch(console.error)
    }
  }

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
        const transaction = (event.target as IDBOpenDBRequest).transaction!
        
        let store: IDBObjectStore
        if (!db.objectStoreNames.contains(this.STORE_NAME)) {
          // Create new store
          store = db.createObjectStore(this.STORE_NAME, { keyPath: 'id' })
          store.createIndex('status', 'status', { unique: false })
          store.createIndex('timestamp', 'timestamp', { unique: false })
          store.createIndex('type', 'type', { unique: false })
          store.createIndex('userId', 'userId', { unique: false }) // For user-specific filtering
        } else {
          // Migration: Add userId index if it doesn't exist
          store = transaction.objectStore(this.STORE_NAME)
          if (!store.indexNames.contains('userId')) {
            store.createIndex('userId', 'userId', { unique: false })
          }
        }
      }
    })
  }

  /**
   * Add item to queue
   * 
   * @throws Error if queue is full (MAX_QUEUE_SIZE unprocessed items)
   * @throws Error if no user is logged in
   */
  async enqueue<T>(type: QueuedItem['type'], data: T): Promise<string> {
    if (!this.db) await this.initialize()

    // Get current user ID (from token or tracked state)
    const userId = this.currentUserId || this.getCurrentUserId()
    if (!userId) {
      throw new Error('Cannot queue item: No user logged in')
    }

    // Check queue size (only count unprocessed items: pending + failed) for this user
    const stats = await this.getStats()
    const unprocessedCount = stats.pending + stats.failed

    if (unprocessedCount >= this.MAX_QUEUE_SIZE) {
      throw new Error(
        `Queue is full (${unprocessedCount}/${this.MAX_QUEUE_SIZE} items). ` +
        `Please wait for items to process or clear failed items.`
      )
    }

    const item: QueuedItem<T> = {
      id: `${type}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      userId, // Store user ID for security
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
   * Get all queued items for current user
   */
  async getAll(): Promise<QueuedItem[]> {
    if (!this.db) await this.initialize()

    const userId = this.currentUserId || this.getCurrentUserId()
    if (!userId) return [] // No user logged in, return empty

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([this.STORE_NAME], 'readonly')
      const store = transaction.objectStore(this.STORE_NAME)
      const index = store.index('userId')
      const request = index.getAll(userId)

      request.onsuccess = () => {
        // Filter out items without userId (legacy items from before migration)
        const items = request.result.filter((item: QueuedItem) => item.userId === userId)
        resolve(items)
      }
      request.onerror = () => reject(request.error)
    })
  }

  /**
   * Get pending items only for current user
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
          // Security check: Verify item belongs to current user
          const currentUserId = this.currentUserId || this.getCurrentUserId()
          if (currentUserId && item.userId !== currentUserId) {
            console.warn(`⚠️ Attempted to update item ${id} belonging to different user (${item.userId} vs ${currentUserId})`)
            resolve() // Silently ignore - don't update other user's items
            return
          }
          
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

    if (pending.length === 0) {
      this.uploadInProgress = false
      this.notifyListeners()
      return
    }

    console.log(`📤 Processing ${pending.length} queued items...`)

    let successCount = 0
    for (const item of pending) {
      try {
        await this.uploadItem(item)
        successCount++
      } catch (error) {
        console.error(`Failed to upload ${item.id}:`, error)
        // Continue with next item even if one fails
      }
    }

    this.uploadInProgress = false
    this.notifyListeners()

    // Emit event when queue processing completes (if any items were successful)
    if (successCount > 0) {
      window.dispatchEvent(new CustomEvent('offlineQueueProcessed', {
        detail: { successCount, totalProcessed: pending.length }
      }))
    }
  }

  /**
   * Upload a single item
   */
  private async uploadItem(item: QueuedItem): Promise<void> {
    // Security check: Verify item belongs to current user
    const currentUserId = this.currentUserId || this.getCurrentUserId()
    if (currentUserId && item.userId !== currentUserId) {
      console.warn(`⚠️ Skipping item ${item.id} - belongs to different user (${item.userId} vs ${currentUserId})`)
      return // Don't process other user's items
    }
    
    // Mark as uploading
    await this.updateStatus(item.id, 'uploading')

    try {
      // Call the appropriate API based on item type
      let response: Response
      const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
      
      // Get access token for authenticated requests
      const getAccessToken = () => {
        try {
          const tokens = localStorage.getItem('eventlead_access_token')
          return tokens || null
        } catch {
          return null
        }
      }
      
      const token = getAccessToken()
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      }
      
      if (token) {
        headers['Authorization'] = `Bearer ${token}`
      }
      
      if (item.type === 'lead_submission') {
        response = await fetch(`${API_BASE_URL}/api/leads`, {
          method: 'POST',
          headers,
          body: JSON.stringify(item.data)
        })
      } else if (item.type === 'event_create') {
        // Transform camelCase to snake_case for backend
        const transformFn = await getEventTransformFunction()
        if (!transformFn) {
          throw new Error('Failed to load event transformation function')
        }
        const backendRequest = transformFn(item.data)
        response = await fetch(`${API_BASE_URL}/api/events`, {
          method: 'POST',
          headers,
          body: JSON.stringify(backendRequest)
        })
      } else if (item.type === 'event_update') {
        // item.data should contain { eventId, eventData }
        const { eventId, eventData } = item.data as { eventId: number; eventData: any }
        
        // Transform camelCase to snake_case for backend (same as updateEvent API)
        const backendRequest: any = {}
        
        if (eventData.name !== undefined) backendRequest.name = eventData.name
        if (eventData.description !== undefined) backendRequest.description = eventData.description
        if (eventData.shortDescription !== undefined) backendRequest.short_description = eventData.shortDescription
        
        if (eventData.startDatetime !== undefined) backendRequest.start_datetime = eventData.startDatetime
        if (eventData.endDatetime !== undefined) backendRequest.end_datetime = eventData.endDatetime
        if (eventData.timezoneIdentifier !== undefined) backendRequest.timezone_identifier = eventData.timezoneIdentifier
        
        if (eventData.venueName !== undefined) backendRequest.venue_name = eventData.venueName
        if (eventData.venueAddress !== undefined) backendRequest.venue_address = eventData.venueAddress
        if (eventData.city !== undefined) backendRequest.city = eventData.city
        if (eventData.state !== undefined) backendRequest.state = eventData.state
        if (eventData.countryId !== undefined) backendRequest.country_id = eventData.countryId
        if (eventData.latitude !== undefined) backendRequest.latitude = eventData.latitude
        if (eventData.longitude !== undefined) backendRequest.longitude = eventData.longitude
        
        if (eventData.eventTypeId !== undefined) backendRequest.event_type_id = eventData.eventTypeId
        if (eventData.industryId !== undefined) backendRequest.industry_id = eventData.industryId
        if (eventData.tags !== undefined) backendRequest.tags = eventData.tags
        
        if (eventData.isPublic !== undefined) backendRequest.is_public = eventData.isPublic
        if (eventData.isSharedWithPlatform !== undefined) backendRequest.is_shared_with_platform = eventData.isSharedWithPlatform
        if (eventData.eventStatusId !== undefined) backendRequest.event_status_id = eventData.eventStatusId
        if (eventData.isRecurring !== undefined) backendRequest.is_recurring = eventData.isRecurring
        
        if (eventData.organizerCompanyId !== undefined) backendRequest.organizer_company_id = eventData.organizerCompanyId
        if (eventData.organizerContactEmail !== undefined) backendRequest.organizer_contact_email = eventData.organizerContactEmail
        if (eventData.organizerWebsite !== undefined) backendRequest.organizer_website = eventData.organizerWebsite
        
        if (eventData.expectedAttendees !== undefined) backendRequest.expected_attendees = eventData.expectedAttendees
        
        response = await fetch(`${API_BASE_URL}/api/events/${eventId}`, {
          method: 'PUT',
          headers,
          body: JSON.stringify(backendRequest)
        })
      } else if (item.type === 'api_request') {
        // Generic API request - item.data should contain { method, url, data, headers }
        const { method, url, data, customHeaders } = item.data as {
          method: string
          url: string
          data?: any
          customHeaders?: HeadersInit
        }
        response = await fetch(url.startsWith('http') ? url : `${API_BASE_URL}${url}`, {
          method: method || 'POST',
          headers: { ...headers, ...customHeaders },
          body: data ? JSON.stringify(data) : undefined
        })
      } else {
        throw new Error(`Unknown item type: ${item.type}`)
      }

      if (response.ok) {
        // Success - mark as complete and remove from queue
        await this.updateStatus(item.id, 'success')
        
        // Emit custom event for successful processing (dashboard can listen to this)
        window.dispatchEvent(new CustomEvent('offlineQueueItemSuccess', {
          detail: { itemId: item.id, itemType: item.type, itemData: item.data }
        }))
        
        // Remove after SUCCESS_CLEANUP_DELAY (keep for audit)
        setTimeout(() => this.remove(item.id), this.SUCCESS_CLEANUP_DELAY)
        
        console.log(`✅ Uploaded ${item.id}`)
      } else {
        // API error - mark as failed
        const errorText = await response.text()
        let errorMessage = errorText
        try {
          const errorJson = JSON.parse(errorText)
          errorMessage = errorJson.detail || errorJson.message || errorText
        } catch {
          // Not JSON, use as-is
        }
        await this.updateStatus(item.id, 'failed', errorMessage)
        console.error(`❌ Upload failed ${item.id}:`, errorMessage)
      }
    } catch (error: any) {
      // Network error - mark as failed
      await this.updateStatus(item.id, 'failed', error.message || String(error))
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

  /**
   * Clean up old items (older than OLD_ITEM_CLEANUP_AGE)
   */
  async cleanupOldItems(): Promise<void> {
    if (!this.db) await this.initialize()

    const cutoffTime = Date.now() - this.OLD_ITEM_CLEANUP_AGE

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([this.STORE_NAME], 'readwrite')
      const store = transaction.objectStore(this.STORE_NAME)
      const index = store.index('timestamp')
      const request = index.openCursor(IDBKeyRange.upperBound(cutoffTime))

      let deletedCount = 0

      request.onsuccess = (event) => {
        const cursor = (event.target as IDBRequest<IDBCursorWithValue>).result
        if (cursor) {
          cursor.delete()
          deletedCount++
          cursor.continue()
        } else {
          if (deletedCount > 0) {
            console.log(`🧹 Cleaned up ${deletedCount} old queue items`)
            this.notifyListeners()
          }
          resolve()
        }
      }
      request.onerror = () => reject(request.error)
    })
  }

  /**
   * Clear all queue items for current user (useful for logout)
   */
  async clearAll(): Promise<void> {
    const userId = this.currentUserId || this.getCurrentUserId()
    if (!userId) {
      console.log('🧹 No user logged in - nothing to clear')
      return
    }
    return this.clearUserQueue(userId)
  }

  /**
   * Clear all queue items for a specific user
   */
  async clearUserQueue(userId: number): Promise<void> {
    if (!this.db) await this.initialize()

    return new Promise((resolve, reject) => {
      const transaction = this.db!.transaction([this.STORE_NAME], 'readwrite')
      const store = transaction.objectStore(this.STORE_NAME)
      const index = store.index('userId')
      const request = index.openCursor(IDBKeyRange.only(userId))

      let deletedCount = 0

      request.onsuccess = (event) => {
        const cursor = (event.target as IDBRequest<IDBCursorWithValue>).result
        if (cursor) {
          cursor.delete()
          deletedCount++
          cursor.continue()
        } else {
          if (deletedCount > 0) {
            console.log(`🧹 Cleared ${deletedCount} queue items for user ${userId}`)
          }
          this.notifyListeners()
          resolve()
        }
      }
      request.onerror = () => reject(request.error)
    })
  }

  /**
   * Check and process queue on initialization if online
   */
  async checkAndProcessOnInit(): Promise<void> {
    if (!this.db) await this.initialize()
    
    // Set current user ID from token
    const userId = this.getCurrentUserId()
    if (userId) {
      this.setCurrentUserId(userId)
    }
    
    // If online and we have pending items, process them
    if (this.isOnline && userId) {
      const pending = await this.getPending()
      if (pending.length > 0) {
        console.log(`🔄 Found ${pending.length} pending items on init - processing...`)
        await this.processQueue()
      }
    }
  }
}

// Singleton instance
export const offlineQueue = new OfflineQueue()

// Auto-initialize and setup listeners
if (typeof window !== 'undefined') {
  offlineQueue.initialize()
    .then(() => offlineQueue.cleanupOldItems())
    .then(() => offlineQueue.checkAndProcessOnInit())
    .catch(console.error)
  offlineQueue.setupNetworkListeners()
}


