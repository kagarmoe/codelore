---
title: High-Assurance Review — Record Admission Model
date: 2026-07-04
reviewer-lens: invariants, decidability, replay guarantees, and accountability checks
artifact: docs/architecture/11-record-admission-model.md
status: amendments applied
tags:
  - codelore
  - review
  - high-assurance
  - record-admission
---

# High-Assurance Review — `docs/architecture/11-record-admission-model.md`

Lens: High-Assurance Reviewer (Cook). Functional focus: checkable guarantees
and the validation kernel.

## Top Findings

### 1. The document needs named invariants

Observation: It says every record has type, identity, provenance, validation,
and accountable reason for existing.

Interpretation: Good, but this should become named checks.

Recommendation: Add:

- `candidate_accountability`
- `stable_record_identity`
- `canonical_records_validated`
- `no_silent_rejection`
- `manifest_reason_codes_valid`

### 2. "Validation behavior" should split schema, reference, and V-rule checks

Observation: Universal admission requirements include validation behavior.

Interpretation: That is too broad for implementation.

Recommendation: Require each admission rule to identify which validation layer
it participates in: schema, referential integrity, stage accountability,
V-rule, audit.

### 3. Generator-based admission needs snapshot-before-parse

Observation: The doc says generator outputs are snapshotted before admission.

Interpretation: Correct. This is a replay invariant and should be elevated.

Recommendation: Add it to named invariants.

## What Is Strong

- Rejected candidates are first-class accountability data.
- Replay mode is treated as a distinct mode.
- Claim failures become drops/abstentions rather than invalid claims.

## What Is Weak Or Risky

- Too many guarantees are not yet named as checks.
- Candidate boundary needs a formal trigger.

## Concrete Recommendations

1. Add named invariants.
2. Add validation-layer field to admission registry.
3. Add snapshot-before-admission invariant for generator stages.

## Open Questions

1. Which invariants must block pack assembly in Phase 2?
