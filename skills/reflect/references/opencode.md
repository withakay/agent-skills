# OpenCode harness guide

Use this guide only when OpenCode is the active harness.

## Session input

Prefer a current session ID or transcript export exposed by the runtime. When the OpenCode CLI is available, use its public session commands instead of reading storage directly:

```bash
opencode session list
opencode export <session-id>
```

Select a session whose directory and opening user prompt match the active workspace and conversation. Write an export only to an approved temporary location outside the repository. Do not query `~/.local/share/opencode/*.db`; the database schema is internal and includes unrelated sessions.

If the CLI or active ID is unavailable, use AgentsView only when installed or build the digest from current context.

## Reviewer dispatch

Issue three `task` calls in one response. Select a general review-capable `subagent_type` from the live tool schema and pass one complete reviewer template to each child. Use configured agent routing; set a model only when the live task tool supports an explicit model field.

Choose an agent profile that can perform read-only repository and MCP lookups. The prompt prohibits file and external writes. After all reviewer outputs return, issue one separate `task` call with the filled synthesizer template.

If the task tool is unavailable, use the three-pass fallback in `SKILL.md`.

## Skill authoring

Load the `skill-creator` skill with OpenCode's skill tool for substantive edits, description tuning, or new skills. Use `apply_patch` for approved manual edits and the repository's skill validator when present. The parent may apply approved trivial edits directly.
