# CodeLore Glossary

## Purpose

CodeLore's documentation deliberately mixes two genres: evidence-and-ontology
modeling and data engineering. Each audience needs the other's vocabulary, and
some words carry different meanings in each genre. This glossary defines terms
as CodeLore uses them and disambiguates the terms that have two lives.

This glossary is hand-curated and governs the working vocabulary of the docs.
It complements the generated ontology reference planned in Phase 4 of the
development plan, which documents the operational taxonomy (claim types,
warrant types, artifact classes) directly from the implemented models.

Like the ontology itself, this glossary is open-world: it starts small and
grows as terms earn their place.

Writing convention for all CodeLore docs: the first use of a genre-specific
term in a document carries a brief inline gloss; this glossary holds the
durable definition. Neither audience should need the other's background to
read any single document.

## Terms With Two Meanings

### policy

- In evidence and ontology contexts: an epistemic governance rule about what
  CodeLore may assert and when — the evidence policy
  (`docs/evidence/02-evidence-policy.md`) and canonicalization policy
  (`docs/architecture/03-identity-and-canonicalization.md`).
- In engineering contexts: a build-and-run constraint on how the pipeline
  operates — the cross-cutting policies in the development plan
  (replayability, testing, pipeline shape).
- When context is not obvious, qualify: "evidence policy" versus "build
  policy."

### model

- In engineering contexts: the pydantic domain models in `models.py`, or the
  data model generally.
- In generation contexts: a language model. The development plan's "zero model
  calls" uses this sense.
- Where both senses could apply, qualify: "domain model" versus "language
  model."

### schema

- The operational schema: the typed record vocabulary in
  `docs/architecture/04-schema.md` — an ontology and data-model commitment.
- A validation schema: the pydantic contract a record must satisfy at a stage
  boundary — an engineering contract.
- Later, an OWL schema: the planned formal export of the ontology.

### validation

- Data validation: deterministic checking of generated records — spans exist,
  quotes match, minimum support is met. An engineering mechanism.
- Hostile validation: empirical evaluation of the whole system on an
  unfavorable corpus (`llama.cpp`). A scientific act.
- Schema validation: pydantic boundary checking (see schema).

### canonical / canonicalization

- In data engineering, canonicalization usually means normalizing values to a
  standard form.
- In CodeLore it means something stronger: an evidence-backed
  identity-resolution decision that window-scoped observations refer to the
  same enduring thing. It is never a name-matching shortcut. See
  `docs/architecture/03-identity-and-canonicalization.md`.
- Value standardization in the data-engineering sense happens in the normalize
  pipeline stage and is called normalization, not canonicalization.

### graph

- Graph semantics: the typed vocabulary of entities and relationships —
  product core, storage-neutral, carried by the pack schema.
- Graph infrastructure: a storage and traversal engine (currently Neo4j) —
  replaceable.

### observation

- In CodeLore's ontology: a window-scoped record of how an entity appeared
  within one `ChangeWindow` (e.g. `ModuleObservation`), deliberately distinct
  from the canonical entity it may later be resolved to.
- Not the colloquial "something we noticed": that is closer to a `Finding`.

## Historical And Ontological Modeling

- **ChangeWindow** — the canonical unit of historical reconstruction: a
  bounded slice of project history (release, commit range, or date range).
  Every claim, observation, and abstention is scoped to a window.
- **Release** — an artifact and one kind of window boundary; not the core
  model.
- **Window-scoped** — true of one window only; never silently flattened into a
  timeless current-state fact.
- **Canonical entity** — a thin identity node representing an enduring thing
  across windows (e.g. `Module`).
- **Lineage** — continuity of a referent across windows, including splits,
  merges, and reappearances.
- **Label versus referent** — a recurring name is weak evidence of a recurring
  thing; `REUSES_LABEL` records name reuse without asserting identity.
- **IdentityResolution** — the recorded decision artifact of a
  canonicalization judgment, with evidence scores and an explicit outcome.
- **Open-world assumption** — the absence of a statement means unknown, not
  false. CodeLore never treats missing evidence as evidence of absence.
- **Admission criteria** — a category becomes first-class ontology only with
  distinct construction rules, distinct query value, and distinct failure
  modes.
