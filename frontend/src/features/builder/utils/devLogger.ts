/**
 * Dev-only logger for frontend interactions (local-first).
 *
 * - Controlled by VITE_ENABLE_DEV_LOGS and VITE_LOG_VERBOSE_RESIZE.
 * - Buffers entries in-memory (FIFO).
 * - Optional persistence to localStorage (off by default):
 *   - Enable with VITE_LOG_PERSIST_TO_STORAGE=true
 * - Download format matches the backend-ready schema:
 *   FrontendLogBatch { entries, sessionId, pageUrl?, browserInfo? }
 *
 * This intentionally does NOT sync to the backend yet (next epic).
 */

type LogLevel = 'debug' | 'info' | 'warn' | 'error';

interface LogEntry {
  ts: number;
  level: LogLevel;
  event: string;
  payload?: Record<string, unknown>;
}

const ENABLED = import.meta.env.VITE_ENABLE_DEV_LOGS === 'true';
const VERBOSE_RESIZE = import.meta.env.VITE_LOG_VERBOSE_RESIZE === 'true';
const PERSIST_TO_STORAGE = import.meta.env.VITE_LOG_PERSIST_TO_STORAGE === 'true';
const MAX_ENTRIES = 500;

// Local storage persistence (optional; no backend sync yet)
const STORAGE_PREFIX = 'eventlead.devLogger';
const STORAGE_SESSIONS_KEY = `${STORAGE_PREFIX}.sessions`;
const STORAGE_SESSION_KEY_PREFIX = `${STORAGE_PREFIX}.session.`;
const SESSION_STORAGE_SESSION_ID_KEY = `${STORAGE_PREFIX}.sessionId`;
const SESSION_STORAGE_CREATED_AT_KEY = `${STORAGE_PREFIX}.createdAt`;

interface FrontendLogBatch {
  entries: LogEntry[];
  sessionId: string;
  pageUrl?: string;
  browserInfo?: string;
  // Extra keys are allowed for local use; backend can ignore them later.
  meta?: Record<string, unknown>;
}

interface StoredSessionIndexEntry {
  sessionId: string;
  createdAt: number;
  updatedAt: number;
  entryCount: number;
  lastEvent?: string;
  pageUrl?: string;
  browserInfo?: string;
}

const buffer: LogEntry[] = [];
let activeSessionId: string | null = null;
let activeSessionCreatedAt: number | null = null;
let persistTimer: number | null = null;

function isBrowser(): boolean {
  return typeof window !== 'undefined' && typeof document !== 'undefined';
}

function safeNow(): number {
  return Date.now();
}

function createSessionId(): string {
  // Keep it URL-safe and backend-friendly.
  try {
    const uuid = (globalThis.crypto as Crypto | undefined)?.randomUUID?.();
    if (uuid) return `sess_${uuid}`;
  } catch {
    // ignore
  }
  return `sess_${safeNow().toString(36)}_${Math.random().toString(36).slice(2, 10)}`;
}

function getOrCreateSessionId(): { sessionId: string; createdAt: number } {
  // If not in a browser context, fall back to a deterministic in-memory id.
  if (!isBrowser()) {
    if (!activeSessionId) {
      activeSessionId = createSessionId();
      activeSessionCreatedAt = safeNow();
    }
    return { sessionId: activeSessionId, createdAt: activeSessionCreatedAt ?? safeNow() };
  }

  if (activeSessionId && activeSessionCreatedAt) {
    return { sessionId: activeSessionId, createdAt: activeSessionCreatedAt };
  }

  const existing = window.sessionStorage.getItem(SESSION_STORAGE_SESSION_ID_KEY);
  const existingCreated = window.sessionStorage.getItem(SESSION_STORAGE_CREATED_AT_KEY);

  const sessionId = existing || createSessionId();
  const createdAt = existingCreated ? Number(existingCreated) : safeNow();

  window.sessionStorage.setItem(SESSION_STORAGE_SESSION_ID_KEY, sessionId);
  window.sessionStorage.setItem(SESSION_STORAGE_CREATED_AT_KEY, String(createdAt));

  activeSessionId = sessionId;
  activeSessionCreatedAt = createdAt;
  return { sessionId, createdAt };
}

