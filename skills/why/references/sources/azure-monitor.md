# Azure Monitor

Azure Application Insights, Log Analytics, and Azure Monitor are the primary sources for deployed runtime evidence.

## What to inspect

- Application Insights requests, dependencies, exceptions, traces, custom events, metrics, availability results, and end-to-end transactions.
- Log Analytics tables and workspace-scoped logs.
- Azure Monitor platform metrics, alert rules, workbooks, activity logs, service health, and resource health.
- Deployment or release markers that can align a behavior change with a code change.

## Search process

1. Confirm the subscription, tenant, resource, environment, and time range before querying. Do not assume the current Azure context is correct.
2. Identify the Application Insights resource and its Log Analytics workspace. Prefer the workspace when telemetry is workspace-based.
3. Start with alerts and workbooks owned by the service. Their queries and thresholds show what the team monitors.
4. Run time-bounded KQL with the service, operation, role, environment, cloud resource, error text, trace ID, or deployment window as filters.
5. Aggregate first. Retrieve individual events only when a representative trace or exception is necessary.
6. Correlate telemetry with the exact deployment or commit window. Check neighboring deployments before attributing a change.

Application Insights table names differ by access path and resource type. Workspace tables commonly include `AppRequests`, `AppDependencies`, `AppExceptions`, `AppTraces`, `AppEvents`, and `AppMetrics`. Application Insights resource queries can expose names such as `requests`, `dependencies`, `exceptions`, `traces`, `customEvents`, and `customMetrics`. Inspect the schema before writing the final query.

Example KQL shape:

```kusto
AppExceptions
| where TimeGenerated between (datetime(<start>) .. datetime(<end>))
| where AppRoleName == "<service>"
| summarize Count=count() by bin(TimeGenerated, 1h), ExceptionType
| order by TimeGenerated asc
```

## Strong evidence

- An alert or workbook query whose condition matches the code's guard, timeout, or threshold.
- A representative exception or distributed trace that passes through the target path.
- A measurable error or latency change aligned with the deployment that introduced the code.
- An activity or deployment record that establishes when the relevant version reached an environment.

Runtime correlation is normally Supported or Inferred evidence. It becomes Direct only when a linked annotation, alert note, incident record, or operator statement explicitly gives the reason.

## Limits and safety

- Telemetry retention, sampling, ingestion delay, schema changes, and changed instrumentation can create false gaps.
- A release includes multiple changes. A before-and-after chart does not identify the cause by itself.
- Azure Monitor data can contain personal data, customer data, tokens, or secrets. Use narrow projections and aggregated results. Do not return raw payloads or sensitive values.
- Use read-only queries. Do not change alerts, dashboards, diagnostic settings, retention, sampling, or cloud resources.

## Return

Return the subscription and resource identifiers at a safe level, environment, table or metric, exact KQL or metric query, UTC time range, filters, compact result summary, relevant trace or alert identifier, retention or sampling limits, and evidence strength.
