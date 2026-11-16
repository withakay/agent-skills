---
name: principle-guard-the-context-window
description: "Apply when context is filling up or a small inquiry expands into planning, implementation, deployment, or release: large outputs, long files, repeated reads, or fan-out work. Route bulk work to subagents and keep summaries in the main thread, not raw payloads."
disable-model-invocation: true
---

# Guard the context window

The context window is finite and non-renewable within a session. Every token that enters should earn its place.

Context overflow degrades reasoning quality, creates compression artifacts, and halts progress. Unlike compute or time, context spent inside a session can't be reclaimed.

## Pattern

- Isolate large payloads. Route verbose outputs, screenshots, and large documents to subagents when the harness provides them; otherwise save them to a file and read only the parts you need. The main context gets summaries, not raw data.
- Don't read what you won't use. Read selectively based on relevance. If a file isn't needed for the current task, skip it.
- Keep frequently used content inline. Templates and references used on every invocation belong in the skill file, not in separate files that cost a read each time.
- Size phases and cap scope. Limit files per phase, set turn budgets, and account for mechanism costs.