function sessionStorageKey(sessionId: string): string {
  return `${STORAGE_SESSION_KEY_PREFIX}${sessionId}`;
}

function getPageUrl(): string | undefined {
  if (!isBrowser()) return undefined;
  try {
    return window.location.href;
  } catch {
    return undefined;
  }
}

function getBrowserInfo(): string | undefined {
  if (!isBrowser()) return undefined;
  try {
    return window.navigator.userAgent;
  } catch {
    return undefined;
  }
}

function toPlainDomRect(value: unknown): Record<string, number> | undefined {
  // DOMRect / DOMRectReadOnly are not reliably JSON-serializable across browsers.
  // Convert to a plain object when we detect it.
  if (!value || typeof value !== 'object') return undefined;
  const v = value as Record<string, number>;
  if (
    typeof v.x === 'number' &&
    typeof v.y === 'number' &&
    typeof v.width === 'number' &&
    typeof v.height === 'number' &&
    typeof v.top === 'number' &&
    typeof v.right === 'number' &&
    typeof v.bottom === 'number' &&
    typeof v.left === 'number'
  ) {
    return {
      x: v.x,
      y: v.y,
      width: v.width,
      height: v.height,
      top: v.top,
      right: v.right,
      bottom: v.bottom,
      left: v.left,
    };
  }
  return undefined;
}

function jsonReplacer(_key: string, value: unknown) {
  if (typeof value === 'bigint') return value.toString();
  if (typeof value === 'number' && !Number.isFinite(value)) return null;

  const rect = toPlainDomRect(value);
  if (rect) return rect;

  if (value instanceof Error) {
    return {
      name: value.name,
      message: value.message,
      stack: value.stack,
    };
  }

  if (value instanceof Map) {
    return Array.from(value.entries());
  }

  if (value instanceof Set) {
    return Array.from(value.values());
  }

  return value;
}

function safeJsonStringify(value: unknown, space: number = 2): string {
  // Handle circular references without throwing.
  const seen = new WeakSet<object>();
  return JSON.stringify(
    value,
    (key, val) => {
      if (val && typeof val === 'object') {
        if (seen.has(val as object)) return '[Circular]';
        seen.add(val as object);
      }
      return jsonReplacer(key, val);
    },
    space
  );
}

