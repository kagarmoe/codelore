# CodeLore Product Definition

## Purpose

This document is the primary product-definition draft for CodeLore.

It returns to the original framing:

`gt-wiki` turns releases into wiki pages. `CodeLore` turns releases into
evidence-backed project memory.

More generally, CodeLore should become a system for constructing, preserving,
and querying how a software project evolved over time.

## Core Abstraction

`ChangeWindow` is the canonical unit of historical reconstruction in CodeLore.

Window types include:

- `ReleaseWindow`
- `CommitRangeWindow`
- `DateRangeWindow`

`Release` remains important, but it should be treated carefully:

- as an artifact with notes, metadata, and project meaning
- as a named boundary for one kind of `ChangeWindow`

This distinction matters because CodeLore is intended to generalize beyond
release-only repos while preserving release-centered analysis as a first-class
case.

## Ontology Discipline

A category becomes first-class only when it has:

- distinct construction rules
- distinct query value
- distinct failure modes

Useful labels are not automatically useful entities.

## 1. Concise Product Definition

### What CodeLore is

CodeLore is a system for reconstructing and querying the evolving knowledge of
a software project over time from bounded change windows and their supporting
evidence.

Its core job is to turn project history into structured memory:

- what changed
- why it changed
- what problem it addressed
- what decisions were made
- what evidence supports those interpretations
- what remains uncertain or unresolved

### Who it is for

CodeLore is for:

- maintainers
- new contributors
- staff and principal engineers
- release managers
- technical investigators
- engineering leaders
- agents that need historically grounded project understanding

### What problem it solves

Software knowledge is scattered across releases, issues, PRs, commits, diffs,
docs, tests, and discussion. Each artifact contains only part of the story.

Current tools usually provide one of the following:

- raw artifact access
- current-state documentation
- code search
- changelogs
- wiki summaries

They do not reliably preserve how project knowledge evolved over time with
evidence attached.

CodeLore solves this by building a structured, queryable memory layer over
project history.

### Primary question classes

CodeLore should answer the following kinds of questions better than changelogs,
wiki pages, or code search alone:

- what changed in this window
- why it changed, when that is evidenced
- which artifacts support a given interpretation
- what problem was explicitly stated, discussed, solved, inferred, or left
  unresolved
- what decisions, tradeoffs, or constraints shaped the change
- how one window relates to earlier or later windows
- which parts of the story are supported versus uncertain

### How it differs from `gt-wiki`

`gt-wiki` is an agent-driven process that turns release evidence into wiki-form
documentation for a specific project.

CodeLore is the generalized product that turns bounded project history into
evidence-backed project memory.

Key difference:

- `gt-wiki` terminates in pages
- CodeLore terminates in structured project memory expressed through claims,
  evidence, timelines, and relationship views, including graphs where useful

### What it is explicitly not trying to do

CodeLore is not primarily:

- a generic wiki generator
- a replacement for reading source in high-stakes cases
- a generic code search product
- a generic knowledge graph toolkit
- an ontology-first research project detached from software evidence
- a system that invents explanations where evidence is weak

### What CodeLore will refuse to do

CodeLore should refuse the following behaviors:

- infer author psychology
- state “why” without adequate support
- collapse conflicting evidence into one tidy story
- silently flatten historical window context
- present unsupported speculation as a supported claim

## 2. Product Boundary

### What should remain part of `gt-wiki`

The following should remain part of `gt-wiki`:

- the domain-specific wiki output workflow
- markdown page generation and organization
- `gastown`-specific schema and vocabulary
- wiki-oriented curation and navigation surfaces
- the existing `.claude/skills` as prototype workflow assets

### What should move into CodeLore

The following should move conceptually into CodeLore:

- bounded change-window analysis
- release and change artifact ingestion
- issue / PR / commit / diff linking
- evidence-backed claim construction
- warrant and contradiction tracking
- timeline and historical context reconstruction
- queryable graph and retrieval logic
- structured uncertainty and abstention handling

### What should be generalized beyond `gt-wiki`

These parts should be generalized:

- release sync becomes change-window assembly
- page-centric synthesis becomes artifact/entity modeling
- drift becomes contradiction/divergence tracking
- `gastown` taxonomy becomes repo-agnostic artifact classes
- batch log discipline becomes provenance/event logging

### What should be postponed as future work

The following should be postponed:

