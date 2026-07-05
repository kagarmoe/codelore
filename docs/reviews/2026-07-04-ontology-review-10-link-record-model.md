---
title: Ontology Review — LinkRecord Model
date: 2026-07-04
reviewer-lens: ontology commitments and relation admission discipline
artifact: docs/architecture/10-link-record-model.md
status: amendments applied
tags:
  - codelore
  - review
  - ontology
  - link-record
---

# Ontology Review — `docs/architecture/10-link-record-model.md`

Lens: Ontology Reviewer (Quine) plus Ontology Reviewer (Peirce). Functional
focus: category admission, relation naming, and artifact-to-meaning discipline.

## Top Findings

### 1. `LinkRecord` is earned

Observation: The doc states relationships must not be hidden in claims,
embedded ID lists, or graph-database edges.

Interpretation: This is a justified category. It has distinct construction
rules, query value, and failure modes. It prevents the pack from being node-rich
and edge-poor.

Recommendation: Keep `LinkRecord` as a first-class record.

### 2. `LinkRecord` still risks becoming the generic "edge thing"

Observation: The summary says if a relationship matters to claims, warrants,
graph projection, or RDF export, it should be a `LinkRecord`.

Interpretation: That is directionally correct, but broad. Some relationships
are interpretive claims, not structural links. If everything relationship-shaped
becomes a link, `LinkRecord` becomes an ontology vacuum.

Recommendation: Add a boundary: Phase 2 `LinkRecord`s are structural or
membership records. Interpretive relationships require a claim and warrant
before they become links, unless admitted by a later relation rule.

### 3. Relation names should not imply more than construction rules prove

Observation: `native_to_window`, `linked_to_window`, `parent_of`, and
`includes_diff` are relatively safe. Candidate `touches_file` is deferred.

Interpretation: Good. `touches_file` can mean name-status, hunk content,
semantic symbol usage, or filesystem path membership. Deferring it avoids false
precision.

Recommendation: Keep relation names close to the extraction mechanism until
later phases justify richer semantics.

### 4. Membership is not identity, and the doc preserves that

Observation: The doc says membership is relational, not identity-defining.

Interpretation: This is essential. A commit can belong to multiple windows or
views without becoming a different commit.

Recommendation: Preserve this line in implementation tests: artifact identity
must not include window ID.

## What Is Strong

- The Claim/Evidence/Warrant framing is clearer than ontology jargon.
- The relation admission criteria are appropriate.
- The doc avoids making RDF or Neo4j source-of-truth artifacts.

## What Is Weak Or Risky

- `LinkRecord` as "structured support" may blur evidence and relation unless
  examples stay concrete.
- `inferred` membership is dangerous before Phase 3 because inference rules are
  not yet admitted.

## Concrete Recommendations

1. Add a scope boundary: Phase 2 links are deterministic structural/membership
   links only.
2. Mark `inferred` as enum-reserved but not emitted in Phase 2.
3. Keep candidate relation names out of implementation until construction rules
   exist.

## Open Questions

1. What relation types require warrants before emission?
2. Should `LinkRecord` ever represent interpretive relationships directly, or
   should those always be claims first?
