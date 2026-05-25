import axios from "axios";

import { apiClient, formatError } from "../../../lib/apiClient";

export type AiGenerationStatus = "completed" | "failed";

export interface AttemptValidationSummary {
  valid: boolean;
  schemaErrorCount: number;
  boundaryViolationCount: number;
  collisionCount: number;
  errorCount: number;
}

export interface AttemptTraceEntry {
  attemptNumber: number;
  phase: "initial" | "correction";
  validation: AttemptValidationSummary;
  correctionIssued: boolean;
  notes?: string | null;
  /** This attempt's collisionCount minus the previous; absent on first attempt. */
  collisionDeltaFromPrevious?: number | null;
  /** vs prior attempt; n_a on first attempt. */
  collisionTrendVsPrevious?: "improved" | "worse" | "unchanged" | "n_a" | null;
  compileDiagnostics?: Record<string, unknown> | null;
}

/** Request + env resolution: sync = one response body; stream = SSE. Auto uses FORM_AI_OPENAI_TRANSPORT on the server (default sync). */
export type OpenAiTransportMode = "auto" | "sync" | "stream";
export type BrandPosture = "local" | "heritage" | "neutral" | "transcreate";

export interface AiGenerationOptions {
  openaiTransport?: OpenAiTransportMode;
  maxSystemCorrectionAttempts?: number;
  systemPromptAddendum?: string;
  /** ref.AudienceLocale.Code — loaded from API only (Story 6.5d). */
  audienceLocale?: string | null;
  formPurposeCode?: string | null;
  respondentTypeCode?: string | null;
  brandPosture?: BrandPosture | null;
  brandHeritageOrigin?: string | null;
}

export interface AiGenerationTrace {
  attemptCount: number;
  maxSystemCorrectionAttempts: number;
  systemCorrectionAttemptsUsed: number;
  terminalReason: string;
  attempts: AttemptTraceEntry[];
  validationSummary?: AttemptValidationSummary | null;
  /** After resolution (auto → sync|stream); compare with your selection to confirm behavior. */
  resolvedOpenaiTransport?: "sync" | "stream" | null;
  promptTemplateVersionId?: number | null;
  promptTemplateVersionRef?: string | null;
  promptAssemblyProfileId?: number | null;
  promptAssemblyProfileRef?: string | null;
  capabilityPolicyVersionId?: number | null;
  capabilityPolicyVersionRef?: string | null;
  componentCapabilitySnapshotId?: number | null;
  componentCapabilitySnapshotRef?: string | null;
  widthClassPolicyVersionId?: number | null;
  widthClassPolicyVersionRef?: string | null;
  validationContractVersion?: string | null;
  governanceResolutionSource?: string | null;
  compilerMode?: "deterministic-grid" | null;
  compileSummary?: Record<string, unknown> | null;
}

export interface AiFormGenerationResponse {
  status: AiGenerationStatus;
  definitionJSON?: Record<string, unknown> | null;
  trace: AiGenerationTrace;
  userMessage: string;
  meta?: {
    locale?: {
      resolved?: string | null;
      source?: string | null;
    };
    clarification?: {
      audienceLocaleCode?: string | null;
      formPurposeCode?: string | null;
      respondentTypeCode?: string | null;
    } | null;
    brand?: {
      resolved?: BrandPosture | null;
      heritageOrigin?: string | null;
      source?: string | null;
    };
    [key: string]: unknown;
  } | null;
  /** True when status is failed but definitionJSON is the last invalid draft for canvas inspection */
  draftHasValidationIssues?: boolean;
  /**
   * Story 6.3.1 UAT round 5 — server-side run id for the second-pass
   * /remeasure call. Absent when the server didn't persist the run (e.g.
   * tests with no DB session). Frontends that don't implement
   * render-then-measure can ignore it entirely.
   */
  generationRunId?: number | null;
}

// ---------- Story 6.3.1 UAT round 5 — render-then-measure ----------

/** A single DOM-measured component height the frontend will POST to /remeasure. */
export interface AiComponentMeasurement {
  componentId: string;
  /** Rendered height in CSS pixels (e.g. element.getBoundingClientRect().height / scale). */
  height: number;
}

export interface AiRemeasureRequest {
  generationRunId: number;
  measurements: AiComponentMeasurement[];
  /** Same runtime context the original /generate call used. */
  runtimeContext?: AiRuntimeContext;
}

export interface AiRemeasureResponse {
  status: AiGenerationStatus;
  /** Refined DefinitionJSON. Null when status === "failed". */
  definitionJSON?: Record<string, unknown> | null;
  compileSummary?: Record<string, unknown> | null;
  validationSummary?: AttemptValidationSummary | null;
  userMessage: string;
  generationRunId: number;
}

export interface RuntimeComponentFootprint {
  componentType: string;
  width: number;
  height: number;
  recommendedGapAfter?: number;
}

export interface RuntimeCanvasContext {
  width: number;
  height: number;
  gridSize?: number;
}