function readSessionIndex(): StoredSessionIndexEntry[] {
  if (!isBrowser()) return [];
  try {
    const raw = window.localStorage.getItem(STORAGE_SESSIONS_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? (parsed as StoredSessionIndexEntry[]) : [];
  } catch {
    return [];
  }
}

function writeSessionIndex(entries: StoredSessionIndexEntry[]): void {
  if (!isBrowser()) return;
  try {
    window.localStorage.setItem(STORAGE_SESSIONS_KEY, safeJsonStringify(entries, 0));
  } catch {
    // ignore (quota / disabled storage)
  }
}

function persistCurrentSession(): void {
  if (!ENABLED || !PERSIST_TO_STORAGE || !isBrowser()) return;

  const { sessionId, createdAt } = getOrCreateSessionId();
  const batch: FrontendLogBatch = {
    entries: buffer.slice(),
    sessionId,
    pageUrl: getPageUrl(),
    browserInfo: getBrowserInfo(),
    meta: {
      createdAt,
      updatedAt: safeNow(),
      maxEntries: MAX_ENTRIES,
    },
  };

  // 1) Write session batch
  const key = sessionStorageKey(sessionId);
  try {
    window.localStorage.setItem(key, safeJsonStringify(batch));
  } catch (err) {
    // Best effort: if quota exceeded, drop oldest half and retry once.
    try {
      if (buffer.length > 50) {
        buffer.splice(0, Math.floor(buffer.length / 2));
        const smallerBatch = { ...batch, entries: buffer.slice(), meta: { ...(batch.meta || {}), truncated: true } };
        window.localStorage.setItem(key, safeJsonStringify(smallerBatch));
      }
    } catch {
      // ignore
    }
  }

  // 2) Update session index (keep last 20 sessions)
  const updatedAt = safeNow();
  const index = readSessionIndex();
  const lastEntry = buffer[buffer.length - 1];
  const nextEntry: StoredSessionIndexEntry = {
    sessionId,
    createdAt,
    updatedAt,
    entryCount: buffer.length,
    lastEvent: lastEntry?.event,
    pageUrl: batch.pageUrl,
    browserInfo: batch.browserInfo,
  };

  const without = index.filter((s) => s.sessionId !== sessionId);
  const next = [nextEntry, ...without].sort((a, b) => b.updatedAt - a.updatedAt).slice(0, 20);
  writeSessionIndex(next);
}

function schedulePersist(): void {
  if (!ENABLED || !PERSIST_TO_STORAGE || !isBrowser()) return;
  if (persistTimer !== null) return;
  persistTimer = window.setTimeout(() => {
    persistTimer = null;
    persistCurrentSession();
  }, 750);
}

function loadPersistedSessionIfAny(): void {
  if (!ENABLED || !PERSIST_TO_STORAGE || !isBrowser()) return;
  const { sessionId } = getOrCreateSessionId();
  const key = sessionStorageKey(sessionId);
  try {
    const raw = window.localStorage.getItem(key);
    if (!raw) return;
    const parsed = JSON.parse(raw) as FrontendLogBatch | null;
    const entries = parsed?.entries;
    if (!Array.isArray(entries) || entries.length === 0) return;
    buffer.length = 0;
    // Only keep the most recent MAX_ENTRIES.
    const slice = entries.slice(-MAX_ENTRIES);
    buffer.push(...slice);
  } catch {
    // ignore
  }
}

function push(entry: LogEntry) {
  buffer.push(entry);
  if (buffer.length > MAX_ENTRIES) {
    buffer.shift();
  }
  schedulePersist();
}

function log(level: LogLevel, event: string, payload?: Record<string, unknown>) {
  if (!ENABLED) return;
  // Ensure session exists early, so persisted logs have stable metadata.
  getOrCreateSessionId();
  const entry: LogEntry = { ts: Date.now(), level, event, payload };
  push(entry);

  // Mirror to console in dev for warn/error; optionally for debug/info when verbose is on.
  const shouldConsole =
    level === 'warn' ||
    level === 'error' ||
    (VERBOSE_RESIZE && (level === 'debug' || level === 'info'));

  if (shouldConsole) {
    const msg = `[DEVLOG] ${new Date(entry.ts).toISOString()} ${level.toUpperCase()} ${event}`;
    // eslint-disable-next-line no-console
    console[level === 'debug' ? 'log' : level](msg, payload || {});
  }
}

export const devLogger = {
  isEnabled: () => ENABLED,
  getSessionId: () => (ENABLED ? getOrCreateSessionId().sessionId : null),
  log,
  debug: (event: string, payload?: Record<string, unknown>) => log('debug', event, payload),
  info: (event: string, payload?: Record<string, unknown>) => log('info', event, payload),
  warn: (event: string, payload?: Record<string, unknown>) => log('warn', event, payload),
  error: (event: string, payload?: Record<string, unknown>) => log('error', event, payload),
  getBuffer: () => buffer.slice(),
  clear: () => {
    buffer.length = 0;
    if (!ENABLED || !PERSIST_TO_STORAGE || !isBrowser()) return;
    const sid = getOrCreateSessionId().sessionId;
    try {
      window.localStorage.removeItem(sessionStorageKey(sid));
    } catch {
      // ignore
    }
  },
  download: () => {
    if (!ENABLED) return;
    const { sessionId, createdAt } = getOrCreateSessionId();
    const batch: FrontendLogBatch = {
      entries: buffer.slice(),
      sessionId,
      pageUrl: getPageUrl(),
      browserInfo: getBrowserInfo(),
      meta: {
        createdAt,
        downloadedAt: safeNow(),
        maxEntries: MAX_ENTRIES,
      },
    };
    const blob = new Blob([safeJsonStringify(batch)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `dev-logs-${sessionId}-${new Date().toISOString()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  },
};

// Module init (when enabled): create/load persisted session and expose on window for agent debugging.
if (ENABLED) {
  try {
    getOrCreateSessionId();
    if (PERSIST_TO_STORAGE) {
      loadPersistedSessionIfAny();
      persistCurrentSession();
    }
    if (isBrowser()) {
      (window as unknown as Record<string, unknown>).devLogger = devLogger;
    }
  } catch {
    // ignore
  }
}


