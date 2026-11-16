# Azure DevOps Work Items

Use Azure DevOps work items to recover delivery, product, and business context linked to the code.

## Search process

1. Use the Azure DevOps web interface by default, or an existing read-only integration when one is already available.
2. Start with work item IDs from commit messages, PRs, branch names, code comments, or release records.
3. Read the full description, acceptance criteria, discussion, history, parent, children, and links.
4. Search by the service name, feature name, symbol, error text, and relevant date range only when no linked work item answers the question.
5. Follow duplicate, predecessor, successor, parent, and incident links. Record cross-source links as leads.

## Strong evidence

- A description or comment that states the problem or decision.
- Acceptance criteria that explain a constraint reflected in the code.
- A parent Feature or Epic that supplies the broader objective.
- A linked incident, PR, design record, or operational task that names the target.

## Limits

- A state, tag, iteration, or title can suggest context but does not prove motivation.
- Scope can change after implementation. Compare revisions and dates with the target commit.
- Templates and generated text can be weak evidence. Prefer specific statements and discussion.
- An inaccessible work item is an access gap, not `No result`.

## Return

Return the work item ID and URL, title, type, author, dates, parent and links, exact supporting text, revision or comment location, query and scope, and evidence strength.
