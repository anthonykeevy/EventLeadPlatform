/// <reference types="vite/client" />

interface Window {
  unsavedWorkTracker?: unknown;
  offlineQueue?: unknown;
}

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
  readonly VITE_APP_NAME: string
  readonly VITE_APP_VERSION: string
  readonly VITE_BUILD_SHA?: string
  readonly VITE_ENABLE_DEV_LOGS?: string
  readonly VITE_LOG_VERBOSE_RESIZE?: string
  readonly VITE_LOG_PERSIST_TO_STORAGE?: string
  readonly VITE_LOG_SEND_TO_BACKEND?: string
  // Add more env variables as needed
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

