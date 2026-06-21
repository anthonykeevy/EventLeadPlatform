# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root — the project's ubiquitous language (glossary). Created lazily by `/grill-with-docs` and `/domain-modeling`; does not exist yet.
- **`docs/architecture/decisions/`** — BMAD Architecture Decision Records (ADR-001 through ADR-004 and successors). Read ADRs that touch the area you're about to work in.
- **`docs/architecture/`** — supplementary architecture docs (handoffs, capsule inventory, story-specific decisions). Check here when an ADR doesn't cover the topic.

If `CONTEXT.md` doesn't exist, **proceed silently**. Don't flag its absence; don't suggest creating it upfront. The `/domain-modeling` skill (reached via `/grill-with-docs` and `/improve-codebase-architecture`) creates it lazily when terms actually get resolved.

## File structure

Single-context repo with BMAD architecture layout:

```
/
├── CONTEXT.md                         ← domain glossary (to be created)
├── docs/
│   ├── architecture/
│   │   ├── decisions/
│   │   │   ├── ADR-001-database-schema-organization.md
│   │   │   ├── ADR-002-backend-abstraction-layer.md
│   │   │   ├── ADR-003-naming-convention-strategy.md
│   │   │   └── ADR-004-database-normalization-for-enum-like-fields.md
│   │   └── …                          ← handoffs, capsule inventory, story decisions
│   └── agents/                        ← Matt Pocock skills configuration (this folder)
├── frontend/src/features/
└── backend/modules/
```

New ADRs from Matt Pocock skills (`/domain-modeling`, `/grill-with-docs`) should be added to `docs/architecture/decisions/` following the existing `ADR-NNN-*.md` naming convention.

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal — either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/domain-modeling`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-002 (backend abstraction layer) — but worth reopening because…_
