---
title: Operational Schema
date: 2026-07-04
status: current
supersedes:
  - docs/architecture/archive/06-schema-draft.md
---

# CodeLore Operational Schema

## Purpose

This document defines the current operational schema for the evidence-pack
architecture. It is intentionally narrower than the earlier graph schema draft.

The schema starts with records CodeLore can construct and validate. Broader
ontology remains deferred until construction rules, query value, and failure
modes are clear.

## Schema Rule

CodeLore stores project memory as:

- thin canonical identities
- window-scoped observations
- normalized artifact records
- relationship records
- evidence records
- claims and warrants
- contradictions, abstentions, and open questions
- explicit identity-resolution decisions

The evidence pack carries the authoritative records. Graphs and RDF are
projections.

## Scope

### Canonical Scope

Canonical records represent enduring identities across windows.

Examples:

- `Project`
- `Module`
- `Symbol`
- deferred `Concept`
- deferred `ProblemClass`
- deferred `DecisionTheme`

Canonical records are thin and should not absorb window-specific history.

### Window Scope

Window-scoped records represent artifacts, observations, evidence, reasoning,
and relationships bound to a `ChangeWindow`.

Examples:

- `ArtifactRecord`
- `LinkRecord`
- `Evidence`
- `Claim`
- `Warrant`
- `ModuleObservation`
- `ProblemObservation`
- `IdentityResolution`

Window membership is relational, represented by `LinkRecord`.

## Core Records

### Project

Required:

- `project_id`
- `name`

Optional:

- `repo_url`
- `default_branch`
- `hosting_provider`

### ChangeWindow

Required:

- `window_id`
- `window_type`
- `label`
- `project_id`

Optional:

- `start_ref`
- `end_ref`
- `start_time`
- `end_time`
- `build_status`

Window types:

- `release`
- `commit_range`
- `date_range`

Phase 2 implements release windows only, with release/tag parsing at the CLI
edge and resolved refs passed to the core builder.

## Artifact Records

`ArtifactRecord` is the normalized record of a source object.

Required:

- `artifact_record_id`
- `artifact_type`
- `locator_type`
- `source_locator`

Optional:

- `source_system`
- `native_id`
- source-derived timestamps
- `normalized_by`
- `checksum`
- metadata

MVP artifact classes:

- `release`
- `tag`
- `commit`
- `diff`
- `pull_request`
- `issue`
- `comment`
- `release_note`
- `doc_change`
- `test_change`
- `adr`

Phase 2 deterministic git subset:

- tag
- commit
- diff
- changed path/doc/test artifacts where constructible

## Link Records

`LinkRecord` is the structured relationship or membership record.

See `01-evidence-pack-pipeline.md` for the Phase 2 relation contract.

Required Phase 2 fields:

- `link_id`
- `window_id`
- `relation_type`
- `source_id`
- `target_id`
- `link_method`

Optional:

- `confidence`
- `membership_type`
- `evidence_ids`

Initial relation types:

- `native_to_window`
- `linked_to_window`
- `parent_of`
- `includes_diff`

## Evidence, Claims, And Warrants

### Evidence

`Evidence` is extracted support from an artifact or structural source.

Required:

- `evidence_id`
- `evidence_type`
- `artifact_record_id` or structural support reference
- `window_id`

Optional:

- `source_ref`
- `span_start`
- `span_end`
- `excerpt`
- `capture_method`
- `evidence_role`

### Claim

`Claim` is a typed, window-scoped proposition.

Required:

- `claim_id`
- `window_id`
- `claim_type`
- `statement`
- `subject_refs`
- `evidence_ids`
- `warrant_ids`
- `confidence`
- `status`

Claim statuses:

- `supported`
- `contested`
- `insufficient`
- `abstained`

MVP claim types:

- `artifact_link`
- `change_fact`
- `explicit_problem`
- `explicit_decision`
- `narrow_inference`

### Warrant

`Warrant` is the rule explaining why evidence supports a claim.

Required:

- `warrant_id`
- `warrant_type`
- `rule_name`
- `rule_text`
- `supporting_artifact_ids`

Optional:

- `counterevidence_ids`
- `limitations`

The claim owns `warrant_ids`; `Warrant` does not need a back-reference to
`claim_id` in the pack.

## Observations

Observation records describe historically bounded state.

Initial observation types:

- `ModuleObservation`
- `SymbolObservation`
- `ConceptObservation`
- `ProblemObservation`
- `DecisionObservation`

Observations carry:

- `observation_id`
- window scope
- observed name or statement
- change kind where applicable
- extraction method
- source artifact count
- status

Observations are not canonical identities. Canonicalization is a later
evidence-backed decision.

## Reasoning And Analysis Records

### Contradiction

Preserved conflict between evidence or claims.

### Abstention

Structured declaration that the evidentiary bar was not met.

Reason codes:

- `no_evidence`
- `insufficient_evidence`
- `conflicting_evidence`
- `unsupported_inference`

### OpenQuestion

Investigation-state record for unresolved questions.

### IdentityResolution

Decision record for canonicalization outcomes:

- `same_identity`
- `likely_same`
- `uncertain`
- `likely_different`
- `different_identity`

Identity resolution carries evidence, method, confidence, and limitations.

## Phase 2 Pack Subset

Phase 2 writes:

- `manifest.json`
- `project.json`
- `window.json`
- `artifacts.jsonl`
- `links.jsonl`

Phase 2 does not yet require:

- text evidence extraction
- claims
- warrants
- observations
- identity resolution
- Neo4j projection
- RDF export

## Validation

Pack validation includes:

- schema validation
- stable ID validation
- referential integrity
- relation contract validation
- stage accountability
- no volatile fields in canonical records
- canonical JSONL ordering

Claims later add V-rule validation and sampled audit validation.

## Deferred Areas

Deferred until earned:

- broad concept graph automation
- root-cause claims
- author intent claims
- aggressive symbol lineage
- concept/problem/decision canonicalization
- asserted OWL domain projection
- graph engine adoption as required infrastructure
