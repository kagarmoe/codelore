# CodeLore Concrete Schema Draft

## Purpose

This document translates the product-definition model into a concrete graph
schema draft suitable for early implementation.

It is intentionally opinionated enough to guide implementation, while still
leaving room for refinement after the first slices.

## Ontology Discipline

A category becomes first-class only when it has:

- distinct construction rules
- distinct query value
- distinct failure modes

Useful labels are not automatically useful entities.

## Schema Rule

CodeLore stores one project memory system as:

- thin canonical identities
- window-scoped observations
- normalized artifact records
- reasoning nodes
- explicit temporal and evidentiary links
- explicit identity-resolution decisions

## 1. Scope Model

### Canonical scope

Canonical nodes represent enduring identities across time.

Required property:

- `scope_type = "canonical"`

### Window scope

Window-scoped nodes represent observations, artifacts, and reasoning bound to a
specific `ChangeWindow`.

Required properties:

- `scope_type = "window"`

### Membership rule

Do not rely on a single `window_id` property as the only representation of
window membership. Use explicit membership edges so an artifact can later
participate in multiple windows or views.

Optional convenience properties such as `primary_window_id` may exist, but the
graph meaning should live in edges.

### Artifact identity across windows

The same artifact may participate in more than one window.

Default rule:

- one artifact node may link to many windows
- window membership is relational, not identity-defining

This applies especially to:

- `Commit`
- `PullRequest`
- `Issue`
- `Comment`
- `ADR`

If a later implementation needs per-window projections of artifacts, that
should be added explicitly rather than implied by `scope_type`.

## 2. Node Labels

### A. Core Window Nodes

#### `Project`

Required:

- `project_id`
- `name`
- `repo_url`

Optional:

- `default_branch`
- `hosting_provider`

#### `ChangeWindow`

Required:

- `window_id`
- `window_type`
- `label`

Optional:

- `start_ref`
- `end_ref`
- `start_time`
- `end_time`
- `build_status`

### B. Canonical Identity Nodes

#### `Module`

Required:

- `module_id`
- `canonical_name`
- `scope_type = "canonical"`

Optional:

- `primary_path`
- `identity_confidence`

#### `Symbol`

Required:

- `symbol_id`
- `canonical_name`
- `scope_type = "canonical"`

Optional:

- `symbol_kind`
- `language`
- `identity_confidence`

#### `Concept`

Required:

- `concept_id`
- `canonical_name`
- `scope_type = "canonical"`

Optional:

- `definition`
- `identity_confidence`

Status:

- deferred canonical ontology unless later implementation proves stable concept
  identity rules

#### `ProblemClass`

Required:

- `problem_class_id`
- `canonical_name`
- `scope_type = "canonical"`

Optional:

- `problem_family`
- `identity_confidence`

Status:

- deferred canonical ontology outside later non-MVP identity work

#### `DecisionTheme`

Required:

- `decision_theme_id`
- `canonical_name`
- `scope_type = "canonical"`

Optional:

- `theme_description`
- `identity_confidence`

Status:

- deferred canonical ontology outside later non-MVP identity work

### C. Observation Nodes

Observation nodes represent historically bounded state and should carry more
operational meaning than canonical nodes.

#### `ModuleObservation`

Required:

- `observation_id`
- `scope_type = "window"`

Optional:

- `observed_name`
- `path`
- `change_kind`
- `summary`
- `source_artifact_count`
- `extracted_by`
- `extraction_method`
- `observed_at`
- `status`

#### `SymbolObservation`

Required:

- `observation_id`
- `scope_type = "window"`

Optional:

- `observed_name`
- `symbol_kind`
- `file_path`
- `signature`
- `change_kind`
- `source_artifact_count`
- `extracted_by`
- `extraction_method`
- `observed_at`
- `status`

#### `ConceptObservation`

Required:

- `observation_id`
- `scope_type = "window"`

Optional:

- `observed_name`
- `summary`
- `change_kind`
- `source_artifact_count`
- `extracted_by`
- `extraction_method`
- `observed_at`
- `status`

#### `ProblemObservation`

Required:

- `observation_id`
- `scope_type = "window"`

Optional:

- `problem_kind`
- `statement`
- `status_hint`
- `source_artifact_count`
- `extracted_by`
- `extraction_method`
- `observed_at`
- `status`

#### `DecisionObservation`

Required:

- `observation_id`
- `scope_type = "window"`

Optional:

- `statement`
- `decision_kind`
- `status_hint`
- `source_artifact_count`
- `extracted_by`
- `extraction_method`
- `observed_at`
- `status`

### D. Artifact Nodes

#### `ArtifactRecord`

Required:

