---
title: Data Engineering And Infrastructure Plan
date: 2026-07-04
status: draft
scope: CodeLore evidence-first implementation
depends_on:
  - docs/plans/00b-development-plan-evidence-first.md
  - docs/reviews/2026-07-04-data-engineering-review-00b.md
  - docs/architecture/06-schema-draft.md
  - docs/architecture/07-canonicalization-policy.md
---

# CodeLore Data Engineering And Infrastructure Plan

## Purpose

This plan defines the data engineering and infrastructure shape CodeLore should
grow into.

It exists because CodeLore's product idea is easy to overstate and hard to
operate unless the data system is disciplined from the beginning. The central
rule is:

**The evidence pack is the source of truth. Graph infrastructure is a derived
serving view that must earn its keep.**

This document is a companion to
`docs/plans/00b-development-plan-evidence-first.md`, not a replacement.

## Design Goals

CodeLore's infrastructure must support:

- replayable historical reconstruction
- explicit provenance for every durable record
- deterministic structural extraction where possible
- validation at every pipeline boundary
- queryable evidence chains
- rebuildable derived views
- clear separation between product semantics and storage engines
- scale growth from a favorable release window to hostile monthly windows

The system should avoid:

- graph-first modeling without a proven query need
- parsing facts back out of prose claims
- one giant JSON document that cannot be indexed or streamed
- bidirectional reference drift
- silent data loss between pipeline stages
- hidden external API or model-call dependencies during replay
- in-place graph migrations

## Core Architecture

CodeLore is an evidence-first ELT pipeline:

1. **Acquire** raw inputs.
2. **Window** them into a `ChangeWindow`.
3. **Normalize** source objects into records.
4. **Extract** evidence and relations.
5. **Reason** into claims, warrants, contradictions, abstentions, and open
   questions.
6. **Assemble** an immutable evidence pack.
7. **Present** answers, dossiers, and rendered views from the pack.
8. **Project** optional derived views, including SQL indexes and Neo4j.

Data authority flows one way:

```text
raw snapshots -> normalized records -> evidence pack -> derived query views
```

No derived view is authoritative. If a derived view conflicts with the pack, the
pack wins.

## Storage Layers

### Layer 0. Raw Snapshots

Raw snapshots are immutable captures of external inputs.

Examples:

- git command outputs where useful
- commit metadata
- patch text or diff hunks
- GitHub REST or GraphQL responses
- release notes
- model outputs, when models are used

Rules:

- Store snapshots under a run-specific or content-addressed path.
- Record checksums.
- Never overwrite an existing snapshot.
- If a fresh fetch differs from an earlier snapshot, record a new snapshot and
  surface the divergence as data, not as silent replacement.

### Layer 1. Materialized Stage Outputs

Each pipeline stage writes its output to disk.

Minimum stage outputs:

- `acquire`
- `window`
- `normalize`
- `extract`
- `reason`
- `assemble`
- `present`

Rules:

- Each stage declares its input record types and output record types.
- Each stage validates records at its boundary.
- Each stage records input count, output count, drop count, and drop reasons.
- Every input record is either represented in an output record or named in a
  drop list.

### Layer 2. Evidence Pack

The evidence pack is the canonical product data artifact for one window.

Initial logical collections:

- project
- window
- run manifest reference
- artifact records
- link records
- evidence records
- claims
- warrants
- contradictions
- abstentions
- open questions
- optional rendered summaries

The canonical on-disk form is a manifest plus per-collection JSONL from Phase 2
(decided 2026-07-04). A single-file JSON pack may exist only as an export
convenience, never as the canonical form, so the serialization spec and pack
checksums never change shape:

```text
evidence-pack/
  manifest.json
  project.json
  window.json
  artifacts.jsonl
  links.jsonl
  evidence.jsonl
  claims.jsonl
  warrants.jsonl
  contradictions.jsonl
  abstentions.jsonl
  open_questions.jsonl
```

