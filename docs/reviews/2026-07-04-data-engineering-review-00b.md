---
title: Data Engineering Review — CodeLore Development Plan 00b
date: 2026-07-04
reviewer-lens: data systems (graph databases, relational, event streaming)
artifact: docs/plans/00b-development-plan-evidence-first.md
status: amendments applied
tags:
  - codelore
  - review
  - data-engineering
  - graph
  - plan
---

# Data Engineering Review — `docs/plans/00b-development-plan-evidence-first.md`

Lens: graph databases / relational systems / event streaming. Findings, not roleplay. O = observation, I = interpretation, R = recommendation, U = uncertainty.

## Top findings (by severity)

### 1. The pack has no relationship record type — this breaks both the Neo4j write path and the RDF export

**O:** `06-schema-draft.md` §3–4 defines ~70 edge types and mandates edge properties (`link_method`, `confidence`, `membership_type`, `time_relation`) as semantic carriers ("graph meaning should live in edges"). `src/codelore/models.py` contains no link/edge/relation model at all. `Claim` carries `subject_refs` + `evidence_ids`, but an `artifact_link` claim ("PR #12 IMPLEMENTED_BY commit abc") has nowhere to store a typed subject–predicate–object triple with its own properties. The plan's "Graph semantics versus graph infrastructure" section promises "typed relationships mappable to predicates" and IRIs for stable identifiers — but relationships without IDs cannot have IRIs.
**I:** Phase 6 would have to parse relations out of claim statements or invent them at load time; the Phase 8 RDF export would have nothing addressable to reify. Property graphs carry edge properties natively; RDF does not — you need RDF-star, standard reification, or named graphs, and all three require the edge to be an identifiable statement. This is the single most consequential modeling gap in the plan.
**R:** Add a `LinkRecord` (or `RelationRecord`) to `models.py` **before Phase 3a** builds `artifact_link` claims: `link_id` (stable, IRI-usable), `source_id`, `relation_type` (enum from the schema draft), `target_id`, `link_method`, `confidence`, `created_by`, `created_at`, `window_id`. `artifact_link` claims then cite link records as evidence subjects. Phase 6 becomes a mechanical `UNWIND` over link records; Phase 8 maps each record to an RDF-star annotation or reified statement, and window scoping maps to one named graph per `ChangeWindow`. State that mapping in the plan's formal-representations bullet now.

### 2. Referential-integrity and bidirectionality hazards in `models.py`

**O:** `Warrant.claim_id` back-references the claim while `Claim.warrant_ids` forward-references warrants — two copies of one fact. `EvidencePack` performs no cross-reference validation: a claim citing a nonexistent `evidence_id` validates cleanly. `ArtifactRecord.window_ids` embeds a many-to-many; the schema draft's membership rule explicitly says membership must be relational (`NATIVE_TO_WINDOW` vs `LINKED_TO_WINDOW` with `membership_type`), which a bare ID tuple cannot express.
**I:** Frozen models make the bidirectional pair circular at construction time and guarantee eventual drift. The pack is "source of truth," so dangling IDs poison every derived view. The native/linked distinction the schema draft treats as primary semantics is currently unrepresentable in the pack.
**R:** Keep one direction only (drop `Warrant.claim_id`; claims own `warrant_ids`). Add a pack-level model validator that checks every ID reference resolves — this is cheap and belongs in the Phase 3a exit criteria. Represent window membership as link records per finding 1, carrying `membership_type`.

### 3. Name the SQL middle tier before the llama.cpp scale test, not during it

**O:** Phase 4 queries the monolithic JSON pack in memory; Phase 8 promises cross-window lineage and change-over-time views; `05-llama-cpp-validation-plan.md` anticipates monthly windows with thousands of commits. Rough envelope: gastown (358 commits, ~44 PRs) yields perhaps 2–5k artifact records, 5–15k evidence spans, a 5–20 MB pack — every paradigm is instant. A llama.cpp monthly window plausibly yields 50–100k artifacts and 100–500k evidence records: a several-hundred-MB single JSON document that pydantic must fully parse (frozen, `extra=forbid`) to answer any question. (U: counts are estimates; the corpus audit pattern should be repeated for llama.cpp.)
**I:** The architecture is sound ELT/event-sourcing: snapshots as immutable log, pack as materialized view, graph as derived view. What breaks first is not the design but the *file shape* — no partial reads, no indexes, N-pack in-memory joins for cross-window questions. The fix is not a new source of truth: DuckDB/SQLite reading pack JSON directly is a disposable query tier that changes nothing upstream.
**R:** (a) Shard the pack on disk into per-collection JSONL (`artifacts.jsonl`, `evidence.jsonl`, …) under one manifest — streaming reads, direct DuckDB querying, same logical pack. (b) Add "structured-query tier over packs (DuckDB or SQLite), no schema authority" as a named Phase 6 comparison arm and a Phase 8 prerequisite. (c) Give Phase 8 explicit scale bounds in its exit criteria: max pack build time, max pack size, max query latency at monthly-window scale.

### 4. "Thin backend boundary / replaceable engine" overpromises

