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

const SECTION_DEFINITIONS: PromptSection[] = [
  {
    id: "layout",
    title: "Canvas Layout",
    objective: "Place components cleanly on canvas with no overlap.",
    instructions: [
      "Use runtimeContext.componentFootprints as authoritative closed-control geometry.",
      "Keep all components inside canvasSettings bounds.",
      "Preserve readable vertical rhythm and row alignment.",
      "For dropdown/select, plan for closed control size (not expanded list).",
    ],
  },
  {
    id: "data_collection",
    title: "Data Collection",
    objective: "Capture requested fields/options with stable ids and tab order.",
    instructions: [
      "Include all requested fields exactly once unless prompt asks for duplicates.",
      "Use explicit labels, placeholders, required flags, and options where relevant.",
      "Use deterministic tabOrder in visual reading order.",
      "Keep export-friendly naming and consistent component typing.",
    ],
  },
  {
    id: "validation_rules",
    title: "Validation Rules",
    objective: "Define clear validation behavior for each input.",
    instructions: [
      "Apply required/format constraints per field type (email, phone, required text).",
      "Keep validation messages concise and user-friendly.",
      "Do not add unsupported keys; keep schema-valid structure.",
      "Ensure validation objects align to Story 6.2 schema expectations.",
    ],
  },
  {
    id: "appearance",
    title: "Appearance Typography Colors",
    objective: "Respect locked global style context while keeping readability.",
    instructions: [
      "Preserve runtimeContext.lockedGlobals values; do not mutate locked globals.",
      "Use style props and component dimensions consistent with framework defaults.",
      "Keep visual parity between toolbox/canvas/runtime assumptions.",
      "Avoid excessive width inflation; keep controls near natural content width.",
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
    objective: "Return concise internal summary metadata for logging and evaluation.",
    instructions: [
      "Ensure output remains one valid DefinitionJSON object only.",
      "Prefer deterministic naming and property ordering when possible.",
      "Do not include markdown or prose outside JSON.",
      "Prioritize schema validity first, then layout quality.",
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

