---
title: Automated Reasoning Review — CodeLore Development Plan 00b
date: 2026-07-04
reviewer-lens: automated reasoning / high-assurance systems (Cook/Chapman style)
artifact: docs/plans/00b-development-plan-evidence-first.md
status: amendments applied
tags:
  - codelore
  - review
  - automated-reasoning
  - formal-methods
  - plan
---

# Review: Evidence-First Development Plan — Automated Reasoning / High-Assurance Lens

Artifact: `docs/plans/00b-development-plan-evidence-first.md`. Grounding read: product definition, evidence policy, claim taxonomy, schema draft, canonicalization policy, acceptance criteria, glossary, `src/codelore/models.py`.

## Top Findings (by severity)

### 1. The validator is quietly assigned undecidable checks
**Observation.** "Verifiability and generation" says the deterministic validator checks that a claim "meets the claim type's minimum support from the evidence policy." But the minimum-support rules in `docs/evidence/02-evidence-policy.md` split into two kinds. Mechanically decidable from the pack: span exists, excerpt matches, artifact class ∈ allowed set, artifact count ≥ N, distinct-artifact-type count ≥ 2 (narrow inference), warrant present and typed. Not decidable: "clearly states the problem," "authoritative source artifact **stating the change**," "no ambiguity" (confidence policy), and "no **stronger** conflicting direct evidence" — "stronger" has no defined ordering for claim conflicts (the evidence tiers in 07 apply only to canonicalization).
**Interpretation.** Soundness for this validator means: no claim violating the policy passes. As written, the policy makes soundness unachievable by any deterministic component — semantic adequacy of a span to a statement is a judgment call. The plan will either silently weaken the check or silently overclaim the validator's guarantee.
**Recommendation.** Split the evidence policy into V-rules (validator-enforced, mechanically decidable, listed exhaustively per claim type) and G-rules (generator obligations, audited by the Phase 3b sampled claim audit). State that the validator is sound and complete **with respect to the V-rules only**. Define "no contradictory evidence" explicitly as closed over the pack's extracted evidence. This is a one-page spec and it makes the flagship guarantee true.

### 2. The ID scheme is the most load-bearing unspecified component
**Observation.** "All record identifiers are stable: rebuilding the same window in replay mode produces identical IDs" (Reproducibility) and "stable identifiers usable as IRIs" (Graph semantics). Nothing in the plan, schema draft, or `models.py` says how an ID is derived — content hash, of what canonical byte form, over which fields.
**Interpretation.** Replay identity, cross-run `REVISED_BY`, IRI export, and byte-identical packs all reduce to this function. If IDs incorporate wall-clock fields (`captured_at`), iteration order, or non-canonical serialization, every downstream guarantee falsifies.
**Recommendation.** Add "ID scheme specification" as a named Phase 2 deliverable: for each record type, the exact input fields, canonical encoding, and hash. Property-test it (Hypothesis): injectivity on distinct inputs, stability across runs, independence from field ordering.

### 3. Determinism is asserted but not specified or tested
**Observation.** Phase 2 exit requires "rebuilding twice produces identical artifact IDs and identical manifest counts"; Phase 3a requires identical claim sets. Good — these are falsifiable. But there is no canonical serialization spec and no CI determinism test. `EvidencePack` holds ordered tuples; nothing fixes the order.
**Interpretation.** Classic leaks that would falsify pack = f(snapshots, code): set iteration under `PYTHONHASHSEED`, `os.listdir`/glob ordering, JSON key order and float formatting, unicode normalization of excerpts (NFC vs NFD), timezone handling in datetime serialization, `captured_at` populated from `now()` during replay instead of from snapshots, locale-dependent sorting, any future parallelism, and git's own nondeterminism (rename-detection thresholds).
**Recommendation.** Write a one-page canonical pack serialization spec: UTF-8, NFC-normalized text, sorted keys, RFC3339 UTC timestamps, no floats (or fixed formatting), all record arrays sorted by ID, LF newlines. CI test: build the fixture window twice with different `PYTHONHASHSEED`, byte-compare the packs (manifests compared modulo timestamps). Strengthen exit criteria from "identical IDs" to "byte-identical packs" — it subsumes them and costs one `cmp`.

