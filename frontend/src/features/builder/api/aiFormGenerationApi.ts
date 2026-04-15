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
}

/** Request + env resolution: sync = one response body; stream = SSE. Auto uses FORM_AI_OPENAI_TRANSPORT on the server (default sync). */
export type OpenAiTransportMode = "auto" | "sync" | "stream";

export interface AiGenerationOptions {
  openaiTransport?: OpenAiTransportMode;
  maxSystemCorrectionAttempts?: number;
  systemPromptAddendum?: string;
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
}

export interface AiFormGenerationResponse {
  status: AiGenerationStatus;
  definitionJSON?: Record<string, unknown> | null;
  trace: AiGenerationTrace;
  userMessage: string;
  /** True when status is failed but definitionJSON is the last invalid draft for canvas inspection */
  draftHasValidationIssues?: boolean;
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
  options: AiGenerationOptions = {}
): Promise<AiFormGenerationResponse> {
  try {
    const {
      openaiTransport = "auto",
      maxSystemCorrectionAttempts,
      systemPromptAddendum,
    } = options;
    const response = await apiClient.post<AiFormGenerationResponse>(
      "/api/form-ai/generate",
      {
        prompt,
        runtimeContext,
        openaiTransport,
        maxSystemCorrectionAttempts,
        systemPromptAddendum,
      },
      { timeout: FORM_AI_GENERATE_TIMEOUT_MS }
    );
    return response.data;
  } catch (error) {
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
