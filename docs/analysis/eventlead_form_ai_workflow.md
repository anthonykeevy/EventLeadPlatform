# EventLead Form AI Workflow

## Overview

This workflow separates the system into two clear responsibilities:

- **Step 1: LLM semantic authoring**
- **Step 2: Deterministic compiler and layout resolution**

This structure lets the LLM focus on form design intent while the compiler handles exact layout, constraints, and final `DefinitionJSON` generation.

This version is deliberately **grid-only**. Non-grid layout modes are removed from semantic and compiler stages.

### Implementation status (Story 6.3.1 hard switch)

- Runtime generation now treats LLM output as semantic intent input (or converts legacy DefinitionJSON into semantic intent), then compiles final layout deterministically in application code.
- Compiler path is enforced as `compilerMode = deterministic-grid` in generation trace metadata.
- Governance versions are used at runtime for compiler decisions via:
  - capability policy JSON
  - width class policy JSON
  - component capability snapshot JSON
  - component validation contracts
- Generation artifacts now persist semantic and compiled attempt payloads for replay/audit.

---

## Critical Review Summary

The proposed architecture is directionally strong, but had four material gaps that must be fixed for predictable delivery:

1. **Prompt governance gap**
   - Prompt text and prompt policy must be rooted in the database with strict versioning, activation windows, and rollback.
   - Runtime prompt assembly must log exact version IDs used per generation request.

2. **Layout model ambiguity**
   - Prior wording mixed grid and non-grid concepts; this creates non-deterministic outcomes and implementation drift.
   - The workflow must be strictly grid-based from semantic hints through physical placement.

3. **Observability and replay gap**
   - Every generation must persist raw semantic plan, compiler decisions, rule applications, and final output so runs are replayable and auditable.

4. **Story boundary blur (6.3.1 vs 6.4)**
   - 6.3.1 should establish deterministic generation and compile pipeline.
   - 6.4 should apply the same pipeline to edit/refinement flows on existing forms, not redesign core compiler behavior.

5. **Capability ingestion gap**
   - Capability and validation metadata cannot be maintained manually in parallel docs forever.
   - The registry needs an auto-ingestion path from component framework metadata so newly added components/features become available without hand-maintained drift.

---

## Workflow Diagram

```mermaid
flowchart TD
    A[Prompt Registry DB<br/>- prompt templates<br/>- template versions<br/>- activation state<br/>- rollback support] --> B[Capability Registry / Policy DB<br/>- component capabilities<br/>- validation capabilities<br/>- step exposure policy]
    Q[Component Metadata Extractor<br/>Build machine-readable capability manifest from framework metadata<br/>and publish versioned snapshot] --> B
    B --> C[Prompt Builder (Runtime)<br/>Build Step 1 prompt from DB versions:<br/>- persona profile<br/>- design priorities<br/>- supported components<br/>- supported validations<br/>- feature exposure policy]

    C --> D[LLM Step 1: Semantic Authoring<br/>Outputs Form Semantic Plan<br/>- component list<br/>- field semantics<br/>- validation intent<br/>- section grouping<br/>- row grouping<br/>- width intent<br/>- action alignment intent<br/>- feature hints]

    D --> E[Semantic Validation Gate<br/>Check:<br/>- supported component types<br/>- allowed feature usage<br/>- required semantic fields<br/>- schema sanity<br/>- unsupported combinations removed]

    E --> F[Compiler Step 2: Capability Resolution<br/>Resolve:<br/>- component support<br/>- surface support<br/>- grid policy compatibility<br/>- current builder constraints]

    F --> G[Compiler Step 2: Validation Normalization<br/>Convert semantic validation intent into final rules<br/>- required<br/>- email / phone / url<br/>- min / max / minLength / maxLength<br/>- messages / priorities]

    G --> H[Compiler Step 2: Width Resolution (Grid)<br/>Compute width targets from:<br/>- width class: compact / half / full<br/>- text length estimator<br/>- maxLength / validation hints<br/>- label/help message width<br/>- component + canvas constraints]

    H --> I[Compiler Step 2: Grid Row/Section Planning<br/>Build deterministic grid structure:<br/>- row partners<br/>- section gaps<br/>- vertical rhythm<br/>- button row policy]

    I --> J[Compiler Step 2: Grid Placement<br/>Calculate:<br/>- x / y from grid cells<br/>- column spans<br/>- horizontal centering policy<br/>- top/bottom margins]

    J --> K[Compiler Step 2: Constraint Pass<br/>Apply:<br/>- collision checks<br/>- canvas boundary rules<br/>- fallback 2-col to 1-col if needed<br/>- canvas height growth if needed<br/>- final grid snapping]

    K --> L[Final Normalization and Trace<br/>- final tab order from geometry<br/>- optional style/props sync<br/>- trace: promptVersion + plan + compile decisions]

    L --> M[DefinitionJSON Output<br/>Executable form definition for canvas / runtime]

    B --> N[New Feature Added]
    N --> O{Expose in Step 1}
    N --> P{Support in Step 2 compiler}
    O -->|Yes| C
    P -->|Yes| F
```

