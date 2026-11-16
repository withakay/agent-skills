# Diagram patterns

Pick the closest kind, then PLAN boxes and edges before drawing.

## Architecture / flow (left to right or top to bottom)

Boxes are components. Arrows are labeled with the thing that moves (HTTP, event, file).

## Sequence

Actors along the top. Time runs down. Keep arrows labeled with the message name.

## State

One box per state. Arrows named with the event. Mark the start state.

## Tree

Parent above children. Use `├` / `└` only in Unicode style; do not mix with `+`.

## Before / after

Two columns separated by a double-line or a labeled gutter. Shared entry sits above the split.

## Split rule

If PLAN width exceeds 100 columns, draw two diagrams (happy path vs errors, or one layer each) instead of shrinking labels into noise.
