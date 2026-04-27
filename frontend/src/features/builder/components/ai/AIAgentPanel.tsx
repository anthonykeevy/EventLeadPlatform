import React from "react";
import { Sparkles, RefreshCw, Upload } from "lucide-react";

import {
  AiComponentMeasurement,
  AiRuntimeContext,
  AttemptTraceEntry,
  AiGenerationOptions,
  generateAiDefinition,
  OpenAiTransportMode,
  remeasureAiDefinition,
} from "../../api/aiFormGenerationApi";
import { useBuilderStore, selectAuthoredPages } from "../../stores/useBuilderStore";
import { DEVICE_DIMENSIONS, FormComponent, FormDefinition } from "../../types/builder.types";
import { getCompanyTermsAssets } from "../../../dashboard/api/companyAssetsApi";
import { getComponentDimensions } from "../../utils/collisionDetection";
import { devLogger } from "../../utils/devLogger";
import { buildSectionedSystemAddendum } from "./sectionedPromptArchitecture";
import {
  HORIZONTAL_LAYOUT_MIN_WIDTH_PX,
  resolveLayoutModeForRequest,
} from "./resolveLayoutModeForRequest";
import { getPreferences, patchPreferences } from "../../../preferences/api/preferencesApi";

const SUPPRESS_WARNING_KEY = "notifications.ai_agent.suppress_replace_warning";

type GenerationUiStatus =
  | "idle"
  | "generating"
  | "validating"
  | "retrying"
  | "completed"
  | "failed";

