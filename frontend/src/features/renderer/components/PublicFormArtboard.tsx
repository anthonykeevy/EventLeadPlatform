import React from 'react'
import type { FormComponent, FormDefinition, FormPage, FormValidationContext } from '../../builder/types/builder.types'
import { ComponentRegistry } from '../../builder/registry/ComponentRegistry'
import { validateField } from '../../builder/utils/validationEngine'
import { evaluateRules } from '../../logic-engine/evaluateRules'
import type { ComponentRuntimeState } from '../../logic-engine/types'
import { ComponentErrorBoundary } from './ComponentErrorBoundary'

type ValueMap = Record<string, unknown>
type FieldErrorMap = Record<string, string>

function getDateValueString(
  value: unknown,
  dateParts?: { year?: boolean; month?: boolean; day?: boolean }
): string {
  if (typeof value === 'string') return value
  if (!value || typeof value !== 'object') return ''
  const parts = value as { year?: string; month?: string; day?: string }
  const showYear = dateParts?.year !== false
  const showMonth = dateParts?.month !== false
  const showDay = dateParts?.day !== false
  if (!showYear || !parts.year) return ''
  const month = showMonth ? (parts.month ?? '') : '01'
  const day = showDay ? (parts.day ?? '') : '01'
  if ((showMonth && !month) || (showDay && !day)) return ''
  return `${parts.year}-${month}-${day}`
}

function flattenComponents(list: FormComponent[]): FormComponent[] {
  const out: FormComponent[] = []
  const walk = (items: FormComponent[]) => {
    for (const c of items) {
      out.push(c)
      if (c.children?.length) walk(c.children)
    }
  }
  walk(list)
  return out
}

function sortByPositionStable(a: FormComponent, b: FormComponent): number {
  const ay = a.position?.y ?? 0
  const by = b.position?.y ?? 0
  if (ay !== by) return ay - by
  const ax = a.position?.x ?? 0
  const bx = b.position?.x ?? 0
  if (ax !== bx) return ax - bx
  return a.id.localeCompare(b.id)
}

function getBaseRequired(component: FormComponent): boolean {
  const requiredFromProps = component.props.required
  const requiredFromValidation = (component.props.validation as any)?.required
  return Boolean(requiredFromProps ?? requiredFromValidation ?? false)
}

function selectAuthoredPages(definition: FormDefinition): FormPage[] {
  // CRITICAL: Do not auto-reflow between profiles. Prefer authored desktopPages if present,
  // otherwise use legacy pages.
  if (definition.desktopPages && definition.desktopPages.length > 0) return definition.desktopPages
  return definition.pages ?? []
}

