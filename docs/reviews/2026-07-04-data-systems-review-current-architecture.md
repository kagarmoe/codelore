---
title: Data Systems Review — Current Architecture
date: 2026-07-04
reviewer-lens: Data Systems Reviewer — source of truth, derived views, workload fit, scale, and operational reality
artifact: docs/architecture/
status: superseded
tags: [codelore, review, data-systems]
---

# Data Systems Review — Current Architecture

> Superseded by
> `docs/reviews/2026-07-04-data-systems-review-current-architecture-database-inside-out.md`.
> This first review treated the evidence pack too much like the deepest source
> of truth. The corrected review uses Kleppmann's database-inside-out framing:
> durable log first, materialized evidence pack second, derived query/export
> views after that.

## Top Findings

### 1. The source-of-truth story is directionally right, but the pack evolution story is under-specified.

The architecture correctly says the evidence pack is canonical and that Neo4j,
RDF, DuckDB, dossiers, and summaries are derived views. That is the right
dependency direction.

The missing piece is schema evolution. The current docs define pack collections
and validation expectations, but they do not yet define how pack schemas change
without breaking old packs or readers.

This matters because CodeLore is committing to replayable historical memory. If
pack schema versions, migration policy, compatibility windows, and reader
behavior are not explicit, the pack will become a pile of JSONL files whose
meaning depends on the current code checkout.

Recommendation:

- Add a pack versioning contract to the architecture.
- Put `pack_schema_version`, `generator_version`, and validation profile in
  `manifest.json`.
- Define whether readers must support old packs directly, through migrations,
  or through rebuild-from-source.
- Treat migrations as data transformations with tests, not as incidental code.

### 2. Stage accountability is a strong idea, but it is not yet operational enough to implement.

The architecture says every declared candidate must be admitted, rejected, or
declared out of scope. That is exactly the right rule. It is also where the
implementation will pay most of its data-engineering tax.

The docs do not yet define the concrete accountability tables, manifests, or
join keys needed to audit candidate flow across stages. Counts are explicitly
called insufficient, but the replacement is not yet fully specified.

This is event-sourcing discipline without a concrete event log yet.

Recommendation:

- Define a per-run `stage_runs.jsonl` and `candidate_events.jsonl` or equivalent
  manifest section.
- Require each candidate event to carry `run_id`, `stage`, `candidate_id`,
  `input_ref`, `decision`, `reason_code`, and optional `output_record_ids`.
- Make fan-out and fan-in explicit. A single input may produce many candidates;
  many candidates may support one record.
- Add acceptance tests that intentionally reject candidates and prove the
  accountability trail is queryable.

### 3. Derived views are correctly demoted, but rebuild semantics need sharper contracts.

The architecture repeatedly says derived views are rebuildable from the pack.
That is necessary, but not sufficient.

Rebuildable can mean several different things:

- drop and regenerate the whole view
- incrementally update from pack changes
- rebuild only one window
- rebuild all windows for a project
- reproduce the exact previous view byte-for-byte
- reproduce equivalent query results under a newer projection version

Those are different operational promises.

Recommendation:

- Define projection manifests for each derived view.
- Record source pack IDs, pack schema versions, projection code version,
  projection options, created time, and validation result.
- For MVP, prefer drop-and-rebuild per pack or per project over incremental
  projection.
- Do not promise incremental view maintenance until the workload demands it.

### 4. Query workload categories are useful, but they need executable examples before engine choices are judged.

The Neo4j section does the right thing by separating graph-worthy questions
from table-worthy questions. It resists premature graph infrastructure.

The missing part is a small workload suite. Without representative queries,
Neo4j, DuckDB, SQLite, pack-direct readers, and RDF export cannot be compared
fairly. Engine choice will drift back into taste.

Recommendation:

- Write 10 to 15 canonical product queries before adopting Neo4j as required
  infrastructure.
- Classify each as pack-direct, relational, traversal, or export.
- For each query, state expected input collections, output shape, and maximum
  acceptable ambiguity.
- Use the same query suite as the graph-value gate.

Good first queries:

- show all artifacts native to this window
- show all links for one artifact
- show the evidence chain for one claim
- show all claims affected by a contradicted artifact
- find observations that may refer to the same module across windows
- show unresolved identity decisions for a project
- show all abstentions for one window and their reason codes

### 5. The temporal model is careful, but temporal indexing and clock conflict handling are not designed yet.

The architecture correctly separates author time, committer time, merge time,
release time, evidence time, and snapshot time. It also correctly refuses to
treat named graph membership as temporal semantics.

What is missing is a query and storage design for those clocks. Multiple clocks
will not stay a prose concern. They will need indexes, validation rules, and
conflict handling.

Recommendation:

- Define a normalized timestamp shape with `time_value`, `time_kind`,
  `source_artifact_id`, `source_system`, `precision`, and `timezone_policy`.
