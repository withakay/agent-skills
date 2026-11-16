# Incident and Postmortem Context

Not a separate source, a **cross-cutting angle**. Incidents often motivate defensive code ("we added this check after the X outage"), so if the target looks defensive (null checks, retry logic, timeout handling, rate limiting, feature flags), specifically hunt for incident history across every available source:

- **Azure DevOps work items:** search linked incidents, bugs, reliability tasks, and post-incident action items. Read parent items and discussion.
- **Source control:** search commits and PRs for incident IDs, mitigations, reverts, follow-up fixes, and defensive changes.
- **Azure Monitor:** search alerts, workbooks, exceptions, traces, metrics, activity logs, and deployment markers around the incident window.
- **AKS/Kubernetes:** when applicable, search retained Container Insights data, workload events, restarts, probe failures, OOM kills, and previous container logs.
- **Grafana:** when the team uses it, inspect incident or deployment annotations and the exact panel and alert queries.
- **Databricks:** when the affected workload uses it, inspect failed runs, query history, audit evidence, pipeline events, and verified operational tables.
- **Aspire:** reproduce the failure locally only when authorized. Treat the result as current local evidence, not proof of the historical incident.
- **Linked records:** follow incident reviews, postmortems, runbooks, and team discussions linked from the repository, PR, or work item. Do not assume a separate knowledge system is installed or searchable.
- **Notion:** when available, search postmortems and action-item pages mentioning the target file, feature, or error string.
- **Linear:** when available, look for tickets labeled `incident`, `sev-*`, `postmortem-action-item`, or `reliability`.
- **Slack:** when available, search incident and severity channels around the dates the target code was added, and read the full thread.
- **Datadog:** when available, search formal incident records, monitors, dashboards, and logs around the incident window.
- **Sentry:** when available, correlate issues, stack traces, releases, and first/last-seen timestamps with the target change.

If you find an incident link, read the full incident record or postmortem. Capture the timeline, impact, contributing factors, corrective actions, owners, and links to the target change. Corroboration is strongest when the same incident ID, deployment, error, and corrective action connect Azure DevOps, source control, and timestamped runtime evidence.

Worth spending time on when the code's defensive character makes an incident-driven origin plausible. Skip it for code that doesn't look defensive.
