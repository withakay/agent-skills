#!/usr/bin/env python3
"""Execute one annotated demo block through the in-process tui-test API."""

from __future__ import annotations

import asyncio
import base64
import fcntl
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Protocol
from uuid import uuid4

from demo import ExecutableBlock

TEMPLATE = Path(__file__).resolve().parent.parent / "assets/evidence-report.html"
MAX_OUTPUT = 200_000
SECRET_PATTERNS = (
    re.compile(r"(?i)authorization:\s*(?:bearer|basic)\s+\S+"),
    re.compile(
        r"(?i)[\"']?(?:client[_-]?secret|access[_-]?token|refresh[_-]?token)"
        r"[\"']?\s*[:=]\s*[\"']?[^\"'\s,}]+"
    ),
    re.compile(r"(?i)[?&](?:sig|se|sp|sv|spr|skoid|sktid)="),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)(?:client-key-data|client-certificate-data|token):\s*\S+"),
    re.compile(r"(?i)(?:device code|devicelogin|microsoft\.com/devicelogin)"),
)


class Terminal(Protocol):
    async def start(
        self, executable: str, source: str, cwd: Path, env: dict[str, str]
    ) -> None: ...

    async def wait_text(self, text: str, timeout: float) -> None: ...

    async def wait_idle(self, timeout: float) -> None: ...

    async def press(self, key: str) -> None: ...

    async def submit(self, text: str) -> None: ...

    async def wait_exit(self, timeout: float) -> None: ...

    async def exit_code(self) -> int | None: ...

    async def text(self) -> str: ...

    async def screenshot(self, path: Path) -> None: ...

    async def close(self) -> None: ...


def utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _atomic_json(path: Path, value: dict) -> None:
    temporary = path.with_name(path.name + "." + uuid4().hex + ".tmp")
    temporary.write_text(json.dumps(value, indent=2), encoding="utf-8")
    temporary.chmod(0o600)
    os.replace(temporary, path)


def _initial_manifest(demo: str, root: Path) -> dict:
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        capture_output=True,
        text=True,
        timeout=5,
        check=False,
    )
    return {
        "schema_version": 2,
        "demo": demo,
        "started": utc(),
        "root": str(root),
        "target_revision": revision.stdout.strip()
        if revision.returncode == 0
        else None,
        "runner_hash": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "template_hash": hashlib.sha256(TEMPLATE.read_bytes()).hexdigest(),
        "binding_version": None,
        "status": "BLOCKED",
        "ledger": {},
        "receipts": [],
        "errors": [],
        "recording": "disabled",
        "updated": utc(),
    }


@contextmanager
def _locked_manifest(run_dir: Path, demo: str, root: Path) -> Iterator[dict]:
    run_dir.mkdir(parents=True, exist_ok=True)
    run_dir.chmod(0o700)
    lock_path = run_dir / ".runner.lock"
    with lock_path.open("a+", encoding="utf-8") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        path = run_dir / "manifest.json"
        manifest = (
            json.loads(path.read_text(encoding="utf-8"))
            if path.exists()
            else _initial_manifest(demo, root)
        )
        if manifest["demo"] != demo or Path(manifest["root"]) != root:
            raise ValueError("Run directory belongs to a different demo or repository")
        yield manifest
        manifest["updated"] = utc()
        _atomic_json(path, manifest)
        _write_report(run_dir, manifest)
        fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def _write_report(run_dir: Path, manifest: dict) -> None:
    cards: list[str] = []
    for receipt in manifest["receipts"]:
        picture = ""
        image_name = receipt.get("image")
        if image_name:
            image = run_dir / image_name
            if image.is_file():
                encoded = base64.b64encode(image.read_bytes()).decode("ascii")
                picture = (
                    '<img alt="Terminal capture" src="data:image/svg+xml;base64,'
                    + encoded
                    + '">'
                )
        cards.append(
            "<article><h2>"
            + html.escape(receipt["id"] + ". " + receipt["title"])
            + '</h2><p class="status">'
            + html.escape(receipt["status"])
            + '</p><p class="meta">'
            + html.escape(
                f"{receipt['started']} — {receipt['ended']}; "
                f"exit {receipt['exit_code'] if receipt['exit_code'] is not None else 'unknown'}; "
                f"expected {receipt['expected_exit']}; terminal {receipt['terminal']}"
            )
            + "</p><h3>Command</h3><pre>"
            + html.escape(receipt["command"])
            + "</pre><h3>Observed output</h3><pre>"
            + html.escape(receipt["output"])
            + "</pre>"
            + "".join(
                '<p class="error">' + html.escape(error) + "</p>"
                for error in receipt["errors"]
            )
            + picture
            + "<details><summary>Command receipt</summary><pre>"
            + html.escape(json.dumps(receipt, indent=2))
            + "</pre></details></article>"
        )
    text = json.dumps(manifest, indent=2)
    values = {
        "TITLE": html.escape(manifest["demo"]),
        "STATUS": html.escape(manifest["status"]),
        "RECEIPTS": "".join(cards),
        "MANIFEST": html.escape(text),
        "ERRORS": "".join(
            '<p class="error">' + html.escape(error) + "</p>"
            for error in manifest["errors"]
        ),
    }
    report = re.sub(
        r"\{\{([A-Z_]+)\}\}",
        lambda match: values[match[1]],
        TEMPLATE.read_text(encoding="utf-8"),
    )
    temporary = run_dir / ("report." + uuid4().hex + ".tmp")
    temporary.write_text(report, encoding="utf-8")
    temporary.chmod(0o600)
    os.replace(temporary, run_dir / "report.html")


