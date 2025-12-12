/**
 * Dev-only logger for frontend interactions (no backend).
 * Controlled by VITE_ENABLE_DEV_LOGS and VITE_LOG_VERBOSE_RESIZE.
 * Defaults to no-op when disabled.
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
const MAX_ENTRIES = 500;

const buffer: LogEntry[] = [];

function push(entry: LogEntry) {
  buffer.push(entry);
  if (buffer.length > MAX_ENTRIES) {
    buffer.shift();
  }
}

function log(level: LogLevel, event: string, payload?: Record<string, unknown>) {
  if (!ENABLED) return;
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
  log,
  debug: (event: string, payload?: Record<string, unknown>) => log('debug', event, payload),
  info: (event: string, payload?: Record<string, unknown>) => log('info', event, payload),
  warn: (event: string, payload?: Record<string, unknown>) => log('warn', event, payload),
  error: (event: string, payload?: Record<string, unknown>) => log('error', event, payload),
  getBuffer: () => buffer.slice(),
  clear: () => {
    buffer.length = 0;
  },
  download: () => {
    if (!ENABLED) return;
    const blob = new Blob([JSON.stringify(buffer, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `dev-logs-${new Date().toISOString()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  },
};