---

## Explanation of Each Step

### 1. Prompt Registry DB (new mandatory control layer)
This is the source of truth for prompt governance. It should define:

- prompt templates
- template versions
- active/inactive states
- effective dates and rollback references
- ownership and change notes

At runtime, every generation request must record which prompt template/version was used.

### 2. Capability Registry / Policy DB
This is the control layer for feature policy. It should define:

- component capabilities
- per-component validation capability map
- surface capabilities
- whether a feature is enabled for Step 1
- whether a feature is enabled for Step 2

Every new feature should be added here first. That allows controlled rollout so a feature can be exposed to the LLM, the compiler, or both.

#### 2.1 Automatic capability ingestion from the Component Framework

Use `docs/COMPONENT-FRAMEWORK-REFERENCE.md` as the architectural contract, but do not parse markdown as runtime source data.

Instead:

1. Build a machine-readable extractor over framework metadata sources (for example registry/capability modules and versioned defaults).
2. Publish a versioned capability snapshot into the DB.
3. Link each generation run to that snapshot version.
4. Regenerate the reference documentation from the same snapshot so docs and runtime stay aligned.

Minimum snapshot content:

- component type + surface support
- supported feature flags per component
- supported validation rules per component (with parameter schema)
- width-class support (`compact`, `half`, `full`) and constraints
- layout constraints required by grid compiler

### 3. Prompt Builder
The prompt builder should construct the Step 1 prompt using only the capabilities and features that are safe for semantic authoring.

It should include:

- persona
- design priorities
- capability boundaries
- supported component catalog
- supported validation rules
- current Step 1 enabled features

It should not rely on the LLM for final layout math.

### 4. LLM Step 1: Semantic Authoring
The LLM should output a **Form Semantic Plan**.

This should include:

- component list
- labels, placeholders, help text, export names
- validation intent
- section grouping
- row grouping
- width intent such as `compact`, `half`, `full`
- button or action alignment intent
- feature hints such as text-length-based sizing intent

The LLM should focus on form structure and design intent, not pixel-perfect placement.

### 5. Semantic Validation Gate
This step validates the semantic plan before compilation.

It should check:

- supported component types
- supported feature usage
- missing required properties
- incompatible combinations
- overall schema sanity

This prevents invalid LLM output from entering the compiler.

### 6. Compiler Step 2: Capability Resolution
This is the first compiler stage.

It resolves:

- whether the selected component supports the requested feature
- whether the current surface supports the requested feature
- whether the requested behavior fits grid layout policy
- whether the requested behavior is safe in the current builder state

This stage makes feature enforcement deterministic.

### 7. Compiler Step 2: Validation Normalization
The LLM decides validation intent. The compiler converts that into the final validation structure.

Examples include:

- `required`
- `email`
- `phone`
- `url`
- `minLength`
- `maxLength`
- `min`
- `max`

The compiler should normalize priorities, messages, and parameter shape.

Validation normalization must be driven by a structured per-component contract, not generic assumptions.

Example contract shape:

- `componentType`
- `allowedRules` (`required`, `email`, `phone`, `url`, `minLength`, `maxLength`, `min`, `max`, etc.)
- `ruleParameterSchema` (types, bounds, required params)
- `ruleCompatibility` (mutual exclusions/dependencies)
- `messagePolicy` (default message keys and override behavior)

### 8. Compiler Step 2: Width Resolution (Grid)
This stage converts semantic width intent into actual sizing decisions.

Inputs to this stage can include:

- width classes such as `compact`, `half`, `full`
- text length estimator
- `maxLength` from validation rules
- label text width
- help and validation message width
- component constraints
- canvas constraints

This is also where the text length indicator can inform Input sizing for supported components.

Width resolution must be canvas-responsive:

