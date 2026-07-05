---
title: General Adversarial Review — CodeLore Development Plan 00b
date: 2026-07-04
reviewer-lens: general adversarial (refutation of central bets)
artifact: docs/plans/00b-development-plan-evidence-first.md
status: amendments applied
tags:
  - codelore
  - review
  - adversarial
  - plan
---

# Adversarial Review: `00b-development-plan-evidence-first.md`

Grounding checks performed: all cited founding docs read; `models.py` read; gastown corpus probed directly (`git ls-remote`, window stats). Corpus facts used below are observations, not hypotheses.

## 1. Top Findings (by severity)

### F1. The acceptance spine is not falsifiable, despite the plan claiming it is
**What:** The Status section claims the revision "makes phase exit criteria falsifiable where the original's were not." Three load-bearing criteria fail that test. Phase 4: "all five acceptance tests pass, **or failures are documented with causes**" — tautologically satisfiable by any outcome. Phase 3b: "a sampled claim audit … **passes** with the error rate recorded" — no threshold defines "passes"; recording any error rate satisfies it. Phase 4: "better-than-changelog utility is demonstrated" — no judge, rubric, or baseline procedure; the sole developer self-grades.
**Why it matters:** The entire resequencing bet is "prove claim quality before paying for graph infrastructure." Claim quality is never given a numeric bar anywhere in the plan, so the central bet's gate condition is unmeasurable.
**Recommendation:** Set explicit thresholds at Phase 3b (e.g., sampled claim error rate ≤ X% on N ≥ 30 claims) and define the Test 4 comparison protocol (questions fixed in the golden set, changelog-only answer written first, blind-ish comparison).

### F2. Phase 5's exit criterion requires a baseline no phase produces
**What:** Phase 5 exit: "the overclaiming rate does not rise above the **Phase 4 baseline**." Phase 4's deliverables include no overclaiming measurement; overclaiming is first measured in Phase 7 ("measure overclaiming … against the acceptance criteria"). The nearest candidate, 3b's sampled audit, measures claim error, not answer-level overclaiming, and is unthresholded (F1).
**Why it matters:** This is a gate depending on data a later phase produces — exactly the circularity class the plan's audit-everything stance should preclude.
**Recommendation:** Move a defined overclaiming metric (definition + sampling procedure) into Phase 4 deliverables, or re-anchor Phase 5's criterion to the 3b audit with a threshold.

### F3. Cross-window promises have no carrier; the Phase 6 gate is quasi-rigged toward "defer"
**What:** Phase 6's gate names cross-window lineage as "the expected strongest candidates" for graph value and requires a second built window. But the semantics those questions need (`POSSIBLY_SAME_AS`, `FOLLOWS`, lineage edges, cross-window canonicalization beyond a second pack's existence) are Phase 8 deliverables. `EvidencePack` (`models.py`) is single-window; no phase defines a multi-window assembly, store, or query surface over multiple packs. Phase 8 then promises module/symbol/concept lineage views, but no phase 2–7 builds `SymbolObservation` or `ConceptObservation` extraction, and schema draft §7 explicitly defers canonical `Concept`.
**Why it matters:** Either Phase 6's comparison tests only single-window questions (where pack filtering predictably wins, making the memo theater), or Phase 8 work must be smuggled forward. And if Phase 6 ends in "defer," Phase 8's lineage exit criterion ("a module's change history renders across at least two real windows") has no defined substrate.
**Recommendation:** Define a minimal multi-window container/index as a named deliverable (Phase 6 or 8 entry), and strike "concept lineage" from Phase 8 or price its extraction explicitly.

### F4. "The pack is the source of truth" does not survive schema evolution
**What:** Packs are stored JSON validated by pydantic models with `frozen=True, extra="forbid"`; `EvidencePack` has no schema-version field; migration is never mentioned. Phase 8 (formal exports, cross-window views) must read packs built by earlier code versions.
**Why it matters:** `extra="forbid"` makes old packs fail validation the moment a required field is added. The run manifest records code version but nothing says packs are versioned, migrated, or rebuilt. "Replayable from snapshots" partially mitigates (rebuild instead of migrate) — but rebuild-on-every-schema-change is a cost the plan never prices, and model-call re-extraction is declared an "explicit, logged choice."
**Recommendation:** Add a `pack_schema_version` field now and state the policy: migrate, or rebuild-from-snapshots, per schema change.

### F5. Phase 4 is the overloaded phase, and it contains an internal contradiction
**What:** Phase 4 gates Phases 5, 6, and effectively 7, yet carries ~7 deliverables: `ask`, rung labeling, dossier, rendered navigable relationship views, generated ontology reference, per-window glossary, timeline view, plus the acceptance run. Rendering format/tooling is unspecified and unpriced. Contradiction: the Verifiability policy says "per-window glossary definitions **may use a model**," while Phase 4's exit requires the window glossary to "regenerate **deterministically** from the models and the pack." The Reproducibility policy snapshots only "model **extraction** outputs," not presentation-stage model calls, so replay does not obviously rescue this.
**Why it matters:** The critical-path phase is the fattest, and its exit criterion cannot be satisfied as written if a model generates glossary definitions.
**Recommendation:** Either extend snapshotting to presentation-stage model calls and define "deterministic" as "deterministic under replay," or make window-glossary definitions extractive-only. Consider splitting Phase 4 (4a: ask/export/acceptance; 4b: rendered views, glossaries, timeline).

