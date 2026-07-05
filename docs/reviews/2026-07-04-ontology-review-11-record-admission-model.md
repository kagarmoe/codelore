---
title: Ontology Review — Record Admission Model
date: 2026-07-04
reviewer-lens: ontology commitments, category admission, and artifact-to-meaning discipline
artifact: docs/architecture/11-record-admission-model.md
status: amendments applied
tags:
  - codelore
  - review
  - ontology
  - record-admission
---

# Ontology Review — `docs/architecture/11-record-admission-model.md`

Lens: Ontology Reviewer (Quine) plus Ontology Reviewer (Peirce). Functional
focus: category admission and the movement from artifact to interpretation.

## Top Findings

### 1. Record admission is an earned category

Observation: The doc defines a specific boundary where information becomes
durable CodeLore data.

Interpretation: This is not unnecessary abstraction. It prevents "we saw it" from
becoming "we know it."

Recommendation: Keep the concept.

### 2. Candidate datum should remain process state, not ontology

Observation: Candidate datum is a stage-local possible record.

Interpretation: Useful, but it should not become a first-class pack entity.
Otherwise CodeLore begins preserving every near-miss as ontology.

Recommendation: State that candidate data are process-state objects, not pack
ontology, unless represented as rejected candidates in the manifest.

### 3. The Claim/Evidence/Warrant sections are good cross-disciplinary language

Observation: The doc avoids "truth bearer" and uses claim/evidence/warrant.

Interpretation: Good. This language travels across ontology, data engineering,
and implementation.

Recommendation: Preserve it.

## What Is Strong

- The doc distinguishes source objects, support, propositions, and reasoning
  rules.
- It does not let failed claims pass through as weak claims.
- It explains why admission rules help review interoperability.

## What Is Weak Or Risky

- Rejected candidates could become a shadow ontology if preserved too richly.
- "Derived record" appears in the user's framing but not as a formal section in
  the doc.

## Concrete Recommendations

1. Add a boundary that candidate data are process state.
2. Add a short "Derived Records" section.
3. Keep rejected candidates in manifests unless they earn product-level status
   such as abstention.

## Open Questions

1. When does a rejected candidate become an abstention rather than only a
   manifest drop?