- Recompute effective pixel widths when `canvasSettings.width` changes.
- Interpret classes (`compact`, `half`, `full`) as policy intents, then map to concrete spans/px for current canvas width and grid columns.
- Apply per-component min/max bounds after class resolution.
- If class resolution violates constraints, deterministically downgrade (`half` -> `full` on narrow canvases or compact breakpoints) based on policy table.
- Persist resolved width decision in trace so behavior is explainable.

### 9. Compiler Step 2: Grid Row and Section Planning
This stage builds semantic structure into deterministic grid rows and sections.

It should:

- align row partners
- apply row and section spacing
- preserve grouping rhythm
- manage grid gap spacing
- keep layout structure consistent

This is where semantic grouping becomes real layout structure.

### 10. Compiler Step 2: Grid Placement
This stage calculates the actual physical layout.

It should compute:

- actual `x` and `y` from grid cells
- column spans
- row alignment
- overall content block width
- horizontal centering
- top margin
- button placement

This replaces LLM-authored coordinates with deterministic layout math.

### 11. Compiler Step 2: Constraint Pass
After placement is calculated, the compiler should enforce constraints.

This includes:

- collision checks
- canvas boundary rules
- fallback from two-column to one-column when needed
- canvas height growth if the form does not fit
- grid snapping

This ensures the layout is valid and usable.

### 12. Final Normalization and Trace
This stage prepares the final runtime-safe output.

It can include:

- final tab order from actual geometry
- optional style/props syncing if still required by the runtime
- trace payload: semantic plan hash, compile rule version, prompt version IDs
- final cleanup and normalization

This replaces repair-style post-processing with a true compiler finalization step.

### 13. DefinitionJSON Output
This is the final executable output used by the canvas and runtime.

The important change is that `DefinitionJSON` is no longer treated as raw LLM-authored truth. It becomes the compiled result of:

- Step 1 semantic authoring
- Step 2 deterministic resolution

---

## Story Boundary Mapping (6.3.1 vs 6.4)

### Story 6.3.1 (must deliver)

- Prompt Registry DB foundation (template + version + activation + rollback)
- Capability Registry / Policy DB integration into runtime prompt builder
- Step 1 semantic-plan contract (generation mode for new forms)
- Semantic validation gate and deterministic compiler stages
- Grid-only row/section planning and placement
- Constraint pass + final normalization + trace persistence
- Builder apply flow for compiled output
- Benchmarks and first-shot evidence on new-form generation

### Story 6.4 (should deliver)

- Reuse the same Step 1 + Step 2 pipeline for edit/refinement prompts on existing forms
- Diff-aware semantic planning (add/remove/modify fields and sections)
- Deterministic recompile for partial updates with minimal layout disruption
- Edit-session prompt/version tracking and replay traces
- UX loop controls and feedback ergonomics for iterative refinement

### Not in 6.3.1 (explicitly defer)

- Conversational multi-turn optimization UX features beyond baseline controls
- Advanced visual design automation beyond deterministic grid policy
- Any object-layout execution path

---

## Data Model Requirements (Prompt and Version Management)

At minimum, the DB model should support:

- `PromptTemplate` (name, purpose, owner, status)
- `PromptTemplateVersion` (templateId, version, content, changelog, activatedAt, retiredAt)
- `PromptAssemblyProfile` (which template versions compose a runtime prompt)
- `CapabilityPolicyVersion` (feature flags and component-level rules)
- `ComponentCapabilitySnapshot` (versioned extracted manifest from framework metadata)
- `ComponentValidationContract` (per-component rule allowlist + parameter schema + compatibility rules)
- `WidthClassPolicyVersion` (class-to-span/px mapping by canvas breakpoint/grid config)
- `GenerationRun` (request metadata, chosen versions, hashes, outcome)
- `GenerationArtifact` (raw semantic plan, normalized plan, final `DefinitionJSON`, trace blobs)

Critical requirement: one generation run must be replayable offline from stored artifacts and version references.

---

## How New Features Fit Into the Model

When a new form builder feature is added, it should be evaluated independently for:

### Expose in Step 1?
If yes, the prompt builder can teach the LLM about the feature and the LLM can include semantic intent for it.

### Support in Step 2?
If yes, the compiler can resolve that feature into final executable layout and behavior.

This allows flexible rollout:

- Step 1 only
- Step 2 only
- both Step 1 and Step 2

---

## Core Principle

**Step 1 owns intent. Step 2 owns resolution.**

That makes the workflow extensible, easier to maintain, and better aligned with how the Form Builder already separates intent, computed values, rendered values, and normalized canvas layout.
