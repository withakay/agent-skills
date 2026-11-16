---
name: deslop
description: Remove AI-generated code slop and clean up code style
---

# Remove AI code slop

Check the branch's diff against its base branch (the repository's default branch unless the user names another) and remove AI-generated slop the branch introduced.

## Focus Areas

- Extra comments that are unnecessary or inconsistent with local style
- Defensive checks or try/catch blocks that are abnormal for trusted code paths
- Type casts used only to bypass type issues
- Deeply nested code that should be simplified with early returns
- Other patterns inconsistent with the file and surrounding codebase

## Guardrails

- Keep behavior unchanged unless fixing a clear bug.
- Prefer minimal, focused edits over broad rewrites.
- End with a short summary of what was removed and anything left in place on purpose.
