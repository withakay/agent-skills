# Skill Discovery and Behavior Testing

Test the behavior the skill changes, not only its Markdown. Use fresh agent contexts when practical so prior conversation does not hide a discovery or instruction defect.

## Pick a Risk Tier

| Tier | Use when failure would | Minimum evidence |
| --- | --- | --- |
| Low | Cause a minor formatting or retrieval defect | Validate YAML and links; run one trigger, one near-miss, and one representative application scenario. |
| Medium | Produce wrong files, wasted work, or a reviewable behavioral error | Add a no-guidance baseline when the skill changes behavior; run two application scenarios, including an edge case; compare output with the contract. |
| High | Cause data loss, a security or privacy breach, an external write, an irreversible action, or repeated discipline failure | Run a no-guidance control and combined-pressure scenarios; test approval/refusal boundaries and recovery; repeat fresh-context samples until behavior is stable. |

Raise the tier when scope is broad, instructions conflict with normal agent incentives, or a failure is hard to detect. A pure reference skill can use retrieval and application tests instead of pressure tests.

## Test Discovery

The frontmatter description is the discovery contract.

- Use concrete user language, symptoms, tools, and file types.
- Describe when to load the skill, not the steps it performs.
- Include a boundary when a nearby skill or ordinary capability should win.
- Avoid vague triggers such as "how do I" and universal rules such as "always use" unless they are necessary and verified.

Test at least these cases:

1. **Trigger:** a request that must load the skill.
2. **Near miss:** a similar request that another skill or normal workflow should handle.
3. **Exclusion:** a request explicitly outside the skill's scope.

## Match Guidance to the Failure

- For skipped safety or discipline rules, state the prohibition and the observable approval or stop condition.
- For wrong output shape, define the required parts and order instead of adding a long prohibition list.
- For omitted fields, put required slots in the template or schema.
- For conditional behavior, key the rule to an observable condition rather than a broad rule with many exceptions.

Use a no-guidance control before adding behavior-shaping prose. If the control does not show the failure, do not add speculative guidance. Review outputs manually; keyword counts can confuse quoted examples with actual behavior.

Record only durable findings: the scenario, expected behavior, observed failure, and the smallest instruction change that corrected it.
