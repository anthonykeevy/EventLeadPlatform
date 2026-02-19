/**
 * Form Branding Defaults Page - Story 5.2 T04
 * Company Settings → Form Branding Defaults
 * Uses same controls as Global Properties Panel + Toolbox-style component preview
 */

import React, { useState, useEffect, useCallback, useMemo, useRef } from 'react'
import { useParams } from 'react-router-dom'
import { Save, History, Palette, ChevronDown, ChevronRight, Grid3x3, Focus, Type, Minus } from 'lucide-react'
import {
  getCompanyFormDefaults,
  putCompanyFormDefaults,
  getCompanyFormDefaultsHistory,
  type FormDefaultsPayload,
  type FormDefaultsVersionEntry
} from '../api/formDefaultsApi'
import { useToastNotifications } from '../../ux'
import {
  FocusColorSection,
  TypographySpacingSection,
  DividersLinesSection,
  GridLayoutDefaultsSection
} from '../../builder/components/properties/GlobalStylesPanel'
import { PropertyColorPicker, PropertyNumberInput } from '../../builder/components/properties/inputs'
import { ComponentRegistry } from '../../builder/registry/ComponentRegistry'
import {
  DEFAULT_GLOBAL_STYLES,
  type GlobalStyles
} from '../../builder/types/builder.types'

type AccordionSection = 'theme' | 'focusColor' | 'typographySpacing' | 'dividersLines' | 'gridLayoutDefaults' | 'canvas'

/** Human-readable labels for defaults keys */
const DEFAULTS_LABELS: Record<string, string> = {
  primaryColor: 'Primary colour',
  backgroundColor: 'Background colour',
  fontFamily: 'Font family',
  fontSize: 'Font size',
  labelFontFamily: 'Label font',
  defaultLayout: 'Default layout',
  defaultObjectLayout: 'Object layout',
  rowGap: 'Default row gap',
  columnGap: 'Default column gap',
  width: 'Canvas width',
  height: 'Canvas height',
  gridSize: 'Grid size',
}

function computeChangeSummary(prev: FormDefaultsPayload | null, next: FormDefaultsPayload): string {
  if (!prev || !next) return 'Updated from Company Settings'
  const changed: string[] = []
  const th = next.theme ?? {}
  const ph = prev.theme ?? {}
  if (th.primaryColor !== ph.primaryColor) changed.push(DEFAULTS_LABELS.primaryColor)
  if (th.backgroundColor !== ph.backgroundColor) changed.push(DEFAULTS_LABELS.backgroundColor)
  if (th.fontFamily !== ph.fontFamily) changed.push(DEFAULTS_LABELS.fontFamily)
  const gs = (next.globalStyles ?? {}) as Record<string, unknown>
  const pgs = (prev.globalStyles ?? {}) as Record<string, unknown>
  if (gs.fontSize !== pgs.fontSize) changed.push(DEFAULTS_LABELS.fontSize)
  if (gs.labelFontFamily !== pgs.labelFontFamily) changed.push(DEFAULTS_LABELS.labelFontFamily)
  if (gs.defaultLayout !== pgs.defaultLayout) changed.push(DEFAULTS_LABELS.defaultLayout)
  if (gs.defaultObjectLayout !== pgs.defaultObjectLayout) changed.push(DEFAULTS_LABELS.defaultObjectLayout)
  const dgl = (gs.defaultGridLayout ?? {}) as Record<string, unknown>
  const pdgl = (pgs.defaultGridLayout ?? {}) as Record<string, unknown>
  if (dgl.rowGap !== pdgl.rowGap) changed.push(DEFAULTS_LABELS.rowGap)
  if (dgl.columnGap !== pdgl.columnGap) changed.push(DEFAULTS_LABELS.columnGap)
  const cs = next.canvasSettings ?? {}
  const pcs = prev.canvasSettings ?? {}
  if (cs.width !== pcs.width) changed.push(DEFAULTS_LABELS.width)
  if (cs.height !== pcs.height) changed.push(DEFAULTS_LABELS.height)
  if (cs.gridSize !== pcs.gridSize) changed.push(DEFAULTS_LABELS.gridSize)
  if (changed.length === 0) return 'Updated from Company Settings'
  return changed.join(', ')
}

