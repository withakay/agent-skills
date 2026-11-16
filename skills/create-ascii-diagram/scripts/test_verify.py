"""Tests for ASCII diagram verification."""

from __future__ import annotations

from pathlib import Path

from grid import Grid
from verify import verify_path, verify_text


def test_verify_text_accepts_aligned_unicode_box() -> None:
    grid = Grid(16, 3)
    grid.box(0, 0, 16, 3, ["ok"])
    assert verify_text(grid.render()) == []


def test_verify_text_rejects_mixed_charset() -> None:
    text = "┌──┐\n|  |\n└──┘\n"
    messages = [finding.message for finding in verify_text(text)]
    assert any("mixed" in message for message in messages)


def test_verify_text_rejects_overwidth() -> None:
    text = "x" * 101 + "\n"
    messages = [finding.message for finding in verify_text(text)]
    assert any("exceeds" in message for message in messages)


def test_verify_text_rejects_tabs_and_trailing_space() -> None:
    text = "┌──┐ \n\t│  │\n└──┘\n"
    messages = [finding.message for finding in verify_text(text)]
    assert any("trailing space" in message for message in messages)
    assert any("tab" in message for message in messages)


def test_verify_path_reports_broken_side(tmp_path: Path) -> None:
    path = tmp_path / "broken.txt"
    path.write_text("┌────┐\n│ hi\n└────┘\n", encoding="utf-8")
    findings = verify_path(str(path))
    assert findings
    assert any(
        "broken side" in finding.message or "shorter" in finding.message
        for finding in findings
    )