- Require every timeline query to name its selected clock.
- Add validation for impossible or suspicious clock relationships without
  rejecting valid history, such as author time after committer time,
  release-note publication after tag time, or snapshot time long after source
  creation.
- Keep temporal claim warrants separate from timestamp storage.

### 6. Stable IDs are named as an invariant, but the ID contract needs to be concrete early.

The architecture depends on stable IDs for records, links, projections, and
rebuilds. The docs say stable inputs and canonical encoding are required, but
they do not yet define the ID namespace rules.

This is a high-leverage omission. If ID rules drift, every downstream view will
inherit churn.

Recommendation:

- Define ID namespaces for `project`, `window`, `artifact`, `link`, `claim`,
  `evidence`, `warrant`, `observation`, and `identity_resolution`.
- Specify which fields participate in each ID and which fields must not.
- Decide whether IDs are human-readable slugs, content hashes, UUID-like
  derived hashes, or a hybrid.
- Add golden tests that prove identical input produces identical IDs across
  runs.

## What Is Strong

The architecture has the right center of gravity: authoritative packs first,
derived views second. It avoids making Neo4j or RDF the source of truth. That
is the most important data-systems decision in the design.

The distinction between `ArtifactRecord`, `LinkRecord`, `Evidence`, `Claim`,
and `Warrant` is also strong. It prevents relationships, source observations,
and reasoning outputs from collapsing into one overloaded graph edge.

The current Phase 2 subset is appropriately conservative. Starting with
deterministic git-derived records and links is better than pretending the full
claim/evidence/warrant system can be built safely in one pass.

The architecture also shows good operational instincts:

- no volatile fields in canonical records
- canonical JSONL ordering
- explicit relation contracts
- rejected-candidate reason codes
- pack validation before canonical writes
- graph projection as rebuild-from-pack

Those are the right bones for a reliable system.

## What Is Weak Or Risky

The architecture is still more explicit about semantics than mechanics. That is
normal at this stage, but the mechanics must arrive before implementation
hardens.

The largest risks are:

- pack versioning is not specified
- run identity and stage execution records are not specified
- candidate accountability lacks concrete event records
- stable ID generation is not yet a written contract
- projection rebuild semantics are too broad
- workload gates are conceptual rather than executable
- timestamp storage and temporal query policy are not yet operational

There is also a subtle source-of-truth risk around generator outputs. The docs
say generator outputs must be snapshotted before parsing or admission. Good.
But the architecture should also say whether those snapshots are part of the
canonical evidence pack, adjacent run artifacts, or external reproducibility
material. If they can affect admitted records, their retention policy matters.

## Concrete Recommendations

1. Add a `manifest.json` contract before adding more record types.

   Minimum fields:

   - `pack_id`
   - `pack_schema_version`
   - `project_id`
   - `window_id`
   - `run_id`
   - `generator_version`
   - `created_at`
   - `source_refs`
   - `validation_profile`
   - `collection_counts`
   - `stage_summaries`

2. Add a run/accountability model.

   The pack is the source of truth for product data, but the run manifest is
   the source of truth for how the pack was produced. Keep those separate but
   linked.

3. Define stable ID rules immediately.

   This should happen before large fixture creation. Otherwise every fixture
   will become unstable when the ID policy changes.

4. Create a small query workload suite.

   Treat it as the graph-value gate. Do not install infrastructure to answer
   queries that can be answered simply by pack-direct or relational reads.

5. Define projection manifests.

   Every Neo4j, DuckDB, SQLite, RDF, or dossier projection should be able to say
   which pack and projection code produced it.

6. Keep Phase 2 narrow.

   Do not add text evidence, claims, warrants, identity resolution, Neo4j, or
   RDF export to the Phase 2 required path until the git-first pack is stable
   and replayable.

7. Add failure fixtures early.

   Include malformed refs, empty ranges, renamed files, merge commits,
   duplicate candidate records, out-of-window author dates, and rejected links.
   The architecture depends on these cases being handled explicitly.

## Open Questions

- Is the evidence pack intended to be immutable once written, or can it be
  rewritten under the same `pack_id`?
- Does `run_id` belong inside every record, only in the manifest, or never in
  canonical records?
- Are rejected candidates product data, reproducibility metadata, or both?
- What is the retention policy for raw snapshots and generator snapshots?
- Will one project have many packs per window over time, or one canonical pack
  per window that is superseded?
- What is the minimum query workload that would justify Neo4j as a required
  local dependency?

## Bottom Line

The architecture is on the right path. It has the correct dependency direction:

```text
raw source material -> admitted records -> evidence pack -> derived views
```

The next data-engineering work should not be ontology expansion or graph
adoption. It should be boring infrastructure:

- manifest contract
- run/accountability records
- stable ID policy
- schema versioning
- projection manifests
- executable query workload gates

That work will decide whether CodeLore becomes a reproducible evidence system
or a collection of semantically thoughtful files that are hard to operate.
