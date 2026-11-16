# Grafana

Use Grafana when the owning team uses it and its dashboards or data sources add evidence not already available from Azure Monitor.

## Search process

1. Confirm the Grafana instance, organization, folder, team ownership, data source, environment, and time range.
2. Search dashboards by service, feature, operation, metric, alert, and error name.
3. Inspect panel queries, transformations, thresholds, alert rules, variables, and annotations. A panel title alone is not evidence.
4. Use Explore only for read-only, time-bounded queries against the relevant data source.
5. Correlate annotations and metric changes with deployments, incidents, and target commits.

## Strong evidence

- A panel or alert query whose threshold matches the target code.
- A deployment or incident annotation linked to a change in the relevant signal.
- A dashboard revision or description that explicitly records why a signal was added.
- A cross-data-source view that connects application failures with platform pressure.

## Limits and safety

- Grafana visualizes other systems. Cite the dashboard and the underlying data source and query.
- Dashboard revisions, variables, and transformations can change the meaning of historical views.
- Shared dashboards can mix environments. Verify variable values and labels.
- Use viewer operations only. Do not save panels, change variables persistently, acknowledge alerts, or modify data sources.
- Aggregate and redact sensitive log content.

## Return

Return the instance and dashboard URL or UID, folder and owner, panel and query, data source, variables, UTC time range, annotation or alert identifiers, compact result summary, and evidence strength.
