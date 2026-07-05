---
title: LinkRecord Model
date: 2026-07-04
status: draft
depends_on:
  - docs/architecture/06-schema-draft.md
  - docs/architecture/08-rdf-export-decision.md
  - docs/architecture/09-temporal-validity.md
  - docs/plans/02-data-engineering-infrastructure-plan.md
  - docs/plans/03-phase-2-implementation-plan.md
---

# CodeLore LinkRecord Model

## Purpose

`LinkRecord` is CodeLore's first-class relationship record.

It exists so relationships are not hidden in prose claims, embedded ID lists, or
graph-database edges that cannot be validated before projection.

The core distinction is:

```text
LinkRecord = structured relationship or membership record
Claim = proposition CodeLore advances
Evidence = cited source support
Warrant = rule connecting evidence to claim
```

`LinkRecord` is part of the evidence pack. Neo4j edges and RDF named reifiers
are derived projections from it.

## What A LinkRecord Is

A `LinkRecord` records that CodeLore has established a typed relationship
between two durable records.

Examples:

- a commit is native to a window
- an artifact is linked to a window as context
- a commit has a parent commit
- a commit includes a diff
- a diff touches a file
- a PR is linked to a commit
- an issue is referenced by a PR
- a release note is linked to a release window

A link record is intentionally small, typed, and mechanically checkable.

## What A LinkRecord Is Not

A `LinkRecord` is not:

- a natural-language claim
- a warrant
- a citation span
- a graph-engine edge as source of truth
- an RDF syntax artifact
- proof that a domain proposition is globally true
- a substitute for temporal validity fields

It may support claims, but it is not itself the whole claim/warrant/evidence
structure.

## Relationship To Claim, Evidence, And Warrant

CodeLore's reasoning shape is:

```text
Evidence + Warrant -> Claim
```

`LinkRecord` participates in that shape as structured support.

Example:

- `LinkRecord`: commit `abc` is native to window `v1.1.0 -> v1.2.0`.
- `Evidence`: git reachability result and resolved refs.
- `Warrant`: reachable from end ref and not from start ref means native window
  membership.
- `Claim`: commit `abc` is part of the release window.

Another example:

- `LinkRecord`: commit `abc` includes diff record `diff-123`.
- `Evidence`: diff name-status and hunk metadata for `scheduler.py`.
- `Warrant`: a diff produced by a native commit supports a `changed_in_window`
  file claim.
- `Claim`: `scheduler.py` changed in this release window.

## Phase 2 Minimal Model

Phase 2 implements the deterministic git-first subset.

Required fields:

- `link_id`
- `window_id`
- `relation_type`
- `source_id`
- `target_id`
- `link_method`

Optional fields:

- `confidence`
- `membership_type`
- `evidence_ids`

Phase 2 deliberately excludes run-scoped and wall-clock fields from record
bodies. Run provenance belongs in `manifest.json`; record bytes must remain
stable across replay.

### Initial Enums

Initial `RelationType` values:

- `native_to_window`
- `linked_to_window`
- `parent_of`
- `includes_diff`

Initial `LinkMethod` values:

- `explicit`
- `structural`
- `heuristic`
- `inferred`

Initial `MembershipType` values:

- `native`
- `linked`
- `inferred`

`inferred` is enum-reserved in Phase 2 but must not be emitted until an
inference rule and warrant contract are admitted.

These are the Phase 2 implementation values, not the full ontology.

### Phase 2 Relation Contract

Phase 2 relation direction is normative.

| relation_type | source kind | target kind | allowed link_method | allowed membership_type | confidence |
| --- | --- | --- | --- | --- | --- |
| `native_to_window` | `window` | `artifact` | `structural` | `native` | optional |
| `linked_to_window` | `window` | `artifact` | `explicit`, `structural`, `heuristic` | `linked` | required for `heuristic` |
| `parent_of` | `commit` | `commit` | `structural` | none | optional |
| `includes_diff` | `commit` | `diff` | `structural` | none | optional |

Endpoint kinds may be stored explicitly or derived from the stable ID prefix,
but the pack integrity checker must validate them mechanically.

Illegal examples:

- `native_to_window` with `membership_type = linked`
- `parent_of` with `membership_type = native`
- `linked_to_window` with `link_method = heuristic` and no confidence
- relation endpoints that do not match the contract table

