# CLAUDE.md — CodeLore Coordination

## What this is

This repository is for CodeLore, a standalone system for constructing,
preserving, and querying evidence-backed project memory over time.

`gt-wiki` turns releases into wiki pages. `CodeLore` turns releases into
evidence-backed project memory.

`AGENTS.md` and `CLAUDE.md` serve the same coordination purpose for different
agent tools. Keep their project stance, orientation docs, and Graphify guidance
in sync when editing either file.

## Non-Interactive Shell Commands

Always use non-interactive flags with file operations to avoid hanging on
confirmation prompts.

Use forms like:

```bash
cp -f source dest
mv -f source dest
rm -f file
rm -rf directory
cp -rf source dest
```

## Current Focus

The repo is currently in founding-document and early-scaffold stage.
The canonical historical unit is `ChangeWindow`, not `Release`, though release
windows are the first implementation slice.

## Core Rules

1. Keep `ChangeWindow` as the primary historical unit.
2. Treat evidence, claims, warrants, and observations as first-class modeling
   concerns.
3. Do not flatten historical context into timeless current-state facts.
4. Do not promote categories to first-class ontology unless admission criteria
   are explicit.
5. Prefer abstention over overclaiming. This rule governs what CodeLore asserts
   in its outputs, not agent effort: an abstention is completed analysis that
   names what is missing. It is never a reason to decline or skip work on the
   system itself.
6. Keep implementation narrower than the full product vision until the first
   slice is proven.

Optimize for:

- evidence-backed historical modeling
- explicit provenance
- careful ontology admission
- graph construction around `ChangeWindow`
- conservative claim discipline

## Primary Docs

Read these first when orienting to the repo:

- `README.md`
- `docs/glossary.md`
- `docs/plans/00b-development-plan-evidence-first.md`
- `docs/plans/01-automated-reasoning-plan.md`
- `docs/plans/02-data-engineering-infrastructure-plan.md`
- `docs/product/00-product-definition.md`
- `docs/evidence/02-evidence-policy.md`
- `docs/evidence/03-claim-taxonomy.md`
- `docs/architecture/06-schema-draft.md`
- `docs/architecture/07-canonicalization-policy.md`

## Local Skills

Project-local skills live in `.claude/skills/`.

Current transferable skills:

- `review-personas`
- `compact-recovery`
- `closing-sessions`

## Graphify

Graphify is optional developer tooling for agent codebase navigation. It is not
part of CodeLore's product architecture, runtime graph, or data model.

Use Graphify only when it is already useful for a codebase-navigation question,
for example when `graphify-out/graph.json` exists and scoped retrieval would be
faster than broad source browsing.

Do not treat `graphify update .` as a required post-edit step. CodeLore's
product graph should be modeled and persisted through the explicit graph
backend, currently planned as Neo4j.

## Working Stance

This repo should be product-shaped, not wiki-shaped. Use `gt-wiki` as source
lineage and reference material, but do not let wiki-generation assumptions
become CodeLore architecture by accident.

Graph construction around `ChangeWindow` means CodeLore's evidence-backed
historical graph, not Graphify's agent-navigation graph.

## Session Discipline

Before ending a work session:

1. verify the working tree with `git status`
2. run relevant checks for the work performed
3. commit if the change is ready to preserve
4. push if a remote is configured and pushing is in scope
5. leave a concise handoff summary

Do not claim work is complete without checking repo state first.
