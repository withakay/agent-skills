# Aspire Local Development

Use Aspire only when an Aspire AppHost is present and local reproduction or current development behavior is relevant. Use the Aspire dashboard or the project's existing development workflow; do not require an additional agent integration.

## Search process

1. Identify the AppHost, resources, endpoints, dependencies, and current run.
2. Reproduce the narrow behavior only when the user has requested or authorized execution.
3. Inspect structured logs, traces, spans, resource state, and configuration visible through the Aspire dashboard.
4. Capture correlation or trace IDs and connect them to the same code path in repository evidence.
5. Compare local telemetry with production evidence only when resource names, versions, configuration, and dependencies are comparable.

## Evidence boundary

Aspire telemetry proves what happened in the inspected local run. It can explain current mechanics, reproduce a failure, or test a hypothesis. It does not prove why code was originally written or what happened in production.

## Limits and safety

- Local configuration, dependencies, data volume, identity, and network behavior can differ from deployed environments.
- A successful local run does not disprove an intermittent or production-only failure.
- Do not expose connection strings, tokens, headers, payloads, or personal data from telemetry.
- Do not modify AppHost configuration or application code during a Why investigation.

## Return

Return the AppHost and resource names, local run window, reproduction steps if authorized, relevant logs or trace identifiers, configuration differences that affect interpretation, and evidence strength. Label the source as local evidence.
