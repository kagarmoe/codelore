---
title: Automated Reasoning And Assurance Plan
date: 2026-07-04
status: draft
scope: CodeLore evidence-first implementation
depends_on:
  - docs/plans/00b-development-plan-evidence-first.md
  - docs/plans/02-data-engineering-infrastructure-plan.md
  - docs/reviews/2026-07-04-automated-reasoning-review-00b.md
  - docs/evidence/02-evidence-policy.md
---

# CodeLore Automated Reasoning And Assurance Plan

## Purpose

This plan defines how CodeLore's guarantees stay true. The central rule is:

**Every guarantee carries a decision procedure: name the check, or rename the
claim.**

This document is a companion to
`docs/plans/00b-development-plan-evidence-first.md` and
`docs/plans/02-data-engineering-infrastructure-plan.md`, not a replacement.
The infrastructure plan defines where data lives and flows; this plan defines
what must be provably true about it.

Terminology: automated reasoning is the technique family (decision
procedures, solvers, reasoners); high assurance is the goal (justified
confidence in stated guarantees). This plan pursues high assurance using
automated reasoning's conceptual toolkit and a small amount of its actual
machinery — the V-rule validator as a decision procedure, the OWL reasoner
consistency check — while deliberately stopping short of theorem proving (see
Calibration).

## Design Goals

The assurance system must provide:

- every stated guarantee mapped to a named mechanical check
- a small assurance kernel that carries all guarantees
- soundness claims scoped to what is actually decidable
- determinism as a tested property, not an assumption
- revision semantics defined before packs can go stale

The system should avoid:

- precision-sounding language without a check behind it
- semantic judgments quietly assigned to deterministic components
- formal machinery beyond what the MVP rules require
- proofs where a property test suffices
- silent weakening of checks under schedule pressure

## The Assurance Kernel

Five components carry every guarantee in the plan set. Together they are on
the order of a few hundred lines. Each is a pure function over explicit
inputs, has a written specification, and is property-tested.

### 1. ID scheme

Specification: `docs/architecture/11-id-and-serialization-spec.md` (Phase 2).

Per record type: input fields, canonical encoding, hash algorithm, namespace
prefix, collision handling. Volatile fields (`captured_at`, run timestamps)
are excluded from ID inputs so replay identity holds.

Properties: injectivity on distinct canonical inputs, stability across runs,
independence from field ordering.

### 2. Canonical serializer

Same specification document. Rules: UTF-8, NFC-normalized text, sorted object
keys, RFC3339 UTC timestamps, no floats in canonical form (or fixed
formatting), record arrays sorted by stable ID, LF newlines. The canonical
on-disk form is a manifest plus per-collection JSONL, per the infrastructure
plan.

Properties: round-trip fidelity, canonicalization idempotence, byte equality
under input reordering.

### 3. Pack integrity checker

Exposed as `codelore check-pack`; runs at the assemble stage; assembly fails
closed on violation.

Checks: every ID reference resolves in-pack; reference direction has a single
owner (claims own `warrant_ids`; no back-references without a validated
reason); every evidence record resolves to an artifact record; every link
source and target resolves; window consistency — claims cite only evidence
scoped to their window, and cited artifacts' membership includes the window.

### 4. Accountability checker

The "nothing is dropped silently" guarantee, stated correctly for fan-out and
fan-in stages: every stage-input record is either referenced by at least one
output record or enumerated in the manifest's drop list with a reason code.
Asserted at each stage boundary; re-checked end to end from the manifest and
materialized intermediates.

### 5. V-rule validator

Sound and complete with respect to the V-rules only (see below). Sits behind
every generator. V-rule rejections are recorded in the manifest distinctly
from audit findings, so mechanical failure and semantic judgment are never
conflated.

## Guarantee-To-Check Map

Every guarantee in the plan set, with its check:

- "Rebuilding in replay mode produces byte-identical packs" -> CI determinism
  gate: build the fixture window twice under different hash seeds,
  byte-compare (manifests compared modulo volatile run metadata).
- "Nothing is dropped silently" -> accountability checker (runtime assertion
  per stage; end-to-end recheck).
- "Claims that fail validation are never passed through" -> V-rule validator
  behind every generator; manifest distinguishes rejection classes.
- "Every claim has provenance, warrant, confidence, and status" -> schema
  validation plus integrity checker.
- "Claims cite only in-window evidence" -> integrity checker window rule.
- "Every dossier sentence traces to claims" -> mechanical citation-coverage
  check on the rendered output; semantic adequacy via the sampled audit.
- "The graph is fully rebuildable from the pack" -> Phase 6 rebuild-twice test:
  load, drop, reload, diff.
- "The ontology is consistent" -> OWL reasoner check at Phase 8 export.
- "Claim quality meets the bar" -> the stratified audit protocol (n >= 30,
  error rate <= 10%, false-abstention sample), which is a G-rule instrument,
  not a validator property.

A guarantee that cannot be placed in this table is renamed an aspiration in
the docs that state it.

## V-Rules And G-Rules

The evidence policy's minimum-support rules split into two kinds.

V-rules are mechanically decidable from the pack alone. Examples: cited span
exists and contains the quoted text; cited artifact class is allowed for the
claim type; distinct-artifact-type count meets the rule; warrant present with
the required type; claim window matches evidence window.