This keeps the logical pack intact while enabling streaming reads, indexed
query tiers, and large-window processing.

### Layer 3. Structured Query Tier

The structured query tier is a disposable query acceleration layer over packs.

Candidate engines:

- DuckDB for local analytical querying over JSON/JSONL and Parquet
- SQLite for simple indexed local storage

Rules:

- The structured query tier has no schema authority.
- It can be deleted and rebuilt from packs.
- It should be included in graph-comparison benchmarks.
- It is the likely default for single-window filters, two-hop joins, and
  window-level dashboards. The recorded acceptance run itself stays
  pack-direct for determinism; the query tier is optional acceleration, never
  the substrate the acceptance results depend on.

### Layer 4. Graph View

The graph view is a derived traversal engine, currently expected to be Neo4j.

The graph is justified only for product-critical questions that benefit from
relationship traversal, especially cross-window lineage and evidence-chain
walking.

Rules:

- Load graph records mechanically from pack records.
- Rebuild the graph from the pack rather than migrating graph state.
- Keep queries engine-specific and disposable.
- Do not allow graph convenience to create facts not present in the pack.

## Record Model Requirements

### Stable Identifiers

Every durable record needs a stable ID.

The ID scheme must specify, per record type:

- input fields
- canonical encoding
- hash algorithm
- namespace prefix
- collision handling

IDs must be stable across replay. Fresh extraction with new snapshots may
produce new IDs, but replay from the same snapshots must be byte-identical.

### Link Records

CodeLore needs explicit relationship records before it needs Neo4j.

`LinkRecord` is the pack-side carrier of graph semantics.

Required fields:

- `link_id`
- `window_id`
- `source_id`
- `relation_type`
- `target_id`
- `link_method`
- `confidence`
- `created_by`
- `created_at`
- `run_id`
- optional `membership_type`
- optional `time_relation`
- optional `evidence_ids`
- optional `limitations`

Rules:

- Do not represent relationships only as prose claim statements.
- Do not duplicate a relationship in multiple owner fields unless a validator
  proves consistency.
- Window membership is represented as link records, not only as embedded
  `window_ids`.
- Edge semantics must be expressible before any graph database is loaded.

### Reference Integrity

The pack validator must reject dangling references.

Minimum checks:

- every claim `evidence_id` exists
- every claim `warrant_id` exists
- every warrant supporting artifact exists
- every evidence record points to an artifact record
- every link source and target exists
- every record scoped to a window points to the current window or an explicitly
  linked window
- every contradiction references existing evidence or claims
- every abstention references the relevant window and, where available,
  relevant evidence

Prefer single ownership for reference direction. For example, if claims own
`warrant_ids`, do not also make warrants own `claim_id` unless the redundancy is
intentional and validated.

### Provenance Fields

Every generated record should carry enough provenance to answer:

- which run produced it
- which stage produced it
- which input records it used
- which generator or rule produced it
- whether it came from deterministic logic, external API data, or model output
- where the raw source can be inspected

## Run Manifest

Every build produces a run manifest.

Required manifest fields:

- `run_id`
- `project_id`
- `window_id`
- CodeLore git commit
- command invocation
- environment summary
- started and completed timestamps
- input snapshot checksums
- stage list
- per-stage input counts
- per-stage output counts
- per-stage drop records
- model invocations, if any
- validation results
- pack schema version
- output pack location

Drop records must include:

- dropped record ID or source locator
- stage
- reason code
- optional explanation

The manifest is append-only. A rebuild creates a new manifest.

## Pipeline Stages

### Acquire

Acquire captures raw inputs.

Initial sources:

- local git repository
- GitHub PRs, issues, comments, and releases after the git-only path works

Acquisition rules:

- Record exact refs and resolved SHAs.
- Record command versions where practical.
- Snapshot forge responses before normalization.
- Treat missing or deleted remote data as first-class acquisition outcomes.

### Window

Windowing defines the historical boundary.

Initial mode:

- release window from `start_ref..end_ref`

The window stage must record:

