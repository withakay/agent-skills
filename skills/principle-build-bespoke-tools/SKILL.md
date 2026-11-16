---
name: principle-build-bespoke-tools
description: "Apply when work has concrete mechanical repetition or needs a rerunnable check that existing tools do not provide. Build the smallest script, codemod, or skill."
disable-model-invocation: true
---

# Build bespoke tools

When existing tools do not fit, build the smallest tool that does or proves the work instead of repeating it by hand.

There are two payoffs. Throughput: a codemod, generator, or script does the work the same way every time and reruns for free. Confidence: the tool is one artifact a reviewer can read and rerun to check the work. Hand-done changes can only be re-verified by redoing them. A deterministic script turns "trust me" into "run this".

## Pattern

Use existing project helpers, the standard library, native platform features, or an installed tool first. Build a new tool only for concrete mechanical repetition or a verification need that those do not cover.

- Do the first unit by hand to learn the recipe, then build the tool. Prove it by rerunning it on that unit and diffing against your hand-done version. Make the tool safe to rerun. A reviewer will.
- Use a codemod or script for edits, a generator for repetitive files, a dump-to-sqlite query for analysis, or a rerunnable check for verification.
- A deterministic tool beats fan-out. If the tool can process every unit in one pass, run it yourself. Don't fan out delegates to hand-apply what a script can do.
- When you fan work out to subagents, write the tool as a skill they all read: the recipe, the verification contract, and the do-not-touch fences in one artifact, so every delegate inherits the same hardened version instead of re-explaining it per prompt and watching each one drift. Keep it outside the delegates' write scope so they can't quietly edit the contract.
- Do not create a file just to satisfy this principle. Do not build a framework or reimplement an existing tool.
- Commit the tool only when the user authorizes commits and the work outlives the session.

## Balance

The bar is concrete need, not non-triviality. A one-off can earn a tool when the tool is what makes the work checkable. Per [Less is more](../principle-less-is-more/SKILL.md), build the smallest script that does or proves the job, never a framework.

This is distinct from [Capture learnings](../principle-capture-learnings/SKILL.md), which makes a recurring instruction a durable guardrail. This principle is throughput and reviewability on the work in front of you. For scripting the verification itself, see [Verify results](../principle-verify-results/SKILL.md).
