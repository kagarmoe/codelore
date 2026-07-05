# Handoff: Active Architecture Planning

Use this prompt for the next CodeLore session when resuming the unresolved
architecture planning from July 4, 2026.

```text
You are taking over work in `/home/kimberly/repos/codelore`.

Your task is not to implement immediately. Your task is to plan two related
architecture issues carefully, review them, and then decide what documentation
or implementation changes are warranted.

## Orient First

Start by reading:

1. `README.md`
2. `docs/plans/00b-development-plan-evidence-first.md`
3. `docs/plans/02-data-engineering-infrastructure-plan.md`
4. `docs/plans/03-phase-2-implementation-plan.md`
5. `docs/architecture/00-overview.md`
6. `docs/architecture/01-evidence-pack-pipeline.md`
7. `docs/architecture/02-temporal-model.md`
8. `docs/architecture/04-schema.md`
9. `docs/evidence/02-evidence-policy.md`
10. `docs/evidence/03-claim-taxonomy.md`
11. the current Data Systems review notes under `docs/reviews/`

Then inspect current repo state:

```bash
git status --short
find docs/handoffs -maxdepth 1 -type f | sort
find docs/architecture -maxdepth 2 -type f | sort
```

## Active Issue 1: State Evidence Versus Change Evidence

CodeLore currently models change evidence better than state evidence.

The architecture is strong on:

- bounded `ChangeWindow`s
- git-first ingestion
- artifact records
- link records
- evidence packs
- temporal membership
- claims, evidence, and warrants

But there is a risk of diff myopia:

If CodeLore focuses too much on changed lines, commits, and release-window
membership, it may explain what changed without understanding what the resulting
module, file, or function does.

Examine whether the architecture should explicitly distinguish:

- change evidence: evidence that something changed in a window
- state evidence: evidence of what code means, does, or is responsible for at a
  particular historical point

Important intuition:

A diff hunk can support "this function changed."
It usually cannot, by itself, support "this function is responsible for X" or
"this module implements Y."

Those latter claims may require code as evidence of itself:

- full file snapshots at `start_ref` and `end_ref`
- function or symbol bodies
- module-level context
- call sites
- tests that exercise behavior
- docs or comments near the code

Potential concepts to evaluate, not blindly adopt:

- `CodeStateEvidence`
- `CodeSnapshotEvidence`
- `ModuleStateObservation`
- `SymbolStateObservation`
- state-vs-change warrant types
- start/end snapshot extraction as part of Phase 2 or Phase 3

Core question:

How can CodeLore preserve evidence-backed historical change while also using
code state as evidence for what modules, files, and functions did at a point in
history?

Likely rule to test:

Claims about change can be supported by diff/window evidence.
Claims about behavior, responsibility, or role require state evidence from the
relevant code snapshot, plus an explicit warrant.

## Active Issue 2: Durable Log And Materialization

Plan the durable log and materialization model before implementation goes much
further.

Recent Data Systems review discussion sharpened the issue:

```text
durable log -> materialized evidence pack -> derived views
```

The unresolved question is what belongs in CodeLore's durable log.

The log must be rich enough to replay and migrate product state, but not so
broad that it quietly becomes an ungoverned product database. Do not treat "log"
as ordinary runtime logging. Treat it as the durable reconstruction substrate.

Plan explicitly before treating pack migration as easy. Questions to settle
include:

- what counts as a log event
- what goes in event payloads versus referenced content-addressed blobs
- how raw git, forge, and generator snapshots are retained
- how candidate creation, rejection, admission, validation, and pack emission
  are represented
- how event schemas are versioned and kept replay-compatible
- whether pack records cite generating event IDs
- how the evidence pack is materialized from a bounded log segment

Recommended artifact:

- a log-and-materialization architecture note reviewed by Data Systems, High
  Assurance, and Schema lenses

## Planning Process

For each issue:

1. Restate the problem in CodeLore terms.
2. Identify current architecture pressure points.
3. Propose the smallest model change that solves the problem.
4. State what must remain deferred.
5. Decide whether the change affects Phase 2, Phase 3, or only later phases.
6. Review before editing architecture or implementation plans.

If `superpowers` skills are available, use the appropriate full cycle. If not,
emulate the same discipline.

Minimum review lenses:

- Data Systems Reviewer
- Schema Skeptic
- Evidence Auditor
- High-Assurance Reviewer
- Ontology Reviewer
- Repository Miner

## Output Discipline

Do not implement immediately.

Do not introduce unclear ontology terms unless they earn their place.

Keep the Claim/Evidence/Warrant framing.

Expected outputs:

- one planning note or architecture draft for state-vs-change evidence
- one planning note or architecture draft for durable log/materialization
- review reports in `docs/reviews/`
- only then, any architecture or plan updates justified by the review
```
