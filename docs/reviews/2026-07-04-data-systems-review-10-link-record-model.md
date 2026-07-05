---
title: Data Systems Review — LinkRecord Model
date: 2026-07-04
reviewer-lens: data systems, source-of-truth design, projections, and scale
artifact: docs/architecture/10-link-record-model.md
status: amendments applied
tags:
  - codelore
  - review
  - data-systems
  - link-record
---

# Data Systems Review — `docs/architecture/10-link-record-model.md`

Lens: Data Systems Reviewer (Kleppmann). Functional focus: source of truth,
projection costs, schema evolution, and query workload fit.

## Top Findings

### 1. The pack-first relation model is the right dependency direction

Observation: `LinkRecord` is authoritative in `links.jsonl`; Neo4j and RDF are
derived projections.

Interpretation: This is sound. It makes graph rebuilds, RDF export changes,
and query-tier experiments cheap.

Recommendation: Preserve this dependency direction in code. No graph loader
should synthesize relationships that are absent from `links.jsonl`.

### 2. The no-run-scoped-fields rule is correct but should be repeated in the
model section

Observation: The doc says run provenance belongs in `manifest.json`; Phase 2
plan says the same.

Interpretation: Good. This is necessary for byte-identical replay. It is
important enough to be part of the model contract, not only temporal semantics.

Recommendation: Add a "Volatile Field Policy" subsection.

### 3. Evidence citation for structural git results is underspecified

Observation: The open decision asks how to cite evidence when the evidence is a
git command result rather than a materialized `Evidence` record.

Interpretation: This is load-bearing. Phase 2 may not yet have `Evidence`
records, but links still need auditability. The manifest or acquire-stage
snapshot must be citeable.

Recommendation: Define a Phase 2 citation target: either manifest acquisition
record IDs or raw snapshot IDs. Do not leave structural links with empty
support forever.

### 4. Relation-type expansion will be the scale wall if not governed

Observation: Relation admission criteria exist.

Interpretation: Good, but they need ownership. Without a registry, relation
types will proliferate as soon as PRs/issues enter.

Recommendation: Add a relation registry section or table in this doc.

## What Is Strong

- Clear rebuildable projection story.
- Minimal Phase 2 scope.
- Consistent with JSONL pack architecture.
- Good separation between record data and manifest provenance.

## What Is Weak Or Risky

- No relation contract table yet.
- No Phase 2 citation mechanism for structural support.
- Projection mapping is described conceptually but not yet testable.

## Concrete Recommendations

1. Add a Phase 2 relation table.
2. Add volatile field policy.
3. Add a temporary Phase 2 support mechanism for structural git links.
4. Later, add projection conformance tests: pack link -> Neo4j edge/RDF reifier.

## Open Questions

1. Should `links.jsonl` be independently queryable without loading artifacts?
2. Should relation records carry enough endpoint display hints for debugging, or
   should all display resolve through artifact records?