G-rules are semantic obligations on generators: "clearly states the problem,"
"authoritative source stating the change," "the inference did not overreach."
Their instrument is the stratified sampled audit, with thresholds recorded in
the development plan and revisable only with written justification.

The V-rules are enumerated exhaustively per claim type in
`docs/evidence/10-v-rule-specification.md`, a Phase 3a entry deliverable:
3a claim code does not merge before the V-rule spec exists.

Scoping rule: "no contradictory direct evidence" (narrow inference) is decided
closed over the pack's extracted evidence and is therefore only as strong as
extraction; every `behavior_guard_inference` warrant states this in
`limitations`.

## Determinism And Replay

Two build modes, never mixed silently:

- Replay: inputs are existing snapshots only; byte-identical output is
  guaranteed and tested.
- Fresh: new acquisition or new model extraction; always a new run with a new
  manifest; IDs change only where content changed.

Known leak classes, each a test obligation: hash-seed-dependent iteration
order, filesystem listing order, JSON key order, float formatting, unicode
normalization (NFC vs NFD), timezone handling, wall-clock reads during replay,
locale-dependent sorting, parallelism, and git's own nondeterminism
(rename-detection thresholds — pin the flags and record the git version in
the manifest).

Runs over the same snapshots with different code versions are distinct runs;
the manifest records the code version, and prior packs remain addressable
(retention policy is an open decision in the infrastructure plan).

## Revision Semantics

Packs are derived views. New evidence means a new run: statuses and rungs are
recomputed by full re-derivation, never mutated in place.

This is sufficient because MVP rules are non-recursive — claims never premise
other claims — so claim status is a well-defined pure function of the pack's
evidence state. No defeasible-logic or argumentation machinery is needed.

`Claim REVISED_BY Claim` relates claims across runs and windows and is
deferred to Phase 8 cross-window work.

Guard: if any future rule admits claims as premises for other claims, stop —
that is the escalation trigger for stratified evaluation or real argumentation
semantics, and it must be designed before such a rule ships.

## Open-World Boundary

The ontology is open-world; every answer is closed over the corpus. The
standard scope line — "complete relative to the ingested corpus recorded in
the run manifest, silent about the world beyond it" — renders on every `ask`
answer and in the dossier header.

Corollary: extraction quality bounds the closure. Checks that quantify over
"all evidence" quantify over extracted evidence, and say so.

## Property-Based Testing

Hypothesis targets, mirroring the kernel:

- ID scheme: injectivity, stability, permutation invariance.
- Serializer: round-trip, idempotence, byte equality across orderings.
- Integrity checker: rejects every generated dangling-reference mutation;
  accepts every generated well-formed pack.
- Accountability checker: conservation holds across generated stage traces.
- V-rules: generated claim/evidence permutations exercise each rule's pass and
  fail sides.

CI gates: the double-build determinism test, and publication of the pack's
JSON Schema so third parties can verify pack integrity independently.

## Calibration: Where Rigor Stops

- No theorem provers, no TLA+, no SPARK-grade proof: CodeLore is a
  single-writer batch pipeline whose kernel is pure functions; property tests
  plus runtime assertions carry the guarantees.
- Extractors, renderers, and CLI get conventional tests plus the sampled
  audit.
- Model outputs are never trusted and never "verified" — they are validated
  (V-rules) and audited (G-rules).
- Escalation triggers: claims-as-premises (argumentation semantics);
  concurrent writers (a real consistency model); a user-facing query language
  (safety review).

## Decision Gates

- V-rule spec gate: Phase 3a claim code does not merge before the V-rule
  specification exists.
- Threshold gate: audit thresholds change only with recorded justification.
- Formality gate: escalate past property testing only on the named triggers.

## Risks

### Risk: the validator is quietly weakened

Mitigation: the V-rule spec is normative; CI runs the validator's property
tests; the manifest separates rejection classes so weakening is visible.

### Risk: determinism rots as features land

Mitigation: the double-build byte-compare is a required CI gate, not an
optional check.

### Risk: audits get skipped under time pressure

Mitigation: audit results are data in the manifest; the acceptance memo
cannot be produced without them.

### Risk: the kernel grows past auditability

Mitigation: a new guarantee requires a new named check in the
guarantee-to-check map; kernel size is reviewed when the map grows.

## Open Decisions

1. Hash algorithm and namespace format for IDs (full SHA-256 versus truncated,
   and the IRI prefix scheme).
2. Where the corpus-scope line renders in the dossier layout.
3. Whether assemble-time integrity failure produces a quarantined partial pack
   for debugging or fails closed with intermediates only (lean: fail closed).
4. Audit stratification unit: per claim type, per generator, or both.

## Immediate Tasks

1. Write `docs/architecture/11-id-and-serialization-spec.md` (with tasks 1-2
   of the infrastructure plan).
2. Write `docs/evidence/10-v-rule-specification.md` before Phase 3a claim
   code.
3. Implement the integrity and accountability checkers with property tests.
4. Add the CI double-build determinism gate.
5. Publish the pack JSON Schema.

## Summary

CodeLore's credibility rests on a small assurance kernel: stable IDs,
canonical serialization, referential integrity, drop accountability, and
decidable validation. Everything else is tested conventionally and audited
statistically. The discipline is one sentence long: name the check, or rename
the claim.
