---
title: Data Systems Review — Temporal Validity Model
date: 2026-07-04
reviewer-lens: data systems, temporal modeling, query workload, and replayability
artifact: docs/architecture/09-temporal-validity.md
status: amendments applied
tags:
  - codelore
  - review
  - data-systems
  - temporal-validity
---

# Data Systems Review — `docs/architecture/09-temporal-validity.md`

Lens: Data Systems Reviewer (Kleppmann), with Repository Miner concerns where
git history semantics matter.

## Top Findings

### 1. The document needs a chosen Phase 2 ordering policy

Observation: The open decisions ask whether commit ordering should be committer
time, author time, or topology-first.

Interpretation: This cannot remain open once ingestion starts. A replayable
pipeline needs one default ordering for deterministic output and a separate set
of timestamp annotations for analysis.

Recommendation: Use topology/ref membership for inclusion, stable deterministic
sort keys for serialization, and record author/committer/merge times as
attributes. Do not use author time for membership. For user-facing timelines,
prefer topology plus selected display timestamp, with the timestamp kind shown.

### 2. `LinkRecord` is carrying several jobs; split required MVP fields from
future fields

Observation: Candidate fields include `membership_type`, `membership_basis`,
`time_relation`, `artifact_time`, `artifact_time_kind`, `evidence_time`, and
`validity_kind`.

Interpretation: This is directionally right, but Phase 2 needs a minimal
contract. Too many optional temporal fields will produce inconsistent records.

Recommendation: For Phase 2, require on membership links:

- `membership_type`
- `membership_basis`
- `source_time`
- `source_time_kind`

Keep `validity_kind` on claims or warrants until relation semantics are clearer.

### 3. Edited forge artifacts need snapshot identity, not just evidence time

Observation: The open questions mention edited comments and updated PR bodies.

Interpretation: A PR body is mutable. `created_at` and `updated_at` are not
enough to reconstruct what text was available at a given earlier time unless
GitHub edit history is captured, which may not be available. The system should
avoid implying historical text availability it cannot prove.

Recommendation: Snapshot time is mandatory provenance. If the textual content
is only known from the snapshot, claims should say "snapshot captured text" and
avoid stronger timing unless the API supplies edit history.

### 4. Named graph warning is correct and operationally useful

Observation: The doc says named graph membership is an export partition, not
temporal validity.

Interpretation: Good. This prevents a common RDF dataset bug where graph name is
silently overloaded as provenance, time, assertion status, and source.

Recommendation: Keep this rule. In exports, make graph name, `cl:observedIn`,
and timestamp properties all present when temporal questions are expected.

## What Is Strong

- Ref-first release window membership is the right data systems choice.
- The distinction between native git membership and linked forge context avoids
  bad joins.
- The document anticipates author-date anomalies and post-hoc release notes.
- It gives queries that will force the model to prove its temporal semantics.

## What Is Weak Or Risky

- The document does not yet define concrete serialization sort keys.
- It does not state whether all timestamps must be normalized to UTC while
  preserving original offset/source text.
- It leaves snapshot time underdeveloped relative to artifact time and evidence
  time.
- It does not yet define how temporal fields appear in the JSONL pack schema.

## Concrete Recommendations

1. Add a Phase 2 default:
   - membership by reachability
   - serialization by stable ID
   - timeline display by explicit selected clock
2. Add `snapshot_time` to the temporal concepts.
3. Require every timestamp field to carry:
   - normalized UTC value
   - source clock kind
   - source system
   - optional original value/offset where available
4. Keep interval properties such as `validFrom` and `validUntil` out of Phase 2
   unless there is a real interval construction rule.

## Open Questions

1. Is `source_time` enough for Phase 2 membership links, or should commit links
   preserve both author and committer times directly?
2. Should forge snapshots become their own artifact class before PR/issue
   enrichment?
3. Which timestamp fields should be required by pydantic versus allowed as
   artifact-type-specific metadata?