- `artifact_record_id`
- `scope_type = "window"`
- `artifact_type`
- `locator_type`
- `source_locator`

Optional:

- `source_system`
- `native_id`
- `captured_at`
- `normalized_by`
- `checksum`

Recommended `locator_type` values:

- `git_commit`
- `git_commit_message`
- `diff_hunk`
- `pr_body`
- `issue_body`
- `comment_body`
- `markdown_section`
- `adr_section`
- `release_note_section`

#### `Release`

Required:

- `release_id`
- `scope_type = "window"`
- `tag_name`

Optional:

- `release_name`
- `published_at`
- `source`

#### `Commit`

Required:

- `commit_id`
- `scope_type = "window"`
- `sha`

Optional:

- `author`
- `committed_at`
- `message`

#### `PullRequest`

Required:

- `pr_id`
- `scope_type = "window"`
- `number`

Optional:

- `title`
- `state`
- `created_at`
- `merged_at`
- `base_ref`
- `head_ref`

#### `Issue`

Required:

- `issue_id`
- `scope_type = "window"`
- `number`

Optional:

- `title`
- `state`
- `created_at`
- `closed_at`

#### `Diff`

Required:

- `diff_id`
- `scope_type = "window"`

Optional:

- `path`
- `change_kind`
- `additions`
- `deletions`

#### `Comment`

Required:

- `comment_id`
- `scope_type = "window"`

Optional:

- `author`
- `created_at`
- `body`
- `comment_context`

#### `DocChange`

Required:

- `doc_change_id`
- `scope_type = "window"`

Optional:

- `path`
- `change_kind`

#### `TestChange`

Required:

- `test_change_id`
- `scope_type = "window"`

Optional:

- `path`
- `change_kind`
- `test_framework`

#### `ADR`

Required:

- `adr_id`
- `scope_type = "window"`

Optional:

- `title`
- `path`
- `status`

#### `ReleaseNote`

Required:

- `release_note_id`
- `scope_type = "window"`

Optional:

- `source_type`
- `title`
- `published_at`

### E. Reasoning Nodes

These nodes are not all peer ontology with artifacts and observations. Some are
best understood as analysis-state or output-structure nodes.

#### `Claim`

Required:

- `claim_id`
- `scope_type = "window"`
- `claim_type`
- `statement`
- `status`
- `confidence`

Optional:

- `subject_kind`
- `claim_priority`

#### `Evidence`

Required:

- `evidence_id`
- `scope_type = "window"`
- `evidence_type`

Optional:

- `source_ref`
- `span_start`
- `span_end`
- `excerpt`
- `capture_method`
- `evidence_role`

Interpretation rule:

- `ArtifactRecord` is the normalized source object
- `Evidence` is the extracted supporting fragment, citation, or reference drawn
  from that source object

#### `Warrant`

Required:

- `warrant_id`
- `scope_type = "window"`
- `warrant_type`
- `rule_name`
- `rule_text`

Optional:

- `limitations`

#### `Finding`

Required:

- `finding_id`
- `scope_type = "window"`
- `finding_type`

Optional:

- `summary`

Interpretation:

- analysis-state or compiled output node unless later graph-native use justifies
  stronger ontology

#### `Contradiction`

Required:

- `contradiction_id`
- `scope_type = "window"`

Optional:

- `summary`
- `severity`

#### `Abstention`

Required:

- `abstention_id`
- `scope_type = "window"`
- `reason_code`

Optional:

- `summary`

Interpretation:

- analysis-state node describing why a claim was not advanced

#### `OpenQuestion`

Required:

- `question_id`
- `scope_type = "window"`
- `question_text`

Optional:

- `question_type`
- `priority`

Interpretation:

- output-structure or investigation-state node unless later implementation
  proves separate graph-native query value

#### `Summary`

Required:

- `summary_id`
- `scope_type = "window"`
- `summary_type`

Optional:

- `text`
- `generated_by`

#### `IdentityResolution`

Required:

- `decision_id`
- `scope_type = "window"`
- `entity_type`
- `decision_outcome`
- `confidence`
- `method`

Optional:

- `timestamp`
- `summary`
- `explicit_score`
- `structural_score`
- `behavioral_score`
- `lexical_score`
- `counterevidence_score`

## 3. Edge Labels

### Scope and membership edges

