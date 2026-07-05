---
title: Evidence Pack Pipeline
date: 2026-07-04
status: current
supersedes:
  - docs/architecture/archive/10-link-record-model.md
  - docs/architecture/archive/11-record-admission-model.md
---

# Evidence Pack Pipeline

## Purpose

This document defines how raw project information becomes durable CodeLore data.

CodeLore is an evidence-first pipeline:

```text
acquire -> window -> normalize -> extract -> reason -> assemble -> present -> project
```

Each stage has declared inputs, declared outputs, validation rules, and
accountability for drops.

## Record Admission

Information becomes a durable record only through an explicit admission rule.

The admission path is:

```text
raw input -> candidate datum -> admitted record -> validated pack record
```

### Raw Input

Raw input is external or upstream material before CodeLore normalizes it:

- git objects
- git command output
- file content
- diff text
- forge API responses
- release note bodies
- model output snapshots

Raw input is snapshotted when replayability requires it.

### Candidate Datum

A candidate datum is a stage-local possible record:

- a commit from `git rev-list`
- a changed path from `git diff --name-status`
- a PR number parsed from a commit message
- a text span that appears to state a problem
- a relationship between durable records

Candidate data are process state, not pack ontology. They become durable only as
admitted records, rejected-candidate manifest entries, or product-level records
such as abstentions.

Parser non-matches are not automatically rejected candidates. A stage must
declare when a possible datum crosses the candidate boundary.

### Admission Rule

An admission rule defines:

- input type
- output record type
- stable ID inputs
- required fields
- provenance requirements
- validation layers
- possible rejection reasons

Admission rules are deterministic unless the stage is explicitly
generator-based. Generator outputs must be snapshotted before parsing or
admission.

### Admitted Record

An admitted record is schema-valid and has a stable ID, but may still fail
pack-level validation.

Admitted-but-not-pack-valid records are stage intermediates only. They must not
be written to canonical JSONL.

### Validated Pack Record

A validated pack record has passed:

- schema validation
- stable ID validation
- referential-integrity validation
- stage-accountability validation
- type-specific V-rules where applicable

Only validated records appear in canonical pack collections.

### Rejected Candidate

A rejected candidate is a declared candidate that does not become a record.

Initial reason codes:

- `out_of_scope`
- `malformed_input`
- `unresolved_reference`
- `unsupported_artifact_type`
- `schema_validation_failed`
- `span_validation_failed`
- `v_rule_failed`
- `duplicate_record`
- `unsupported_inference`
- `conflicting_evidence`
- `insufficient_evidence`

Reason codes are manifest-schema values, not free text.

## Record Types

### ArtifactRecord

`ArtifactRecord` is the normalized record of a source object.

Examples:

- commit
- tag
- diff
- changed path
- PR
- issue
- comment
- release note

Artifact records are not claims. They say CodeLore captured or normalized a
source object.

### LinkRecord

`LinkRecord` is the first-class relationship or membership record.

It exists so relationships are not hidden in prose claims, embedded ID lists, or
graph-engine edges.

The core distinction is:

```text
LinkRecord = structured relationship or membership record
Claim = proposition CodeLore advances
Evidence = cited source support
Warrant = rule connecting evidence to claim
```

Phase 2 minimal fields:

- `link_id`
- `window_id`
- `relation_type`
- `source_id`
- `target_id`
- `link_method`
- optional `confidence`
- optional `membership_type`
- optional `evidence_ids`

Run-scoped and wall-clock fields do not belong in canonical link records.

### Evidence

`Evidence` is extracted support from an artifact or structural source:

- text span
- diff hunk
- structural relation support
- release note section

Evidence is not itself a claim. It is cited support.

Phase 2 structural git support lives in manifest/acquire records. Phase 3 may
promote structural support into `Evidence` records where claims need direct
evidence citations.

### Claim

`Claim` is a typed, window-scoped proposition CodeLore advances, contests,
marks insufficient, or abstains from.

Claims require:

- claim type
- window ID
- subject references
- evidence or structured support
- warrant IDs
- status
- confidence when applicable

Claims that fail deterministic V-rules are rejected or converted into
abstentions. They are not emitted as weak claims.

### Warrant

`Warrant` is the explicit reasoning rule connecting evidence to claim.

```text
Evidence + Warrant -> Claim
```

A warrant is not extra evidence and is not itself the claim.

### Abstention

`Abstention` is a completed analysis result when the evidentiary bar is not
met.

It is not a pipeline failure. It is a product output that says CodeLore does
not have enough support to claim something.

## LinkRecord Relation Contract

Phase 2 relation direction is normative.

| relation_type | source kind | target kind | allowed link_method | allowed membership_type | confidence |
| --- | --- | --- | --- | --- | --- |
| `native_to_window` | `window` | `artifact` | `structural` | `native` | optional |
| `linked_to_window` | `window` | `artifact` | `explicit`, `structural`, `heuristic` | `linked` | required for `heuristic` |
| `parent_of` | `commit` | `commit` | `structural` | none | optional |
| `includes_diff` | `commit` | `diff` | `structural` | none | optional |

Endpoint kinds may be stored explicitly or derived from stable ID prefixes, but
the pack integrity checker must validate them mechanically.

`inferred` is enum-reserved in Phase 2 but must not be emitted until an
inference rule and warrant contract are admitted.

## Stage Accountability

Every stage declares its input scope.

For every declared stage-input candidate, one of the following must be true:

- it is represented by at least one admitted output record
- it is recorded as rejected with a reason
- it is out of scope by the stage's declared filter

Counts alone are not enough. Fan-out stages need record-level accountability.

## State Transitions

| from | to | allowed when |
| --- | --- | --- |
| raw input | candidate datum | stage extractor declares a possible datum in scope |
| candidate datum | admitted record | admission rule passes local checks |
| candidate datum | rejected candidate | admission rule fails or candidate is out of scope |
| admitted record | validated pack record | pack-level validation passes |
| admitted record | rejected candidate | pack-level validation fails |
| validated pack record | derived record candidate | downstream stage declares a derivation |

No transition may write canonical JSONL before pack validation.

## Named Invariants

- `candidate_accountability`: every declared candidate is admitted, rejected, or
  declared out of scope.
- `stable_record_identity`: admitted records use stable ID inputs and canonical
  encoding.
- `canonical_records_validated`: only pack-valid records enter canonical JSONL.
- `no_silent_rejection`: rejected candidates in stage input scope have reason
  codes.
- `manifest_reason_codes_valid`: rejection reasons come from the manifest
  vocabulary.
- `snapshot_before_generator_admission`: generator outputs are snapshotted
  before parsing or admission.
- `link_contract_valid`: every link matches the relation contract table.

## Admission Rule Registry

Each stage should maintain an admission-rule registry.

Minimum fields:

- rule name
- stage
- input type
- output record type
- deterministic or generator-based
- validation layers
- required validators
- possible rejection reasons

The registry may start as documentation and become code once the pipeline
stabilizes.
