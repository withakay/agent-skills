# Source playbooks

Full mode may assign one read-only investigator per relevant evidence category when the coding assistant supports parallel investigators. Otherwise, use the relevant playbooks sequentially. Give each investigator one source-specific playbook and adapt its queries to the available owning skill or integration.

The baseline requires only repository search in the coding assistant or editor and standard Git. Use existing browser access for Azure DevOps, Azure Monitor, or another relevant team source when evidence there is necessary and the engineer has permission. Optional integrations and command-line tools are not prerequisites. Do not install or configure extra software only for this investigation. Mark an unavailable optional source `Not searched` and give the reason.

The coding assistant can prepare KQL, SQL, and search terms when it cannot open a web source. The engineer can run the query in the existing web interface and provide redacted results. Do not imply that the assistant searched a source that only the engineer can access.

| Category | Playbook | Typical system or tool |
|---|---|---|
| Source control history | [`code-archaeology.md`](./sources/code-archaeology.md) | Git and repository host |
| Delivery and business context | [`azure-devops-work-items.md`](./sources/azure-devops-work-items.md) | Azure DevOps Boards work items |
| GitHub delivery context | [`github-issues.md`](./sources/github-issues.md) | GitHub Issues when the repository uses them |
| Primary runtime observability | [`azure-monitor.md`](./sources/azure-monitor.md) | Application Insights, Log Analytics, Azure Monitor |
| AKS runtime detail | [`kubernetes.md`](./sources/kubernetes.md) | Azure Monitor Container Insights, `kubectl` |
| Team dashboards | [`grafana.md`](./sources/grafana.md) | Azure Managed Grafana or team-managed Grafana |
| Data platform evidence | [`databricks.md`](./sources/databricks.md) | Azure Databricks SQL and system tables |
| Local development evidence | [`aspire.md`](./sources/aspire.md) | Aspire dashboard and telemetry |
| Issue or ticket tracker | [`linear.md`](./sources/linear.md) | Linear, or an adapted Jira/GitHub Issues integration |
| Long-form documents | [`notion.md`](./sources/notion.md) | Notion, or an adapted Confluence/Docs integration |
| Real-time team chat | [`slack.md`](./sources/slack.md) | Slack, Teams, Discord, or another owning chat integration |
| Infrastructure observability | [`datadog.md`](./sources/datadog.md) | Datadog, Grafana, New Relic, Honeycomb, or Splunk |
| Error and exception tracking | [`sentry.md`](./sources/sentry.md) | Sentry, Rollbar, Bugsnag, or Airbrake |

Select sources in this order:

1. Search source control and linked Azure DevOps work items for stated rationale. Search a linked GitHub Issue when it is the delivery record.
2. Follow the source named by the repository, PR, work item, or incident. Prefer the owning system over a generic search.
3. For deployed operational behavior, use Azure Monitor before optional observability systems. Use Datadog, Grafana, Sentry, or another source only when its data can answer a material gap.
4. Use AKS/Kubernetes or Grafana only when the service runs there, access exists, and the primary runtime source does not answer the question.
5. Use Databricks only when the target belongs to a Databricks workload or data flow. Use Aspire only for local reproduction or current development behavior; do not use local telemetry as proof of past production motivation.
6. Use Linear, Notion, Slack, or equivalent organizational sources only when available and relevant. Do not install or configure an integration solely for a Why investigation.

Cross-cutting:

- [`incident-postmortem.md`](./sources/incident-postmortem.md). Add this if the target code looks defensive (null checks, retry, timeout, rate limit, feature flag, egress guard, OOM handler).
