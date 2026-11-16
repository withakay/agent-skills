# Apiiro and Sonar evidence

Use these optional installed skills when the user requests their evidence or
repository configuration identifies a relevant integration within the permitted
tool scope. They are not bundled dependencies. A portable local-only review
does not require remote access. Add a planned check for each selected capability;
record why other integrations were not selected in the review configuration.

| Skill ID | Select for | SAST use |
| --- | --- | --- |
| `apiiro-risk-evidence` | Existing Apiiro risks, supplied reports, or Apiiro records linked to upstream scanners | Read scoped risks and sanitized evidence. Reconcile repository, branch, risk IDs, capture time, and current state. |
| `apiiro-guardian-scan` | A requested or configured Apiiro secrets, OSS, or diff scan within the authorized review scope | Run only the selected, permitted scan mode. Secrets and OSS checks supplement source-led SAST; they do not replace source tracing. |
| `sonar` | Existing SonarQube issues for a project, branch, or pull request | Resolve the exact project key and retrieve scoped, paginated issues. This retrieves an existing analysis; it does not run one. |
| `sonarqube-rules` | Exact Sonar rule interpretation, catalog checks, or PR and resolved-issue evidence needed for a candidate | Read relevant catalog entries or use the scoped read-only query helpers. Catalog checks are advisory, and resolved issues are a snapshot rather than a full transition history. |

Load the selected skills by ID through the current harness. Follow their
installed CLI help, authentication, scope resolution, and pagination procedures.
Do not copy credentials between tools or assume their environment variables are
interchangeable. Keep tokens out of arguments, files, and reports.

## Collect within the review scope

1. Confirm the repository or project identity and the requested branch or PR
   before retrieval. Record the server default if no branch or PR was requested.
   A checkout does not select server-side scope. Record the analysis revision
   and time when available; a matching branch name alone does not prove that
   the analysis matches the frozen source.
2. Use existing reports or authorized read-only service queries first. Confirm
   network and upload behavior before running an Apiiro scan. A fast-scan label
   does not grant permission to transmit source. New remote scans and code
   uploads require separate authorization. The workflow does not install hooks,
   bypass hooks, run builds or tests, start Sonar analysis, edit rule catalogs,
   or change issue, risk, or suppression state.
3. Capture raw responses and errors only in restricted temporary storage
   outside the source and run inputs. Retain sanitized evidence in the run;
   omit secrets, source excerpts, credential-bearing URLs, and unreviewed HTML.
   Remove temporary captures when no longer needed. Preserve safe record IDs,
   rule IDs, locations, upstream scanner names, original severities, statuses,
   query scope, filters, capture time, and pagination counts.
4. Collect existing evidence before freezing the run. Include each sanitized
   snapshot and selected skill resource in `inputs`. Copy those snapshots into
   the appropriate `workers/CHECK_ID/` directory after initialization for local
   artifact references. A fresh authorized scan can produce evidence there
   during the run using frozen scan configuration. Changed snapshots, source
   inventory, or review inputs require a fresh run.

Report denied access, missing credentials or skills, pending scans, parse
failures, and incomplete pagination as gaps in selected checks. Do not turn
errors into empty results. Continue manual source checks; they cannot complete
a scan or retrieval that did not succeed. Optional integrations outside the
agreed scope need no check. Once selected, an unavailable integration remains
visible as skipped or failed with partial overall coverage.

## Map to the shared result contract

- Use `capability: specialist` for successful evidence retrieval or rule
  interpretation through these skills, `scanner` for a scan actually run,
  and `manual` for a conceptual source fallback. Record commands, filters,
  versions, scan or analysis identity, and limitations in sanitized artifacts
  and check reasons. Retrieved issues do not prove that a current scan ran.
- Keep security-relevant candidates for source investigation. Record why
  unrelated quality, style, or dependency-only records are outside the agreed
  SAST scope. Neither Apiiro risk severity nor Sonar rule type alone establishes
  an exploitable flow.
- Start candidates as `validation: hypothesis` and `disposition: open`.
  Preserve original remote statuses in artifacts. Change the local disposition
  only with the evidence required by the result contract. An `Accepted`,
  `Ignored`, `FIXED`, or missing record does not by itself prove acceptance
  authority, a false positive, or a fix in the reviewed source.
- Verify each path and line against the frozen inventory before adding source
  evidence. Remote component keys and URLs are not local paths. If a stale or
  unlocated record cannot be mapped, retain it in the sanitized check artifact
  and explain the unresolved coverage gap. Do not invent a location to satisfy
  the finding schema. Map known locations only; keep unknown flow fields null
  with explicit uncertainty.
- Add `tool_refs` with the collecting tool, exact rule ID, original severity,
  and run-relative sanitized artifact path. Use the literal `unknown` when a
  rule or severity is absent, and explain the missing field in the artifact.
  Retain Apiiro risk IDs, Sonar issue keys, upstream scanner and external rule
  IDs in that artifact. Keep the reviewer's CWE and severity assessment separate.
- Match stable record IDs and explicit cross-tool links before grouping. An
  Apiiro record labelled SonarQube does not prove a current direct Sonar issue
  exists. After source tracing establishes the same failed control and affected
  operation, merge duplicate candidates and retain all contributing check IDs
  and tool references. Matching titles, rule IDs, or nearby lines alone are
  insufficient. Preserve conflicting state or severity observations with their
  scopes and capture times.

Complete retrieval means the declared query was exhausted, not that all source
was scanned or reviewed. Cite relevant source or configuration locations in
check evidence and record query completeness in the artifact. Continue the
workflow's manual tracing and skeptical evidence review, including sensitive
entry points with no scanner candidates.
