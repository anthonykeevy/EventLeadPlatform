# UAT Checklist: T01

**Story:** 5.1  
**Task:** Asset Contracts + Config Foundations  
**Generated:** 2026-02-09

---

## Pre-conditions

- [ ] Repo checked out at task branch
- [ ] Editor can open backend + frontend files

## Test Steps

### AC1: Asset metadata contract exists (FE + BE)
- [ ] Step 1: Open `backend/modules/assets/asset_schemas.py` → Verify `BackgroundAssetMetadata` exists with assetId/assetKey/displayName/originalFilename/mimeType/byteSize/widthPx/heightPx/checksumSha256 fields.
- [ ] Step 2: Open `frontend/src/features/builder/types/builder.types.ts` → Verify matching `BackgroundAssetMetadata` interface fields.

### AC2: Placement contract is defined
- [ ] Step 1: In backend schema, verify `BackgroundPlacement` includes position/size and optional crop.
- [ ] Step 2: In TS types, verify `BackgroundPlacement` exists and `BackgroundDefinition` references it.

### AC3: Config keys are documented
- [ ] Step 1: Open `backend/common/constants.py` → Verify `forms.assets.images.*` keys are listed and defaults exist.

### AC4: Resolver contract is defined
- [ ] Step 1: Verify `BackgroundAssetResolver` exists in backend schemas (Protocol).
- [ ] Step 2: Verify `BackgroundAssetResolver` exists in TS types.

## Regression Check

- [ ] Verify no other files outside assets/types/constants were modified.

## Post-conditions

- [ ] Contracts are present and readable; no runtime behavior changes.

## Edge Cases (if applicable)

- [ ] Data URL guard expectation is documented in background contract comments.

---

**Instructions for Human Tester:**
1. Execute each step in order
2. Mark ✅ or ❌ for each item
3. Add notes for any failures
4. When complete, run `@ralf-uat *record-uat` with your results

