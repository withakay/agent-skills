#!/usr/bin/env python3
"""List and validate repository Markdown demos."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import re
import shlex
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, cast
from urllib.parse import unquote

NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_PATTERN = re.compile(r"\A---\n(?P<value>.*?)\n---(?:\n|\Z)", re.DOTALL)
# Whitespace other than the line boundaries str.splitlines() recognises, so a
# step heading never spans lines. Only match.start() is used, so the pattern
# stops at the first title character.
_INLINE_SPACE = r"[^\S\n\r\v\f\x1c-\x1e\x85\u2028\u2029]"
STEP_PATTERN = re.compile(
    rf"^###{_INLINE_SPACE}+(?:Step{_INLINE_SPACE}+)?\d+"
    rf"(?:[.:]{_INLINE_SPACE}+|{_INLINE_SPACE}+(?:-{_INLINE_SPACE}+)?)\S",
    re.IGNORECASE | re.MULTILINE,
)
# After .strip(), the title equals what r"^##\s+(.+?)\s*$" captured, without the
# overlapping quantifiers that let that pattern backtrack.
H2_PATTERN = re.compile(r"^##\s(.+)$")
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REQUIRED_STEP_FIELDS = ("Action", "Verify", "Accept")
DEMO_ATTRIBUTES = {
    "id",
    "effect",
    "terminal",
    "mode",
    "capture",
    "timeout",
    "expected-exit",
    "wait-text",
    "before-capture",
    "after-capture",
    "observe-text",
}
BLOCK_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

Role = Literal["action", "verify", "cleanup"]
Effect = Literal["read", "local", "write", "cleanup"]
Mode = Literal["command", "prompt", "tui", "manual"]
Capture = Literal["safe", "none"]


@dataclass(frozen=True)
class Demo:
    name: str
    description: str
    kind: str
    path: Path
    errors: tuple[str, ...]


@dataclass(frozen=True)
class ExecutableBlock:
    id: str
    role: Role
    shell: str
    terminal: str
    effect: Effect
    mode: Mode
    capture: Capture
    source: str
    line: int
    timeout: float
    expected_exit: int
    wait_text: str | None
    before_capture: tuple[str, ...]
    after_capture: tuple[str, ...]
    observe_text: str | None

    @property
    def source_hash(self) -> str:
        return hashlib.sha256(self.source.encode("utf-8")).hexdigest()


def _scalar(frontmatter: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.*?)\s*$", frontmatter, re.MULTILINE)
    if not match:
        return ""
    value = match.group(1).strip()
    if value in ("|", ">"):
        tail = frontmatter[match.end() :]
        lines: list[str] = []
        for line in tail.splitlines():
            if line and not line[0].isspace():
                break
            if line.strip():
                lines.append(line.strip())
        return ("\n" if value == "|" else " ").join(lines).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value.strip()


def _step_sections(text: str) -> list[str]:
    steps_heading = re.search(r"^##\s+Steps\s*$", text, re.IGNORECASE | re.MULTILINE)
    if not steps_heading:
        return []
    steps_body = text[steps_heading.end() :]
    next_heading = re.search(r"^##\s+", steps_body, re.MULTILINE)
    if next_heading:
        steps_body = steps_body[: next_heading.start()]
    matches = list(STEP_PATTERN.finditer(steps_body))
    return [
        steps_body[
            match.start() : matches[index + 1].start()
            if index + 1 < len(matches)
            else len(steps_body)
        ]
        for index, match in enumerate(matches)
    ]


def _local_link_errors(path: Path, text: str) -> list[str]:
    errors: list[str] = []
    for raw_target in LINK_PATTERN.findall(text):
        target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
        if not target or target.startswith(
            ("#", "/", "http://", "https://", "mailto:")
        ):
            continue
        target = unquote(target.split("#", 1)[0])
        if target and not (path.parent / target).exists():
            errors.append(f"broken local link: {raw_target}")
    return errors


def _attribute_values(tokens: list[str], line: int) -> tuple[dict[str, str], list[str]]:
    values: dict[str, str] = {}
    errors: list[str] = []
    for token in tokens:
        if "=" not in token:
            errors.append(f"line {line}: invalid demo attribute '{token}'")
            continue
        key, value = token.split("=", 1)
        if key not in DEMO_ATTRIBUTES:
            errors.append(f"line {line}: unknown demo attribute '{key}'")
        elif key in values:
            errors.append(f"line {line}: duplicate demo attribute '{key}'")
        elif not value:
            errors.append(f"line {line}: demo attribute '{key}' cannot be empty")
        else:
            values[key] = value
    return values, errors


def _keys(value: str | None) -> tuple[str, ...]:
    return tuple(key.strip() for key in (value or "").split(",") if key.strip())


def executable_blocks(
    path: Path,
) -> tuple[tuple[ExecutableBlock, ...], tuple[str, ...]]:
    """Parse explicitly annotated shell fences without changing their bodies."""
    lines = path.read_text(encoding="utf-8").splitlines()
    blocks: list[ExecutableBlock] = []
    errors: list[str] = []
    current_h2 = ""
    current_field = ""
    index = 0
    while index < len(lines):
        line = lines[index]
        h2 = H2_PATTERN.match(line)
        if h2:
            current_h2 = h2.group(1).strip().lower()
            current_field = ""
        field = re.match(
            r"^\*\*(Action|Run|Verify|Evidence|Cleanup)\*\*\s*$",
            line,
            re.IGNORECASE,
        )
        if field:
            current_field = field.group(1).lower()
        fence = re.match(r"^```([^`]*)$", line)
        if not fence:
            index += 1
            continue
        fence_line = index + 1
        info = fence.group(1).strip()
        end = index + 1
        while end < len(lines) and not re.match(r"^```\s*$", lines[end]):
            end += 1
        if end == len(lines):
            errors.append(f"line {fence_line}: unclosed code fence")
            break
        try:
            tokens = shlex.split(info)
        except ValueError as error:
            errors.append(f"line {fence_line}: invalid fence metadata: {error}")
            index = end + 1
            continue
        if len(tokens) < 2 or tokens[1] != "demo":
            index = end + 1
            continue
        language = tokens[0].lower()
        if language not in ("bash", "sh", "pwsh", "powershell"):
            errors.append(
                f"line {fence_line}: demo fence must use bash, sh, pwsh, or powershell"
            )
            index = end + 1
            continue
        values, attribute_errors = _attribute_values(tokens[2:], fence_line)
        errors.extend(attribute_errors)
        block_id = values.get("id", "")
        effect = values.get("effect", "")
        if not block_id:
            errors.append(f"line {fence_line}: demo block requires id")
        elif not BLOCK_ID_PATTERN.fullmatch(block_id):
            errors.append(f"line {fence_line}: invalid demo block id '{block_id}'")
        if effect not in ("read", "local", "write", "cleanup"):
            errors.append(
                f"line {fence_line}: effect must be read, local, write, or cleanup"
            )
        terminal = values.get("terminal", "main")
        if not BLOCK_ID_PATTERN.fullmatch(terminal):
            errors.append(f"line {fence_line}: invalid terminal name '{terminal}'")
        mode = values.get("mode", "command")
        if mode not in ("command", "prompt", "tui", "manual"):
            errors.append(f"line {fence_line}: invalid mode '{mode}'")
        capture = values.get("capture", "safe")
        if capture not in ("safe", "none"):
            errors.append(f"line {fence_line}: capture must be safe or none")
        try:
            timeout = float(values.get("timeout", "30"))
            if not 0 < timeout <= 3600:
                raise ValueError
        except ValueError:
            timeout = 30
            errors.append(f"line {fence_line}: timeout must be > 0 and <= 3600")
        try:
            expected_exit = int(values.get("expected-exit", "0"))
        except ValueError:
            expected_exit = 0
            errors.append(f"line {fence_line}: expected-exit must be an integer")
        wait_text = values.get("wait-text")
        if mode in ("prompt", "tui") and not wait_text:
            errors.append(f"line {fence_line}: mode={mode} requires wait-text")
        after_capture = _keys(values.get("after-capture"))
        if mode == "tui" and not after_capture:
            errors.append(f"line {fence_line}: mode=tui requires after-capture")
        role: Role = (
            "verify"
            if current_field == "verify"
            else "cleanup"
            if current_field == "cleanup" or current_h2 == "cleanup"
            else "action"
        )
        if role == "verify" and effect and effect != "read":
            errors.append(f"line {fence_line}: Verify blocks must use effect=read")
        source = "\n".join(lines[index + 1 : end])
        if block_id and effect in ("read", "local", "write", "cleanup"):
            blocks.append(
                ExecutableBlock(
                    id=block_id,
                    role=role,
                    shell="bash" if language in ("bash", "sh") else "pwsh",
                    terminal=terminal,
                    effect=cast(Effect, effect),
                    mode=cast(Mode, mode),
                    capture=cast(Capture, capture),
                    source=source,
                    line=fence_line,
                    timeout=timeout,
                    expected_exit=expected_exit,
                    wait_text=wait_text,
                    before_capture=_keys(values.get("before-capture")),
                    after_capture=after_capture,
                    observe_text=values.get("observe-text"),
                )
            )
        index = end + 1
    seen: set[str] = set()
    for block in blocks:
        if block.id in seen:
            errors.append(f"duplicate demo block id '{block.id}'")
        seen.add(block.id)
    return tuple(blocks), tuple(errors)


def inspect_demo(path: Path) -> Demo:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    frontmatter_match = FRONTMATTER_PATTERN.match(text)
    frontmatter = frontmatter_match.group("value") if frontmatter_match else ""
    name = _scalar(frontmatter, "name")
    description = _scalar(frontmatter, "description")

    if not frontmatter_match:
        errors.append("missing or invalid YAML frontmatter")
    if not name:
        errors.append("missing frontmatter name")
    elif name != path.parent.name:
        errors.append(
            f"frontmatter name '{name}' does not match directory '{path.parent.name}'"
        )
    if name and not NAME_PATTERN.fullmatch(name):
        errors.append("name must use lowercase hyphen-case")
    if not description:
        errors.append("missing frontmatter description")

    has_steps_heading = bool(
        re.search(r"^##\s+Steps\s*$", text, re.IGNORECASE | re.MULTILINE)
    )
    sections = _step_sections(text)
    kind = "runnable" if has_steps_heading else "markdown"
    if has_steps_heading and not sections:
        errors.append("Steps section has no numbered H3 steps")
    for index, section in enumerate(sections, start=1):
        for field in REQUIRED_STEP_FIELDS:
            if not re.search(
                rf"^\*\*{field}\*\*\s*$", section, re.IGNORECASE | re.MULTILINE
            ):
                errors.append(f"step {index} is missing {field}")
        accept_match = re.search(
            r"^\*\*Accept\*\*\s*$", section, re.IGNORECASE | re.MULTILINE
        )
        accept_body = section[accept_match.end() :] if accept_match else ""
        next_field = re.search(r"^\*\*[^*]+\*\*\s*$", accept_body, re.MULTILINE)
        if next_field:
            accept_body = accept_body[: next_field.start()]
        if accept_match and not re.search(
            r"^- \[[ xX]\] .+", accept_body, re.MULTILINE
        ):
            errors.append(f"step {index} has no acceptance checklist item")

    errors.extend(_local_link_errors(path, text))
    _, execution_errors = executable_blocks(path)
    errors.extend(execution_errors)
    return Demo(name or path.parent.name, description, kind, path, tuple(errors))


def demo_paths(root: Path) -> list[Path]:
    demos = root / "demos"
    if not demos.is_dir():
        return []
    return sorted(
        demo / "DEMO.md"
        for demo in demos.iterdir()
        if demo.is_dir() and (demo / "DEMO.md").is_file()
    )


def list_demos(root: Path) -> int:
    paths = demo_paths(root)
    if not paths:
        print(f"No demos found in {root / 'demos'}")
        return 0
    print("| Name | Kind | Valid | Description | Path |")
    print("| --- | --- | --- | --- | --- |")
    for path in paths:
        demo = inspect_demo(path)
        description = demo.description.replace("|", "\\|") or "—"
        print(
            f"| {demo.name} | {demo.kind} | {'yes' if not demo.errors else 'no'} "
            f"| {description} | {path.relative_to(root)} |"
        )
    return 0


def validate_demos(root: Path, name: str | None) -> int:
    if name:
        if not NAME_PATTERN.fullmatch(name):
            print(
                f"ERROR {name}: demo name must use lowercase hyphen-case",
                file=sys.stderr,
            )
            return 2
        path = root / "demos" / name / "DEMO.md"
        if not path.is_file():
            print(f"ERROR {name}: {path} does not exist", file=sys.stderr)
            return 2
        paths = [path]
    else:
        paths = demo_paths(root)
        if not paths:
            print(f"ERROR: no demos found in {root / 'demos'}", file=sys.stderr)
            return 2

    failed = False
    for path in paths:
        demo = inspect_demo(path)
        if demo.errors:
            failed = True
            for error in demo.errors:
                print(f"FAIL {demo.name}: {error}")
        else:
            print(f"PASS {demo.name}: valid {demo.kind} demo")
    return 1 if failed else 0


def _named_demo(root: Path, name: str) -> Path:
    if not NAME_PATTERN.fullmatch(name):
        raise ValueError("demo name must use lowercase hyphen-case")
    path = root / "demos" / name / "DEMO.md"
    if not path.is_file():
        raise ValueError(f"{path} does not exist")
    return path


def plan_demo(root: Path, name: str) -> int:
    path = _named_demo(root, name)
    demo = inspect_demo(path)
    if demo.errors:
        for error in demo.errors:
            print(f"FAIL {name}: {error}")
        return 1
    blocks, _ = executable_blocks(path)
    print("| ID | Role | Effect | Terminal | Mode | Capture | Timeout |")
    print("| --- | --- | --- | --- | --- | --- | ---: |")
    for block in blocks:
        print(
            f"| {block.id} | {block.role} | {block.effect} | {block.terminal} "
            f"| {block.mode} | {block.capture} | {block.timeout:g} |"
        )
    return 0


def run_demo_block(
    root: Path,
    name: str,
    block_id: str,
    run_dir: Path,
    work_dir: Path | None,
    approved: str | None,
) -> int:
    path = _named_demo(root, name)
    demo = inspect_demo(path)
    if demo.errors:
        raise ValueError("Demo is invalid; run validate before execution")
    blocks, _ = executable_blocks(path)
    block = next((candidate for candidate in blocks if candidate.id == block_id), None)
    if not block:
        raise ValueError(f"Demo has no executable block '{block_id}'")
    if block.mode == "manual":
        print(block.source)
        print(f"MANUAL {block.id}: runner did not execute or capture this block")
        return 3
    from evidence import run_block

    result = asyncio.run(
        run_block(
            demo=name,
            block=block,
            root=root,
            run_dir=run_dir,
            work_dir=work_dir,
            approved=approved,
        )
    )
    print(json.dumps(result))
    return 0 if result["status"] == "PASS" else 1 if result["status"] == "FAIL" else 3


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="repository root (default: current directory)",
    )
    commands = result.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="list repository demos")
    validate = commands.add_parser(
        "validate", help="validate one or all repository demos"
    )
    validate.add_argument("name", nargs="?", help="demo directory name")
    plan = commands.add_parser(
        "plan", help="show executable blocks without running them"
    )
    plan.add_argument("name", help="demo directory name")
    run = commands.add_parser("run", help="execute one named demo block exactly once")
    run.add_argument("name", help="demo directory name")
    run.add_argument("block", help="annotated block id")
    run.add_argument("--run-dir", type=Path, required=True)
    run.add_argument(
        "--work-dir",
        type=Path,
        help="private demo state directory (default: sibling of --run-dir)",
    )
    run.add_argument(
        "--approve",
        help="exact block id approval for one external write or cleanup",
    )
    return result


def main(arguments: list[str] | None = None) -> int:
    options = parser().parse_args(arguments)
    root = options.root.resolve()
    try:
        if options.command == "list":
            return list_demos(root)
        if options.command == "validate":
            return validate_demos(root, options.name)
        if options.command == "plan":
            return plan_demo(root, options.name)
        return run_demo_block(
            root,
            options.name,
            options.block,
            options.run_dir,
            options.work_dir,
            options.approve,
        )
    except (OSError, ValueError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