- `Project HAS_WINDOW ChangeWindow`
- `ChangeWindow HAS_BOUNDARY Release`
- `ChangeWindow NATIVE_TO_WINDOW ArtifactRecord`
- `ChangeWindow NATIVE_TO_WINDOW Commit`
- `ChangeWindow NATIVE_TO_WINDOW PullRequest`
- `ChangeWindow NATIVE_TO_WINDOW Issue`
- `ChangeWindow NATIVE_TO_WINDOW Diff`
- `ChangeWindow NATIVE_TO_WINDOW Comment`
- `ChangeWindow NATIVE_TO_WINDOW DocChange`
- `ChangeWindow NATIVE_TO_WINDOW TestChange`
- `ChangeWindow NATIVE_TO_WINDOW ADR`
- `ChangeWindow LINKED_TO_WINDOW ArtifactRecord`
- `ChangeWindow LINKED_TO_WINDOW Commit`
- `ChangeWindow LINKED_TO_WINDOW PullRequest`
- `ChangeWindow LINKED_TO_WINDOW Issue`
- `ChangeWindow LINKED_TO_WINDOW Diff`
- `ChangeWindow LINKED_TO_WINDOW Comment`
- `ChangeWindow LINKED_TO_WINDOW DocChange`
- `ChangeWindow LINKED_TO_WINDOW TestChange`
- `ChangeWindow LINKED_TO_WINDOW ADR`
- `ChangeWindow HAS_CLAIM Claim`
- `ChangeWindow HAS_FINDING Finding`
- `ChangeWindow HAS_SUMMARY Summary`

### Canonicalization edges

`OBSERVES` is provisional unless backed by at least one positive
`IdentityResolution`.

Trusted query paths should ignore unresolved canonical links by default.

- `ModuleObservation OBSERVES Module`
- `SymbolObservation OBSERVES Symbol`
- `ConceptObservation OBSERVES Concept`
- `ProblemObservation OBSERVES ProblemClass`
- `DecisionObservation OBSERVES DecisionTheme`

### Uncertainty and lineage edges

- `ModuleObservation POSSIBLY_SAME_AS ModuleObservation`
- `SymbolObservation POSSIBLY_SAME_AS SymbolObservation`
- `ConceptObservation POSSIBLY_SAME_AS ConceptObservation`
- `ProblemObservation POSSIBLY_SAME_AS ProblemObservation`
- `DecisionObservation POSSIBLY_SAME_AS DecisionObservation`
- `ConceptObservation REUSES_LABEL ConceptObservation`
- `ProblemObservation REUSES_LABEL ProblemObservation`
- `DecisionObservation REUSES_LABEL DecisionObservation`
- `ModuleObservation DERIVES_FROM ModuleObservation`
- `SymbolObservation DERIVES_FROM SymbolObservation`
- `ConceptObservation DERIVES_FROM ConceptObservation`
- `ProblemObservation DERIVES_FROM ProblemObservation`
- `DecisionObservation DERIVES_FROM DecisionObservation`
- `ModuleObservation SPLITS_INTO ModuleObservation`
- `ModuleObservation MERGES_INTO ModuleObservation`

### Identity resolution edges

- `IdentityResolution EVALUATES ModuleObservation`
- `IdentityResolution EVALUATES SymbolObservation`
- `IdentityResolution EVALUATES ConceptObservation`
- `IdentityResolution EVALUATES ProblemObservation`
- `IdentityResolution EVALUATES DecisionObservation`
- `IdentityResolution SUPPORTS Module`
- `IdentityResolution SUPPORTS Symbol`
- `IdentityResolution SUPPORTS Concept`
- `IdentityResolution SUPPORTS ProblemClass`
- `IdentityResolution SUPPORTS DecisionTheme`
- `IdentityResolution SUPPORTED_BY Evidence`
- `IdentityResolution JUSTIFIED_BY Warrant`

### Artifact relationship edges

- `PullRequest IMPLEMENTED_BY Commit`
- `Issue RELATED_TO PullRequest`
- `Issue RELATED_TO Commit`
- `Diff MODIFIES ModuleObservation`
- `Diff MODIFIES SymbolObservation`
- `Commit TOUCHES ModuleObservation`
- `Commit TOUCHES SymbolObservation`
- `Commit INCLUDES Diff`
- `ADR RECORDS DecisionObservation`
- `Comment DISCUSSES ProblemObservation`
- `Comment DISCUSSES DecisionObservation`
- `ReleaseNote DESCRIBES Claim`
- `TestChange SUPPORTS Claim`
- `DocChange SUPPORTS Claim`
- `Evidence EXTRACTED_FROM ArtifactRecord`

`RELATED_TO` is a staging edge for early ingestion only.

It should later be replaced or refined by narrower link families such as:

- `REFERENCES`
- `CLOSES`
- `IMPLEMENTS`
- `MENTIONS`

### Reasoning edges