- **Defeasible** — held revisable; any claim or identity decision can be
  contested by later counterevidence.

## Evidence And Reasoning

- **ArtifactRecord** — the normalized record of a source object (commit, PR,
  issue, diff, release note) with a locator and provenance.
- **Evidence** — an extracted supporting fragment (text span, diff hunk,
  structural relation) drawn from an ArtifactRecord.
- **Claim** — a typed, window-scoped proposition carrying evidence references,
  warrants, confidence, and status.
- **Warrant** — the explicit, typed rule explaining why cited evidence
  supports a claim; the term comes from Toulmin's model of argument. A warrant
  is not extra evidence and is not itself the claim. It is the reasoning bridge:
  evidence plus warrant supports, contests, or fails to support a claim.
- **Confidence** — a reflection of evidence quality (`high`, `medium`, `low`),
  never of a language model's self-assurance.
- **Contradiction** — a preserved conflict between evidence; conflicts are
  recorded, not resolved away.
- **Abstention** — a structured declaration that the evidentiary bar was not
  met. It is completed analysis that names what is missing; it governs what
  CodeLore asserts, not whether work is attempted.
- **Why ladder** — the admission order for "why" content: explicit, inferred
  under a typed rule, candidate (below threshold, labeled), rich abstention.
- **Evidence pack** — the assembled, source-of-truth output for one window:
  artifacts, evidence, claims, warrants, contradictions, abstentions, open
  questions.
- **Dossier** — the human-readable rendering derived from a pack; every
  sentence traces back to claims.
- **Golden question set** — hand-verified concrete acceptance questions with
  expected supporting artifacts; the disconfirmation baseline for every later
  phase.

## Pipeline And Engineering

- **Automated reasoning** — machine-performed logical inference: theorem
  proving, SAT/SMT solving, model checking, description-logic reasoners. In
  CodeLore it appears in small, deliberate doses — the V-rule validator as a
  decision procedure, the OWL reasoner consistency check — never as
  theorem-proving machinery.
- **High assurance** — the engineering goal of justified confidence in a
  system's stated guarantees, achieved by specification, invariants, testing,
  and automated reasoning where it pays. Related but not equivalent to
  automated reasoning: one is the goal, the other a technique family.
- **Stage** — a named transformation (acquire, window, normalize, extract,
  reason, assemble, present, project) with declared inputs and outputs,
  validated at its boundary.
- **Materialized intermediate** — a stage output written to disk so it can be
  inspected, tested, and audited.
- **Snapshot** — an immutable on-disk capture of external input: forge API
  responses, language-model outputs.
- **Replay** — rebuilding a window from snapshots without new external calls;
  replays are deterministic and produce identical identifiers.
- **Run manifest** — the per-run process record: code version, input
  checksums, per-stage input/output/dropped counts, model invocations,
  timestamps.
- **Generator** — a component that proposes claims or definitions, rule-based
  or model-based.
- **Validator** — the deterministic checker behind every generator; failures
  become drops or abstentions, never claims.
- **Provenance** — the recorded origin and mechanism of every record,
  including which run and stage produced it.
- **Stable identifier** — a deterministic ID, identical across replays,
  designed to be usable as an IRI.
- **Forge** — the code-hosting service (GitHub) supplying PRs, issues, and
  release metadata.
- **Fixture repository** — the small synthetic git repo in `tests/` used for
  deterministic unit tests.

## Interop And Formats

- **Property graph** — the labeled-nodes-and-edges-with-properties model used
  by Neo4j.
- **RDF** — the W3C triple-based data model; the planned export format for
  pack data.
- **RDF 1.2 named reifier** — CodeLore's accepted RDF export pattern for
  statement metadata: a stable CodeLore resource reifies a triple term with
  `rdf:reifies` and carries evidence, warrant, confidence, and provenance
  links. Classic RDF 1.1 reification is only a compatibility export.
- **SKOS** — the W3C vocabulary standard for taxonomies and glossaries; the
  planned export format for CodeLore's taxonomy and glossary.
- **OWL** — the W3C ontology language; the planned export format for the
  ontology schema.
- **IRI** — the global identifier form used by RDF and OWL; CodeLore's stable
  identifiers are designed to map to IRIs.
