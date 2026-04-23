/**
 * Story 6.3.1 (UAT round 6) — shared layout-mode helpers.
 *
 * Single source of truth for the "horizontal label layout needs a wide
 * canvas" rule. Used in two places:
 *
 *   1. AI request side (``buildRuntimeContext`` in ``AIAgentPanel.tsx``):
 *      decides what ``defaultObjectLayout`` value to *ship* to the LLM /
 *      compiler so the AI plans for a layout that will actually render.
 *
 *   2. Render side (``SortableComponent`` and friends): decides what
 *      ``defaultObjectLayout`` value the canvas should *paint with* for the
 *      active preview mode, without mutating the form's stored Global
 *      Styles. Switching the preview back to Tablet/Desktop reverts
 *      automatically.
 *
 * Lives in ``builder/utils/`` (not under ``components/ai/``) so renderer
 * code can import it without taking a structural dependency on the AI
 * panel folder. The helpers themselves are pure: same inputs always yield
 * the same outputs, no I/O, no DOM access — easy to unit-test.
 */

/**
 * Minimum canvas width (CSS px) at which horizontal label layout is allowed.
 *
 * Chosen at 600 because:
 *   * desktop preview (1920) and tablet preview (~768) stay horizontal;
 *   * mobile preview (375–414) is comfortably below the threshold and
 *     downgrades to vertical;
 *   * leaves headroom for any future "small tablet" preview in the
 *     480–600 band — those would also be too narrow for a 3-column row.
 */
export const HORIZONTAL_LAYOUT_MIN_WIDTH_PX = 600;

export interface LayoutModeDecision {
  /**
   * The value to ship in ``runtimeContext.lockedGlobals.globalStyles
   * .defaultObjectLayout`` for *this generation*. Equal to
   * ``originalLayout`` unless ``downgraded`` is true.
   */
  layout: unknown;
  /** The form's stored ``defaultObjectLayout``, untouched. */
  originalLayout: unknown;
  /**
   * True when ``originalLayout === "horizontal"`` but the active canvas is
   * below ``HORIZONTAL_LAYOUT_MIN_WIDTH_PX`` and we have therefore overridden
   * ``layout`` to ``"vertical"``.
   */
  downgraded: boolean;
}

/**
 * Resolve the per-request layout mode for a Form-AI generation.
 *
 * Returns the form's stored layout unchanged unless we detect the
 * "horizontal layout on a too-narrow canvas" case described above. Any value
 * other than the literal string ``"horizontal"`` is considered "not
 * horizontal" and is returned as-is — we deliberately do NOT canonicalise
 * ``"vertical"`` / ``"mixed"`` / ``undefined``, so the backend continues to
 * see exactly what the form has stored.
 */
export function resolveLayoutModeForRequest(
  storedGlobalStyles: Record<string, unknown> | null | undefined,
  canvasWidth: number
): LayoutModeDecision {
  const originalLayout = storedGlobalStyles?.defaultObjectLayout;
  if (
    originalLayout === "horizontal" &&
    Number.isFinite(canvasWidth) &&
    canvasWidth < HORIZONTAL_LAYOUT_MIN_WIDTH_PX
  ) {
    return {
      layout: "vertical",
      originalLayout,
      downgraded: true,
    };
  }
  return {
    layout: originalLayout,
    originalLayout,
    downgraded: false,
  };
}

/**
 * Story 6.3.1 (UAT round 6) — Phase 1 *completion*: render-time downgrade.
 *
 * Returns a globalStyles object whose ``defaultObjectLayout`` has been
 * forced to ``"vertical"`` if (and only if) the form is configured for
 * horizontal layout AND the active canvas is below
 * ``HORIZONTAL_LAYOUT_MIN_WIDTH_PX``. In every other case, the original
 * reference is returned untouched so React shallow-equality short-circuits
 * downstream re-renders.
 *
 *   * Single source of truth: same constant, same predicate as the AI-side
 *     ``resolveLayoutModeForRequest`` — keeps "what we ask the LLM" and
 *     "what we render" in lockstep.
 *
 *   * Non-mutating: the user's stored Global Styles are never touched, so
 *     switching the preview from Mobile back to Tablet/Desktop reverts to
 *     ``"horizontal"`` automatically with no persistence side-effect.
 *
 *   * Surgical: only ``defaultObjectLayout`` is overridden. Theme, spacing,
 *     fonts, grid layouts and every other Global Style field is preserved
 *     by reference (shallow copy).
 *
 * Call sites pass the *active preview canvas width* (typically
 * ``DEVICE_DIMENSIONS[previewMode].width``), NOT the form's stored
 * ``canvasSettings.width`` — that's what makes the resolver "device-aware":
 * the same form auto-downgrades on Mobile preview and stays horizontal on
 * Tablet/Desktop preview.
 *
 * Generic over the consumer's globalStyles type so each call site keeps
 * its existing typing — the helper just narrows the ``defaultObjectLayout``
 * field.
 */
export function applyMobileLayoutDowngrade<
  T extends { defaultObjectLayout?: unknown } | null | undefined,
>(globalStyles: T, canvasWidth: number): T {
  if (!globalStyles) return globalStyles;
  const originalLayout = globalStyles.defaultObjectLayout;
  if (
    originalLayout === "horizontal" &&
    Number.isFinite(canvasWidth) &&
    canvasWidth < HORIZONTAL_LAYOUT_MIN_WIDTH_PX
  ) {
    return { ...globalStyles, defaultObjectLayout: "vertical" } as T;
  }
  return globalStyles;
}
