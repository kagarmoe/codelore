---
title: Data Systems Review — Current Architecture, Database Inside-Out Correction
date: 2026-07-04
reviewer-lens: Data Systems Reviewer — log as system of record, materialized views, workload fit, replay, and operational reality
artifact: docs/architecture/
status: findings delivered
tags: [codelore, review, data-systems, database-inside-out]
supersedes:
  - docs/reviews/2026-07-04-data-systems-review-current-architecture.md
---

# Data Systems Review — Current Architecture, Database Inside-Out Correction

## Top Findings

### 1. The architecture should distinguish the system of record from the canonical product artifact.

The current architecture says the evidence pack is the source of truth. That is
useful shorthand for product behavior: Neo4j, DuckDB, RDF, dossiers, and
summaries must not invent facts outside the pack.

But the deeper data-systems model should be Kleppmann's database-inside-out
shape:

```text
durable append-only log -> materialized evidence pack -> derived query/export views
```

The durable log is the system of record. The evidence pack is a validated,
materialized product view over that log. Neo4j, DuckDB, RDF, dossiers, and
summaries are further views.

This matters because CodeLore is a historical reconstruction system. It should
preserve not only the final validated records, but also the durable event stream
from which those records can be replayed, reprojected, audited, and migrated.

Recommendation:

- Amend the architecture to say the log is the reconstruction source of truth.
- Keep the evidence pack canonical for product consumption and validation.
- Reserve "source of truth" for the durable log when discussing replay,
  migration, and recovery.
- Use "canonical product artifact" for the pack when discussing queries,
  evidence citation, and derived views.

### 2. Pack migrations should be mostly projection work, not primary data rewrites.

If the log is durable and sufficiently semantic, pack migration becomes easier:
replay old events through a new assembler or projector and produce a new pack
schema version.

That is the main advantage of the database-inside-out model. It reduces the
pressure to mutate old pack files in place.

The hard part moves to the log contract. If log events are merely incidental
debug traces, replay will not work. If they are durable domain events with
stable semantics, migration is straightforward.

Recommendation:

- Treat the pack as a materialized view whose schema can change.
- Treat log event semantics as the compatibility boundary.
- Version event schemas separately from pack schemas.
- Test migration by replaying an older fixture log into the current pack shape.

### 3. The architecture currently has stage accountability, but not yet a durable event model.

The architecture already says candidates must be admitted, rejected, or marked
out of scope. That is good. It is close to the right event model.

What is missing is the explicit durable log shape:

- acquisition events
- stage-started and stage-completed events
- candidate-created events
- admission-decision events
- validation-decision events
- rejection events
- pack-record-emitted events
- projection-built events

Without that model, "stage accountability" remains a validation rule over
outputs rather than a replayable history of how outputs came to exist.

Recommendation:

- Define a `log_events.jsonl` contract or equivalent event stream.
- Give every event a stable `event_id`, `event_type`, `event_schema_version`,
  `run_id`, timestamp, causal predecessor references, payload, and checksum
  policy.
- Ensure pack records can cite the event IDs that produced them.
- Preserve rejected candidates in the log even when they do not appear in the
  product pack.

### 4. The evidence pack should remain canonical for users, agents, and derived views.

The correction does not demote the evidence pack into a cache.

The pack should still be the canonical product artifact: the thing users query,
agents cite, validators inspect, and derived views project. If Neo4j or RDF
conflicts with the pack, the pack wins.

The distinction is layered:

```text
log = system of record for reconstruction
pack = canonical validated product state
views = disposable query/export surfaces
```

That gives CodeLore two forms of authority:

- operational authority: replay the log
- product authority: cite the pack

Recommendation:

- State both authorities explicitly.
- Avoid saying only "the pack is the source of truth" without qualification.
- Avoid saying only "the log is the source of truth" in user-facing evidence
  contexts, because users should not have to query event logs to inspect
  CodeLore's claims.

### 5. Query workload gates still matter, but they should be evaluated against materialized views.

The graph-value question does not disappear under the log model. It becomes
cleaner.

