# PDF Rotation and View Options — Research

**Purpose:** Research alternatives for rotating PDFs in browser embeds; document Edit View vs Prod View.  
**Context:** Story 5.7 Terms display; user wants rotation without CSS transform.  
**Created:** 2026-02-18  

---

## 1. Can We Send Keystrokes to the PDF Viewer?

**Question:** Can we programmatically send Ctrl+] / Ctrl+[ to Chrome's embedded PDF viewer to rotate?

**Answer: No.** Chrome's built-in PDF viewer runs in a sandboxed context. Key findings:

- The Chrome PDF viewer (`chrome-extension://` or internal) is **not accessible** to parent-page JavaScript.
- `iframe.contentDocument` is **null or cross-origin** when the iframe loads a PDF — we cannot access it.
- `dispatchEvent` on `contentDocument` fails (security) or has no effect — the viewer doesn't listen to synthetic events from the parent.
- Chrome's PDF viewer exposes only a limited `handleScriptingMessage` with `getAccessibilityJSON`, `getSelectedText`, `print`, `selectAll` — **no `sendKeyEvent` or rotation command**.
- Manually dispatching `KeyboardEvent` with `ctrlKey: true, key: ']'` does **not** reach the viewer.

**Conclusion:** Keystroke injection is not feasible for Chrome's native PDF viewer.

---

## 2. Why Not CSS Transform?

**Issue:** Applying `transform: rotate(90deg)` to the iframe wrapper rotates the entire viewer, not the PDF content.

- The PDF viewer's toolbar, zoom controls, and page navigation are also rotated.
- Layout and clipping can be wrong (e.g. left side cut off).
- The browser's PDF controls (fit-to-width, zoom, etc.) no longer behave as expected.
- User experience is degraded.

**Conclusion:** CSS transform is not a good solution and should be avoided.

---

## 3. Alternatives for PDF Rotation

| Approach | How It Works | Pros | Cons |
|----------|--------------|------|------|
| **PDF.js (Mozilla)** | Use `pdf.js` to render pages; `page.getViewport({ rotation: 90 })` for viewport; render to canvas. | Proper rotation baked into viewport; keeps full control. | Requires custom viewer (not a simple iframe); ~500KB+; more dev effort. |
| **Server-side (PyPDF2 / pypdf)** | Rotate PDF bytes on server; store/serve rotated copy. | Permanent fix; works with any viewer; no client changes. | New endpoint; storage for rotated version or on-the-fly transform. |
| **PDF.js built-in viewer** | Use `pdfjs-dist` + `pdf_viewer.js`; set `PDFViewerApplication.pdfViewer.pagesRotation`. | Built-in rotation API. | Heavier; must replace iframe with PDF.js viewer. |
| **Apryse / commercial** | Commercial SDK for PDF manipulation. | Full-featured. | Cost; vendor lock-in. |

---

## 4. PDF.js Rotation (Client-Side)

PDF.js supports rotation via the viewport when rendering to canvas:

```javascript
const viewport = page.getViewport({ scale: 1.5, rotation: 90 });
const context = canvas.getContext('2d');
page.render({ canvasContext: context, viewport });
```

- `rotation` accepts 0, 90, 180, 270.
- Requires building a custom viewer (render each page to canvas).
- If using the full PDF.js viewer: `PDFViewerApplication.pdfViewer.pagesRotation = 90` then refresh.

**Effort:** Medium–high. Need to add `pdfjs-dist`, implement or embed viewer.

---

## 5. Server-Side Rotation (Python)

Using PyPDF2 or pypdf:

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()
for page in reader.pages:
    page.rotate(90)  # 90, 180, 270
    writer.add_page(page)
with open("output.pdf", "wb") as f:
    writer.write(f)
```

**Options:**
- **On save:** When user clicks Save with rotation, call API that rotates the stored PDF and overwrites or stores rotated version.
- **On serve:** When serving PDF, apply rotation on-the-fly (cached) based on `display_rotation_degrees`.
- **Derived asset:** Store rotated PDF as a separate “display” version; original unchanged.

**Effort:** Medium. New API route, optional storage strategy.

---

## 6. Recommendation

| Phase | Action |
|-------|--------|
| **Now** | Remove CSS transform and keystroke attempts. Keep `display_rotation_degrees` in schema for future use. Implement Edit View vs Prod View (see §7). |
| **Short-term** | Server-side rotation (pypdf) — rotate on save or on serve. Simpler than PDF.js; works with native iframe. |
| **Long-term** | Consider PDF.js if we need a richer custom viewer (annotations, search, etc.). |

---

## 7. Edit View vs Prod View

**User need:** Two distinct modes when viewing Terms in Company Settings.

### Edit View (Configure)
- **Audience:** Company Admin configuring display.
- **Purpose:** Adjust size, orientation, and other display settings.
- **UI:** Size presets (Small/Medium/Large/Full), Rotate (when implemented), Save, page-navigation hint, Open in new tab.
- **Shown:** When admin is setting up how Terms will appear to form users.

### Prod View (Preview)
- **Audience:** Company Admin previewing the final result.
- **Purpose:** See exactly what form users will see.
- **UI:** Minimal — modal at configured size, PDF only, close button. No Size, Rotate, Save, or hints.
- **Shown:** Toggle or separate “Preview as customer” action.

**Implementation:** Add an “Edit” | “Prod view” toggle in the modal header. In Prod View, hide configuration controls and show only the PDF at the saved size with toolbar hidden (`toolbar=0`).

---

## 8. References

- Chrome PDF viewer: [Chromium PDF viewer base](https://chromium.googlesource.com/chromium/src/+/main/chrome/browser/resources/pdf/)
- PDF.js `getViewport`: [mozilla/pdf.js](https://github.com/mozilla/pdf.js) — `getViewport({ scale, rotation })`
- PyPDF2 / pypdf: [pypdf.readthedocs.io](https://pypdf.readthedocs.io/)
- Keystroke to iframe: [Stack Overflow: Fire keypress for PDF iframe](https://stackoverflow.com/questions/13307468/) — cross-origin restriction

---

*Research for Story 5.7 Terms display — use to guide rotation and view-mode implementation*
