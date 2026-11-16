# Source Control Archaeology

## What this source contains

- Commit history (messages, dates, authors, diffs)
- PR descriptions, review comments, and discussion threads from the repository host
- Inline code comments, TODOs, FIXMEs, deprecation notes
- ADRs (architectural decision records) if the repo keeps them
- Tests. Names and assertions often encode the edge cases that motivated a change
- Related files modified in the same commits (co-change signal)
- CHANGELOG entries, release notes in the repo
- Issue/ticket IDs mentioned in commit messages and PR bodies

This evidence is tied directly to the code and is available to any engineer with repository access. It can still be incomplete when rationale was recorded elsewhere.

## How to search it

Expand the seed commit list:

```bash
# Full history of the file through renames
git log --follow --oneline -- <file>

# Pickaxe: commits that added or removed this exact text
git log -S '<exact_string_from_code>' -- <file>

# Or for patterns:
git log -G '<regex>' -- <file>

# Who wrote each line and when
git blame -L <start>,<end> <file>

# The full diff of a specific commit
git show <hash>

# Commits between two points affecting this file
git log <old>..<new> -p -- <file>
```

For each substantive commit, read the PR context in the repository host or through an available read-only integration. Do not require a provider-specific CLI.

Use `git log -1 --format=%B <hash>` to find PR or work-item references in a commit message. In the PR, read the description, review comments, linked work items, changed files, author, and dates. When GitHub CLI is already available, it can fetch the full context:

```bash
# Find the PR number from the merge commit or branch
 git log -1 --format=%B <hash>

# Full PR context: body, review comments, linked issues, and changed files
 gh pr view <number> --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews,files
```

If the host or CLI is unavailable, use the existing read-only integration or mark that source `Not searched`; do not require installation of a new tool.

Look for out-of-band docs:

Use the coding assistant's built-in file and text search for ADRs, `TODO`, `FIXME`, `HACK`, `NOTE`, target symbols, and related tests. These searches work without installing an additional utility. When a repository has a conventional docs layout, narrow the search with commands such as:

```bash
rg -l -i 'architecture\\.decision' --glob '*.md'
rg -n -C2 '(TODO|FIXME|HACK|XXX|NOTE)' <target_file>
rg -l '<symbol>' --glob '*test*'
```

## What good evidence looks like here

- A PR description that explains the problem being solved, not just the change ("This fixes the pagination bug that caused X")
- A long review thread where alternatives were debated
- An inline comment near the target line that explains a non-obvious constraint
- A test named `test_handles_edge_case_when_X` that reveals an edge case motivating the code
- A commit message that references a ticket or incident ID
- A CHANGELOG entry that summarizes the user-visible rationale

## Common pitfalls

- **Squash-merge flatlands.** If the repo squashes PRs, individual commits in the branch history are lost. Fall back to PR body and comments.
- **Misleading commit messages.** "Small refactor" sometimes hides an intentional behavior change. Look at the diff, not the message.
- **Cargo-culted patterns.** The author may have copied a pattern without understanding why. Check if the pattern originated earlier in the codebase and investigate *that* commit.
- **Bot commits and auto-merges.** Dependabot, Renovate, and automated backports usually don't carry motivation. Skip them when trying to find intent.
- **Treating code as evidence of intent.** The code itself isn't evidence for why it exists. Evidence comes from commit messages, PRs, comments, tests, docs. Don't cite "the function is named X" as evidence of intent.

## What to return

Every commit/PR/comment that bears on the question, with:
- The exact text (quoted)
- The hash / PR number / file:line
- Author and date
- Whether it's direct (explicitly addresses the question) or circumstantial
