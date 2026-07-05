---
title: Record Admission Model
date: 2026-07-04
status: draft
depends_on:
  - docs/plans/00b-development-plan-evidence-first.md
  - docs/plans/02-data-engineering-infrastructure-plan.md
  - docs/architecture/09-temporal-validity.md
  - docs/architecture/10-link-record-model.md
---

# CodeLore Record Admission Model

## Purpose

This document defines how information becomes a durable CodeLore record.

It fills the ETL gap between raw source material and canonical evidence-pack
records.

The central rule is:

**Information becomes a record only through an explicit admission rule.**

Finding something in a repository is not enough. CodeLore must decide:

- what kind of record it is
- how it is identified
- where it came from
- which stage admitted it
- which validation rules apply
- what happens if it is rejected

## Admission Pipeline

The admission path is:

```text
raw input -> candidate datum -> admitted record -> validated pack record
```

Rejected candidates are not silently dropped. They are recorded in the run
manifest drop list with a reason code when they were within the stage's input
scope.

## Core Terms

### Raw Input

Raw input is external or upstream material before CodeLore has normalized it.

Examples:

- git object
- git command output
- file content
- diff text
- GitHub API response
- release note body
- model output snapshot

Raw input is preserved as a snapshot when replayability requires it.

### Candidate Datum

A candidate datum is something a stage has found that may become a record.

Examples:

- a commit from `git rev-list`
- a changed path from `git diff --name-status`
- a PR number parsed from a commit message
- a text span that appears to state a problem
- a relationship between two artifacts

Candidate data are process-state objects, not pack ontology. They become
durable only as admitted records, rejected-candidate manifest entries, or
product-level records such as abstentions.

### Admission Rule

An admission rule decides whether a candidate datum becomes a record.

Every admission rule should define:

- input type
- output record type
- required fields
- stable ID inputs
- provenance requirements
- validation checks
- rejection reasons

Admission rules should be deterministic unless the stage is explicitly
generator-based. Generator-based stages still require deterministic validation.

### Admitted Record

An admitted record is schema-valid and has a stable ID, but may still fail
pack-level integrity checks.

Examples:

- an `ArtifactRecord` for commit `abc`
- a `LinkRecord` connecting a window to that commit
- an `Evidence` span extracted from a PR body
- a `Claim` produced by a claim generator
- a `Warrant` attached to the claim

### Validated Pack Record

A validated pack record has passed:

- pydantic schema validation
- stable ID validation
- referential-integrity validation
- stage accountability validation
- any type-specific V-rules

Only validated records appear in canonical JSONL pack collections.

Admitted-but-not-pack-valid records are stage intermediates only. They must not
be written to canonical JSONL.

### Rejected Candidate

A rejected candidate is a candidate datum that did not become a record.

Examples:

- malformed commit metadata
- PR number parse that does not resolve
- text span that fails span validation
- relationship whose endpoints cannot be resolved
- claim candidate that lacks required evidence

Rejected candidates should be recorded in the manifest when they were part of a
stage's declared input scope.

Parser non-matches are not automatically rejected candidates. A stage must
declare when a possible datum crosses the candidate boundary. Non-matches before
that boundary may be summarized as parser metrics.

### Derived Record

A derived record is produced from already admitted upstream records.

Examples:

- a `LinkRecord` derived from admitted window and commit records
- an `Evidence` record derived from an admitted artifact record
- a deterministic `Claim` derived from admitted evidence and links

Derived records still require admission rules. Derivation does not bypass
validation.

## Universal Admission Requirements

Every admitted record needs:

1. record type
2. stable ID
3. stable ID input fields
4. source or upstream record reference
5. stage name
6. admission rule name
7. schema-valid fields
8. validation behavior
9. rejection behavior

Run-scoped metadata belongs in the manifest, not canonical record bodies, unless
the record type explicitly admits it as source-derived data.

Each admission rule must state which validation layers apply:

- schema validation
- referential-integrity validation
- stage-accountability validation
- V-rule validation
- sampled audit validation

## Record-Type Admission

### ArtifactRecord Admission

`ArtifactRecord` admits normalized source objects.

Candidate examples:

- commit
- tag
- diff
- changed path
- PR
- issue
- comment
- release note

Admission requires:

- artifact type
- locator type
- source locator
- stable ID inputs
- source system
- source-derived timestamps when available

Artifact records are not claims. They record that CodeLore captured or
normalized a source object.

### LinkRecord Admission

`LinkRecord` admits typed relationships between durable records.

Candidate examples:

- window includes commit by reachability
- commit has parent commit
- commit includes diff
- release note linked to release window
- PR linked to commit

Admission requires:

