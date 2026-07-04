# CodeLore Extraction Memo

## Purpose

This memo defines what CodeLore should inherit from `gt-wiki`, what it should
generalize, what it should replace, and what it should discard.

Core framing:

`gt-wiki` turns releases into wiki pages. `CodeLore` turns releases into
evidence-backed project memory.

More precisely after the current design update:

- `gt-wiki` is an agent-driven release-analysis and wiki-output process
- `CodeLore` is the standalone system for constructing, preserving, and
  querying project evolution over bounded change windows

## Preserve

These are the assets that should move conceptually into CodeLore with minimal
change.

### 1. Code-first and evidence-first discipline

The strongest reusable idea in `gt-wiki` is that source artifacts outrank
derived prose. CodeLore should preserve that in generalized form:

- code and raw artifacts are authoritative inputs
- generated summaries are downstream products
- every meaningful claim should point back to supporting artifacts
- drift between narrative and evidence is a first-class failure mode

### 2. Window-bounded analysis

`gt-wiki` is release-scoped. CodeLore should preserve the bounded-analysis
discipline but generalize the window type:

- release windows
- commit-range windows
- date-range windows

The important inheritance is not "release" alone. It is the rule that project
knowledge must be reconstructed relative to a bounded historical window rather
than flattened into a timeless current-state summary.

### 3. Structured workflow thinking

The skills in `.claude/skills` encode a process with explicit discipline:

- establish the change boundary
- gather and classify relevant artifacts
- verify against source
- distinguish signal from noise
- record unresolved questions

CodeLore should preserve that workflow shape as product logic.

### 4. Historical context matters

`gt-wiki` already assumes that older changes still explain current structure.
CodeLore should preserve this premise and make it computational:

- obsolete names can still explain current APIs
- old workarounds can explain current constraints
- vestigial code can still carry historical meaning
- implementation choices can outlive the issue or PR that introduced them

### 5. Explicit handling of incomplete understanding

The wiki process already allows "notes / open questions" and unresolved drift.
CodeLore should preserve the norm that uncertainty is valid output.

## Generalize

These parts are useful, but too specialized to move unchanged.

### 1. Release sync becomes change-window assembly

The current sync workflow is anchored to tagged releases. CodeLore should
generalize that to a `ChangeWindow` model:

- `release`
- `commit_range`
- `date_range`

Implementation MVP should still start with `release` windows, but the model
should be designed so the release case is one subtype rather than the whole
product.

### 2. Entity/page thinking becomes artifact/entity modeling

`gt-wiki` thinks in pages. CodeLore should think in entities and artifacts:

- commit
- PR
- issue
- file/module/symbol
- test changes
- doc changes
- claim
- evidence
- warrant
- unresolved question

Pages may later be generated from these, but the internal representation should
not depend on page structure.

### 3. Drift becomes contradiction and divergence handling

The wiki's "drift" concept is a good seed, but CodeLore should generalize it:

- narrative vs code contradictions
- PR intent vs implementation mismatch
- release notes vs actual change mismatch
- explicit rationale vs inferred behavioral consequence mismatch
- missing justification rather than contradictory justification

### 4. Topic-specific taxonomy becomes repo-agnostic classification

The `gastown` categories such as commands, packages, binaries, roles, and
specific schema conventions should not become core product ontology. CodeLore
should generalize toward repo-agnostic concepts:

- artifact class
- code surface
- behavioral change
- evidence source
- change consequence

### 5. Batch logging becomes provenance and event logging

The log discipline in `gt-wiki` is useful, but CodeLore should generalize it
into system provenance:

- what inputs were read
- which window was built
- which links were explicit vs heuristic
- which claims were generated
- which claims were rejected or left unresolved

## Replace

These elements are important in `gt-wiki`, but they should be replaced rather
than carried forward.

### 1. Wiki pages as the primary output

Replace with:

- evidence pack as the primary machine-readable artifact
- compiled summary as a downstream output
- queryable graph / structured store for retrieval

### 2. Obsidian-shaped file structure

Replace with product-shaped storage and interfaces:

- domain models
- ingestion pipelines
- evidence storage
- graph storage
- query/export layers

### 3. Human-readable section schema as the internal model

Replace page sections such as "What it actually does," "Docs claim," and
"Drift" with typed objects and relations:

- claims
- evidence
- warrants
- contradictions
- unresolved questions

### 4. Project-local agent skills as the execution surface

Replace with a product interface:

- CLI commands
- programmatic pipeline boundaries
- structured export formats

The logic in the skills remains valuable, but the product should not depend on
Claude-specific instruction files as its runtime interface.

### 5. `gastown`-specific assumptions

Replace with configurable project adapters and schemas where necessary. The
first prototype may be evaluated on `gastown`, but the product should not carry
its vocabulary or workflow structure as global defaults.

## Product Shape

This section states the desired CodeLore operating model directly, rather than
describing it mainly through exclusions.

### 1. Primary product artifact: evidence pack

CodeLore should produce a bounded evidence pack for a change window as its
primary artifact. The evidence pack should contain:

- window metadata
- artifact inventory
- claims
- evidence links
- warrants
- contradictions
- unresolved questions

Readable summaries may be compiled from the evidence pack, but they are
downstream products rather than the system's core representation.

### 2. Primary product unit: change window

CodeLore should organize project memory around bounded historical windows. A
window may eventually be:

- a release
- a commit range
- a date range

The important design rule is that project knowledge remains anchored to a
specific historical slice.

### 3. Primary success measure: trustworthy reconstruction

CodeLore should be evaluated by whether it reconstructs project evolution in a
traceable and queryable way. Core quality signals are:

- claim traceability
- evidence quality
- correct abstention under weak support
- useful historical retrieval

Completeness of prose output is not the main success metric.

### 4. Primary runtime surface: product interfaces

CodeLore should run through product-shaped interfaces such as:

- CLI commands
- programmatic pipeline boundaries
- structured export formats

The prototype skills remain useful source material, but they are not the
product runtime model.

### 5. Primary portability rule: repo-agnostic core

CodeLore should assume incomplete metadata by default. Its core should work on
top of bounded project evidence even when:

- release notes are weak
- GitHub linkage is partial
- discussion metadata is sparse

Clean repo metadata is an accelerator, not a prerequisite.

## Historical Material To Leave Behind

Some elements of `gt-wiki` remain valuable as prototype history, but they
should not shape CodeLore's core architecture.

### 1. Wiki-phase execution structure

The Phase 2 / Phase 3 discipline is useful as historical process context, but
CodeLore should define its own product phases around ingestion, evidence,
claims, and retrieval.

### 2. Vault-specific operating conventions

Obsidian-specific structure, task handling conventions, and wiki schema
operations belong to the prototype environment rather than the generalized
product.

### 3. Page-coverage orientation

Per-page completeness is useful for a wiki workflow, but CodeLore should focus
on bounded historical reconstruction and evidence quality.

## Boundary Statement

`gt-wiki` should be treated as:

- a prototype workflow
- a corpus of outputs
- an evaluation fixture
- a source of process insights

CodeLore should be treated as:

- the standalone product
- the canonical domain model
- the bounded evidence and claim system
- the long-term retrieval and memory framework

## Immediate Implications For MVP

1. The first MVP should build a bounded evidence pack for one release window.
2. The first MVP should treat readable summaries as derived output.
3. The first MVP should prefer abstention over unsupported explanation.
4. The first MVP should prove that structured project memory is more useful than
   a changelog or summary page for at least a few important historical
   questions.
