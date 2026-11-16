---
name: setup-subspace
description: Use only to install, update, or remove the Subspace plugin in Claude Code, OpenAI Codex, or OpenCode.
---

# Setup Subspace

Subspace ships as one plugin from the `withakay/agent-skills` repository. Each harness installs it with its own plugin manager, so there are no files to copy and no separate installer.

These commands change the user's harness configuration, so run them only after the user asks to install, update, or remove Subspace. Use the harness the user names. If they name none, ask: the harness running this session is the usual answer, but the user may be setting up a different one.

| Harness | Install | Update | Remove |
| --- | --- | --- | --- |
| Claude Code | `claude plugin marketplace add withakay/agent-skills`, then `claude plugin install subspace@withakay` | `claude plugin marketplace update withakay`, then `claude plugin update subspace@withakay` | `claude plugin uninstall subspace@withakay` |
| OpenAI Codex | `codex plugin marketplace add withakay/agent-skills`, then `codex plugin add subspace@withakay` | `codex plugin marketplace upgrade withakay` | `codex plugin remove subspace@withakay` |
| OpenCode | `opencode plugin add github:withakay/agent-skills` | `opencode plugin update github:withakay/agent-skills` | `opencode plugin remove github:withakay/agent-skills` |

Every command installs for the user. Claude Code also accepts `--scope project` on `install`, which records the plugin in the repository's settings so collaborators are offered it.

## Verify

List the installed plugins with `claude plugin list`, `codex plugin list -m withakay`, or `opencode plugin list`, and confirm `subspace` is present and enabled. Skills load when a session starts, so ask the user to open a new session, then confirm the `subspace` skill is offered there. Claude Code namespaces plugin skills, so it appears as `subspace:subspace`.

Report the harness, the command results, and whether the new session saw the skill. If a command fails, report its output instead of working around the plugin manager by copying skill folders: a hand-copied install is invisible to later updates.

## Change-artifact home

The full workflow writes change artifacts to `docs/changes/`. When the user wants another location for a repository, create `.agents/config/subspace/config.json` there:

```json
{ "changes_home": "work/changes" }
```
