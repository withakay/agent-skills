---
name: principle-explore-the-design-space
description: "Apply when facing a novel UI interaction or architectural decision with no precedent in the codebase. Build two or three competing prototypes and compare them side by side before committing."
disable-model-invocation: true
---

# Explore the design space

When a novel interaction or architectural decision has no established precedent, build two or three competing prototypes or sketches before implementation. Building the wrong thing costs more than exploring three options. A second flavor of the first shape doesn't count.

Compare the alternatives on interface size, invalid states they prevent, and how you would verify the winner. Record why you rejected each loser. Only then commit.

## When it applies

- Novel UI interactions with no prior art in the codebase
- Architectural choices with multiple viable approaches
- Product design decisions where user experience depends on feel, not logic

## When it doesn't

- Mechanical implementation where the pattern is established
- Bug fixes or refactors with a clear target state
- Changes where constraints dictate a single viable approach
