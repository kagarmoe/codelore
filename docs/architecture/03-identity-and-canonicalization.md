---
title: Identity And Canonicalization
date: 2026-07-04
status: current
supersedes:
  - docs/architecture/archive/07-canonicalization-policy.md
---

# CodeLore Identity And Canonicalization

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

## Scope Model

CodeLore distinguishes:

- canonical identities
- window-scoped observations
- artifacts
- evidence
- claims
- warrants
- identity-resolution decisions

Observations are built before canonical merges.

Canonical nodes are thin. The historically meaningful content remains in
window-scoped observations and evidence.

## Canonicalization Outcomes

Every candidate identity decision resolves to one of:

- `same_identity`
- `likely_same`
- `uncertain`
- `likely_different`
- `different_identity`

Create or attach to a canonical node only when:

- outcome is `same_identity`, or
- outcome is `likely_same` and the merge materially improves reasoning with low
  distortion risk

When uncertain, preserve separate observations and an uncertainty relation.

## Evidence Tiers

### Tier 1. Explicit Continuity

Strongest evidence:

- rename commit
- PR stating "restore X"
- ADR or release note explicitly linking old and new
- code note explicitly naming continuity

### Tier 2. Structural Continuity

Strong evidence:

- file lineage through rename or move history
- symbol lineage across refactors
- stable dependency neighborhood
- stable workflow role

### Tier 3. Behavioral Continuity

Moderate evidence:

- same functional role
- same tests continue to exercise it
- same category of behavior preserved through change

### Tier 4. Lexical Continuity

Weak evidence:

- same name
- similar wording
- similar issue titles

Lexical continuity is never sufficient by itself.

## Counterevidence

Counterevidence can block or downgrade canonicalization:

- same name with clearly different role
- same path rewritten into a different architectural function
- explicit replacement rather than continuation
- same concept label with incompatible neighboring relationships
- similar problem wording in a different subsystem with a different cause

## Decision Standard

Canonicalization should satisfy:

1. Positive continuity evidence exists.
2. No stronger counterevidence dominates it.
3. The merge improves historical reasoning.
4. The merge does not erase a meaningful historical break.

If condition 4 fails, do not merge.

## Entity-Type Policy

### Project

Canonical by default.

### Module

Often suitable for canonicalization when path lineage, rename history, or
stable architectural role is present.

### Symbol

Often suitable when rename lineage, stable signature, semantic role, or
caller/callee neighborhood supports continuity.

### Concept

Canonicalize cautiously. Require continuity of role, not just wording.

### ProblemClass

Canonicalize only when recurrence concerns the same enduring class of problem,
not merely similar symptoms.

### DecisionTheme

Canonicalize as a recurring theme, not as every individual decision.

## Procedure

1. Build window-scoped observations.
2. Gather explicit, structural, behavioral, lexical, and counterevidence.
3. Score or summarize evidence by tier.
4. Resolve to one of the canonicalization outcomes.
5. Write the relationship explicitly.
6. Preserve provenance, evidence, method, confidence, timestamp, and
   limitations.

Canonicalization itself is claim-like: it has evidence, warrant, confidence,
and can be revised by later counterevidence.

## Special Cases

### Appears, Disappears, Reappears

Do not auto-merge by name. Compare old and new observations using explicit and
structural evidence. Use uncertainty when continuity is ambiguous.

### Same Name, Different Meaning

Keep distinct unless continuity of referent is evidenced. Use `REUSES_LABEL`
where useful.

### Split Identity

Preserve the old canonical node and link later observations through successor
style edges.

### Merged Identity

Preserve earlier distinct identities and link the later observation with
derivation or supersession edges.

## What Canonicalization Is For

Canonicalization helps CodeLore answer:

- how the same thing changed over time
- when a problem recurred
- when a decision theme persisted or was replaced
- when a concept evolved versus when a label was reused

It is not for reducing node count or making the graph look neat.

## MVP Scope

The MVP should limit canonicalization to the safest subset, likely module-level
identity where path lineage and explicit rename evidence are available.

Concept, problem-class, and decision-theme canonicalization remain deferred
until construction rules and query value are demonstrated.
