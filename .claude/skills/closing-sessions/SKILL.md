---
name: closing-sessions
description: Use at the end of any CodeLore work session when about to say work is done, complete, wrapped up, or ready for handoff. Enforces a close-out checklist: verify docs/code state, run relevant quality gates, commit when appropriate, push when configured, and leave a concise handoff summary.
---

# Closing Sessions

## Overview

A session is not closed just because a file changed. Close only after the repo
state is checked, relevant validation has run, and the next session can resume
cleanly.

## Checklist

1. Verify the working tree with `git status`.
2. Run relevant quality gates for the kind of work completed.
3. Check whether any follow-up work should be captured in docs or issues.
4. Commit if the work is ready to preserve.
5. Push if a remote is configured and push is intended for this session.
6. Re-check `git status`.
7. Leave a short handoff summary with:
   - what changed
   - what was verified
   - what remains next
   - blockers or open questions

## Rules

- Do not claim completion without checking `git status`.
- Do not describe unverified work as verified.
- If no remote exists yet, say so explicitly rather than pretending the push happened.
- Prefer a clean, resumable repo state over an ambiguous one.
