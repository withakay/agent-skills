---
name: principle-focus-on-the-core-domain
description: "Apply when prioritizing domain discovery, bespoke development, or reuse across capabilities. Not for ranking tasks by technical difficulty."
---

# Focus on the core domain

Concentrate modeling effort on the domain capability that makes the system
distinctive and valuable. The Core Domain is not automatically the largest,
most complex, or currently edited subsystem.

- Use business goals and available evidence to explain what is core. Mark
  uncertain classifications as hypotheses; revisit them when strategy changes.
- State the domain vision briefly: the valuable capability and why it matters.
  Make the core easy to locate in the model and implementation.
- Separate generic capabilities from distinctive domain knowledge. Consider
  existing products or simpler implementations before bespoke development.
- Keep necessary supporting work proportionate to its role. Generic does not
  mean optional, low quality, or exempt from security and reliability needs.
- Judge a proposed abstraction by whether it clarifies the core. Do not build
  a reusable framework merely because the current problem permits one.

For example, an allocation optimizer may justify deep domain modeling while
identity uses an established product. Confirm that distinction from the
system's goals rather than assuming it for every business.

Use [Domain modeling](../domain-modeling/SKILL.md) to connect this decision to
the current intent and delivery plan.