Neo4j, DuckDB, SQLite, RDF, dossiers, and rendered pages are all projections.
They should earn their place by answering concrete workloads better than
simpler projections.

Recommendation:

- Define canonical product queries over the evidence pack.
- Benchmark pack-direct, SQL, and graph projections against the same workload.
- Treat Neo4j as a derived traversal view, not as the place where graph facts
  originate.
- Make projection manifests record source log position, source pack ID, pack
  schema version, projection version, and validation result.

### 6. The main risk is now event-semantic drift, not pack-schema drift.

The first review overstated pack migration risk. If logs are durable,
pack-schema migration is manageable.

The real risk is that old log events stop meaning what the new code thinks they
mean. Event names, payload fields, admission decisions, rejection reasons, and
causal links must remain interpretable.

Recommendation:

- Design event schemas conservatively.
- Never change event meaning in place.
- Add new event types or schema versions instead of redefining old ones.
- Keep migration tests around old fixture logs.
- Document the minimum backward-compatibility promise.

## What Is Strong

The architecture is already close to this model in spirit. It emphasizes:

- replayability
- explicit provenance
- stage accountability
- immutable packs
- derived graph and RDF views
- no in-graph authority
- deterministic Phase 2 construction

Those choices align well with database-inside-out thinking. The architecture
does not need a new infrastructure stack. It needs clearer layering language
and a durable event contract.

## What Is Weak Or Risky

The phrase "evidence pack is the source of truth" is doing too much work.

It is correct when comparing the pack to derived views. It is misleading when
discussing replay, migration, recovery, or audit. In those contexts, the log
must be deeper than the pack.

The architecture also does not yet define:

- event schema versions
- event identity
- event ordering and causal references
- replay checkpoints
- log compaction policy, if any
- retention policy for raw snapshots and generator outputs
- how pack records cite generating events
- how projections record their source log offsets or pack IDs

Those omissions are manageable now and expensive later.

## Concrete Recommendations

1. Add a short "System Of Record" section to the architecture overview.

   Suggested language:

   ```text
   The durable append-only log is the system of record for reconstruction.
   The evidence pack is the canonical validated product artifact materialized
   from that log. Derived views are query and export projections from the pack
   or from pack-compatible materializations.
   ```

2. Add a log/event contract before expanding beyond Phase 2.

   Minimum event fields:

   - `event_id`
   - `event_type`
   - `event_schema_version`
   - `run_id`
   - `occurred_at`
   - `producer`
   - `predecessor_event_ids`
   - `payload`
   - `payload_checksum`

3. Split schema versions.

   Track at least:

   - `log_schema_version`
   - `pack_schema_version`
   - `projection_schema_version`
   - `generator_version`
   - `validation_profile`

4. Make pack assembly a projection from the log.

   The assembler should consume a bounded log segment and emit a validated pack.
   That turns pack creation into a reproducible materialization step.

5. Add replay tests.

   Keep at least one old fixture log and prove it can be replayed into the
   current pack shape or into a documented compatibility shape.

6. Keep Phase 2 narrow.

   Do not add Neo4j, RDF, generator extraction, or broad claims until the
   log-to-pack materialization path is stable.

## Open Questions

- What is the first durable log artifact: a single JSONL event stream, staged
  JSONL files, or a manifest plus stage-local event files?
- Are raw git snapshots part of the log payload, content-addressed blobs
  referenced by events, or both?
- What is the retention policy for generator outputs that influence admitted
  records?
- Does the pack cite generating event IDs directly, or only cite source
  artifacts and run IDs?
- What backward-compatibility promise does CodeLore make for old logs?
- Are packs immutable materializations, or can a pack ID be superseded by a new
  pack generated from the same log segment?

## Bottom Line

The corrected data-systems model is:

```text
durable log -> materialized evidence pack -> derived views
```

That is stronger than "evidence pack as source of truth" and more precise than
"everything is rebuildable from packs."

The evidence pack should remain canonical for product use. The log should be
authoritative for reconstruction, replay, audit, and migration. If CodeLore
gets that layering right now, migrations should be easy and infrastructure
choices can stay workload-driven.
