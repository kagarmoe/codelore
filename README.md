# CodeLore

CodeLore reconstructs, preserves, and queries how a software project evolved over time.

`gt-wiki` turns releases into wiki pages. `CodeLore` turns releases into evidence-backed project memory.

## Current Focus

This repository starts from the product and architecture work extracted from `gt-wiki`, but it is not a wiki generator and should not inherit wiki-shaped assumptions as its core model.

The current foundation is organized around:

- `ChangeWindow` as the primary historical unit
- evidence-backed claims with explicit warrants
- historically scoped observations rather than flattened current-state facts
- graph construction as a core product capability, not a presentation detail

## Docs

- `docs/glossary.md`
- `docs/product/00-product-definition.md`
- `docs/extraction/01-extraction-memo.md`
- `docs/evidence/02-evidence-policy.md`
- `docs/evidence/03-claim-taxonomy.md`
- `docs/validation/04-gastown-slice-acceptance.md`
- `docs/validation/05-llama-cpp-validation-plan.md`
- `docs/architecture/06-schema-draft.md`
- `docs/architecture/07-canonicalization-policy.md`
- `docs/plans/00-development-plan.md`
- `docs/plans/00b-development-plan-evidence-first.md`
- `docs/plans/01-automated-reasoning-plan.md`
- `docs/plans/02-data-engineering-infrastructure-plan.md`
- `docs/handoffs/01-agent-handoff-prompt.md`

## Initial Target

The first implementation target is an end-to-end slice on `gastown v1.1.0 -> v1.2.0` that proves:

- git-first ingestion
- release-window assembly
- evidence extraction
- claim and warrant generation
- graph population
- queryable historical outputs

## Status

This repo is in founding-document and early scaffold stage. The next step is to
turn the Phase 1 scaffold into a working `gastown v1.1.0 -> v1.2.0`
git-first ingestion path.

## License

CodeLore is licensed under the Apache License 2.0. See `LICENSE`.
