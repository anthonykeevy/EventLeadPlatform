/**
 * Theme Feature Index for Epic 2 Story 2.2
 * Exports all theme-related components and utilities
 */

// Context
export { ThemeProvider, useTheme, useThemeState, useThemeActions } from './context/ThemeContext'
export type { ThemeState, ThemeAction, ThemeContextType } from './context/ThemeContext'

// Components
export { default as ThemeSelector } from './components/ThemeSelector'
export { default as DensitySelector } from './components/DensitySelector'
export { default as FontSizeSelector } from './components/FontSizeSelector'

// Pages
export { default as ThemeSettingsPage } from './pages/ThemeSettingsPage'

// Styles
import './styles/theme-variables.css'
