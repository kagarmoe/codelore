# `llama.cpp` Validation Plan For CodeLore

## Purpose

This document defines how `llama.cpp` should be used as the first hostile
validation corpus after the initial `gastown` MVP slice.

Location:

- repo: `/home/kimberly/repos/llama.cpp`

This validation follows the first end-to-end implementation target. It is the
first serious test of whether CodeLore generalizes beyond a favorable,
release-structured corpus.

## Why `llama.cpp` Matters

`gastown` is useful for proving that the pipeline works at all. `llama.cpp`
extends that validation toward product generality.

`llama.cpp` is valuable because it is likely to pressure the design in ways
that `gastown` does not:

- faster and noisier change flow
- weaker dependence on neat release-centered narratives
- more pressure toward continuous-delivery interpretation
- more uneven issue / PR / commit linkage
- more cases where "what changed" is easier to recover than "why it changed"

That makes it a better test of whether CodeLore is genuinely constructing
project memory or merely exploiting a repo with good metadata.

## Validation Goals

The `llama.cpp` validation pass should answer these questions:

1. Can CodeLore still build useful evidence packs when release metadata is less
   central?
2. Does the MVP abstain correctly when "why" evidence is sparse?
3. Does the claim model remain useful when GitHub linkage is incomplete?
4. Are the current artifact classes sufficient for a CD-style repo?
5. Does graph-style retrieval add value beyond filtered document retrieval?

## Validation Position In The Roadmap

`llama.cpp` should be used only after:

1. the `gastown v1.1.0 -> v1.2.0` release slice works end to end
2. the evidence policy has been exercised on real output
3. the MVP claim taxonomy has survived at least one review pass

It should occur before:

1. public claims of broad repo generality
2. expansion of claim types
3. support for arbitrary date windows in the public interface

## Recommended Window Strategy

Because `llama.cpp` is intended as a hostile validation case, use more than one
window shape conceptually, but introduce them in order.

### Phase A: Release-aligned validation if usable

If the repo has usable tagged releases with enough supporting context, first try
one bounded release-style window. This gives a comparison point against the
`gastown` slice while changing the repo characteristics.

### Phase B: Monthly date-range validation

Then test a calendar-month `date_range` window as the first CD-style view.

Reason:

- it is bounded
- it is reproducible
- it avoids arbitrary cherry-picked ranges
- it provides a realistic default for continuous-delivery projects

### Phase C: Arbitrary date-range spot check

Only after monthly windows behave reasonably should CodeLore test arbitrary date
windows on demand.

## Questions The Validation Should Be Able To Ask

These questions should be tested explicitly:

1. What changed during this month or window?
2. Which commits and changed files support that answer?
3. Which issues or PRs can be linked confidently, and which should remain
   unresolved?
4. Which problem statements are explicit versus absent?
5. Where does CodeLore abstain on "why" because the evidence is too weak?

## Expected Stress Areas

### 1. Sparse or noisy rationale

The system may find many change facts and few trustworthy problem or decision
claims.

Desired behavior:

- preserve useful structure
- abstain on unsupported explanation
- keep rationale absent or unresolved when support is weak

### 2. Incomplete GitHub linkage

The system may not be able to map issues, PRs, and commits as cleanly as in a
favorable repo.

Desired behavior:

- downgrade confidence
- preserve unresolved linkage
- still answer what changed from git-native evidence

### 3. High-volume windows

Date windows may be much larger or more heterogeneous than a carefully bounded
release.

Desired behavior:

- avoid collapsing too much change into shallow summary
- preserve artifact counts and unresolved complexity
- show when the evidence pack is broad and heterogeneous

### 4. Retrieval-mode mismatch

This validation should reveal whether graph traversal is truly helping or
whether simpler filtering over structured artifacts answers the main questions
just as well.

Desired behavior:

- compare graph-style retrieval against simpler structured retrieval

## Evaluation Criteria

### 1. Utility under weak metadata

The evidence pack should still answer "what changed" and "what supports that"
even when "why" is incomplete.

### 2. Abstention quality

The system should refuse unsupported causal or motivational explanations rather
than inventing them.

### 3. Link precision

When the system claims artifact relationships, sampled links should hold up
under inspection.

### 4. Retrieval value

For at least a few test questions, CodeLore should provide better historical
navigation than:

- changelog reading alone
- commit log alone
- raw code search alone

### 5. Failure visibility

Weaknesses should be explicit in the output:

- missing links
- contested claims
- unsupported "why"
- over-broad windows

## Validation Signals

The `llama.cpp` validation should be read through the following signals:

1. Whether CodeLore remains useful when GitHub metadata is sparse.
2. Whether the system preserves evidence quality under weaker rationale.
3. Whether monthly windows remain traceable at higher change volume.
4. Whether graph machinery improves retrieval quality enough to justify itself.
5. Whether the product preserves a clear distinction between supported,
   unresolved, and abstained outputs.

## Likely Outcomes And What They Mean

### Outcome A: Works well enough

Meaning:

- the MVP model is on the right track
- date-window support is worth implementing after release windows

### Outcome B: Good on change facts, weak on rationale

Meaning:

- the git-first core is solid
- the "why" layer needs stricter limits and better abstention defaults

### Outcome C: Weak even on basic traceability

Meaning:

- the ingestion/linkage model is too dependent on favorable metadata
- product generality still needs more validation

### Outcome D: Graph adds little value

Meaning:

- keep graph semantics in the conceptual model
- reconsider how much graph infrastructure belongs in the early product

## Recommended Deliverable

After running the `llama.cpp` validation, produce a short validation memo with:

- window used
- artifact counts
- claim counts by type
- abstention counts
- sampled good answers
- sampled weak spots
- whether graph retrieval outperformed simpler retrieval
- recommended changes to the model

## Decision Rule

Use `llama.cpp` to discover where the current model remains strong, where it
becomes uncertain, and where the roadmap needs tightening.

If the validation shows that CodeLore currently performs best on cleaner
release-oriented repos, treat that as a product-boundary discovery and fold it
back into the roadmap.
