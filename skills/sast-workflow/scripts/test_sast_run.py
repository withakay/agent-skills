#!/usr/bin/env python3
"""Offline fixture checks. Run: python3 -B scripts/test_sast_run.py"""

import copy
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

import sast_run


class RunTests(unittest.TestCase):
    def setUp(self) -> None:
        fixture = tempfile.TemporaryDirectory(
            prefix=".sast-test-", dir=Path(__file__).parent
        )
        self.addCleanup(fixture.cleanup)
        self.base = Path(fixture.name).resolve()
        self.source = self.base / "source"
        self.source.mkdir()
        (self.source / "handler.py").write_text(
            "def handle(request):\n    return store[request.key]\n", encoding="utf-8"
        )
        for name in ("prompt.txt", "config.json", "workflow.md"):
            (self.base / name).write_text("fixture input\n", encoding="utf-8")
        self.plan = self.base / "plan.json"
        self.write(
            self.plan,
            {
                "scope": "Read the synthetic handler",
                "budget": "One bounded fixture check",
                "source_files": ["handler.py"],
                "inputs": {
                    "prompt": "prompt.txt",
                    "config": "config.json",
                    "workflow": "workflow.md",
                },
                "checks": [
                    {
                        "id": "auth",
                        "skill": "sast-authorization",
                        "reason": "Request-selected record",
                    }
                ],
            },
        )
        self.run = sast_run.initialize(self.source, self.plan, self.base / "run")
        self.result = sast_run.load_json(self.run / "result.json")
        self.loc = {"path": "handler.py", "start_line": 1, "end_line": 2}

    def _fixture_path(self, path: Path) -> Path:
        base = self.base.resolve()
        candidate = (base / path).resolve()
        try:
            candidate.relative_to(base)
        except ValueError as error:
            raise ValueError(
                f"fixture path escapes temporary directory: {path}"
            ) from error
        return candidate

    def write(self, path: Path, value: Any) -> None:
        path = self._fixture_path(path)
        with path.open("w", encoding="utf-8") as stream:
            json.dump(value, stream)

    def save(self) -> None:
        self.write(self.run / "result.json", self.result)

    def validate(self) -> int:
        return sast_run.validate(self.run, self.source, self.plan)

    def test_load_json_rejects_non_file_path(self) -> None:
        with self.assertRaisesRegex(ValueError, "not a regular file"):
            sast_run.load_json(self.base)

    def complete(self) -> None:
        self.result["checks"][0].update(
            status="complete", capability="manual", evidence=[self.loc]
        )
        self.result["coverage"] = {
            "status": "complete",
            "reason": "Declared check reviewed",
            "limitations": [],
        }

    def finding(self) -> dict[str, Any]:
        return {
            "id": "F1",
            "title": "Unresolved object permission",
            "check_ids": ["auth"],
            "root_cause_key": "handler-record-read-permission",
            "actor": "Caller supplying a key",
            "prerequisites": ["Caller can reach handler"],
            "entry_point": self.loc,
            "sensitive_sink": {"action": "Read a stored record", "location": self.loc},
            "controls": [
                {
                    "check": "Object permission",
                    "result": "unknown",
                    "explanation": "Caller policy is outside this fixture",
                    "evidence": [],
                }
            ],
            "mechanism": "The visible handler uses the supplied key; permission enforcement is unresolved.",
            "evidence": [
                {
                    "location": self.loc,
                    "observation": "Key selects stored record",
                    "origin": "source",
                }
            ],
            "cwe": {
                "value": "CWE-862",
                "origin": "model",
                "rationale": "Provisional missing permission check",
            },
            "severity": {
                "value": "unknown",
                "origin": "model",
                "rationale": "Impact not established",
            },
            "validation": "hypothesis",
            "disposition": "open",
            "disposition_reason": "Needs caller analysis",
            "uncertainty": ["Reachability and caller checks unknown"],
            "coverage": "Handler only",
            "tool_refs": [],
            "reproduction": None,
        }

    def test_new_identity_same_snapshot_and_existing_output_refused(self) -> None:
        second = sast_run.initialize(self.source, self.plan, self.base / "second")
        first_manifest = (self.run / "manifest.json").read_bytes()
        first = json.loads(first_manifest)
        other = sast_run.load_json(second / "manifest.json")
        self.assertNotEqual(first["run_id"], other["run_id"])
        self.assertEqual(first["snapshot_id"], other["snapshot_id"])
        with self.assertRaisesRegex(ValueError, "already exists"):
            sast_run.initialize(self.source, self.plan, self.run)
        self.assertEqual(first_manifest, (self.run / "manifest.json").read_bytes())
        self.assertTrue((self.run / "workers" / "auth").is_dir())

    def test_empty_existing_output_and_source_output_refused(self) -> None:
        empty = self.base / "empty"
        empty.mkdir()
        with self.assertRaisesRegex(ValueError, "already exists"):
            sast_run.initialize(self.source, self.plan, empty)
        with self.assertRaisesRegex(ValueError, "outside the source root"):
            sast_run.initialize(self.source, self.plan, self.source / "output")
        self.assertEqual(list(empty.iterdir()), [])

    def test_changed_source_requires_new_snapshot(self) -> None:
        before = sast_run.load_json(self.run / "manifest.json")["snapshot_id"]
        (self.source / "handler.py").write_text("changed source\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "changed; start a fresh run"):
            self.validate()
        second = sast_run.initialize(self.source, self.plan, self.base / "changed")
        self.assertNotEqual(
            before, sast_run.load_json(second / "manifest.json")["snapshot_id"]
        )

    def test_changed_prompt_config_and_plan_detected(self) -> None:
        for path in (self.base / "prompt.txt", self.base / "config.json", self.plan):
            path = self._fixture_path(path)
            with self.subTest(path=path.name):
                before = path.read_bytes()
                with path.open("ab") as stream:
                    stream.write(b"\n")
                with self.assertRaisesRegex(ValueError, "changed; start a fresh run"):
                    self.validate()
                with path.open("wb") as stream:
                    stream.write(before)

    def test_plan_input_path_escape_rejected(self) -> None:
        plan = sast_run.load_json(self.plan)
        plan["inputs"]["prompt"] = "../sast_run.py"
        self.write(self.plan, plan)
        with self.assertRaisesRegex(ValueError, "invalid relative path"):
            sast_run.initialize(self.source, self.plan, self.base / "escaped-input")

    def test_fixture_writer_rejects_paths_outside_temp_dir(self) -> None:
        with self.assertRaisesRegex(ValueError, "escapes temporary directory"):
            self.write(self.base.parent / "outside.json", {})

    def test_absolute_plan_input_is_supported(self) -> None:
        plan = sast_run.load_json(self.plan)
        plan["inputs"]["workflow"] = str(Path(sast_run.__file__).resolve())
        self.write(self.plan, plan)
        run = sast_run.initialize(self.source, self.plan, self.base / "absolute-input")
        self.assertTrue((run / "manifest.json").is_file())

    def test_absolute_plan_input_must_be_canonical(self) -> None:
        helper = Path(sast_run.__file__).resolve()
        # A second leading slash survives normpath but not resolve on POSIX; on
        # Windows the same text has no drive, so it is not absolute at all and
        # local_file rejects it as an invalid relative path instead.
        for name, message in (
            (
                str(helper.parent / ".." / "scripts" / helper.name),
                "canonical absolute path",
            ),
            ("/" + str(helper), "canonical absolute path|invalid relative path"),
        ):
            with self.subTest(name=name):
                plan = sast_run.load_json(self.plan)
                plan["inputs"]["workflow"] = name
                self.write(self.plan, plan)
                with self.assertRaisesRegex(ValueError, message):
                    sast_run.initialize(
                        self.source, self.plan, self.base / "escaped-absolute"
                    )

    def test_validate_only_follows_the_roots_it_is_given(self) -> None:
        other = self.base / "other-source"
        other.mkdir()
        (other / "handler.py").write_bytes((self.source / "handler.py").read_bytes())
        with self.assertRaisesRegex(ValueError, "does not match --source-root"):
            sast_run.validate(self.run, other, self.plan)
        other_plan = self.base / "other-plan.json"
        other_plan.write_bytes(self.plan.read_bytes())
        with self.assertRaisesRegex(ValueError, "does not match --plan"):
            sast_run.validate(self.run, self.source, other_plan)
        manifest = sast_run.load_json(self.run / "manifest.json")
        for key, value in (("source_root", str(other)), ("plan_file", str(other_plan))):
            with self.subTest(key=key):
                tampered = copy.deepcopy(manifest)
                if key == "source_root":
                    tampered["source_root"] = value
                else:
                    tampered["snapshot"]["plan_file"]["path"] = value
                    tampered["snapshot_id"] = sast_run.digest_json(tampered["snapshot"])
                self.write(self.run / "manifest.json", tampered)
                with self.assertRaisesRegex(ValueError, "does not match"):
                    self.validate()

    def test_pending_checks_are_partial_and_cannot_claim_complete(self) -> None:
        self.assertEqual(self.validate(), 3)
        self.result["coverage"]["status"] = "complete"
        self.save()
        with self.assertRaisesRegex(ValueError, "require partial coverage"):
            self.validate()

    def test_complete_bounded_review_and_hypothesis(self) -> None:
        self.complete()
        self.result["findings"] = [self.finding()]
        self.save()
        self.assertEqual(self.validate(), 0)
        self.assertEqual(
            sast_run.load_json(self.run / "result.json")["findings"][0]["validation"],
            "hypothesis",
        )

    def test_unknown_flow_can_only_be_an_uncertain_hypothesis(self) -> None:
        finding = self.finding()
        finding.update(
            entry_point=None, sensitive_sink=None, root_cause_key="candidate:F1"
        )
        self.result["findings"] = [finding]
        self.save()
        self.assertEqual(self.validate(), 3)
        finding["validation"] = "model-confirmed"
        self.save()
        with self.assertRaisesRegex(
            ValueError, "requires a hypothesis with uncertainty"
        ):
            self.validate()

    def test_trace_roles_and_dead_end_limit_validation(self) -> None:
        self.complete()
        finding = self.finding()
        finding["evidence"] = [
            {**finding["evidence"][0], "role": "source"},
            {
                "location": self.loc,
                "observation": "Key comes from a stored value with unknown writers",
                "origin": "model",
                "role": "dead-end",
            },
        ]
        self.result["findings"] = [finding]
        self.save()
        self.assertEqual(self.validate(), 0)
        finding["validation"] = "model-confirmed"
        self.save()
        with self.assertRaisesRegex(ValueError, "ends in a dead-end"):
            self.validate()
        finding["validation"] = "hypothesis"
        finding["evidence"][1]["role"] = "guess"
        self.save()
        with self.assertRaisesRegex(ValueError, "evidence role"):
            self.validate()

    def test_unavailable_scanner_remains_partial_and_manual_is_not_scanner(
        self,
    ) -> None:
        plan = sast_run.load_json(self.plan)
        plan["checks"][0]["skill"] = "sast-semgrep"
        self.write(self.plan, plan)
        self.run = sast_run.initialize(self.source, self.plan, self.base / "scanner")
        self.result = sast_run.load_json(self.run / "result.json")
        self.result["checks"][0].update(
            status="skipped", capability="unavailable", reason="Scanner not installed"
        )
        self.save()
        self.assertEqual(self.validate(), 3)
        self.result["checks"][0].update(status="complete", evidence=[self.loc])
        self.save()
        with self.assertRaisesRegex(ValueError, "unavailable"):
            self.validate()
        self.result["checks"][0]["capability"] = "manual"
        self.save()
        with self.assertRaisesRegex(ValueError, "cannot complete a scanner"):
            self.validate()

    def test_failed_partial_and_skipped_checks_cannot_claim_complete(self) -> None:
        for status, reason in (
            ("failed", "Parser failed"),
            ("partial", "Budget exhausted"),
            ("skipped", "No time"),
        ):
            with self.subTest(status=status):
                self.result["checks"][0].update(
                    status=status, capability="manual", reason=reason
                )
                self.result["coverage"]["status"] = "complete"
                self.save()
                with self.assertRaisesRegex(ValueError, "require partial coverage"):
                    self.validate()

    def test_missing_check_and_cross_run_result_rejected(self) -> None:
        original = copy.deepcopy(self.result)
        self.result["checks"] = []
        self.save()
        with self.assertRaisesRegex(ValueError, "missing planned checks"):
            self.validate()
        self.result = original
        self.result["run_id"] = "different-run"
        self.save()
        with self.assertRaisesRegex(ValueError, "does not match"):
            self.validate()

    def test_bad_locations_and_incomplete_findings_rejected(self) -> None:
        self.complete()
        for location in (
            {"path": "../outside.py", "start_line": 1, "end_line": 1},
            {"path": "/etc/passwd", "start_line": 1, "end_line": 1},
            {"path": "handler.py", "start_line": 0, "end_line": 1},
            {"path": "handler.py", "start_line": 1, "end_line": 99},
            {"path": "handler.py", "start_line": True, "end_line": 1},
            {"path": "handler.py", "start_line": 2, "end_line": 1},
            {"path": "handler.py", "start_line": 1},
        ):
            with self.subTest(location=location):
                finding = self.finding()
                finding["evidence"][0]["location"] = location
                self.result["findings"] = [finding]
                self.save()
                with self.assertRaises(ValueError):
                    self.validate()
        self.result["findings"] = [{"title": "A tool match"}]
        self.save()
        with self.assertRaisesRegex(ValueError, "missing required fields"):
            self.validate()

    def test_source_symlink_escape_and_artifact_escape_rejected(self) -> None:
        outside = self.base / "outside.py"
        outside.write_text("outside\n", encoding="utf-8")
        (self.source / "escape.py").symlink_to(outside)
        plan = sast_run.load_json(self.plan)
        plan["source_files"] = ["escape.py"]
        self.write(self.plan, plan)
        with self.assertRaisesRegex(ValueError, "escapes root"):
            sast_run.initialize(self.source, self.plan, self.base / "escaped")
        plan["source_files"] = ["handler.py"]
        self.write(self.plan, plan)
        self.complete()
        finding = self.finding()
        finding["tool_refs"] = [
            {
                "tool": "fixture",
                "rule_id": "candidate",
                "original_severity": "warning",
                "artifact": "../outside.py",
            }
        ]
        self.result["findings"] = [finding]
        self.save()
        with self.assertRaisesRegex(ValueError, "invalid relative path"):
            self.validate()

    def test_not_applicable_requires_evidence_and_reproduction_requires_record(
        self,
    ) -> None:
        self.result["checks"][0].update(status="not-applicable", capability="manual")
        self.save()
        with self.assertRaisesRegex(ValueError, "must not be empty"):
            self.validate()
        self.complete()
        finding = self.finding()
        finding["validation"] = "reproduced"
        self.result["findings"] = [finding]
        self.save()
        with self.assertRaisesRegex(ValueError, "reproduction: expected object"):
            self.validate()

    def test_cli_partial_and_malformed_json_exit_codes(self) -> None:
        command = [
            sys.executable,
            "-B",
            str(Path(sast_run.__file__)),
            "validate",
            "--run",
            str(self.run),
            "--source-root",
            str(self.source),
            "--plan",
            str(self.plan),
        ]
        pending = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(pending.returncode, 3, pending.stderr)
        self.assertIn("partial coverage", pending.stdout)
        (self.run / "result.json").write_text(
            '{"checks": [], "checks": []}', encoding="utf-8"
        )
        malformed = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(malformed.returncode, 2)
        self.assertIn("duplicate JSON key", malformed.stderr)
        self.assertNotIn("Traceback", malformed.stderr)


class BundleTests(unittest.TestCase):
    def test_frontmatter_links_and_ui_metadata(self) -> None:
        root = Path(__file__).resolve().parent.parent
        content = (root / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = content.split("---\n", 2)[1]
        self.assertEqual(
            re.findall(r"^([a-z_]+):", frontmatter, re.MULTILINE),
            ["name", "description"],
        )
        self.assertIn(f"name: {root.name}\n", frontmatter)
        for path in root.rglob("*.md"):
            for target in re.findall(
                r"\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8")
            ):
                if "://" not in target and not target.startswith("#"):
                    self.assertTrue(
                        (path.parent / target.split("#", 1)[0]).is_file(),
                        f"{path.name}: {target}",
                    )
        metadata = (root / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("$sast-workflow", metadata)
        self.assertIn("SAST workflow", metadata)


if __name__ == "__main__":
    unittest.main(verbosity=2)
