# Story 6.5 Feasibility Notes — Image-to-Form

**Date:** 2026-04-23 (revised same day to incorporate Tonyk's feedback re: GPT-5 mini, canvas preservation, PII risk)  
**Author:** Bob (SM Agent), desk research  
**Spike type:** Q17 (1-day feasibility check, agreed with Tonyk during 2026-04-23 PM/SM scope review)  
**Verdict (TL;DR):** ✅ **HIGH-CONFIDENCE FEASIBLE.** Recommend proceeding to story draft. Stay on the GPT-5 mini we already use; Story 6.5 inherits the cost/quality profile from the current text-prompt path.

---

## 1. Question we set out to answer

> *Can a multimodal LLM reliably convert a screenshot/photo of a form into a `FormSemanticPlan` (the same intermediate representation Story 6.3.1 produces from text prompts), so that the existing deterministic compiler and render-then-measure pipeline can produce a working form on the canvas?*

If yes, image-to-form becomes a transport-layer addition to the 6.3.1 architecture — not a new architectural surface. That's the bet that justified rescoping Story 6.5.

---

## 2. Findings (from vendor docs + third-party benchmarks)

### 2.1 Both major providers support this pattern in production today

| Provider | Vision model | Structured-output support | Cookbook for image→JSON | Verdict |
|----------|-------------|--------------------------|------------------------|---------|
| OpenAI | `gpt-4o` (and `gpt-4.1` family) | **Native** — `response_format` with JSON schema enforcement (GA since Sep 2024) | [OpenAI cookbook: Data extraction with GPT-4o](https://developers.openai.com/cookbook/examples/data_extraction_transformation/) — exact pattern, document image → structured JSON | ✅ Production-ready |
| Anthropic | `claude-3-5-sonnet` / `claude-opus-4-x` | Prompt-only schema (no native enforcement, but very reliable in practice) | Anthropic vision docs + Graphlit benchmark | ✅ Production-ready |

**Both** vendors support exactly the workflow we need: a single base64-encoded image → prompt with embedded target schema → structured JSON response.

### 2.2 Accuracy on document/form-style images

- Microsoft Azure team [published](https://techcommunity.microsoft.com/blog/azureforisvandstartupstechnicalblog/using-structured-outputs-in-azure-openai%E2%80%99s-gpt-4o-for-consistent-document-data-p/4261737) on GPT-4o + structured outputs for document extraction at production scale (invoices, complex tabular layouts).
- Graphlit's third-party benchmark of [Claude 3.5 Sonnet for document extraction](https://www.graphlit.com/blog/testing-claude-3-5-sonnet-for-document-text-extraction) reported Sonnet **more accurate than GPT-4o on tabular structure** — but with one specific weakness: **radio button selected state** (Claude sometimes picks the wrong option). This weakness *does not affect us* — we only need the form's *structure* (what fields exist, what type, what label, what options), not which option happened to be ticked in the source image.
- OpenAI's [GPT-4o Vision Guide](https://getstream.io/blog/gpt-4o-vision-guide/) demonstrates extraction of UI screenshots into structured JSON with the exact element-typing schema we'd need.

### 2.3 Token economics — and why we should stay on GPT-5 mini

**Tonyk asked: can GPT-5 mini handle images, and do we need to downgrade to GPT-4o?**

Answer: **Yes, GPT-5 mini supports vision natively** (confirmed via [OpenAI's models docs](https://developers.openai.com/api/docs/models): *"All latest OpenAI models support text and image input"* and [GPT-5 mini API documentation](https://www.segmind.com/models/gpt-5-mini/api): *"This model supports vision capabilities. You can include images in your requests."*). Multimodal input format is identical to GPT-4o (`type: "image_url"` content block).

**Therefore: NO downgrade required.** Story 6.5 should keep using the same `gpt-5-mini` model the platform is already calibrated against. This is a meaningful win — we avoid:
- Re-running the entire UAT/calibration baseline on a different model (which is what swapping to 4o would force)
- A second prompt-tuning effort to compensate for any model behavioral differences
- Cost regression (gpt-5-mini ~$0.25/M input vs gpt-4o ~$5/M — ~20× cheaper)

**Combination strategy** (in case Story 6.5 dev UAT reveals a vision-specific accuracy gap on 5-mini):
- Stay on `gpt-5-mini` for **text-prompt path** (Story 6.3.1 + Story 6.4 baseline — proven, calibrated)
- Add a **vendor/model selector at the OutboundTransport layer keyed on generation source** (text vs image), so image-mode could fall back to `gpt-5` (full) or `gpt-4o` *only for the image path*, leaving the text path untouched
- Decision gate: if 5-mini scores ≥80% on the image-mode UAT benchmark (≥4 of 5 source-image fixtures producing usable forms), keep 5-mini for both paths. Only fall back to a larger model if accuracy demands it.
- This means **the text path UAT baseline is never invalidated by image-mode work** — Story 6.4's calibration is preserved.

**Token economics on `gpt-5-mini` (revised):**
- GPT-5 family image tokenization: 70 base + 140 per 512px tile (per OpenAI docs §2.5 of vision guide).
- Typical 1024×768 form screenshot → ~6–9 tiles ≈ **~900–1,330 tokens for the image alone**.

| Component | Tokens |
|-----------|--------|
| Image (high detail, gpt-5 tile cost) | ~1,200 |
| Capability snapshot + prompt template + schema | ~3,000 |
| Output (FormSemanticPlan JSON) | ~1,500 |
| **Total** | **~5,700** |

At `gpt-5-mini` pricing (~$0.25/M input, output pricing TBC but in the same order) that's roughly **$0.002–$0.005 per generation** — **an order of magnitude cheaper** than the GPT-4o estimate I gave in the first draft. Not a cost concern in any direction.

### 2.4 Architectural fit with Story 6.3.1

The 6.3.1 pipeline is:

```
Text prompt
    │
    ▼
[ Outbound transport ] ──► LLM ──► FormSemanticPlan (Pydantic)
    │
    ▼
[ Deterministic Compiler (Python) ] ──► DefinitionJSON with geometry
    │
    ▼
[ Render-then-measure round-trip ] ──► final layout
    │
    ▼
[ Validation ] ──► canvas
```

Image-to-form changes **only the first two boxes**:

```
Image upload (PNG/JPG)
    │
    ▼
[ Outbound transport — multimodal mode ] ──► LLM ──► FormSemanticPlan ◄── unchanged from here down
```

Everything from `FormSemanticPlan` onward — the compiler, the render-then-measure round-trip, the validation contract, the capability snapshot governance, the GenerationRun/GenerationArtifact recording — runs **unchanged**. That is exactly the win we hoped for when we set the question.

### 2.5 Failure modes and known mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| Phone photos with perspective skew, glare, low resolution | M | UX copy steers users toward screenshots / flat scans first. Document "best results from a clean screenshot" in the upload modal. Reject images below a minimum resolution at upload time. |
| Hallucinated fields not present in source | M | Prompt instructs model to extract only visible elements + flag uncertainty. User can delete unwanted fields via existing builder tools. Generation logged in `GenerationArtifact` for inspection. |
| **PII captured in source image (NEW — per Tonyk 2026-04-23)** | **M–H** | Source images may contain real personal data when users screenshot a competitor's form they've part-filled, or photograph a real-world paper form already filled in by a person. Mitigation has two parts: **(a) detection** — run a PII-detection pass (either a regex sweep on extracted text + a lightweight vision-LLM check for handwritten names/numbers, OR a managed service like Azure/AWS Comprehend PII) before the image is persisted; **(b) classification** — store a `pii_status` flag on the persisted image record (`none` / `mock_data` / `real_data_detected`) and surface it in the AI Agent panel UI so the user can choose to delete the image after generation. **Mock vs. real differentiation** likely needs an explicit "Is this mock data?" checkbox on the upload UI as a user-asserted ground truth, plus the automated detection as a second-line check. Detailed design will live in Story 6.5; this risk and its detection layer should be a first-class AC, not an afterthought. |
| Multi-page paper forms exceeding single-image capacity | L (MVP) | MVP scope: **single image, single form**. Multi-image stitching deferred. Documented out-of-scope. |
| LLM emits component types we don't render | L | **Already solved by 6.3.1's Capability Snapshot Rule** — `allowed_components` is injected into the prompt; the validation contract rejects any out-of-snapshot types and the compiler will not emit them. |
| User uploads a non-form image (selfie, meme, blank screenshot) | L | Pre-flight LLM call ("does this image contain a form?") OR rely on `FormSemanticPlan` returning empty/near-empty — UI shows "couldn't detect any form fields" + retry. |
| Cost spike from large images | L | Cap image upload at 5MB; downsize to ≤2048px longest side server-side before sending. |

None of these are deal-breakers. The PII risk is the one new requirement that needs first-class design treatment in Story 6.5 — see §3.3 below.

### 2.6 Canvas-size preservation when replacing an embedded form (NEW — per Tonyk 2026-04-23)

**Tonyk's question:** *"If the user wants to replace a form that has been embedded in their site, would we be able to set the canvas size to the same space currently used by the existing form?"*

**Answer: yes, and this naturally falls out of the architecture if we adopt one design principle:**

> **Image provides structure; current canvas provides dimensions.**

Story 6.3.1's compiler is already canvas-responsive — `WidthClassPolicyVersion` resolves width intents (`compact`/`half`/`full`) against the **current canvas settings** (width and grid). Image-to-form should **inherit, not infer, canvas dimensions**:
- If the user uploads an image while the canvas is **non-empty** (the typical "replace my embedded form" path) → preserve the existing canvas width/height/grid; pass them to the compiler unchanged.
- If the user uploads an image while the canvas is **empty** (first-time use) → use the user's default canvas settings (or the new-form template defaults), again **never** inferring from the image. The image's pixel dimensions are about the screenshot, not the embed target.

This means the existing replace-form warning from Story 6.4 (§2.2) does double duty here: it both warns about the destructive action AND signals that canvas dimensions will be preserved. A small note in the warning copy when the trigger is image-mode is sufficient: *"This will replace your form. Your current canvas size will be kept (so anything embedded on your site keeps fitting)."*

**Implication for Story 6.5 design:** the image-to-form endpoint accepts the current canvas settings as part of the request payload (already in the request shape for the text path — verify, don't refactor). No new compiler logic. No new types. This is essentially a "free" feature that emerges from doing the integration cleanly.

---

## 3. Recommended implementation approach for Story 6.5

### 3.1 Provider selection (revised per Tonyk 2026-04-23)

**Primary: GPT-5 mini** — the model the platform is already calibrated against from Story 6.3.1 + Story 6.4 work. Vision support is native and pricing is ~20× cheaper than GPT-4o. **No model swap, no re-calibration round.**

**Internal fallback (within the OpenAI/GPT family): GPT-5 (full) or GPT-4o for image-mode only**, only if dev UAT shows 5-mini scoring below the bar on the image benchmark. Text-mode stays on 5-mini regardless. This is implemented by extending the existing OutboundTransport's model-resolution logic to be aware of `generation_source` (text vs image) — small, local change.

**Out of scope: Claude as a vendor.** Tonyk's preference is to stay within the GPT family for MVP given the existing investment, calibration, and operational comfort. Revisit post-MVP only if a clear pricing/accuracy gap emerges.

### 3.2 Endpoint shape (proposed for the story)

```
POST /api/forms/{form_id}/ai/generate-from-image
Content-Type: multipart/form-data
Body:
  - image: file (png|jpg|webp, ≤5MB)
  - context_hint: string (optional, max 500 chars — e.g. "this is a job application form")
  - is_mock_data: boolean (user-asserted ground truth: "this image contains no real PII"; defaults to false)
  - canvas_width / canvas_height / grid: numeric (optional — server falls back to current form's canvas if omitted; per §2.6 "image provides structure; current canvas provides dimensions")

Response:
  - GenerationRun id (recorded as `generation_source: "image"`)
  - FormSemanticPlan (same shape as text path)
  - pii_status: "none" | "mock_data" | "real_data_detected" (informational; UI surfaces this so user can choose to delete the stored image)
  - Then the existing render-then-measure round-trip kicks in
```

This is **one new endpoint** plus **one new prompt template** plus **a multipart upload UI panel** plus **a PII detection step** (see §3.3). Database-wise: add a `generation_source` column to `GenerationRun`, plus a small `GenerationSourceImage` table (image bytes path / `pii_status` / `is_mock_data` / linked `GenerationRunID`).

### 3.3 PII detection + mock-vs-real differentiation (NEW — first-class per Tonyk 2026-04-23)

This is a non-trivial design point that deserves its own AC bundle in Story 6.5. Outline of the recommended approach:

| Layer | What it does | Implementation approach |
|-------|--------------|------------------------|
| **User-asserted (ground truth)** | "Is this image mock/sample data only?" checkbox on the upload panel — user must affirm. Default: unchecked (i.e. "treat as potentially real"). | Plain UI checkbox; passes through as `is_mock_data` on the request. |
| **Automated detection (defence in depth)** | Run after upload, before persistence. Two-pass: **(1)** lightweight regex sweep on any text the LLM extracts from the image (emails, phone patterns, credit-card-like sequences, names matching common-name dictionary). **(2)** A second small LLM call: *"Does this image contain personally identifiable information (e.g. names, emails, phone numbers, addresses, signatures, faces)?"* — yes/no with confidence. | Backend service, single new module (`backend/modules/form_ai/pii_detector.py`). Logs results to `GenerationArtifact`. |
| **Classification & response** | Combine: `pii_status = "mock_data"` if user asserted AND no high-confidence PII detected; `pii_status = "real_data_detected"` if either user did not assert OR detection flagged with high confidence; `pii_status = "none"` only if user asserted AND detection found nothing. | Calculated server-side; returned in API response and persisted. |
| **Storage policy** | All images persisted by default (per Tonyk's 4.1). When `pii_status = "real_data_detected"`, surface a banner on the UI: *"This image appears to contain real personal data. We've stored a copy linked to your form. [Delete image now]"* — one-click deletion endpoint that nulls the bytes path on the storage row but keeps the `GenerationRun` record for audit. | Plus standard retention policy (TBD with PM) — e.g. auto-delete real-data images after 30 days. |
| **Audit trail** | Every PII detection result + user assertion is logged. Admin can later query "show me all uploads flagged real-data". | Lives on `GenerationSourceImage.pii_status` + `GenerationArtifact` rows. |

**Why this matters:** without the differentiation layer, every persisted image is treated as potentially-PII, which is overly conservative and noisy. With explicit user assertion + automated detection, mock/test/sample images stay clean and real-data images get the attention they deserve.

**Effort impact on story sizing:** PII detection adds ~1–2 days (mostly the second-pass LLM check + UI banner + deletion endpoint). Story stays at M.

### 3.4 Story sizing (revised)

- Endpoint + transport extension (with model-aware fallback per §3.1): ~2 days
- Prompt template + capability snapshot integration: ~1 day
- Frontend upload UI + integration with existing AI panel + canvas-preservation wiring: ~2 days
- PII detection layer + UI surfacing per §3.3: ~1.5 days
- Storage of source image + `GenerationSourceImage` table + deletion endpoint: ~1 day
- UAT (2–3 rounds — single-variable per round per the Multi-Round UAT Protocol): ~2–3 days
- Closeout report (MANDATORY — schema migrations + new endpoint = both criteria triggered) + governance hygiene: ~1 day

**Estimate: 10–12 working days (M).** Slightly larger than the first-draft estimate of 8–10 days — the PII layer accounts for the difference. Still comparable to Story 6.2.2 + 6.3.1 in shape.

### 3.5 What the story does NOT need to invent

- ❌ No new Pydantic model for `FormSemanticPlan` (reused unchanged)
- ❌ No compiler changes
- ❌ No render-then-measure changes
- ❌ No capability/validation/width policy changes
- ❌ No new validation contract surface
- ❌ No model swap or text-path re-calibration (5-mini stays primary for both modes)

That's the architecture leverage we bought with Story 6.3.1, plus the model-stability win we keep by staying on 5-mini.

---

## 4. Decisions logged (Tonyk 2026-04-23)

All open questions answered. Captured here as the authoritative input to the Story 6.5 draft.

| # | Question | Decision | Notes |
|---|----------|----------|-------|
| 4.1 | Persist uploaded source image? | ✅ **Yes — persist locally** | Plus add PII detection step (see §3.3) and `is_mock_data` user assertion to differentiate test images from real data. PII handling is now a first-class AC bundle for Story 6.5, not an afterthought. |
| 4.2 | Re-use Story 6.4 replace-form warning when image upload would replace existing canvas? | ✅ **Yes — same warning** | Plus extend warning copy to mention canvas-size preservation per §2.6 ("Your current canvas size will be kept so anything embedded on your site keeps fitting"). Inherits the "don't show again" preference from 6.4 cleanly. |
| 4.3 | GPT family only (no Claude in MVP)? | ✅ **Yes — GPT family only** | Specifically: stay on GPT-5 mini as primary (already calibrated). Internal fallback to GPT-5 (full) or GPT-4o for image-mode only if 5-mini scores below the bar on UAT. **No model swap of the text path** — keeps Story 6.4 baseline intact. |
| 4.4 | Image preprocessor — upload-and-go or in-product cropping/rotation? | ✅ **Upload-and-go** | UI hint copy steers toward clean screenshots. In-product image editing deferred until usage data shows demand. |
| 4.5 | Canvas size when replacing existing form? *(NEW — raised by Tonyk in feedback)* | ✅ **Preserve existing canvas dimensions** | Design principle: *"Image provides structure; current canvas provides dimensions."* See §2.6. Falls naturally out of Story 6.3.1's canvas-responsive compiler — essentially a free feature with one-line wiring on the request payload. |

---

## 5. Verdict (revised 2026-04-23 after Tonyk feedback)

**Proceed to Story 6.5 draft.** Confidence is now even higher than the first draft because:

1. **No model swap required.** GPT-5 mini handles vision natively — Story 6.4's calibration baseline carries forward to Story 6.5 without re-tuning. Saves an entire UAT round and keeps the cost profile ~20× cheaper than the GPT-4o option I originally suggested.
2. **Canvas-size preservation falls out for free.** The "image provides structure; current canvas provides dimensions" principle means the existing compiler does the work — image-to-form for embedded-form replacement is a one-line wiring change on the request payload, not new architecture.
3. **PII handling has a concrete shape.** The two-layer approach (user assertion + automated detection) gives users control while protecting against accidental real-data uploads. Adds ~1.5 days to the story but is genuinely first-class.

The 1-day feasibility budget did not need a code spike — vendor docs gave a confident answer in desk-research time. Saved capacity recommended use: an extra UAT round on Story 6.4 polish (the polish UI is the user's first impression of the panel — worth getting right) and a small calibration spike at the start of Story 6.5 to confirm 5-mini's vision accuracy against 3–5 representative form screenshots before Dev commits to the full story.

---

## 6. Sources

### GPT-5 mini vision (primary path)
- OpenAI Models index: [Models | OpenAI API](https://developers.openai.com/api/docs/models) — *"All latest OpenAI models support text and image input"*
- Segmind GPT-5 mini API docs: [GPT-5 Mini API Documentation](https://www.segmind.com/models/gpt-5-mini/api) — confirms multimodal request format
- OpenAI: [Images and vision guide](https://developers.openai.com/api/docs/guides/images-vision) — image tokenization, detail levels, cost calculation
- OpenAI cookbook: [Multimodal document understanding tips](https://developers.openai.com/cookbook/examples/multimodal/document_and_multimodal_understanding_tips) — `detail: "original"` for dense pages, reasoning effort for compositional answers

### General multimodal patterns
- OpenAI cookbook: [Data extraction & transformation with vision](https://developers.openai.com/cookbook/examples/data_extraction_transformation/)
- GetStream: [GPT-4o Vision Guide — Building with OpenAI's Image API](https://getstream.io/blog/gpt-4o-vision-guide/) — UI-screenshot extraction template
- Microsoft Azure tech blog: [Structured Outputs in GPT-4o for document data processing](https://techcommunity.microsoft.com/blog/azureforisvandstartupstechnicalblog/using-structured-outputs-in-azure-openai%E2%80%99s-gpt-4o-for-consistent-document-data-p/4261737)
- Microsoft Learn: [GPT-4o PDF extraction sample](https://learn.microsoft.com/en-us/samples/azure-samples/azure-openai-gpt-4-vision-pdf-extraction-sample/using-azure-openai-gpt-4o-to-extract-structured-json-data-from-pdf-documents/)

### Cross-vendor reference (out-of-MVP-scope but useful for context)
- Anthropic: [Claude vision API docs](https://docs.anthropic.com/claude/docs/vision)
- Graphlit benchmark: [Testing Claude 3.5 Sonnet for document text extraction](https://www.graphlit.com/blog/testing-claude-3-5-sonnet-for-document-text-extraction)

---

*Feasibility notes — Story 6.5 (Image-to-Form)*  
*Author: Bob (SM Agent) · Date: 2026-04-23 (revised same day per Tonyk feedback: GPT-5 mini stays primary, canvas preservation principle added, PII handling promoted to first-class) · Q17 desk-research spike*
