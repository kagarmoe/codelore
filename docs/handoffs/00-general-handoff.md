# Handoff: General CodeLore Orientation

Use this prompt when handing CodeLore to a new agent.

```text
You are taking over work in `/home/kimberly/repos/codelore`.

Your job is to continue turning CodeLore into a standalone product and
implementation. Orient from the repo as it exists now; this repo is changing
quickly, so do not assume filenames or phase details from memory.

## Product Frame

CodeLore reconstructs how a software project changed over time and turns that
history into evidence-backed project memory.

Core distinction:

`gt-wiki` turns releases into wiki pages.
`CodeLore` turns project history into evidence-backed memory.

This is not a wiki generator. Do not let wiki-shaped assumptions become
CodeLore's architecture.

The canonical historical unit is `ChangeWindow`, not `Release`, though release
windows remain the first implementation slice.

## First Actions

Before coding, inspect the repo state and current documentation structure:

```bash
git status --short
git log --oneline -10
find docs -maxdepth 2 -type f | sort
find src -maxdepth 3 -type f | sort
```

Then read:

1. `README.md`
2. the current authoritative development plan under `docs/plans/`
3. the current architecture sequence under `docs/architecture/`
4. the evidence policy and claim taxonomy under `docs/evidence/`
5. the current Phase 2 or active implementation plan under `docs/plans/`
6. `AGENTS.md` and `CLAUDE.md`

Prefer the README and directory contents over stale handoff assumptions. If a
handoff points to a moved file, locate the current equivalent rather than
stopping.

Install Beads before planning or implementation if it is not already available
in the environment. Use the current Beads install instructions rather than a
remembered command, then initialize or inspect the repo's Beads issue state as
appropriate.

## Current Architectural Commitments

Preserve these commitments unless a reviewed architecture update changes them:

- Evidence pack first; derived views are not source of truth.
- Records are admitted through explicit rules, not merely discovered.
- Use the cross-disciplinary reasoning shape:

  ```text
  Evidence + Warrant -> Claim
  ```

- `LinkRecord` is the pack-side relationship primitive.
- Temporal validity is explicit; window membership alone is not temporal truth.
- Canonicalization is evidence-backed identity resolution, not name matching.
- Graph semantics matter, but graph infrastructure such as Neo4j is a derived
  view and must earn its place.
- Abstention is a valid analysis result when evidence is insufficient.

## Current Product Discipline

Optimize for:

- evidence-backed historical modeling
- explicit provenance
- careful ontology admission
- graph construction around `ChangeWindow` semantics, not graph-first tooling
- conservative claim discipline
- replayable, inspectable data transformations

Avoid:

- wiki-first architecture
- release-only assumptions
- unsupported why claims
- collapsing code history into timeless current-state docs
- treating broad labels as admitted ontology
- letting Neo4j or RDF become the source of truth

## Review Process

The repo has local review-persona guidance under `.claude/skills/`.
Use the functional lens, not the famous-person alias, as authoritative.

For important architecture or plan changes, use focused reviews such as:

- Evidence Auditor
- Schema Skeptic
- Data Systems Reviewer
- High-Assurance Reviewer
- Ontology Reviewer
- Repository Miner
- Plan Skeptic

Write review reports to `docs/reviews/`.

## Environment Notes

The setup runbook contains host details and should be treated as current only to
the extent it matches the actual machine.

Known stance:

- Python and `uv` are the primary development stack.
- Neo4j is optional infrastructure until a graph-value gate is passed.
- GPU/model work is future-facing and should be host-verified, not inferred
  from sandbox output.
- Graphify is optional agent-navigation tooling, not CodeLore's product graph.

## First Validation Target

The favorable first corpus remains:

- `gastown v1.1.0 -> v1.2.0`

The hostile/post-MVP validation corpus remains:

- `llama.cpp`

## Before Ending A Session

Follow repo session discipline:

1. check `git status`
2. run relevant checks for any work performed
3. commit and push if the change is ready and in scope
4. leave a concise handoff summary
```
