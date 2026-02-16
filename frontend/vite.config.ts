import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      // Bypass libphonenumber-js package exports (subpath not in exports map)
      'libphonenumber-js/mobile/examples/examples.mobile.json': path.resolve(
        __dirname,
        'node_modules/libphonenumber-js/mobile/examples/examples.mobile.json'
      ),
    },
  },
  server: {
    port: 3000,
    allowedHosts: [
      'localhost',
      '127.0.0.1',
      '.signalplatforms.io',
      'dev.signalplatforms.io',
    ],
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
})

