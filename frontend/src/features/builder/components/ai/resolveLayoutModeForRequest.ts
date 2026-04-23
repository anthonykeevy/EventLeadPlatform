/**
 * Story 6.3.1 (UAT round 6) — re-export shim.
 *
 * The actual implementation moved to ``builder/utils/layoutMode.ts`` so
 * renderer code can import the helpers without taking a structural
 * dependency on the AI panel folder. This file is kept so callers that
 * already import from ``components/ai/resolveLayoutModeForRequest`` (the
 * AI panel itself + its existing test) keep working without churn.
 */
export {
  HORIZONTAL_LAYOUT_MIN_WIDTH_PX,
  applyMobileLayoutDowngrade,
  resolveLayoutModeForRequest,
} from "../../utils/layoutMode";
export type { LayoutModeDecision } from "../../utils/layoutMode";
