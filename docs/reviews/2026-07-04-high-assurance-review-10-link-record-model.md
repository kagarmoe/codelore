---
title: High-Assurance Review — LinkRecord Model
date: 2026-07-04
reviewer-lens: invariants, decidability, replay guarantees, and validation kernel
artifact: docs/architecture/10-link-record-model.md
status: amendments applied
tags:
  - codelore
  - review
  - high-assurance
  - link-record
---

# High-Assurance Review — `docs/architecture/10-link-record-model.md`

Lens: High-Assurance Reviewer (Cook). Functional focus: checkable guarantees,
decidability, and the minimal validation kernel.

## Top Findings

### 1. Several guarantees need named checks

Observation: The doc says link records are mechanically checkable, validated,
and replay-stable.

Interpretation: These are good goals, but each needs a named check.

Recommendation: Define checks:

- `unique_link_ids`
- `resolved_link_endpoints`
- `legal_relation_contract`
- `no_volatile_link_fields`
- `canonical_link_order`
- `link_id_recomputes`

### 2. ID stability depends on the ID input-field spec

Observation: The doc says `link_id` is stable but does not name the exact input
fields.

Interpretation: Stability is not a property of the field. It is a property of
the ID function.

Recommendation: Link directly to the ID/serialization spec once created, and
state that `link_id` is recomputed from fixed fields in tests.

### 3. Legal relation combinations must be a table, not prose

Observation: Validation rules mention legal relation and membership type
combinations.

Interpretation: Without a table, the validator has no source of truth.

Recommendation: Add a normative Phase 2 relation contract table.

### 4. Empty `evidence_ids` needs an invariant or a reason

Observation: `evidence_ids` defaults to empty.

Interpretation: For Phase 2 structural links, empty evidence may be acceptable
if the supporting source is the deterministic acquire/window stage and manifest.
But that needs a rule. Otherwise the field trains the system to accept
unsupported links.

Recommendation: Add `support_basis`: either `evidence_ids` non-empty, or the
link is structural and supported by named manifest/acquire-stage inputs.

## What Is Strong

- Validation is clearly pack-side.
- Invalid links fail assembly.
- Run-scoped volatility is excluded from records.
- Relation admission requires validation rules.

## What Is Weak Or Risky

- "Mechanically checkable" is not yet a decision procedure.
- The minimal model lacks endpoint kind unless derived from IDs.
- `inferred` is listed before inference rules exist.

## Concrete Recommendations

1. Add named invariants and make them pack-integrity checker requirements.
2. Add a relation contract table.
3. Mark `inferred` as not emitted in Phase 2.
4. Add a support-basis invariant for empty `evidence_ids`.

## Open Questions

1. Should `link_id` include `window_id` for all relation types, or only
   window-scoped links?
2. Can two links with the same source, relation, and target differ by method or
   evidence, and if so are they one link or two?
