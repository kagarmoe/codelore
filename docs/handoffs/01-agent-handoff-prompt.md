# Agent Handoff Prompt

Use this prompt when handing CodeLore to a new agent.

```text
You are taking over work in `/home/kimberly/repos/codelore`.

Your job is to continue turning CodeLore into a standalone product and implementation, using the current founding docs and setup runbooks as the source of truth.

Before doing any implementation work, orient yourself carefully and do not assume the repo is further along than it is.

## Product frame

CodeLore is a system for constructing, preserving, and querying how a software project evolved over time.

Core distinction:
`gt-wiki` turns releases into wiki pages.
`CodeLore` turns releases into evidence-backed project memory.

This is not a wiki generator. Do not let wiki-shaped assumptions become CodeLore’s core architecture.

The canonical historical unit is `ChangeWindow`, not `Release`, though release windows are the first implementation slice.

## Repo state

This repo lives at:

`/home/kimberly/repos/codelore`

It currently contains founding docs, local agent skills, repo-level coordination
files, a setup runbook, and an initial Phase 1 Python scaffold.

Current top-level files of interest:

- `README.md`
- `CLAUDE.md`
- `AGENTS.md`

Current docs structure:

- `docs/product/00-product-definition.md`
- `docs/extraction/01-extraction-memo.md`
- `docs/evidence/02-evidence-policy.md`
- `docs/evidence/03-claim-taxonomy.md`
- `docs/validation/04-gastown-slice-acceptance.md`
- `docs/validation/05-llama-cpp-validation-plan.md`
- `docs/architecture/06-schema-draft.md`
- `docs/architecture/07-canonicalization-policy.md`
- `docs/plans/00-development-plan.md`
- `docs/handoffs/01-agent-handoff-prompt.md`
- `docs/runbooks/00-setup-runbook.md`

Current scaffold files of interest:

- `pyproject.toml`
- `.python-version`
- `.env.example`
- `compose.yaml`
- `src/codelore/__init__.py`
- `src/codelore/cli.py`
- `src/codelore/models.py`
- `tests/test_cli.py`
- `tests/test_models.py`

Current local skills:

- `.claude/skills/review-personas/`
- `.claude/skills/compact-recovery/`
- `.claude/skills/closing-sessions/`

There is a `.codex/` directory, but it is currently empty.

## Important lineage context

CodeLore was extracted from work previously done in:

- `/home/kimberly/repos/gt-wiki`
- with `gastown` as the first favorable corpus
- and `llama.cpp` as a hostile/post-MVP validation corpus

Important source repos:

- `codelore`: `/home/kimberly/repos/codelore`
- `gt-wiki`: `/home/kimberly/repos/gt-wiki`
- `gastown`: `/home/kimberly/repos/gastown`
- `llama.cpp`: `/home/kimberly/repos/llama.cpp`

Do not import `gt-wiki` assumptions blindly. Treat it as prototype lineage and source material, not product architecture.

## Required orientation order

Read these first, in order:

1. `README.md`
2. `docs/plans/00-development-plan.md`
3. `docs/runbooks/00-setup-runbook.md`
4. `docs/product/00-product-definition.md`
5. `docs/evidence/02-evidence-policy.md`
6. `docs/evidence/03-claim-taxonomy.md`
7. `docs/architecture/06-schema-draft.md`
8. `docs/architecture/07-canonicalization-policy.md`
9. `CLAUDE.md`
10. `AGENTS.md`

Also inspect repo state:

- `git status --short`
- `git log --oneline -10`
- `find . -maxdepth 3 -type f | sort`

Do not start coding until you can summarize the current state accurately.

## Current product and modeling commitments

These are the current nontrivial commitments already made in the docs:

### Historical unit
- `ChangeWindow` is the canonical unit
- supported model direction is:
  - `release`
  - later `commit_range`
  - later `date_range`
- first implementation slice should still stay narrow and prove the release-window path first

### Product stance
- CodeLore is for reconstructing and querying project memory over time
- graph construction is a core product capability, not presentation garnish
- historical context must not be flattened into timeless current-state facts

### Evidence stance
- claims must remain tied to evidence and warrants
- abstention is preferred to overclaiming
- unsupported speculation must not be smuggled in as explanation
- the system must preserve provenance and contradiction, not just polished summaries

### Graph / schema stance
- keep identity thin
- keep history window-scoped
- keep reasoning attached to evidence

The model currently distinguishes:
- canonical identities
- window-scoped observations
- artifacts
- reasoning structures

### Canonicalization stance
Canonical nodes are not extracted directly from labels.
They are earned from repeated observations plus evidence of continuity.

Identity continuity must be evidence-backed, not name-based.

### Ontology stance
The docs have already been pressure-tested by multiple review lenses.
Important current discipline:

- not every useful label deserves first-class ontology
- recurring terminology does not by itself imply recurring ontology
- some categories are broader product-language umbrellas, not yet admitted schema entities

## Important ontology review outcomes

Two ontology reviewer lenses were added and used:

### Quine
Primary concern:
- category admission
- entity proliferation
- naming discipline
- whether distinctions are ontologically earned

Quine’s main warnings:
- the docs sometimes defer categories in prose after half-admitting them in lists or schema labels
- `Release` still risks having too much weight relative to `ChangeWindow`
- `Problem`, `Decision`, `Concept`, `ProblemClass`, `DecisionTheme`, `Finding`, `Abstention`, `OpenQuestion`, and `Summary` need careful admission-status discipline

### Peirce
Primary concern:
- how categories emerge from artifacts
- sign interpretation
- path from evidence to concept
- whether distinctions improve inquiry

Peirce’s main warnings:
- some parts of the model still move from artifact to concept too quickly
- `ProblemObservation`, `DecisionObservation`, and especially `ConceptObservation` still need stronger formation rules
- the path
  `ArtifactRecord -> Evidence -> Observation -> Canonical commitment`
  should be made more explicit

If you revise docs or scaffold implementation, preserve these review gains.

## Reviewer personas available

A reusable review-personas skill exists in:

- `.claude/skills/review-personas/SKILL.md`
- `.claude/skills/review-personas/references/personas.md`

Current personas include:

- `Evidence Auditor (Popper)`
- `Lineage Reviewer (Hennig)`
- `Paradigm Critic (Kuhn)`
- `Product Critic (Drucker)`
- `Schema Skeptic (Sadalage)`
- `Ontology Reviewer (Quine)`
- `Ontology Reviewer (Peirce)`

Use the functional lens, not the famous name, as the authoritative part.

## Setup and environment facts

The setup runbook is now part of the repo and is mandatory context.

Key environment facts already captured there:

### Host hardware
- Ubuntu 24.04
- AMD Ryzen 7 7700X
- 61 GiB RAM
- ~1.1 TiB free disk
- NVIDIA RTX 3090 with 24 GiB VRAM

### GPU / CUDA
Authoritative host-shell report from Kimberly:
- `nvidia-smi` works normally on the host
- NVIDIA driver version: `580.159.03`
- reported CUDA version from `nvidia-smi`: `13.0`

Agent-observed environment:
- `nvcc` exists
- `nvcc --version` reported CUDA toolkit `12.0`
- sandboxed `nvidia-smi` failed earlier

Interpretation:
- the host GPU is healthy
- sandboxed agent execution is not authoritative for GPU visibility
- GPU-dependent work should be verified from a normal host shell or unsandboxed execution

### Tooling already present
- Python `3.13.13`
- `uv 0.11.26`
- Docker `29.4.1`
- Docker Compose `v5.1.0`
- Git `2.43.0`
- Node `v24.14.1`
- GitHub CLI `2.45.0`
- Graphify `0.9.5`

### Development stance
CodeLore should be developed with a GPU-aware, host-first stance.

That means:
- use the GPU where it materially helps
- do not trust sandbox output for CUDA/device health
- keep ingestion/schema work CPU-safe
- treat GPU acceleration as a first-class path for semantic layers

## Headroom and related repo awareness

The setup runbook requires Headroom to be installed and made aware of:

- `~/repos/codelore`
- `~/repos/gastown`
- `~/repos/gt-wiki`
- `~/repos/llama.cpp`

Intent:
- `codelore`: product repo context
- `gt-wiki`: extraction lineage
- `gastown`: favorable corpus
- `llama.cpp`: hostile validation corpus

If you perform Headroom setup work, verify the current upstream README at install time rather than assuming stale commands.

## Current development plan

The current development plan in `docs/plans/00-development-plan.md` stages work as:

- Phase 0: founding alignment
- Phase 1: repo scaffold
- Phase 2: git-first ingestion
- Phase 3: evidence and claim pipeline
- Phase 4: graph population
- Phase 5: query and export
- Phase 6: evaluation
- Phase 7: post-MVP validation

Immediate next tasks already identified are:

1. Tighten `00-product-definition.md` using the latest Quine and Peirce review points.
2. Tighten `06-schema-draft.md` so the artifact -> evidence -> observation -> canonical commitment path is explicit.
3. Choose the Python project scaffold and local graph database setup.
4. Create the package layout and minimal CLI entrypoint. DONE in initial
   scaffold.
5. Start Phase 2 on the `gastown` release window.

## What not to do

Do not:
- revert to a wiki-first architecture
- assume `Release` is the only real unit
- treat broad product nouns as already-admitted ontology
- overbuild support for `commit_range` or `date_range` before the first release slice works
- turn the graph into one flat timeless structure
- allow evidence-poor “why” explanations to harden into claims
- assume `gt-wiki` skills like entity-page writing belong in CodeLore
- trust sandboxed GPU checks over host-shell verification

## What to do next

Your first task is not to code immediately. Your first task is to orient and
then propose the exact next implementation step from the current plan.

After orientation, produce a concise but concrete status summary covering:

- what CodeLore currently is in this repo
- what is already decided
- what is still unresolved
- what the highest-value next implementation step is
- what files you expect to create first if Phase 1 begins now
- whether any host-level setup is required before coding

Then, unless blocked, continue Phase 1 verification or start Phase 2 git-first
ingestion work in the repo.

## Implementation preference

Current intended implementation direction:

- Python
- database-first storage
- real graph database service from day one
- CLI plus generated evidence-pack / dossier output first
- agent retrieval first, human polish second

## First validation target

Primary first slice:
- `gastown v1.1.0 -> v1.2.0`

Post-MVP hostile validation:
- `llama.cpp`

## Final rule

Optimize for historical truth over graph neatness.
If a cleaner model would erase uncertainty, branching, weak support, or temporal context, do not simplify it that way.
```
