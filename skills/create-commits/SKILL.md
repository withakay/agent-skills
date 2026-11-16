---
name: create-commits
description: Use only when the user explicitly asks to create a Git commit or draft a commit message, including atomic or stacked commits.
---

# Create Commits

Create focused commits without staging unrelated work. A request to edit, test, prepare a pull request, or suggest a message is not consent to commit.

For a message-only request, inspect the diff, return the message, and stop before staging.

## Consent

Require explicit commit consent in the current request. When the user asks to commit, choose logical groups and messages, then proceed without separate message or grouping approval.

Treat consent as bounded to the requested changes. Ask again only if the commit scope must expand beyond that request. Do not infer consent from flags, prior sessions, parent workflows, or generated metadata. A commit request authorizes local commits only. An explicit PR-creation request authorizes pushing the intended branch as needed to create that PR; use `writing-pull-requests` for that operation.

## Process

1. Run `git status --short`, `git diff`, `git diff --cached`, and `git log --oneline -10`.
2. Identify user changes and unrelated work. Never revert, rewrite, or stage changes outside the approved commit.
3. Group files by one logical behavior change. Keep its implementation, tests, and directly required documentation together.
4. Follow the repository's commit-message conventions. Otherwise use Conventional Commits: `type(scope): summary` or `type: summary` when no scope is useful.
5. Select each group's paths and message without pausing for approval.
6. Stage explicit paths with `git add -- <paths>` only when all their changes belong to the group; otherwise stage selected hunks. Check `git diff --cached` and `git status --short`. The entire staged diff must contain only the approved group. Preserve unrelated staged work; if you cannot isolate the group safely, stop and explain the conflict.
7. Run `git commit -m "<message>"`. Do not bypass hooks. If a hook changes intended files, inspect and re-stage only changes belonging to the group, then recheck the entire staged diff before retrying.
8. Verify with `git status --short` and `git log --oneline -n <count>`; report commit SHAs and any remaining changes.

For stacked commits and GitHub pull-request stacks, load the `gh-stack` skill and use `gh stack` for stack operations. If the user explicitly requests Git Town, load the `git-town` skill and verify `git town version`. Inspect repository configuration and create only the branches the user approved. Do not push the stack unless requested.

## Messages

- Describe one observable change in imperative mood.
- Use the real module or ticket scope when it helps retrieval.
- Keep summaries specific and omit the final period.
- Do not claim tests, fixes, or behavior that the diff does not show.

Except for the hook-generated changes handled above, stop the group and report the exact failure if staging or a commit fails. Do not amend, reset, skip hooks, force push, or stage all files as a recovery shortcut unless the user explicitly requests the specific action and it is safe.
