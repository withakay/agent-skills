# GitHub Copilot CLI harness guide

Use this guide only when GitHub Copilot CLI is the active harness.

## Session input

Prefer a transcript or session-export tool exposed to the agent by the current Copilot runtime. Copilot's interactive `/share` command can export the current session to Markdown, and non-interactive runs can use `--share=<path>` after completion, but do not claim to invoke a user-only slash command.

Do not query or parse `~/.copilot/session-store.db` or other internal state databases. Their schema is not a public reflection contract, and the store contains sessions from multiple workspaces.

If no model-facing export exists, use AgentsView only when available. Otherwise build the digest from the current conversation context.

## Reviewer dispatch

Use the agent or task delegation tool exposed by Copilot and issue the three independent reviewer calls in one turn. Use Fleet mode when it is already available; do not require the user to enable it only for reflection.

Use the configured subagent model routing, visible through `/subagents` in interactive Copilot. Do not hardcode provider model IDs. Give each child the complete prompt template and transcript path or digest; do not rely on inherited chat context.

After all reviewer tasks finish, dispatch one separate general review-capable agent with the filled synthesizer template. If no delegation tool is available, use the three-pass fallback in `SKILL.md`.

## Skill authoring

For substantive edits, description tuning, or new skills, invoke the installed `skill-creator` or equivalent skill-authoring skill. If no authoring skill is discoverable, follow the target skill's existing structure and keep the approved change minimal. The parent may apply approved trivial edits directly.