export const PublicFormArtboard: React.FC<{
  definition: FormDefinition
  onSubmissionDeferred?: (payload: any) => void
  /** When true (builder iframe), suppress page chrome like outer borders */
  embed?: boolean
  /** Optional action trigger from query params (validate/reset). */
  action?: string | null
  /** Layout mode for embedding in builder canvas. */
  layoutMode?: 'default' | 'builder'
  /** Optional className for the outer container. */
  containerClassName?: string
  /** Optional style override for the outer container. */
  containerStyle?: React.CSSProperties
}> = ({ definition, onSubmissionDeferred, embed, action, layoutMode = 'default', containerClassName, containerStyle }) => {
  const pages = selectAuthoredPages(definition)
  const page = pages[0]
  
  // Determine background color: prefer page.background.value (if color type), fallback to theme.backgroundColor
  const backgroundColor = React.useMemo(() => {
    if (page?.background?.type === 'color' && page.background.value) {
      return page.background.value
    }
    return definition.theme?.backgroundColor ?? '#ffffff'
  }, [page, definition.theme])

  const components = React.useMemo(() => {
    if (!page) return []
    const flattened = flattenComponents(page.components)
    // Sort by tabOrder first, then by position (for components without tabOrder)
    return flattened.sort((a, b) => {
      const tabOrderA = a.props.tabOrder ?? 999
      const tabOrderB = b.props.tabOrder ?? 999
      if (tabOrderA !== tabOrderB) return tabOrderA - tabOrderB
      return sortByPositionStable(a, b)
    })
  }, [page])

  const componentsById = React.useMemo(() => {
    const map: Record<string, FormComponent> = {}
    for (const c of components) map[c.id] = c
    return map
  }, [components])

  const baseStateById = React.useMemo(() => {
    const base: Record<string, ComponentRuntimeState> = {}
    for (const c of components) {
      // Apply initial state from component props (logic rules can override)
      const initiallyVisible = c.props.initialVisibility !== 'hidden'
      const initiallyEnabled = c.props.initialEnabled !== 'disabled'
      base[c.id] = { 
        visible: initiallyVisible, 
        enabled: initiallyEnabled, 
        required: getBaseRequired(c) 
      }
    }
    return base
  }, [components])

  const rules = definition.logic?.rules ?? []

  const [values, setValues] = React.useState<ValueMap>({})
  const [showValidation, setShowValidation] = React.useState(false)
  const [submitMessage, setSubmitMessage] = React.useState<string | null>(null)
  const inputRefs = React.useRef<Record<string, React.RefObject<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>>>({})

  React.useEffect(() => {
    if (!action) return
    if (action === 'reset') {
      setValues({})
      setShowValidation(false)
      setSubmitMessage(null)
    }
    if (action === 'validate') {
      setShowValidation(true)
    }
  }, [action])

  const { stateById, warnings } = React.useMemo(() => {
    return evaluateRules({
      rules,
      valuesByComponentId: values,
      componentsById,
      baseStateById,
    })
  }, [rules, values, componentsById, baseStateById])

  // Validation messages for all validation criteria (non-required)
  const validationMessages: FieldErrorMap = React.useMemo(() => {
    const next: FieldErrorMap = {}
    for (const c of components) {
      const runtime = stateById[c.id]
      if (!runtime?.visible) continue

      const validation = c.props.validation
      if (!validation) continue

      // Skip selection/structural components here; required handling is in the form-level pass.
      if (c.type === 'dropdown' || c.type === 'radio' || c.type === 'checkbox' || c.type === 'terms' || c.type === 'submit-button' || c.type === 'divider') {
        continue
      }

      const effectiveRules = { ...validation, required: false }
      let valueForValidation: unknown = values[c.id]
      let componentType = c.type

      if (c.type === 'date') {
        const dateValue = getDateValueString(values[c.id], c.props.dateParts)
        if (dateValue.length === 0) continue
        valueForValidation = dateValue
        componentType = 'date'
      }

      const result = validateField(valueForValidation, effectiveRules, componentType, {
        dateFormat: c.props?.dateFormat,
      })
      if (!result.isValid && result.errors.length > 0) {
        const customMessage = c.props.validationMessage || validation.customError
        next[c.id] = customMessage || result.errors[0].message
      }
    }
    return next
  }, [components, stateById, values])

  const computeErrors = React.useCallback((includeRequired: boolean) => {
    if (!includeRequired) return {}
    const next: FieldErrorMap = { ...validationMessages }
    for (const c of components) {
      const runtime = stateById[c.id]
      if (!runtime?.visible) continue
      if (!runtime?.required) continue
      const v = values[c.id]
      const isDate = c.type === 'date'
      const isEmpty =
        v === null ||
        v === undefined ||
        (typeof v === 'string' && v.trim().length === 0) ||
        (Array.isArray(v) && v.length === 0) ||
        (isDate && getDateValueString(v, c.props.dateParts).length === 0)
      if (isEmpty) next[c.id] = 'This field is required.'
    }
    return next
  }, [components, stateById, values, validationMessages])

  const errors: FieldErrorMap = React.useMemo(() => {
    if (!showValidation) return {}
    return computeErrors(true)
  }, [showValidation, computeErrors])

  const isValid = Object.keys(errors).length === 0

  // Build form-level validation context for submit button
  const formValidationContext: FormValidationContext = React.useMemo(() => {
    const errorsByPriority: FormValidationContext['errorsByPriority'] = []
    
    // Collect all errors with their tabOrder and label
    for (const [componentId, error] of Object.entries(errors)) {
      const component = componentsById[componentId]
      const tabOrder = component?.props.tabOrder ?? 9999
      const label = component?.props.label ?? 'Field'
      errorsByPriority.push({ componentId, error, tabOrder, label })
    }
    
    // Sort by tabOrder
    errorsByPriority.sort((a, b) => a.tabOrder - b.tabOrder)
    
    // Build user-friendly summary message
    let firstError: string | undefined
    if (errorsByPriority.length === 1) {
      firstError = '1 field needs attention'
    } else if (errorsByPriority.length > 1) {
      firstError = `${errorsByPriority.length} fields need attention`
    }
    
    return {
      errors,
      errorsByPriority,
      firstError,
      errorCount: errorsByPriority.length,
    }
  }, [errors, componentsById])

  const getInputRef = React.useCallback((componentId: string) => {
    if (!inputRefs.current[componentId]) {
      inputRefs.current[componentId] = React.createRef<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>()
    }
    return inputRefs.current[componentId]
  }, [])

  React.useEffect(() => {
    if (!showValidation) return
    const firstErrorComponentId = formValidationContext.errorsByPriority[0]?.componentId
    if (!firstErrorComponentId) return
    const ref = inputRefs.current[firstErrorComponentId]
    if (!ref?.current) return
    // Focus after DOM updates to ensure the element is ready.
    setTimeout(() => {
      ref.current?.focus()
    }, 0)
  }, [showValidation, formValidationContext.errorsByPriority])

  const setValue = (id: string, v: unknown) => {
    setValues(prev => ({ ...prev, [id]: v }))
  }

  const onSubmit = () => {
    const nextErrors = computeErrors(true)
    setShowValidation(true)
    setSubmitMessage(null)
    if (Object.keys(nextErrors).length > 0) return
    const payload = {
      formId: definition.formId,
      submittedAtClient: new Date().toISOString(),
      answersByComponentId: values,
    }
    setSubmitMessage('Client-side validation passed. Submission transport/outbox is deferred to Story 3.10.')
    onSubmissionDeferred?.(payload)
  }

  const canvasWidth = definition.canvasSettings?.width ?? 1024
  const canvasHeight = definition.canvasSettings?.height ?? 768

  const containerRef = React.useRef<HTMLDivElement | null>(null)
  const [scale, setScale] = React.useState<number>(1)
  const firstInputRef = React.useRef<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement | null>(null)
  
  // Get primary color for focus styling
  const primaryColor = definition.theme?.primaryColor ?? definition.globalStyles?.primaryColor ?? '#0055FF'
  
  // Set initial focus on component with tabOrder: 1
  React.useEffect(() => {
    if (firstInputRef.current) {
      // Small delay to ensure DOM is ready
      setTimeout(() => {
        firstInputRef.current?.focus()
      }, 100)
    }
  }, [components])

  React.useEffect(() => {
    const el = containerRef.current
    if (!el) return

    const compute = () => {
      const rect = el.getBoundingClientRect()
      const padding = 24
      const maxW = Math.max(0, rect.width - padding)
      const maxH = Math.max(0, rect.height - padding)
      const next = Math.min(1, maxW / canvasWidth, maxH / canvasHeight)
      setScale(Number.isFinite(next) && next > 0 ? next : 1)
    }

    compute()
    const ro = new ResizeObserver(() => compute())
    ro.observe(el)
    return () => ro.disconnect()
  }, [canvasWidth, canvasHeight])

  const outerStyle = containerStyle ?? { height: 'calc(100vh - 64px)' }
  const isBuilderLayout = layoutMode === 'builder'
  const outerClasses = isBuilderLayout
    ? `w-full h-full bg-gray-200 relative ${containerClassName ?? ''}`.trim()
    : `w-full ${containerClassName ?? ''}`.trim()

  return (
    <div ref={containerRef} className={outerClasses} style={outerStyle}>
      <div className={isBuilderLayout ? 'h-full w-full flex items-center justify-center p-8' : 'h-full overflow-auto p-4'}>
        {!isBuilderLayout && warnings.length > 0 && (
          <div className="mb-4 rounded border border-yellow-200 bg-yellow-50 p-3 text-sm text-yellow-900">
            <div className="font-medium">Warnings</div>
            <ul className="list-disc pl-5 mt-1">
              {warnings.map(w => (
                <li key={`${w.ruleId}-${w.code}-${w.sourceComponentId ?? ''}-${w.targetComponentId ?? ''}`}>{w.message}</li>
              ))}
            </ul>
          </div>
        )}

        {!isBuilderLayout && !definition.canvasSettings && (
          <div className="mb-4 rounded border border-blue-200 bg-blue-50 p-3 text-sm text-blue-900">
            Canvas settings missing in definition; rendering with fallback dimensions.
          </div>
        )}

        {!isBuilderLayout && submitMessage && (
          <div className="mb-4 rounded border border-green-200 bg-green-50 p-3 text-sm text-green-900">
            {submitMessage}
          </div>
        )}

        <div
          className={embed ? 'mx-auto bg-white shadow-sm' : 'mx-auto bg-white shadow-sm border border-gray-200'}
          style={{
            width: canvasWidth * scale,
            height: canvasHeight * scale,
          }}
        >
          <div
            style={{
              width: canvasWidth,
              height: canvasHeight,
              transform: `scale(${scale})`,
              transformOrigin: 'top left',
              position: 'relative',
              backgroundColor: backgroundColor,
              fontFamily: definition.theme?.fontFamily ?? 'Inter',
            }}
          >
            {components.map(c => {
              const runtime = stateById[c.id] ?? { visible: true, enabled: true, required: getBaseRequired(c) }
              if (!runtime.visible) return null

              // Check if component type exists in registry
              const def = ComponentRegistry[c.type]
              if (!def) {
                console.warn(`Component type "${c.type}" not found in ComponentRegistry`)
                return null // Skip rendering unsupported components instead of showing error
              }
              
              const RuntimeComp = def.runtimeComponent
              if (!RuntimeComp) {
                console.warn(`Component type "${c.type}" has no runtimeComponent`)
                return null // Skip rendering components without runtime component
              }

              const left = c.position?.x ?? 0
              const top = c.position?.y ?? 0
              
              // Calculate width: parse from props, apply component scale, match builder logic
              const componentScale = c.props.componentScale ?? 100
              const widthFromProps = c.props.width
              const widthFromStyle = c.style?.width != null ? `${c.style.width}px` : null
              
              // Width parity with Builder Canvas:
              // - If width is authored (props or style), apply it (scaled) so preview/production matches.
              // - If width is NOT authored, do NOT force a default width; allow content/layout to size naturally,
              //   matching the current builder canvas behavior for legacy/unconfigured components.
              let width: string | undefined
              if (widthFromProps || widthFromStyle) {
                // Parse width to pixels (handles "385px", "50%", or raw numbers)
                let baseWidthPx: number
                if (widthFromProps) {
                  if (widthFromProps.endsWith('px')) {
                    baseWidthPx = parseInt(widthFromProps, 10)
                  } else if (widthFromProps.endsWith('%')) {
                    // Convert percentage to pixels based on canvas width
                    const pct = parseInt(widthFromProps, 10)
                    baseWidthPx = Math.round((pct / 100) * canvasWidth)
                  } else {
                    // Try parsing as raw number
                    const parsed = parseInt(widthFromProps, 10)
                    baseWidthPx = Number.isFinite(parsed) ? parsed : 300
                  }
                } else {
                  baseWidthPx = parseInt(widthFromStyle as string, 10)
                }

                // Apply component scale (matches builder behavior)
                const scaledWidthPx = baseWidthPx * (componentScale / 100)
                width = `${scaledWidthPx}px`
              }
              
              const height = c.style?.height != null ? `${c.style.height}px` : undefined

              return (
                <div
                  key={c.id}
                  style={{
                    position: 'absolute',
                    left: `${left}px`,
                    top: `${top}px`,
                    width,
                    height,
                    zIndex: c.style?.zIndex ?? 1,
                  }}
                >
                  <ComponentErrorBoundary
                    fallback={
                      <div className="rounded border border-gray-200 bg-gray-50 p-3 text-sm text-gray-700">
                        Component failed to render safely: <span className="font-mono">{c.type}</span>
                      </div>
                    }
                  >
                    <RuntimeComp
                      component={c}
                      value={values[c.id]}
                      onChange={v => setValue(c.id, v)}
                      disabled={!runtime.enabled}
                      required={runtime.required}
                      error={errors[c.id]}
                      allFormErrors={c.type === 'submit-button' ? errors : undefined}
                      formValidationContext={c.type === 'submit-button' ? formValidationContext : undefined}
                      onSubmit={c.type === 'submit-button' ? onSubmit : undefined}
                      tabIndex={c.props.tabOrder ?? undefined}
                      primaryColor={primaryColor}
                      inputRef={getInputRef(c.id)}
                      styleOverrides={c.props.styleOverrides}
                      globalStyles={definition.globalStyles}
                      layout={c.props.layout}
                    />
                  </ComponentErrorBoundary>
                </div>
              )
            })}
          </div>
        </div>
      </div>

      {isBuilderLayout && (
        <div className="absolute left-6 bottom-6 flex items-center gap-2">
          <button className="btn-secondary text-sm" onClick={() => setShowValidation(true)}>
            Validate
          </button>
          <button
            className="btn-secondary text-sm"
            onClick={() => {
              setValues({})
              setShowValidation(false)
              setSubmitMessage(null)
            }}
          >
            Reset
          </button>
        </div>
      )}
    </div>
  )
}

