#!/usr/bin/env python3
"""Create fresh SAST runs and validate evidence structure, paths, and freshness."""

import argparse
import hashlib
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path, PurePath, PurePosixPath
from typing import Any


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def text(value: Any, label: str) -> str:
    require(
        isinstance(value, str) and bool(value.strip()),
        f"{label}: expected nonempty text",
    )
    return value


def object_with(value: Any, fields: str, label: str) -> dict[str, Any]:
    require(isinstance(value, dict), f"{label}: expected object")
    require(
        set(fields.split()) <= value.keys(),
        f"{label}: missing required fields: {fields}",
    )
    return value


def array(value: Any, label: str, nonempty: bool = False) -> list[Any]:
    require(isinstance(value, list), f"{label}: expected array")
    require(not nonempty or bool(value), f"{label}: must not be empty")
    return value


def texts(value: Any, label: str, nonempty: bool = False) -> list[str]:
    return [text(item, label) for item in array(value, label, nonempty)]


def choice(value: Any, allowed: str, label: str) -> None:
    require(
        isinstance(value, str) and value in allowed.split(),
        f"{label}: expected {allowed}",
    )


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    path = path.resolve(strict=True)
    require(path.is_file(), f"not a regular file: {path}")
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)


def write_json(path: Path, value: Any) -> None:
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write("\n")


