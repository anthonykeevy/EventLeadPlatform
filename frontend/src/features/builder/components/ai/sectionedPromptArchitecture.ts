export const SECTIONED_PROMPT_PROFILE_VERSION = "v1.0.1";

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
    objective: "Place components on canvas with no overlap and no boundary violations.",
    instructions: [
      "Use runtimeContext.componentFootprints as authoritative geometry when provided.",
      "Treat dropdown/select as closed controls for placement geometry.",
      "Keep all components within canvasSettings width and height bounds.",
      "Use deterministic vertical rhythm and spacing with readable row flow.",
    ],
  },
  {
    id: "data_collection",
    title: "Data Collection",
    objective: "Capture requested fields and options with stable structure.",
    instructions: [
      "Include all requested inputs with deterministic ids and labels.",
      "Set required flags, placeholders, and option lists where relevant.",
      "Assign tabOrder in visual reading order.",
      "Use component types that best match user intent.",
    ],
  },
  {
    id: "validation_rules",
    title: "Validation Rules",
    objective: "Apply clear validation contract per input type.",
    instructions: [
      "Use validation keys compatible with Story 6.2 schema.",
      "Apply required, email, phone, url, and length constraints where implied.",
      "Keep validation messages concise and user-friendly.",
      "Never emit unsupported keys.",
    ],
  },
  {
    id: "appearance",
    title: "Appearance Typography Colors",
    objective: "Preserve readability while respecting locked globals and framework defaults.",
    instructions: [
      "Respect runtimeContext.lockedGlobals for theme/globalStyles/canvasSettings.",
      "Prefer framework-consistent default dimensions over inflated widths.",
      "Keep styles editable in builder after generation.",
      "Maintain toolbox/canvas/runtime parity assumptions.",
    ],
  },
  {
    id: "logic",
    title: "Logic Rules",
    objective: "Add only necessary logic with valid references.",
    instructions: [
      "Add logic only when user asks or behavior clearly requires it.",
      "Ensure sourceComponentId and targetComponentId exist and are different.",
      "Use valid operator/action pairs.",
      "Keep rule set minimal and deterministic.",
    ],
  },
  {
    id: "delivery_summary",
    title: "Delivery Summary",
    objective: "Guarantee parseable deterministic JSON output.",
    instructions: [
      "Return a single DefinitionJSON object only.",
      "Place tabOrder only inside component.props.tabOrder, never as component.tabOrder.",
      "Do not include markdown, prose, or code fences.",
      "Prioritize schema validity first, then layout quality.",
    ],
  },
];

export interface BuiltSectionedPrompt {
  version: string;
  sections: PromptSection[];
  addendum: string;
}

export function buildSectionedSystemAddendum(): BuiltSectionedPrompt {
  const lines: string[] = [];
  lines.push(
    `Sectioned Prompt Architecture ${SECTIONED_PROMPT_PROFILE_VERSION} (apply all sections):`
  );
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
    version: SECTIONED_PROMPT_PROFILE_VERSION,
    sections: SECTION_DEFINITIONS,
    addendum: lines.join("\n").trim(),
  };
}

