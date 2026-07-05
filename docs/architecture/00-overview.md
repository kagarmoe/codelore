---
title: CodeLore Architecture Overview
date: 2026-07-04
status: current
supersedes:
  - docs/architecture/archive/06-schema-draft.md
  - docs/architecture/archive/08-rdf-export-decision.md
  - docs/architecture/archive/10-link-record-model.md
  - docs/architecture/archive/11-record-admission-model.md
---

# CodeLore Architecture Overview

## Purpose

This directory defines the durable architecture for CodeLore.

CodeLore is an evidence system for reconstructing how a software project
changed over time. It turns bounded slices of project history into durable
records, evidence, claims, warrants, temporal context, and queryable derived
views without flattening history into timeless current-state documentation.

The architecture has two jobs:

1. Preserve the evidentiary chain from raw source material to every claim
   CodeLore is willing to make or abstain from.
2. Keep every derived view — query indexes, graph databases, RDF exports,
   dossiers, and summaries — rebuildable from the evidence pack.

That makes the core dependency direction:

```text
raw snapshots -> admitted records -> evidence pack -> derived views
```

The evidence pack is the source of truth. Derived views help people and agents
query, inspect, or exchange the memory CodeLore built; they do not become
authoritative data.

## Read Order

Read the current architecture documents in this order:

1. `00-overview.md` — system shape and architectural commitments.
2. `01-evidence-pack-pipeline.md` — how information becomes records and how the
   pack is assembled.
3. `02-temporal-model.md` — how windows, artifact clocks, and temporal
   validity work.
4. `03-identity-and-canonicalization.md` — how window observations may become
   canonical identities.
5. `04-schema.md` — current operational schema and Phase 2 subset.
6. `05-derived-views-and-rdf.md` — Neo4j, structured query tiers, and RDF
   projection policy.

The `archive/` directory contains earlier architecture drafts preserved for
traceability. They are no longer the orientation path.

## Core Commitments

### Evidence Pack First

The evidence pack is canonical product data.

The canonical on-disk shape is a directory of JSON and JSONL collections:

```text
evidence-pack/
  manifest.json
  project.json
  window.json
  artifacts.jsonl
  links.jsonl
  evidence.jsonl
  claims.jsonl
  warrants.jsonl
  contradictions.jsonl
  abstentions.jsonl
  open_questions.jsonl
```

Phase 2 starts with the subset it can build deterministically:

```text
manifest.json
project.json
window.json
artifacts.jsonl
links.jsonl
```

### Records Are Admitted, Not Discovered

Information becomes durable only through an explicit admission rule.

The record lifecycle is:

```text
raw input -> candidate datum -> admitted record -> validated pack record
```

Rejected candidates are accounted for in the run manifest when they cross a
stage's declared candidate boundary.

### Claim, Evidence, Warrant

CodeLore uses one cross-disciplinary reasoning shape:

```text
Evidence + Warrant -> Claim
```

- **Evidence** is cited source support.
- **Warrant** is the rule explaining why evidence supports a claim.
- **Claim** is the proposition CodeLore advances, contests, marks insufficient,
  or abstains from.

This language is intentionally preferred over discipline-specific terms that do
not travel well across ontology, data engineering, and implementation.

### Relationships Are Records

`LinkRecord` is the pack-side relationship primitive.

Relationships must not live only in:

- prose claim statements
- embedded ID lists
- Neo4j edges
- RDF syntax

If a relationship matters to claims, warrants, graph projection, or RDF export,
it should be explicit, typed, validated, and replay-stable in `links.jsonl`.

### Time Is Explicit

A `ChangeWindow` scopes analysis. It does not by itself define truth over time.

Temporal validity must be represented through explicit artifact clocks,
membership rules, evidence times, snapshot times, and warrant rules.

Named graph membership in RDF is an export partition and provenance boundary,
not temporal validity by itself.

### Graph Semantics Before Graph Infrastructure

The graph semantics are product core:

- records
- links
- evidence
- claims
- warrants
- observations
- identity decisions

Graph infrastructure such as Neo4j is a derived traversal view and must earn
its place through query value. The graph is rebuilt from the pack, never edited
as source data.

## Current Phase 2 Subset

Phase 2 is deterministic and git-first. It admits:

- `Project`
- `ChangeWindow`
- `ArtifactRecord`
- `LinkRecord`
- run manifest records

It does not yet admit text-derived evidence, full claims, warrants, or graph
projection as required outputs.

Phase 2 implementation follows:

- `docs/plans/00b-development-plan-evidence-first.md`
- `docs/plans/02-data-engineering-infrastructure-plan.md`
- `docs/plans/03-phase-2-implementation-plan.md`

## Review Rule

Architecture changes should be reviewed against at least one of these lenses:

- schema clarity
- data systems and source-of-truth design
- high-assurance invariants
- ontology/category discipline
- evidence and warrant discipline

Review reports live in `docs/reviews/`.
