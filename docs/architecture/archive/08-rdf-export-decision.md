---
title: RDF Export Statement-Metadata Decision
date: 2026-07-04
status: accepted
depends_on:
  - docs/plans/00b-development-plan-evidence-first.md
  - docs/plans/02-data-engineering-infrastructure-plan.md
  - docs/architecture/10-link-record-model.md
---

# RDF Export Statement-Metadata Decision

## Decision

CodeLore will use **RDF 1.2 named reifiers** for RDF statement metadata.

The canonical CodeLore data model remains the evidence pack:

- `LinkRecord`
- `Claim`
- `Warrant`
- `Evidence`
- `ArtifactRecord`

RDF is an export/projection format, not the source of truth.

The export preserves the core reasoning shape:

```text
Evidence + Warrant -> Claim
```

`LinkRecord` provides an identifiable relationship or membership statement that
claims may cite. A `Warrant` remains the reasoning rule explaining why cited
evidence supports a claim; it is not extra evidence and is not itself the
claim.

## Export Shape

Each first-class CodeLore relation record maps to a stable RDF resource.

When a relation corresponds to an RDF subject-predicate-object proposition, the
relation resource may use `rdf:reifies` with an RDF 1.2 triple term:

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

Window scope maps to named graphs, one named graph per `ChangeWindow`.

Named graph membership is an export partition and provenance boundary. It is
not, by itself, a temporal truth condition.

## Rationale

CodeLore needs identifiable relationship statements and identifiable claims.

Confidence, evidence IDs, limitations, contradiction status, run ID, and window
scope all attach to durable CodeLore records. Anonymous RDF-star annotations are
too weak for this because CodeLore needs to preserve claim, evidence, and
warrant roles explicitly.

RDF 1.2 named reifiers give CodeLore a concise RDF projection while preserving
stable statement resources. They also support unasserted, candidate, contested,
or contradicted propositions because the reified proposition does not have to be
asserted as true.

The default RDF export is therefore an epistemic/provenance graph: it records
what CodeLore observed, claimed, warranted, contested, or abstained from within
a window. Any OWL-friendly asserted domain graph must be a separate, explicit,
filtered projection from supported claims.

Classic RDF 1.1 reification using `rdf:Statement`, `rdf:subject`,
`rdf:predicate`, and `rdf:object` is retained only as a possible compatibility
export for systems that cannot consume RDF 1.2.

## Consequences

- `LinkRecord` is required before RDF export.
- Stable CodeLore IDs must be mappable to IRIs.
- RDF export must distinguish asserted claims from candidate, abstained, or
  contested statements.
- Named graphs carry `ChangeWindow` scope, but temporal semantics must be
  represented explicitly with CodeLore vocabulary such as `cl:inWindow`,
  `cl:observedIn`, `cl:validDuring`, or more specific properties when they are
  admitted.
- Any asserted OWL/RDFS domain projection must be explicit and filtered from
  supported claims; it is never the default RDF export.
- RDF output is rebuilt from packs; it is never edited as authoritative data.
- A legacy RDF 1.1 reification export may be added later, but it is not the
  primary representation.

## Non-Goals

- Do not make RDF the operational source of truth.
- Do not rely on RDF syntax to compensate for missing `LinkRecord` semantics.
- Do not assert candidate or contested propositions as true merely because they
  are represented in RDF.
- Do not treat named graph membership as equivalent to temporal validity.
