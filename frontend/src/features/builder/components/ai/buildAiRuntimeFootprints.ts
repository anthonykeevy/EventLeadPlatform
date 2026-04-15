/**
 * Canvas-faithful component footprints for /api/form-ai/generate runtimeContext.
 * Toolbox tiles use compact surface previews; backend heuristics need builder drop sizing.
 * See story-6.3.md §2.5.
 */

import {
  ComponentRegistry,
  generateComponent,
  type ComponentDefinition,
} from "../../registry/ComponentRegistry";
import type { ComponentType, FormComponent, FormDefinition, GlobalStyles } from "../../types/builder.types";
import { getComponentDimensions } from "../../utils/collisionDetection";

const STORY621_FORCE_INCLUDE: ComponentType[] = ["url", "rating", "paragraph", "file-upload"];

/** Match backend `form_ai` post-process clamp so DOM-measured submits do not inflate spacing. */
const SUBMIT_BUTTON_MAX_FOOTPRINT_HEIGHT = 72;

/**
 * Default planning width for runtime footprints (not full-bleed on wide canvases).
 * LLM and collision math use these; keep aligned with STORY-6.2-AI-CONTEXT-PACK.md.
 */
export function recommendedMaxFootprintWidth(componentType: string, canvasWidth: number): number {
  const w = Math.max(320, canvasWidth);
  if (componentType === "submit-button") return 220;
  if (componentType === "divider") {
    return Math.min(640, Math.max(200, Math.round(w * 0.4)));
  }
  if (componentType === "textarea" || componentType === "address") {
    return Math.min(720, Math.max(360, Math.round(w * 0.52)));
  }
  return Math.min(560, Math.max(280, Math.round(w * 0.48)));
}

function clampFootprintWidth(componentType: string, width: number, canvasWidth: number): number {
  const cap = recommendedMaxFootprintWidth(componentType, canvasWidth);
  return Math.min(Math.max(1, width), cap);
}

export type AiComponentFootprint = {
  componentType: string;
  width: number;
  height: number;
  recommendedGapAfter: number;
};

function parsePositiveNumber(value: unknown, fallback: number): number {
  if (typeof value === "number" && Number.isFinite(value) && value > 0) return value;
  if (typeof value === "string") {
    const normalized = value.trim().toLowerCase().replace(/px$/, "");
    const parsed = Number(normalized);
    if (Number.isFinite(parsed) && parsed > 0) return parsed;
  }
  return fallback;
}

/** Same policy as legacy AIAgentPanel sizing: mirrors “new drop” width/height heuristics on canvas. */
export function estimateConfiguredFootprint(
  component: FormComponent,
  canvasWidth: number
): { width: number; height: number } {
  const style = (component.style ?? {}) as Record<string, unknown>;
  const widthFromStyle = parsePositiveNumber(style.width, 0);
  const heightFromStyle = parsePositiveNumber(style.height, 0);

  const baseHeightByType: Record<string, number> = {
    header: 52,
    divider: 20,
    "submit-button": 64,
    text: 110,
    "first-name": 110,
    email: 110,
    phone: 110,
    number: 110,
    date: 110,
    address: 120,
    dropdown: 120,
    select: 120,
    checkbox: 120,
    radio: 120,
    /** Match form_ai collision floor + context pack (validation band below control). */
    textarea: 200,
    terms: 120,
    url: 110,
    rating: 96,
    paragraph: 88,
    "file-upload": 132,
  };

  const options = Array.isArray(component.props?.options) ? component.props.options : [];
  const optionsGrowth =
    component.type === "checkbox" ||
    component.type === "radio" ||
    component.type === "dropdown" ||
    component.type === "select"
      ? Math.max(0, options.length - 3) * 20
      : 0;

  const minHeight = (baseHeightByType[component.type] ?? 110) + optionsGrowth;
  const estimatedHeight = Math.max(heightFromStyle, minHeight);

  const capW = recommendedMaxFootprintWidth(component.type, canvasWidth);
  let estimatedWidth: number;
  if (component.type === "submit-button") {
    const raw = widthFromStyle > 0 ? widthFromStyle : 220;
    estimatedWidth = Math.min(Math.max(180, raw), 220);
  } else {
    const raw =
      widthFromStyle > 0 ? Math.min(widthFromStyle, capW) : capW;
    estimatedWidth = Math.min(Math.max(240, raw), capW);
  }

  return {
    width: Math.round(estimatedWidth),
    height: Math.round(estimatedHeight),
  };
}

