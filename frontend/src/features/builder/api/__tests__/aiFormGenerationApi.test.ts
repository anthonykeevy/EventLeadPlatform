import { describe, expect, it, vi, beforeEach } from "vitest";

import { generateAiDefinition } from "../aiFormGenerationApi";
import { apiClient } from "../../../../lib/apiClient";

vi.mock("../../../../lib/apiClient", () => ({
  apiClient: {
    post: vi.fn(),
  },
  formatError: (error: unknown) =>
    error instanceof Error ? error : new Error("Unknown API error"),
}));

describe("generateAiDefinition", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("posts prompt to Story 6.2 backend endpoint", async () => {
    const mockResponse = {
      status: "completed",
      definitionJSON: { schemaVersion: "1.0", formId: "ai-form", pages: [] },
      trace: {
        attemptCount: 1,
        maxSystemCorrectionAttempts: 3,
        systemCorrectionAttemptsUsed: 0,
        terminalReason: "validated-success",
        attempts: [],
      },
      userMessage: "ok",
    };
    vi.mocked(apiClient.post).mockResolvedValue({ data: mockResponse });

    const result = await generateAiDefinition("Build a contact form");

    expect(apiClient.post).toHaveBeenCalledWith(
      "/api/form-ai/generate",
      {
        prompt: "Build a contact form",
        runtimeContext: undefined,
        openaiTransport: "auto",
        maxSystemCorrectionAttempts: undefined,
        systemPromptAddendum: undefined,
      },
      { timeout: 1_200_000 }
    );
    expect(result.status).toBe("completed");
    expect(result.trace.attemptCount).toBe(1);
  });

  it("throws formatted error when request fails", async () => {
    vi.mocked(apiClient.post).mockRejectedValue(new Error("network-down"));

    await expect(generateAiDefinition("Build a lead form")).rejects.toThrow(
      "network-down"
    );
  });
});