- wiki generation as a downstream output
- broad concept-graph and architecture-graph automation
- aggressive inferred intent and decision extraction
- cross-repo global memory
- polished web UI
- broad non-GitHub connector strategy beyond the core git model

## 3. Proposed MVP

### The smallest coherent version of CodeLore

The smallest coherent CodeLore is:

- ingest one repo for one bounded release window
- gather commits, diffs, docs, tests, PRs, issues, and release artifacts
- build a structured evidence pack
- create a small set of evidence-backed claims
- preserve contradictions, uncertainties, and unresolved questions
- answer a small number of historical questions from that structure

### Product model versus first implementation slice

The product model supports multiple `ChangeWindow` types:

- `ReleaseWindow`
- `CommitRangeWindow`
- `DateRangeWindow`

The first implementation slice should operationalize only one bounded case:

- a `ReleaseWindow`
- on `gastown v1.1.0 -> v1.2.0`

This keeps the product definition general while keeping the first build narrow.

### Required inputs

For the first slice:

- local git repo
- release tags
- commits in the release window
- diffs in the release window
- changed docs
- changed tests
- changelog and release notes where present
- GitHub PR and issue metadata where available

### Core outputs

Core outputs for MVP:

- change-window record
- artifact index
- claims
- evidence links
- warrants
- contradictions
- unresolved questions
- derived summary

### First supported workflow

First workflow:

1. select a release window
2. ingest and classify in-window artifacts
3. link artifacts structurally and explicitly
4. generate an evidence pack
5. answer bounded historical questions against that pack

Canonical first slice:

- `gastown v1.1.0 -> v1.2.0`

### What graph capabilities are required for MVP

Required for MVP:

- change-window-scoped subgraph
- artifact relationship graph
- claim-to-evidence-to-warrant relationships
- timeline ordering within the window

### What graph capabilities can wait

Can wait:

- deep concept graphs
- broad decision graphs across many releases
- symbol-evolution graphs across the whole repo
- cross-repo graph merging
- automatic architecture graphs

## 4. Conceptual Architecture

### Core components

#### Git ingestion

Responsible for:

- tags
- commits
- diffs
- changed files
- timestamps
- ancestry and window membership

#### GitHub ingestion

Responsible for:

- PRs
- issues
- comments
- release metadata
- discussions where available

#### Evidence normalization and provenance

Responsible for:

- artifact canonicalization
- provenance capture
- stable artifact and evidence identifiers
- source span or reference extraction
- evidence-type classification
- confidence and linkage metadata where applicable

This layer turns heterogeneous raw artifacts into normalized evidence records
that later stages can reason over consistently.

#### Change-window builder

Responsible for:

- defining the bounded analysis slice
- collecting in-window artifacts
- assigning provenance and membership

#### Issue / PR linker

Responsible for:

- explicit references
- merge relationships
- issue closure links
- unresolved linkage where confidence is low

#### Commit and diff analyzer

Responsible for:

- changed files
- changed modules
- changed tests
- changed docs
- behaviorally relevant file changes

#### Graph builder

Responsible for:

- project graph
- change-window subgraph
- claim/evidence/warrant edges
- timeline relations

#### Embedding builder

Useful but secondary in MVP. Responsible for:

- semantic retrieval over artifacts and summaries
- similarity support for later question answering

Embeddings should support retrieval, not replace evidence structure.

#### Summarizer

Responsible for:

- deriving readable summaries from structured evidence
- preserving traceability back to claims and artifacts

#### ADR / decision extractor

Responsible for:

- explicit decision evidence
- explicit tradeoffs
- explicit constraints

Aggressive inference should wait until after the first slice.

#### Timeline builder

Responsible for:

- ordering events inside the window
- connecting artifacts to historical progression

#### Intent / problem extractor

Responsible for:

- explicit problem statements
- discussed problems
- solved problems
- inferred problems
- possible problems

The broader model should exist now even if MVP implements only the safer subset.

#### Evidence / warrant manager

Responsible for:

- evidence references
- warrant typing
- contradiction tracking
- abstention / unresolved state

#### Storage layer

Responsible for:

- artifact storage
- graph storage
- provenance storage
- query support

#### Interface layer

Initial surface:

- CLI
- evidence-pack export
- derived summary export

Future surface:

- local web explorer
- API / library interface

## 5. Data Model

### Core entities

- `Project`
- `ChangeWindow`
- `Release`
- `Commit`
- `PullRequest`
- `Issue`
- `Diff`
- `Module`
- `Symbol`
- `Problem`
- `Decision`
- `Evidence`
- `Warrant`
- `Concept`
- `TimelineEvent`
- `ADR`
- `Summary`
- `Claim`