**O:** The plan says the engine is "replaceable... without touching the semantics" and Phase 6 puts the write path "behind a thin backend boundary."
**I:** The write path *can* be engine-agnostic (pack → node/edge records → adapter). The query path cannot: Cypher variable-length traversals, SQL recursive CTEs, and SPARQL property paths are structurally different programs. Engine-agnostic query abstraction is a known tar pit; its cost exceeds the cost of rewriting queries.
**R:** Reword to: "The **write path** sits behind a thin backend interface and is engine-agnostic. **Queries are engine-specific and disposable**: because the pack is the source of truth and the graph is fully rebuildable, replacing the engine means rewriting the query layer, not migrating data." That is a promise you can keep.

### 5. Phase 6 write path is underspecified

**O:** Phase 6 deliverables name a write path but not: uniqueness constraints, MERGE vs CREATE, transaction sizing, or graph schema evolution.
**R:** Add to Phase 6: (a) create a uniqueness constraint on every ID property before first load — without the constraint's backing index, `MERGE` degrades to label scans and loads go quadratic; (b) state the load contract explicitly — given full rebuildability, prefer *drop-and-rebuild per window* with `CREATE` into a constrained empty store, or `MERGE` keyed on stable IDs if incremental; (c) batch via `UNWIND` with parameter lists, ~1–10k records per transaction (irrelevant at gastown scale, load-bearing at llama.cpp scale); (d) state **rebuild-not-migrate** as the schema-evolution policy: the graph never migrates, it re-derives from the pack. This is the right strategy — say so in writing so nobody writes a Cypher migration later.
**compose.yaml:** 1G heap is fine for these workloads, but set `NEO4J_server_memory_pagecache_size` explicitly (~512m) rather than inheriting the heuristic. Note that community edition supports uniqueness constraints but not property-existence/node-key constraints — required-property enforcement must stay in the pack validator, which happily matches the plan's stance that validation lives pack-side.

### 6. The Phase 6 comparison could strawman either side

**O:** The gate requires a "comparison memo" and (correctly) a second window if the hypothesis is cross-window. Protocol details are absent.
**I:** Classifying the five acceptance questions: (1) what changed, (3) explicit problems, (4) explicit decisions, (5) unresolved — all single-collection filters; (2) which artifacts support — a two-hop join. None rewards traversal; dict joins or SQL win at any scale. Graph value appears only at variable-length lineage (`DERIVES_FROM*`, `POSSIBLY_SAME_AS` chains) — the plan already says this, and the gate itself is well designed. The risks: unindexed JSON scans as the "files" arm (strawman vs. files), single-window latency microbenchmarks (strawman vs. graph — everything is sub-ms at gastown scale), cold JVM vs warm Python.
**R:** Fix the query set in writing before implementing either arm; permit indexes/preprocessing on all arms (dicts/SQLite for the pack, constraints for Neo4j); report warm and cold separately; record developer-time-to-correct-query and query line count alongside latency; include the SQL tier as a third arm.

### 7. Event streaming: correctly absent — add three cheap forward provisions

**O/I:** No Kafka case exists now: single writer, batch pipeline, bounded corpora, no independent consumers; snapshots already provide replay. A broker adds operational weight with zero retrieval or throughput benefit. The snapshot/manifest design is already log-shaped, which is why later continuous ingestion is survivable.
**R:** Make three rules explicit so webhooks/multi-repo later need no rewrite: (a) run manifests are append-only — a rebuild is a new run record, never a mutation; (b) packs are immutable and versioned — rebuilds produce a new pack version addressed by run ID or content hash; (c) manifest entries are ordered, timestamped, typed records (event-shaped), and acquisition records carry a resumable cursor/watermark per forge resource. `(project_id, window_id)` is already the natural partition key — good.

## What is strong

- The gated, evidence-first sequencing is genuinely good data engineering: proving claim quality before paying for graph infrastructure honors the acceptance criteria's own failure condition (`04-gastown-slice-acceptance.md` failure 4).
- Pack-as-source-of-truth with a fully rebuildable derived graph is the correct dependency direction, and stable replay-identical IDs are exactly what both MERGE idempotency and IRI minting need.
- Immutable checksummed snapshots + per-run manifests + per-stage drop counts is a disciplined provenance design many production pipelines lack.
- The Phase 6 requirement that a cross-window hypothesis needs a second built window preempts the most common self-deception in graph adoption.

## What is weak or risky

- Findings 1–3 concentrated: the pack schema is currently node-rich and edge-free while the entire architecture document argues edges carry the meaning.
- "Rendered relationship views... per-claim evidence neighborhoods" (Phase 4) will not survive 100k-claim windows as pre-rendered output; plan for on-demand rendering.
- Phase 8's four deliverables (window generality, lineage views, RDF/OWL/SKOS exports, hostile validation) are a phase-and-a-half; the RDF export in particular inherits finding 1's debt.

## Open questions

1. Is the pack one JSON document forever, or is per-collection JSONL acceptable as the canonical on-disk form? (Determines whether finding 3a is a change or a clarification.)
2. When a window is rebuilt after code changes, do old pack versions remain addressable (full event-sourcing) or is latest-wins acceptable?
3. For RDF: RDF-star or standard reification? Named graphs per window seem settled by the model; per-edge metadata does not.
4. What are the actual llama.cpp monthly counts? Run the corpus-audit pattern there before Phase 8 commits exit criteria.