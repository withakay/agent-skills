# OpenAI Codex harness guide

Use this guide only when OpenAI Codex CLI or the Codex app is the active harness.

## Session input

Prefer an active-thread export or transcript path exposed by the runtime. When Codex exposes only its local rollout store, use `$CODEX_HOME/sessions` (default `~/.codex/sessions`) and inspect only recent date-partitioned candidates.

```bash
CODEX_HOME=${CODEX_HOME:-$HOME/.codex}
ls -t "$CODEX_HOME/sessions/$(date +%Y/%m/%d)"/rollout-*.jsonl 2>/dev/null
```

Read candidate metadata before message content. Require the `session_meta` working directory to equal the active workspace, then confirm the opening user prompt. Do not search older date partitions or other working directories merely to find a match. If no candidate resolves, use AgentsView when available or create a digest.

## Reviewer dispatch

Use Codex multi-agent tools when they are present. Multi-agent support can require `[features] multi_agent = true` in `~/.codex/config.toml`; do not modify user configuration solely to run reflection.

Spawn the three reviewers in parallel with isolated context (`fork_turns: "none"`). Set `model` and `reasoning_effort` explicitly only after checking the current spawn allowlist; otherwise use configured agent types that already carry deliberate routing. Never copy stale model names from this skill.

Wait once in a bounded 5-10 minute interval when idle, then reconcile child status. After all reviewer outputs arrive, spawn a separate synthesizer with the complete filled template. If multi-agent tools are absent, use the three-pass fallback in `SKILL.md`.

## Skill authoring

For substantive edits, description tuning, or new skills, invoke the installed `skill-creator` or equivalent skill-authoring skill. The parent may apply approved trivial edits directly.
