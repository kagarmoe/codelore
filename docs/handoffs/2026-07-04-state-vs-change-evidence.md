# Handoff: State Evidence Versus Change Evidence

Use this prompt for the next CodeLore session.

```text
You are taking over work in `/home/kimberly/repos/codelore`.

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

Then stop and focus on this architectural gap:

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

We need to examine whether the architecture should explicitly distinguish:

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

Do not implement immediately.

Run a full planning/review cycle first. If the `superpowers` skills are
available in the next session, use the appropriate full cycle. If not, emulate
the same discipline:

1. Restate the problem.
2. Identify current architecture pressure points.
3. Propose the smallest model change that handles state evidence.
4. Review it with at least:
   - Data Systems Reviewer
   - Schema Skeptic
   - Evidence Auditor
   - Ontology Reviewer
   - Repository Miner
5. Decide whether this changes Phase 2, Phase 3, or only later phases.
6. Only then update architecture/plans.

Core question:

How can CodeLore preserve evidence-backed historical change while also using
code state as evidence for what modules, files, and functions did at a point in
history?

A likely rule to test:

Claims about change can be supported by diff/window evidence.
Claims about behavior, responsibility, or role require state evidence from the
relevant code snapshot, plus an explicit warrant.

Keep the Claim/Evidence/Warrant framing. Avoid introducing unclear ontology
terms unless they earn their place.
```
