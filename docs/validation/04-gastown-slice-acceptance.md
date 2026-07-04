# Acceptance Criteria For The First CodeLore Prototype Slice

## Scope

This document defines what success means for the first end-to-end CodeLore
prototype slice:

- project: `gastown`
- window type: `release`
- window: `v1.1.0 -> v1.2.0`

This slice is intended to validate the product core, not to prove full
generality.

## Primary Goal

Produce a trustworthy evidence pack for one release window that answers a small
set of historical questions better than a changelog alone.

## Required Inputs

The slice should ingest, at minimum:

- git tags for `v1.1.0` and `v1.2.0`
- commits in the release window
- diffs for the release window
- `CHANGELOG.md`
- release note or release-evidence artifacts if present
- available GitHub PR and issue metadata for the window

## Required Outputs

### 1. Window record

Must include:

- project identifier
- window type
- start tag
- end tag
- commit count
- artifact counts by class

### 2. Artifact index

Must include at least:

- commits
- PRs
- issues
- changed files
- changed docs
- changed tests

### 3. Claim set

Must include only MVP-allowed claim types and must preserve:

- supporting evidence references
- warrant references
- confidence
- status

### 4. Contradictions and abstentions

Must explicitly record:

- unsupported “why” questions
- contested claims
- missing or incomplete linkage

### 5. Compiled summary

May exist as a derived output, but only if every sentence can be traced back to
claims in the evidence pack.

## Questions The Slice Must Answer

The prototype should answer these reliably:

1. What changed in `v1.2.0` relative to `v1.1.0`?
2. Which issues, PRs, commits, and diffs support those changes?
3. Which problems are explicitly stated in release artifacts?
4. Which decisions or tradeoffs are explicitly stated?
5. Which meaningful questions remain unresolved because evidence is weak or
   absent?

## Questions The Slice Does Not Need To Fully Answer

These are out of scope for first-slice success:

- global architecture evolution across many releases
- symbol-level historical reasoning across the whole codebase
- reliable root-cause explanation for every change
- full semantic intent reconstruction

## Minimum Quality Bar

### Structural linkage quality

The system should correctly establish:

- release membership for commits
- PR-to-commit links when metadata is available
- issue-to-PR links when explicitly referenced

False linkage should be visibly rare.

### Claim quality

Every reported claim must have:

- at least one evidence link
- at least one warrant
- a confidence label
- a status label

No free-floating narrative claims are allowed.

### Abstention quality

If the system cannot justify “why,” it must say so explicitly instead of
inventing explanation.

### Traceability

A reviewer should be able to select any claim and navigate to the supporting
artifact set without manual reconstruction.

## Acceptance Tests

The slice is acceptable only if all of the following are true.

### Test 1. Window integrity

Given `v1.1.0 -> v1.2.0`, the system builds a coherent window record with the
expected bounded artifact set.

### Test 2. Artifact traceability

For sampled claims, a reviewer can trace the claim back to specific artifacts
without ambiguity.

### Test 3. Abstention behavior

For sampled “why” questions with weak evidence, the system returns abstention or
uncertainty instead of confident narrative.

### Test 4. Better-than-changelog utility

For at least three representative questions, the evidence pack provides more
useful historical support than reading `CHANGELOG.md` alone.

Suggested question categories:

- change provenance
- explicit problem statement
- explicit decision/tradeoff

### Test 5. Contradiction visibility

If metadata conflicts or is incomplete, the conflict is preserved rather than
collapsed.

## Failure Conditions

The slice should be considered unsuccessful if any of these occur:

1. The summary contains claims not backed by structured evidence.
2. The system frequently infers “why” from weak evidence.
3. Artifact linking is noisy enough that reviewers distrust the output.
4. The graph/storage model dominates implementation effort before claim quality
   is proven.
5. The resulting output is not materially better than a filtered changelog plus
   commit list.

## What Success Enables Next

If this slice succeeds, the next justified steps are:

- expose `commit_range` windows
- expose `date_range` windows
- test a hostile internal slice with weaker metadata
- evaluate a CD-style repo such as `llama.cpp`
- expand claim types carefully
