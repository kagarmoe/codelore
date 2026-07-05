---
title: Derived Views, Graphs, And RDF
date: 2026-07-04
status: current
supersedes:
  - docs/architecture/archive/08-rdf-export-decision.md
---

# Derived Views, Graphs, And RDF

## Purpose

This document defines how CodeLore projects evidence-pack records into derived
query and interoperability views.

The rule is:

**Derived views are rebuildable from the evidence pack and are never the source
of truth.**

## View Types

### Pack-Direct Views

Pack-direct code reads canonical JSON/JSONL files.

Use for:

- fixture tests
- deterministic acceptance checks
- simple lookup by ID
- local claim-to-evidence navigation

### Structured Query Tier

DuckDB or SQLite may index packs for shallow joins and filters.

Use for:

- filtering claims by type/status/confidence
- joining claims to warrants and evidence
- artifact counts
- window dashboards
- bounded exploratory queries

The structured query tier has no schema authority. It can be deleted and
rebuilt from packs.

### Neo4j Graph View

Neo4j is a derived traversal engine.

Adopt it only if it answers important questions better than pack-direct or
structured-query approaches.

Graph-worthy questions include:

- What evidence chain supports this claim through multiple artifacts?
- Which claims are affected if an artifact is contradicted?
- Did this module/problem/decision recur across windows?
- Is this the same entity, label reuse, or uncertain continuity?
- Which identity-resolution paths connect these observations?

Non-graph-worthy questions include:

- list all claims in a window
- count changed files
- find explicit problems
- show claims for one artifact
- export a dossier

Those are table or pack queries unless a traversal requirement appears.

## Neo4j Projection

Neo4j nodes and edges are derived from pack records.

Rules:

- `LinkRecord` projects to edges.
- Endpoint IDs identify source and target nodes.
- `relation_type` maps to edge label/type.
- `link_id`, `link_method`, `membership_type`, and `confidence` map to edge
  properties.
- Graph schema evolution is rebuild-from-pack, not in-graph migration.
- The loader must not synthesize relationships absent from `links.jsonl`.

Before loading:

- create uniqueness constraints for stable node IDs
- choose drop-and-rebuild or constrained `MERGE`
- batch writes with `UNWIND`
- keep transaction sizes explicit

## RDF Export Decision

CodeLore uses RDF 1.2 named reifiers for RDF statement metadata.

The canonical model remains:

- `LinkRecord`
- `Claim`
- `Warrant`
- `Evidence`
- `ArtifactRecord`

RDF is an export/projection format.

The export preserves:

```text
Evidence + Warrant -> Claim
```

`LinkRecord` provides an identifiable relationship or membership statement that
claims may cite. A `Warrant` remains the reasoning rule explaining why cited
evidence supports a claim.

## RDF Shape

When a link corresponds to an RDF subject-predicate-object proposition, the link
resource may use `rdf:reifies` with an RDF 1.2 triple term:

```turtle
GRAPH :window-gastown-v1_1_0-v1_2_0 {
  :link-123
    rdf:reifies <<( :commit-abc :touchesFile :file-scheduler )>> ;
    a cl:LinkRecord ;
    cl:linkMethod cl:GitDiff ;
    cl:confidence cl:High ;
    cl:supportedBy :evidence-456 ;
    cl:inWindow :window-gastown-v1_1_0-v1_2_0 .

  :claim-789
    a cl:Claim ;
    cl:claimType cl:ChangeFact ;
    cl:aboutLink :link-123 ;
    cl:hasWarrant :warrant-555 ;
    cl:hasEvidence :evidence-456 .
}
```

Named graphs package `ChangeWindow` exports.

Named graph membership is an export partition and provenance boundary. It is
not temporal validity by itself.

## Epistemic Export Versus Asserted Domain Graph

The default RDF export is an epistemic/provenance graph. It records what
CodeLore observed, claimed, warranted, contested, or abstained from within a
window.

An OWL/RDFS asserted domain graph must be a separate, explicit, filtered
projection from supported claims.

Candidate, contested, insufficient, or abstained statements must not be
asserted as ordinary domain facts merely because they are represented in RDF.

## Compatibility

Classic RDF 1.1 reification using `rdf:Statement`, `rdf:subject`,
`rdf:predicate`, and `rdf:object` may be added as a compatibility export for
systems that cannot consume RDF 1.2.

It is not the primary representation.

## Formal Exports

Future formal exports:

- RDF for pack data
- SKOS for taxonomy and glossary outputs
- OWL for ontology schema

OWL export should be checked with a standard reasoner for mechanical
consistency: unsatisfiable classes, domain/range violations, and related formal
issues.

The reasoner check validates formal structure, not historical truth.
