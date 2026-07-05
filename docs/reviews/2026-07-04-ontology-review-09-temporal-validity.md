---
title: Ontology Review — Temporal Validity Model
date: 2026-07-04
reviewer-lens: ontology commitments, temporal category admission, and sign-to-claim interpretation
artifact: docs/architecture/09-temporal-validity.md
status: amendments applied
tags:
  - codelore
  - review
  - ontology
  - temporal-validity
---

# Ontology Review — `docs/architecture/09-temporal-validity.md`

Lens: Ontology Reviewer (Quine) plus Ontology Reviewer (Peirce). Functional
focus: category admission, naming discipline, and the path from artifact time to
historical interpretation.

## Top Findings

### 1. `validity_kind` risks becoming a premature ontology

Observation: The document lists initial values such as `observed_in_window`,
`introduced_in_window`, `changed_in_window`, and `documented_after_window`.

Interpretation: These are useful analytical statuses, but not all are
ontologically equal. `changed_in_window` is construction-rule backed by diff and
membership evidence. `introduced_in_window` is stronger and requires absence or
prior-state evidence. `documented_after_window` describes evidence timing, not
domain validity.

Recommendation: Keep these as candidate statuses until each has explicit
construction rules. In the MVP, admit only the values needed by Phase 2/3a:
`observed_in_window`, `changed_in_window`, and
`unknown_temporal_validity`. Treat `introduced_in_window` as deferred unless
prior-state comparison is implemented.

### 2. The document correctly separates scope from assertion roles

Observation: It says a window scopes analysis and named graph membership is not
truth over time.

Interpretation: Good. The useful cross-disciplinary distinction is claim,
evidence, and warrant. More philosophical vocabulary would not travel cleanly
across ontology, data engineering, and implementation work.

Recommendation: Use a short "Claim, Evidence, And Warrant Roles" section:

- artifact records are source objects
- link records are CodeLore relation records
- claims are propositions advanced by CodeLore
- warrants justify claims
- observations are window-scoped interpretations
- asserted domain facts are filtered projections

This prevents `LinkRecord` from accidentally becoming both assertion and
evidence.

### 3. `Artifact time`, `Evidence time`, and `Claim validity` are earned
distinctions

Observation: The document distinguishes source artifact clocks, evidence timing,
and what CodeLore may claim.

Interpretation: This distinction is ontologically useful because each has
different construction rules and failure modes. Commit author time can be
misleading for membership. Evidence time matters for whether a "why" is
pre-change or post-hoc. Claim validity is a CodeLore assertion status.

Recommendation: Preserve these distinctions. They are not category sprawl; they
prevent false historical claims.

### 4. `Release note membership` is well handled

Observation: The document says release notes may be linked to the window even if
published after the final included commit, while retaining their own evidence
time.

Interpretation: This is the right semiotic move. A release note is a sign
created at one time about code produced earlier. It can support "this release
was described as X" more directly than "the implementation was motivated by X."

Recommendation: Carry this distinction into warrant rules. Release-note-derived
why claims need explicit limitations unless corroborated by pre-merge evidence.

## What Is Strong

- The document blocks a serious modeling error: treating named graph membership
  as temporal validity.
- It does not flatten git topology into timestamps.
- It acknowledges that release windows are ref-defined first and time-described
  second.
- It keeps canonical identity out of temporal observation validity.

## What Is Weak Or Risky

- The candidate temporal vocabulary is useful but broad. Without admission
  rules, it may harden into ontology too quickly.
- `validDuring`, `validFrom`, and `validUntil` are semantically strong terms.
  They should not be admitted until CodeLore can prove interval validity, not
  merely window observation.
- `introduced_in_window` is especially risky because it requires evidence of
  absence before the window or a reliable prior-state comparison.

## Concrete Recommendations

1. Add the "Claim, Evidence, And Warrant Roles" section described above.
2. Mark the temporal validity kinds as candidate vocabulary and specify the MVP
   admitted subset.
3. Rename or constrain `validDuring` candidate usage. Prefer `observedIn` and
   `membershipBasis` until interval semantics are implemented.
4. Require every temporal validity kind to have:
   - construction rule
   - query value
   - failure mode
   - warrant requirement

## Open Questions

1. Does Phase 2 need `introduced_in_window`, or only `changed_in_window`?
2. Should `documented_after_window` be a claim validity kind, an evidence-time
   relation, or a warrant limitation?
3. Will CodeLore ever assert interval truth, or only window-scoped observation,
   before cross-window lineage exists?
