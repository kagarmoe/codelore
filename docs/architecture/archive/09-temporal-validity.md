---
title: Temporal Validity Model
date: 2026-07-04
status: draft
depends_on:
  - docs/architecture/06-schema-draft.md
  - docs/architecture/07-canonicalization-policy.md
  - docs/architecture/08-rdf-export-decision.md
  - docs/architecture/10-link-record-model.md
  - docs/plans/00b-development-plan-evidence-first.md
  - docs/plans/02-data-engineering-infrastructure-plan.md
---

# CodeLore Temporal Validity Model

## Purpose

CodeLore reconstructs project history from bounded `ChangeWindow`s. That means
time is not metadata garnish. It is part of what CodeLore is allowed to claim.

This document defines the temporal concepts CodeLore needs before implementing
git ingestion, evidence packs, graph projection, or RDF export.

The central rule is:

**A window scopes analysis. It does not, by itself, define truth over time.**

Temporal validity must be established through explicit artifact times,
membership rules, evidence times, and claim/observation validity fields.

## Why This Distinction Matters

A release window has boundaries. Commits, tags, releases, PRs, issues, comments,
and release notes have dates and times. But these clocks do not all mean the
same thing.

For example, a commit in a release window may have:

- an author date before the window
- a committer date inside the window
- a merge date inside the window
- a tag/release date after the commit
- PR discussion that started before the window and ended inside it
- release notes published after the tagged code state

If CodeLore says "this changed in the window," the warrant must say which
temporal rule made that true.

## Temporal Concepts

### Claim, Evidence, And Warrant Roles

CodeLore must keep claim, evidence, and warrant roles separate:

- `ArtifactRecord` records a source object.
- `Evidence` records an extracted source fragment or structural fact.
- `LinkRecord` records a CodeLore relationship or membership assertion.
- `Claim` records a proposition CodeLore advances within a window.
- `Warrant` records the rule explaining why evidence supports a claim.
- `Observation` records a window-scoped interpretation.
- asserted domain facts are filtered projections from supported claims.

This prevents a `LinkRecord` from accidentally meaning the source relation, the
claim about that relation, and the warrant for that claim all at once.

In short:

```text
Evidence + Warrant -> Claim
```

The warrant is not extra evidence and is not itself the claim. It is the
reasoning bridge from cited evidence to the claim CodeLore is willing, or
unwilling, to advance.

### 1. Artifact Time

Artifact time is the timestamp carried by a source artifact.

Examples:

- commit author time
- commit committer time
- tagger time for annotated tags
- release published time
- PR created, updated, closed, and merged times
- issue created, updated, and closed times
- comment created and edited times
- file modification time only when explicitly captured and justified

Artifact time answers:

- when did this source object say it happened?
- which clock produced the timestamp?
- how reliable is that clock for this question?

Artifact time does not automatically establish window membership. A commit can
be reachable from a release tag while having an author date outside the release
window.

### 2. Window Boundary Time

Window boundary time is the temporal interpretation of a `ChangeWindow`
boundary.

For a `ReleaseWindow`, the boundary is primarily ref-based:

- start ref
- end ref
- resolved start SHA
- resolved end SHA

The release may also have timestamps:

- tagger time
- release publication time
- changelog date

These are important, but they are not interchangeable with ref reachability.

For the first release-window implementation, membership is determined by the
documented ref traversal policy, not by timestamp alone.

### 3. Window Membership

Window membership answers why a record belongs to a `ChangeWindow`.

Membership is a relation, not only a property.

Examples:

- commit reachable from `end_ref` and not from `start_ref`
- changed file touched by an included commit
- diff hunk produced by an included commit
- PR linked to an included commit
- issue referenced by an included PR
- release note associated with the end release

Membership records must carry:

- source record
- target window
- membership type
- membership basis
- rule or method
- confidence
- relevant timestamps

This is a `LinkRecord` responsibility.

### 4. Evidence Time

Evidence time is the timestamp associated with the evidence used to support a
claim.

Examples:

- a text span in a PR body has PR creation/update time
- a comment span has comment creation/edit time
- a diff hunk has the commit's selected timestamp
- release-note evidence has publication time or source artifact time

Evidence time helps CodeLore distinguish:

- what was known before a change
- what was stated during implementation
- what was described after release
- what was reconstructed later

Evidence time is especially important for "why" claims. A post-release summary
may support "the release notes described the change as X"; it is weaker support
for "the original implementation was motivated by X" unless corroborated by
in-window or pre-merge evidence.

