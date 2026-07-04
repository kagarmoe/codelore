# CodeLore MVP Claim Taxonomy And Warrant Model

## Purpose

This document defines the minimum claim system for the first CodeLore slice.

The MVP needs a small taxonomy that is:

- useful
- defensible
- easy to evaluate
- hard to misuse

## Design Goals

1. Keep claim classes narrow.
2. Prefer explicit over inferred claims.
3. Make structural relations first-class.
4. Separate claim content from supporting evidence.
5. Make abstention easy.

## Claim Object

Each claim should have, at minimum:

- `claim_id`
- `window_id`
- `claim_type`
- `statement`
- `subject_refs`
- `evidence_ids`
- `warrant_ids`
- `confidence`
- `status`

### Status

Allowed MVP statuses:

- `supported`
- `contested`
- `insufficient`
- `abstained`

## Minimum Claim Types

### 1. `change_fact`

Definition:
What changed within the window.

Examples:

- command X gained a new flag
- file Y was removed
- release Z includes fix W

Evidence base:

- diffs
- commits
- release notes
- PR descriptions

### 2. `artifact_link`

Definition:
Two or more artifacts are structurally related.

Examples:

- PR X merged commit Y
- issue A is referenced by PR B
- release Z contains commit C

Evidence base:

- git ancestry
- merge metadata
- explicit references

### 3. `explicit_problem`

Definition:
An artifact explicitly states the problem being addressed.

Examples:

- issue says scheduler attempts work on closed beads
- PR says daemon crash-loop handling is broken under rate limits

Evidence base:

- issue bodies
- PR bodies
- release notes
- commit messages

### 4. `explicit_decision`

Definition:
An artifact explicitly states a decision, tradeoff, or constraint.

Examples:

- PR discussion says Windows tests were replaced with smoke tests for speed
- commit or ADR states a guard was added for safety over convenience

Evidence base:

- PR discussion
- ADR text
- commit message
- docs with direct rationale

### 5. `narrow_inference`

Definition:
A limited inferred claim allowed only under a typed rule.

Examples:

- test change in same PR plus targeted code change suggests intended behavior
  guard

Evidence base:

- two or more corroborating artifact types
- explicit typed warrant rule

This should be rare in MVP.

## Later Claim Types

- broad concept evolution
- architectural worldview claims
- author-intent narratives
- root-cause diagnosis unless directly evidenced
- tradeoff inference from code shape alone

## Warrant Object

Each warrant should have:

- `warrant_id`
- `warrant_type`
- `claim_id`
- `rule_name`
- `rule_text`
- `supporting_artifact_ids`
- `counterevidence_ids`
- `limitations`

## Warrant Types

### `explicit_statement`

Use when the claim is directly stated in an artifact.

### `structural_membership`

Use when the claim follows from a verifiable structural relation such as commit
membership in a tag range or PR merge association.

### `cross_artifact_corroboration`

Use when multiple artifacts support the same claim from different angles.

### `behavior_guard_inference`

Use only for narrow inference where tests and code changes jointly support a
behavioral interpretation.

## Artifact Classes Relevant To MVP

- `release`
- `tag`
- `commit`
- `diff`
- `pull_request`
- `issue`
- `comment`
- `release_note`
- `doc_change`
- `test_change`

GitHub artifacts are enrichments, not mandatory foundations.

## Subject References

Claims should point at typed subjects first, with raw text used as supporting
context where needed.

Initial subject categories:

- `window`
- `artifact`
- `file`
- `module`
- `test`
- `release`

Avoid symbol-level claims in the first slice unless the extraction is already
strong enough to do them reliably.

## Claim Generation Order

Recommended order:

1. Generate structural `artifact_link` claims.
2. Generate `change_fact` claims from diffs and release artifacts.
3. Generate `explicit_problem` claims.
4. Generate `explicit_decision` claims.
5. Generate `narrow_inference` claims only after all direct evidence has been
   processed.

This ordering reduces the temptation to fill gaps with inference too early.

## Query Utility Goal

This minimum taxonomy should be enough to support questions like:

- What changed in this release?
- Which PRs and commits support that?
- Which problems were explicitly stated?
- Which decisions were explicitly recorded?
- Which parts are evidenced versus unresolved?

This taxonomy is intentionally sized for the first slice. It supports bounded
historical questions before broader product-why reasoning is introduced.
