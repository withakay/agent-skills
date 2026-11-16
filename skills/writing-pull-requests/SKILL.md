---
name: writing-pull-requests
description: Use only to draft, create, or update a GitHub pull request title or body.
---

# Writing pull requests

<!-- toc -->
## Contents

- [Separate PR content from the session handoff](#separate-pr-content-from-the-session-handoff)
- [Collect evidence](#collect-evidence)
- [Title and body conventions](#title-and-body-conventions)
- [Make review fast](#make-review-fast)
- [Body](#body)
- [Boundaries](#boundaries)
- [Final pass](#final-pass)
- [Create or update](#create-or-update)
<!-- tocstop -->

Write a reviewer-facing cover note, not a changelog, diff summary, release note, or validation log.

Write for a busy reviewer who is switching context and has not read the issue,
chat, or earlier PRs. Give enough context to understand the problem, benefit,
scope and main decision without opening those sources. Explain unfamiliar
terms briefly; use links for supporting detail, not as substitutes for context.

## Separate PR content from the session handoff

Describe the repository change, design decisions, relevant verification and
actual merge consequences. A true session fact does not automatically belong
in a PR.

Distinguish authored guidance and examples from changes to a running system.
Describe guidance as guidance, not as deployed behavior.

Keep the author's workstation state, personal installation status, permissions
granted to the agent, review-team narration and generic assurances about actions
not performed in the session handoff, not the PR body.

Mention environment, deployment or publication status only when it establishes
a real adoption dependency, rollout step, verification limit or merge consequence.
Preserve material unrun checks and irreversible migrations. Do not invent a
limitation to fill a paragraph. Technical paths and test environments remain
appropriate when they explain the changed contract or verification evidence.
A handoff note such as "publication remains separate" does not establish a
release dependency. Require change-related evidence for that claim.

## Collect evidence

Use authenticated `gh` for GitHub state and Git for branch evidence. For a draft-only request, continue with local Git evidence if `gh` is unavailable; never create or update a PR without authenticated `gh`.

```bash
git branch --show-current
git status --porcelain
gh pr view --json number,title,body,url,baseRefName,headRefName
gh repo view --json defaultBranchRef
```

Resolve `BASE` from the existing PR, the explicit request, or the repository default, in that order. For stacked work, use the declared parent branch. If a requested base conflicts with an existing PR's base, resolve that conflict before proceeding.

Use the branch name for `gh pr create --base`. For evidence, fetch that branch from the base repository and set `BASE_REF` to its up-to-date remote-tracking ref; do not assume a local branch or `origin` is the correct base. If a text-only draft must use stale or incomplete evidence, state that limitation.

```bash
git log "$BASE_REF"..HEAD --oneline
git diff "$BASE_REF"...HEAD --stat
git diff "$BASE_REF"...HEAD
```

If the full diff is large, read it path by path. Also inspect `git diff` and `git diff --cached` when drafting from uncommitted work.

Readiness precedence is explicit user readiness (ready or draft) wins, then an
explicit calling-workflow readiness requirement, then standalone ready for
review.

Before a GitHub mutation, verify that intended changes are committed and review the whole branch diff, not only the latest commit or current PR text. Do not create a PR from `main` or `master`; create a feature branch first.

Draft directly when evidence supports one result. Ask only when an answer can materially change the title, base, compatibility or migration guidance, risk, or reviewer aid. Omit unsupported claims and optional issue references.

## Title and body conventions

Follow the repository's title conventions and required PR template. Otherwise, use a Conventional Commit title, `<type>(<scope>): <subject>` or `<type>: <subject>`, and the smallest useful body.

- Name the concrete changed behaviour and relevant scope in the title, rather than the work performed. Describe the dominant full-branch change with the narrowest accurate type and scope; do not overstate the benefit.
- Use `!` only for an external breaking contract and explain that contract in the body.
- Avoid vague subjects such as `update`, `cleanup`, `misc`, or `address feedback`; omit the trailing period.
- When updating the title, keep it only if it still describes the whole diff.

## Make review fast

The body exists to let a reviewer decide. Cover these in whatever order reads best; drop one when it adds nothing.

- **Decision.** Name what the reviewer must judge: an algorithm, a contract change, a product tradeoff, or migration safety. Point to the file or symbol that carries it, and give a reading order when the diff is large or spread across systems.
- **Domain language.** Use the terms the repository already uses in its documentation, specifications, and identifiers. Do not invent a synonym for a modelled concept. When this change introduces or redefines a term, record it in the project's glossary and link that entry instead of defining the term in the body. See [`domain-modeling`](../domain-modeling/references/glossary.md) for where that glossary lives.
- **Evidence.** Show that the change works: a screenshot or clip for user-visible behavior, the relevant lines of test or command output, before and after values for data or performance, or the reproduction that now passes. Quote only what you produced or read, and attribute a result someone else reported. Name the environment when it changes the result.
- **Merge risk.** Judge whether merging is reversible: a revert or a flag restores the previous behavior, or it does not. Data migration, deletion, a published artifact, an external contract, and a rotated credential survive a revert. Include irreversible steps, their recovery cost and backout steps the reviewer cannot infer. Omit routine Git-revert assurances when recovery is obvious and merging has no persistent effect.
- **Views.** Use a compact call tree, file tree, diff sketch, or Mermaid diagram when the shape of the change is faster to see than to read. See [`show-me`](../show-me/SKILL.md) for view shapes.

## Body

- Lead with the benefit and the concrete behaviour that provides it. State the problem when the title does not make it evident; do not use unsupported benefit claims.
- If a material risk, blocker, limitation or tradeoff exists, explain it early. Do not manufacture one or add "no known risks" filler.
- State the scope clearly: affected users, environments or components, and important behaviour that stays unchanged. When the change crosses systems, name the affected interfaces and include compatibility and migration steps for changed APIs, schemas, payloads, configuration, permissions, storage, or CLI contracts.
- Name an alternative only when user input, branch evidence, commits, or PR discussion records it.
- Choose structure to help reviewers scan. A small change may need one paragraph; a change with distinct scope, dependencies, risks or verification usually benefits from short, meaningful headings and concise bullets. Conventional headings such as `Scope`, `Module dependency` and `Verification` are useful when they contain relevant information, not a mandatory template.
- Keep the body to what a reviewer needs in order to decide. Add length only for substance, such as adopter instructions for a breaking change or migration.
- For follow-up commits or review feedback, describe the current PR as a whole; do not narrate revision history.
- Avoid process narration such as who authorized the work, which agents reviewed it, or the sequence of commands run. Keep decisions, required approvals, deployment constraints and verification evidence that affect review or rollout; link detailed execution records instead of copying them into the body.

Write clear Simplified Technical English. Preserve technical meaning and modality, and use exact versions, counts, limits, and units when relevant to the claim. See [language rules](references/language.md).

## Boundaries

- Follow required repository templates. Otherwise omit empty sections, placeholder checklists and repeated information, not useful headings. Omit commit logs, bulk command output, exhaustive file lists and diff statistics. A short quoted excerpt that carries evidence is not bulk output.
- Include verification details that help reviewers assess coverage or risk, and any required by the repository template. Never claim a check you did not run, and never write only "tested locally".
- Use `Fixes <issue>` or `Refs <issue>` only when the reference is verified.
- Never include secrets. Do not disclose private information that is not approved for the PR's audience.
- Preserve code, identifiers, paths, commands, product names, and quoted errors exactly.

## Final pass

Read the title and body once. Remove repetition, process narration, courtesy text, unsupported claims, and structure that does not help review. Confirm the first sentence names the change, any material risk appears early, and a reviewer can tell what to check and any required adoption or recovery steps. Do not mention this pass in the body.

Can a reviewer find the benefit, affected scope, main risk or dependency, and
verification without reading every paragraph or reconstructing the chat?
If not, add the missing context or improve headings and bullets. Do not merely
shorten the text.

For each sentence, ask whether it helps a reviewer understand or decide whether
to merge the repository change. Remove session-only facts instead of turning
them into scope disclaimers.

## Create or update

Create or update a PR only when requested. An explicit PR-creation request authorizes pushing the intended branch as needed to create that PR, but does not authorize committing uncommitted work. A text-only request authorizes neither. Creating a draft PR is a GitHub mutation, distinct from drafting PR text.

For either creation or update, prepare a private temporary file containing the exact body. Keep it available for the selected operation and remove it afterward:

```bash
BODY_FILE="$(mktemp)"
chmod 600 "$BODY_FILE"
trap 'rm -f "$BODY_FILE"' EXIT
# Write the exact PR body to "$BODY_FILE".
```

For creation, push the committed feature branch to the intended head repository if needed. Create the PR with the selected readiness and explicit base. Use `--draft` when draft is selected; use `--draft=false` when ready is selected:

```bash
gh pr create --draft=false --base "$BASE" --title '<title>' --body-file "$BODY_FILE"
```

For an existing PR, update only the requested fields rather than creating another PR. For a body-only update, omit `-f title='<title>'` from this example:

```bash
PR_NUMBER="$(gh pr view --json number --jq .number)"
gh api -X PATCH "repos/{owner}/{repo}/pulls/$PR_NUMBER" -f title='<title>' -F body=@"$BODY_FILE"
```

Within the requested update scope, refresh text when follow-up changes make it inaccurate, including meaningful renames. Describe the current PR as a whole. If another field needs correction, report it without changing it.

Read the PR back with `gh pr view` and verify its title, body, base, and readiness. Report its URL and any mismatch; do not claim success from the mutation command alone.

See [PR body examples](references/examples.md) for small, flow-oriented, evidence-carrying, and breaking-contract descriptions.
