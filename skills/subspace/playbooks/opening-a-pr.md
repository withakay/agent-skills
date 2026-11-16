### Opening a PR

Invoked at the end of every other playbook.

**Worktree.** Work from a git worktree off `main` when the host and repository support it. Give each writer an exclusive branch or worktree. If the branch contains unrelated edits, preserve them, create a clean worktree, and apply only the intended patch. Do not discard work you did not create.

**Commits.** Use [`create-commits`](../../create-commits/SKILL.md) for explicitly authorized commits or commit-message drafts. Keep commits small, ordered, buildable, and independently understandable. A request to prepare a pull request does not authorize committing or amending.

**PRs.** Run the repository's `deslop` and `unslop` checks when available. Use [`writing-pull-requests`](../../writing-pull-requests/SKILL.md) for the title, body, and requested GitHub creation or update. Follow its evidence, format, and authorization rules. Attach videos or screenshots when they prove a claim.

**Size and dependencies.** Prefer narrow pull requests to one large pull request. For dependent work, branch the next pull request from the previous branch, set its GitHub base accordingly, and state the dependency in the body. When the stack-management extension is installed, `gh stacks` may create, inspect, synchronize, or submit the stack, but the GitHub base and dependency still need to be explicit. Use `main` for independent work. Update dependent branches from current `main` or their declared base before review.

**Readiness.** Default to ready for review. An explicit user readiness request
(ready or draft) wins; otherwise honor an explicit readiness mode from the
calling workflow. With GitHub CLI, pass the selected mode when creating the
pull request. If the selected mode is ready but it opens as a draft, mark it
ready with `gh pr ready <number>`. Run `gh pr view <number>` before you report
its status.

**External-reference ledger.** When the work has a change folder, create or update its `ext-refs.md` in the pull-request branch. Record the branch, pull-request URL, base, dependency relationships, current state, and exact head SHA, mapped to the matching plan phase. Refresh the state and head after review changes and before the merge-ready report.

**Review.** Request the repository's automated code review when one is enabled, for example GitHub Copilot code review. Read every automated and human review comment, fix valid findings, and reply with the reason for any comment you reject. Re-run the focused checks after review changes.

**Live verification.** For behavioral or user-facing changes, use the project's project-local verification skill for the matching surface. If none exists, run **create-verification-skill**; if its feature map or harness is stale, run **maintain-verification-skill** before reporting the pull request ready.

**Babysit.** Opening a PR does not start a babysit. Post the URL and keep building. Finish the phase or stack first. Run a separate babysit pass only when the user asks for one after the whole stack exists. A babysit for each new PR stalls the build and spends checks on commits that later waves restart. Push back when feedback drifts from intent.

An agent that opens a pull request returns the URL and the exact head SHA. It does not wait for or merge the pull request unless the workflow explicitly assigns that responsibility.
