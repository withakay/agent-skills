#!/usr/bin/env python3
"""Tests for demo.py."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import time
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("demo.py")
SPEC = importlib.util.spec_from_file_location("runnable_demo_tool", MODULE_PATH)
assert SPEC and SPEC.loader
DEMO_TOOL = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = DEMO_TOOL
SPEC.loader.exec_module(DEMO_TOOL)


class HeadingPatternTests(unittest.TestCase):
    """Heading patterns match the same lines as before in linear time."""

    def step_starts(self, text: str) -> list[int]:
        return [match.start() for match in DEMO_TOOL.STEP_PATTERN.finditer(text)]

    def h2_title(self, line: str) -> str | None:
        match = DEMO_TOOL.H2_PATTERN.match(line)
        return match.group(1).strip() if match else None

    def test_step_pattern_accepts_supported_heading_forms(self) -> None:
        for heading in (
            "### 1. Greet",
            "### 2: Greet",
            "### 3 - Greet",
            "### 4 Greet",
            "### Step 5 Greet",
            "### step\t6. Greet",
            "### 7 -Greet",
        ):
            with self.subTest(heading=heading):
                self.assertEqual([0], self.step_starts(heading))

    def test_step_pattern_rejects_non_step_headings(self) -> None:
        for heading in (
            "### Greet",
            "### 1.Greet",
            "#### 1. Greet",
            "### 1.",
            "### 1.   ",
        ):
            with self.subTest(heading=heading):
                self.assertEqual([], self.step_starts(heading))

    def test_step_pattern_keeps_each_heading_on_its_own_line(self) -> None:
        text = "### 1\n### 2. Second\n###\n3. Not a heading\n"
        self.assertEqual([text.index("### 2")], self.step_starts(text))

    def test_step_pattern_does_not_cross_other_line_boundaries(self) -> None:
        for boundary in ("\r", "\r\n", "\v", "\f", "\x1c", "\x85", "\u2028", "\u2029"):
            for text in (f"### 1{boundary}2. Greet", f"### 1.{boundary}Greet"):
                with self.subTest(text=text):
                    self.assertEqual([], self.step_starts(text))

    def test_step_pattern_is_linear_on_long_whitespace(self) -> None:
        text = ("### 1" + " " * 50_000 + "\n") * 4
        started = time.perf_counter()
        self.assertEqual([], self.step_starts(text))
        self.assertLess(time.perf_counter() - started, 1.0)

    def test_h2_pattern_is_linear_on_long_whitespace(self) -> None:
        # The former regex took seconds here; this one takes milliseconds.
        line = "##" + " " * 50_000 + "x" + " " * 50_000 + "\x00"
        started = time.perf_counter()
        self.assertEqual("x" + " " * 50_000 + "\x00", self.h2_title(line))
        self.assertLess(time.perf_counter() - started, 1.0)

    def test_h2_pattern_matches_level_two_headings_only(self) -> None:
        cases = {
            "## Cleanup": "Cleanup",
            "##\tSteps  ": "Steps",
            "##  ": "",
            "## ": None,
            "##Cleanup": None,
            "### Cleanup": None,
            "# Cleanup": None,
            "": None,
        }
        for line, expected in cases.items():
            with self.subTest(line=line):
                self.assertEqual(expected, self.h2_title(line))


class DemoToolTests(unittest.TestCase):
    def write_demo(self, root: Path, name: str, body: str) -> Path:
        path = root / "demos" / name / "DEMO.md"
        path.parent.mkdir(parents=True)
        path.write_text(body, encoding="utf-8")
        return path

    def test_accepts_markdown_demo(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_demo(
                Path(directory),
                "hello",
                "---\nname: hello\ndescription: Show a greeting.\n---\n\n# Hello\n",
            )
            demo = DEMO_TOOL.inspect_demo(path)
            self.assertEqual("markdown", demo.kind)
            self.assertEqual((), demo.errors)

    def test_accepts_complete_runnable_step(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_demo(
                Path(directory),
                "hello",
                """---
name: hello
description: Show a greeting.
---

## Steps

### 1. Greet

**Action**

Say hello.

**Verify**

Read the output.

**Accept**

- [ ] Output is `hello`.
""",
            )
            demo = DEMO_TOOL.inspect_demo(path)
            self.assertEqual("runnable", demo.kind)
            self.assertEqual((), demo.errors)

    def test_numbered_heading_outside_steps_stays_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_demo(
                Path(directory),
                "hello",
                """---
name: hello
description: Show a greeting.
---

### 1. Narrative section

This is not a runnable step.
""",
            )
            demo = DEMO_TOOL.inspect_demo(path)
            self.assertEqual("markdown", demo.kind)
            self.assertEqual((), demo.errors)

    def test_rejects_incomplete_step_and_broken_link(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_demo(
                Path(directory),
                "hello",
                """---
name: hello
description: Show a greeting.
---

[Missing](references/missing.md)

## Steps

### 1. Greet

**Action**

Say hello.
""",
            )
            errors = DEMO_TOOL.inspect_demo(path).errors
            self.assertIn("step 1 is missing Verify", errors)
            self.assertIn("step 1 is missing Accept", errors)
            self.assertIn("broken local link: references/missing.md", errors)

    def test_parses_named_executable_fence_without_changing_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_demo(
                Path(directory),
                "hello",
                """---
name: hello
description: Show a greeting.
---

## Steps

### 1. Greet

**Action**

```bash demo id=greet effect=local terminal=main timeout=45
name='world'
printf 'hello %s\\n' "$name"
```

**Verify**

```bash demo id=verify-greeting effect=read
grep -qx 'hello world' greeting.txt
```

**Accept**

- [ ] Output is `hello world`.
""",
            )

            blocks, errors = DEMO_TOOL.executable_blocks(path)

            self.assertEqual((), errors)
            self.assertEqual(2, len(blocks))
            self.assertEqual("greet", blocks[0].id)
            self.assertEqual("action", blocks[0].role)
            self.assertEqual(
                "name='world'\nprintf 'hello %s\\n' \"$name\"", blocks[0].source
            )
            self.assertEqual(45.0, blocks[0].timeout)
            self.assertEqual("main", blocks[1].terminal)

    def test_rejects_unsafe_or_ambiguous_execution_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_demo(
                Path(directory),
                "hello",
                """---
name: hello
description: Show a greeting.
---

## Steps

### 1. Greet

**Action**

```bash demo id=same effect=write surprise=yes
echo one
```

**Verify**

```bash demo id=same effect=write
echo two
```

**Accept**

- [ ] Output exists.
""",
            )

            errors = DEMO_TOOL.inspect_demo(path).errors

            self.assertIn("line 12: unknown demo attribute 'surprise'", errors)
            self.assertIn("line 18: Verify blocks must use effect=read", errors)
            self.assertIn("duplicate demo block id 'same'", errors)

    def test_tui_and_prompt_modes_require_wait_text(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_demo(
                Path(directory),
                "hello",
                """---
name: hello
description: Show a greeting.
---

## Steps

### 1. Greet

**Action**

```bash demo id=status effect=read mode=tui after-capture=q
status-ui
```

**Verify**

Read the screen.

**Accept**

- [ ] Status is ready.
""",
            )

            errors = DEMO_TOOL.inspect_demo(path).errors

            self.assertIn("line 12: mode=tui requires wait-text", errors)


if __name__ == "__main__":
    unittest.main()
