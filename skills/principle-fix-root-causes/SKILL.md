---
name: principle-fix-root-causes
description: "Apply when debugging. Trace each symptom to its root cause and fix it there. Reproduce first, ask why until you reach it, and resist nil-check guards that silence crashes."
disable-model-invocation: true
---

# Fix root causes

When debugging, don't paper over symptoms. Trace every problem to its root cause and fix it there.

Symptom fixes accumulate. Each workaround makes the system harder to reason about, and the real bug remains. Root-cause fixes take longer up front but reduce total debugging time.

## Pattern

- Reproduce first. If you can't reproduce it, you can't verify your fix.
- Ask why until you hit the root cause.
- Resist the urge to add guards. Adding a nil check to silence a crash is a symptom fix.
- If a workaround needs a paragraph-long comment to justify it, the code is wrong. Fix the code, not the comment.
- Check for the pattern, not just the instance. Search for the same pattern, and fix all instances.
- When stuck, instrument. Don't guess. Add logging, and read the actual error.

## Restart bugs

Code doesn't change between runs. State does. When something fails after restart, suspect stale persistent state first: config files, caches, lock files, and serialized state. If clearing a state file restores behavior, prioritize state validation as the fix.