### F6. "Deterministic validation" guarantees less than the bet's rhetoric implies
**What (interpretation):** The validator checks span existence, quote match, and minimum-support counts — all mechanical. But minimum support for `explicit_problem`/`explicit_decision` is "clearly states the problem/decision" (evidence policy), a semantic judgment. A model generator can cite a real, matching, irrelevant span; the validator passes it. The only semantic backstop is the unthresholded sampled audit (F1).
**Why it matters:** Bet 2 prevents fabricated quotes, not wrong claims. "Claim quality proven" rests on the audit, which is the plan's weakest instrument.
**Recommendation:** State this limit explicitly in the Verifiability policy and make the sampled audit's size, sampling rule, and threshold the real gate.

### F7. Evaluator independence and unpriced audit labor (corpus-grounded)
**What (observation):** The window is real but large: v1.2.0 exists on `gastownhall/gastown`; the window holds **358 commits, 44 merges, ~70 commits referencing #NNN**, spanning ~3 months. The local clone's `origin` still points at `steveyegge/gastown` (redirects; plan's repoint step is correct). The repo also carries curated release-evidence docs (`docs/release/gt-1.2-release-evidence.md`), so the "better than changelog" baseline is stronger than "CHANGELOG.md alone."
**Why it matters:** Hand-verifying golden questions, sampled audits at 3b/4/5, and Test 2 reviewer navigation over a 358-commit window is substantial unpriced labor — performed by the same person who built the generators. Self-review invalidates Tests 2–4 as evidence for outside audiences (the Phase 7 portfolio claim).
**Recommendation:** Fix sample sizes now; budget the audit hours; get at least one external reviewer for the Phase 4 acceptance memo. Also: Test 4 should name the in-repo release-evidence docs as part of the baseline, or the comparison flatters CodeLore.

### F8. No rework loop after a failed acceptance
**What:** Phase 6 requires "Phase 4 acceptance passed"; Phase 4 permits exit via documented failure; Phase 5 explicitly tolerates abstention-shaped failure but not "structural failures," which "must be fixed in Phase 4." No phase or task budget exists for that fix loop, and Phase 5 may change claim sets after acceptance without a scheduled re-run of the acceptance tests before Phase 6's comparison.
**Recommendation:** Add an explicit "Phase 4 remediation loop" and require acceptance re-run after Phase 5 before the Phase 6 memo.

## 2. What Is Strong
- The resequencing itself is well-motivated: it operationalizes acceptance failure condition 4 (graph effort dominating before claim quality). Genuine improvement over `00`.
- Corpus audit and golden question set as Phase 2 *entry* tasks — disconfirmation baseline before extractor code — is excellent discipline, and my corpus probe confirms the audit would have caught the stale clone (local tags stop at v1.1.0).
- The 3a/3b split cleanly isolates model risk; "zero model calls; running twice yields identical claim sets" is genuinely falsifiable, as are Phase 2's ID/checksum criteria and the no-release-typed-inputs check.
- Scheduling forge ingestion fixes a real hole in `00` (required at acceptance, never scheduled).
- Semantics-vs-infrastructure separation is the plan's best conceptual move and honestly handles the tension with the product definition's "required MVP graph capabilities."
- Snapshot/replay, manifests, and materialized intermediates are coherent and mutually reinforcing.

## 3. What Is Weak or Risky
- The falsifiability claim in the Status section oversells (F1, F2).
- Phase 4 and Phase 8 are both overloaded; Phase 8 bundles four workstreams (window types, lineage viz, SKOS/OWL/RDF, llama.cpp) and inherits unbuilt inputs (F3, F5).
- Unpriced: GitHub API auth/rate limits and snapshot infra for ~44 PRs + issues + comments; rendering implementation; SKOS/OWL/RDF mapping labor; audit hours; remediation loops.
- Rung 3 representation is hand-waved ("existing claim status machinery"): `ClaimStatus.INSUFFICIENT` conflates below-threshold candidates with degraded claims, and no `ClaimType` or warrant exists for a candidate-why (hypothesis: this surfaces as a schema fight in Phase 5).
- Product definition §3's "required MVP graph capabilities" remains authoritative while contradicting the gated-graph stance; only §8 is declared historical.

## 4. Open Questions
1. What error-rate threshold makes the 3b audit and Phase 4 acceptance "pass," and who besides the author judges Tests 2 and 4?
2. If Phase 4 exits with documented failures, is Phase 6 blocked permanently, and where is the remediation loop scheduled?
3. What structure holds cross-window state if Phase 6 defers the graph — a multi-pack index, or nothing until Phase 8?
4. Are presentation-stage model calls (dossier, glossary phrasing) snapshotted for replay, or exempt from reproducibility?
5. What is the pack versioning/migration policy given `extra="forbid"` models and long-lived stored packs?
6. Does Test 4's baseline include gastown's in-repo curated release-evidence docs, or only `CHANGELOG.md`?