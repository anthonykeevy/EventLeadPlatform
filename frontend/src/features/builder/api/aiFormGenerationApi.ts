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

export interface PostProcessingComponentPositionDelta {
  componentId: string;
  componentType?: string | null;
  before: { x: number; y: number };
  after: { x: number; y: number };
}

export interface PostProcessingSummary {
  changedComponentCount: number;
  changedComponents: PostProcessingComponentPositionDelta[];
  canvasHeightBefore?: number | null;
  canvasHeightAfter?: number | null;
  canvasHeightChanged: boolean;
}

export interface AttemptTraceEntry {
  attemptNumber: number;
  phase: "initial" | "correction";
  validation: AttemptValidationSummary;
  correctionIssued: boolean;
  notes?: string | null;
  postProcessing?: PostProcessingSummary | null;
}

export interface AiGenerationTrace {
  attemptCount: number;
  maxSystemCorrectionAttempts: number;
  systemCorrectionAttemptsUsed: number;
  terminalReason: string;
  attempts: AttemptTraceEntry[];
  validationSummary?: AttemptValidationSummary | null;
  postProcessingSummary?: PostProcessingSummary | null;
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

/** Factual event metadata when the user enables “Include event information” on the AI panel. */
export interface RuntimeEventInformation {
  eventId: number;
  name: string;
  startDateTime?: string;
  endDateTime?: string | null;
  timezoneIdentifier?: string | null;
  venueName?: string | null;
  venueAddress?: string | null;
  city?: string | null;
  state?: string | null;
  shortDescription?: string | null;
}

export interface AiRuntimeContext {
  formId?: string;
  canvasSettings?: RuntimeCanvasContext;
  globalStylesLocked?: boolean;
  globalStyles?: Record<string, unknown> | null;
  theme?: Record<string, unknown> | null;
  termsDefaults?: RuntimeTermsDefaults;
  componentFootprints?: RuntimeComponentFootprint[];
  eventInformation?: RuntimeEventInformation;
}

export interface AiGenerationOptions {
  maxSystemCorrectionAttempts?: number;
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
    const { maxSystemCorrectionAttempts } = options;
    const response = await apiClient.post<AiFormGenerationResponse>(
      "/api/form-ai/generate",
      {
        prompt,
        runtimeContext,
        maxSystemCorrectionAttempts,
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
