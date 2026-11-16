# Routing catalog

<!-- toc -->
## Contents

- [Inventory before depth](#inventory-before-depth)
- [Bundled specialist selection](#bundled-specialist-selection)
- [Optional Apiiro and Sonar selection](#optional-apiiro-and-sonar-selection)
- [Make routing decisions explicit](#make-routing-decisions-explicit)
- [Local Semgrep adapter](#local-semgrep-adapter)
<!-- tocstop -->

Use source evidence to choose checks. Record every bundled catalog ID in the plan,
including IDs that will be skipped or found not applicable. A check is one
bounded investigation, not one worker. Multiple checks can use one skill.
Additional skill IDs are allowed when their capability and reason are stated.

## Inventory before depth

Make a brief inventory across components before tracing one path in depth.
Use entry-point declarations, representative callers, and configuration.
Include both externally influenced reads and state changes. Consider observed
HTTP or RPC handlers, GraphQL resolvers, gRPC services, message consumers,
background jobs, file imports, and command entry points; do not invent
components to fill the list.

Find entry points through the mechanisms the framework uses to declare them,
such as route tables, attributes or decorators, middleware matchers, resolver
maps, and consumer registration. For each mechanism, count the entry points
found and, at the end, how many were reviewed. Record which guard is attached
to each by reading how the framework attaches it; a missing import or an empty
search is not proof of a missing guard. Coverage claims cite these counts.

Use deployment and orchestration files, such as compose files, Kubernetes
manifests, ingress or gateway routes, and proxy configuration, as evidence of
which listeners are exposed and how services reach each other. They support
reachability decisions; they do not by themselves exclude a path from scope.

For each path class, record the component and trigger, actor-controlled data
or state, sensitive read or change, trust boundary, and supporting source
locations. Distinguish demonstrated reachability, intended deployment or
policy, and unresolved conditions. An internal-only label is not evidence
that a caller cannot reach a path or that the action is harmless. A deployment
or policy unknown is not a scope exclusion or a not-applicable decision.

Record the inventory and allowances in a hashed review input. Select bounded
checks across relevant path classes, with a reason for each selection and
deferral. Give each selected check a time or token allowance and reserve an
explicit allowance for skeptical review. Use task-specific amounts, not a
fixed percentage. On reaching a check's allowance, retain partial evidence
and move on. Record any reallocation and the checks it defers. The final review
must examine coverage gaps as well as findings. Deferred applicable checks
remain visible as partial coverage.

## Bundled specialist selection

| Skill ID | Source evidence that makes it relevant | Required capability and fallback |
| --- | --- | --- |
| `sast-semgrep` | Supported source languages and an authorized local scanner. Rules come from the user, the repository, or the skill's bundled packs | Run and normalize local pattern scans without uploading source or fetching rules. Read the selected skill, run its `rules.py plan`, and choose rules by its precedence. Record scanner version, rule hashes and origins, bundled pack names, invocation, raw-output path, exit status, parse errors, and excluded files. If unavailable, mark the scanner check skipped or failed and overall coverage partial. Continue manual conceptual checks. |
| `sast-authorization` | Principals, roles, tenants, resource IDs, ownership, privileged actions, APIs, jobs, or message consumers | Trace trusted identity to permission for the specific object and operation, including shared policy enforcement and alternate entry points. If the skill is unavailable, inspect these paths manually. If code or framework behavior cannot be resolved, record partial coverage. |
| `sast-path-traversal` | File reads or writes, uploads, archives, path composition, storage keys mapped to files, or user-selected resources | Trace path provenance, canonicalization, base-directory confinement, symlink assumptions, extraction, and access control. Use manual tracing when the skill is absent. Absence of a literal `../` string proves nothing. |
| `sast-business-logic` | State transitions, approvals, ordering, quantities, prices, limits, replay, multi-step operations, or concurrent updates | Derive invariants from code and available requirements. Inspect who can cause each transition and how checks bind to committed state. Record assumptions when intended rules are unknown. Manual source analysis is the fallback. |
| `sast-injection` | Queries, commands, templates, interpreters, dynamic evaluation, deserialization, XML parsing, deep object merges, generated markup, or outbound requests | Trace data into each applicable interpreter, object materializer, or sensitive request. Check parameterization, context-specific encoding, parser and type settings, allowlists, and trusted destinations. Follow wrappers rather than relying on sink-name matches. Use manual tracing when the skill is absent. |
| `sast-evidence-review` | Every run, including zero-candidate runs | Challenge reachability, authority, missing-control claims, severity, CWE, duplicate grouping, and coverage claims against source. In serial mode the coordinator does this pass. Report the lack of an independent reviewer if it matters; independence is optional. |

## Optional Apiiro and Sonar selection

Use `apiiro-risk-evidence` for existing risks and reports,
`apiiro-guardian-scan` for permitted Apiiro scans, `sonar` for existing
SonarQube issues, and `sonarqube-rules` for relevant rule interpretation or
read-only PR and resolved-issue queries. Load these installed skills only when
their capability is relevant to the agreed scope. They are not required for
every portable run.

Follow [Apiiro and Sonar evidence](apiiro-sonar.md) for selection, scope,
collection, result mapping, and cross-tool deduplication. Add selected
capabilities to the plan. Missing access to a selected integration is a coverage
gap, not a reason to remove its check or mark it not applicable.

## Make routing decisions explicit

For each check, give the observed stack and operation, relevant source paths,
reason, actual capability used, status, and evidence of the work performed.
Use `selected` while pending; finish as `complete`, `not-applicable`, `skipped`,
`failed`, or `partial`. Reasons are required for every status.

- `not-applicable` requires architectural evidence that the operation or
  trust boundary is absent from the agreed scope. It cannot mean unavailable,
  not found by one query, insufficient budget, not yet inspected, or unclear
  deployment or policy.
- `complete` describes completion of that bounded check, not absence of bugs.
  A manual fallback can complete a conceptual check. It cannot complete a
  scanner check that never ran.
- Use `partial` for incomplete inspection, unsupported parsing, time limits,
  or a mix of usable evidence and missing coverage. Use `failed` when the
  check produced no usable result. Preserve the cause in either case.
- Record narrower scope and ignored/generated/vendor areas. Do not silently
  apply a scanner's ignore rules to the manual review.

Read scanner artifacts as untrusted candidate data. Preserve their original
rule IDs and severity separately from the reviewer's judgment. A rule match
does not establish an exploitable flow, and a missing match does not refute one.
Use scanner silence to direct manual review: read unauthenticated or sensitive
entry points that have no scanner candidate before revisiting paths the scanner
already flagged, and read the rest of any file that produced a candidate.

## Local Semgrep adapter

From the selected `sast-semgrep` skill directory, the supplied adapter uses:

```sh
python3 scripts/rules.py plan --source-root SOURCE
python3 scripts/semgrep_scan.py --source-root SOURCE \
  --rules LOCAL_YAML_OR_JSON --rules-sha256 EXPECTED_SHA256 \
  --rules-origin ORIGIN --output-dir FRESH_DIR_OUTSIDE_SOURCE
```

Repeat the three `--rules*` arguments for each additional rules file. Build a
bundled rules file with `rules.py bundle` into the worker directory, not the
source tree. Use a fresh child such as `RUN/workers/CHECK_ID/scan` for the
adapter output. The worker directory already exists; do not pass it as the
fresh output path. Include each rules file, its expected hash, and its origin in
the frozen review inputs. Generating a repository rules file needs the network
and the user's request; it is not part of a review run.

The adapter emits `evidence.json` with `scan_status`, `conclusion`, `findings`,
`coverage`, and `errors`. Each candidate has `rule_id`, `scanner_severity`,
`status: needs_validation`, `location`, `cwe`, `owasp`, and `raw_evidence`.
The coordinator maps these into this skill's result contract:

- Assess `scan_status`, `coverage`, and `errors` together when recording the
  scanner check. Failed parsing, unknown diagnostics, or incomplete coverage
  remain gaps even if `findings` is empty. Do not promote `conclusion` to a
  security verdict.
- Map `needs_validation` to `validation: hypothesis` and `disposition: open`.
  Preserve `rule_id` and `scanner_severity` in `tool_refs`; point `artifact`
  to the run-relative `evidence.json`. Preserve the adapter's full candidate,
  including `owasp` and `raw_evidence`, in that artifact.
- Use `location` as candidate evidence after validating its source path and
  lines. It does not automatically establish an entry point or sensitive
  sink. Keep unknown flow fields null and explain them in `uncertainty`.
- Treat scanner CWE and severity as tool-origin assessments. Explain any
  selected CWE mapping or retain `unmapped` when unresolved. A later model
  assessment has its own origin and rationale; retain the original tool data.