### Supporting entities

- `DocChange`
- `TestChange`
- `Comment`
- `ArtifactLink`
- `Contradiction`
- `UnresolvedQuestion`

### Reasoning and status classes

The broader reasoning model distinguishes:

- explicitly stated problems
- discussed problems
- solved problems
- inferred problems
- possible problems
- unsupported speculation

These should be treated first as reasoning classes or claim/status classes.
They should become first-class entities only if later implementation proves
they need distinct identity and query behavior.
- `Observation`
- `Finding`
- `Abstention`

### Core relationships

- `Project HAS_WINDOW ChangeWindow`
- `Release IS_WINDOW ChangeWindow`
- `ChangeWindow CONTAINS Commit`
- `ChangeWindow CONTAINS PullRequest`
- `ChangeWindow CONTAINS Issue`
- `ChangeWindow CONTAINS Diff`
- `PullRequest IMPLEMENTED_BY Commit`
- `Issue RELATED_TO PullRequest`
- `Diff MODIFIES Module`
- `Diff MODIFIES Symbol`
- `Claim SUPPORTED_BY Evidence`
- `Claim JUSTIFIED_BY Warrant`
- `Claim CONTRADICTED_BY Evidence`
- `Claim EVIDENCED_IN_WINDOW ChangeWindow`
- `Problem ADDRESSED_BY PullRequest`
- `Problem DISCUSSED_IN Issue`
- `Problem DISCUSSED_IN PullRequest`
- `Problem OBSERVED_AS Observation`
- `Decision DERIVES_FROM Evidence`
- `Decision OBSERVED_AS Observation`
- `Decision CONSTRAINS Change`
- `Artifact DERIVES_FROM Artifact`
- `Artifact SUPERSEDES Artifact`
- `TimelineEvent PRECEDES TimelineEvent`

### Temporal semantics

CodeLore should distinguish between canonical entities and window-scoped
observations.

#### Canonical entities

These represent the ongoing identity of a thing across time, such as:

- a module
- a concept
- a problem class
- a long-lived decision theme

#### Window-scoped observations

These represent how a canonical entity appears within a specific
`ChangeWindow`.

Examples:

- a module as modified in `v1.1.0 -> v1.2.0`
- a problem as explicitly discussed in one release window
- a concept as renamed or reframed in a specific month

#### Recommended rule

When historical identity matters across windows, use a canonical entity plus
window-scoped observations. When the entity exists only meaningfully within a
single window, a window-scoped object alone is sufficient.

### MVP simplification

The full data model should exist conceptually, but MVP may operationalize only a
subset:

- `Project`
- `ChangeWindow`
- `Release`
- `Commit`
- `PullRequest`
- `Issue`
- `Diff`
- `Claim`
- `Evidence`
- `Warrant`
- `TimelineEvent`

## 6. Knowledge Representation Strategy

### Primary representation

Use a property-graph-oriented model for operational reasoning about
relationships among artifacts, claims, evidence, and timelines.

### Additional representations

- release-scoped or change-window-scoped subgraphs
- event logs for provenance
- vector embeddings for retrieval support
- structured links back to GitHub artifacts and local git artifacts
- claim/evidence/warrant records as typed structures

### RDF triples where useful

RDF may be useful for export or interoperability, but CodeLore should not be
designed as an ontology-first or RDF-first product. The model should emerge from
software project evidence rather than from adopting an external ontology
wholesale.

### Representation principles

1. Evidence precedes narrative.
2. Window context should be preserved.
3. Structural links and semantic links should remain distinguishable.
4. Explicit and inferred knowledge should remain distinguishable.
5. Uncertainty should be representable directly.

## 7. Reasoning Model For Evidence

CodeLore should distinguish between the following classes:

### Explicitly stated problems

Problems directly named in issues, PRs, release notes, ADRs, commit messages,
or comments.

### Discussed problems

Problems discussed in comments, threads, or documentation even if not crisply
formalized as the central issue statement.

Threshold:

- there is direct textual evidence of concern, risk, or pain
- the artifact discusses the problem without necessarily selecting it as the
  operative problem the implementation addresses

### Solved problems

Problems that have both:

- evidence of the problem, and
- evidence of the implemented response

Threshold:

