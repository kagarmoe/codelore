# CodeLore Development Plan (Evidence-First Revision)

## Status

Proposed and adopted 2026-07-04 as a revision of `00-development-plan.md`, following a multi-lens review (Product Critic, Evidence Auditor, Schema Skeptic) of the original plan. The original remains in place as historical record with a supersession note.

The main change is an evidence-first resequencing: query, export, and the acceptance tests run against the JSON evidence pack before any graph infrastructure is built, and graph population is gated on a retrieval-value comparison. This follows the acceptance criteria's own failure condition: the slice fails if the graph/storage model dominates implementation effort before claim quality is proven.

Other changes from the original:

- adds a corpus audit and a golden question set as Phase 2 entry tasks
- splits the claim pipeline into a deterministic sub-phase and a text-derived sub-phase
- places forge (PR/issue) ingestion explicitly, which the original required at acceptance but never scheduled
- adds the why ladder and a gated why-layer phase, so reasoned "why" is scheduled product work rather than indefinitely deferred inference
- structures the build as an explicit staged transformation pipeline with materialized intermediates and per-run manifests, so the process is auditable end to end
- adds cross-cutting policies for verifiability (deterministic validation, flexible generation), reproducibility, and testing
- separates graph semantics (evidence, ontology, and reasoning: explicit, governable, auditable, carried by the pack schema) from graph infrastructure (a replaceable engine), and serves human visibility of the structure from the pack in Phase 4
- adds generated glossary and taxonomy outputs (a system ontology reference derived from the models, and a per-window observed-entity glossary) under an explicit open-world ontology stance
- commits to change-over-time visualization (repo timeline, then module, symbol, and concept lineage) and formal exports (SKOS, OWL, RDF) as scheduled Phase 8 outputs, with the pack schema designed for both from the start
- makes phase exit criteria falsifiable where the original's were not

Amended 2026-07-04 after a four-lens review panel — adversarial (plan structure), mining software repositories (corpus and linkage), automated reasoning (guarantees and invariants), and data engineering (storage and modeling). The reports live in `docs/reviews/`. The amendments tighten thresholds, specifications, and the pack's relation model without changing the phase sequence.

Adopted 2026-07-04: `00-development-plan.md` carries a supersession note and remains in place as historical record; this document is the authoritative phase sequence. The staged plan in section 8 of `docs/product/00-product-definition.md` is historical, and section 3's "required MVP graph capabilities" are read as semantic requirements carried by the evidence pack, with the engine gated per Phase 6.

## Goal

Build the first standalone version of CodeLore as a Python system for constructing, preserving, and querying evidence-backed project memory over time.

The first implementation slice should prove the model on `gastown v1.1.0 -> v1.2.0` before broadening to other window types or hostile validation corpora.

## Guiding Rules

- Keep `ChangeWindow` as the canonical historical unit.
- Treat `Release` as one window boundary mode, not the entire product model.
- Keep identity thin, keep history window-scoped, keep reasoning attached to evidence.
- Prefer abstention over overclaiming. This governs what CodeLore asserts in its outputs, not whether work is attempted: an abstention is completed analysis that names the missing evidence, per the why ladder — never a reason for an agent to skip a task.
- Do not promote categories to first-class ontology until admission criteria are explicit.
- Treat the ontology as open-world: it starts small and incomplete, and absence of evidence within a window means unknown, never false.
- Keep the first implementation narrow enough to evaluate clearly.
- Prove claim quality before paying for graph infrastructure.

## Cross-Cutting Policies

These apply to every phase below.

### Pipeline shape and process auditability

CodeLore is built as an explicit data transformation pipeline, and the process itself must be auditable, not only the data it produces.