## Membership Links

Window membership is represented by link records.

This follows the schema rule that membership is relational, not identity
defining.

Examples:

```text
window --native_to_window--> commit
window --linked_to_window--> release_note
window --linked_to_window--> pull_request
```

`membership_type` refines the membership:

- `native`: directly part of the window by construction rule
- `linked`: contextual artifact connected to a native artifact or boundary
- `inferred`: included by a weaker rule that must be warranted

For Phase 2, native git membership should be structural and deterministic.

## Structural Links

Structural links record deterministic relationships among artifacts.

Examples:

```text
commit --parent_of--> commit
commit --includes_diff--> diff
```

Only relation types implemented in code should be emitted. Candidate relation
names belong in architecture docs until admitted.

## Temporal Semantics

`LinkRecord` can carry temporal membership semantics, but it should not become a
catch-all time model.

For Phase 2, the accepted policy is:

- membership is ref-reachability based
- canonical serialization sorts by stable ID
- timelines label the selected clock
- run timestamps live in the manifest

Future temporal fields may include:

- `membership_basis`
- `source_time`
- `source_time_kind`
- `snapshot_time`

These are proposed in `docs/architecture/09-temporal-validity.md` but are not
part of the minimal Phase 2 model unless the implementation plan is updated.

## Volatile Field Policy

Canonical `LinkRecord` bodies must not contain run-scoped or wall-clock fields.

Excluded from canonical links:

- `run_id`
- `created_at`
- ingestion wall-clock timestamps
- command invocation
- environment details

These belong in `manifest.json` or stage records. This keeps `links.jsonl`
byte-identical under replay.

## Validation Rules

The pack integrity checker should validate:

- every `link_id` is unique
- every `window_id` resolves
- every `source_id` resolves
- every `target_id` resolves
- every `evidence_id` resolves
- `membership_type` is present for `native_to_window` and `linked_to_window`
  links
- no run-scoped volatile fields appear in canonical link records
- relation type and membership type combinations are legal
- relation endpoints match the Phase 2 relation contract
- `confidence` is present when required by the contract
- `link_id` recomputes from the canonical ID input fields
- canonical link ordering is by `link_id`
- support basis is present: either `evidence_ids` is non-empty, or the link is
  structural and supported by named acquire/window-stage inputs in the run
  manifest

Invalid links should fail pack assembly. They should not be silently dropped
unless the drop is recorded in the run manifest with a reason.

## Neo4j Projection

Neo4j edges are derived from `LinkRecord`.

Projection rules:

- `relation_type` maps to edge label or edge type.
- `link_id` maps to an edge property.
- `confidence`, `membership_type`, and `link_method` map to edge properties.
- source and target IDs identify endpoint nodes.
- the graph is rebuildable from the pack.

The graph must not invent relationships that are absent from `links.jsonl`.

## RDF Projection

RDF export uses `LinkRecord` as the named reifier resource when a link
corresponds to a subject-predicate-object proposition.

Example:

```turtle
:link-123
  rdf:reifies <<( :commit-abc cl:touchesFile :file-scheduler )>> ;
  a cl:LinkRecord ;
  cl:linkMethod cl:Structural ;
  cl:membershipType cl:Native .
```

The RDF representation is a projection. The pack record remains authoritative.

## Relation Admission

A new relation type should be admitted only when it has:

- distinct construction rules
- distinct query value
- distinct failure modes
- validation rules
- projection behavior for JSONL, Neo4j, and RDF where relevant

Do not add relation types only because they are convenient labels.

## Open Decisions

1. Should `touches_file` be admitted in Phase 2, or represented through
   `includes_diff` plus diff artifact fields until Phase 3?
2. Should `membership_basis` be added to the Phase 2 model immediately, or
   captured in warrants and manifest policy first?
3. Should `confidence` be required for non-structural links?
4. How should `LinkRecord` cite evidence when the evidence is a structural git
   command result rather than a separately materialized `Evidence` record?

## Summary

`LinkRecord` is the pack-side relationship primitive. It gives CodeLore a stable
way to represent membership and structural relationships before any graph
database or RDF export exists.

The test for `LinkRecord` is simple: if a relationship matters to claims,
warrants, graph projection, or RDF export, it should be explicit, typed,
validated, and replay-stable in `links.jsonl`.
