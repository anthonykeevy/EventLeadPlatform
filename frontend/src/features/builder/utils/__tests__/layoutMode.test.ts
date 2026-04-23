import { describe, expect, it } from "vitest";

import {
  HORIZONTAL_LAYOUT_MIN_WIDTH_PX,
  applyMobileLayoutDowngrade,
  resolveLayoutModeForRequest,
} from "../layoutMode";

/**
 * Story 6.3.1 (UAT round 6) — Phase 1 + Phase 1 *completion*.
 *
 * Two helpers, one rule. ``resolveLayoutModeForRequest`` decides what value
 * we *send to the LLM/compiler* for one generation;
 * ``applyMobileLayoutDowngrade`` decides what value the *renderer* paints
 * with for the active preview canvas. Both share the same 600 px
 * threshold so "what we asked for" and "what we render" stay in lockstep.
 */
describe("layoutMode helpers", () => {
  it("exposes the documented threshold (600px)", () => {
    expect(HORIZONTAL_LAYOUT_MIN_WIDTH_PX).toBe(600);
  });

  // -------------------------------------------------------------------------
  // resolveLayoutModeForRequest — AI request side
  // -------------------------------------------------------------------------
  describe("resolveLayoutModeForRequest (horizontal stored)", () => {
    const horizontalGlobalStyles = { defaultObjectLayout: "horizontal" };

    it("downgrades on a 375px mobile-preview canvas", () => {
      const d = resolveLayoutModeForRequest(horizontalGlobalStyles, 375);
      expect(d.downgraded).toBe(true);
      expect(d.layout).toBe("vertical");
      expect(d.originalLayout).toBe("horizontal");
    });

    it("downgrades on the upper edge of the mobile band (414px)", () => {
      const d = resolveLayoutModeForRequest(horizontalGlobalStyles, 414);
      expect(d.downgraded).toBe(true);
      expect(d.layout).toBe("vertical");
    });

    it("downgrades just below the threshold (599px)", () => {
      const d = resolveLayoutModeForRequest(horizontalGlobalStyles, 599);
      expect(d.downgraded).toBe(true);
      expect(d.layout).toBe("vertical");
    });

    it("keeps horizontal exactly at the threshold (600px)", () => {
      const d = resolveLayoutModeForRequest(horizontalGlobalStyles, 600);
      expect(d.downgraded).toBe(false);
      expect(d.layout).toBe("horizontal");
    });

    it("keeps horizontal on a tablet canvas (768px)", () => {
      const d = resolveLayoutModeForRequest(horizontalGlobalStyles, 768);
      expect(d.downgraded).toBe(false);
      expect(d.layout).toBe("horizontal");
    });

    it("keeps horizontal on a desktop canvas (1920px)", () => {
      const d = resolveLayoutModeForRequest(horizontalGlobalStyles, 1920);
      expect(d.downgraded).toBe(false);
      expect(d.layout).toBe("horizontal");
    });

    it("never downgrades on a non-finite canvas width", () => {
      const d = resolveLayoutModeForRequest(horizontalGlobalStyles, Number.NaN);
      expect(d.downgraded).toBe(false);
      expect(d.layout).toBe("horizontal");
    });
  });

  describe("resolveLayoutModeForRequest (non-horizontal stored)", () => {
    it("returns vertical untouched even on a tiny canvas", () => {
      const d = resolveLayoutModeForRequest(
        { defaultObjectLayout: "vertical" },
        320
      );
      expect(d.downgraded).toBe(false);
      expect(d.layout).toBe("vertical");
    });

    it("preserves an unknown / future layout token", () => {
      const d = resolveLayoutModeForRequest(
        { defaultObjectLayout: "mixed" },
        320
      );
      expect(d.downgraded).toBe(false);
      expect(d.layout).toBe("mixed");
    });

    it("returns undefined when no defaultObjectLayout set", () => {
      const d = resolveLayoutModeForRequest({}, 320);
      expect(d.downgraded).toBe(false);
      expect(d.layout).toBeUndefined();
    });

    it("handles null globalStyles", () => {
      const d = resolveLayoutModeForRequest(null, 320);
      expect(d.downgraded).toBe(false);
      expect(d.layout).toBeUndefined();
    });

    it("handles undefined globalStyles", () => {
      const d = resolveLayoutModeForRequest(undefined, 320);
      expect(d.downgraded).toBe(false);
      expect(d.layout).toBeUndefined();
    });
  });

  // -------------------------------------------------------------------------
  // applyMobileLayoutDowngrade — renderer side
  // -------------------------------------------------------------------------
  describe("applyMobileLayoutDowngrade", () => {
    it("returns the SAME object reference when no downgrade is needed", () => {
      // React shallow-equality matters here: forcing a new object on every
      // render would invalidate every memo downstream of globalStyles.
      const styles = {
        defaultObjectLayout: "horizontal" as const,
        primaryColor: "#abc",
      };
      const out = applyMobileLayoutDowngrade(styles, 1920);
      expect(out).toBe(styles); // referential equality
    });

    it("returns the SAME reference for non-horizontal stored layouts", () => {
      const styles = { defaultObjectLayout: "vertical" as const };
      expect(applyMobileLayoutDowngrade(styles, 320)).toBe(styles);
      expect(applyMobileLayoutDowngrade(styles, 1920)).toBe(styles);
    });

    it("returns the SAME reference when no defaultObjectLayout is set", () => {
      const styles = { primaryColor: "#abc" };
      expect(applyMobileLayoutDowngrade(styles, 320)).toBe(styles);
    });

    it("downgrades to vertical on a 375px mobile preview canvas", () => {
      const styles = {
        defaultObjectLayout: "horizontal" as const,
        primaryColor: "#abc",
        baseSpacing: 8,
      };
      const out = applyMobileLayoutDowngrade(styles, 375);
      expect(out).not.toBe(styles); // new reference (object changed)
      expect(out.defaultObjectLayout).toBe("vertical");
      // Every other field is preserved exactly.
      expect(out.primaryColor).toBe("#abc");
      expect(out.baseSpacing).toBe(8);
    });

    it("downgrades just below the threshold (599px)", () => {
      const styles = { defaultObjectLayout: "horizontal" as const };
      expect(applyMobileLayoutDowngrade(styles, 599).defaultObjectLayout).toBe(
        "vertical"
      );
    });

    it("keeps horizontal exactly at the threshold (600px)", () => {
      const styles = { defaultObjectLayout: "horizontal" as const };
      const out = applyMobileLayoutDowngrade(styles, 600);
      expect(out).toBe(styles);
      expect(out.defaultObjectLayout).toBe("horizontal");
    });

    it("does NOT mutate the input object", () => {
      const styles: { defaultObjectLayout: string; primaryColor: string } = {
        defaultObjectLayout: "horizontal",
        primaryColor: "#abc",
      };
      applyMobileLayoutDowngrade(styles, 375);
      expect(styles.defaultObjectLayout).toBe("horizontal"); // untouched
    });

    it("returns null when given null", () => {
      expect(applyMobileLayoutDowngrade(null, 375)).toBeNull();
    });

    it("returns undefined when given undefined", () => {
      expect(applyMobileLayoutDowngrade(undefined, 375)).toBeUndefined();
    });

    it("never downgrades on a non-finite canvas width", () => {
      const styles = { defaultObjectLayout: "horizontal" as const };
      expect(applyMobileLayoutDowngrade(styles, Number.NaN)).toBe(styles);
    });
  });

  // -------------------------------------------------------------------------
  // The two helpers must agree pixel-for-pixel: "what we ask for" and "what
  // we paint" can never drift. If we ever add a new threshold band here,
  // both helpers should pick it up at the same time.
  // -------------------------------------------------------------------------
  describe("AI request and renderer agree on every threshold", () => {
    const stored = { defaultObjectLayout: "horizontal" as const };
    const widths = [200, 320, 375, 414, 480, 599, 600, 768, 1024, 1920];
    for (const w of widths) {
      it(`agree at ${w}px`, () => {
        const requestSide = resolveLayoutModeForRequest(stored, w);
        const renderSide = applyMobileLayoutDowngrade(stored, w);
        const renderDowngraded = renderSide !== stored;
        expect(renderDowngraded).toBe(requestSide.downgraded);
      });
    }
  });
});
