#!/usr/bin/env python3
"""Check ASCII/Unicode box diagrams for alignment and charset problems."""

from __future__ import annotations

import argparse
import sys
import unicodedata
from collections.abc import Sequence
from dataclasses import dataclass

MAX_WIDTH = 100
ASCII_BOX = frozenset("+-|")
UNICODE_BOX = frozenset("┌┐└┘─│├┤┬┴┼╭╮╯╰╔╗╚╝═║┏┓┗┛━┃▶◀▼▲")


@dataclass(frozen=True)
class Finding:
    """One verification problem in a diagram file."""

    line: int
    message: str


def _has_emoji(text: str) -> bool:
    """Return True if ``text`` contains emoji or other wide symbols."""
    for char in text:
        if unicodedata.east_asian_width(char) in {"F", "W"}:
            return True
        name = unicodedata.name(char, "")
        if "EMOJI" in name or name.startswith("REGIONAL INDICATOR"):
            return True
    return False


def _box_runs(
    line: str, open_char: str, close_char: str, fill_char: str
) -> list[tuple[int, int]]:
    """Return ``(start, end)`` inclusive columns for top or bottom box borders."""
    runs: list[tuple[int, int]] = []
    index = 0
    while index < len(line):
        if line[index] != open_char:
            index += 1
            continue
        end = index + 1
        while end < len(line) and line[end] == fill_char:
            end += 1
        if end < len(line) and line[end] == close_char and end > index + 1:
            runs.append((index, end))
            index = end + 1
        else:
            index += 1
    return runs


def _check_boxes(lines: Sequence[str], style: str) -> list[Finding]:
    """Check that detected boxes keep a straight right border.

    :param lines: Diagram rows.
    :param style: ``unicode`` or ``ascii``.
    :returns: Findings for ragged boxes.
    """
    findings: list[Finding] = []
    if style == "unicode":
        top_open, top_close, fill, side, bottom_open, bottom_close = (
            "┌",
            "┐",
            "─",
            "│",
            "└",
            "┘",
        )
    else:
        top_open = top_close = bottom_open = bottom_close = "+"
        fill, side = "-", "|"

    for row_index, line in enumerate(lines):
        for start, end in _box_runs(line, top_open, top_close, fill):
            found_bottom = False
            for scan in range(row_index + 1, len(lines)):
                candidate = lines[scan]
                if len(candidate) <= end:
                    findings.append(
                        Finding(
                            scan + 1,
                            f"box starting at line {row_index + 1} is shorter than its top border",
                        )
                    )
                    found_bottom = True
                    break
                if candidate[start] == bottom_open and candidate[end] == bottom_close:
                    inner = candidate[start + 1 : end]
                    if set(inner) <= {fill}:
                        found_bottom = True
                        break
                if candidate[start] != side or candidate[end] != side:
                    findings.append(
                        Finding(
                            scan + 1,
                            f"box from line {row_index + 1} has a broken side at columns {start}-{end}",
                        )
                    )
                    found_bottom = True
                    break
            if not found_bottom:
                findings.append(
                    Finding(row_index + 1, "box top has no matching bottom border")
                )
    return findings


def verify_text(text: str) -> list[Finding]:
    """Verify diagram text.

    :param text: Raw diagram contents.
    :returns: Findings; empty means the diagram passed.
    """
    findings: list[Finding] = []
    lines = text.splitlines()
    used_ascii = False
    used_unicode = False
    for number, line in enumerate(lines, start=1):
        if "\t" in line:
            findings.append(
                Finding(number, "tab characters break alignment; use spaces")
            )
        if line.endswith(" "):
            findings.append(Finding(number, "trailing space"))
        if len(line) > MAX_WIDTH:
            findings.append(
                Finding(number, f"line width {len(line)} exceeds {MAX_WIDTH}")
            )
        if _has_emoji(line):
            findings.append(Finding(number, "emoji or wide characters shift columns"))
        chars = set(line)
        if chars & ASCII_BOX:
            used_ascii = True
        if chars & UNICODE_BOX:
            used_unicode = True
    if used_ascii and used_unicode:
        findings.append(
            Finding(1, "mixed ASCII and Unicode box characters; pick one charset")
        )
    style = (
        "unicode" if used_unicode and not used_ascii else "ascii" if used_ascii else ""
    )
    if style:
        findings.extend(_check_boxes(lines, style))
    return findings


def verify_path(path: str) -> list[Finding]:
    """Verify a diagram file.

    :param path: File path.
    :returns: Findings from :func:`verify_text`.
    :raises OSError: If the file cannot be read.
    """
    with open(path, encoding="utf-8") as handle:
        return verify_text(handle.read())


def main(argv: Sequence[str] | None = None) -> int:
    """Run the verifier CLI.

    :param argv: Optional argument list.
    :returns: ``0`` when the diagram passes, ``1`` when findings exist.
    """
    parser = argparse.ArgumentParser(
        description="Verify ASCII/Unicode box-diagram alignment."
    )
    parser.add_argument(
        "path", help="path to a .txt or Markdown file containing the diagram"
    )
    args = parser.parse_args(argv)
    findings = verify_path(args.path)
    if not findings:
        sys.stdout.write("PASS\n")
        return 0
    for finding in findings:
        sys.stdout.write(f"{args.path}:{finding.line}: {finding.message}\n")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