export interface RuntimeLockedGlobals {
  theme?: Record<string, unknown> | null;
  globalStyles?: Record<string, unknown> | null;
  canvasSettings?: Record<string, unknown> | null;
}

export interface RuntimeTermsDefaults {
  companyId?: number;
  hasCompanyTerms?: boolean;
  defaultTermsAssetId?: number | null;
  source?: "form-existing" | "company-default" | "none";
  termsLinkText?: string | null;
  termsUrl?: string | null;
  termsDisplayMode?: "popup" | "new_tab" | null;
  preserveCompanyTermsLink?: boolean;
}

export interface AiRuntimeContext {
  formId?: string;
  audienceLocale?: string | null;
  formPurposeCode?: string | null;
  respondentTypeCode?: string | null;
  brandPosture?: BrandPosture | null;
  brandHeritageOrigin?: string | null;
  canvas?: RuntimeCanvasContext;
  lockedGlobals?: RuntimeLockedGlobals;
  termsDefaults?: RuntimeTermsDefaults;
  componentFootprints?: RuntimeComponentFootprint[];
}

/**
 * Client wait budget for POST /api/form-ai/generate.
 * Backend may call OpenAI up to (max correction attempts + 1) times, each with up to
 * OPENAI_TIMEOUT_SECONDS (default 180s) — see backend/modules/form_ai/service.py.
 * Keep this above that worst-case total so the UI does not abort while the server is still working.
 */
const FORM_AI_GENERATE_TIMEOUT_MS = 1_200_000;

export async function generateAiDefinition(
  prompt: string,
  runtimeContext?: AiRuntimeContext,
  options: AiGenerationOptions = {},
  signal?: AbortSignal
): Promise<AiFormGenerationResponse> {
  try {
    const {
      openaiTransport = "auto",
      maxSystemCorrectionAttempts,
      systemPromptAddendum,
      audienceLocale = runtimeContext?.audienceLocale ?? null,
      formPurposeCode = runtimeContext?.formPurposeCode ?? options.formPurposeCode ?? null,
      respondentTypeCode =
        runtimeContext?.respondentTypeCode ?? options.respondentTypeCode ?? null,
      brandPosture = runtimeContext?.brandPosture ?? null,
      brandHeritageOrigin = runtimeContext?.brandHeritageOrigin ?? null,
    } = options;
    const response = await apiClient.post<AiFormGenerationResponse>(
      "/api/form-ai/generate",
      {
        prompt,
        runtimeContext,
        audienceLocale,
        formPurposeCode,
        respondentTypeCode,
        brandPosture,
        brandHeritageOrigin,
        openaiTransport,
        maxSystemCorrectionAttempts,
        systemPromptAddendum,
      },
      { timeout: FORM_AI_GENERATE_TIMEOUT_MS, signal }
    );
    return response.data;
  } catch (error) {
    if (axios.isCancel(error)) {
      throw new DOMException("AI generation was cancelled.", "AbortError");
    }
    if (axios.isAxiosError(error) && error.code === "ECONNABORTED") {
      const seconds = Math.round(FORM_AI_GENERATE_TIMEOUT_MS / 1000);
      const minutes = Math.round(FORM_AI_GENERATE_TIMEOUT_MS / 60000);
      throw new Error(
        `Request timed out after ${seconds}s (${minutes} min client wait). ` +
          "One generate call runs up to 4 model attempts on the server (initial + 3 corrections); " +
          "each attempt can take a long time. Try again, or shorten the prompt / reduce validator load. " +
          "“Load last draft” only appears when the server returns JSON — a client timeout cancels the request before any draft arrives."
      );
    }
    throw formatError(error);
  }
}

/**
 * Story 6.3.1 UAT round 5 — render-then-measure second pass.
 *
 * Sends the DOM-rendered heights of each component to the backend, which
 * recompiles using ground-truth measurements instead of per-type estimates.
 * Returns a refined DefinitionJSON that exactly matches what the renderer
 * is going to paint. The caller is responsible for falling back to the
 * first-pass definition on failure (status === "failed").
 *
 * The endpoint runs no LLM calls so this is fast (~50–200 ms typical).
 */
const FORM_AI_REMEASURE_TIMEOUT_MS = 30_000;

export async function remeasureAiDefinition(
  request: AiRemeasureRequest,
  signal?: AbortSignal
): Promise<AiRemeasureResponse> {
  try {
    const response = await apiClient.post<AiRemeasureResponse>(
      "/api/form-ai/remeasure",
      request,
      { timeout: FORM_AI_REMEASURE_TIMEOUT_MS, signal }
    );
    return response.data;
  } catch (error) {
    if (axios.isCancel(error)) {
      throw new DOMException("Remeasure was cancelled.", "AbortError");
    }
    if (axios.isAxiosError(error) && error.code === "ECONNABORTED") {
      throw new Error(
        "Render-then-measure timed out. The first-pass layout will be used."
      );
    }
    throw formatError(error);
  }
}
