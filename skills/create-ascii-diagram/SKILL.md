---
name: create-ascii-diagram
description: "Use when asked to draw, sketch, or visualize architecture, flow, sequence, state, tree, before/after, or box-and-arrow structure as ASCII or Unicode text; when a diagram must render in a terminal, git diff, code comment, or Markdown fence; or when existing text boxes are misaligned. Do not use when the user asks for Mermaid, PlantUML, or SVG source as the deliverable, or for raster-to-ASCII art."
---

# Create ASCII Diagram

Draw structure on a character grid. Alignment is computed, not counted.

## Output

1. Optional one-line title.
2. Diagram in a fenced `text` block.
3. One to three bullets on how to read it.

## Workflow

1. **PLAN.** Choose a kind from [`references/patterns.md`](references/patterns.md). List elements, edges, direction, and sizes. Box width = longest label + 4. Gutter ≥ 3. Total width ≤ 100; split if it will not fit. Write the plan before any drawing.
2. **DRAW.** Write and run a Python snippet that constructs `Grid`, calls `box` / `h_arrow` / `v_arrow`, and prints `render()`. `--demo` is only a smoke test. Pasting Unicode by hand is the same defect as counting `+` boxes. Unicode style is the default (`┌ ─ │ ▶ ▼`). Use `style="ascii"` only for code comments or when the user asks for plain ASCII.
3. **VERIFY.** Write the diagram to a temp file and run `python3 scripts/verify.py <path>`. Exit 0 is required before showing the diagram. If nested boxes confuse the checker, print a column ruler, fix remaining ragged borders, and re-run. The checker counts any `+`, `-`, or `|` as an ASCII box character, so in a Unicode diagram a label that contains one, such as a hyphenated word, is reported as a mixed charset; reword the label.

```bash
python3 scripts/grid.py --help
python3 scripts/grid.py --demo
python3 scripts/verify.py diagram.txt
```

Resolve `scripts/` relative to this skill directory.

## Charset

- Unicode: `┌┐└┘─│├┤┬┴┼▶▼◀▲`
- ASCII fallback: `+ - | > < v ^`
- Never mix the two. No emoji. No tabs. Label every arrow.

## Rationalizations

| Excuse | Reality |
| --- | --- |
| "Quick sketch, I'll align later" | Misaligned boxes are the deliverable defect. Verify before showing. |
| "I can count columns" | Hand-counted columns drift. `Grid` computes them. |
| "Plus-minus is close enough" | Default is Unicode. ASCII only for the fallback cases above. |
| "I ran --demo / I used Unicode so Grid is optional" | The drawing is the `Grid` snippet. Verify cannot invent layout. |

## Red flags

Freehand `+--+` or freehand Unicode after this skill loaded, unlabeled arrows, mixed `┌` and `+`, width past 100, presenting a diagram that `verify.py` has not passed, or a crowded canvas that should have been split.
