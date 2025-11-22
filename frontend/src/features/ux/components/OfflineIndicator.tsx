/**
 * Offline Status Indicator Component
 * 
 * Displays offline status and queue information in the top-right corner.
 * Shows when user is offline or has pending queue items.
 * 
 * Features:
 * - Visual indicator when offline
 * - Queue status (pending items count)
 * - Sync progress indicator
 * - Auto-hides when online and queue empty
 */

import React, { useState, useEffect } from 'react'
import { WifiOff, Wifi, Loader2, CheckCircle2 } from 'lucide-react'
import { offlineQueue, OfflineQueueStats } from '../../../utils/offlineQueue'

export const OfflineIndicator: React.FC = () => {
  const [isOnline, setIsOnline] = useState(navigator.onLine)
  const [queueStats, setQueueStats] = useState<OfflineQueueStats | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)

  useEffect(() => {
    // Subscribe to online/offline events
    const handleOnline = () => {
      setIsOnline(true)
      setIsProcessing(true)
      // Process queue when back online
      offlineQueue.processQueue().finally(() => {
        setIsProcessing(false)
      })
    }

    const handleOffline = () => {
      setIsOnline(false)
      setIsProcessing(false)
    }

    window.addEventListener('online', handleOnline)
    window.addEventListener('offline', handleOffline)

    // Subscribe to queue stats changes
    const unsubscribe = offlineQueue.subscribe((stats) => {
      setQueueStats(stats)
    })

    // Get initial stats
    offlineQueue.getStats().then(setQueueStats)

    return () => {
      window.removeEventListener('online', handleOnline)
      window.removeEventListener('offline', handleOffline)
      unsubscribe()
    }
  }, [])

  // Don't show if online and queue is empty
  if (isOnline && queueStats && queueStats.pending === 0 && queueStats.failed === 0) {
    return null
  }

  const hasPendingItems = queueStats && (queueStats.pending > 0 || queueStats.failed > 0)
  const totalPending = queueStats ? queueStats.pending + queueStats.failed : 0

  return (
    <div
      className={`fixed top-4 right-4 z-[100] flex items-center gap-2 px-4 py-2 rounded-lg shadow-lg transition-all duration-300 ${
        isOnline && isProcessing
          ? 'bg-blue-50 border border-blue-200 text-blue-800'
          : isOnline && hasPendingItems
          ? 'bg-yellow-50 border border-yellow-200 text-yellow-800'
          : 'bg-red-50 border border-red-200 text-red-800'
      }`}
      role="status"
      aria-live="polite"
      aria-label={isOnline ? 'Online with pending items' : 'Offline'}
    >
      {isOnline && isProcessing ? (
        <>
          <Loader2 className="w-4 h-4 animate-spin" />
          <span className="text-sm font-medium">Syncing...</span>
        </>
      ) : isOnline && hasPendingItems ? (
        <>
          <Wifi className="w-4 h-4" />
          <span className="text-sm font-medium">
            {totalPending} {totalPending === 1 ? 'item' : 'items'} pending
          </span>
        </>
      ) : (
        <>
          <WifiOff className="w-4 h-4" />
          <span className="text-sm font-medium">Offline</span>
          {hasPendingItems && (
            <span className="text-xs ml-1">
              ({totalPending} {totalPending === 1 ? 'item' : 'items'} queued)
            </span>
          )}
        </>
      )}
    </div>
  )
}