- `Claim SUPPORTED_BY Evidence`
- `Claim JUSTIFIED_BY Warrant`
- `Claim CONTRADICTED_BY Evidence`
- `Claim ABOUT ModuleObservation`
- `Claim ABOUT SymbolObservation`
- `Claim ABOUT ProblemObservation`
- `Claim ABOUT DecisionObservation`
- `Finding INCLUDES Claim`
- `Contradiction INVOLVES Claim`
- `Abstention ABOUT ProblemObservation`
- `Abstention ABOUT Claim`
- `OpenQuestion ABOUT Claim`
- `Summary DERIVES_FROM Claim`
- `Warrant USES Evidence`

### Temporal and cross-window edges

- `ChangeWindow PRECEDES ChangeWindow`
- `ModuleObservation FOLLOWS ModuleObservation`
- `ConceptObservation EVOLVES_TO ConceptObservation`
- `DecisionObservation SUPERSEDES DecisionObservation`
- `ProblemObservation REVISITS ProblemObservation`
- `ProblemObservation RESOLVED_IN ChangeWindow`
- `Claim REVISED_BY Claim`

## 4. Edge Properties

All inferred, heuristic, or explicit edges should support:

- `link_method`
- `confidence`
- `created_by`
- `created_at`
- `membership_type`
- `time_relation`

Recommended `link_method` values:

- `explicit`
- `structural`
- `heuristic`
- `inferred`

Recommended `membership_type` values:

- `native`
- `linked`
- `inferred`

Rule:

- use `NATIVE_TO_WINDOW` and `LINKED_TO_WINDOW` as the primary semantic carrier
- use `membership_type` only as a refinement

Recommended `time_relation` values:

- `within`
- `precedes`
- `follows`
- `overlaps`

Recommended `decision_outcome` values for `IdentityResolution`:

- `same_identity`
- `likely_same`
- `uncertain`
- `likely_different`
- `different_identity`

Recommended `evidence_role` values:

- `direct`
- `corroborating`
- `contradictory`

## 5. Identity and Observation Rule

### Rule

Canonical nodes hold enduring identity.

Observation nodes hold historically bounded state.

Claims and evidence should usually attach to observations, not directly to the
canonical node.

Identity-resolution decisions should be recorded explicitly through
`IdentityResolution` nodes rather than hidden inside bare canonicalization
edges.

`OBSERVES` may exist before final resolution, but in that case it should carry
an unresolved state and must not be treated as trusted identity by default.

### Example

- canonical: `Module("scheduler")`
- observation: `ModuleObservation("scheduler@v1.1.0..v1.2.0")`
- claim: “scheduler guards skip closed beads”

Preferred link pattern:

- `ModuleObservation OBSERVES Module`
- `Claim ABOUT ModuleObservation`
- `Claim SUPPORTED_BY Evidence`

## 6. MVP Schema Subset

Operationalize first:

- `Project`
- `ChangeWindow`
- `Release`
- `ArtifactRecord`
- `Commit`
- `PullRequest`
- `Issue`
- `Diff`
- `Claim`
- `Evidence`
- `Warrant`
- `Finding`
- `Abstention`
- `OpenQuestion`

Observation nodes can start with:

- `ModuleObservation`
- `ProblemObservation`
- `DecisionObservation`

Canonical nodes can start with:

- `Module`

Identity resolution in MVP should be limited to:

- `ModuleObservation`
- `Module`
- `IdentityResolution`

`TimelineEvent` can be approximated initially by ordered windows and artifact
timestamps.

### Deferred canonicalization in MVP

The following may exist in the broader schema, but should not be treated as
first-slice canonicalization commitments:

- `ProblemObservation OBSERVES ProblemClass`
- `DecisionObservation OBSERVES DecisionTheme`
- `ConceptObservation OBSERVES Concept`
- non-module lineage and reidentification workflows

## 7. Deferred Schema Areas

Defer until after the first slice unless clearly justified:

- full symbol graph
- broad concept graph
- cross-repo graph
- dense architecture graph
- aggressive inferred-problem expansion
- canonical `ProblemClass`
- canonical `DecisionTheme`
- non-trivial `IdentityResolution` for anything beyond `Module`
- canonical `Concept`

## 8. Mapping To Product-Definition Terms

This schema draft uses a few narrower implementation names than the product
definition.

- product `Problem` -> schema `ProblemObservation` and later `ProblemClass`
- product `Decision` -> schema `DecisionObservation` and later `DecisionTheme`
- product `UnresolvedQuestion` -> schema `OpenQuestion`
- product `Observation` -> schema `ModuleObservation`, `ProblemObservation`,
  `DecisionObservation`, `SymbolObservation`, `ConceptObservation`
- product raw artifact source -> schema `ArtifactRecord`