- resolved start SHA
- resolved end SHA
- traversal policy
- timestamp policy
- merge style observations
- inclusion and exclusion rules

Release-specific parsing should happen at the CLI edge. The core window model
should operate on resolved refs and window type.

### Normalize

Normalize turns source objects into `ArtifactRecord` and `LinkRecord` objects.

Examples:

- commit artifact
- tag artifact
- diff artifact
- changed file artifact
- doc change artifact
- test change artifact
- window-membership link
- commit-parent link
- commit-touches-file link

Normalization should not produce interpretive claims.

### Extract

Extract creates evidence records from artifacts.

Examples:

- text spans
- diff hunks
- structural relations
- explicit references

Extraction may be deterministic or model-assisted later, but deterministic
extractors should be preferred wherever they are sufficient.

### Reason

Reasoning creates claims and warrants.

Initial claim order:

1. structural `artifact_link`
2. deterministic `change_fact`
3. `explicit_problem`
4. `explicit_decision`
5. narrow inference only after direct evidence is processed

No claim should be created without:

- claim type
- window ID
- subject references
- evidence IDs
- warrant IDs
- confidence
- status

### Assemble

Assemble writes the evidence pack and runs the integrity checker.

Assembly fails if:

- schema validation fails
- referential integrity fails
- accountability invariant fails
- canonical serialization fails

### Present

Presentation includes:

- bounded `ask`
- dossier export
- rendered claim-to-evidence navigation
- glossary and taxonomy output

Presentation outputs are derived from the pack. They are not authoritative.

### Project

Projection creates disposable query views:

- DuckDB/SQLite indexes
- Neo4j graph
- RDF/SKOS/OWL exports later

Projection is allowed to fail without corrupting the pack.

## Canonical Serialization

CodeLore needs a written canonical serialization spec before relying on
deterministic output.

Required rules:

- UTF-8
- normalized newlines
- sorted object keys
- record arrays sorted by stable ID
- stable timestamp format
- no environment-dependent ordering
- no volatile fields inside records that must byte-compare
- explicit placement for volatile run metadata

CI should build a fixture pack twice under different hash seeds and compare
bytes.

## Validation System

Validation is not one check. It has layers.

### Schema Validation

Pydantic validates record shape and enum values.

### Pack Integrity Validation

The pack integrity checker validates cross-record references and stage
accountability.

### V-Rule Validation

V-rules are mechanically decidable evidence-policy checks.

Examples:

- cited span exists
- cited artifact type is allowed for claim type
- warrant exists and has the required type
- distinct artifact type count meets the rule
- claim is scoped to the same window as its evidence

### Audit Validation

Semantic judgments that cannot be fully decided mechanically are sampled and
audited.

Examples:

- a span clearly states a problem
- a decision claim really expresses a decision
- a narrow inference did not overreach

Audit results should be written as data, not only prose.

## Query Strategy

Different question classes deserve different query substrates.

### Pack-Direct Queries

Use pack-direct code for:

- small fixture tests
- deterministic acceptance checks
- simple lookup by ID
- rendering local evidence neighborhoods

### Structured Query Tier

Use DuckDB or SQLite for:

- filtering by claim type/status/confidence
- joining claims to warrants and evidence
- artifact counts
- window-level dashboards
- bounded, shallow exploratory queries (the recorded acceptance run itself is
  pack-direct)

### Graph Queries

Use Neo4j only when traversal is the product requirement.

Candidate graph-worthy questions:

- What evidence chain supports this claim through multiple artifacts?
- Which claims are affected if this artifact is contradicted?
- Did this module/problem/decision recur across windows?
- Is this the same entity, a label reuse, or uncertain continuity?
- Which identity-resolution paths connect these observations?

Non-graph-worthy questions:

- list all claims in a window
- count changed files
- find explicit problems
- show claims for one artifact
- export a dossier

Those are table or pack queries unless a traversal requirement appears.

## Neo4j Load Plan

Neo4j is a derived view.