### 4. Pack referential integrity is unstated; the models permit dangling references
**Observation.** `models.py` carries string ID references with no cross-checks. Nothing states that a claim cannot cite evidence from another window.
**Interpretation.** A well-formed pack must satisfy at least: every `Claim.evidence_ids` and `warrant_ids` resolves in-pack; `Warrant.claim_id` back-references a claim that lists that warrant (bidirectional consistency — currently a warrant can point at claim A while claim B lists it); `Evidence.artifact_record_id` resolves; `Warrant.supporting_artifact_ids` and `counterevidence_ids` resolve; `SubjectRef.subject_id` resolves for typed subjects; `Contradiction`/`Abstention.evidence_ids` resolve; and window consistency — `claim.window_id == pack.window.window_id == evidence.window_id` for all cited evidence, with cited artifacts' `window_ids` containing the window. None is enforced anywhere.
**Recommendation.** Name a **pack integrity checker** as a Phase 3a deliverable: a pure function over `EvidencePack` enforcing the list above, run at the assemble stage and exposed as `codelore check-pack`. It is small, pure, and property-testable — ideal kernel material. Acceptance Test 2 (traceability) then has a mechanical precondition instead of relying on reviewer sampling alone.

### 5. The conservation law is bookkeeping, not an invariant — and naively stated it is ill-typed
**Observation.** The manifest records per-stage input/output/dropped counts; no document states input = output + dropped, and "nothing is dropped silently" is asserted, not checked.
**Interpretation.** Count equality does not even hold for fan-out/fan-in stages (extract yields many evidence records per artifact; reason consumes many evidence per claim). The correct invariant is accountability: every input record is either referenced by ≥1 output record or enumerated (not merely counted) in the drop list, with a reason code.
**Recommendation.** State the accountability invariant per stage, enforce it as a runtime assertion at each stage boundary, and have the integrity checker verify it end-to-end from the manifest plus intermediates. "Nothing dropped silently" then becomes a theorem, not a promise.

### 6. Defeasibility has no defined re-evaluation semantics
**Observation.** Claims are "defeasible (open to revision when counterevidence appears)" (why ladder); the schema has `Claim REVISED_BY Claim`; `models.py` has no revision fields and the plan defines no procedure for evidence arrival.
**Interpretation.** You do not need defeasible logic or Dung-style argumentation frameworks now. MVP rules are non-recursive (claims never premise claims), so status is a well-defined function of the pack's evidence state, computable by full re-derivation. The gap is that this rule is nowhere written, so packs silently go stale.
**Recommendation.** Document: "Packs are derived views. New evidence means a new run; status is recomputed, never mutated in place. `REVISED_BY` relates claims across runs/windows and is deferred until cross-window work (Phase 8)." Add a guard: if any future rule admits claims as premises, revisit — that is where stratification and real argumentation machinery become necessary.

### 7. The open-world/closed-corpus boundary is unstated for `ask`
**Observation.** The plan commits to open-world semantics ("absence of evidence within a window means unknown, never false"), yet `codelore ask` answering "what changed in this window" enumerates — implicitly closing the world over the corpus.
**Recommendation.** State the closure boundary: "Answers are complete relative to the ingested corpus recorded in the run manifest, and silent about the world beyond it — closed over corpus, open over world." Have every `ask` answer carry that corpus-scope line. Also note the narrow-inference "no contradictory evidence" check is closed over extracted evidence, hence only as strong as extraction.

## What Is Strong
- Exit criteria are genuinely falsifiable (replay identity, zero-model-call 3a, golden-set audits) — a real improvement most plans never make.
- The deterministic-spine / flexible-generation split, snapshot-based replay, and validator-behind-every-generator architecture are exactly the right decomposition for assurance.
- The effort allocation broadly matches the kernel/non-kernel split: deterministic claims first, model-derived content gated and audited, graph engine gated on retrieval value. Extractors and renderers correctly get conventional testing plus sampled audit.
- Ontology admission discipline and the canonicalization policy's explicit outcome lattice are unusually careful.

## What Is Weak or Risky
- The high-assurance kernel — ID scheme, validator V-rules, integrity checker, conservation checker, canonical serialization — exists only implicitly. Name each as a deliverable; together they are perhaps 500 lines and carry every guarantee.
- Free wins unclaimed: Phase 8 frames OWL export as documentation, not as enabling mechanical consistency checking by existing reasoners (unsatisfiable classes, domain/range violations) — claim it. The Testing policy never mentions property-based testing; Hypothesis on the validator, ID scheme, and serialization round-trip is cheap and high-value. A published JSON Schema for the pack would let third parties verify integrity independently.

## Open Questions
- What are the ID scheme's inputs, exactly — and is `captured_at` excluded from them during replay?
- Is a validator rejection distinguishable from a policy-judgment abstention in the manifest (V-rule failure vs G-rule audit finding)?
- When two runs over the same snapshots but different code versions produce packs, which is authoritative — is code version part of pack identity?
- Does `counterevidence_ids` reference `Evidence` or `ArtifactRecord`? The models leave it ambiguous; the integrity checker needs an answer.