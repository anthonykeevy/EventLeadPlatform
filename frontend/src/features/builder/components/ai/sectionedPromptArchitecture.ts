export type PromptSectionId =
  | "layout"
  | "data_collection"
  | "validation_rules"
  | "appearance"
  | "logic"
  | "delivery_summary";

export interface PromptSection {
  id: PromptSectionId;
  title: string;
  objective: string;
  instructions: string[];
}

// Story 6.3.1: the deterministic compiler now owns ALL layout, sizing, and
// styling. The LLM only emits a FormSemanticPlan (component types, labels,
// validation intent, semantic grouping). The sections below intentionally
// avoid any instructions about coordinates, pixel widths, canvas bounds, or
// styles — those used to drift the model into emitting layout it cannot
// influence (and into trusting `componentFootprints` types the capability
// snapshot rejects).
const SECTION_DEFINITIONS: PromptSection[] = [
  {
    id: "layout",
    title: "Semantic Grouping",
    objective:
      "Express intent only — the deterministic compiler computes positions, widths, and canvas size.",
    instructions: [
      "Do NOT emit position, x/y, pixel widths, style blocks, or canvasSettings — the compiler owns all geometry.",
      "Group related fields by setting the same `section` (e.g. \"contact\", \"company\") on consecutive components.",
      "Use `rowGroup` on two adjacent components when they should sit side-by-side on the same row.",
      "`widthIntent` is a HINT (compact | half | full) — choose only from the values listed in ALLOWED COMPONENT TYPES for that type. The deterministic compiler decides the final pixel width from a per-type tier table and may shrink the component further or wrap it onto its own row to make the layout fit. Treat widthIntent as a *cap*: pick \"compact\" for short content (zip, age, state code), \"full\" only when the field truly should span the row.",
    ],
  },
  {
    id: "data_collection",
    title: "Data Collection",
    objective: "Capture requested fields/options with stable ids and tab order.",
    instructions: [
      "Use only `componentType` values listed in ALLOWED COMPONENT TYPES; if a requested feature has no registered type, pick the closest type and explain in helpText.",
      "Include all requested fields exactly once unless prompt asks for duplicates.",
      "Use explicit labels, placeholders, and options where relevant.",
      "Tab order is implied by component order in the array; sequence them in visual reading order.",
    ],
  },
  {
    id: "validation_rules",
    title: "Validation Rules",
    objective: "Define clear validation behavior for each input.",
    instructions: [
      "Emit `validationIntent` as an OBJECT (e.g. {\"required\": true, \"email\": true}) — never an array of strings.",
      "Apply required/format constraints per field type (email, phone, required text).",
      "Use only the keys allowed for the type by the registered validation contract.",
      "Omit `validationIntent` entirely for components that do not need validation (e.g. submit-button, header).",
    ],
  },
  {
    id: "appearance",
    title: "Theming Hands-Off",
    objective: "Do not touch styling — the canvas owns theme, colours, fonts, and component dimensions.",
    instructions: [
      "Do NOT emit `theme`, `globalStyles`, `style`, `width`, `height`, or any colour/font keys.",
      "lockedGlobals in runtimeContext are read-only context; never mirror or mutate them in the plan.",
      "Visual parity is guaranteed by the deterministic compiler + canvas — your job is semantics, not appearance.",
    ],
  },
  {
    id: "logic",
    title: "Logic Rules",
    objective: "Attach only necessary logic with valid source/target references.",
    instructions: [
      "Include logic only when required by prompt or obvious UX necessity.",
      "Ensure source and target component ids exist and are not identical.",
      "Use valid operator/action pairs compatible with schema and runtime.",
      "Keep logic minimal and deterministic.",
    ],
  },
  {
    id: "delivery_summary",
    title: "Delivery Summary",
    objective: "Return one valid FormSemanticPlan JSON object — nothing else.",
    instructions: [
      "Output must be a single valid FormSemanticPlan JSON object, no markdown or prose.",
      "Required root keys: semanticPlanVersion (\"1.0\"), formId, title, components.",
      "Do not emit a DefinitionJSON shape — coordinates, pages[], or style blocks will be rejected.",
      "Prioritise schema validity and component-type validity over everything else.",
    ],
  },
];

export interface BuiltSectionedPrompt {
  sections: PromptSection[];
  addendum: string;
}

export function buildSectionedSystemAddendum(): BuiltSectionedPrompt {
  const lines: string[] = [];
  lines.push("Sectioned Prompt Architecture v1 (apply all sections):");
  lines.push("");
  SECTION_DEFINITIONS.forEach((section, index) => {
    lines.push(`${index + 1}. [${section.id}] ${section.title}`);
    lines.push(`Objective: ${section.objective}`);
    section.instructions.forEach((instruction) => {
      lines.push(`- ${instruction}`);
    });
    lines.push("");
  });
  return {
    sections: SECTION_DEFINITIONS,
    addendum: lines.join("\n").trim(),
  };
}

