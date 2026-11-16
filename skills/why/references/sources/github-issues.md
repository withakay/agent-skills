# GitHub Issues

Use GitHub Issues only when the repository or pull request identifies one as the delivery record. Azure DevOps Boards remains the default work tracker.

## Search process

1. Start with issue numbers and URLs from branch names, commits, pull requests, code comments, and release records.
2. Read the issue title, description, acceptance criteria, labels, linked pull requests, timeline, and closure reason.
3. Search by service name, feature name, symbol, error text, and relevant date range only when no linked issue answers the question.
4. Follow linked issues and pull requests. Record links to Azure Boards, incidents, design records, or discussions as leads for the matching evidence route.

## Strong evidence

- A description or comment that states the problem or decision.
- Acceptance criteria that explain a constraint reflected in the code.
- A linked pull request or commit that names the implementation and timing.
- A parent issue or linked project item that supplies the broader objective.

## Limits

- A label, milestone, assignee, or title can suggest context but does not prove motivation.
- Issue scope can change after implementation. Compare revisions and dates with the target commit.
- Templates and generated text can be weak evidence. Prefer specific statements and discussion.
- An inaccessible issue is an access gap, not `No result`.

## Return

Return the issue number and URL, title, author, dates, linked pull requests and work items, exact supporting text, timeline location, query and scope, and evidence strength.
