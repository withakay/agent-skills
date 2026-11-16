"""Tests for the ASCII diagram grid helper."""

from __future__ import annotations

import pytest
from grid import MAX_WIDTH, Grid, main
from verify import verify_text


def test_grid_box_right_border_aligns_when_labels_vary() -> None:
    grid = Grid(20, 5)
    grid.box(0, 0, 12, 5, ["A", "longer"])
    lines = grid.render().splitlines()
    widths = {len(line) for line in lines}
    assert widths == {12}
    assert lines[0].startswith("┌")
    assert lines[-1].startswith("└")
    assert lines[1].startswith("│")
    assert lines[1].endswith("│")


def test_grid_h_arrow_places_head_and_label() -> None:
    grid = Grid(20, 4)
    grid.box(0, 1, 7, 3, ["L"])
    grid.box(13, 1, 7, 3, ["R"])
    grid.h_arrow(7, 12, 2, "http")
    rendered = grid.render()
    assert "http" in rendered
    assert "▶" in rendered


def test_grid_rejects_width_over_budget() -> None:
    with pytest.raises(ValueError, match="width must be"):
        Grid(MAX_WIDTH + 1, 3)


def test_grid_ascii_style_uses_plus_corners() -> None:
    grid = Grid(10, 3, style="ascii")
    grid.box(0, 0, 10, 3, ["X"])
    lines = grid.render().splitlines()
    assert lines[0].startswith("+")
    assert "|" in lines[1]


def test_grid_demo_cli_prints_unicode_boxes(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--demo"]) == 0
    output = capsys.readouterr().out
    assert "Subspace" in output
    assert "┌" in output
    assert verify_text(output) == []
