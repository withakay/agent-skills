#!/usr/bin/env python3
"""Behavior tests for the skill table-of-contents generator."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("add_toc.py")
SPEC = importlib.util.spec_from_file_location("add_toc", SCRIPT)
add_toc = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(add_toc)

FILLER = ["Text."] * 100


def skill(*body: str) -> str:
    return (
        "\n".join(
            ["---", "name: demo", "description: Demo.", "---", "", "# Demo", "", *body]
        )
        + "\n"
    )


class AddTocTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name, "SKILL.md")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_script(self, text: str) -> str:
        self.path.write_text(text, encoding="utf-8")
        add_toc.process(self.path, write=True)
        return self.path.read_text(encoding="utf-8")

    def test_adds_two_level_toc_after_title_and_skips_code_fences(self) -> None:
        text = skill(
            "## Gate Function",
            "### A / B",
            "#### Too deep",
            "````markdown",
            "```",
            "## Not a heading",
            "```",
            "````",
            "## Gate Function",
            *FILLER,
        )
        result = self.run_script(text)

        self.assertIn(
            "# Demo\n\n<!-- toc -->\n## Contents\n\n"
            "- [Gate Function](#gate-function)\n"
            "  - [A / B](#a--b)\n"
            "- [Gate Function](#gate-function-1)\n"
            "<!-- tocstop -->\n\n## Gate Function",
            result,
        )
        self.assertNotIn("not-a-heading", result)
        self.assertNotIn("too-deep", result)
        self.assertTrue(result.startswith("---\nname: demo"))

    def test_rerun_is_stable_and_follows_heading_changes(self) -> None:
        first = self.run_script(skill("## One", "## Two", *FILLER))
        self.assertEqual(self.run_script(first), first)

        renamed = self.run_script(first.replace("## Two", "## Three"))
        self.assertIn("- [Three](#three)", renamed)
        self.assertNotIn("(#two)", renamed)

    def test_replaces_hand_written_contents_in_place(self) -> None:
        text = skill(
            "Intro.",
            "",
            "## Contents",
            "",
            "- [One](#one)",
            "",
            "## One",
            "## Two",
            *FILLER,
        )
        result = self.run_script(text)

        self.assertIn(
            "Intro.\n\n<!-- toc -->\n## Contents\n\n- [One](#one)\n- [Two](#two)\n",
            result,
        )
        self.assertEqual(result.count("## Contents"), 1)

    def test_short_file_is_untouched_and_loses_a_stale_toc(self) -> None:
        short = skill("## One", "## Two")
        self.assertEqual(self.run_script(short), short)

        long_file = self.run_script(skill("## One", "## Two", *FILLER))
        self.assertEqual(self.run_script(long_file.replace("Text.\n" * 100, "")), short)


if __name__ == "__main__":
    unittest.main()
