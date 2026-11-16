# Claude Code harness guide

Use this guide only when Claude Code is the active harness. A Claude model running in another application uses that application's guide.

## Session input

Prefer an active transcript path exposed by Claude Code. Otherwise derive the current project directory under `~/.claude/projects/` from the absolute workspace path, then verify the `cwd` field before reading message content. Claude Code commonly stores parent transcripts as `<session-id>.jsonl` and child transcripts below a session-specific `subagents/` directory.

```bash
project_key=$(pwd -P | tr '/' '-')
ls -t "$HOME/.claude/projects/$project_key"/*.jsonl "$HOME/.claude/projects/$project_key"/*/subagents/*.jsonl 2>/dev/null
```

Confirm the opening user prompt and use the matching parent transcript. Do not glob across all `~/.claude/projects/*/` directories. If the project-key convention does not resolve safely, use AgentsView when available or create a digest.

## Reviewer dispatch

Issue three `Agent` or `Task` calls in one response with a general-purpose subagent type. Pass each complete template and the transcript path or digest. Use configured model aliases or inheritance; do not hardcode a model ID that the active Claude Code installation may not expose.

Allow the read and MCP tools required for referenced-context lookups while the reviewer prompt prohibits writes. After all three reviewers return, dispatch one separate general-purpose agent with the filled synthesizer template.

If subagents are unavailable, use the three-pass fallback in `SKILL.md`.

## Skill authoring

Invoke the installed `skill-creator` or equivalent skill-authoring skill for substantive edits, description tuning, or new skills. If none is installed, preserve the target skill's current structure and apply only the approved change. The parent may apply approved trivial edits directly.