def _reserve(run_dir: Path, demo: str, root: Path, block: ExecutableBlock) -> None:
    if block.effect not in ("write", "cleanup"):
        return
    with _locked_manifest(run_dir, demo, root) as manifest:
        existing = manifest["ledger"].get(block.id)
        if existing:
            raise ValueError(
                f"Block {block.id} already RESERVED or completed; reconcile it instead of repeating it"
            )
        manifest["ledger"][block.id] = {
            "state": "RESERVED",
            "source_hash": block.source_hash,
            "effect": block.effect,
            "started": utc(),
        }


def _secret_hit(text: str) -> str | None:
    return next(
        (pattern.pattern for pattern in SECRET_PATTERNS if pattern.search(text)), None
    )


async def _receipt(
    *,
    demo: str,
    block: ExecutableBlock,
    root: Path,
    run_dir: Path,
    terminal: Terminal,
    status: str,
    exit_code: int | None,
    title: str,
    resolves: tuple[str, ...] = (),
    errors: list[str] | None = None,
) -> dict:
    receipt_id = uuid4().hex
    image_name: str | None = None
    output = ""
    receipt_errors = list(errors or [])
    if block.capture == "safe":
        try:
            output = (await terminal.text())[-MAX_OUTPUT:]
        except Exception as error:  # noqa: BLE001 - evidence must record unknown binding failures.
            status = "BLOCKED"
            receipt_errors.append(f"Could not read terminal text: {error}")
        else:
            secret = _secret_hit(output)
            if secret:
                status = "BLOCKED"
                output = ""
                receipt_errors.append(
                    "Capture suppressed because visible text matched a secret-bearing pattern"
                )
            else:
                image_name = f"evidence/{block.terminal}/{receipt_id}.svg"
                try:
                    await terminal.screenshot(run_dir / image_name)
                except Exception as error:  # noqa: BLE001 - preserve receipt on capture failure.
                    image_name = None
                    status = "BLOCKED"
                    receipt_errors.append(f"Could not capture terminal SVG: {error}")
    receipt = {
        "id": receipt_id,
        "block": block.id,
        "title": title,
        "role": block.role,
        "effect": block.effect,
        "terminal": block.terminal,
        "source_line": block.line,
        "source_hash": block.source_hash,
        "command": block.source,
        "started": utc(),
        "ended": utc(),
        "exit_code": exit_code,
        "expected_exit": block.expected_exit,
        "status": status,
        "output": output,
        "image": image_name,
        "text": f"evidence/{block.terminal}/{receipt_id}.txt",
        "json": f"evidence/{block.terminal}/{receipt_id}.json",
        "errors": receipt_errors,
        "resolves": list(resolves),
    }
    with _locked_manifest(run_dir, demo, root) as manifest:
        for checkpoint_id in resolves:
            checkpoint = next(
                (item for item in manifest["receipts"] if item["id"] == checkpoint_id),
                None,
            )
            if not checkpoint or checkpoint["status"] != "BLOCKED":
                raise ValueError("Resolution does not identify an open checkpoint")
            checkpoint["resolved_by"] = receipt_id
        text_path = run_dir / receipt["text"]
        json_path = run_dir / receipt["json"]
        text_path.parent.mkdir(parents=True, exist_ok=True)
        text_path.write_text(output, encoding="utf-8")
        text_path.chmod(0o600)
        json_path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
        json_path.chmod(0o600)
        manifest["receipts"].append(receipt)
        manifest["status"] = (
            "FAIL"
            if any(item["status"] == "FAIL" for item in manifest["receipts"])
            else "BLOCKED"
            if any(
                item["status"] == "BLOCKED" and not item.get("resolved_by")
                for item in manifest["receipts"]
            )
            else "PASS"
        )
        if block.effect in ("write", "cleanup") and exit_code is not None:
            manifest["ledger"][block.id]["state"] = (
                "COMPLETED" if exit_code == block.expected_exit else "FAILED"
            )
            manifest["ledger"][block.id]["ended"] = utc()
    return receipt


