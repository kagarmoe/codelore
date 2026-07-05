---
title: Schema Review — LinkRecord Model
date: 2026-07-04
reviewer-lens: schema ambiguity, implementation contract, and evolvability
artifact: docs/architecture/10-link-record-model.md
status: amendments applied
tags:
  - codelore
  - review
  - schema
  - link-record
---

# Schema Review — `docs/architecture/10-link-record-model.md`

Lens: Schema Skeptic (Sadalage). Functional focus: implementation ambiguity,
schema drift, and contracts multiple implementers could read differently.

## Top Findings

### 1. `source_id` and `target_id` need endpoint typing

Observation: Phase 2 fields include `source_id` and `target_id`, but no
`source_kind` or `target_kind`.

Interpretation: ID prefixes may be enough for code, but they are an implicit
contract. The validator must know whether `native_to_window` expects
`window -> artifact`, `artifact -> window`, or both. Without explicit endpoint
typing or a typed-ID registry, relation validation becomes string parsing.

Recommendation: Add either `source_kind`/`target_kind` fields or a formal
record-ID prefix registry that the integrity checker uses. Do not leave endpoint
types implicit in prose.

### 2. Directionality is under-specified

Observation: Examples show `window --native_to_window--> commit`, but the Phase
2 implementation plan may be read by someone as source artifact to target
window.

Interpretation: Direction is semantic. If implementers reverse it, Neo4j,
RDF, and pack queries will disagree.

Recommendation: Add a direction table for every Phase 2 `RelationType`.

### 3. `membership_type` duplicates relation type for window membership

Observation: There are relation types `native_to_window` and
`linked_to_window`, plus `membership_type` values `native` and `linked`.

Interpretation: This is useful only if `membership_type` is a refinement that
can vary independently. For Phase 2, it appears redundant and therefore risks
inconsistent records such as relation `native_to_window` with membership
`linked`.

Recommendation: Either make the combination table explicit and reject illegal
pairs, or remove `membership_type` from Phase 2 and let the relation type carry
the distinction.

### 4. `confidence` optionality is right for structural links but vague for
heuristic/inferred links

Observation: `confidence` is optional, and link methods include `heuristic` and
`inferred`.

Interpretation: A structural link can be confidence-less or high by rule. A
heuristic/inferred link without confidence is under-specified.

Recommendation: Require `confidence` when `link_method` is `heuristic` or
`inferred`.

## What Is Strong

- The doc sharply separates `LinkRecord` from claims and warrants.
- It aligns with the pack-first source-of-truth design.
- It correctly treats Neo4j and RDF as projections.
- It keeps Phase 2 small.

## What Is Weak Or Risky

- Endpoint direction and kind are not yet machine-checkable.
- Relation type and membership type can drift unless constrained.
- The minimal model may be too minimal for validation unless ID prefix parsing
  is specified elsewhere.

## Concrete Recommendations

1. Add a Phase 2 relation contract table:
   `relation_type`, source kind, target kind, allowed `link_method`, allowed
   `membership_type`, whether `confidence` is required.
2. Decide whether endpoint kind is stored or derived from stable ID prefixes.
3. Add illegal-combination examples.

## Open Questions

1. Are relation directions intended to mirror natural language labels, RDF
   predicate direction, or ingestion convenience?
2. Should `native_to_window` be named `has_native_artifact` if the direction is
   `window -> artifact`?
