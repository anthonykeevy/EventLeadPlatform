import { describe, expect, it } from "vitest";

import {
  buildComponentFootprintsForAiRuntime,
  recommendedMaxFootprintWidth,
} from "../buildAiRuntimeFootprints";
import type { FormDefinition } from "../../../types/builder.types";

describe("recommendedMaxFootprintWidth", () => {
  it("caps typical inputs on a wide canvas", () => {
    expect(recommendedMaxFootprintWidth("text", 1920)).toBe(560);
    expect(recommendedMaxFootprintWidth("textarea", 1920)).toBe(720);
    expect(recommendedMaxFootprintWidth("submit-button", 1920)).toBe(220);
  });
});

describe("buildComponentFootprintsForAiRuntime", () => {
  it("uses canvas-scale widths for empty form footprints (not toolbox thumbnail scale)", () => {
    const formDefinition: FormDefinition = {
      schemaVersion: "1.0",
      formId: "empty-ai-test",
      theme: {},
      canvasSettings: { width: 1920, height: 980, gridSize: 8 },
      pages: [{ id: "p1", title: "Page 1", components: [] }],
    };

    const footprints = buildComponentFootprintsForAiRuntime(formDefinition, 1, null);
    const text = footprints.find((f) => f.componentType === "text");
    expect(text).toBeDefined();
    expect(text!.width).toBe(560);
    expect(text!.height).toBeGreaterThanOrEqual(100);
    const textarea = footprints.find((f) => f.componentType === "textarea");
    expect(textarea).toBeDefined();
    expect(textarea!.height).toBeGreaterThanOrEqual(200);
    const submit = footprints.find((f) => f.componentType === "submit-button");
    expect(submit).toBeDefined();
    expect(submit!.width).toBe(220);
    expect(submit!.height).toBe(64);
  });
});