export function FormBrandingDefaultsPage() {
  const { companyId } = useParams<{ companyId: string }>()
  const toast = useToastNotifications()

  const [defaults, setDefaults] = useState<FormDefaultsPayload | null>(null)
  const lastLoadedDefaults = useRef<FormDefaultsPayload | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [history, setHistory] = useState<FormDefaultsVersionEntry[]>([])
  const [showHistory, setShowHistory] = useState(false)
  const [expandedSection, setExpandedSection] = useState<AccordionSection>('theme')
  const [focusedComponentIndex, setFocusedComponentIndex] = useState(0)

  const id = companyId ? parseInt(companyId, 10) : NaN

  const loadDefaults = useCallback(async () => {
    if (isNaN(id)) return
    setIsLoading(true)
    try {
      const res = await getCompanyFormDefaults(id)
      const d = res.defaults ?? {}
      setDefaults(d)
      lastLoadedDefaults.current = d
    } catch (err) {
      toast.error('Failed to load form defaults', 'Error')
      setDefaults({})
    } finally {
      setIsLoading(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps -- toast causes infinite re-fetch
  }, [id])

  const loadHistory = useCallback(async () => {
    if (isNaN(id)) return
    try {
      const res = await getCompanyFormDefaultsHistory(id)
      setHistory(res.items ?? [])
    } catch {
      setHistory([])
    }
  }, [id])

  useEffect(() => {
    loadDefaults()
  }, [loadDefaults])

  useEffect(() => {
    if (showHistory) loadHistory()
  }, [showHistory, loadHistory])

  const handleSave = async () => {
    if (isNaN(id) || !defaults) return
    const changeSummary = computeChangeSummary(lastLoadedDefaults.current, defaults)
    setIsSaving(true)
    try {
      await putCompanyFormDefaults(id, defaults, changeSummary)
      toast.success('Form branding defaults saved', 'Success')
      loadDefaults()
      if (showHistory) loadHistory()
    } catch (err) {
      toast.error('Failed to save form defaults', 'Error')
    } finally {
      setIsSaving(false)
    }
  }

  const effectiveGlobalStyles = useMemo((): GlobalStyles => {
    const gs = (defaults?.globalStyles ?? {}) as Partial<GlobalStyles>
    const theme = defaults?.theme ?? {}
    const base = gs.baseSpacing ?? 8
    const rowGap = gs.defaultGridLayout?.rowGap
    const derivedGap = rowGap != null ? rowGap / base : undefined
    return {
      ...DEFAULT_GLOBAL_STYLES,
      ...gs,
      primaryColor: (theme.primaryColor as string) ?? gs.primaryColor ?? DEFAULT_GLOBAL_STYLES.primaryColor,
      // When Default Row Gap controls spacing: use grid rowGap only, zero margins to avoid double spacing
      ...(derivedGap != null && {
        labelGap: 0,
        inputHelpGap: 0,
        objectRowGapPx: 0,
      }),
    }
  }, [defaults])

  const onGlobalStylesChange = useCallback((updates: Partial<GlobalStyles>) => {
    setDefaults((prev) => {
      const next = { ...prev } as FormDefaultsPayload
      const gs = { ...(prev?.globalStyles ?? {}), ...updates } as Partial<GlobalStyles>
      // Deep-merge defaultGridLayout to avoid overwriting rows/columns/columnGap
      if (updates.defaultGridLayout) {
        gs.defaultGridLayout = { ...(gs.defaultGridLayout ?? {}), ...updates.defaultGridLayout }
        const rowGap = gs.defaultGridLayout?.rowGap
        if (rowGap != null) {
          // Spacing comes from grid rowGap only; zero margins avoid double spacing between rows
          gs.labelGap = 0
          gs.inputHelpGap = 0
          gs.objectRowGapPx = 0
        }
      }
      // Sync primaryColor to theme
      if (updates.primaryColor != null) {
        next.theme = { ...(prev?.theme ?? {}), primaryColor: updates.primaryColor }
      }
      next.globalStyles = gs
      return next
    })
  }, [])

  const theme = defaults?.theme ?? {}
  const canvas = defaults?.canvasSettings ?? {}

  const updateTheme = (key: string, value: string) => {
    setDefaults((prev) => ({
      ...prev,
      theme: { ...(prev?.theme ?? {}), [key]: value }
    }))
  }

  const updateCanvas = (key: string, value: number) => {
    setDefaults((prev) => ({
      ...prev,
      canvasSettings: { ...(prev?.canvasSettings ?? {}), [key]: value }
    }))
  }

  const allComponents = useMemo(
    () => Object.values(ComponentRegistry).filter((c) => c?.previewComponent),
    []
  )

  // Input components only (have input object) - for Focus Color cycling
  const inputComponents = useMemo(
    () => allComponents.filter((c) => c.category === 'input'),
    [allComponents]
  )

  // When Focus Color section is open, cycle through INPUT components only every 1s
  useEffect(() => {
    if (expandedSection !== 'focusColor' || !inputComponents.length) return
    setFocusedComponentIndex(0)
    const id = setInterval(() => {
      setFocusedComponentIndex((i) => (i + 1) % inputComponents.length)
    }, 1000)
    return () => clearInterval(id)
  }, [expandedSection, inputComponents.length])

  const toggleSection = (section: AccordionSection) => {
    setExpandedSection((prev) => (prev === section ? prev : section))
  }

  if (isNaN(id)) {
    return <div className="p-8 text-red-600">Invalid company ID</div>
  }

  return (
    <div className="h-full flex flex-col overflow-hidden">
      {/* Page toolbar */}
      <div className="flex-shrink-0 flex items-center justify-end gap-2 px-4 py-2 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
        <button
          onClick={() => setShowHistory(!showHistory)}
          className="inline-flex items-center gap-2 px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-800"
        >
          <History className="w-4 h-4" />
          {showHistory ? 'Hide' : 'Show'} History
        </button>
        <button
          onClick={handleSave}
          disabled={isSaving || !defaults}
          className="inline-flex items-center gap-2 px-3 py-1.5 text-sm bg-teal-600 text-white rounded-md hover:bg-teal-700 disabled:opacity-50"
        >
          <Save className="w-4 h-4" />
          {isSaving ? 'Saving...' : 'Save'}
        </button>
      </div>

      {isLoading ? (
        <div className="flex-1 flex items-center justify-center text-gray-500">Loading...</div>
      ) : (
        <div className="flex-1 flex overflow-hidden">
          {/* Left: Accordion controls */}
          <div className="w-[380px] flex-shrink-0 flex flex-col bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 overflow-hidden">
            <div className="flex-1 overflow-y-auto min-h-0">
              {/* Theme accordion */}
              <div className="border-b border-gray-200 dark:border-gray-700">
                <button
                  type="button"
                  onClick={() => toggleSection('theme')}
                  className="w-full flex items-center gap-2 px-4 py-3 text-left hover:bg-gray-50 dark:hover:bg-gray-800"
                >
                  {expandedSection === 'theme' ? (
                    <ChevronDown className="w-4 h-4 text-gray-500" />
                  ) : (
                    <ChevronRight className="w-4 h-4 text-gray-500" />
                  )}
                  <Palette className="w-4 h-4 text-teal-500" />
                  <span className="font-medium text-sm">Theme</span>
                </button>
                {expandedSection === 'theme' && (
                  <div className="px-4 pb-4 pt-0 space-y-3">
                    <p className="text-xs text-gray-500 dark:text-gray-400 -mt-1">
                      Base theme applied across all forms.
                    </p>
                    <PropertyColorPicker
                      label="Background Color"
                      value={(theme.backgroundColor as string) ?? '#FFFFFF'}
                      onChange={(v) => updateTheme('backgroundColor', v)}
                    />
                  </div>
                )}
              </div>

              {/* Focus Color accordion */}
              <div className="border-b border-gray-200 dark:border-gray-700">
                <button
                  type="button"
                  onClick={() => toggleSection('focusColor')}
                  className="w-full flex items-center gap-2 px-4 py-3 text-left hover:bg-gray-50 dark:hover:bg-gray-800"
                >
                  {expandedSection === 'focusColor' ? (
                    <ChevronDown className="w-4 h-4 text-gray-500" />
                  ) : (
                    <ChevronRight className="w-4 h-4 text-gray-500" />
                  )}
                  <Focus className="w-4 h-4 text-blue-500" />
                  <span className="font-medium text-sm">Focus Color</span>
                </button>
                {expandedSection === 'focusColor' && (
                  <FocusColorSection
                    globalStyles={effectiveGlobalStyles}
                    onGlobalStylesChange={onGlobalStylesChange}
                  />
                )}
              </div>

              {/* Typography & Spacing accordion */}
              <div className="border-b border-gray-200 dark:border-gray-700">
                <button
                  type="button"
                  onClick={() => toggleSection('typographySpacing')}
                  className="w-full flex items-center gap-2 px-4 py-3 text-left hover:bg-gray-50 dark:hover:bg-gray-800"
                >
                  {expandedSection === 'typographySpacing' ? (
                    <ChevronDown className="w-4 h-4 text-gray-500" />
                  ) : (
                    <ChevronRight className="w-4 h-4 text-gray-500" />
                  )}
                  <Type className="w-4 h-4 text-gray-500" />
                  <span className="font-medium text-sm">Typography & Spacing</span>
                </button>
                {expandedSection === 'typographySpacing' && (
                  <TypographySpacingSection
                    globalStyles={effectiveGlobalStyles}
                    onGlobalStylesChange={onGlobalStylesChange}
                  />
                )}
              </div>

              {/* Dividers & Lines accordion */}
              <div className="border-b border-gray-200 dark:border-gray-700">
                <button
                  type="button"
                  onClick={() => toggleSection('dividersLines')}
                  className="w-full flex items-center gap-2 px-4 py-3 text-left hover:bg-gray-50 dark:hover:bg-gray-800"
                >
                  {expandedSection === 'dividersLines' ? (
                    <ChevronDown className="w-4 h-4 text-gray-500" />
                  ) : (
                    <ChevronRight className="w-4 h-4 text-gray-500" />
                  )}
                  <Minus className="w-4 h-4 text-gray-500" />
                  <span className="font-medium text-sm">Dividers & Lines</span>
                </button>
                {expandedSection === 'dividersLines' && (
                  <DividersLinesSection
                    globalStyles={effectiveGlobalStyles}
                    onGlobalStylesChange={onGlobalStylesChange}
                  />
                )}
              </div>

              {/* Grid Layout Defaults accordion */}
              <div className="border-b border-gray-200 dark:border-gray-700">
                <button
                  type="button"
                  onClick={() => toggleSection('gridLayoutDefaults')}
                  className="w-full flex items-center gap-2 px-4 py-3 text-left hover:bg-gray-50 dark:hover:bg-gray-800"
                >
                  {expandedSection === 'gridLayoutDefaults' ? (
                    <ChevronDown className="w-4 h-4 text-gray-500" />
                  ) : (
                    <ChevronRight className="w-4 h-4 text-gray-500" />
                  )}
                  <Grid3x3 className="w-4 h-4 text-gray-500" />
                  <span className="font-medium text-sm">Grid Layout Defaults</span>
                </button>
                {expandedSection === 'gridLayoutDefaults' && (
                  <GridLayoutDefaultsSection
                    globalStyles={effectiveGlobalStyles}
                    onGlobalStylesChange={onGlobalStylesChange}
                  />
                )}
              </div>

              {/* Canvas Settings accordion */}
              <div className="border-b border-gray-200 dark:border-gray-700">
                <button
                  type="button"
                  onClick={() => toggleSection('canvas')}
                  className="w-full flex items-center gap-2 px-4 py-3 text-left hover:bg-gray-50 dark:hover:bg-gray-800"
                >
                  {expandedSection === 'canvas' ? (
                    <ChevronDown className="w-4 h-4 text-gray-500" />
                  ) : (
                    <ChevronRight className="w-4 h-4 text-gray-500" />
                  )}
                  <Grid3x3 className="w-4 h-4 text-gray-500" />
                  <span className="font-medium text-sm">Canvas Settings</span>
                </button>
                {expandedSection === 'canvas' && (
                  <div className="px-4 pb-4 pt-0 space-y-3">
                    <p className="text-xs text-gray-500 dark:text-gray-400 -mt-1">
                      Default canvas dimensions for the form builder.
                    </p>
                    <div className="space-y-3">
                      <PropertyNumberInput
                        label="Width"
                        value={(canvas.width as number) ?? 1920}
                        onChange={(v) => updateCanvas('width', v)}
                        min={800}
                        max={3840}
                      />
                      <PropertyNumberInput
                        label="Height"
                        value={(canvas.height as number) ?? 980}
                        onChange={(v) => updateCanvas('height', v)}
                        min={400}
                        max={2160}
                      />
                      <PropertyNumberInput
                        label="Grid Size"
                        value={(canvas.gridSize as number) ?? 8}
                        onChange={(v) => updateCanvas('gridSize', v)}
                        min={4}
                        max={32}
                      />
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Right: Toolbox grid preview */}
          <div className="flex-1 overflow-y-auto bg-white dark:bg-gray-900">
            <div className="p-4 border-b border-gray-100 dark:border-gray-800">
              <h3 className="font-semibold text-gray-700 dark:text-gray-300">Toolbox</h3>
              <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">
                Live preview of all components with current defaults
              </p>
            </div>
            <div
              className="p-4"
              style={{
                backgroundColor: (theme.backgroundColor as string) ?? '#FFFFFF',
                fontFamily: effectiveGlobalStyles.fontFamily ?? 'Inter'
              }}
            >
              <div
                className="grid"
                style={{
                  gridTemplateColumns: `repeat(auto-fill, minmax(${
                    effectiveGlobalStyles.defaultObjectLayout === 'horizontal' ? 420 : 280
                  }px, 1fr))`,
                  gridAutoRows: 'minmax(min-content, auto)',
                  gap: 0
                }}
              >
                {allComponents.map((item) => (
                  <div
                    key={item.type}
                    className="rounded-lg border border-dashed border-gray-300 dark:border-gray-600 p-3 min-w-0"
                  >
                    {React.isValidElement(item.previewComponent)
                      ? React.cloneElement(item.previewComponent as React.ReactElement, {
                          globalStyles: effectiveGlobalStyles,
                          simulateFocus:
                            expandedSection === 'focusColor' &&
                            inputComponents[focusedComponentIndex]?.type === item.type
                        })
                      : item.previewComponent}
                  </div>
                ))}
              </div>
            </div>

            {showHistory && (
              <div className="m-4 p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                  Change History
                </h4>
                <div className="space-y-2 max-h-64 overflow-y-auto">
                  {history.length === 0 ? (
                    <p className="text-sm text-gray-500">No changes yet</p>
                  ) : (
                    history.map((entry) => (
                      <div
                        key={entry.versionNumber}
                        className="flex justify-between items-start gap-2 p-2 rounded bg-gray-50 dark:bg-gray-800 text-sm"
                      >
                        <div>
                          <span className="font-medium">Version {entry.versionNumber}</span>
                          {entry.changeSummary && (
                            <span className="text-gray-600 dark:text-gray-400 ml-2">
                              — {entry.changeSummary}
                            </span>
                          )}
                          <div className="text-xs text-gray-500 mt-0.5">
                            {entry.createdDate
                              ? new Date(entry.createdDate).toLocaleString()
                              : ''}
                            {entry.createdByEmail
                              ? ` • ${entry.createdByEmail}`
                              : entry.createdBy
                                ? ` • User ID ${entry.createdBy}`
                                : ''}
                          </div>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