- Named stages with materialized outputs: acquire (raw git objects and forge snapshots, immutable and checksummed) -> window (bounded `ChangeWindow` assembly) -> normalize (`ArtifactRecord`) -> extract (`Evidence`) -> reason (claims, warrants, contradictions, abstentions) -> assemble (evidence pack) -> present (human surfaces: ask, dossier, rendered views, glossary and taxonomy outputs) -> project (derived machine views: structured-query indexes, the graph, and formal exports — projection may fail without corrupting the pack).
- Each stage declares its inputs and outputs, validates both against the pydantic models at its boundary, and can be run and tested independently.
- Every `build-window` run emits a run manifest recording: the CodeLore code version, input snapshot checksums, per-stage input, output, and dropped counts, model invocations (model, prompt hash, output snapshot reference), and timestamps.
- Manifests are append-only, ordered, typed records: a rebuild is a new run, never a mutation, and acquisition entries carry a resumable cursor per forge resource. Packs are immutable and versioned by run. These provisions are what later continuous ingestion needs; an event broker is not warranted at MVP scale.
- Nothing is dropped silently, stated as a checkable accountability invariant: every stage-input record is either referenced by at least one output record or enumerated in the manifest's drop list with a reason code (counts alone cannot express fan-out stages). The invariant is asserted at each stage boundary and re-checked end to end by the pack integrity checker. Where meaningful, drops are preserved as abstentions.
- Records carry the run and stage that produced them, through the existing provenance fields plus a run reference, so any claim can be walked back to raw inputs and any run can be reconstructed stage by stage.
- The pipeline stays framework-free in the MVP: stages are modules with file-based intermediates and schema contracts, not an orchestrator dependency. The existing package layout (`ingest`, `windows`, `artifacts`, `evidence`, `claims`, `query`, `export`, `graph`) maps onto the stages; stage boundaries are module boundaries.

### Verifiability and generation

Principle: deterministic validation, flexible generation.

- The structural spine is hard-deterministic: `artifact_link` claims, git-derived `change_fact` claims, window membership, and all identifiers are computed mechanically from the underlying artifacts and never depend on a model.
- Text-derived claim extraction in Phase 3b may use rule-based or model-based generators, chosen per claim type by reliability. Every generator must emit span-cited claims.
- A deterministic validator sits behind every generator. The evidence policy's minimum-support rules split in two: V-rules, mechanically decidable from the pack (span exists and matches, artifact classes and counts, distinct-artifact-type counts, warrant present and typed), and G-rules, semantic judgments such as "clearly states the problem," which are generator obligations checked by the sampled claim audit. The validator is sound and complete with respect to the V-rules only, and "no contradictory evidence" is decided closed over the pack's extracted evidence. Claims that fail validation are dropped or recorded as abstentions, never passed through, and V-rule failures are distinguishable from audit findings in the manifest.
- The generation mechanism is recorded in provenance (`capture_method`, `normalized_by`), so explicit and model-derived content stay distinguishable.
- Phase 4 presentation surfaces (answer phrasing, dossier summaries, and per-window glossary definitions) may use a model; every produced statement must cite claims or evidence from the pack. Presentation-stage model outputs are snapshotted exactly like extraction outputs, and "regenerates deterministically" throughout this plan means deterministic under replay.

### Reproducibility

- The pipeline is replayable rather than everywhere-deterministic: forge (GitHub) API responses and model outputs (extraction and presentation) are snapshotted to disk, and evidence packs must be rebuildable offline from those snapshots.
- The ID scheme and a canonical pack serialization (normalized text, sorted keys, fixed timestamp form, record arrays sorted by ID) are written specifications delivered in Phase 2, not conventions. The canonical on-disk form is a manifest plus per-collection JSONL from the start — a single-file JSON pack is an export convenience, never canonical — so the serialization spec and pack checksums stay stable for the project's life. Determinism is tested in CI: build the fixture window twice under different hash seeds and byte-compare the packs.
- All record identifiers are stable: rebuilding the same window in replay mode produces byte-identical packs. Re-extraction (fresh model calls) is an explicit, logged choice, not a side effect.
- Packs carry a `pack_schema_version`. Schema evolution is rebuild-from-snapshots, never in-place migration — for the pack and for every derived view, including the graph.
- The evidence pack is the source of truth for every derived view (graph, query tiers, exports); the snapshot log is the authority the pack itself is rebuilt from. If a view conflicts with the pack, the pack wins; if a pack must change, it is rebuilt from the log.

