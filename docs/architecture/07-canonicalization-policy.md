# CodeLore Formal Canonicalization Policy

## Purpose

This document defines how CodeLore decides when multiple window-scoped
observations refer to the same enduring identity.

Canonicalization is an evidence-backed identity-resolution process. It is not a
name-matching shortcut.

## Core Rule

A canonical identity is justified only when continuity of referent is stronger
than continuity of wording.

That means:

- same label is weak evidence
- explicit continuity is strong evidence
- structural lineage is strong evidence
- historical truth outranks graph neatness

Recurring terminology does not by itself imply recurring ontology.

## Canonicalization Outcomes

Every candidate cross-window identity decision should resolve to one of these:

### 1. `same_identity`

The observations refer to the same enduring entity with strong support.

### 2. `likely_same`

The observations probably refer to the same enduring entity, but some ambiguity
remains.

### 3. `uncertain`

There is meaningful evidence in both directions or not enough evidence either
way.

### 4. `likely_different`

The observations share some resemblance, but the evidence leans toward distinct
identities.

### 5. `different_identity`

The observations should remain distinct identities.

## Merge Policy

Create or attach to a canonical node only when:

- the outcome is `same_identity`, or
- the outcome is `likely_same` and the merge materially improves historical
  reasoning with low distortion risk

When the outcome is `uncertain`:

- keep separate observations
- preserve a tentative relationship

When the outcome is `likely_different` or `different_identity`:

- keep distinct identities

## Evidence Tiers

### Tier 1. Explicit continuity

Strongest evidence.

Examples:

- rename commit
- PR stating “restore X”
- PR stating “replace old X with new X”
- ADR or release note explicitly linking old and new
- comment or code note explicitly naming continuity

### Tier 2. Structural continuity

Strong evidence.

Examples:

- same file lineage through rename or move history
- same symbol lineage across refactors
- stable dependency neighborhood
- stable call graph neighborhood
- stable workflow role across windows

### Tier 3. Behavioral continuity

Moderate evidence.

Examples:

- same functional role
- same tests continue to exercise it
- same category of behavior preserved through change

### Tier 4. Lexical continuity

Weak evidence.

Examples:

- same name
- similar wording
- similar issue titles

Lexical continuity is never sufficient by itself.

## Counterevidence

Counterevidence can block or downgrade canonicalization.

Examples:

- same name with clearly different role
- same path but rewritten into a different architectural function
- explicit replacement rather than continuation
- same concept label but incompatible surrounding relationships
- same problem wording but different subsystem and different operative cause

## Decision Standard

Canonicalization should satisfy all of the following:

1. Positive continuity evidence exists.
2. No stronger counterevidence dominates it.
3. The merge improves historical reasoning.
4. The merge does not erase a meaningful historical break.

If condition 4 fails, do not merge.

## Entity-Type Policies

### `Project`

Canonical by default.

### `Module`

Often suitable for canonicalization.

Strong signals:

- path lineage
- rename history
- stable role in architecture
- explicit restoration or continuation language

### `Symbol`

Often suitable when lineage is strong.

Strong signals:

- rename lineage
- stable signature or semantic role
- stable neighborhood of callers/callees

### `Concept`

Canonicalize cautiously.

Required:

- continuity of role, not just wording
- stable relation to neighboring concepts or artifacts
- preferably explicit conceptual continuity

### `ProblemClass`

Canonicalize only when recurrence is about the same enduring class of problem,
not merely a similar symptom.

Required:

- repeated evidence of the same underlying concern
- continuity of system context or explicit recurrence linkage

### `DecisionTheme`

Canonicalize as a recurring theme, not as every individual decision.

Use canonical `DecisionTheme` plus per-window `DecisionObservation`.

## Evaluation Questions

For every candidate canonicalization, ask:

1. If I removed the label, would I still believe these observations refer to the
   same thing?
2. Is there lineage evidence rather than only naming similarity?
3. Would a historian of the project treat these as one evolving referent?
4. Would merging these observations hide a meaningful break?

If question 4 is yes, keep them separate.

## Formal Resolution Procedure

### Step 1. Build window-scoped observations

Create observations before any canonical merge attempt.

Examples:

- `ModuleObservation`
- `SymbolObservation`
- `ProblemObservation`
- `DecisionObservation`
- `ConceptObservation`

### Step 2. Gather continuity evidence

Collect:

- explicit references
- structural lineage
- behavioral continuity
- lexical continuity
- counterevidence

### Step 3. Score the candidate

Recommended scoring dimensions:

- `explicit_score`
- `structural_score`
- `behavioral_score`
- `lexical_score`
- `counterevidence_score`

The exact numeric weights can evolve later. The important rule is that lexical
score should never dominate explicit or structural evidence.

### Step 4. Resolve outcome

Map the evidence state to one of:

- `same_identity`
- `likely_same`
- `uncertain`
- `likely_different`
- `different_identity`

### Step 5. Write the relationship explicitly

Possible edge patterns:

- `OBSERVES`
- `FOLLOWS`
- `EVOLVES_TO`
- `SUPERSEDES`
- `REVISITS`
- `POSSIBLY_SAME_AS`
- `REUSES_LABEL`

### Step 6. Preserve provenance

Every canonicalization decision should preserve:

- source observations
- evidence used
- method
- confidence
- timestamp

## Special Cases

### Appears, disappears, reappears

A reappearance should not be auto-merged by name.

Preferred treatment:

- compare old and new observations using explicit and structural evidence
- preserve uncertainty when continuity is ambiguous
- use `POSSIBLY_SAME_AS` when needed

### Same name, different meaning

Treat as distinct unless continuity of referent is evidenced.

Possible relation:

- `REUSES_LABEL`

### Split identity

If one old entity becomes multiple later entities:

- preserve the old canonical node
- link later observations through successor-style edges

### Merged identity

If multiple earlier entities collapse into one later entity:

- preserve earlier distinct identities
- link later observation with derivation or supersession edges

## Claims About Canonicalization

Canonicalization itself should be treated as a claim-like analytical act with:

- evidence
- warrant
- confidence
- the possibility of contradiction later

This means identity resolution can be revised as the graph grows.

## What Canonicalization Is For

Canonicalization should help CodeLore answer:

- how the same thing changed over time
- when a problem recurred
- when a decision theme persisted or was replaced
- when a concept evolved versus when a label was reused

It should not be used merely to reduce node count or make the graph look neat.

## Summary Rule

Create canonical nodes only from repeated observations with enough explicit or
structural continuity to justify an enduring identity, and keep uncertain
continuity visible instead of forcing a merge.