- relation type
- source endpoint
- target endpoint
- endpoint kinds or mechanically derivable endpoint kinds
- link method
- legal relation contract
- membership type where required

Invalid endpoint combinations are rejected.

### Evidence Admission

`Evidence` admits extracted support from artifacts or structural acquisition.

Candidate examples:

- quoted text span
- diff hunk
- structural relation support
- release note section

Admission requires:

- source artifact or structural support reference
- evidence type
- locator or span where applicable
- extraction method
- exact excerpt where text is used
- span validation for textual evidence

Evidence is not itself a claim. It is cited support.

### Claim Admission

`Claim` admits a proposition CodeLore is willing to advance, contest, mark
insufficient, or abstain from within a window.

Candidate examples:

- file changed in window
- PR explicitly stated a problem
- release includes commit
- test change supports a narrow behavior-guard inference

Admission requires:

- claim type
- window ID
- subject references
- evidence IDs or structured support
- warrant IDs
- status
- confidence when status requires it

Claims that fail V-rules are rejected or converted into abstentions, not
silently emitted.

### Warrant Admission

`Warrant` admits a reasoning rule connecting evidence to a claim.

Candidate examples:

- reachability supports window membership
- direct quoted PR text supports an explicit problem claim
- diff produced by native commit supports changed-in-window claim
- test hunk plus code hunk supports a narrow behavior-guard inference

Admission requires:

- warrant type
- rule name
- rule text
- supporting evidence or artifact IDs
- limitations
- counterevidence IDs where available

A warrant is not extra evidence and is not itself the claim. It is the reasoning
bridge:

```text
Evidence + Warrant -> Claim
```

### Abstention Admission

`Abstention` admits a completed analysis result when the evidentiary bar was
not met.

Candidate examples:

- why claim lacks support
- conflicting evidence cannot be resolved
- candidate inference lacks a typed rule
- source artifacts are too sparse

Admission requires:

- reason code
- window ID
- summary
- relevant evidence or missing-evidence description

An abstention is not a pipeline failure. It is a valid product result.

## Stage Accountability

Every stage declares its input scope.

For every stage-input candidate, one of the following must be true:

- it is represented by at least one admitted output record
- it is recorded as rejected with a reason
- it is out of scope by the stage's declared filter

Counts alone are not enough. Fan-out stages need record-level accountability.

## Rejection Reasons

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

Reason codes are part of the manifest vocabulary and should stay stable.
They should be modeled as enum-like manifest schema values, not free text.

## State Transitions

Allowed transitions:

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

Initial invariants:

- `candidate_accountability`: every declared candidate is admitted, rejected, or
  declared out of scope.
- `stable_record_identity`: admitted records use stable ID inputs and canonical
  encoding.
- `canonical_records_validated`: only pack-valid records enter canonical JSONL.
- `no_silent_rejection`: rejected candidates in stage input scope have reason
  codes.
- `manifest_reason_codes_valid`: rejection reason codes come from the manifest
  vocabulary.
- `snapshot_before_generator_admission`: generator outputs are snapshotted
  before parsing or admission.

Phase 2 structural git support lives in manifest/acquire records. Phase 3 may
promote structural support into `Evidence` records where claims need direct
evidence citations.

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
stabilizes. A suggested initial location is
`docs/architecture/12-admission-rule-registry.md`, unless Phase 2 implements the
registry directly in code first.

## Replay And Determinism

In replay mode, admitted records must be stable for the same inputs and code.

Rules:

- stable IDs derive only from specified canonical inputs
- run-scoped metadata stays in the manifest
- generator outputs are snapshotted before admission
- fresh generation is a new run, not replay
- canonical JSONL records sort by ID

## Interoperability

Record admission supports several kinds of interoperability:

- data interoperability: JSONL, Neo4j, RDF, structured query tiers
- disciplinary interoperability: maintainers, data engineers, ontology
  reviewers, and historians can inspect the same admission rules
- agent interoperability: future agents can determine whether a record should
  exist without guessing
- review interoperability: critiques can target admission rules rather than
  vague extraction behavior

## Open Decisions

1. Should admission-rule registries live in docs first, code first, or both?
2. Which rejected candidates must be listed individually versus summarized by
   count?
3. Should `Evidence` admit structural git support in Phase 2, or should
   structural support live in manifest records until Phase 3?
4. Which rejection reason codes are mandatory for Phase 2?
5. Should admission failures become abstentions only in reasoning stages, or
   can earlier-stage failures also produce abstention records?

## Summary

Record admission is the boundary where information becomes durable CodeLore
data.

Without explicit admission rules, the pipeline cannot be replayable,
auditable, or honestly reviewed. With them, every record in the evidence pack
has a type, identity, provenance, validation path, and accountable reason for
existing.
