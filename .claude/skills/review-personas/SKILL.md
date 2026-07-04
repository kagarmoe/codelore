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

Read [references/personas.md](references/personas.md) before using one of these
reviewers. It defines:

- review focus
- main questions
- preferred failure modes to catch
- light writing-style guidance

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

Avoid duplicate lenses that mostly check the same thing.

## Output shape

Default output shape:

1. Top findings ordered by severity
2. What is strong
3. What is weak or risky
4. Concrete recommendations
5. Open questions if needed

## Calibration rule

If a persona push would make the writing harder to understand, weaken the style
and preserve the lens.
