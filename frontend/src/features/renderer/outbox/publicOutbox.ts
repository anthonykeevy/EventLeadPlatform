import type { PublicOutboxItem } from '../types/publicSubmission.types'
import { submitPublicFormSubmission } from '../api/publicSubmissionApi'
import { shouldAttemptOutboxItem } from './publicOutboxRetry'

const DB_NAME = 'eventlead_public_outbox'
const DB_VERSION = 1
const STORE_NAME = 'publicOutbox'
const INDEX_STATUS = 'status'
const INDEX_CREATED_AT = 'createdAt'
const INDEX_TOKEN = 'token'

let dbPromise: Promise<IDBDatabase> | null = null
let isProcessorRunning = false
let onlineListenerAttached = false

function requestToPromise<T>(request: IDBRequest<T>): Promise<T> {
  return new Promise((resolve, reject) => {
    request.onsuccess = () => resolve(request.result)
    request.onerror = () => reject(request.error ?? new Error('IndexedDB request failed.'))
  })
}

function transactionToPromise(transaction: IDBTransaction): Promise<void> {
  return new Promise((resolve, reject) => {
    transaction.oncomplete = () => resolve()
    transaction.onerror = () =>
      reject(transaction.error ?? new Error('IndexedDB transaction failed.'))
    transaction.onabort = () =>
      reject(transaction.error ?? new Error('IndexedDB transaction aborted.'))
  })
}

function ensureIndexedDbAvailable(): void {
  if (typeof indexedDB === 'undefined') {
    throw new Error('IndexedDB is not available in this environment.')
  }
}

export function openPublicOutboxDb(): Promise<IDBDatabase> {
  ensureIndexedDbAvailable()

  if (dbPromise) {
    return dbPromise
  }

  dbPromise = new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION)

    request.onupgradeneeded = () => {
      const db = request.result
      const store = db.objectStoreNames.contains(STORE_NAME)
        ? request.transaction?.objectStore(STORE_NAME)
        : db.createObjectStore(STORE_NAME, { keyPath: 'outboxItemId' })

      if (store) {
        if (!store.indexNames.contains(INDEX_STATUS)) {
          store.createIndex(INDEX_STATUS, 'status', { unique: false })
        }
        if (!store.indexNames.contains(INDEX_CREATED_AT)) {
          store.createIndex(INDEX_CREATED_AT, 'createdAt', { unique: false })
        }
        if (!store.indexNames.contains(INDEX_TOKEN)) {
          store.createIndex(INDEX_TOKEN, 'token', { unique: false })
        }
      }
    }

    request.onsuccess = () => resolve(request.result)
    request.onerror = () =>
      reject(request.error ?? new Error('Failed to open IndexedDB.'))
  })

  return dbPromise
}

async function withStore<T>(
  mode: IDBTransactionMode,
  handler: (store: IDBObjectStore) => IDBRequest<T> | void,
): Promise<T | void> {
  const db = await openPublicOutboxDb()
  const transaction = db.transaction(STORE_NAME, mode)
  const store = transaction.objectStore(STORE_NAME)
  const request = handler(store)

  if (request) {
    const result = await requestToPromise(request)
    await transactionToPromise(transaction)
    return result
  }

  await transactionToPromise(transaction)
  return undefined
}

export async function enqueuePublicOutboxItem(item: PublicOutboxItem): Promise<void> {
  await withStore('readwrite', (store) => store.add(item))
}

export async function getPublicOutboxItem(
  outboxItemId: string,
): Promise<PublicOutboxItem | undefined> {
  const item = await withStore('readonly', (store) => store.get(outboxItemId))
  return item as PublicOutboxItem | undefined
}

export async function listPublicOutboxItems(): Promise<PublicOutboxItem[]> {
  const items = await withStore('readonly', (store) => store.getAll())
  return (items as PublicOutboxItem[]) ?? []
}

export async function listPendingOrFailedPublicOutboxItems(): Promise<PublicOutboxItem[]> {
  const items = await listPublicOutboxItems()
  return items.filter((item) => item.status === 'pending' || item.status === 'failed')
}

async function updatePublicOutboxItem(
  outboxItemId: string,
  mutate: (item: PublicOutboxItem) => PublicOutboxItem,
): Promise<PublicOutboxItem | null> {
  const existing = await getPublicOutboxItem(outboxItemId)
  if (!existing) {
    return null
  }

  const updated = mutate(existing)
  await withStore('readwrite', (store) => store.put(updated))
  return updated
}

function isBrowserOnline(): boolean {
  if (typeof navigator === 'undefined') return false
  if (typeof navigator.onLine === 'boolean') return navigator.onLine
  return true
}

export async function processPublicOutbox(): Promise<void> {
  if (isProcessorRunning) return
  if (!isBrowserOnline()) return

  isProcessorRunning = true

  try {
    const items = await listPendingOrFailedPublicOutboxItems()
    const nowMs = Date.now()

    for (const item of items) {
      if (!shouldAttemptOutboxItem(nowMs, item)) {
        continue
      }

      await updatePublicOutboxItem(item.outboxItemId, (current) => ({
        ...current,
        status: 'uploading',
      }))

      try {
        await submitPublicFormSubmission(item.token, item.request)
        await updatePublicOutboxItem(item.outboxItemId, (current) => ({
          ...current,
          status: 'success',
          lastError: undefined,
        }))
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Unknown error'
        await updatePublicOutboxItem(item.outboxItemId, (current) => ({
          ...current,
          status: 'failed',
          retryCount: current.retryCount + 1,
          lastError: message,
          lastTriedAt: Date.now(),
        }))
      }
    }
  } finally {
    isProcessorRunning = false
  }
}

export function registerPublicOutboxOnlineHandler(): void {
  if (typeof window === 'undefined') return
  if (onlineListenerAttached) return

  onlineListenerAttached = true
  window.addEventListener('online', () => {
    void processPublicOutbox()
  })
}

export const publicOutboxConfig = {
  dbName: DB_NAME,
  storeName: STORE_NAME,
}
