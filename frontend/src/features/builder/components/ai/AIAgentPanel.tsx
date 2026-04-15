import React from "react";
import { Sparkles, RefreshCw, AlertTriangle, CheckCircle2 } from "lucide-react";

import {
  AiGenerationOptions,
  AiRuntimeContext,
  AttemptTraceEntry,
  RuntimeEventInformation,
  generateAiDefinition,
} from "../../api/aiFormGenerationApi";
import { getEventById } from "../../../events/api/eventsApi";
import { useBuilderStore } from "../../stores/useBuilderStore";
import { FormComponent, FormDefinition } from "../../types/builder.types";
import { getCompanyTermsAssets } from "../../../dashboard/api/companyAssetsApi";
import { getComponentDimensions } from "../../utils/collisionDetection";
import { buildComponentFootprintsForAiRuntime } from "./buildAiRuntimeFootprints";
import { devLogger } from "../../utils/devLogger";

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

const SYSTEM_PROMPT_PROFILE_VERSION = "AI-FORM-BUILDER-SYSTEM-PROMPT sections-1-6";

function parsePositiveNumber(value: unknown, fallback: number): number {
  if (typeof value === "number" && Number.isFinite(value) && value > 0) return value;
  if (typeof value === "string") {
    const normalized = value.trim().toLowerCase().replace(/px$/, "");
    const parsed = Number(normalized);
    if (Number.isFinite(parsed) && parsed > 0) return parsed;
  }
  return fallback;
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
  if (v.valid) {
    return `${phaseLabel}: validation passed`;
  }
  const bits: string[] = [];
  if (v.collisionCount > 0) bits.push(`${v.collisionCount} collision(s)`);
  if (v.boundaryViolationCount > 0) bits.push(`${v.boundaryViolationCount} boundary`);
  if (v.schemaErrorCount > 0) bits.push(`${v.schemaErrorCount} schema`);
  const detail = bits.length > 0 ? bits.join(", ") : `${v.errorCount} error(s)`;
  const tail = entry.correctionIssued ? " → sent correction to model" : "";
  return `${phaseLabel}: ${detail}${tail}`;
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
    formDefinition,
    formContext,
    scale,
    initComponents,
    setAiAgentSettings,
  } = useBuilderStore();
  const prompt =
    formDefinition?.aiAgentSettings?.lastPrompt ?? "";
  const includeEventInformation =
    formDefinition?.aiAgentSettings?.includeEventInformation ?? true;
  const maxSystemCorrectionAttempts =
    formDefinition?.aiAgentSettings?.maxSystemCorrectionAttempts ?? 1;
  const globalStylesLocked =
    formDefinition?.aiAgentSettings?.globalStylesLocked ?? true;

  const [status, setStatus] = React.useState<GenerationUiStatus>("idle");
  const [message, setMessage] = React.useState<string | null>(null);
  const [traceSummary, setTraceSummary] = React.useState<string | null>(null);
  const [promptSnapshot, setPromptSnapshot] = React.useState<string | null>(null);
  const [attemptLines, setAttemptLines] = React.useState<string[] | null>(null);
  const [pendingInvalidDraft, setPendingInvalidDraft] = React.useState<Record<
    string,
    unknown
  > | null>(null);
  const [isSubmitting, setIsSubmitting] = React.useState(false);

  const buildRuntimeContext = React.useCallback(async (): Promise<AiRuntimeContext | undefined> => {
    if (!formDefinition) return undefined;
    // componentFootprints: use canvas-scale defaults from registry (new-drop policy), not toolbox
    // thumbnail getBoundingClientRect — toolbox uses compact surface previews (story-6.3 §2.5).
    const initCodes = initComponents?.map((c) => c.componentCode) ?? null;
    const componentFootprints = buildComponentFootprintsForAiRuntime(
      formDefinition,
      scale,
      initCodes
    );

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

    let eventInformation: RuntimeEventInformation | undefined;
    const useEvent =
      (formDefinition?.aiAgentSettings?.includeEventInformation ?? true) &&
      Boolean(formContext?.eventId && formContext.eventId > 0);
    const eventId = formContext?.eventId;
    if (useEvent && typeof eventId === "number" && eventId > 0) {
      try {
        const ev = await getEventById(eventId);
        if (ev.name?.trim()) {
          eventInformation = {
            eventId: ev.eventId,
            name: ev.name.trim(),
            startDateTime: ev.startDateTime,
            endDateTime: ev.endDateTime,
            timezoneIdentifier: ev.timezoneIdentifier,
            venueName: ev.venueName,
            venueAddress: ev.venueAddress,
            city: ev.city,
            state: ev.state,
            shortDescription: ev.shortDescription,
          };
        }
      } catch {
        // Omit event block if the event cannot be loaded (permissions, network, etc.).
      }
    }

    return {
      formId: formDefinition.formId,
      canvasSettings: {
        width: formDefinition.canvasSettings?.width ?? 1920,
        height: formDefinition.canvasSettings?.height ?? 980,
        gridSize: formDefinition.canvasSettings?.gridSize,
      },
      globalStylesLocked,
      theme: (formDefinition.theme as unknown as Record<string, unknown>) ?? null,
      globalStyles:
        (formDefinition.globalStyles as unknown as Record<string, unknown>) ?? null,
      termsDefaults,
      componentFootprints,
      ...(eventInformation ? { eventInformation } : {}),
    };
  }, [formContext, formDefinition, globalStylesLocked, initComponents, scale]);

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

      const gap = availableSpace / (sorted.length + 1);

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
    setPromptSnapshot(trimmed.length > 160 ? `${trimmed.slice(0, 160)}…` : trimmed);
    setAttemptLines(null);
    setPendingInvalidDraft(null);
    setMessage(
      "Sending one request to the server. It may run up to 4 internal model attempts (initial + 3 corrections); this can take several minutes."
    );
    setTraceSummary(null);

    try {
      const runtimeContext = await buildRuntimeContext();
      setAiAgentSettings({
        sectionedPromptProfileVersion: SYSTEM_PROMPT_PROFILE_VERSION,
      });
      devLogger.info("ai.sections.run.start", {
        profileVersion: SYSTEM_PROMPT_PROFILE_VERSION,
        promptChars: trimmed.length,
        maxSystemCorrectionAttempts,
        globalStylesLocked,
      });
      const options: AiGenerationOptions = {
        maxSystemCorrectionAttempts,
      };
      const response = await generateAiDefinition(trimmed, runtimeContext, options);
      setStatus("validating");

      const lines = (response.trace.attempts ?? []).map((entry) => formatAttemptLine(entry));
      setAttemptLines(lines.length > 0 ? lines : null);

      const usedRetries = response.trace.systemCorrectionAttemptsUsed;
      const postProcessChanged = response.trace.postProcessingSummary?.changedComponentCount ?? 0;
      const summary = `Server attempts: ${response.trace.attemptCount} · Retries used: ${usedRetries}/${response.trace.maxSystemCorrectionAttempts} · Terminal: ${response.trace.terminalReason} · Post-process moves: ${postProcessChanged}`;
      setTraceSummary(summary);
      devLogger.info("ai.sections.run.result", {
        profileVersion: SYSTEM_PROMPT_PROFILE_VERSION,
        status: response.status,
        terminalReason: response.trace.terminalReason,
        attemptCount: response.trace.attemptCount,
        maxSystemCorrectionAttempts,
        globalStylesLocked,
        validationSummary: response.trace.validationSummary ?? null,
        postProcessingSummary: response.trace.postProcessingSummary ?? null,
        attemptPostProcessing: (response.trace.attempts ?? []).map((entry) => ({
          attemptNumber: entry.attemptNumber,
          phase: entry.phase,
          changedComponentCount: entry.postProcessing?.changedComponentCount ?? 0,
          changedComponents: entry.postProcessing?.changedComponents ?? [],
          canvasHeightBefore: entry.postProcessing?.canvasHeightBefore ?? null,
          canvasHeightAfter: entry.postProcessing?.canvasHeightAfter ?? null,
          canvasHeightChanged: entry.postProcessing?.canvasHeightChanged ?? false,
        })),
      });

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
        setPendingInvalidDraft(null);
        return;
      }

      setStatus("failed");
      setMessage(response.userMessage);
      const offerInvalidDraft =
        response.definitionJSON &&
        (response.draftHasValidationIssues ??
          /* older API responses omitted the flag; any definition on failed is inspectable */
          true);
      if (offerInvalidDraft) {
        setPendingInvalidDraft(response.definitionJSON as Record<string, unknown>);
      } else {
        setPendingInvalidDraft(null);
      }
    } catch (error) {
      setStatus("failed");
      setAttemptLines(null);
      setPendingInvalidDraft(null);
      const raw = error instanceof Error ? error.message : "AI generation failed.";
      setMessage(raw);
      devLogger.error("ai.sections.run.error", {
        maxSystemCorrectionAttempts,
        globalStylesLocked,
        message: raw,
      });
    } finally {
      setIsSubmitting(false);
    }
  }, [
    applyValidatedDefinition,
    buildRuntimeContext,
    isSubmitting,
    maxSystemCorrectionAttempts,
    globalStylesLocked,
    prompt,
    relayoutFromRenderedHeights,
    setAiAgentSettings,
  ]);

  const handleLoadInvalidDraft = React.useCallback(() => {
    if (!pendingInvalidDraft) return;
    applyValidatedDefinition(
      pendingInvalidDraft as unknown as FormDefinition,
      "Load AI draft (unresolved validation issues)"
    );
    setPendingInvalidDraft(null);
    setMessage(
      "Draft loaded on canvas. Collisions or boundaries may still be present — inspect in the builder."
    );
  }, [applyValidatedDefinition, pendingInvalidDraft]);

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
          HTTP response returns. The status log shows each attempt after the response arrives.
        </p>
      </div>

      <div className="p-4 space-y-3">
        <label className="flex items-center gap-2 cursor-pointer select-none">
          <input
            type="checkbox"
            checked={includeEventInformation}
            onChange={(e) =>
              setAiAgentSettings({ includeEventInformation: e.target.checked })
            }
            disabled={!formContext?.eventId || formContext.eventId <= 0}
            className="rounded border-gray-300 text-violet-600 focus:ring-violet-500 disabled:opacity-50"
          />
          <span className="text-xs font-medium text-gray-700 dark:text-gray-300">
            Include event information
          </span>
        </label>
        {formContext?.eventId && formContext.eventId > 0 ? (
          <p className="text-[11px] text-gray-500 dark:text-gray-400 -mt-2">
            Sends the linked event&apos;s name, schedule, and venue (when loaded) in the AI
            request. Turn off if you want a generic layout only.
          </p>
        ) : (
          <p className="text-[11px] text-amber-700/90 dark:text-amber-300/90 -mt-2">
            This form is not linked to an event — event details cannot be included.
          </p>
        )}

        <label className="flex items-center gap-2 cursor-pointer select-none">
          <input
            type="checkbox"
            checked={globalStylesLocked}
            onChange={(e) =>
              setAiAgentSettings({ globalStylesLocked: e.target.checked })
            }
            disabled={isSubmitting}
            className="rounded border-gray-300 text-violet-600 focus:ring-violet-500 disabled:opacity-50"
          />
          <span className="text-xs font-medium text-gray-700 dark:text-gray-300">
            Lock global styles (preserve company brand)
          </span>
        </label>
        <p className="text-[11px] text-gray-500 dark:text-gray-400 -mt-2">
          When locked, AI can still use per-component style overrides but should keep
          globalStyles unchanged.
        </p>

        <label className="text-xs font-medium text-gray-700 dark:text-gray-300 block">
          Prompt
        </label>
        <textarea
          value={prompt}
          onChange={(event) => setAiAgentSettings({ lastPrompt: event.target.value })}
          placeholder="Example: Create a registration form with name, email, phone, and consent checkbox."
          className="w-full min-h-[140px] rounded-md border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 px-3 py-2 text-sm text-gray-800 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-violet-500"
        />

        <label className="text-xs font-medium text-gray-700 dark:text-gray-300 block">
          System correction attempts (retry count)
        </label>
        <input
          type="number"
          min={0}
          max={10}
          step={1}
          value={maxSystemCorrectionAttempts}
          onChange={(event) => {
            const parsed = Number(event.target.value);
            if (!Number.isFinite(parsed)) return;
            const clamped = Math.max(0, Math.min(10, Math.round(parsed)));
            setAiAgentSettings({ maxSystemCorrectionAttempts: clamped });
          }}
          disabled={isSubmitting}
          className="w-full rounded-md border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 px-3 py-2 text-sm text-gray-800 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-violet-500"
          aria-label="System correction attempts"
        />
        <p className="text-[11px] text-gray-500 dark:text-gray-400 -mt-2">
          Set to <code>1</code> for baseline section-evaluation runs.
        </p>
        <p className="text-[11px] text-gray-500 dark:text-gray-400 -mt-2">
          System prompt profile: <code>{SYSTEM_PROMPT_PROFILE_VERSION}</code>.
        </p>

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
          {pendingInvalidDraft && (
            <button
              type="button"
              onClick={handleLoadInvalidDraft}
              className="mt-2 w-full rounded-md border border-amber-300 bg-amber-50 px-2 py-1.5 text-[11px] font-medium text-amber-900 hover:bg-amber-100 dark:border-amber-700 dark:bg-amber-950/40 dark:text-amber-100 dark:hover:bg-amber-900/40"
            >
              Load last draft on canvas (has validation issues)
            </button>
          )}
        </div>

        <div className="rounded-md border border-gray-200 dark:border-gray-700 p-3 text-xs text-gray-600 dark:text-gray-400">
          <div className="flex items-start gap-2 mb-1">
            <CheckCircle2 size={13} className="text-emerald-500 mt-0.5" />
            <span>
              On success, the validated draft is applied automatically. If generation fails
              but a last draft is returned, you can load it to inspect collisions on the
              canvas. After a client timeout, no draft is available until the server responds.
            </span>
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