### 4a. Snapshot Time

Snapshot time is when CodeLore captured a mutable external source.

Examples:

- GitHub PR body fetched at time T
- issue comments fetched at time T
- release metadata fetched at time T
- language-model output snapshotted at time T

Snapshot time is not the same as artifact time. If a forge API does not expose
edit history, CodeLore may know only that the snapshotted text existed at
capture time, not that the same text existed at the artifact's creation time.

Claims derived from mutable forge text must preserve this distinction.

### 5. Claim Scope

Claim scope says the claim is made within, or about, a window.

Examples:

- "Within `v1.1.0 -> v1.2.0`, file X changed."
- "In this window, PR Y explicitly stated problem Z."
- "For this release, the supported evidence links commit C to issue I."

Claim scope is not the same as global truth.

A scoped claim may be supported for one window while absent, contradicted, or
irrelevant in another.

### 6. Claim Validity

Claim validity describes what kind of temporal assertion CodeLore is making.

Initial validity kinds:

- `observed_in_window`: supported as an observation within a window
- `changed_in_window`: support indicates the thing changed during the window
- `discussed_in_window`: support indicates the topic was discussed during the
  window
- `documented_after_window`: support comes from documentation after the code
  change or release boundary
- `unknown_temporal_validity`: evidence supports some relationship, but not
  when it became true or stopped being true

These values are analytical statuses. They should not become broad ontology
unless they prove distinct construction rules, query value, and failure modes.

MVP-admitted validity kinds should stay narrower:

- `observed_in_window`
- `changed_in_window`
- `discussed_in_window`
- `documented_after_window`
- `unknown_temporal_validity`

Stronger interval or lifecycle statuses such as `introduced_in_window`,
`removed_in_window`, `validFrom`, `validUntil`, and `validDuring` are deferred
until CodeLore has construction rules that can prove prior state, later state,
or interval boundaries.

### 7. Observation Validity

Observation validity applies to window-scoped observations such as
`ModuleObservation`, `SymbolObservation`, `ProblemObservation`, and
`DecisionObservation`.

An observation may be valid only as:

- observed in this window
- inferred from this window's artifacts
- carried forward from an earlier state
- contradicted by later evidence
- uncertain due to missing lineage

Observation validity must not be silently promoted to canonical identity.
Canonicalization still follows `docs/architecture/07-canonicalization-policy.md`.

### 8. Asserted Domain Validity

Asserted domain validity is the strongest form: CodeLore exports or serves a
statement as an ordinary domain fact.

This is not the default.

The default CodeLore record is epistemic:

- artifact A says X
- evidence E supports claim C
- warrant W justifies C under rule R
- claim C is supported, contested, insufficient, or abstained

An asserted domain projection may be created only from filtered supported claims
with explicit rules. Candidate, contested, insufficient, and abstained
statements must not be asserted as domain facts.

## Temporal Rules For Release Windows

For the MVP `ReleaseWindow`, CodeLore should use a ref-first membership model.

Phase 2 defaults:

- membership is determined by ref reachability, not timestamp ordering
- canonical serialization is sorted by stable ID
- timelines use explicit selected clocks and label the clock kind
- author time, committer time, merge time, tag time, release time, and snapshot
  time are preserved as distinct values when available

### Commit Membership

A commit is native to the window when it is reachable from `end_ref` and not
reachable from `start_ref`, under the documented traversal policy.

The corpus audit must record:

- whether traversal is all-ancestry or first-parent
- whether first-parent status is merely annotated or membership-defining
- resolved start and end SHAs
- merge style
- how out-of-window author dates are handled

### File And Diff Membership

A file change or diff hunk is native to the window when it is produced by a
native commit.

The timestamp inherited by the hunk should identify which commit clock is used:

- committer time by default for replayed git history
- author time recorded separately
- merge time when available through forge data

### PR And Issue Membership

PRs and issues are not native to a git window merely because their timestamps
fall inside the window.

They become linked records when there is a structural or explicit relation:

- PR contains an included commit
- PR merged to produce an included commit
- commit message references PR or issue
- PR body references issue
- release notes reference PR or issue

The membership type should distinguish native git membership from linked
context.

### Release Note Membership

Release notes associated with the end release are linked to the window even if
published after the final included commit.

Their evidence time remains the release-note publication or source time. This
prevents post-hoc release descriptions from being mistaken for pre-change
motivation.

## RDF And Named Graphs

