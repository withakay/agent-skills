#!/usr/bin/env python3
"""Tests for in-process tui-test demo evidence execution."""

from __future__ import annotations

import asyncio
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))

DEMO_SPEC = importlib.util.spec_from_file_location("demo", SCRIPTS / "demo.py")
assert DEMO_SPEC and DEMO_SPEC.loader
DEMO = importlib.util.module_from_spec(DEMO_SPEC)
sys.modules[DEMO_SPEC.name] = DEMO
DEMO_SPEC.loader.exec_module(DEMO)

EVIDENCE_SPEC = importlib.util.spec_from_file_location(
    "evidence", SCRIPTS / "evidence.py"
)
assert EVIDENCE_SPEC and EVIDENCE_SPEC.loader
EVIDENCE = importlib.util.module_from_spec(EVIDENCE_SPEC)
sys.modules[EVIDENCE_SPEC.name] = EVIDENCE
EVIDENCE_SPEC.loader.exec_module(EVIDENCE)


class FakeTerminal:
    def __init__(
        self,
        *,
        exit_code: int = 0,
        text: str = "ok",
        close_error: Exception | None = None,
    ) -> None:
        self.expected_exit = exit_code
        self.screen = text
        self.started: list[tuple[str, str, Path, dict[str, str]]] = []
        self.waited_for: list[str] = []
        self.keys: list[str] = []
        self.responses: list[str] = []
        self.text_reads = 0
        self.screenshots = 0
        self.closed = False
        self.close_error = close_error

    async def start(
        self,
        executable: str,
        source: str,
        cwd: Path,
        env: dict[str, str],
    ) -> None:
        self.started.append((executable, source, cwd, env))

    async def wait_text(self, text: str, timeout: float) -> None:
        self.waited_for.append(text)

    async def wait_idle(self, timeout: float) -> None:
        return None

    async def press(self, key: str) -> None:
        self.keys.append(key)

    async def submit(self, text: str) -> None:
        self.responses.append(text)

    async def wait_exit(self, timeout: float) -> None:
        return None

    async def exit_code(self) -> int | None:
        return self.expected_exit

    async def text(self) -> str:
        self.text_reads += 1
        return self.screen

    async def screenshot(self, path: Path) -> None:
        self.screenshots += 1
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("<svg/>", encoding="utf-8")

    async def close(self) -> None:
        self.closed = True
        if self.close_error:
            raise self.close_error


class EvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="demo-runner-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.run = self.root / "run"

    def block(self, **changes: object):
        values = {
            "id": "check",
            "role": "verify",
            "shell": "bash",
            "terminal": "main",
            "effect": "read",
            "mode": "command",
            "capture": "safe",
            "source": "printf 'ok\\n'",
            "line": 12,
            "timeout": 30.0,
            "expected_exit": 0,
            "wait_text": None,
            "before_capture": (),
            "after_capture": (),
            "observe_text": None,
        }
        values.update(changes)
        return DEMO.ExecutableBlock(**values)

    def execute(self, block, terminal: FakeTerminal, **options: object) -> dict:
        return asyncio.run(
            EVIDENCE.run_block(
                demo="sample",
                block=block,
                root=self.root,
                run_dir=self.run,
                terminal_factory=lambda: terminal,
                **options,
            )
        )

    def manifest(self) -> dict:
        return json.loads((self.run / "manifest.json").read_text(encoding="utf-8"))

    def test_executes_exact_source_once_and_writes_safe_evidence(self) -> None:
        terminal = FakeTerminal(text="safe output")
        block = self.block(source="value=42\nprintf '%s\\n' \"$value\"")

        result = self.execute(block, terminal)

        self.assertEqual("PASS", result["status"])
        self.assertEqual(block.source, terminal.started[0][1])
        self.assertEqual(
            str(self.run.resolve().with_name("run-work")),
            terminal.started[0][3]["DEMO_WORK_DIR"],
        )
        self.assertEqual(1, len(terminal.started))
        self.assertEqual(1, terminal.text_reads)
        self.assertEqual(1, terminal.screenshots)
        self.assertTrue(terminal.closed)
        self.assertTrue((self.run / "report.html").is_file())
        receipt = self.manifest()["receipts"][0]
        self.assertEqual("safe output", (self.run / receipt["text"]).read_text())
        self.assertTrue((self.run / receipt["json"]).is_file())

    def test_write_requires_exact_approval_and_cannot_repeat(self) -> None:
        block = self.block(id="create", role="action", effect="write")
        refused = FakeTerminal()

        with self.assertRaisesRegex(ValueError, "approve create"):
            self.execute(block, refused)
        self.assertEqual([], refused.started)

        first = FakeTerminal()
        self.execute(block, first, approved="create")
        self.assertEqual(1, len(first.started))
        self.assertEqual("COMPLETED", self.manifest()["ledger"]["create"]["state"])

        repeated = FakeTerminal()
        with self.assertRaisesRegex(ValueError, "already RESERVED or completed"):
            self.execute(block, repeated, approved="create")
        self.assertEqual([], repeated.started)

    def test_capture_none_never_reads_or_screenshots_terminal(self) -> None:
        terminal = FakeTerminal(text="device code must not be retained")
        result = self.execute(self.block(capture="none"), terminal)

        self.assertEqual("PASS", result["status"])
        self.assertEqual(0, terminal.text_reads)
        self.assertEqual(0, terminal.screenshots)
        receipt = self.manifest()["receipts"][0]
        self.assertEqual("", receipt["output"])
        self.assertIsNone(receipt["image"])

    def test_suppressed_write_capture_does_not_make_completed_effect_repeatable(
        self,
    ) -> None:
        terminal = FakeTerminal(text="Authorization: Bearer hidden")
        block = self.block(id="create", role="action", effect="write")

        result = self.execute(block, terminal, approved="create")

        self.assertEqual("BLOCKED", result["status"])
        self.assertEqual("COMPLETED", self.manifest()["ledger"]["create"]["state"])
        self.assertEqual(0, terminal.screenshots)

    def test_quoted_camel_case_json_secret_suppresses_capture(self) -> None:
        terminal = FakeTerminal(text='{"accessToken": "not-retained"}')

        result = self.execute(self.block(), terminal)

        self.assertEqual("BLOCKED", result["status"])
        self.assertEqual("", result["output"])
        self.assertEqual(0, terminal.screenshots)

    def test_secret_prompt_is_not_answered_or_resolved(self) -> None:
        terminal = FakeTerminal(text='{"clientSecret": "not-retained"}')
        responses: list[str] = []
        block = self.block(
            id="prompt",
            role="action",
            effect="write",
            mode="prompt",
            wait_text="Continue",
        )

        result = self.execute(
            block,
            terminal,
            approved="prompt",
            response_provider=lambda text: responses.append(text) or "yes",
        )

        self.assertEqual("BLOCKED", result["status"])
        self.assertEqual([], responses)
        checkpoint = self.manifest()["receipts"][0]
        self.assertNotIn("resolved_by", checkpoint)

    def test_secret_tui_checkpoint_remains_unresolved(self) -> None:
        terminal = FakeTerminal(text='{"refreshToken": "not-retained"}')
        block = self.block(
            id="status",
            mode="tui",
            wait_text="all resources",
            after_capture=("q",),
        )

        result = self.execute(block, terminal)

        self.assertEqual("BLOCKED", result["status"])
        self.assertNotIn("resolved_by", self.manifest()["receipts"][0])

    def test_secret_observation_is_not_printed(self) -> None:
        terminal = FakeTerminal(text='{"access_token": "not-retained"}')
        observed: list[str] = []

        result = self.execute(
            self.block(observe_text="Submitted:"),
            terminal,
            observer=observed.append,
        )

        self.assertEqual("BLOCKED", result["status"])
        self.assertEqual([], observed)

    def test_terminal_close_failure_changes_returned_result_to_blocked(self) -> None:
        terminal = FakeTerminal(close_error=RuntimeError("close failed"))

        result = self.execute(self.block(), terminal)

        self.assertEqual("BLOCKED", result["status"])
        self.assertEqual("BLOCKED", self.manifest()["status"])
        self.assertIn("close failed", " ".join(result["errors"]))

    def test_tui_waits_captures_then_quits_and_resolves_checkpoint(self) -> None:
        terminal = FakeTerminal(text="all resources ready")
        block = self.block(
            id="status",
            mode="tui",
            wait_text="all resources",
            before_capture=("a",),
            after_capture=("q",),
        )

        result = self.execute(block, terminal)

        self.assertEqual("PASS", result["status"])
        self.assertEqual(["all resources"], terminal.waited_for)
        self.assertEqual(["a", "q"], terminal.keys)
        receipts = self.manifest()["receipts"]
        self.assertEqual("BLOCKED", receipts[0]["status"])
        self.assertEqual(receipts[1]["id"], receipts[0]["resolved_by"])
        self.assertEqual("PASS", self.manifest()["status"])

    def test_prompt_uses_original_operation_and_does_not_resubmit_command(self) -> None:
        terminal = FakeTerminal(text="Type CREATE AUDIT run-id")
        block = self.block(
            id="prepare-audit",
            role="action",
            effect="write",
            mode="prompt",
            wait_text="CREATE AUDIT",
        )

        result = self.execute(
            block,
            terminal,
            approved="prepare-audit",
            response_provider=lambda _: "CREATE AUDIT run-id",
        )

        self.assertEqual("PASS", result["status"])
        self.assertEqual(1, len(terminal.started))
        self.assertEqual(["CREATE AUDIT run-id"], terminal.responses)
        receipts = self.manifest()["receipts"]
        self.assertEqual(receipts[1]["id"], receipts[0]["resolved_by"])

    def test_prompt_without_provider_reads_the_response_off_the_event_loop(
        self,
    ) -> None:
        terminal = FakeTerminal(text="Type CREATE AUDIT run-id")
        block = self.block(
            id="prepare-audit",
            role="action",
            effect="write",
            mode="prompt",
            wait_text="CREATE AUDIT",
        )
        prompts: list[str] = []

        def fake_input(prompt: str) -> str:
            with self.assertRaises(RuntimeError, msg="input() ran on the loop"):
                asyncio.get_running_loop()
            prompts.append(prompt)
            return "CREATE AUDIT run-id"

        with mock.patch("builtins.input", fake_input):
            result = self.execute(block, terminal, approved="prepare-audit")

        self.assertEqual("PASS", result["status"])
        self.assertEqual(["CREATE AUDIT run-id"], terminal.responses)
        self.assertEqual(
            ["Response for prepare-audit (input is not stored): "], prompts
        )

    def test_observe_text_reports_running_output_without_resubmission(self) -> None:
        terminal = FakeTerminal(text="Submitted: request-id")
        observed: list[str] = []
        block = self.block(observe_text="Submitted:")

        result = self.execute(block, terminal, observer=observed.append)

        self.assertEqual("PASS", result["status"])
        self.assertEqual(["Submitted:"], terminal.waited_for)
        self.assertEqual(["Submitted: request-id"], observed)
        self.assertEqual(1, len(terminal.started))

    def test_failed_exit_records_failure_without_retry(self) -> None:
        terminal = FakeTerminal(exit_code=7, text="failed")

        result = self.execute(self.block(), terminal)

        self.assertEqual("FAIL", result["status"])
        self.assertEqual(1, len(terminal.started))
        self.assertEqual(7, self.manifest()["receipts"][0]["exit_code"])

    @unittest.skipUnless(
        importlib.util.find_spec("tui_test"), "install tui-test binding"
    )
    def test_live_binding_runs_bash5_and_captures_direct_exit(self) -> None:
        block = self.block(
            source="printf 'BASH=%s\\n' \"$BASH_VERSION\"; exit 7",
            expected_exit=7,
        )

        result = asyncio.run(
            EVIDENCE.run_block(
                demo="live",
                block=block,
                root=self.root,
                run_dir=self.run,
            )
        )

        self.assertEqual("PASS", result["status"])
        self.assertRegex(result["output"], r"BASH=5\.")
        self.assertEqual("0.1.0-beta.3", self.manifest()["binding_version"])

    @unittest.skipUnless(
        importlib.util.find_spec("tui_test"), "install tui-test binding"
    )
    def test_live_binding_captures_tui_before_quit(self) -> None:
        block = self.block(
            id="local-tui",
            source="printf 'all resources ready\\n'; IFS= read -r -n 1 key; [[ $key == q ]]",
            mode="tui",
            wait_text="all resources ready",
            after_capture=("q",),
        )

        result = asyncio.run(
            EVIDENCE.run_block(
                demo="live",
                block=block,
                root=self.root,
                run_dir=self.run,
            )
        )

        self.assertEqual("PASS", result["status"])
        receipts = self.manifest()["receipts"]
        self.assertIn("all resources ready", receipts[0]["output"])
        self.assertTrue((self.run / receipts[0]["image"]).is_file())


if __name__ == "__main__":
    unittest.main()