### Constraints

Before loading, create uniqueness constraints for every stable ID property used
as a node key.

Community edition supports uniqueness constraints, but required-property
enforcement remains pack-side.

### Load Contract

Preferred MVP load contract:

- drop and rebuild the target window graph from the pack
- use `CREATE` or constrained `MERGE` only where idempotency requires it
- batch with `UNWIND`
- use parameterized writes
- target 1k to 10k records per transaction

### Schema Evolution

Graph schema evolution is rebuild-from-pack.

Do not write Cypher migrations for derived graph state unless a future
operational requirement proves that rebuilds are impossible.

### Local Compose

Local Neo4j should set:

- explicit heap size
- explicit page cache size
- deterministic ports
- local persistent volumes

Neo4j does not need to run for Phase 2 through Phase 4 acceptance unless a
specific comparison task requires it.

## RDF, SKOS, And OWL

Formal exports are derived from the pack.

Requirements before RDF export:

- stable IDs mappable to IRIs
- first-class `LinkRecord`
- window named-graph strategy
- decision between RDF-star and standard reification
- clear mapping for link metadata

SKOS should describe taxonomy and glossary outputs.

OWL should describe the ontology schema and be checked with a standard reasoner
for mechanical consistency. The reasoner check validates formal structure, not
historical truth.

## Event Streaming Position

CodeLore does not need Kafka or another broker for MVP.

Current properties:

- single writer
- bounded batch windows
- file-based replay
- no independent consumers
- no low-latency ingestion requirement

Forward-compatible provisions:

- manifests are append-only
- packs are immutable and versioned
- acquisition records carry cursors/watermarks
- `(project_id, window_id)` is the natural partition key
- every stage output is event-shaped enough to replay later

Introduce a broker only when there are independent consumers or continuous
multi-repo ingestion that file manifests can no longer support.

## Infrastructure Environments

### Local Development

Required:

- Python 3.13
- `uv`
- git
- pytest
- ruff

Optional:

- Neo4j via Docker Compose
- DuckDB or SQLite query tier
- GitHub CLI for manual diagnostics
- GPU/model stack for later semantic extraction

Local development should work without GPU and without Neo4j through the
evidence-pack acceptance phase.

### CI

Initial CI should run:

- `uv sync --group dev`
- `uv run ruff check .`
- `uv run pytest`
- deterministic fixture pack build twice and byte-compare, once implemented

CI should not require Neo4j until the graph phase.

When Neo4j is introduced, graph tests should be separated:

- unit tests for pack-to-graph record mapping without Neo4j
- integration tests requiring a service container

### Secrets

Do not commit live tokens.

Use environment variables for:

- GitHub tokens
- model API keys
- Neo4j password overrides

Snapshots may contain public GitHub data, but the policy should still avoid
capturing private tokens, auth headers, or local filesystem secrets.

## Observability And Operations

Minimum operational outputs:

- run manifest
- stage logs
- validation report
- drop report
- pack summary
- audit summary

Metrics to record:

- stage duration
- records read/written
- records dropped by reason
- validation failures by type
- pack size
- query latency for golden questions
- graph load time when graph exists

For model-assisted stages, also record:

- prompt hash
- model name
- input snapshot
- output snapshot
- parse failures
- validation drops

## Scale Plan

### Favorable Corpus Scale

`gastown v1.1.0 -> v1.2.0` is expected to be small enough for direct JSON and
in-memory testing.

Do not infer scalability from this case.

### Hostile Corpus Scale

Before `llama.cpp` monthly-window validation, run a corpus audit estimating:

- commits per window
- changed files per window
- diff hunks per window
- PR/issue/comment volume
- expected artifact records
- expected evidence records
- expected pack size

Phase 8 should define explicit limits:

- maximum pack build time
- maximum pack size
- maximum structured-query latency
- maximum graph load time, if graph is used

## Security And Data Hygiene

CodeLore should assume inputs may contain:

- secrets accidentally committed to repositories
- private issue text in non-public deployments
- author emails
- deleted or edited comments
- misleading or malicious text

Rules:

- preserve provenance, but avoid unnecessary credential retention
- allow redaction policies before export
- keep raw snapshots separate from public dossiers
- label generated summaries as derived
- avoid author-intent claims in MVP

## Development Phasing

### Immediate Data Engineering Tasks

1. Write the ID scheme spec.
2. Write the canonical serialization spec.
3. Add `LinkRecord`.
4. Remove or validate bidirectional claim-warrant references.
5. Add a pack integrity checker.
6. Add run manifest v1.
7. Add fixture repo tests.
8. Add deterministic replay test.

### Before GitHub Enrichment

1. Define snapshot layout.
2. Define forge acquisition cursor/watermark records.
3. Define dedup policy for issues versus PRs.
4. Define edited/deleted content handling.
5. Define auth and redaction policy.

### Before Neo4j

1. Complete Phase 4a acceptance from the pack.
2. Write a retrieval-value hypothesis.
3. Define graph query set in advance.
4. Include pack-direct and SQL-tier baselines.
5. Decide keep/defer after measurement.

### Before RDF/OWL/SKOS

1. Confirm stable IRI mapping.
2. Confirm link reification strategy.
3. Confirm named graph strategy for windows.
4. Export small fixture pack first.
5. Run formal parser/reasoner checks.

## Decision Gates

### Graph Infrastructure Gate

Adopt Neo4j only if it answers important questions better than pack-direct or
SQL-tier querying.

Evidence should include:

- correctness
- query clarity
- query maintainability
- latency
- developer time to write the query
- ability to express variable-length lineage

### Streaming Gate

Adopt event streaming only if file manifests and batch replay no longer support
the workload.

### Model-Assisted Extraction Gate

Adopt model-assisted extraction only after the validator contract the model
must satisfy is defined. Deterministic extractors are preferred where they are
sufficient, but the safety property lives in the validator and the audit, not
in the generator.

### Cross-Window Ontology Gate

Admit canonical identities only when continuity evidence satisfies
`docs/architecture/07-canonicalization-policy.md`.

## Risks

### Risk: Edge Soup

Mitigation:

- relation types enumerated
- link records validated
- graph load mechanical
- ontology admission criteria enforced

### Risk: Pack Becomes Too Large

Mitigation:

- per-collection JSONL
- structured query tier
- streaming validation
- corpus audits before hostile validation

### Risk: Graph Becomes Source Of Truth

Mitigation:

- rebuild-only graph policy
- no graph migrations
- pack wins on conflict
- graph comparison gate

### Risk: Claims Overrun Evidence

Mitigation:

- V-rule validation
- sampled audits
- rich abstentions
- explicit why ladder

### Risk: Rebuilds Are Not Reproducible

Mitigation:

- snapshots
- canonical serialization
- stable IDs
- manifest checksums
- replay mode

## Open Decisions

1. Decided (2026-07-04): per-collection JSONL is the canonical pack
   representation from Phase 2; single-file JSON is an export convenience. The
   byte-identity CI test and pack checksums therefore never change form.
2. Should the structured query tier be DuckDB, SQLite, or both during the graph
   comparison?
3. What exact fields belong in `LinkRecord` v1?
4. Should old pack versions be retained forever, or can local development prune
   them while preserving published/demo packs?
5. Which RDF edge-metadata strategy should be used: RDF-star or standard
   reification?
6. What redaction policy is required before publishing evidence packs derived
   from non-public repositories?

## Summary

The data engineering answer to "why graph?" is:

CodeLore should not begin with a graph database. It should begin with durable,
validated, replayable evidence records and first-class relationship records.
The graph becomes useful only as a derived traversal view over those records.

If the pack and structured query tier can answer the product questions clearly,
Neo4j can wait. If cross-window lineage and evidence-chain traversal become
central, Neo4j has a clean, mechanical load path because the pack already
contains explicit graph semantics.
