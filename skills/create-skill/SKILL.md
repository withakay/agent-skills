---
name: create-skill
description: Use when creating, updating, or validating agent skills.
---

# Skill Creator

Create the smallest skill that changes behavior reliably. Reuse an existing skill before adding a new one, and automate mechanical constraints instead of documenting them.

## Workflow

1. **Define use cases.** Collect concrete trigger, near-miss, and out-of-scope examples. Identify the failure or repeated decision the skill must address.
2. **Choose resources.** Keep judgment and the core workflow in `SKILL.md`. Put reusable code in `scripts/`, on-demand detail in `references/`, and output material in `assets/`. Keep references one level below `SKILL.md`.
3. **Initialize or inspect.** For a new skill, run `uv run --script scripts/init_skill.py <name> --path <root> [--resources scripts,references,assets]`. For an existing skill, inspect its files and callers before editing.
4. **Write minimally.** Use imperative instructions, one source of truth per rule, and one strong example only when it teaches non-obvious behavior. Match specificity to risk: heuristics for flexible work, exact commands or scripts for fragile work.
5. **Test behavior.** Read [`references/behavior-testing.md`](references/behavior-testing.md). Select its low, medium, or high tier from the skill's consequences, then test discovery and behavior at that tier.
6. **Validate.** Run `uv run --script scripts/quick_validate.py <skill-directory>`, check local links, test added scripts, and, when the skill ships `agents/openai.yaml`, verify it still describes the skill.
7. **Add contents lists.** Run `uv run --script scripts/add_toc.py <skill-directory>` after every edit. It adds or refreshes a `## Contents` list of headings in `SKILL.md` and `references/` files over 100 lines, and removes the list when a file no longer needs it. Do not edit the list between `<!-- toc -->` and `<!-- tocstop -->` by hand. Use `--check` to report stale lists without writing.
8. **Iterate from evidence.** Tighten guidance only for observed trigger misses, unsafe behavior, output defects, or repeated confusion.

## Skill Shape

```text
skill-name/
|-- SKILL.md
|-- agents/openai.yaml       # optional vendor sidecar: OpenAI UI metadata
|-- scripts/                 # deterministic or reused code
|-- references/              # read only when needed
`-- assets/                  # copied or transformed output material
```

Use lowercase letters, digits, and hyphens for the directory and frontmatter `name`; keep them identical. Prefer a short verb-led name.

Frontmatter contains only `name` and `description`. Make `description` a trigger contract: state when to load the skill with concrete terms, include important exclusions, and do not summarize the workflow. Avoid universal triggers unless the skill truly applies to every request.

Keep `SKILL.md` concise. Do not add README, changelog, installation guide, or duplicated reference files. Link each on-demand reference directly from `SKILL.md`; do not create reference chains.

## Resources

- Read [`references/openai_yaml.md`](references/openai_yaml.md) before generating UI metadata.
- Generate metadata with `uv run --script scripts/generate_openai_yaml.py <skill-directory> --interface key=value`.
- Test every added script with representative input before completion.

Do not commit, push, publish, install globally, or open a pull request without explicit user approval.
