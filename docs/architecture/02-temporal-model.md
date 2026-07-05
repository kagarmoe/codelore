---
title: Temporal Model
date: 2026-07-04
status: current
supersedes:
  - docs/architecture/archive/09-temporal-validity.md
---

# CodeLore Temporal Model

## Purpose

CodeLore reconstructs project history from bounded `ChangeWindow`s. Time is
part of what CodeLore is allowed to claim.

The central rule is:

**A window scopes analysis. It does not, by itself, define truth over time.**

Temporal validity must be established through explicit artifact clocks,
membership rules, evidence times, snapshot times, and warrants.

## Why This Matters

A commit in a release window may have:

- an author date before the window
- a committer date inside the window
- a merge date inside the window
- a tag/release date after the commit
- PR discussion that started before the window and ended inside it
- release notes published after the code change

If CodeLore says "this changed in the window," the warrant must say which
temporal rule supports that claim.

## Temporal Concepts

### Artifact Time

Artifact time is the timestamp carried by a source artifact.

Examples:

- commit author time
- commit committer time
- annotated tagger time
- release published time
- PR created, updated, closed, and merged times
- issue created, updated, and closed times
- comment created and edited times

Artifact time does not automatically establish window membership.

### Window Boundary Time

For a `ReleaseWindow`, the boundary is primarily ref-based:

- start ref
- end ref
- resolved start SHA
- resolved end SHA

Release timestamps such as tagger time or release publication time are useful
but not interchangeable with ref reachability.

### Window Membership

Window membership answers why a record belongs to a `ChangeWindow`.

Membership is a `LinkRecord`, not only a property.

Examples:

- commit reachable from end ref and not from start ref
- diff hunk produced by an included commit
- PR linked to an included commit
- issue referenced by an included PR
- release note associated with the end release

Membership links state membership type, basis, method, confidence where needed,
and relevant temporal support.

### Evidence Time

Evidence time is the timestamp associated with the evidence used to support a
claim.

It helps distinguish:

- what was known before a change
- what was stated during implementation
- what was described after release
- what was reconstructed later

Release-note evidence can directly support "the release notes described the
change as X." It is weaker support for "the implementation was motivated by X"
unless corroborated by pre-merge or in-window evidence.

### Snapshot Time

Snapshot time is when CodeLore captured a mutable external source.

If a forge API does not expose edit history, CodeLore may know only that the
snapshotted text existed at capture time, not that it existed at artifact
creation time.

Claims derived from mutable forge text must preserve this distinction.

### Claim Scope And Validity

Claim scope says the claim is made within, or about, a window.

Claim validity describes what kind of temporal assertion CodeLore is making.

MVP validity kinds:

- `observed_in_window`
- `changed_in_window`
- `discussed_in_window`
- `documented_after_window`
- `unknown_temporal_validity`

Deferred until construction rules exist:

- `introduced_in_window`
- `removed_in_window`
- `validFrom`
- `validUntil`
- `validDuring`

### Observation Validity

Observation validity applies to window-scoped observations such as module,
symbol, problem, or decision observations.

Observation validity must not be silently promoted to canonical identity.
Canonicalization follows `03-identity-and-canonicalization.md`.

### Asserted Domain Validity

The default CodeLore record is epistemic:

- artifact A says X
- evidence E supports claim C
- warrant W justifies C under rule R
- claim C is supported, contested, insufficient, or abstained

An asserted domain projection may be created only from filtered supported claims
under explicit rules. Candidate, contested, insufficient, and abstained
statements must not be asserted as domain facts.

## Release Window Rules

Phase 2 uses a ref-first membership model:

- membership is determined by ref reachability, not timestamp ordering
- canonical serialization sorts by stable ID
- timelines label the selected clock
- author time, committer time, merge time, tag time, release time, and snapshot
  time are preserved as distinct values when available

### Commit Membership

A commit is native to the window when it is reachable from `end_ref` and not
reachable from `start_ref`, under the documented traversal policy.

The corpus audit records:

- all-ancestry versus first-parent policy
- resolved start and end SHAs
- merge style
- how out-of-window author dates are handled

### File And Diff Membership

A file change or diff hunk is native to the window when produced by a native
commit.

The selected clock must be labeled:

- committer time by default for replayed git history
- author time recorded separately
- merge time when available through forge data

### Forge Artifact Membership

PRs and issues are not native to a git window merely because their timestamps
fall inside it.

They are linked when there is structural or explicit relation:

- PR contains an included commit
- PR merged to produce an included commit
- commit message references PR or issue
- PR body references issue
- release notes reference PR or issue

### Release Note Membership

Release notes associated with the end release are linked to the window even if
published after the final included commit.

Their evidence time remains the release-note publication or source time.

## RDF And Named Graphs

RDF named graphs package window-scoped exports.

Named graph membership is an export partition and provenance boundary. It does
not by itself assert:

- that a proposition was true for the whole window
- that it became true at the start boundary
- that it stopped being true at the end boundary
- that every artifact shares one timestamp semantics

Temporal validity must be represented explicitly with CodeLore vocabulary such
as:

- `cl:observedIn`
- `cl:nativeToWindow`
- `cl:linkedToWindow`
- `cl:membershipBasis`
- `cl:evidenceTime`
- `cl:artifactTime`
- `cl:temporalValidityKind`

Interval vocabulary such as `validFrom`, `validUntil`, and `validDuring` is
deferred until CodeLore can construct interval validity.

## Invariants

- Every window-scoped record references a `ChangeWindow`.
- Every membership link states its basis or follows an explicit relation
  contract.
- Every timestamp records its kind or source clock.
- Every temporal claim has a warrant naming the temporal rule.
- Named graph membership never substitutes for `observedIn`,
  `membershipBasis`, or validity kind.
- Candidate, contested, insufficient, or abstained claims are not exported as
  asserted domain facts.
- Release-note evidence is temporally distinguishable from implementation-time
  evidence.
