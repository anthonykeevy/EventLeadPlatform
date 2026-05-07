# Design Task: 6.5a – Clarification Options Data Model (Form Purpose, Respondent Type, Locale Relationships)

**Owner:** Dimitri (Data Domain Architect)  
**Story:** 6.5a – Clarification Questions  
**Status:** Draft for Review  
**Created:** 2026-05-07

---

## 1. Platform Context & Strategic Intent

EventLeadPlatform is building an **AI-first form builder** focused on high-quality, publish-ready forms for events, lead generation, feedback, waivers, and operational workflows.

The core value proposition is:

- Users describe what they want in natural language.
- The AI produces a complete, locale-appropriate semantic form plan.
- The output requires minimal manual correction before publishing.

A major source of poor AI output historically has been **insufficient situational context** — the model does not know:
- Who the form is for (audience locale, cultural expectations, legal jurisdiction).
- What the form is for (registration, feedback, waiver, lead capture, etc.).
- Who will be filling it out (attendees, members, customers, staff, parents, etc.).

Story 6.5a introduces **situational awareness clarification dropdowns** in the AI Agent panel to close this gap. The selected values must be injected into the LLM prompt and must be stored in a way that supports future expansion (more clarification types, more locales, richer prompt hints).

---

## 2. Problem Statement

We currently have no reference data model for structured clarification options (Form Purpose, Respondent Type, etc.).

We need to decide:

- How these new domains relate to the existing `AudienceLocale` and `Country` concepts.
- Whether we build narrow tables or a generic, extensible pattern.
- How selected values are turned into effective prompt context for the LLM.

A poor model here will create technical debt as we add more clarification questions in future stories (6.5b style, 6.5c PII, industry-specific prompts, etc.).

---

## 3. Research Request (Competitors & Analogous Platforms)

Before proposing a schema, Dimitri is asked to conduct light research into how other platforms solve this class of problem.

### 3.1 Form Builders & AI Form Tools (Primary)

- Typeform, Jotform, Tally, Fillout, Google Forms, Microsoft Forms
- Any newer AI-native form builders (e.g. Relume + Webflow AI flows, Cursor + AI, or dedicated tools)

**Focus areas:**
- Do they offer audience / purpose / respondent type selectors before or during AI generation?
- How do they handle locale / language / regional variation?
- Are options hardcoded, or driven from reference data?
- How do they surface “why this matters” help text to users?

### 3.2 Analogous Platforms (Secondary)

- Notion AI, Linear, Figma AI, Cursor, GitHub Copilot Chat — how they gather context before generation.
- Any platform that combines structured reference data with LLM prompting (e.g. CRM + AI email, survey tools with conditional logic, etc.).

**Key questions to answer:**
- What patterns exist for storing “clarification / context” options?
- How extensible are those patterns when new question types are added?
- How do they balance global vs locale-specific options?

### 3.3 Deliverable from Research

A short section (½–1 page) summarising:
- Relevant patterns observed.
- Pros/cons of the approaches seen.
- Any ideas worth stealing or avoiding.

---

## 4. Key Open Design Questions

1. **Relationship Model**
   - Should `FormPurpose` and `RespondentType` be global concepts with locale-specific display names + prompt hints?
   - Or should they have explicit many-to-many links to `AudienceLocale` / `Country`?
   - How do we handle the non-country `AudienceLocale` values (`INTL_ONLINE`, `APAC`, `EU`, `NEUTRAL`)?

2. **Generic vs Specific Tables**
   - Is a generic `ref.ClarificationOption` table (with `OptionType`, `Code`, `DisplayName`, `PromptHint`, `AudienceLocale`, `CountryID`, `SortOrder`, `IsActive`) the right long-term pattern?
   - Or should we create narrow tables (`ref.FormPurpose`, `ref.RespondentType`) for now?

3. **Prompt Injection Strategy**
   - How should selected clarification values be turned into text the LLM sees?
     - Structured JSON block?
     - Natural language paragraphs?
     - Both?
   - Should this live in the existing locale block mechanism or as a separate “clarification context” block?

4. **Auditability & Traceability**
   - How do we want these values captured in `GenerationRun` / `GenerationTraceMetadata`?
   - Do we need a new column or JSON payload?

5. **Future Extensibility**
   - What other clarification domains are likely in the next 6–12 months (industry, event category, tone preference, data sensitivity, etc.)?
   - Does the model support adding them with minimal schema changes?

---

## 5. Expected Deliverable

A single markdown document:

**Location:** `docs/architecture/decision-6.5a-clarification-options-data-model.md`

**Contents:**
1. Executive summary of recommended model.
2. ERD or table relationship diagram (text or mermaid is fine).
3. Rationale for the chosen approach (including insights from competitor research).
4. Migration / seeding strategy (high-level).
5. Open risks or questions that need Tony’s decision.
6. Any constraints this model places on Story 6.5a implementation.

---

## 6. Next Steps After Approval

1. Tony reviews and approves the decision document.
2. Story 6.5a is updated to reference the approved model.
3. Developer is given a clear starting point with the schema already defined.

---

**Prepared by:** Bob (Scrum Master) on behalf of Tony  
**For:** Dimitri (Data Domain Architect)