- the problem is stated or strongly evidenced, and
- the window includes a linked implementation response, and
- the evidence supports that the response addresses the problem within the same
  or clearly connected windows

### Inferred problems

Problems not directly stated, but supported by multiple converging artifacts
such as code diffs, tests, failure-oriented changes, and surrounding discussion.

Threshold:

- at least two converging artifact types support the interpretation
- a typed warrant explains the inference
- no stronger conflicting direct evidence is present

### Possible problems

Plausible candidate problems that have suggestive but incomplete support.

Threshold:

- evidence is suggestive but below supported-claim threshold
- the interpretation is worth preserving as a live possibility
- the output should keep it separate from supported claims

### Unsupported speculation

Interpretations that are interesting but insufficiently supported by evidence.
These should be marked as unresolved or excluded from strong output.

Threshold:

- the interpretation lacks sufficient evidence, typed warrant support, or
  contradiction handling to qualify even as a possible problem
- it should not appear as a supported claim in the evidence pack

### Reasoning discipline

Every claim should preserve:

- evidence source
- warrant
- confidence
- contradiction state
- abstention state where needed

### MVP reasoning subset

The broader reasoning model above is part of the product definition.
The first implementation slice should start with the safer subset:

- explicit change claims
- structural linkage claims
- explicit problem claims
- explicit decision claims
- very narrow inferred claims only where typed warrant rules exist

### Claims, findings, abstentions, and open questions

CodeLore should distinguish between:

- `Claim`: a supported or contested proposition with evidence and warrant
- `Finding`: a noteworthy result of analysis, which may include a claim,
  contradiction, or missing-link observation
- `Abstention`: a structured declaration that the system does not have enough
  support to advance a claim
- `OpenQuestion`: a historically relevant question preserved for future
  investigation

## 8. Staged Implementation Plan

### Phase 0. Product definition

- define product boundary
- define change-window model
- define reasoning model
- define MVP evidence policy

### Phase 1. Extract reusable process from `gt-wiki`

- read and map the `.claude/skills`
- identify preserve / generalize / replace / defer decisions
- separate process logic from wiki output assumptions

### Phase 2. Design the first bounded model

- change-window model
- minimum artifact model
- claim / evidence / warrant model
- contradiction and abstention model

### Phase 3. Build ingestion prototype

- git ingestion
- release window assembly
- basic artifact indexing
- GitHub enrichment where available

### Phase 4. Build release graph prototype

- project and window graph
- structural artifact links
- timeline construction
- claim-to-evidence relationships

### Phase 5. Build summarization and query prototype

- evidence pack export
- bounded question answering
- traceable derived summary

### Phase 6. Evaluate graph quality and claim support

- linkage accuracy
- unsupported-claim rate
- abstention quality
- usefulness beyond changelog / code search

### Phase 7. Package as a portfolio-ready case study

- present `gastown v1.1.0 -> v1.2.0`
- show what CodeLore preserves that a wiki or changelog misses
- document model strengths and limitations

### Phase 8. Hostile validation

- validate on `llama.cpp`
- test monthly and arbitrary date windows after the first release slice is sound

## 9. Open Questions And Risks

### Graph scope

- How much graph structure is truly required for differentiated value?
- Which questions need graph traversal rather than structured retrieval?

### Cost

- What is the cost of enrichment, summarization, and repeated window builds?

### Speed

- How large can a window be before the evidence pack becomes too broad?

### Repository size

- How should the model degrade for large repos and noisy windows?

### Release cadence

- How should CodeLore behave when releases are sparse or weakly documented?

### Continuous-delivery projects

- How should date windows and monthly blocks interact with whatever release
  structure does exist?

### Noisy or incomplete GitHub metadata

- How much should the product rely on GitHub semantics versus git-native facts?

### Incomplete issue / PR linkage

- How should uncertainty be surfaced when linkage is plausible but not certain?

### Inferred intent

- How far should inference go before trust collapses?

### Overclaiming

- How can the product preserve abstention discipline under pressure to explain?

### Evaluation quality

- What acceptance tests prove utility, not just fluency?

### Storage choices

- When does graph storage justify itself over simpler alternatives?

### Retrieval mode

- When should CodeLore use graph retrieval, vector retrieval, structured
  filtering, or compiled summaries?

## Summary

CodeLore should be defined first as a product for evidence-backed project
memory, not as a wiki successor and not as a graph demo.

Its central promise is that bounded project history can become structured,
traceable memory that supports historical reconstruction, reasoning, and query
with evidence attached.