function flattenComponents(definition: FormDefinition): FormComponent[] {
  const pages =
    definition.desktopPages && definition.desktopPages.length > 0
      ? definition.desktopPages
      : definition.pages ?? [];
  const firstPage = pages[0];
  if (!firstPage) return [];

  const collected: FormComponent[] = [];
  const walk = (components: FormComponent[]) => {
    components.forEach((component) => {
      collected.push(component);
      if (component.children && component.children.length > 0) walk(component.children);
    });
  };
  walk(firstPage.components ?? []);
  return collected;
}

function mergeFootprint(
  map: Map<string, AiComponentFootprint>,
  componentType: string,
  width: number,
  height: number,
  canvasWidth: number,
  recommendedGapAfter = 24
): void {
  const wIn = clampFootprintWidth(componentType, width, canvasWidth);
  let h = height;
  if (componentType === "submit-button") {
    h = Math.min(h, SUBMIT_BUTTON_MAX_FOOTPRINT_HEIGHT);
  }
  const existing = map.get(componentType);
  if (!existing) {
    map.set(componentType, {
      componentType,
      width: wIn,
      height: h,
      recommendedGapAfter,
    });
    return;
  }
  const nextH =
    componentType === "submit-button"
      ? Math.min(Math.max(existing.height, h), SUBMIT_BUTTON_MAX_FOOTPRINT_HEIGHT)
      : Math.max(existing.height, h);
  map.set(componentType, {
    componentType,
    width: Math.max(existing.width, wIn),
    height: nextH,
    recommendedGapAfter: Math.max(existing.recommendedGapAfter ?? recommendedGapAfter, recommendedGapAfter),
  });
}

/** Toolbox-eligible types (matches ComponentSidebar init filter + Story 6.2.1 force-include). */
export function getToolboxTypesForAiFootprints(
  initComponentCodes: string[] | null | undefined
): ComponentType[] {
  const defs = Object.values(ComponentRegistry).filter((d): d is ComponentDefinition => Boolean(d));
  const base = defs
    .filter((d) => d.category === "input" || d.category === "display")
    .map((d) => d.type as ComponentType);
  if (!initComponentCodes?.length) return base;
  const force = new Set(STORY621_FORCE_INCLUDE);
  return base.filter((t) => initComponentCodes.includes(t) || force.has(t));
}

export function buildComponentFootprintsForAiRuntime(
  formDefinition: FormDefinition,
  scale: number,
  initComponentCodes: string[] | null | undefined
): AiComponentFootprint[] {
  const canvasWidth = formDefinition.canvasSettings?.width ?? 1920;
  const map = new Map<string, AiComponentFootprint>();

  for (const component of flattenComponents(formDefinition)) {
    const type = component.type?.trim();
    if (!type) continue;

    let width: number;
    let height: number;
    if (typeof document !== "undefined") {
      const el = document.querySelector(`[data-component-id="${component.id}"]`) as HTMLElement | null;
      if (el) {
        const dims = getComponentDimensions(component, el, scale * 100);
        width = Math.max(1, Math.round(dims.width));
        height = Math.max(1, Math.round(dims.height));
      } else {
        const est = estimateConfiguredFootprint(component, canvasWidth);
        width = est.width;
        height = est.height;
      }
    } else {
      const est = estimateConfiguredFootprint(component, canvasWidth);
      width = est.width;
      height = est.height;
    }
    mergeFootprint(map, type, width, height, canvasWidth);
  }

  const globalStyles = formDefinition.globalStyles as GlobalStyles | undefined;
  for (const t of getToolboxTypesForAiFootprints(initComponentCodes)) {
    const synth = generateComponent(t, globalStyles);
    const est = estimateConfiguredFootprint(synth, canvasWidth);
    mergeFootprint(map, t, est.width, est.height, canvasWidth);
  }

  return Array.from(map.values());
}