const STATUS_LABELS: Record<GenerationUiStatus, string> = {
  idle: "Idle",
  generating: "Generating",
  validating: "Validating",
  retrying: "Retrying",
  completed: "Completed",
  failed: "Failed",
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

function estimateConfiguredFootprint(
  component: FormComponent,
  canvasWidth: number
): { width: number; height: number } {
  const style = (component.style ?? {}) as Record<string, unknown>;
  const widthFromStyle = parsePositiveNumber(style.width, 0);
  const heightFromStyle = parsePositiveNumber(style.height, 0);

  const baseHeightByType: Record<string, number> = {
    header: 52,
    divider: 20,
    "submit-button": 81,
    text: 110,
    email: 110,
    phone: 110,
    number: 110,
    date: 110,
    address: 120,
    dropdown: 120,
    select: 120,
    checkbox: 120,
    radio: 120,
    textarea: 200,
    terms: 120,
  };

  const options = Array.isArray(component.props?.options)
    ? component.props.options
    : [];
  const optionsGrowth =
    component.type === "checkbox" ||
    component.type === "radio" ||
    component.type === "dropdown" ||
    component.type === "select"
      ? Math.max(0, options.length - 3) * 20
      : 0;

  const minHeight = (baseHeightByType[component.type] ?? 110) + optionsGrowth;
  const estimatedHeight = Math.max(heightFromStyle, minHeight);

  const defaultWidth =
    component.type === "submit-button"
      ? 220
      : Math.max(240, canvasWidth - 40);
  const estimatedWidth = Math.max(widthFromStyle, defaultWidth);

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

function getFirstPageComponents(definition: FormDefinition): FormComponent[] {
  const pages =
    definition.desktopPages && definition.desktopPages.length > 0
      ? definition.desktopPages
      : definition.pages ?? [];
  return pages[0]?.components ?? [];
}

function isSingleColumn(components: FormComponent[], gridSize: number): boolean {
  if (components.length < 2) return false;
  const xs = components.map((component) => component.position?.x ?? 0);
  const minX = Math.min(...xs);
  const maxX = Math.max(...xs);
  const tolerance = Math.max(32, gridSize * 2);
  return maxX - minX <= tolerance;
}

async function nextPaint(): Promise<void> {
  await new Promise<void>((resolve) => requestAnimationFrame(() => resolve()));
  await new Promise<void>((resolve) => requestAnimationFrame(() => resolve()));
}

function formatAttemptLine(entry: AttemptTraceEntry): string {
  const v = entry.validation;
  const phaseLabel =
    entry.phase === "initial"
      ? "Attempt 1 (initial)"
      : `Attempt ${entry.attemptNumber} (correction ${entry.attemptNumber - 1})`;
  const delta = entry.collisionDeltaFromPrevious;
  const trend =
    entry.collisionTrendVsPrevious != null &&
    entry.collisionTrendVsPrevious !== "n_a" &&
    delta != null
      ? ` — collisions ${delta < 0 ? "↓" : delta > 0 ? "↑" : "="} (${entry.collisionTrendVsPrevious})`
      : "";
  if (v.valid) {
    return `${phaseLabel}: validation passed${trend}`;
  }
  const bits: string[] = [];
  if (v.collisionCount > 0) bits.push(`${v.collisionCount} collision(s)`);
  if (v.boundaryViolationCount > 0) bits.push(`${v.boundaryViolationCount} boundary`);
  if (v.schemaErrorCount > 0) bits.push(`${v.schemaErrorCount} schema`);
  const detail = bits.length > 0 ? bits.join(", ") : `${v.errorCount} error(s)`;
  const tail = entry.correctionIssued ? " → sent correction to model" : "";
  return `${phaseLabel}: ${detail}${trend}${tail}`;
}

function hashText(value: string): string {
  let hash = 2166136261;
  for (let i = 0; i < value.length; i += 1) {
    hash ^= value.charCodeAt(i);
    hash = Math.imul(hash, 16777619);
  }
  return `h_${(hash >>> 0).toString(16)}`;
}

function findFirstTermsComponent(definition: FormDefinition): FormComponent | null {
  const pages =
    definition.desktopPages && definition.desktopPages.length > 0
      ? definition.desktopPages
      : definition.pages ?? [];
  const firstPage = pages[0];
  if (!firstPage) return null;

  const walk = (components: FormComponent[]): FormComponent | null => {
    for (const component of components) {
      if (component.type === "terms") return component;
      if (component.children && component.children.length > 0) {
        const nested = walk(component.children);
        if (nested) return nested;
      }
    }
    return null;
  };

  return walk(firstPage.components ?? []);
}

export const AIAgentPanel: React.FC = () => {
  const {
    applyValidatedDefinition,
    setAiAgentSettings,
    saveDraft,
    formDefinition,
    formContext,
    scale,
    previewMode,
  } = useBuilderStore();
  const [prompt, setPrompt] = React.useState("");
  const [status, setStatus] = React.useState<GenerationUiStatus>("idle");
  const [message, setMessage] = React.useState<string | null>(null);
  const [traceSummary, setTraceSummary] = React.useState<string | null>(null);
  const [promptSnapshot, setPromptSnapshot] = React.useState<string | null>(null);
  const [attemptLines, setAttemptLines] = React.useState<string[] | null>(null);
  const [isSubmitting, setIsSubmitting] = React.useState(false);
  // Story 6.4 AC-5: transport is locked to "auto"; selector removed.
  const [openaiTransport] = React.useState<OpenAiTransportMode>("auto");
  // Story 6.3.1 UAT round 6 — surfaces the "horizontal-layout-downgraded-to-
  // vertical-because-canvas-is-too-narrow" notice. Set as a side-effect of
  // ``buildRuntimeContext`` and rendered in the panel header. Cleared on each
  // new generate so the notice doesn't stick after the user switches preview
  // mode back to desktop.
  const [layoutDowngradeNotice, setLayoutDowngradeNotice] = React.useState<
    string | null
  >(null);

  // Story 6.4 AC-2/3: replace-form warning modal state
  const [showReplaceWarning, setShowReplaceWarning] = React.useState(false);
  const [dontShowAgain, setDontShowAgain] = React.useState(false);
  const [suppressWarning, setSuppressWarning] = React.useState(false);

  // Holds the AbortController for the in-flight generate + remeasure requests.
  // Aborted on component unmount (user navigates away) and on Cancel button click.
  const abortControllerRef = React.useRef<AbortController | null>(null);

  React.useEffect(() => {
    return () => {
      // Abort any in-flight AI generation when the panel unmounts (navigation away).
      abortControllerRef.current?.abort();
    };
  }, []);

  // Story 6.4 AC-1: hydrate prompt from DB-backed lastPrompt on mount
  const promptHydratedRef = React.useRef(false);
  React.useEffect(() => {
    if (promptHydratedRef.current) return;
    const lastPrompt = formDefinition?.aiAgentSettings?.lastPrompt;
    if (lastPrompt) {
      setPrompt(lastPrompt);
      promptHydratedRef.current = true;
    } else if (formDefinition) {
      // formDefinition loaded but no lastPrompt — mark as hydrated so we don't
      // overwrite if user types before formDefinition resolves
      promptHydratedRef.current = true;
    }
  }, [formDefinition]);

  // Story 6.4 AC-3: load suppress-warning preference on mount
  React.useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const prefs = await getPreferences();
        if (cancelled) return;
        for (const cat of prefs.categories) {
          for (const entry of cat.entries) {
            if (entry.preferenceKey === SUPPRESS_WARNING_KEY) {
              setSuppressWarning(entry.value === "true");
              return;
            }
          }
        }
      } catch {
        // Preference load failure is non-blocking; default to show warning
      }
    })();
    return () => { cancelled = true; };
  }, []);

  const buildRuntimeContext = React.useCallback(async (): Promise<AiRuntimeContext | undefined> => {
    if (!formDefinition) return undefined;
    // Story 6.3.1 UAT round 3 — compile against the device tab the user is
    // actively previewing (desktop / tablet / mobile). Previously we always
    // sent the desktop canvas (1920x980), which is why "switch to mobile and
    // re-run the prompt" produced a desktop layout that overflowed the mobile
    // viewport. The compiler will pin x to MARGIN_X, shrink columns to fit,
    // and grow canvas height vertically as needed.
    const deviceDim = DEVICE_DIMENSIONS[previewMode];
    const canvasWidth = deviceDim.width;
    const canvasHeight = deviceDim.height;

    const nodes = Array.from(
      document.querySelectorAll<HTMLElement>("[data-toolbox-component-type]")
    );
    const toolboxFootprints = nodes
      .map((node) => {
        const componentType = node.dataset.toolboxComponentType?.trim();
        if (!componentType) return null;
        const bounds = node.getBoundingClientRect();
        if (!Number.isFinite(bounds.width) || !Number.isFinite(bounds.height)) return null;
        if (bounds.width <= 0 || bounds.height <= 0) return null;
        return {
          componentType,
          width: Math.round(bounds.width),
          height: Math.round(bounds.height),
          recommendedGapAfter: 24,
        };
      })
      .filter((item): item is NonNullable<typeof item> => item !== null);

    const mergedFootprints = new Map<
      string,
      { width: number; height: number; recommendedGapAfter: number }
    >();

    toolboxFootprints.forEach((footprint) => {
      mergedFootprints.set(footprint.componentType, footprint);
    });

    flattenComponents(formDefinition).forEach((component) => {
      const type = component.type?.trim();
      if (!type) return;
      const existing = mergedFootprints.get(type);
      if (existing) {
        // Keep toolbox rendered dimensions authoritative when available.
        return;
      }
      const estimated = estimateConfiguredFootprint(component, canvasWidth);
      mergedFootprints.set(type, {
        componentType: type,
        width: estimated.width,
        height: estimated.height,
        recommendedGapAfter: 24,
      });
    });

    const existingTerms = findFirstTermsComponent(formDefinition);
    const existingTermsLinkText =
      typeof existingTerms?.props.termsLinkText === "string"
        ? existingTerms.props.termsLinkText
        : undefined;
    const existingTermsUrl =
      typeof existingTerms?.props.termsUrl === "string"
        ? existingTerms.props.termsUrl
        : undefined;
    const existingDisplayMode =
      existingTerms?.props.termsDisplayMode === "new_tab" ? "new_tab" : "popup";

    let termsDefaults: AiRuntimeContext["termsDefaults"] | undefined = existingTerms
      ? {
          source: "form-existing",
          termsLinkText: existingTermsLinkText ?? "Terms of Service",
          termsUrl: existingTermsUrl ?? null,
          termsDisplayMode: existingDisplayMode,
          preserveCompanyTermsLink: true,
        }
      : undefined;

    if (formContext?.companyId && formContext.companyId > 0) {
      try {
        const termsAssets = await getCompanyTermsAssets(formContext.companyId);
        const hasCompanyTerms = (termsAssets.assets?.length ?? 0) > 0;
        const defaultAsset =
          termsAssets.assets.find(
            (asset) => asset.assetId === termsAssets.defaultTermsAssetId
          ) ?? termsAssets.assets[0];

        if (hasCompanyTerms) {
          if (!termsDefaults) {
            termsDefaults = {
              source: "company-default",
              termsLinkText:
                existingTermsLinkText ?? defaultAsset?.displayName ?? "Terms of Service",
              termsUrl: defaultAsset?.sourceType === "url" ? defaultAsset.sourceUrl ?? null : null,
              termsDisplayMode: defaultAsset?.termsDisplayMode ?? "popup",
              preserveCompanyTermsLink: true,
            };
          }
          termsDefaults = {
            ...termsDefaults,
            companyId: formContext.companyId,
            hasCompanyTerms: true,
            defaultTermsAssetId: termsAssets.defaultTermsAssetId ?? null,
            preserveCompanyTermsLink: true,
          };
        }
      } catch {
        // Best-effort enrichment; generation should still proceed without terms defaults.
      }
    }

    // Story 6.3.1 UAT round 6 — pre-flight horizontal→vertical downgrade
    // when the active preview canvas is too narrow for horizontal label
    // layout. We override only the per-request ``defaultObjectLayout`` and
    // leave the form's stored Global Styles untouched so the user's
    // preference persists for desktop generations.
    const storedGlobalStyles =
      (formDefinition.globalStyles as Record<string, unknown>) ?? null;
    const layoutDecision = resolveLayoutModeForRequest(
      storedGlobalStyles,
      canvasWidth
    );
    const effectiveGlobalStyles: Record<string, unknown> | null =
      storedGlobalStyles
        ? layoutDecision.downgraded
          ? { ...storedGlobalStyles, defaultObjectLayout: layoutDecision.layout }
          : storedGlobalStyles
        : null;

    if (layoutDecision.downgraded) {
      const notice =
        `Horizontal label layout needs at least ${HORIZONTAL_LAYOUT_MIN_WIDTH_PX}px ` +
        `of canvas width — this preview is ${Math.round(canvasWidth)}px. ` +
        "Generating with vertical layout for this run; your form's Global Styles are unchanged.";
      setLayoutDowngradeNotice(notice);
      devLogger.info("ai.runtime.layout-downgraded", {
        previewMode,
        canvasWidth: Math.round(canvasWidth),
        threshold: HORIZONTAL_LAYOUT_MIN_WIDTH_PX,
        originalLayout: layoutDecision.originalLayout,
        effectiveLayout: layoutDecision.layout,
      });
    } else {
      setLayoutDowngradeNotice(null);
    }

    return {
      formId: formDefinition.formId,
      audienceLocale: null,
      brandPosture: null,
      brandHeritageOrigin: null,
      canvas: {
        width: canvasWidth,
        height: canvasHeight,
        gridSize: formDefinition.canvasSettings?.gridSize,
      },
      // ``lockedGlobals.canvasSettings`` still ships the form's stored
      // canvasSettings so the LLM (if it ever inspects locked globals) sees
      // the canonical width — but ``runtimeContext.canvas`` (used by the
      // compiler) reflects the active device preview.
      //
      // ``lockedGlobals.globalStyles`` may have ``defaultObjectLayout``
      // overridden for this single request when the canvas is below
      // ``HORIZONTAL_LAYOUT_MIN_WIDTH_PX`` — see ``resolveLayoutModeForRequest``.
      lockedGlobals: {
        theme: (formDefinition.theme as Record<string, unknown>) ?? null,
        globalStyles: effectiveGlobalStyles,
        canvasSettings:
          (formDefinition.canvasSettings as Record<string, unknown>) ?? null,
      },
      termsDefaults,
      componentFootprints: Array.from(mergedFootprints.values()),
    };
  }, [formContext, formDefinition, previewMode]);

  const relayoutFromRenderedHeights = React.useCallback(
    async (definition: FormDefinition): Promise<FormDefinition | null> => {
      await nextPaint();

      const components = getFirstPageComponents(definition);
      if (components.length < 2) return null;

      const gridSize = definition.canvasSettings?.gridSize ?? 8;
      if (!isSingleColumn(components, gridSize)) return null;

      const measured = components.map((component) => {
        const element = document.querySelector(
          `[data-component-id="${component.id}"]`
        ) as HTMLElement | null;
        if (!element) return null;
        const dims = getComponentDimensions(component, element, scale * 100);
        const measuredHeight = Math.max(
          1,
          Math.round(
            Math.max(
              dims.height,
              parsePositiveNumber(component.props?.height, 0),
              parsePositiveNumber(component.style?.height, 0)
            )
          )
        );
        return { id: component.id, measuredHeight };
      });

      if (measured.some((item) => item === null)) return null;

      const byId = new Map(
        measured
          .filter((item): item is { id: string; measuredHeight: number } => item !== null)
          .map((item) => [item.id, item.measuredHeight])
      );

      const sorted = [...components].sort((a, b) => {
        const ay = a.position?.y ?? 0;
        const by = b.position?.y ?? 0;
        if (ay !== by) return ay - by;
        return (a.position?.x ?? 0) - (b.position?.x ?? 0);
      });

      const canvasHeight = definition.canvasSettings?.height ?? 980;
      const totalHeight = sorted.reduce(
        (sum, component) => sum + (byId.get(component.id) ?? 0),
        0
      );
      const availableSpace = canvasHeight - totalHeight;
      if (availableSpace <= 0) return null;

      const gap = Math.floor(availableSpace / (sorted.length + 1));
      if (gap < 0) return null;

      const cloned = JSON.parse(JSON.stringify(definition)) as FormDefinition;
      const clonedComponents = getFirstPageComponents(cloned);
      const clonedById = new Map(clonedComponents.map((component) => [component.id, component]));

      let yCursor = gap;
      let hasChanges = false;
      sorted.forEach((component) => {
        const next = clonedById.get(component.id);
        if (!next) return;
        const height = byId.get(component.id) ?? 0;
        const nextY = Math.round(yCursor);
        if ((next.position?.y ?? 0) !== nextY) hasChanges = true;
        if (parsePositiveNumber(next.props?.height, 0) !== height) hasChanges = true;
        if (parsePositiveNumber(next.style?.height, 0) !== height) hasChanges = true;

        next.position = { ...(next.position ?? { x: 0, y: 0 }), y: nextY };
        next.props = { ...(next.props ?? {}), height };
        next.style = { ...(next.style ?? {}), height };
        yCursor += height + gap;
      });

      return hasChanges ? cloned : null;
    },
    [scale]
  );

  /**
   * Story 6.3.1 UAT round 5 — render-then-measure second pass.
   *
   * After the first-pass DefinitionJSON is painted on the canvas, walk every
   * component element, measure its actual rendered height from the DOM, and
   * POST those heights to ``/api/form-ai/remeasure``. The backend recompiles
   * with ground-truth heights so spacing matches what the user sees, fixing
   * the "compiler said 131px / validator inflated to 220px / collision fired"
   * class of bugs that no amount of per-type estimation can eliminate.
   *
   * Returns the refined ``FormDefinition`` on success, or ``null`` if the
   * pass should be skipped (no run id, missing elements, server error, or
   * the refined definition failed validation). Callers fall back to the
   * first-pass definition when this returns ``null``.
   */
  const measureAndRemeasure = React.useCallback(
    async (
      generationRunId: number,
      firstPassDefinition: FormDefinition,
      runtimeContext: AiRuntimeContext,
      signal?: AbortSignal
    ): Promise<FormDefinition | null> => {
      // One paint cycle so the canvas has had a chance to render the new
      // components before we measure them. Two cycles in case the renderer
      // does its own post-mount measurement (terms component, file-upload
      // dropzone, etc.) that bumps the height after first paint.
      await nextPaint();
      await nextPaint();

      const components = getFirstPageComponents(firstPassDefinition);
      if (components.length === 0) {
        devLogger.info("ai.remeasure.skipped", {
          reason: "no-components",
        });
        return null;
      }

      const measurements: AiComponentMeasurement[] = [];
      const missing: string[] = [];
      for (const component of components) {
        const element = document.querySelector(
          `[data-component-id="${component.id}"]`
        ) as HTMLElement | null;
        if (!element) {
          missing.push(component.id);
          continue;
        }
        const dims = getComponentDimensions(component, element, scale * 100);
        const measuredHeight = Math.max(
          1,
          Math.round(
            Math.max(
              dims.height,
              parsePositiveNumber(component.props?.height, 0),
              parsePositiveNumber(component.style?.height, 0)
            )
          )
        );
        measurements.push({
          componentId: component.id,
          height: measuredHeight,
        });
      }

      // If we couldn't find any element to measure, the canvas hasn't
      // mounted yet — bail rather than send an empty measurement set.
      if (measurements.length === 0) {
        devLogger.info("ai.remeasure.skipped", {
          reason: "no-elements-found",
          missingComponentIds: missing,
        });
        return null;
      }

      try {
        const refined = await remeasureAiDefinition({
          generationRunId,
          measurements,
          runtimeContext,
        }, signal);
        devLogger.info("ai.remeasure.result", {
          status: refined.status,
          measuredCount: measurements.length,
          missingCount: missing.length,
          validationSummary: refined.validationSummary ?? null,
          compileSummary: refined.compileSummary ?? null,
        });
        if (refined.status === "completed" && refined.definitionJSON) {
          return refined.definitionJSON as unknown as FormDefinition;
        }
        return null;
      } catch (error) {
        // Render-then-measure is a refinement, not a hard requirement.
        // Log + fall back to the first-pass definition.
        devLogger.error("ai.remeasure.error", {
          generationRunId,
          message: error instanceof Error ? error.message : "remeasure failed",
        });
        return null;
      }
    },
    [scale]
  );

  const handleCancelGenerate = React.useCallback(() => {
    abortControllerRef.current?.abort();
  }, []);

  // Story 6.4 AC-2/3/4: check replace-warning condition then kick off generation
  const executeGenerate = React.useCallback(async () => {
    const trimmed = prompt.trim();
    if (!trimmed || isSubmitting) return;

    // Create a fresh AbortController for this run. Any prior run was already
    // completed or cancelled, so the old controller can be discarded safely.
    const controller = new AbortController();
    abortControllerRef.current = controller;
    const { signal } = controller;

    setIsSubmitting(true);
    setStatus("generating");
    setPromptSnapshot(trimmed.length > 160 ? `${trimmed.slice(0, 160)}…` : trimmed);
    setAttemptLines(null);
    setMessage(
      "Sending one request to the server. It may run up to 4 internal model attempts (initial + 3 corrections); this can take several minutes."
    );
    setTraceSummary(null);

    try {
      const runtimeContext = await buildRuntimeContext();
      const sectioned = buildSectionedSystemAddendum();
      const sectionSummaries = sectioned.sections.map((section) => {
        const body = [
          `Objective: ${section.objective}`,
          ...section.instructions.map((instruction) => `- ${instruction}`),
        ].join("\n");
        return {
          id: section.id,
          title: section.title,
          chars: body.length,
          hash: hashText(body),
        };
      });
      devLogger.info("ai.sections.run.start", {
        promptChars: trimmed.length,
        openaiTransport,
        sectionCount: sectioned.sections.length,
        sections: sectionSummaries,
      });
      // Story 6.4 AC-6: maxSystemCorrectionAttempts no longer sent from frontend.
      // The backend reads form_ai.default_retries from config.AppSetting.
      const generationOptions: AiGenerationOptions = {
        openaiTransport,
        systemPromptAddendum: sectioned.addendum,
      };
      const response = await generateAiDefinition(
        trimmed,
        runtimeContext,
        generationOptions,
        signal
      );
      setStatus("validating");

      const lines = (response.trace.attempts ?? []).map((entry) => formatAttemptLine(entry));
      setAttemptLines(lines.length > 0 ? lines : null);

      const usedRetries = response.trace.systemCorrectionAttemptsUsed;
      const transport =
        response.trace.resolvedOpenaiTransport ?? "—";
      const compilerMode = response.trace.compilerMode ?? "legacy";
      const compileSummary = response.trace.compileSummary as
        | { fallbackCount?: number; outputComponentCount?: number; canvasHeightGrew?: boolean }
        | undefined;
      const summary = `OpenAI transport (resolved): ${transport} · Server attempts: ${response.trace.attemptCount} · Retries used: ${usedRetries}/${response.trace.maxSystemCorrectionAttempts} · Compiler: ${compilerMode} · Output components: ${compileSummary?.outputComponentCount ?? "—"} · Fallbacks: ${compileSummary?.fallbackCount ?? "—"} · Canvas grew: ${compileSummary?.canvasHeightGrew ? "yes" : "no"} · Terminal: ${response.trace.terminalReason}`;
      setTraceSummary(summary);
      devLogger.info("ai.sections.run.result", {
        status: response.status,
        terminalReason: response.trace.terminalReason,
        attemptCount: response.trace.attemptCount,
        openaiTransport,
        resolvedOpenaiTransport: transport,
        validationSummary: response.trace.validationSummary ?? null,
        sectionCount: sectioned.sections.length,
        sections: sectionSummaries,
      });

      if (response.status === "completed" && response.definitionJSON) {
        if (usedRetries > 0) setStatus("retrying");
        const aiDefinition = response.definitionJSON as unknown as FormDefinition;
        applyValidatedDefinition(aiDefinition, "Apply AI generated layout");
        // Story 6.3.1 UAT round 5 — branch on compiler mode for the post-
        // apply refinement step. Two distinct, mutually-exclusive flows:
        //
        //   * deterministic-grid (current): run the render-then-measure
        //     second pass. The first-pass layout uses per-type height
        //     estimates which can disagree with what the renderer actually
        //     paints (option-heavy checkbox, paragraph text wrap, etc.) —
        //     the second pass swaps them out for ground-truth DOM heights
        //     so collisions can't fire from estimation error. See
        //     measureAndRemeasure() above for the full rationale.
        //   * legacy: keep relayoutFromRenderedHeights, the Story 6.2
        //     single-column reflow that re-measures heights and redis-
        //     tributes y positions evenly. Not safe for deterministic-grid
        //     because it overwrites style.height with body+chrome heights,
        //     which the textarea/submit renderers interpret as input-body
        //     only and re-stack chrome on top of, causing the exact
        //     "Comments overlaps Submit" failure the chrome budget fixes.
        const isDeterministicGrid = compilerMode === "deterministic-grid";
        if (isDeterministicGrid) {
          if (typeof response.generationRunId === "number") {
            const refined = await measureAndRemeasure(
              response.generationRunId,
              aiDefinition,
              runtimeContext,
              signal
            );
            if (refined) {
              applyValidatedDefinition(
                refined,
                "Refine AI layout with rendered measurements"
              );
            }
          } else {
            devLogger.info("ai.remeasure.skipped", {
              reason: "no-generation-run-id",
              compilerMode,
            });
          }
        } else {
          const measuredRelayout = await relayoutFromRenderedHeights(aiDefinition);
          if (measuredRelayout) {
            applyValidatedDefinition(
              measuredRelayout,
              "Rebalance AI layout from rendered component heights"
            );
          }
        }
        setStatus("completed");
        setMessage(response.userMessage);
        // Story 6.4 AC-1: persist last prompt to DB on successful dispatch
        setAiAgentSettings({ lastPrompt: trimmed });
        const formId = formDefinition?.formId;
        if (formId) {
          saveDraft(formId).catch(() => {
            // Non-blocking: prompt is in local state; DB persistence failure
            // is noted but doesn't interrupt the generation success flow.
          });
        }
        return;
      }

      setStatus("failed");
      setMessage(response.userMessage);

      // Story 6.4 AC-7: silent autoload — if backend returned a definition
      // (even with soft validation issues) apply it immediately without prompting.
      const hasDefinition = !!response.definitionJSON;
      const hasSoftIssues =
        response.draftHasValidationIssues ??
        /* older API responses omitted the flag; any definition on failed is inspectable */
        true;
      if (hasDefinition && hasSoftIssues) {
        applyValidatedDefinition(
          response.definitionJSON as unknown as FormDefinition,
          "Load AI draft (soft validation issues — auto-applied)"
        );
        // Also save the prompt that produced this draft
        setAiAgentSettings({ lastPrompt: trimmed });
        const formId = formDefinition?.formId;
        if (formId) saveDraft(formId).catch(() => {});
      }
      // Story 6.4 AC-8: if no definition returned, keep the existing failure message (already set above)
    } catch (error) {
      if (error instanceof DOMException && error.name === "AbortError") {
        // User navigated away or clicked Cancel — treat as a clean cancellation.
        setStatus("idle");
        setMessage(null);
        setTraceSummary(null);
        devLogger.info("ai.sections.run.cancelled", { openaiTransport });
      } else {
        setStatus("failed");
        setAttemptLines(null);
        setMessage(error instanceof Error ? error.message : "AI generation failed.");
        devLogger.error("ai.sections.run.error", {
          openaiTransport,
          message: error instanceof Error ? error.message : "AI generation failed",
        });
      }
    } finally {
      setIsSubmitting(false);
    }
  }, [
    applyValidatedDefinition,
    buildRuntimeContext,
    formDefinition,
    isSubmitting,
    measureAndRemeasure,
    openaiTransport,
    prompt,
    relayoutFromRenderedHeights,
    saveDraft,
    setAiAgentSettings,
  ]);

  // Story 6.4 AC-2/3/4: entry point for Generate button click
  const handleGenerate = React.useCallback(async () => {
    const trimmed = prompt.trim();
    if (!trimmed || isSubmitting) return;

    // AC-4: empty canvas → skip warning
    const allComponents = formDefinition
      ? selectAuthoredPages(formDefinition).flatMap((p) => p.components)
      : [];
    const hasComponents = allComponents.length > 0;

    if (hasComponents && !suppressWarning) {
      // Show the replace-form warning modal; actual generation proceeds from modal Confirm
      setShowReplaceWarning(true);
      return;
    }

    await executeGenerate();
  }, [prompt, isSubmitting, formDefinition, suppressWarning, executeGenerate]);

  // Story 6.4 AC-7: silent autoload means handleLoadInvalidDraft is no longer used.
  // Kept as a no-op placeholder to avoid breaking any downstream references during transition.

  // ---- Dev-only: load a DefinitionJSON from a local file -------------------
  // Story 6.3.1 UAT round 3: pairs with backend/scripts/story_631_replay.py to
  // let an operator iterate on compiler tweaks without burning OpenAI calls.
  // Visible only when VITE_ENABLE_DEV_LOGS=true so it never ships to prod
  // builders.
  const devLogsEnabled = import.meta.env.VITE_ENABLE_DEV_LOGS === "true";
  const replayFileInputRef = React.useRef<HTMLInputElement | null>(null);

  const handleLoadDefinitionFromFile = React.useCallback(
    async (event: React.ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0];
      // Reset so the same file can be re-selected after iteration.
      event.target.value = "";
      if (!file) return;
      try {
        const text = await file.text();
        const parsed = JSON.parse(text) as unknown;
        if (
          !parsed ||
          typeof parsed !== "object" ||
          !("pages" in (parsed as Record<string, unknown>)) ||
          !Array.isArray((parsed as { pages: unknown }).pages)
        ) {
          setMessage(
            `Selected file does not look like a FormDefinition (missing "pages" array): ${file.name}`
          );
          return;
        }
        applyValidatedDefinition(
          parsed as FormDefinition,
          `Load DefinitionJSON from file (${file.name})`
        );
        setMessage(
          `Loaded ${file.name} onto the canvas — bypassing the LLM. Compile diagnostics from the file are not shown here.`
        );
      } catch (exc) {
        setMessage(
          `Failed to load ${file.name}: ${exc instanceof Error ? exc.message : String(exc)}`
        );
      }
    },
    [applyValidatedDefinition]
  );

  const statusColorClass =
    status === "completed"
      ? "text-emerald-700 bg-emerald-50 border-emerald-200 dark:text-emerald-300 dark:bg-emerald-900/20 dark:border-emerald-900"
      : status === "failed"
      ? "text-rose-700 bg-rose-50 border-rose-200 dark:text-rose-300 dark:bg-rose-900/20 dark:border-rose-900"
      : "text-blue-700 bg-blue-50 border-blue-200 dark:text-blue-300 dark:bg-blue-900/20 dark:border-blue-900";

  return (
    <div className="flex-1 overflow-y-auto">
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center gap-2 mb-2">
          <Sparkles size={16} className="text-violet-500" />
          <h3 className="text-sm font-semibold text-gray-800 dark:text-gray-200">
            AI Agent
          </h3>
        </div>
        <p className="text-xs text-gray-500 dark:text-gray-400">
          One request may run several internal validator retries on the server before the
          HTTP response returns. Use the status log below to see each attempt after the
          response arrives.
        </p>
      </div>

      <div className="p-4 space-y-3">
        <label className="text-xs font-medium text-gray-700 dark:text-gray-300 block">
          Prompt
        </label>
        <textarea
          value={prompt}
          onChange={(event) => setPrompt(event.target.value)}
          placeholder="Example: Create a registration form with name, email, phone, and consent checkbox."
          className="w-full min-h-[140px] rounded-md border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 px-3 py-2 text-sm text-gray-800 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-violet-500"
        />

        <div className="flex gap-2">
          <button
            type="button"
            onClick={handleGenerate}
            disabled={isSubmitting || prompt.trim().length < 3}
            className="flex-1 inline-flex items-center justify-center gap-2 rounded-md px-3 py-2 text-sm font-medium text-white bg-violet-600 hover:bg-violet-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {isSubmitting ? <RefreshCw size={14} className="animate-spin" /> : <Sparkles size={14} />}
            Generate Form Draft
          </button>
          {isSubmitting && (
            <button
              type="button"
              onClick={handleCancelGenerate}
              className="inline-flex items-center justify-center px-3 py-2 rounded-md text-sm font-medium text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors"
              title="Cancel generation and free the browser connection"
            >
              Cancel
            </button>
          )}
        </div>

        {devLogsEnabled && (
          <div className="space-y-1">
            <input
              ref={replayFileInputRef}
              type="file"
              accept="application/json,.json"
              onChange={handleLoadDefinitionFromFile}
              className="hidden"
              aria-label="Load DefinitionJSON from file"
            />
            <button
              type="button"
              onClick={() => replayFileInputRef.current?.click()}
              disabled={isSubmitting}
              className="w-full inline-flex items-center justify-center gap-2 rounded-md px-3 py-2 text-xs font-medium text-violet-700 dark:text-violet-300 border border-dashed border-violet-300 dark:border-violet-700 bg-violet-50/50 dark:bg-violet-950/20 hover:bg-violet-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Upload size={12} />
              Load DefinitionJSON from file (dev only)
            </button>
            <p className="text-[10px] text-gray-500 dark:text-gray-400">
              Pairs with <code>backend/scripts/story_631_replay.py</code>. Loads the file
              straight onto the canvas — no LLM call, no validation gate.
            </p>
          </div>
        )}

        {layoutDowngradeNotice && (
          <div
            role="status"
            aria-live="polite"
            className="rounded-md border border-amber-300 bg-amber-50 px-3 py-2 text-[11px] text-amber-900 dark:border-amber-700 dark:bg-amber-950/40 dark:text-amber-100"
            data-testid="ai-panel-layout-downgrade-notice"
          >
            <div className="font-semibold mb-0.5">Layout adjusted for narrow canvas</div>
            <div className="whitespace-pre-wrap">{layoutDowngradeNotice}</div>
          </div>
        )}

        <div className={`rounded-md border px-3 py-2 text-xs ${statusColorClass}`}>
          <div className="font-semibold mb-1">Status: {STATUS_LABELS[status]}</div>
          {promptSnapshot && (
            <div className="mb-1 text-[11px] opacity-90 border-b border-current/10 pb-1">
              <span className="font-medium">Prompt: </span>
              {promptSnapshot}
            </div>
          )}
          {message && <div className="whitespace-pre-wrap">{message}</div>}
          {attemptLines && attemptLines.length > 0 && (
            <ul className="mt-2 list-disc pl-4 space-y-0.5 text-[11px] opacity-95">
              {attemptLines.map((line, idx) => (
                <li key={idx}>{line}</li>
              ))}
            </ul>
          )}
          {traceSummary && <div className="mt-2 text-[11px] opacity-90">{traceSummary}</div>}
        </div>

      </div>

      {/* Story 6.4 AC-2/3: Replace-form warning modal */}
      {showReplaceWarning && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full p-6">
            <h3 className="text-base font-semibold text-gray-900 dark:text-gray-100 mb-3">
              Replace existing form?
            </h3>
            <p className="text-sm text-gray-700 dark:text-gray-300 mb-4">
              Generating a new form will <strong>replace</strong> what's currently on the
              canvas. You can <strong>Undo</strong> this if needed (Ctrl/Cmd+Z). Continue?
            </p>
            <label className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400 mb-5 cursor-pointer">
              <input
                type="checkbox"
                checked={dontShowAgain}
                onChange={(e) => setDontShowAgain(e.target.checked)}
                className="rounded border-gray-300 text-violet-600 focus:ring-violet-500"
              />
              Don't show this again
            </label>
            <div className="flex items-center justify-end gap-3">
              <button
                type="button"
                onClick={() => {
                  setShowReplaceWarning(false);
                  setDontShowAgain(false);
                }}
                className="px-4 py-2 text-sm text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={async () => {
                  setShowReplaceWarning(false);
                  if (dontShowAgain) {
                    setSuppressWarning(true);
                    // Persist preference — fire and forget
                    patchPreferences({ [SUPPRESS_WARNING_KEY]: "true" }).catch(() => {});
                  }
                  setDontShowAgain(false);
                  await executeGenerate();
                }}
                className="px-4 py-2 text-sm font-medium text-white bg-violet-600 hover:bg-violet-700 rounded-lg transition-colors"
              >
                Continue
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
