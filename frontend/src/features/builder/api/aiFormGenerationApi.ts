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
}

export interface AiGenerationTrace {
  attemptCount: number;
  maxSystemCorrectionAttempts: number;
  systemCorrectionAttemptsUsed: number;
  terminalReason: string;
  attempts: AttemptTraceEntry[];
  validationSummary?: AttemptValidationSummary | null;
}

export interface AiFormGenerationResponse {
  status: AiGenerationStatus;
  definitionJSON?: Record<string, unknown> | null;
  trace: AiGenerationTrace;
  userMessage: string;
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

export async function generateAiDefinition(
  prompt: string,
  runtimeContext?: AiRuntimeContext
): Promise<AiFormGenerationResponse> {
  try {
    const response = await apiClient.post<AiFormGenerationResponse>(
      "/api/form-ai/generate",
      { prompt, runtimeContext },
      // Story 6.2: generation can include multiple retries and exceed the default 30s timeout.
      { timeout: 180000 }
    );
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.code === "ECONNABORTED") {
      throw new Error(
        "AI generation is taking longer than expected (timeout after 180s). " +
          "Try a shorter prompt or retry once."
      );
    }
    throw formatError(error);
  }
}
