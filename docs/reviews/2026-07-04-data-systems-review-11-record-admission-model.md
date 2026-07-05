---
title: Data Systems Review — Record Admission Model
date: 2026-07-04
reviewer-lens: data systems, ETL boundaries, source-of-truth design, and replayability
artifact: docs/architecture/11-record-admission-model.md
status: amendments applied
tags:
  - codelore
  - review
  - data-systems
  - record-admission
---

# Data Systems Review — `docs/architecture/11-record-admission-model.md`

Lens: Data Systems Reviewer (Kleppmann). Functional focus: ETL boundaries,
source-of-truth design, replayability, and operational accounting.

## Top Findings

### 1. The doc names the missing ETL boundary

Observation: It defines raw input, candidate datum, admitted record, validated
pack record, and rejected candidate.

Interpretation: This is the right abstraction. It prevents raw extraction from
becoming durable data without a contract.

Recommendation: Keep this as required orientation for pipeline implementation.

### 2. Candidate accountability needs a pragmatic scope limit

Observation: The doc says rejected candidates are recorded when within the
stage's input scope.

Interpretation: Good caveat. Without it, stages that scan text or diffs could
produce enormous rejected-candidate logs.

Recommendation: Add a rule: only declared candidates need individual accounting.
Exploratory parser non-matches can be summarized by parser metrics unless they
cross the candidate boundary.

### 3. Structural support should have a Phase 2 decision

Observation: The doc leaves open whether structural git support becomes
`Evidence` in Phase 2.

Interpretation: This blocks implementation choices. Phase 2 creates links and
artifacts but not the full evidence pipeline.

Recommendation: Decide: Phase 2 structural support lives in manifest/acquire
records; Phase 3 promotes structural support into `Evidence` where needed.

## What Is Strong

- Clear lifecycle from raw input to validated pack record.
- Manifest drop accountability is included.
- Replay and determinism rules are aligned with JSONL pack design.

## What Is Weak Or Risky

- The line between candidate datum and parser non-match needs tightening.
- The admission-rule registry is not yet assigned a concrete file or owner.

## Concrete Recommendations

1. Add declared-candidate boundary language.
2. Decide the Phase 2 structural-support location.
3. Add a suggested registry path, even if it starts as docs.

## Open Questions

1. Should `docs/architecture/12-admission-rule-registry.md` be created before
   implementation, or should the first registry live in code?
