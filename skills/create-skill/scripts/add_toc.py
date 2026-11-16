#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Add or refresh a heading table of contents in long skill Markdown files.

Targets each SKILL.md and each Markdown file under a references/ directory with
more than 100 lines, not counting an existing generated TOC. The TOC lists two
heading levels, uses GitHub and DocFX heading anchors, and sits between
<!-- toc --> and <!-- tocstop --> markers so that reruns replace it. A
hand-written "Contents" or "Table of Contents" link list is replaced in place.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

MIN_LINES = 100
MIN_ENTRIES = 2
TOC_START = "<!-- toc -->"
TOC_END = "<!-- tocstop -->"
TOC_HEADING = "## Contents"

HEADING = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.*?)(?:[ \t]+#+)?[ \t]*$")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")
CONTENTS_TITLE = re.compile(r"^(table of )?contents$", re.IGNORECASE)
LIST_ITEM = re.compile(r"^\s*([-*+]|\d+\.)\s+")
RULE = {"---", "***", "___"}

Heading = tuple[int, int, str]  # line index, level, text


def is_target(path: Path) -> bool:
    return path.suffix == ".md" and (
        path.name == "SKILL.md" or "references" in path.parent.parts
    )


def strip_generated(lines: list[str]) -> tuple[list[str], int | None]:
    """Remove a generated TOC block; return the lines and the block's position."""
    if TOC_START not in lines or TOC_END not in lines:
        return lines, None
    start = lines.index(TOC_START)
    after = lines.index(TOC_END, start) + 1
    if after < len(lines) and lines[after] == "":
        after += 1
    return lines[:start] + lines[after:], start


def front_matter_end(lines: list[str]) -> int:
    if lines and lines[0] == "---":
        for index in range(1, len(lines)):
            if lines[index] in ("---", "..."):
                return index + 1
    return 0


def find_headings(lines: list[str], start: int) -> list[Heading]:
    """Return ATX headings outside code fences and HTML comments."""
    headings = []
    fence = None
    in_comment = False
    for index in range(start, len(lines)):
        line = lines[index]
        if in_comment:
            in_comment = "-->" not in line
            continue
        match = FENCE.match(line)
        if fence:
            marker = match.group(1) if match else ""
            if (
                marker[:1] == fence[0]
                and len(marker) >= len(fence)
                and not match.group(2).strip()
            ):
                fence = None
            continue
        if match and not (match.group(1)[0] == "`" and "`" in match.group(2)):
            fence = match.group(1)
            continue
        if line.lstrip().startswith("<!--") and "-->" not in line:
            in_comment = True
            continue
        heading = HEADING.match(line)
        if heading:
            headings.append((index, len(heading.group(1)), heading.group(2).strip()))
    return headings


def strip_links(text: str) -> str:
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return re.sub(r"!?\[([^\]]*)\]\[[^\]]*\]", r"\1", text)


def plain_text(text: str) -> str:
    """Approximate the rendered text of inline Markdown."""
    text = re.sub(r"<[^>]+>", "", strip_links(text))
    text = re.sub(r"(\*\*|__)(.+?)\1", r"\2", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"\1", text)
    text = re.sub(r"(?<!\w)_(?!\s)(.+?)(?<!\s)_(?!\w)", r"\1", text)
    return text.replace("`", "")


def slugify(text: str) -> str:
    """Heading anchor: lowercase; keep letters, digits, marks, _ and -; space to -."""
    kept = []
    for char in plain_text(text).strip().lower():
        category = unicodedata.category(char)
        if char in "-_" or category[0] in "LN" or category == "Mn":
            kept.append(char)
        elif char == " ":
            kept.append("-")
    return "".join(kept)


def existing_toc_span(
    lines: list[str], headings: list[Heading]
) -> tuple[int, int] | None:
    """Locate a hand-written Contents section made only of list items."""
    for position, (index, _level, text) in enumerate(headings):
        if not CONTENTS_TITLE.match(plain_text(text).strip()):
            continue
        end = headings[position + 1][0] if position + 1 < len(headings) else len(lines)
        body = [
            line
            for line in lines[index + 1 : end]
            if line.strip() and line.strip() not in RULE
        ]
        if body and all(LIST_ITEM.match(line) for line in body):
            stop = index + 1
            while stop < end and (
                not lines[stop].strip() or LIST_ITEM.match(lines[stop])
            ):
                stop += 1
            return index, stop
    return None


def build(lines: list[str], previous: int | None) -> tuple[list[str] | None, str]:
    """Return lines with a TOC, or None and the reason a TOC does not apply."""
    body_start = front_matter_end(lines)
    headings = find_headings(lines, body_start)
    span = existing_toc_span(lines, headings)
    if span:
        start, stop = span
        lines = lines[:start] + lines[stop:]
        headings = [
            (index if index < start else index - (stop - start), level, text)
            for index, level, text in headings
            if not start <= index < stop
        ]

    title = headings[0] if headings and headings[0][1] == 1 else None
    sections = [heading for heading in headings if heading is not title]
    if not sections:
        return None, "no section headings"
    base = min(level for _, level, _ in sections)
    entries = [heading for heading in sections if heading[1] <= base + 1]
    if len(entries) < MIN_ENTRIES:
        return None, f"only {len(entries)} heading(s)"

    if span:
        insert_at = span[0]
    elif previous is not None:
        insert_at = previous
    elif title:
        insert_at = title[0] + 1
    else:
        insert_at = body_start

    # Repeated headings get -1, -2 suffixes in document order, including the TOC heading.
    ordered = [h for h in headings if h[0] < insert_at] + [(insert_at, 2, "Contents")]
    ordered += [h for h in headings if h[0] >= insert_at]
    seen: dict[str, int] = {}
    anchors = {}
    for heading in ordered:
        slug = slugify(heading[2])
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        anchors[heading] = f"{slug}-{count}" if count else slug

    toc = [TOC_START, TOC_HEADING, ""]
    for heading in entries:
        label = strip_links(heading[2]).replace("[", r"\[").replace("]", r"\]")
        toc.append(f"{'  ' * (heading[1] - base)}- [{label}](#{anchors[heading]})")
    toc += [TOC_END, ""]

    before, after = lines[:insert_at], lines[insert_at:]
    while before and before[-1] == "":
        before.pop()
    while after and after[0] == "":
        after.pop(0)
    return before + ([""] if before else []) + toc + after, f"{len(entries)} entries"


def process(path: Path, write: bool) -> tuple[bool, str]:
    """Return whether the file changes (or would change) and a status note."""
    original = path.read_text(encoding="utf-8")
    lines = original.split("\n")
    trailing_newline = lines[-1] == ""
    if trailing_newline:
        lines.pop()
    lines, previous = strip_generated(lines)
    if len(lines) <= MIN_LINES:
        new_lines, note = lines, f"{MIN_LINES} lines or fewer"
    else:
        built, note = build(lines, previous)
        new_lines = built if built is not None else lines
    updated = "\n".join(new_lines) + ("\n" if trailing_newline else "")
    if updated == original:
        return False, note
    if write:
        path.write_text(updated, encoding="utf-8")
    return True, note


def target_files(paths: list[Path]) -> list[Path]:
    files = set()
    for path in paths:
        if path.is_dir():
            files.update(p for p in path.rglob("*.md") if is_target(p))
        elif is_target(path):
            files.add(path)
    return sorted(files)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="skill directories, skill roots, or Markdown files",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="report stale files and exit 1 without writing",
    )
    args = parser.parse_args()

    stale = 0
    for path in target_files(args.paths):
        changed, note = process(path, write=not args.check)
        if changed:
            stale += 1
            print(f"{'stale' if args.check else 'updated'}: {path} ({note})")
    return 1 if args.check and stale else 0


if __name__ == "__main__":
    sys.exit(main())