class PythonTuiTerminal:
    """Small boundary over tui_test 0.1.0b3; sessions remain process-local."""

    def __init__(self, shell: str) -> None:
        try:
            from tui_test import TuiTest, __version__
        except ImportError as error:
            raise RuntimeError(
                "Install tui-test 0.1.0b3 for Python: "
                "python3 -m pip install --pre 'tui-test==0.1.0b3'"
            ) from error
        if __version__ != "0.1.0-beta.3":
            raise RuntimeError(
                f"Unsupported tui-test Python binding {__version__}; expected 0.1.0-beta.3"
            )
        self.binding_version = __version__
        self.shell = shell
        self.client = TuiTest.ephemeral(
            prefix="demo",
            profile={"scrollback": 10_000},
            recording={"mode": "disabled"},
        )

    async def start(
        self, executable: str, source: str, cwd: Path, env: dict[str, str]
    ) -> None:
        arguments = (
            ("--noprofile", "--norc", "-c", source)
            if self.shell == "bash"
            else ("-NoProfile", "-Command", source)
        )
        await self.client.run(
            executable,
            *arguments,
            cwd=str(cwd),
            env=env,
            cols=100,
            rows=30,
            wait_ready=False,
        )

    async def wait_text(self, text: str, timeout: float) -> None:
        await self.client.get_by_text(text, full=True).expect(
            timeout=int(timeout * 1000)
        )

    async def wait_idle(self, timeout: float) -> None:
        await self.client.wait_idle(timeout=int(timeout * 1000))

    async def press(self, key: str) -> None:
        await self.client.press(key)

    async def submit(self, text: str) -> None:
        await self.client.submit(text)

    async def wait_exit(self, timeout: float) -> None:
        await self.client.wait_exit(timeout=int(timeout * 1000))

    async def exit_code(self) -> int | None:
        return (await self.client.state()).exited

    async def text(self) -> str:
        return await self.client.text(full=True)

    async def screenshot(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        await self.client.screenshot(str(path), full=True)

    async def close(self) -> None:
        await self.client.close_quiet()


def _executable(shell: str) -> str:
    if shell == "pwsh":
        executable = shutil.which("pwsh")
        if not executable:
            raise RuntimeError("pwsh is required for this explicitly PowerShell block")
        return executable
    requested = os.environ.get("DEMO_BASH")
    candidates = [requested] if requested else []
    candidates.extend(
        ("/opt/homebrew/bin/bash", "/usr/local/bin/bash", shutil.which("bash"))
    )
    for candidate in candidates:
        if not candidate or not Path(candidate).is_file():
            continue
        version = subprocess.run(
            [candidate, "-c", "printf '%s' \"${BASH_VERSINFO[0]}\""],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if (
            version.returncode == 0
            and version.stdout.isdigit()
            and int(version.stdout) >= 5
        ):
            return str(Path(candidate).resolve())
    raise RuntimeError(
        "Bash 5 is required; install it with 'brew install bash' or set DEMO_BASH"
    )


async def run_block(
    *,
    demo: str,
    block: ExecutableBlock,
    root: Path,
    run_dir: Path,
    work_dir: Path | None = None,
    approved: str | None = None,
    terminal_factory: Callable[[], Terminal] | None = None,
    response_provider: Callable[[str], str] | None = None,
    observer: Callable[[str], None] | None = None,
) -> dict:
    """Execute one block once; external writes require exact approval."""
    root = root.resolve(strict=True)
    run_dir = run_dir.resolve()
    work_dir = (
        work_dir.resolve() if work_dir else run_dir.with_name(run_dir.name + "-work")
    )
    if block.effect in ("write", "cleanup") and approved != block.id:
        raise ValueError(f"External effect requires --approve {block.id}")
    if block.mode == "manual":
        raise ValueError(
            f"Block {block.id} is manual; copy its source into an approved terminal"
        )
    with _locked_manifest(run_dir, demo, root) as manifest:
        recorded_work_dir = manifest.get("work_dir")
        if recorded_work_dir and Path(recorded_work_dir) != work_dir:
            raise ValueError("Run directory is already bound to a different --work-dir")
        manifest["work_dir"] = str(work_dir)
    _reserve(run_dir, demo, root, block)
    terminal = (
        terminal_factory() if terminal_factory else PythonTuiTerminal(block.shell)
    )
    executable = "fake-shell" if terminal_factory else _executable(block.shell)
    binding_version = getattr(terminal, "binding_version", None)
    if binding_version:
        with _locked_manifest(run_dir, demo, root) as manifest:
            manifest["binding_version"] = binding_version
    environment = dict(os.environ)
    environment.update(
        {
            "DEMO_EVIDENCE_DIR": str(run_dir),
            "DEMO_WORK_DIR": str(work_dir),
            "HISTFILE": "/dev/null",
        }
    )
    checkpoints: list[dict] = []
    final: dict | None = None
    try:
        await terminal.start(executable, block.source, root, environment)
        if block.mode in ("prompt", "tui"):
            assert block.wait_text
            await terminal.wait_text(block.wait_text, block.timeout)
            await terminal.wait_idle(min(block.timeout, 10))
            for key in block.before_capture:
                await terminal.press(key)
                await terminal.wait_idle(min(block.timeout, 10))
            checkpoint = await _receipt(
                demo=demo,
                block=block,
                root=root,
                run_dir=run_dir,
                terminal=terminal,
                status="BLOCKED",
                exit_code=None,
                title=block.id + " checkpoint",
            )
            checkpoints.append(checkpoint)
            if block.mode == "prompt":
                if checkpoint["errors"]:
                    raise RuntimeError(
                        "Prompt capture was suppressed; response not submitted"
                    )
                prompt_text = checkpoint["output"]
                if response_provider:
                    response = response_provider(prompt_text)
                else:
                    response = await asyncio.to_thread(
                        input, f"Response for {block.id} (input is not stored): "
                    )
                await terminal.submit(response)
            else:
                for key in block.after_capture:
                    await terminal.press(key)
        if block.observe_text:
            await terminal.wait_text(block.observe_text, block.timeout)
            await terminal.wait_idle(min(block.timeout, 10))
            observation = await _receipt(
                demo=demo,
                block=block,
                root=root,
                run_dir=run_dir,
                terminal=terminal,
                status="BLOCKED",
                exit_code=None,
                title=block.id + " observed",
            )
            checkpoints.append(observation)
            if observation["output"] and not observation["errors"]:
                (observer or print)(observation["output"])
        await terminal.wait_exit(block.timeout)
        exit_code = await terminal.exit_code()
        status = (
            "FAIL"
            if exit_code != block.expected_exit
            else "BLOCKED"
            if any(checkpoint["errors"] for checkpoint in checkpoints)
            else "PASS"
        )
        final = await _receipt(
            demo=demo,
            block=block,
            root=root,
            run_dir=run_dir,
            terminal=terminal,
            status=status,
            exit_code=exit_code,
            title=block.id,
            resolves=tuple(
                checkpoint["id"]
                for checkpoint in checkpoints
                if not checkpoint["errors"]
            ),
        )
    except Exception as error:  # noqa: BLE001 - unknown completion must be retained, never retried.
        final = await _receipt(
            demo=demo,
            block=block,
            root=root,
            run_dir=run_dir,
            terminal=terminal,
            status="BLOCKED",
            exit_code=None,
            title=block.id + " incomplete",
            resolves=tuple(
                checkpoint["id"]
                for checkpoint in checkpoints
                if not checkpoint["errors"]
            ),
            errors=[str(error)],
        )
        with _locked_manifest(run_dir, demo, root) as manifest:
            if block.effect in ("write", "cleanup"):
                manifest["ledger"][block.id]["state"] = "UNKNOWN"
        return final
    finally:
        try:
            await terminal.close()
        except Exception as error:  # noqa: BLE001 - closing failure changes final truth.
            message = f"Could not close terminal: {error}"
            if final:
                final["status"] = "BLOCKED"
                final["errors"].append(message)
            with _locked_manifest(run_dir, demo, root) as manifest:
                manifest["errors"].append(message)
                if final:
                    saved = next(
                        item
                        for item in manifest["receipts"]
                        if item["id"] == final["id"]
                    )
                    saved["status"] = "BLOCKED"
                    saved["errors"].append(message)
                    json_path = run_dir / saved["json"]
                    json_path.write_text(json.dumps(saved, indent=2), encoding="utf-8")
                    json_path.chmod(0o600)
                manifest["status"] = "BLOCKED"
    return final
