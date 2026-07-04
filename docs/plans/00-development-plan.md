# CodeLore Development Plan

## Goal

Build the first standalone version of CodeLore as a Python system for constructing, preserving, and querying evidence-backed project memory over time.

The first implementation slice should prove the model on `gastown v1.1.0 -> v1.2.0` before broadening to other window types or hostile validation corpora.

## Guiding Rules

- Keep `ChangeWindow` as the canonical historical unit.
- Treat `Release` as one window boundary mode, not the entire product model.
- Keep identity thin, keep history window-scoped, keep reasoning attached to evidence.
- Prefer abstention over overclaiming.
- Do not promote categories to first-class ontology until admission criteria are explicit.
- Keep the first implementation narrow enough to evaluate clearly.

## Phase 0: Founding Alignment

Deliverables:

- stabilize the founding docs in `docs/`
- align terminology across product, evidence, and schema documents
- make admission status explicit for core, umbrella, and deferred categories
- lock the first implementation target as `gastown v1.1.0 -> v1.2.0`

Exit criteria:

- `00`, `02`, `03`, `06`, and `07` read coherently together
- evidence policy and schema draft do not contradict each other
- the MVP ontology is visibly narrower than the broader product model

## Phase 1: Repo Scaffold

Deliverables:

- Python project scaffold
- dependency and environment setup
- initial package layout
- local dev instructions
- graph database dev configuration

Recommended package shape:

- `src/codelore/ingest`
- `src/codelore/windows`
- `src/codelore/artifacts`
- `src/codelore/evidence`
- `src/codelore/claims`
- `src/codelore/graph`
- `src/codelore/query`
- `src/codelore/export`

Exit criteria:

- repo installs cleanly
- local graph service can be started deterministically
- basic CLI entrypoint exists

## Phase 2: Git-First Ingestion

Deliverables:

- local git ingestion for tags, commits, diffs, changed files, timestamps
- `ChangeWindow` builder with `release` support first
- normalized `ArtifactRecord` output for the target window

Exit criteria:

- can build a release window from `gastown v1.1.0 -> v1.2.0`
- artifacts are stored with stable provenance and locators
- release-specific logic does not leak into the core window model

## Phase 3: Evidence And Claim Pipeline

Deliverables:

- evidence extraction from artifact records
- MVP claim types from the current evidence policy
- warrant generation with explicit support chains
- abstention and contradiction handling

Exit criteria:

- each generated claim has provenance, warrant, and confidence
- unsupported or weakly supported interpretations are preserved as abstentions or open questions
- the first slice produces a usable evidence pack

## Phase 4: Graph Population

Deliverables:

- graph schema implementation for MVP nodes and edges
- explicit window membership relations
- `IdentityResolution` support for MVP canonicalization scope
- write path from evidence pack into the graph store

Exit criteria:

- graph can represent one `gastown` release window cleanly
- evidence, claims, and observations remain window-scoped
- canonicalization is limited to the MVP-safe subset

## Phase 5: Query And Export

Deliverables:

- CLI commands for building a window, asking questions, and exporting results
- retrieval-oriented dossier or evidence-pack export
- first historical question set for evaluation

Candidate CLI:

- `codelore build-window`
- `codelore ask`
- `codelore export-evidence-pack`

Exit criteria:

- can answer core questions for the first slice with citations
- outputs are useful for agent retrieval first, human reading second

## Phase 6: Evaluation

Deliverables:

- run acceptance criteria from `docs/validation/04-gastown-slice-acceptance.md`
- measure overclaiming, weak warrants, and ontology drift
- identify where the model still jumps too quickly from artifacts to concepts

Exit criteria:

- first slice is credible enough to serve as a portfolio demo
- known ontology and grounding weaknesses are documented explicitly

## Phase 7: Post-MVP Validation

Deliverables:

- extend `ChangeWindow` support to `commit_range`
- then add `date_range`
- validate on `llama.cpp` using the hostile-validation plan

Exit criteria:

- model survives a less release-centered repo
- monthly and arbitrary date windows are supported without flattening history

## Immediate Next Tasks

1. Tighten `00-product-definition.md` using the latest Quine and Peirce review points.
2. Tighten `06-schema-draft.md` to make the artifact -> evidence -> observation -> canonical commitment path explicit.
3. Choose the Python project scaffold and local graph database setup.
4. Create the package layout and minimal CLI entrypoint.
5. Start Phase 2 on the `gastown` release window.