RDF named graphs are useful for packaging window-scoped RDF exports:

```turtle
GRAPH :window-v1_1-to-v1_2 {
  :link-123
    rdf:reifies <<( :commit-abc cl:touchesFile :file-scheduler )>> ;
    cl:observedIn :window-v1_1-to-v1_2 ;
    cl:membershipBasis cl:ReachableFromEndNotStart .
}
```

But graph membership is only an export partition and provenance boundary. It
does not by itself assert:

- that the proposition was true for the whole window
- that the proposition became true at the start boundary
- that the proposition stopped being true at the end boundary
- that every artifact in the graph shares the same timestamp semantics

Temporal validity must be represented explicitly with CodeLore vocabulary.

Candidate properties:

- `cl:observedIn`
- `cl:nativeToWindow`
- `cl:linkedToWindow`
- `cl:membershipBasis`
- `cl:evidenceTime`
- `cl:artifactTime`
- `cl:temporalValidityKind`
- deferred: `cl:validDuring`
- deferred: `cl:validFrom`
- deferred: `cl:validUntil`

These names are candidates until admitted into the implemented schema.

## Pack Model Implications

### Artifact Records

Artifact records should preserve source-specific timestamps without collapsing
them.

Examples:

- `authored_at`
- `committed_at`
- `tagged_at`
- `published_at`
- `created_at`
- `updated_at`
- `merged_at`
- `closed_at`

Avoid a generic `timestamp` field unless it is accompanied by `timestamp_kind`.

Every normalized timestamp should preserve:

- normalized UTC value
- timestamp kind
- source system
- original value or offset where available

### Link Records

`LinkRecord` should carry temporal membership semantics where relevant.

Candidate fields:

- `membership_type`
- `membership_basis`
- `source_time`
- `source_time_kind`
- `snapshot_time`

Future fields:

- `time_relation`
- `evidence_time`
- `validity_kind`

The MVP should keep this small but explicit. A weak first version is better than
implicit temporal meaning hidden in code.

### Claims

Claims should carry temporal status through claim type, warrant, and possibly a
dedicated validity field.

Examples:

- a `change_fact` claim may be `changed_in_window`
- an `explicit_problem` claim may be `discussed_in_window`
- a release-note-derived claim may be `documented_after_window`
- a weak inference may have `unknown_temporal_validity`

### Warrants

Warrants must name the temporal rule used.

Examples:

- `reachable_from_end_not_start`
- `native_commit_touches_file`
- `release_note_for_end_release`
- `pr_merged_in_window`
- `issue_referenced_by_included_pr`

Temporal ambiguity belongs in warrant limitations.

## Query Implications

CodeLore should support questions such as:

- What changed in this window?
- Which evidence was created before the release?
- Which explanations are post-release descriptions?
- Which PRs were merged inside the window?
- Which commits have author dates outside the membership window?
- Which claims are supported only by after-the-fact documentation?
- Which observations are scoped to this window but not valid globally?

These questions require explicit temporal fields. Named graph membership alone
cannot answer them safely.

## Invariants

Initial invariants:

1. Every window-scoped record references a `ChangeWindow`.
2. Every membership link states its membership basis.
3. Every timestamp records its kind or source clock.
4. Every claim has a warrant that explains any temporal assertion it makes.
5. A named graph membership never substitutes for `observedIn`,
   `membershipBasis`, or `validity_kind`.
6. Candidate, contested, insufficient, or abstained claims are not exported as
   asserted domain facts.
7. Release-note evidence is temporally distinguishable from implementation-time
   evidence.

## Open Decisions

1. Decided (2026-07-04): Phase 2 membership is ref-reachability based;
   canonical serialization sorts by stable ID; timelines must label the clock
   used for display.
2. Proposed Phase 2 `LinkRecord` temporal field set:
   `membership_type`, `membership_basis`, `source_time`, `source_time_kind`,
   and optional `snapshot_time`.
3. Should `validity_kind` live on `LinkRecord`, `Claim`, both, or only in
   warrants for MVP?
4. Which temporal vocabulary terms should be admitted to the schema now versus
   kept as candidate export terms?
5. How should edited comments and updated PR bodies represent prior versus
   current textual evidence time?

## Summary

CodeLore needs temporal validity, but it must be explicit.

`ChangeWindow` and named graphs provide scope. Git and forge artifacts provide
source clocks. Link records explain membership. Warrants explain why temporal
claims follow from the evidence. Only that combination supports historically
disciplined claims.
