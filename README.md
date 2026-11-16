# Agent skills

Skills for coding agents: workflow routing and delivery playbooks (Subspace), engineering principles, debugging, testing, static security review, and technical writing. Each skill is a folder under [`skills/`](skills/) in the [Agent Skills](https://agentskills.io) format, written to be portable across agent harnesses and models.

## Install with skills.sh

```bash
npx skills add withakay/agent-skills
```

The command lets you pick skills and the agents to install them for. Add `--skill <name>` to install one skill, or `-g` to install for every project.

## Install as a plugin

The same repository is a plugin for the harnesses below, which installs every skill and keeps them updated through the harness's plugin manager.

| Harness | Command |
| --- | --- |
| Claude Code | `claude plugin marketplace add withakay/agent-skills`, then `claude plugin install subspace@withakay` |
| OpenAI Codex | `codex plugin marketplace add withakay/agent-skills`, then `codex plugin add subspace@withakay` |
| OpenCode | `opencode plugin add github:withakay/agent-skills` |

## Where to start

Load the `subspace` skill to route a request to the right workflow, or `ask-subspace` to ask which skill fits a situation.
