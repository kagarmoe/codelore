# CodeLore MVP Evidence Policy

## Purpose

This document defines the hard rules for what CodeLore may claim in the MVP and
how those claims must be supported.

The goal is to make CodeLore a disciplined evidence system whose outputs remain
traceable, bounded, and trustworthy.

## Core Rules

### Rule 1. Claims are downstream of evidence

Every claim should point to one or more source artifacts and a warrant that
explains why those artifacts support the claim.

### Rule 2. Support quality outranks fluency

A terse answer with strong support is better than a polished answer with weak
support.

### Rule 3. Missing evidence is a valid result

CodeLore must be allowed to say:

- no sufficient evidence found
- evidence is conflicting
- likely but unsupported
- this window explains what changed, but not why

### Rule 4. Explicit and inferred claims are not equivalent

Claims drawn directly from artifacts must be distinguished from claims inferred
from patterns across artifacts.

### Rule 5. Claims must preserve window context

Every claim must be attached to a specific `ChangeWindow`. Cross-window
comparisons may exist, but claims should never silently lose their temporal
context.

## Allowed Claim Classes In MVP

### Allowed

1. Explicit change claims
   Example: release notes or PR text explicitly state that a crash-loop fix was
   added.

2. Structural linkage claims
   Example: PR X merged commit Y; commit Y changed files A and B; release Z
   includes PR X.

3. Explicit problem claims
   Example: an issue or PR description names the problem being addressed.

4. Explicit decision claims
   Example: PR discussion, ADR, or commit message explicitly states a design
   choice or tradeoff.

5. Narrow inferred intent claims
   Only when the inference rule is typed, explicit, and high-confidence.
   Initial MVP should support at most one or two narrow inferred types.

### Deferred Claim Classes

1. Broad inferred architectural narratives
2. Psychological intent claims about authors
3. High-level product rationale unsupported by artifacts
4. Root-cause claims unless explicitly stated or very strongly evidenced
5. “Why” explanations synthesized solely from embeddings or generic summaries

## Minimum Support Requirements

### Explicit change claim

Minimum:

- one authoritative source artifact stating the change, and
- one confirming structural artifact where possible

Preferred artifact combinations:

- release note + commits/diff
- PR description + commits/diff
- changelog entry + tagged window diff

### Structural linkage claim

Minimum:

- direct system evidence of the relationship

Examples:

- merge metadata
- commit ancestry
- file diff membership
- tagged release membership

### Explicit problem claim

Minimum:

- issue text, PR text, release note, commit message, or ADR that clearly states
  the problem

### Explicit decision claim

Minimum:

- direct textual evidence of a decision, tradeoff, or constraint

### Narrow inferred intent claim

Minimum:

- at least two supporting artifacts of different types, and
- a typed inference rule, and
- no contradictory direct evidence

Example narrow rule:

- test added or updated in the same PR as a behavior-changing code diff may
  support the claim that the change was intended to guard a specific behavior

## Warrant Requirements

A warrant explains why the cited evidence supports the claim.

Each warrant in MVP must contain:

- `warrant_type`
- `rule_text`
- `supporting_artifact_ids`
- `limitations`

### Suggested warrant types

- `explicit_statement`
- `structural_membership`
- `cross_artifact_corroboration`
- `behavior_guard_inference`
- `release_inclusion`

## Confidence Policy

Confidence must reflect evidence quality, not model confidence.

Allowed MVP levels:

- `high`
- `medium`
- `low`

### High

- direct explicit statement, or
- direct structural relationship with no ambiguity

### Medium

- multiple corroborating artifacts, but some ambiguity remains

### Low

- weakly supported inference that is still allowed by MVP rules

Low-confidence claims should be rare in MVP. If many claims end up `low`, the
system should abstain more aggressively.

## Contradiction Handling

When evidence conflicts, CodeLore should preserve the conflict as part of the
historical record.

Required behavior:

- record the conflicting artifacts
- mark the claim as `contested` or `insufficient`
- surface the conflict in output

Examples:

- PR text says "refactor only," but tests and observable behavior changed
- release notes omit a major behavior change present in the diff
- issue frames one problem, but the merged implementation addresses another

## Abstention Rules

CodeLore must abstain when any of the following are true:

1. A claim would require unsupported causal explanation.
2. Evidence exists for what changed, but not why.
3. A typed inference rule is not available for the claim class.
4. Conflicting evidence exists and cannot be resolved within the window.
5. The available artifacts are too sparse to justify a nontrivial claim.

Allowed abstention outputs:

- `no_evidence`
- `insufficient_evidence`
- `conflicting_evidence`
- `unsupported_inference`

## Output Contract For MVP

The primary artifact should be an evidence pack containing:

- window metadata
- artifact index
- claims
- evidence references
- warrants
- contradictions
- unresolved questions
- abstentions

Any human-readable summary should be derived from this pack and should preserve
claim traceability back to the structured artifact.

## MVP Focus
CodeLore MVP focuses on bounded historical reconstruction. The following areas
remain outside the first slice:

- infer global architecture from one window
- infer team strategy from sparse metadata
- explain every change
- replace reading the underlying evidence for high-stakes interpretation
