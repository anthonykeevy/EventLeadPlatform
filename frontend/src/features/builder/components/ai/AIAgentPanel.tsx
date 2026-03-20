import React from "react";
import { Sparkles, RefreshCw, AlertTriangle, CheckCircle2 } from "lucide-react";

import { AiRuntimeContext, generateAiDefinition } from "../../api/aiFormGenerationApi";
import { useBuilderStore } from "../../stores/useBuilderStore";
import { FormComponent, FormDefinition } from "../../types/builder.types";
import { getCompanyTermsAssets } from "../../../dashboard/api/companyAssetsApi";
import { getComponentDimensions } from "../../utils/collisionDetection";

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
    textarea: 140,
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
  const { applyValidatedDefinition, formDefinition, formContext, scale } = useBuilderStore();
  const [prompt, setPrompt] = React.useState("");
  const [status, setStatus] = React.useState<GenerationUiStatus>("idle");
  const [message, setMessage] = React.useState<string | null>(null);
  const [traceSummary, setTraceSummary] = React.useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = React.useState(false);

  const buildRuntimeContext = React.useCallback(async (): Promise<AiRuntimeContext | undefined> => {
    if (!formDefinition) return undefined;
    const canvasWidth = formDefinition.canvasSettings?.width ?? 1920;

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
      const estimated = estimateConfiguredFootprint(component, canvasWidth);
      const existing = mergedFootprints.get(type);
      if (!existing) {
        mergedFootprints.set(type, {
          componentType: type,
          width: estimated.width,
          height: estimated.height,
          recommendedGapAfter: 24,
        });
        return;
      }
      mergedFootprints.set(type, {
        componentType: type,
        width: Math.max(existing.width, estimated.width),
        height: Math.max(existing.height, estimated.height),
        recommendedGapAfter: Math.max(existing.recommendedGapAfter ?? 24, 24),
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

    return {
      formId: formDefinition.formId,
      canvas: {
        width: formDefinition.canvasSettings?.width ?? 1920,
        height: formDefinition.canvasSettings?.height ?? 980,
        gridSize: formDefinition.canvasSettings?.gridSize,
      },
      lockedGlobals: {
        theme: (formDefinition.theme as Record<string, unknown>) ?? null,
        globalStyles: (formDefinition.globalStyles as Record<string, unknown>) ?? null,
        canvasSettings:
          (formDefinition.canvasSettings as Record<string, unknown>) ?? null,
      },
      termsDefaults,
      componentFootprints: Array.from(mergedFootprints.values()),
    };
  }, [formContext, formDefinition]);

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

  const handleGenerate = React.useCallback(async () => {
    const trimmed = prompt.trim();
    if (!trimmed || isSubmitting) return;

    setIsSubmitting(true);
    setStatus("generating");
    setMessage("Generating draft DefinitionJSON...");
    setTraceSummary(null);

    try {
      const runtimeContext = await buildRuntimeContext();
      const response = await generateAiDefinition(trimmed, runtimeContext);
      setStatus("validating");

      const usedRetries = response.trace.systemCorrectionAttemptsUsed;
      const summary = `Attempts: ${response.trace.attemptCount} (retries: ${usedRetries}/3), terminal reason: ${response.trace.terminalReason}`;
      setTraceSummary(summary);

      if (response.status === "completed" && response.definitionJSON) {
        if (usedRetries > 0) setStatus("retrying");
        const aiDefinition = response.definitionJSON as unknown as FormDefinition;
        applyValidatedDefinition(aiDefinition, "Apply AI generated layout");
        const measuredRelayout = await relayoutFromRenderedHeights(aiDefinition);
        if (measuredRelayout) {
          applyValidatedDefinition(
            measuredRelayout,
            "Rebalance AI layout from rendered component heights"
          );
        }
        setStatus("completed");
        setMessage(response.userMessage);
        return;
      }

      setStatus("failed");
      setMessage(response.userMessage);
    } catch (error) {
      setStatus("failed");
      setMessage(error instanceof Error ? error.message : "AI generation failed.");
    } finally {
      setIsSubmitting(false);
    }
  }, [applyValidatedDefinition, buildRuntimeContext, isSubmitting, prompt, relayoutFromRenderedHeights]);

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
          Describe a single-page form. AI generates, validates, and retries up to 3
          correction attempts before applying to canvas.
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

        <button
          type="button"
          onClick={handleGenerate}
          disabled={isSubmitting || prompt.trim().length < 3}
          className="w-full inline-flex items-center justify-center gap-2 rounded-md px-3 py-2 text-sm font-medium text-white bg-violet-600 hover:bg-violet-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {isSubmitting ? <RefreshCw size={14} className="animate-spin" /> : <Sparkles size={14} />}
          Generate Form Draft
        </button>

        <div className={`rounded-md border px-3 py-2 text-xs ${statusColorClass}`}>
          <div className="font-semibold mb-1">Status: {STATUS_LABELS[status]}</div>
          {message && <div>{message}</div>}
          {traceSummary && <div className="mt-1 opacity-90">{traceSummary}</div>}
        </div>

        <div className="rounded-md border border-gray-200 dark:border-gray-700 p-3 text-xs text-gray-600 dark:text-gray-400">
          <div className="flex items-start gap-2 mb-1">
            <CheckCircle2 size={13} className="text-emerald-500 mt-0.5" />
            <span>Validated output is applied to canvas only after passing validator.</span>
          </div>
          <div className="flex items-start gap-2">
            <AlertTriangle size={13} className="text-amber-500 mt-0.5" />
            <span>
              If retries are exhausted, refine your prompt and run again. Single-page
              generation only in Story 6.2.
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
