---
name: why
description: Use when investigating why code, architecture, thresholds, operational behavior, or prior decisions took their current form; use how for mechanics-only walkthroughs without a rationale question.
---

# Why

Recover rationale without turning plausible code-reading into history.

## Modes

- **Quick:** default for a scoped symbol or decision. Anchor current code, run a bounded history search, and return the strongest evidence plus gaps.
- **Full:** use when requested, when evidence conflicts, or when the decision has broad operational or architectural impact. Search all relevant evidence routes, reconcile contradictions, and report coverage.

State the selected mode. Escalate Quick to Full when the first pass cannot distinguish credible explanations.

## Evidence Routes

- **Current repository:** use lean-ctx when available. Call `ctx_compose` first, then `ctx_graph`/`ctx_callgraph`, `ctx_search`, and `ctx_read` as needed. Otherwise use the editor's file, text, symbol, reference, and call-hierarchy search. Current code proves mechanics and present boundaries, not original intent.
- **Source control history:** use standard Git history, blame, diffs, commit messages, and the repository host's PR view. Follow linked work-item and incident IDs. When `gh` is available, use it to read the full PR context; do not require a provider-specific CLI.
- **Historical evidence:** invoke `agentsview-finding-history` when available rather than recreating session-history searches. Give it the target, symbols, dates, commits, work-item IDs, and bounded queries.
- **Azure DevOps work items:** read linked work items when commits, PRs, or code comments identify one, or when the question needs delivery or business context. Use Azure DevOps by default for delivery context.
- **GitHub Issues:** read a linked issue when it is the delivery record, or when no Azure Boards item owns the work. Treat it as optional, not a second source of truth.
- **Broader organizational or cross-repository context:** invoke `ask-second-brain` when available. Treat stale pages as historical context, not current implementation evidence.
- **Linked organizational records:** read design records, incident reviews, runbooks, or team discussions only when the repository, PR, or work item links them and the engineer already has access. Treat stale records as historical context, not current implementation evidence.
- **Deployed runtime evidence:** prefer Azure Application Insights, Log Analytics, and Azure Monitor. Use AKS/Kubernetes logs, Grafana, or Datadog only when the owning team has access and those sources can answer a material gap.
- **Error and exception evidence:** use Sentry when it is available and relevant to defensive or corrective code. Treat release and issue correlation as supporting evidence, not proof by itself.
- **Data and analytics evidence:** use Databricks only for workloads that run on or publish evidence to Databricks. Use Aspire monitoring only when an Aspire AppHost is present and local behavior is relevant.
- **Other organizational sources:** use Linear, Notion, Slack, or another owning integration only when it is available, relevant, and read-only. Mark unavailable sources `Not searched` rather than guessing.

Use the least privilege and narrowest scope that can answer the question. Never write files, update work items, post comments, change cloud state, create knowledge, commit, push, or create remote artifacts during a Why investigation. If a tool cannot be made read-only, do not use it.

Do not require the engineer to install a CLI, extension, agent skill, or connector. When the coding assistant cannot access a relevant web source, prepare the smallest read-only query for the engineer to run in the existing web interface. Continue from redacted results that the engineer supplies. If the source remains unavailable, mark it `Not searched` and continue with available evidence.

## Process

1. Restate the target and question. If ambiguous, state the interpretation.
2. Build a code anchor: cited files/lines, symbols, present call or dependency path, and known identifiers.
3. Run the mode's relevant evidence routes. Do not search every source by default. Record every query and source searched.
4. Classify claims using `references/epistemics.md`: Direct, Supported, Inferred, Speculative, or Unknown.
5. Surface conflicting evidence. Never cite current code as proof of its own historical motivation.
6. Label an empty search exactly `No result`, followed by source, query, scope/date range, and any access limitation. An unsearched source is `Not searched`, with the reason; it is not a no-result finding.

Full mode may use `references/investigator-prompt.md`, the category index in `references/source-playbook.md`, and `references/synthesizer-prompt.md`. Parallelize only independent read-only searches.

## Return

- **Question and code anchor**
- **Direct evidence**, with citations and dates
- **Supported conclusions**, with evidence chain
- **Inferences or competing hypotheses**, clearly hedged
- **Unknowns and No result searches**
- **Sources consulted**, including exact query and scope
- **Confidence summary**

Every factual rationale claim needs a verifiable citation such as an AgentsView reference, commit, PR, work-item or incident identifier, URL, or `file:line`. Preserve source wording when it changes meaning; otherwise summarize plainly.
