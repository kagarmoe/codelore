---
title: Schema Review — Record Admission Model
date: 2026-07-04
reviewer-lens: schema contracts, implementation ambiguity, and validation boundaries
artifact: docs/architecture/11-record-admission-model.md
status: amendments applied
tags:
  - codelore
  - review
  - schema
  - record-admission
---

# Schema Review — `docs/architecture/11-record-admission-model.md`

Lens: Schema Skeptic (Sadalage). Functional focus: implementation contracts and
where ambiguous schema boundaries will drift.

## Top Findings

### 1. The model needs record-state names that map to code

Observation: The doc has raw input, candidate datum, admitted record, validated
pack record, and rejected candidate.

Interpretation: Good. But these names should map to code/test fixtures, or they
will remain conceptual.

Recommendation: Add a small state transition table with allowed transitions.

### 2. "Admitted but not validated" needs containment

Observation: An admitted record is schema-valid but may fail pack-level checks.

Interpretation: That is useful internally, but dangerous if admitted records are
written to canonical JSONL before pack checks.

Recommendation: State that only validated pack records enter canonical JSONL.
Admitted-but-not-pack-valid records are stage intermediates only.

### 3. Rejection reasons need ownership

Observation: Reason codes are listed as manifest vocabulary.

Interpretation: Good, but codes will drift unless the manifest schema owns
them.

Recommendation: Specify that rejection reason codes are enum-like manifest
schema values.

## What Is Strong

- Clear universal admission requirements.
- Strong separation of artifact/evidence/claim/warrant admission.
- Good interoperability rationale.

## What Is Weak Or Risky

- "Candidate datum" may be interpreted too broadly.
- The registry could duplicate code unless generated or tested.

## Concrete Recommendations

1. Add a state transition table.
2. State canonical JSONL contains only validated pack records.
3. Tie rejection reason codes to manifest schema.

## Open Questions

1. Should admission rules be pydantic models, plain functions, or documented
   validators in Phase 2?
