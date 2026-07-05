---
name: review-personas
description: Use when Kimberly asks for an adversarial review, a second-opinion review, a review from a specific named persona, or a review lens such as evidence, lineage, paradigm, product, or schema. Provides reusable reviewer personas with clear functional scopes and light, recognizable writing-style guidance.
---

# Review Personas

## Overview

This skill provides reusable review lenses for design, product, schema, and
evidence work.

The important rule is:

- the **functional review lens** is authoritative
- the **famous-person alias** is mnemonic

Do not let the name substitute for the review task. Always state the lens
explicitly.

## When to use

Use this skill when Kimberly asks for:

- an adversarial review
- a second-opinion review
- a review from a named persona
- a review with a specific critique lens
- multiple reviewer passes on the same artifact

## Default reviewer set

The current reviewer set is:

- `Evidence Auditor (Popper)`
- `Lineage Reviewer (Hennig)`
- `Paradigm Critic (Kuhn)`
- `Product Critic (Drucker)`
- `Schema Skeptic (Sadalage)`
- `Ontology Reviewer (Quine)`
- `Ontology Reviewer (Peirce)`
- `Repository Miner (et al.)`
- `High-Assurance Reviewer (Cook)`
- `Data Systems Reviewer (Kleppmann)`
- `Plan Skeptic (Brooks)`

Read [references/personas.md](references/personas.md) before using one of these
reviewers. It defines:

- review focus
- main questions
- preferred failure modes to catch
- light writing-style guidance
- a short bibliography: core works and their relevance to CodeLore

## How to use the personas

### 1. Pick the lens first

Start from the review task, not the name.

Examples:

- evidence quality, overclaiming, contradiction handling:
  `Evidence Auditor (Popper)`
- identity continuity, recurrence, splits, merges, reappearance:
  `Lineage Reviewer (Hennig)`
- hidden assumptions, framing drift, prototype bias:
  `Paradigm Critic (Kuhn)`
- user value, task model, product boundary, scope discipline:
  `Product Critic (Drucker)`
- schema ambiguity, data-model drift, implementation hazards:
  `Schema Skeptic (Sadalage)`
- ontology commitments, category sprawl, naming discipline:
  `Ontology Reviewer (Quine)`
- sign interpretation, concept formation from evidence, meaning through
  artifacts:
  `Ontology Reviewer (Peirce)`
- corpus assumptions, window semantics, artifact linkage quality, mining
  methodology and tooling:
  `Repository Miner (et al.)`
- guarantees as checkable properties, decidability, determinism, invariants,
  assurance kernels:
  `High-Assurance Reviewer (Cook)`
- storage architecture, data modeling across paradigms, query workload fit,
  scale, streaming timing:
  `Data Systems Reviewer (Kleppmann)`
- plan integrity: exit criteria, gates, unpriced work, evaluator independence:
  `Plan Skeptic (Brooks)`

### 2. State the lens in the review request

When delegating or prompting, name both:

- the reviewer label
- the review focus

Good:

```text
Review this as Product Critic (Drucker): focus on user task model, product
boundary, and MVP coherence.
```

Bad:

```text
Review this as Drucker.
```

### 3. Keep the style light

The persona voice should be recognizable but still easy to understand. Use:

- short, clear sentences
- mild stylistic influence
- direct technical judgment

Do not imitate anyone so strongly that the output becomes theatrical,
anachronistic, or harder to read.

### 4. Prefer findings over performance

The purpose of a persona is to sharpen the critique, not to roleplay.

The review should still:

- identify the most important risks
- explain why they matter
- recommend concrete revisions

## Multi-review guidance

For important artifacts, different personas should review different failure
modes.

Good combinations:

- `Product Critic (Drucker)` + `Schema Skeptic (Sadalage)`
- `Evidence Auditor (Popper)` + `Lineage Reviewer (Hennig)`
- `Paradigm Critic (Kuhn)` + `Product Critic (Drucker)`
- `Ontology Reviewer (Quine)` + `Schema Skeptic (Sadalage)`
- `Ontology Reviewer (Quine)` + `Ontology Reviewer (Peirce)`
- `Plan Skeptic (Brooks)` + `High-Assurance Reviewer (Cook)`
- `Repository Miner (et al.)` + `Evidence Auditor (Popper)`
- `Data Systems Reviewer (Kleppmann)` + `Schema Skeptic (Sadalage)`

Avoid duplicate lenses that mostly check the same thing.

## Output shape

Default output shape:

1. Top findings ordered by severity
2. What is strong
3. What is weak or risky
4. Concrete recommendations
5. Open questions if needed

## Report location

Every persona review is written to `docs/reviews/` as its own markdown file —
the file is the artifact of record; the chat summary just points at it.

- Filename: `YYYY-MM-DD-<lens-slug>-review-<artifact-slug>.md`
  (example: `2026-07-04-msr-review-00b.md`)
- YAML frontmatter:

  ```yaml
  ---
  title: <Lens> Review — <artifact title>
  date: YYYY-MM-DD
  reviewer-lens: <functional lens, not just the alias>
  artifact: <repo-relative path of the reviewed artifact>
  status: findings delivered | amendments applied | superseded
  tags: [codelore, review, <lens-slug>]
  ---
  ```

- Body follows the output shape above.

When delegating a review to a subagent, instruct it to write the report file
to `docs/reviews/` itself and return a short summary. If the subagent cannot
write files, write the file verbatim from its returned review before
summarizing it in chat.

## Calibration rule

If a persona push would make the writing harder to understand, weaken the style
and preserve the lens.
