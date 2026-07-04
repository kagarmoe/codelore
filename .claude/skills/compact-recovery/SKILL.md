---
name: compact-recovery
description: Use at the start of any session that has lost context — after auto-compact, `/clear`, `/resume`, a fresh session, or whenever you realize you do not know the current state of CodeLore work. Walks through a minimal reading checklist (current docs, active plan, git state, and repo structure) and produces a short situational summary before new work begins.
---

# Compact Recovery

## Overview

Use this skill when session context is incomplete and you need to re-orient
before acting. The goal is a short, accurate situational summary so work resumes
from evidence rather than memory.

Core principle:

- do not start implementing until you know the current repo state

## Read-in-order checklist

1. Read [README.md](../../../README.md).
2. Read [docs/plans/00-development-plan.md](../../../docs/plans/00-development-plan.md).
3. Read the most relevant current founding docs for the task at hand:
   - `docs/product/00-product-definition.md`
   - `docs/evidence/02-evidence-policy.md`
   - `docs/evidence/03-claim-taxonomy.md`
   - `docs/architecture/06-schema-draft.md`
   - `docs/architecture/07-canonicalization-policy.md`
4. Check git state:
   - `git status --short`
   - `git log --oneline -10`
5. Check current repo structure if implementation has started:
   - `find . -maxdepth 3 -type f | sort`

## Synthesis

Produce a short summary in this shape:

- current phase
- most recent committed or drafted work
- in-flight changes
- next action
- blockers or uncertainties

If anything is unclear, say so explicitly rather than guessing.
