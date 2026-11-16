#!/usr/bin/env python3
"""Character-grid helper for aligned ASCII and Unicode box diagrams.

Agents import ``Grid`` from this module, place boxes and arrows by coordinate,
and print ``render()``. Do not count columns by hand.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

MAX_WIDTH = 100

UNICODE_STYLE = "unicode"
ASCII_STYLE = "ascii"

_STYLES: dict[str, dict[str, str]] = {
    UNICODE_STYLE: {
        "h": "─",
        "v": "│",
        "tl": "┌",
        "tr": "┐",
        "bl": "└",
        "br": "┘",
        "right": "▶",
        "left": "◀",
        "down": "▼",
        "up": "▲",
    },
    ASCII_STYLE: {
        "h": "-",
        "v": "|",
        "tl": "+",
        "tr": "+",
        "bl": "+",
        "br": "+",
        "right": ">",
        "left": "<",
        "down": "v",
        "up": "^",
    },
}


class Grid:
    """Mutable character canvas with 0-based columns and rows."""

    def __init__(self, width: int, height: int, style: str = UNICODE_STYLE) -> None:
        """Create a blank canvas filled with spaces.

        :param width: Column count, inclusive of borders.
        :param height: Row count.
        :param style: ``unicode`` (default) or ``ascii``.
        :raises ValueError: If size or style is invalid.
        """
        if width < 1 or height < 1:
            raise ValueError("width and height must be at least 1")
        if width > MAX_WIDTH:
            raise ValueError(f"width must be <= {MAX_WIDTH}")
        if style not in _STYLES:
            raise ValueError(f"style must be one of {sorted(_STYLES)}")
        self._width = width
        self._height = height
        self._style = style
        self._cells: list[list[str]] = [
            [" " for _ in range(width)] for _ in range(height)
        ]

    @property
    def width(self) -> int:
        """Return the canvas width in columns."""
        return self._width

    @property
    def height(self) -> int:
        """Return the canvas height in rows."""
        return self._height

    @property
    def style(self) -> str:
        """Return the box-drawing style name."""
        return self._style

    def put(self, x: int, y: int, char: str) -> None:
        """Write one character at ``(x, y)``.

        :param x: Column.
        :param y: Row.
        :param char: Single character.
        :raises ValueError: If ``char`` is not length 1 or the cell is out of bounds.
        """
        if len(char) != 1:
            raise ValueError("char must be a single character")
        if not (0 <= x < self._width and 0 <= y < self._height):
            raise ValueError(
                f"cell ({x}, {y}) is outside the {self._width}x{self._height} grid"
            )
        self._cells[y][x] = char

    def text(self, x: int, y: int, value: str) -> None:
        """Write ``value`` starting at ``(x, y)`` without wrapping.

        :param x: Starting column.
        :param y: Row.
        :param value: Text to write.
        :raises ValueError: If the text would leave the canvas.
        """
        if y < 0 or y >= self._height:
            raise ValueError(f"row {y} is outside the grid")
        if x < 0 or x + len(value) > self._width:
            raise ValueError(f"text at column {x} exceeds grid width {self._width}")
        for index, char in enumerate(value):
            self.put(x + index, y, char)

    def box(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        lines: Sequence[str] | None = None,
    ) -> None:
        """Draw a rectangle and center optional interior labels.

        :param x: Left column of the box.
        :param y: Top row of the box.
        :param width: Box width including borders.
        :param height: Box height including borders.
        :param lines: Interior labels, truncated to the inner width.
        :raises ValueError: If the box does not fit.
        """
        if width < 2 or height < 2:
            raise ValueError("box width and height must be at least 2")
        if x < 0 or y < 0 or x + width > self._width or y + height > self._height:
            raise ValueError("box does not fit on the grid")
        glyphs = _STYLES[self._style]
        inner_width = width - 2
        top = glyphs["tl"] + (glyphs["h"] * inner_width) + glyphs["tr"]
        bottom = glyphs["bl"] + (glyphs["h"] * inner_width) + glyphs["br"]
        self.text(x, y, top)
        for row in range(1, height - 1):
            self.put(x, y + row, glyphs["v"])
            self.put(x + width - 1, y + row, glyphs["v"])
        self.text(x, y + height - 1, bottom)
        labels = list(lines or ())
        inner_height = height - 2
        start_row = y + 1 + max((inner_height - len(labels)) // 2, 0)
        for offset, label in enumerate(labels[:inner_height]):
            clipped = label[:inner_width]
            pad_left = (inner_width - len(clipped)) // 2
            self.text(x + 1 + pad_left, start_row + offset, clipped)

    def h_arrow(self, x1: int, x2: int, y: int, label: str = "") -> None:
        """Draw a horizontal arrow from ``x1`` toward ``x2`` at row ``y``.

        :param x1: Start column.
        :param x2: End column, which receives the arrow head.
        :param y: Row.
        :param label: Optional connector label, placed on the row above when possible.
        :raises ValueError: If the arrow is too short or out of bounds.
        """
        if x1 == x2:
            raise ValueError("horizontal arrow needs distinct columns")
        glyphs = _STYLES[self._style]
        step = 1 if x2 > x1 else -1
        head = glyphs["right"] if step > 0 else glyphs["left"]
        for column in range(x1, x2, step):
            self.put(column, y, glyphs["h"])
        self.put(x2, y, head)
        if label and y > 0:
            span = abs(x2 - x1) + 1
            clipped = label[:span]
            start = min(x1, x2) + max((span - len(clipped)) // 2, 0)
            self.text(start, y - 1, clipped)

    def v_arrow(self, x: int, y1: int, y2: int, label: str = "") -> None:
        """Draw a vertical arrow from ``y1`` toward ``y2`` at column ``x``.

        :param x: Column.
        :param y1: Start row.
        :param y2: End row, which receives the arrow head.
        :param label: Optional connector label, placed to the right when possible.
        :raises ValueError: If the arrow is too short or out of bounds.
        """
        if y1 == y2:
            raise ValueError("vertical arrow needs distinct rows")
        glyphs = _STYLES[self._style]
        step = 1 if y2 > y1 else -1
        head = glyphs["down"] if step > 0 else glyphs["up"]
        for row in range(y1, y2, step):
            self.put(x, row, glyphs["v"])
        self.put(x, y2, head)
        if label:
            clipped = label
            if x + 1 + len(clipped) <= self._width:
                self.text(x + 1, min(y1, y2) + abs(y2 - y1) // 2, clipped)

    def render(self) -> str:
        """Return the canvas as newline-separated text without trailing spaces.

        :returns: Diagram text with a trailing newline.
        """
        lines = ["".join(row).rstrip() for row in self._cells]
        while lines and not lines[-1]:
            lines.pop()
        return "\n".join(lines) + ("\n" if lines else "")


def _demo() -> str:
    """Return a small routing diagram used as a smoke example."""
    grid = Grid(40, 9)
    grid.box(12, 0, 16, 3, ["Request"])
    grid.v_arrow(19, 3, 4, "in")
    grid.box(8, 5, 24, 3, ["Subspace"])
    return grid.render()


def main(argv: Sequence[str] | None = None) -> int:
    """Run the grid helper CLI.

    :param argv: Optional argument list; defaults to ``sys.argv[1:]``.
    :returns: Process exit code.
    """
    parser = argparse.ArgumentParser(
        description="Build aligned box diagrams on a character grid."
    )
    parser.add_argument("--demo", action="store_true", help="print a sample diagram")
    args = parser.parse_args(argv)
    if args.demo:
        sys.stdout.write(_demo())
        return 0
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
