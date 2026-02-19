# Asset Management — Platform Review

**Purpose:** Research how other platforms handle assets, asset types, and document/terms integration.  
**Context:** Story 5.7 Company Settings Hub; EventLead asset taxonomy (IMAGE, DOCUMENT, TERMS, etc.)  
**Created:** 2026-02-17  

---

## 1. Executive Summary

Platforms typically use **MIME-based or semantic asset types** and support **images, documents, and videos**. Terms of Service / consent documents are usually handled as **linked documents** (PDF), stored in media libraries or document repositories. Event/form platforms often separate **branding assets** from **legal documents**.

---

## 2. Digital Asset Management (DAM) Systems

### 2.1 Core Asset Categories

DAM systems typically use these primary types:

| Type | Description | MIME Examples | Notes |
|------|-------------|---------------|-------|
| **Image** | Static visuals | image/jpeg, image/png, image/webp, image/svg+xml | Thumbnails, dimensions, format conversion |
| **Video** | Moving media | video/mp4, video/mpeg | Streaming, transcoding |
| **Document/File** | Business docs, PDFs | application/pdf, application/msword | Any non-image/non-video |
| **Audio** | Sound clips | audio/mpeg, audio/wav | Podcasts, voiceovers |

### 2.2 Semantic / Business Asset Types

Beyond MIME, platforms add **semantic types** for business use:

| Platform | Approach | Examples |
|----------|----------|----------|
| **Oracle Content Cloud** | Seeded + custom types | Auto-assign from MIME; custom e.g. "Marketing-Images" with required metadata |
| **Adobe AEM Assets** | Rich metadata, derivatives | Primary + derivatives (thumbnails, optimized), sub-assets |
| **Sanity** | `image` vs `file` types | Images: JPG, PNG, WebP, SVG, GIF; Files: PDF, docs, archives, videos |
| **Contentful** | Media assets | Images, video, audio; managed via API and web app |

**Idea for EventLead:** Combine **MIME-based** storage (technical) with **semantic types** in ref.AssetType (IMAGE, DOCUMENT, TERMS, VIDEO) for UI and business rules.

---

## 3. Form Builder Platforms

### 3.1 Jotform

- **Image library:** "My Images" — reusable uploads across forms  
- **Sources:** Device upload, URL, or library  
- **Elements:** Image (logo, banner), Image Picker, Image Gallery  
- **Limitation:** Widgets favour URL; full library access in standard fields  

### 3.2 Terms / Consent Documents

- **WPForms, Gravity Forms, Jotform:** Checkbox + link to terms PDF  
- **Pattern:** Upload PDF to media library → embed link in checkbox text  
  ```html
  I agree to the <a href="https://example.com/Terms.pdf" target="_blank">Terms of Service</a>
  ```  
- **Implication:** Terms stored as **documents** in an asset/media library; form references by URL or asset ID.

---

## 4. Event Management Platforms

### 4.1 EventMobi

- **Document types:** .doc, .docx, .ppt, .pptx, .xls, .xlsx, .pdf, .jpeg, .png, .bmp, .webp  
- **Max size:** 150 MB per document  
- **Use:** Central library; attach to profiles, sessions, sections; role-based access  

### 4.2 EventBuilder

- **Asset types:** Slides, videos, PDFs, images  
- **Features:** Metadata, tagging, search, presenters can upload during events  
- **Restrictions:** Files &lt; 500 MB; filenames without non-ASCII  

### 4.3 Branding / White-label

- **Certain, Accelevents:** Logo, colours, typography, custom domains  
- **Assets:** Logo variants (colour, reverse, icon), font specs, brand colours  
- **Legal:** Brand guidelines as PDF; separate from runtime assets  

---

## 5. HubSpot & Enterprise

### 5.1 HubSpot

- **Files tool:** Branding assets (logos, icons, banners); most file types; up to 2 GB (paid)  
- **Documents tool:** .pptx, .pdf, .docx, .xlsx only — for sharing with contacts, engagement tracking  
- **Brand association:** Assets tied to brand domains, forms, pages  
- **Separation:** Branding files vs documents for sharing/compliance  

### 5.2 Salesforce

- **Assets:** Files, documents, Chatter; org-level and record-level  
- **Types:** ContentVersion for file storage; ContentDocument for metadata  

---

## 6. Ideas for EventLead

### 6.1 Asset Type Taxonomy

| TypeCode | Description | Use Case | Dimensions |
|----------|-------------|----------|------------|
| **IMAGE** | Logos, backgrounds, icons | Form Builder, branding | WidthPx, HeightPx required |
| **DOCUMENT** | PDFs, Word, Excel | General docs, slides | WidthPx, HeightPx nullable |
| **TERMS** | Terms of Service, Privacy Policy | Consent checkboxes | Same as DOCUMENT; semantic subtype |
| **VIDEO** | Future: video backgrounds | Rich media | Optional dimensions |

**Alternatives:**
- **Single DOCUMENT type** — TERMS as metadata/category on DOCUMENT  
- **Separate TERMS type** — Explicit for consent linking, clearer in Company Settings UI  

### 6.2 Terms-of-Agreement Pattern

- Store Terms PDF in Asset (AssetType=TERMS or DOCUMENT)  
- Form consent component references `assetId` or `assetKey`  
- Company Settings Assets tab: upload, list, delete Terms documents  
- Future: "Default Terms" in Company–Asset defaults  

### 6.3 Organization Patterns

| Pattern | Pros | Cons |
|---------|------|------|
| **MIME-only** | Simple, standard | No business semantics |
| **Semantic types (IMAGE, DOCUMENT, TERMS)** | Clear UI, domain rules | More ref data to maintain |
| **CompanyAsset relationship table** | Company-level defaults per asset type | New table; migration |
| **Tags/categories on Asset** | Flexible | Weaker structure, harder queries |

### 6.4 Recommendations

1. **ref.AssetType:** Add `DOCUMENT` and `TERMS` (or `DOCUMENT` with TERMS as a category).  
2. **Asset:** WidthPx/HeightPx nullable for non-image types.  
3. **Terms linking:** Consent component stores `assetRef` (e.g. `asset:{id}`) — same pattern as form backgrounds.  
4. **Company Settings:** Assets tab with filters by type (Images | Terms | Documents).  
5. **Future:** CompanyAsset or CompanyAssetDefaults for per-company policies (max size, required Terms, etc.).  

---

## 7. Summary Table

| Platform | Image | Document | Terms/Legal | Video | Organisation |
|----------|-------|----------|-------------|-------|--------------|
| DAM (Oracle, Adobe) | ✅ Primary | ✅ File type | — | ✅ Primary | MIME + custom types |
| Sanity | ✅ image type | ✅ file type | — | In file | image vs file |
| Jotform | ✅ My Images | — | Link to external | — | Reusable library |
| EventMobi | ✅ | ✅ Office + PDF | — | — | Central repo, metadata |
| HubSpot | ✅ Files | ✅ Docs (4 formats) | — | — | Brand vs Documents |
| EventLead (current) | ✅ IMAGE | — | — | — | Asset.CompanyID, AssetType |

---

*Last Updated: 2026-02-17*
