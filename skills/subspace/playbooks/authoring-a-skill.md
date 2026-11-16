### Authoring or modifying a skill

**You own the skill's voice.** Agent-facing prose has a higher bar than human prose; unhelpful sentences become instructions.

1. Use the **create-skill** skill if present, otherwise follow the guides here https://agentskills.io/home.
2. Validate the skill: frontmatter has `name` and `description`, referenced files exist, cross-skill links resolve. Run the **create-skill** `scripts/add_toc.py` on the skill directory to refresh contents lists in long files.
3. Test cases if structural; skip if subjective.
4. Ask the user if they want to create a PR

When in doubt, delete; prose earns its keep by changing a decision. Tell it to do the thing and skip the reason. Explain only when the rule is confusing without one. Match tone to scope. Point at structural sources (types, READMEs, config); hardcoded details go stale (**principle-capture-learnings**). Delegate to other skills by path; don't restate. A workflow you keep hitting but isn't captured → propose a new skill.

**Reply:** summary of the skill, key design decisions, validation notes.