### The why ladder

CodeLore's product value includes why things changed, and explicit statements will not always exist. Reasoned interpretation is therefore part of the product, admitted rung by rung and never unlabeled:

1. Explicit why: stated directly in an artifact (`explicit_problem`, `explicit_decision`).
2. Inferred why: constructed under a typed inference rule, requiring at least two converging artifact types and no stronger conflicting direct evidence, per the evidence policy's inferred-problem threshold.
3. Candidate why: suggestive but below-threshold interpretations, preserved and clearly separated from supported claims (the product definition's "possible problems" tier), represented through existing claim status machinery rather than new ontology.
4. Rich abstention: when even candidates are too weak, the abstention records what is missing, which interpretations were considered, and what evidence would settle the question.

Every rung is span-cited and defeasible (open to revision when counterevidence appears), and a claim's rung is visible through its claim type, warrant, and confidence. The MVP implements rungs 1, 2 (one rule), and 4. Rung 3 and additional rung-2 rules are admitted in Phase 5, driven by where Phase 4a's acceptance run actually abstained.

### Graph semantics versus graph infrastructure

CodeLore's graph is two separable things, and the plan treats them differently.

- Graph semantics are product core: the typed vocabulary of evidence, ontology, and reasoning — which entities exist, which relationships are legal, and what each relationship means, per the current architecture set beginning at `docs/architecture/00-overview.md` and the operational schema in `docs/architecture/04-schema.md`. These semantics must be explicit (typed records and ID references in the pack schema, never implicit in code), governable (changes go through the ontology admission criteria), and auditable (visible to the validator, the run manifest, and any reviewer walking the pack). They are storage-neutral and present in every branch of this plan.
- The ontology is deliberately open-world and incomplete: categories start small and grow only through the admission criteria, and no output may treat the absence of a statement as a negative fact. Glossary and taxonomy outputs (Phase 4) make the operational ontology human-readable without freezing it.
- Formal representations are planned, not hypothetical: SKOS for the taxonomy and glossary, OWL for the ontology schema, RDF for pack data (Phase 8). The pack schema is designed now so the mapping stays mechanical: stable identifiers usable as IRIs, and relationships as first-class typed records (`LinkRecord`) with their own stable IDs carrying edge semantics (`link_method`, `confidence`, `membership_type`) — so the property-graph load is a mechanical iteration and the RDF export has identifiable statements to annotate. RDF export uses RDF 1.2 named reifiers (`rdf:reifies` over triple terms) with one named graph per window; classic RDF 1.1 reification is only a compatibility export. CodeLore remains evidence-first rather than ontology-first; the formal exports document the ontology the evidence earned.
- Graph infrastructure is a storage and traversal engine, currently planned as Neo4j. The write path is engine-agnostic: a mechanical translation from pack records behind a thin backend interface. Queries are engine-specific and disposable — replacing the engine means rewriting the query layer, not migrating data, because the pack is the source of truth and every view is rebuildable.
- Human visibility of the structure is a product need served by rendering from the pack (Phase 4), not a reason to adopt an engine.

### Testing

- A small synthetic fixture repository lives in `tests/` (two tags, a handful of commits, docs, and tests) so ingestion and claim generation have deterministic unit tests.
- `gastown` is the integration target, not the unit-test substrate.
- Property-based tests (Hypothesis) cover the assurance kernel: the ID scheme (injectivity, stability, field-order independence), the validator's V-rules, canonical serialization round-trips, and the pack integrity checker.
- The pack's JSON Schema is published so third parties can verify pack integrity independently.
- Quality gates for every phase: `pytest` and `ruff` pass.

## Phase 0: Founding Alignment (complete)

Delivered:

- stabilized founding docs in `docs/`
- aligned terminology across product, evidence, and schema documents
- explicit admission status for core, umbrella, and deferred categories
- first implementation target locked as `gastown v1.1.0 -> v1.2.0`

## Phase 1: Repo Scaffold (complete)

Delivered:

- uv-based Python 3.13 project with `src/codelore` package layout
- pydantic MVP domain models matching the claim taxonomy (`models.py`)
- Typer CLI entrypoint with scaffolded `build-window`, `ask`, and `export-evidence-pack` commands
- Neo4j compose configuration (optional infrastructure; not on the MVP critical path)
- initial tests for models and CLI

## Phase 2: Corpus Audit and Git-First Ingestion

Entry tasks (before extractor code):

1. Corpus audit: repoint the local `gastown` clone to `gastownhall/gastown`, fetch tags, verify the `v1.1.0 -> v1.2.0` boundary exists, and inventory which artifact classes are actually present in the window (commits, PRs, issues, changelog, release notes) with counts. The window's development is expected to have flowed mostly through GitHub PRs and issues; the audit verifies that expectation rather than assuming it. The audit must also define the window-membership policy explicitly — reachability (`end ^start`), traversal mode (all-ancestry, with first-parent annotated per commit), and which timestamp is authoritative (author versus committer, which diverge under rebase) — record the repo's merge style (merge-commit, squash, or mixed), and treat out-of-window author dates as a known artifact class rather than noise. Audit counts must be produced independently of the ingester (for example, the GitHub compare view plus manual tag inspection), so the exit-criterion match is a cross-check, not self-consistency. Record the result as `docs/validation/08-gastown-corpus-audit.md`.
2. Golden question set: write concrete instances of the five acceptance questions for this window, each with hand-verified expected supporting artifacts. Record as `docs/validation/09-golden-question-set.md`. This is the disconfirmation baseline every later phase is checked against.

Deliverables:

- local git ingestion for tags, commits, diffs, changed files, timestamps
- `ChangeWindow` builder with `release` boundary support first; release/tag resolution happens at the CLI edge so the core window model only sees resolved refs
- normalized `ArtifactRecord` output for the target window
- the ID scheme specification: per record type, the exact input fields, canonical encoding, and hash; property-tested
- the canonical pack serialization specification (the determinism spec the CI byte-compare test enforces)
- typed relation records (`LinkRecord`) in the domain models: stable `link_id`, source, relation type from the schema draft, target, `link_method`, `confidence`, and window scope — the pack-side carrier of edge semantics, including native/linked window membership; `Warrant.claim_id` is dropped at the same time so the claim-warrant direction has one owner
- an evaluation of existing mining tooling (PyDriller, Perceval) before custom extractors are written, with any custom choice documented against it
- run manifest v1 covering the acquire, window, and normalize stages, with per-stage counts and checksums
- synthetic fixture repo and deterministic ingestion tests

Exit criteria:

- the corpus audit memo and golden question set exist and are hand-verified
- `codelore build-window` produces a window record for `gastown v1.1.0 -> v1.2.0` whose commit and changed-file counts match the audit
- rebuilding the window twice produces byte-identical packs (subsuming identical IDs) and identical manifest counts and checksums, verified by the CI determinism test
- fixture-repo ingestion tests pass
- release-specific logic exists only at the CLI boundary, verified by the core window builder having no release-typed inputs

## Phase 3: Evidence and Claim Pipeline

Split into two sub-phases so deterministic work is never blocked by extraction-strategy risk.

### Phase 3a: Deterministic evidence and claims

Deliverables:

- evidence extraction from artifact records (spans, structural relations, diff hunks)
- `artifact_link` claims built over relation records, and `change_fact` claims scoped at file/hunk granularity — tangled commits (a substantial fraction of real commits address multiple concerns) make commit-granularity subjects overclaim — with structural warrants
- the V-rule specification: the exhaustive, mechanically decidable validation rules per claim type, extracted from the evidence policy
- the pack integrity checker (`codelore check-pack`): every ID reference resolves, window consistency holds (claims cite only in-window evidence), and the manifest's accountability invariant is satisfied end to end; run at the assemble stage
- a hand-built ground-truth PR-to-commit link set for the window, with link precision and a recall estimate reported against it; commits with no recoverable PR counted as a reportable category
- contradiction and abstention plumbing, exercised in tests
- run manifest extended to the extract and reason stages, counting validation drops per stage

Exit criteria:

- every generated claim has provenance, warrant, confidence, and status
- the 3a pipeline makes zero model calls; running it twice yields identical claim sets
- the pack passes the integrity checker
- link precision and estimated recall are reported against the ground-truth set
- fixture-repo claim tests pass

### Phase 3b: Forge enrichment and explicit claims

Entry decision (written before code): record the generator choice (rule-based or model-based) per claim type, and the validation contract each generator's output must satisfy under the verifiability policy above.

Deliverables:

- PR, issue, and release-note ingestion with on-disk snapshots, handling the forge API's known hazards: the issues endpoint also returns PRs (dedup required), ghost/deleted users, edited or deleted content, and a pinned API version; a re-fetch that diverges from an existing snapshot surfaces as a `Contradiction`, never an overwrite. Author fields are ingested as raw strings; no author-level claims exist in MVP and none may be added without an identity policy
- `explicit_problem` and `explicit_decision` claims traceable to text spans
- at most one `narrow_inference` rule (`behavior_guard_inference`), which must cite the specific hunk-and-test pairs it relies on rather than whole commits, and records tangling as a warrant limitation by rule
- changelog or release-note entries with no traceable supporting artifact recorded as a named contradiction class (the inverse of release notes omitting changes, which the evidence policy already covers)
- rich abstentions and open questions recorded where evidence is weak: each names the candidate interpretations considered and what evidence would settle the question

Exit criteria:

- the evidence pack is replayable offline from snapshots (forge inputs and model outputs)
- every text-derived claim passed span validation; validation failures appear as drops or abstentions, not as claims
- a stratified sampled claim audit (at least 30 claims or all claims if fewer, stratified by claim type) reports an error rate at or below 10% — the threshold is revisable, but only with the justification recorded — and a same-size abstention sample reports the false-abstention rate; single-rater labeling is declared as a limitation wherever the audit is cited
- unsupported or weakly supported interpretations are preserved as abstentions or open questions, not dropped
- sampled abstentions name candidates and missing evidence, not bare insufficient-evidence markers
- if many claims land at `low` confidence, the pipeline abstains more aggressively, per the evidence policy

## Phase 4: Query, Export, and Acceptance

Split into two sub-phases so the acceptance run is not hostage to presentation breadth.

### Phase 4a: Ask, export, and the acceptance run

Deliverables:

- `codelore ask` bounded to the five acceptance-question categories, answered from the JSON evidence pack with citations; not open natural-language question answering
- every answer labels its why-ladder rung (explicit, inferred, candidate, or abstained) and carries the corpus-scope line: answers are complete relative to the ingested corpus recorded in the run manifest and silent about the world beyond it — closed over corpus, open over world
- dossier export where every sentence traces back to claims in the pack
- rendered claim-to-artifact navigation, minimal but sufficient for acceptance Test 2, so a reviewer can walk any claim to its support without a running graph service
- a defined overclaiming metric (definition and sampling procedure), measured during the acceptance run; this is the baseline Phase 5 is judged against
- the Test 4 protocol, fixed before any comparison: golden questions as written, baseline answers produced first from `CHANGELOG.md` and gastown's in-repo curated release-evidence docs, comparison recorded against that baseline
- execution of Tests 1-5 from `docs/validation/04-gastown-slice-acceptance.md`, with results in an acceptance memo reviewed by at least one reader other than the author

Exit criteria:

- the acceptance suite passes; a failed run enters a remediation loop (fix, re-run) rather than exiting by documentation, and if remediation stalls, the recorded decision is no-go and Phases 5 and 6 stay blocked
- a reviewer can navigate from any sampled claim to its supporting artifacts using the rendered navigation alone (acceptance Test 2)
- better-than-changelog utility is demonstrated for at least three golden questions under the fixed Test 4 protocol
- the overclaiming baseline is recorded
- an explicit go/no-go decision on the slice is recorded

### Phase 4b: Presentation surfaces

Deliverables:

- full rendered relationship views: per-claim evidence neighborhoods with navigable walking, rendered on demand from the pack (pre-rendering every neighborhood does not survive large windows)
- a generated ontology reference: human-readable glossary and taxonomy of claim types, warrant types, artifact classes, statuses, and why-ladder rungs, derived from the implemented models so documentation cannot drift from the operational ontology; complements the hand-curated `docs/glossary.md`, which governs the working vocabulary across the doc set's two genres
- a per-window glossary in the dossier: observed entities with span-cited, evidence-backed definitions, plus artifact and claim counts by class, explicitly labeled as partial under the open-world assumption
- a within-window timeline view ordering commits, artifacts, and claims by time, rendered from the pack; the first step toward cross-window change-over-time views in Phase 8

Exit criteria:

- the ontology reference and window glossary regenerate deterministically under replay from the models and the pack, with no hand-maintained copies

## Phase 5: The Why Layer (gated)

Entry gate:

- Phase 4a acceptance run complete, with its abstention pattern recorded: which golden questions ended in abstention or candidate-only answers, and why. A full pass is not required — the why layer is the designed remedy when acceptance falls short on thin "why" coverage — but structural failures (traceability, linkage) must be fixed in Phase 4a's remediation loop, not compensated for here.

Deliverables:

- additional typed inference rules (rung 2), each chosen to address a recorded abstention, with an explicit name, threshold, and counterevidence behavior
- the candidate-why tier (rung 3), with an explicit representation decision recorded at entry: a dedicated status or marker rather than overloading `insufficient`, which also covers degraded claims; preserved in the pack and visibly separated from supported claims, with no new first-class ontology unless the admission criteria in the founding docs are met
- validator and sampled-audit coverage extended to every new rule

Exit criteria:

- golden questions that previously ended in bare abstention now resolve to a supported inferred why, a labeled candidate why, or a rich abstention, measured against the golden set
- sampled inferred-claim precision is recorded, and the overclaiming rate, measured by the Phase 4a metric, does not rise above the recorded baseline
- no unlabeled inference: every inferred or candidate why carries its typed warrant and rung label

## Phase 6: Graph Population (gated)

Entry gate:

- Phase 4a acceptance passed; if Phase 5 has changed the claim set since the last acceptance run, the acceptance suite is re-run before the comparison memo
- a written retrieval-value hypothesis naming the questions graph traversal should answer better than structured filtering over the pack; cross-window lineage and change-over-time questions (Phase 8) are the expected strongest candidates
- a minimal multi-window pack index, if the hypothesis requires cross-window questions — the substrate those questions run against

This gate tests retrieval and query value only. Human visibility of the structure is already served from the pack in Phase 4, and a defer outcome means the engine waits: graph semantics remain in the pack schema, and their governance and auditability are unchanged. If the retrieval-value hypothesis rests on cross-window questions, the comparison must include at least one additional built window; a single-window corpus cannot test them.

Deliverables:

- graph schema implementation for the MVP node and edge subset from `docs/architecture/04-schema.md`
- explicit window-membership edges
- `IdentityResolution` support limited to `Module` canonicalization
- write path from the evidence pack into Neo4j behind the engine-agnostic backend interface, with an explicit load contract: uniqueness constraints on every ID property created before first load, drop-and-rebuild per window (or MERGE keyed on stable IDs if incremental), batched transactions; the graph is fully rebuildable from the pack, and graph schema evolution is rebuild-from-pack, never in-graph migration

Exit criteria:

- the graph represents the `gastown` release window cleanly, with evidence, claims, and observations window-scoped
- canonicalization stays within the MVP-safe subset
- a comparison memo whose protocol is fixed before either arm is implemented: query set written in advance, indexes and preprocessing permitted on every arm, a structured-query tier (DuckDB or SQLite over packs) included as a third arm, warm and cold results reported separately, and developer-time-to-correct-query recorded alongside latency; the memo ends in an explicit keep/defer decision on the graph engine — defer is an abstention on insufficient evidence, not a refutation — and a defer outcome leaves graph semantics in the pack schema unchanged

## Phase 7: Evaluation and Portfolio Packaging

Deliverables:

- measure overclaiming, weak warrants, abstention quality, and ontology drift against the acceptance criteria
- document where the model still jumps too quickly from artifacts to concepts
- package the `gastown` slice as a portfolio case study: what CodeLore preserves that a changelog or wiki misses, plus known limitations stated plainly

Exit criteria:

- the first slice is credible as a demo, with known ontology and grounding weaknesses documented explicitly

## Phase 8: Time, Generality, and Interop (post-MVP)

Deliverables:

- extend `ChangeWindow` support to `commit_range`, then `date_range`
- change-over-time views built on cross-window semantics: a repo-level timeline of windows, and entity lineage views following the canonicalization policy's admission order — module first, then symbol, then concept — with identity decisions (`IdentityResolution`, `POSSIBLY_SAME_AS`, `REUSES_LABEL`) visible in the rendering rather than smoothed away. Symbol lineage is priced as its own research-grade sub-project (AST-diff tooling, language-specific, imperfect), with rename-detection thresholds and tool versions recorded as provenance on lineage decisions; concept lineage proceeds only if the admission criteria are met, since no established tooling exists
- formal ontology and data exports layered on the pack: SKOS for the taxonomy and glossary, OWL for the ontology schema, RDF for pack data; the OWL export is run through a standard reasoner as a mechanical consistency check of the ontology (unsatisfiable classes, domain and range violations), not only as documentation
- a structured-query tier over packs (DuckDB or SQLite) as a prerequisite for monthly-window scale; pack storage is already per-collection JSONL from Phase 2
- validate on `llama.cpp` using `docs/validation/05-llama-cpp-validation-plan.md`, with the corpus-audit pattern repeated on `llama.cpp` before this phase commits its exit criteria

Exit criteria:

- the model survives a less release-centered repo
- monthly and arbitrary date windows are supported without flattening history
- a module's change history renders across at least two real windows, with uncertain continuity shown as uncertain
- formal exports parse and validate in standard RDF/OWL tooling, and the OWL ontology passes a reasoner consistency check
- explicit scale bounds are met and recorded: maximum pack build time, pack size, and query latency at monthly-window scale, with the bounds set from the `llama.cpp` corpus audit

## Immediate Next Tasks

1. Run the Phase 2 corpus audit against `gastownhall/gastown` — including the window-membership policy, merge-style report, and independently produced counts — and write the audit memo.
2. Write the golden question set with hand-verified expected artifacts.
3. Write the ID scheme and canonical pack serialization specifications; add `LinkRecord` to the domain models and drop `Warrant.claim_id`.
4. Implement git ingestion and the window builder, with fixture-repo tests and the CI determinism test.
5. Implement the Phase 3a deterministic pipeline: V-rule specification, integrity checker, relation records, and the ground-truth link measurement.
6. Record the Phase 3b entry decision (generator choice and validation contract per claim type) before starting Phase 3b.