def digest_file(path: Path) -> str:
    require(path.is_file(), f"not a regular file: {path}")
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def digest_json(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def local_file(root: Path, value: Any) -> Path:
    name = text(value, "relative path")
    posix = PurePosixPath(name)
    require(
        not posix.is_absolute()
        and ".." not in posix.parts
        and "\\" not in name
        and "\x00" not in name
        and name != "."
        and posix.as_posix() == name,
        f"invalid relative path: {name}",
    )
    path = (root / name).resolve(strict=True)
    require(
        path.is_relative_to(root) and path.is_file(),
        f"file escapes root or is not regular: {name}",
    )
    return path


def canonical_path(value: Any, label: str) -> Path:
    """Accept an explicitly declared absolute input path only in canonical form.

    The plan may name inputs outside its own directory. Such a value is checked
    as text before any filesystem access: it must be absolute, already
    normalised, and free of parent traversal. A POSIX path with two leading
    separators is rejected as well: ``normpath`` keeps it, ``resolve`` does not,
    so it would be followed as a different path than the one declared.
    """
    name = text(value, label)
    pure = PurePath(name)
    require(
        pure.is_absolute()
        and ".." not in pure.parts
        and "\x00" not in name
        and not name.startswith("//")
        and os.path.normpath(name) == name,
        f"{label}: expected a canonical absolute path: {name}",
    )
    return Path(name).resolve(strict=True)


def capture(source_root: Path, plan_path: Path) -> dict[str, Any]:
    plan = object_with(
        load_json(plan_path), "scope budget source_files inputs checks", "plan"
    )
    text(plan["scope"], "scope")
    text(plan["budget"], "budget")
    sources = texts(plan["source_files"], "source_files", nonempty=True)
    require(len(set(sources)) == len(sources), "duplicate source files")
    source_hashes = {
        name: digest_file(local_file(source_root, name)) for name in sources
    }
    inputs = object_with(plan["inputs"], "prompt config workflow", "inputs")
    input_hashes = {}
    for label, name in inputs.items():
        text(label, "input label")
        input_name = text(name, "input path")
        if PurePath(input_name).is_absolute():
            path = canonical_path(input_name, "input path")
            require(path.is_file(), f"not a regular file: {path}")
        else:
            path = local_file(plan_path.parent, input_name)
        input_hashes[label] = {"path": str(path), "sha256": digest_file(path)}
    check_ids = set()
    for item in array(plan["checks"], "checks", nonempty=True):
        check = object_with(item, "id skill reason", "planned check")
        check_id = text(check["id"], "check id")
        require(
            bool(re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", check_id)), "invalid check id"
        )
        require(check_id not in check_ids, "duplicate check id")
        check_ids.add(check_id)
        text(check["skill"], "skill")
        text(check["reason"], "check reason")
    return {
        "plan": plan,
        "plan_file": {"path": str(plan_path), "sha256": digest_file(plan_path)},
        "sources": source_hashes,
        "inputs": input_hashes,
        "helper_sha256": digest_file(Path(__file__).resolve()),
    }


def initialize(source_root: Path, plan_path: Path, output: Path) -> Path:
    source_root = source_root.resolve(strict=True)
    require(source_root.is_dir(), "source root is not a directory")
    output = output.parent.resolve(strict=True) / output.name
    require(
        not output.is_relative_to(source_root), "output must be outside the source root"
    )
    require(
        not output.exists() and not output.is_symlink(),
        "output already exists; choose a fresh path",
    )
    snapshot = capture(source_root, plan_path.resolve(strict=True))
    manifest = {
        "schema_version": 1,
        "run_id": str(uuid.uuid4()),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_root": str(source_root),
        "snapshot_id": digest_json(snapshot),
        "snapshot": snapshot,
    }
    output.mkdir(exist_ok=False)
    write_json(output / "manifest.json", manifest)
    (output / "workers").mkdir()
    checks = []
    for check in snapshot["plan"]["checks"]:
        (output / "workers" / check["id"]).mkdir()
        checks.append(
            {**check, "status": "selected", "capability": "unassessed", "evidence": []}
        )
    write_json(
        output / "result.json",
        {
            "schema_version": 1,
            "run_id": manifest["run_id"],
            "snapshot_id": manifest["snapshot_id"],
            "coverage": {
                "status": "partial",
                "reason": "Review not finished",
                "limitations": ["Checks pending"],
            },
            "checks": checks,
            "findings": [],
        },
    )
    return output


def validate(run: Path, source_root: Path, plan: Path) -> int:
    """Check a run against the source root and plan the operator names.

    The manifest records both paths, but a manifest is data inside the run
    directory, so the helper never follows a path that only the manifest
    supplies: the recorded values must equal the trusted arguments.
    """
    run = run.resolve(strict=True)
    source_root = source_root.resolve(strict=True)
    require(source_root.is_dir(), "source root is not a directory")
    plan_path = plan.resolve(strict=True)
    manifest = object_with(
        load_json(local_file(run, "manifest.json")),
        "schema_version run_id source_root snapshot_id snapshot",
        "manifest",
    )
    require(
        type(manifest["schema_version"]) is int and manifest["schema_version"] == 1,
        "unsupported manifest version",
    )
    uuid.UUID(text(manifest["run_id"], "run_id"))
    snapshot = object_with(manifest["snapshot"], "plan_file", "snapshot")
    plan_file = object_with(snapshot["plan_file"], "path", "plan_file")
    require(
        text(manifest["source_root"], "source_root") == str(source_root),
        "manifest source root does not match --source-root",
    )
    require(not run.is_relative_to(source_root), "run must be outside source root")
    require(
        digest_json(snapshot) == manifest["snapshot_id"],
        "manifest snapshot hash mismatch",
    )
    require(
        text(plan_file["path"], "plan path") == str(plan_path),
        "manifest plan path does not match --plan",
    )
    current = capture(source_root, plan_path)
    require(
        current == snapshot,
        "source, prompt, configuration, plan, or helper changed; start a fresh run",
    )
    result = object_with(
        load_json(local_file(run, "result.json")),
        "schema_version run_id snapshot_id coverage checks findings",
        "result",
    )
    require(
        type(result["schema_version"]) is int and result["schema_version"] == 1,
        "unsupported result version",
    )
    for key in ("run_id", "snapshot_id"):
        require(result[key] == manifest[key], f"result {key} does not match manifest")
    line_counts: dict[str, int] = {}

    def location(value: Any) -> None:
        loc = object_with(value, "path start_line end_line", "location")
        require(len(loc) == 3, "location has unexpected fields")
        name = text(loc["path"], "location path")
        require(
            name in snapshot["sources"], f"location not in source inventory: {name}"
        )
        path = local_file(source_root, name)
        if name not in line_counts:
            line_counts[name] = len(path.read_text(encoding="utf-8").splitlines())
        start, end = loc["start_line"], loc["end_line"]
        require(
            type(start) is int and type(end) is int, "line numbers must be integers"
        )
        require(
            1 <= start <= end <= line_counts[name], f"line range outside file: {name}"
        )

    def locations(value: Any, nonempty: bool = False) -> None:
        for item in array(value, "locations", nonempty):
            location(item)

    coverage = object_with(result["coverage"], "status reason limitations", "coverage")
    choice(coverage["status"], "complete partial", "coverage status")
    text(coverage["reason"], "coverage reason")
    texts(coverage["limitations"], "limitations")
    planned = {check["id"]: check for check in snapshot["plan"]["checks"]}
    seen_checks = set()
    incomplete = False
    for item in array(result["checks"], "checks"):
        check = object_with(item, "id skill status capability reason evidence", "check")
        check_id = text(check["id"], "check id")
        require(
            check_id in planned and check_id not in seen_checks,
            "unknown or duplicate check id",
        )
        seen_checks.add(check_id)
        require(check["skill"] == planned[check_id]["skill"], "check skill changed")
        choice(
            check["status"],
            "selected complete not-applicable skipped failed partial",
            "check status",
        )
        choice(
            check["capability"],
            "unassessed manual specialist scanner unavailable",
            "capability",
        )
        text(check["reason"], "check reason")
        finished = check["status"] in ("complete", "not-applicable")
        require(
            not finished or check["capability"] not in ("unassessed", "unavailable"),
            "unavailable or unassessed capability cannot complete a check",
        )
        if check["skill"] == "sast-semgrep" and check["status"] == "complete":
            require(
                check["capability"] == "scanner",
                "manual review cannot complete a scanner check",
            )
        locations(check["evidence"], nonempty=finished)
        incomplete |= not finished
    require(seen_checks == planned.keys(), "missing planned checks")
    require(
        not incomplete or coverage["status"] == "partial",
        "incomplete checks require partial coverage",
    )

    finding_ids = set()
    root_causes = set()
    for item in array(result["findings"], "findings"):
        finding = object_with(
            item,
            "id title check_ids root_cause_key actor prerequisites entry_point "
            "sensitive_sink controls mechanism evidence cwe severity validation disposition "
            "disposition_reason uncertainty coverage tool_refs reproduction",
            "finding",
        )
        for key in (
            "id",
            "title",
            "root_cause_key",
            "actor",
            "mechanism",
            "disposition_reason",
            "coverage",
        ):
            text(finding[key], key)
        require(finding["id"] not in finding_ids, "duplicate finding id")
        finding_ids.add(finding["id"])
        require(
            finding["root_cause_key"] not in root_causes,
            "duplicate root_cause_key; coordinator must merge",
        )
        root_causes.add(finding["root_cause_key"])
        contributors = texts(finding["check_ids"], "check_ids", nonempty=True)
        require(set(contributors) <= seen_checks, "finding references unknown checks")
        texts(finding["prerequisites"], "prerequisites")
        texts(finding["uncertainty"], "uncertainty")
        choice(
            finding["validation"], "hypothesis model-confirmed reproduced", "validation"
        )
        for key in ("entry_point", "sensitive_sink"):
            if finding[key] is None:
                require(
                    finding["validation"] == "hypothesis"
                    and bool(finding["uncertainty"]),
                    f"unknown {key} requires a hypothesis with uncertainty",
                )
            elif key == "entry_point":
                location(finding[key])
            else:
                sink = object_with(finding[key], "action location", key)
                text(sink["action"], "sink action")
                location(sink["location"])
        for value in array(finding["controls"], "controls", nonempty=True):
            control = object_with(value, "check result explanation evidence", "control")
            text(control["check"], "control check")
            text(control["explanation"], "control explanation")
            choice(control["result"], "present absent unknown", "control result")
            locations(control["evidence"], nonempty=control["result"] != "unknown")
        for value in array(finding["evidence"], "evidence", nonempty=True):
            evidence = object_with(value, "location observation origin", "evidence")
            location(evidence["location"])
            text(evidence["observation"], "observation")
            choice(evidence["origin"], "source tool model execution", "evidence origin")
            if "role" in evidence:
                choice(
                    evidence["role"],
                    "source hop control sink dead-end",
                    "evidence role",
                )
                require(
                    evidence["role"] != "dead-end"
                    or (
                        finding["validation"] == "hypothesis"
                        and bool(finding["uncertainty"])
                    ),
                    "a trace that ends in a dead-end requires a hypothesis with uncertainty",
                )
        for key in ("cwe", "severity"):
            assessment = object_with(finding[key], "value origin rationale", key)
            choice(assessment["origin"], "tool model human", f"{key} origin")
            text(assessment["rationale"], f"{key} rationale")
            if key == "cwe":
                require(
                    bool(
                        re.fullmatch(
                            r"CWE-[1-9][0-9]*|unmapped",
                            text(assessment["value"], "CWE"),
                        )
                    ),
                    "invalid CWE",
                )
            else:
                choice(
                    assessment["value"],
                    "unknown info low medium high critical",
                    "severity",
                )
        choice(
            finding["disposition"],
            "open false-positive risk-accepted out-of-scope fixed",
            "disposition",
        )
        for value in array(finding["tool_refs"], "tool_refs"):
            ref = object_with(
                value, "tool rule_id original_severity artifact", "tool reference"
            )
            for key in ("tool", "rule_id", "original_severity"):
                text(ref[key], key)
            local_file(run, ref["artifact"])
        if finding["validation"] == "reproduced":
            record = object_with(
                finding["reproduction"],
                "authorization observed artifact",
                "reproduction",
            )
            text(record["authorization"], "reproduction authorization")
            text(record["observed"], "reproduction observation")
            local_file(run, record["artifact"])
        else:
            require(
                finding["reproduction"] is None,
                "only reproduced findings can have a reproduction record",
            )
    return 3 if coverage["status"] == "partial" else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="create a new run; refuse existing outputs")
    init.add_argument("--source-root", type=Path, required=True)
    init.add_argument("--plan", type=Path, required=True)
    init.add_argument("--out", type=Path, required=True)
    check = commands.add_parser(
        "validate", help="check result structure, locations, and input freshness"
    )
    check.add_argument("--run", type=Path, required=True)
    check.add_argument("--source-root", type=Path, required=True)
    check.add_argument("--plan", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "init":
            print(initialize(args.source_root, args.plan, args.out))
            return 0
        code = validate(args.run, args.source_root, args.plan)
        print(
            "Valid structure; partial coverage"
            if code == 3
            else "Valid structure; declared scope complete"
        )
        print(
            "Location and hash checks are not semantic proof or a clean security verdict."
        )
        return code
    except (OSError, ValueError, TypeError, KeyError, RecursionError) as error:
        print(f"Invalid run: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
