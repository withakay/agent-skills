# Run and result contract, version 1

<!-- toc -->
## Contents

- [Fresh local run](#fresh-local-run)
- [Result envelope](#result-envelope)
- [Finding](#finding)
- [Validator limits and exit codes](#validator-limits-and-exit-codes)
<!-- tocstop -->

This skill owns the result schema. Specialists provide evidence to this
contract or provide a documented adapter mapping. They do not create competing
finding schemas. Only the coordinator writes the merged result.

## Fresh local run

The helper uses Python 3.10+ and the standard library. It reads explicitly
listed files, hashes their bytes, and creates a new output directory. It does
not execute scanners, repository code, network requests, or model clients.

Create a local `plan.json` outside the source root. This small example shows
the format; a real plan accounts for every bundled ID in the routing catalog
and each selected optional integration.

```json
{
  "scope": "Review the request handler and shared permission checks",
  "budget": "30 minutes; check allowances and skeptical-review reserve are in config",
  "source_files": ["app/handler.py", "app/policy.py"],
  "inputs": {
    "prompt": "review-request.txt",
    "config": "review-config.json",
    "workflow": "/local/skills/sast-workflow/SKILL.md"
  },
  "checks": [
    {"id": "authorization", "skill": "sast-authorization", "reason": "Handler accesses caller-selected records"}
  ]
}
```

`source_files` contains unique, source-relative POSIX file paths. Include
relevant callers, controls, configuration, and project instructions, not
only potential vulnerable lines. The file list is a declared inventory, not
proof that every relevant file was found. Record omissions in coverage.

Each `checks` entry needs a unique `id`, a `skill`, and a `reason`. An `id` is
1 to 64 lowercase letters, digits, or hyphens, starts with a letter or digit,
and names the worker directory.

`inputs` maps unique labels to local files. The labels `prompt`, `config`, and
`workflow` are required; add others as needed. Relative input paths resolve from
the plan's directory and must remain beneath it; absolute paths are permitted
when explicitly declared and must already be canonical: absolute, normalised,
and without parent traversal. Include the exact task prompt, review configuration,
loaded skills and references, pinned local scanner rules if used, and sanitized
snapshots of existing Apiiro or Sonar evidence selected for the review. Collect
snapshots before initialization and copy them into the selected worker directory
afterward for run-relative `tool_refs`. Keep raw service responses and credentials
out of inputs and artifacts. The configuration states exclusions, tool versions
or absence, permissions, and
budgets. Include the cross-component read and state-change inventory, selected
and deferred path classes with reasons, per-check allowances, and a reserved
skeptical-review allowance. Record deployment and policy unknowns separately
from agreed scope exclusions. Do not include credentials or raw authentication
data. Substantive new worker instructions must be inputs before the run starts.
Record actual budget use and deviations in check reasons and coverage; do not
rewrite frozen inputs to conceal a deferral.

```sh
python3 /local/skills/sast-workflow/scripts/sast_run.py init \
  --source-root /local/source --plan /local/reviews/plan.json \
  --out /local/reviews/new-run

python3 /local/skills/sast-workflow/scripts/sast_run.py validate \
  --run /local/reviews/new-run \
  --source-root /local/source --plan /local/reviews/plan.json
```

`validate` takes the same source root and plan as `init`. The manifest records
both paths, but the helper never follows a path that only the manifest
supplies: the recorded values must equal the arguments, and the drift checks
read the source tree and plan the operator names.

The output parent must already exist. An existing `--out`, including an
empty directory or symlink, is an error. The helper never deletes or resumes
it. Each run has a new UUID. Its `snapshot_id` hashes the plan, source hashes,
input hashes, and helper hash. Never edit `manifest.json`. The helper checks
for drift again during validation. Changed or expanded inputs need a new run.
Keep source stable during the run. These hashes are not an atomic filesystem
snapshot or a defense against concurrent malicious file replacement.

The helper creates `workers/CHECK_ID/` for disjoint evidence output and a
coordinator-owned `result.json` template. Workers return candidate findings
and check evidence to their directory. They use the same finding fields below.
The coordinator merges these into `result.json`; no automatic merge is assumed.

## Result envelope

Required keys are `schema_version` with value `1`, `run_id`, `snapshot_id`,
`coverage`, `checks`, and `findings`. IDs must match the manifest. Preserve
every planned check exactly once; do not remove a failed or empty check.

`coverage` is an object:

| Field | Type and meaning |
| --- | --- |
| `status` | `complete` or `partial`, for the declared scope only |
| `reason` | Nonempty explanation of the coverage conclusion |
| `limitations` | Array of nonempty strings identifying exclusions, unavailable capabilities, uncertainties, and remaining work; may be empty |

Each `checks` entry has:

| Field | Type and meaning |
| --- | --- |
| `id`, `skill` | Exact strings from the plan |
| `status` | `selected`, `complete`, `not-applicable`, `skipped`, `failed`, or `partial` |
| `capability` | `unassessed`, `manual`, `specialist`, `scanner`, or `unavailable`, describing what was actually available and used |
| `reason` | Nonempty explanation, including selection or deferral reason, budget deviations, and fallback or failure details |
| `evidence` | Array of source locations supporting the review or routing decision; required for complete and not-applicable checks |

Coverage must be partial if any check is pending, skipped, failed, partial,
unassessed, or unavailable. A not-applicable check requires source evidence.
A successful empty scanner result can complete its own check only after exit
status, parse failures, exclusions, and rule coverage are investigated.
The helper checks status consistency, not whether the evidence justifies it.

## Finding

Every finding, including normalized tool candidates, uses these fields:

| Field | Type and meaning |
| --- | --- |
| `id` | Nonempty run-local ID |
| `title` | Short description of the failed control |
| `check_ids` | Nonempty array of contributing planned check IDs |
| `root_cause_key` | Grouping key derived from the affected operation, failed control, and mechanism; never from title alone. Use a unique `candidate:ID` while the root cause is unknown |
| `actor` | Nonempty description of who can attempt the action and their authority |
| `prerequisites` | Array of strings describing required access, state, deployment conditions, or knowledge; empty means none known |
| `entry_point` | Source location where the relevant flow starts, or `null` if unknown in a hypothesis |
| `sensitive_sink` | Object with nonempty `action` and source `location`, or `null` if unknown in a hypothesis |
| `controls` | Nonempty array of objects with `check`, `result`, `explanation`, and `evidence`. `result` is `present`, `absent`, or `unknown`; `evidence` is an array of source locations |
| `mechanism` | Nonempty causal argument connecting the actor, data flow, failed control, and consequence |
| `evidence` | Nonempty array of objects with source `location`, nonempty `observation`, and `origin` as `source`, `tool`, `model`, or `execution`. List items in trace order. Optional `role` is `source`, `hop`, `control`, `sink`, or `dead-end`; a `dead-end` item marks where tracing stopped without reaching a source, and requires a `hypothesis` with uncertainty |
| `cwe` | Object with `value` as `CWE-N` or `unmapped`, `origin` as `tool`, `model`, or `human`, and nonempty `rationale` |
| `severity` | Object with `value` as `unknown`, `info`, `low`, `medium`, `high`, or `critical`, plus `origin` and `rationale` as for CWE |
| `validation` | `hypothesis`, `model-confirmed`, or `reproduced` |
| `disposition` | `open`, `false-positive`, `risk-accepted`, `out-of-scope`, or `fixed` |
| `disposition_reason` | Explanation; for non-open states cite the counterevidence, scope decision, existing acceptance authority, or fresh fix evidence |
| `uncertainty` | Array of strings stating unresolved assumptions and missing evidence |
| `coverage` | Nonempty description of the branches, controls, and conditions investigated and those not investigated |
| `tool_refs` | Array of objects with nonempty `tool`, `rule_id`, `original_severity`, and `artifact`, a run-relative local file path; empty for manual candidates |
| `reproduction` | `null` unless reproduced; then an object with nonempty `authorization`, `observed`, and `artifact`, a run-relative file path |

A source location is exactly `{ "path": "app/handler.py", "start_line": 4,
"end_line": 9 }`. Lines are inclusive and 1-based. Paths must be in the declared
inventory and resolve to regular files inside the source root. Absolute paths,
parent traversal, backslashes, invalid ranges, and escaped symlinks are invalid.
Evidence files must be UTF-8. Artifact paths must be relative to the run, resolve
inside it, and exist. Do not include secrets or unnecessary source excerpts.

Keep a tool-only candidate as `hypothesis`; use `unknown` controls or severity
when necessary instead of inventing facts. Use `null` for an unknown entry point
or sink and explain the gap in `uncertainty`. Label an unknown actor explicitly.
A scanner match location alone need not be an entry point or a sink.
Tool references preserve original severity;
the `severity` field is the current assessment with its stated origin.

`model-confirmed` requires a source-supported static argument. `reproduced`
requires separately authorized execution and observed evidence; a suggested
payload, a passing unit test, or a validator exit code is not reproduction.
`false-positive`, `risk-accepted`, `out-of-scope`, and `fixed` are distinct
dispositions. None can be inferred from disappearance from scanner output.

## Validator limits and exit codes

- `0`: the result passed structural and location checks, and declares complete
  coverage. This does not prove security, reachability, authority, or severity.
- `2`: invalid structure, missing or changed inputs, malformed evidence, or an
  inconsistent coverage claim. Correct the result or start a fresh run.
- `3`: structurally valid result with explicitly partial coverage. Preserve the
  result and report the gaps; do not turn this into a success by dropping checks.

The helper verifies types, required fields, IDs, hashes, file containment, and
line bounds. It cannot prove that all relevant source was listed, that the
reasoning is correct, that authorization is genuine, or that two findings have
the same root cause. Evidence review remains required.

Run the offline helper and bundle checks with:

```sh
python3 -B /local/skills/sast-workflow/scripts/test_sast_run.py
```
