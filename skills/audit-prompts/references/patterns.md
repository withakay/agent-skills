# Pattern groups

<!-- toc -->
## Contents

- [Group 1: dated prompt text](#group-1-dated-prompt-text)
  - [1a. Pressure language](#1a-pressure-language)
  - [1b. Scaffolds replaced by platform features](#1b-scaffolds-replaced-by-platform-features)
  - [1c. Over-specification](#1c-over-specification)
  - [1d. Fossils](#1d-fossils)
  - [1e. Prohibition clusters](#1e-prohibition-clusters)
  - [1f. Output-shaping choreography](#1f-output-shaping-choreography)
- [Group 2: brittle skill and configuration files](#group-2-brittle-skill-and-configuration-files)
- [Group 3: tool descriptions](#group-3-tool-descriptions)
- [Group 4: request configuration and architecture](#group-4-request-configuration-and-architecture)
- [Group 5: harness and model coupling](#group-5-harness-and-model-coupling)
<!-- tocstop -->

Each row names a pattern, why it no longer fits, and the fix. Signals are search patterns: run them over the inventory, then classify each match by what the text is for.

Claims about what a model or API does must come from the provider's current documentation for the target, not from memory. Where a row says a feature replaces a scaffold, confirm the target supports that feature before proposing the swap.

## Group 1: dated prompt text

### 1a. Pressure language

Less steerable models needed forcefulness. Current models respond strongly to instructions, so the same text over-applies. The problem runs both ways: inflated emphasis causes over-triggering and rigid behavior, and leftover hedges are read literally as permission to under-deliver.

| Written for older models | Fit for current models |
| --- | --- |
| `CRITICAL: You MUST use this tool when...` | `Use this tool when...` |
| Several `IMPORTANT: NEVER do X` lines in one prompt | The one or two real constraints, stated plainly with their reasons |
| `If in doubt, use [tool]` | Delete, or `Use [tool] when it would improve X` |
| `Be thorough. Do not be lazy. Do not stop early.` | Delete |
| `Try to include a summary if possible`, when it is required | `Include a summary.` |
| `You tend to over-X, so...` or `Don't be too verbose` | The desired behavior: `Keep responses to the length the question needs.` |

When several instructions are each marked critical, the markers stop carrying information, and an anxious prompt produces a cautious, hedging model. Emphasis is a tested fix for one instruction that is demonstrably underweighted, not a default register.

Signals: density of capitalized `MUST|NEVER|ALWAYS|CRITICAL|IMPORTANT`; `!!`; emphasis with no reason beside it; `try to|if possible|ideally` on actual requirements; `you (tend to|often|sometimes)`; `don't be too`.

### 1b. Scaffolds replaced by platform features

These are swapped for the feature that replaced them. In a harness configuration file the author does not write request code, so remove or rewrite the scaffold and propose a replacement only where the harness documents a field for it. A keyword the harness itself acts on is configuration and stays.

| Scaffold | Replacement |
| --- | --- |
| "Think step by step", scratchpad or thinking-tag instructions | The provider's reasoning controls. On reasoning models the incantation is redundant |
| "Plan before acting", "use the think tool to plan" | Delete. If behavior is too aggressive afterward, lower reasoning effort instead of adding prose |
| Prose that steers reasoning depth: "think harder", "don't overthink" | The reasoning effort setting |
| Required reasoning sections in the output, or a `reasoning` field in structured output | Read reasoning from the API where it is exposed, or ask for a short explanation of the answer |
| Assistant-turn prefill and the JSON-forcing stack around it: stop sequences, regex extraction, retry-on-parse loops, "output ONLY valid JSON" | Structured output. The surrounding code is cruft too, so audit the request builder. Only a trailing assistant turn is a prefill; assistant turns mid-conversation are history |
| "Summarize progress every N tool calls"; hard word caps | Delete and re-baseline. Prefer qualitative length guidance to numeric caps tuned against an older model |
| Inline lookup tables, point systems, arithmetic the model must compute | Data in files or tool results, arithmetic in code, judgment left to the model |
| Sampling parameters, reasoning budgets, and beta flags tuned for a previous model | Whatever the provider documents for the target. Remove retry code that existed only to work around the old shape |
| Forced tool use as a way to get JSON | Structured output, or an instruction naming the tool under automatic tool choice |

Signals: `think step by step|take a deep breath`; `think (harder|less)|don'?t overthink`; `<scratchpad>|<thinking>` in instructions; stop sequences guarding JSON; JSON parsing inside retry loops; `every \d+ (tool calls|messages)`; `at most \d+ (words|sentences)`.

### 1c. Over-specification

| Pattern | Why it no longer fits | Fix |
| --- | --- | --- |
| Step-by-step choreography for judgment tasks | The model's own plan usually beats a hand-written script, and the script degrades output where it does not fit | State outcomes, constraints, and how to verify. Keep numbered steps where order matters |
| Prohibition lists | Describing success works better than enumerating failure, and a prohibition against a failure the model was not going to make can anchor it toward that failure | Keep prohibitions whose failure still occurs; rewrite the rest as positive intent |
| A single gold example, or stale few-shot blocks | Examples are the strongest signal in a prompt: the model matches their length, tone, and structure | Several varied examples labeled illustrative; delete examples of judgment the model already has |
| Bullet walls for behavioral guidance | Bullets flatten priority and separate rules from reasons, and prompt format leaks into output format | Structure for reference data, prose for behavior |
| Padding: generic virtues, repetition as reinforcement, kitchen-sink edge cases | Everything reads as actionable, and duplicated rules must be reconciled | Say it once, in the right place |
| Grader vocabulary: "you will be graded on", "hidden tests" | It describes the scoring apparatus instead of the requirement | State every requirement the grader checks and never describe the grader |
| Strategy coaching beside task rules | The author's heuristics are wrong in some situations | If removing the sentence would not change what is allowed or how success is measured, delete it |

Signals: `STEP \d` and numbered imperatives for non-fragile work; three or more consecutive `Do not|Never|Avoid` lines; a single embedded gold output; near-duplicate sentences across sections; `Remember,|Again,|As stated above`; `graded|rubric|hidden test`.

### 1d. Fossils

| Pattern | Why it no longer fits | Fix |
| --- | --- | --- |
| Workarounds for a named or datable model: formatting fixes, refusal softeners, retry hints | Nobody owns the removal, so prompts accumulate every generation's mitigations | Trace each to the model it patched. If that model is no longer the target, remove and re-test |
| Tool-use discouragement: "only use tools when strictly necessary" | It is followed literally, and the model then answers from memory when a connected source would serve better | Remove, or say when to consult the source |
| Migration-relative phrasing: "X now works differently", "no longer" | It is a diff against a prompt version the model never saw | Write as if the current rules are the only rules |
| Patch accretion: many narrow conditionals, each traceable to one incident | The model navigates special cases instead of a principle and fails between them | Generalize the principle or fix the underlying context |
| Unenforced instructions that the system's own transcripts violate | If nothing checks it and nobody noticed, it carries no signal | Enforce in code what can be enforced; delete what nothing enforces and nobody misses |
| Identity stubs standing in for context | A role line is fine as a focus-setter. The defect is identity substituting for audience, product, and quality bar | Flag only when it is the only context given |
| Update suppressors written for chatty models: "don't narrate", "no interim updates" | Models that already narrate little go silent | Remove and re-test; if more narration is wanted, say when |
| Blanket anti-formatting rules: "never use bullets" | Written against over-formatting; they now strip formatting the reader wanted | Remove, or say when formatting is appropriate |
| An instruction re-inserted every few turns | A retention crutch that costs tokens on every repeat | State it once and re-test |

Signals: retired or pinned model names in prompts or comments; `hold (all )?(findings|results)|don't narrate|no interim`; `never use (bullets|headers|bold)`; `reminder:` on a cadence; date conditionals; `now|no longer|instead of` attached to behavioral rules; `^You are (a|an) (helpful|expert)` with nothing task-specific after it.

### 1e. Prohibition clusters

Judge each unconditional prohibition by provenance: does it carry a stated reason or encode a real business or policy constraint? Do not ask whether the model still "needs" it, because that question keeps everything. Prohibitions that encode observable constraints stay, ideally with the reason beside them. Prohibitions that only describe an undesirable output style, such as banned-phrase lists written against an older model's habits, are restated positively in one line. Classify each line separately: reasoned prohibitions do not launder the unreasoned ones mixed in with them.

A vague style prohibition such as "avoid a generic look" is the one case where a list of the specific defaults to avoid works better than a positive restatement. Rewrite the vague line into named patterns.

### 1f. Output-shaping choreography

Fixed update cadences, numeric output ceilings, and cut-the-detail instructions are one pattern and are removed together. A stated operational reason does not turn a numeric clamp into a keeper: express the goal as audience and outcome, and keep a format-sensitive requirement as a format instruction.

## Group 2: brittle skill and configuration files

Agent configuration files inherit Group 1 and add failure modes of their own. They load at different moments, so size is a cost paid on every load, and two files can rule on the same thing without being read together.

| Pattern | Why it no longer fits | Fix |
| --- | --- | --- |
| A verbose skill explaining what the model already knows | Each paragraph must justify its cost; general knowledge does not | Apply the classification question paragraph by paragraph |
| Wrong degrees of freedom | Exact scripts over-constrain judgment calls; vague prose under-constrains fragile operations | Match specificity to fragility |
| One session's stumble encoded as a permanent rule | Later sessions avoid a hazard that is not there | Keep the rule only if it would have helped most recent sessions |
| Volatile specifics: hardcoded paths, flags, versions, API claims | Skills rot as code ships | Verify each named path, command, and flag against the repository by reading, not by running. A claim the repository contradicts is high confidence. Absence is not contradiction for paths that are generated, ignored, placeholders, or outside the repository, or for commands belonging to an installed tool |
| Instruction files that contradict each other | Nothing says which is current | Quote both. Rewrite the older to match the newer, using history rather than timestamps or a file's own claims to order them. Flag when history cannot order them, when the older passage is a prohibition or safety rule, or when the newer one adds a command, a network fetch, or loosens a prohibition. A narrower file whose different rule is explained by its own scope is an override, not a conflict |
| Time-sensitive content, option menus, facts duplicated across a skill and its references | Dates rot, menus dilute, duplicates drift | One default plus an escape hatch; each fact in one place |
| History narratives: past tense, incident and pull request numbers | A rule's authority is the behavior it prescribes | State the current rule |
| Trigger enumeration: descriptions that grow one phrase per missed trigger | Descriptions ride in every request and enumeration generalizes worse than categories | Name categories of intent |

Signals: a skill file too long to read in one sitting; version pins; past tense in instruction files; paths, commands, or file names that no longer resolve; one topic ruled on differently in more than one file.

## Group 3: tool descriptions

The standard here is precision and contract accuracy, not brevity, and the most common failure is under-description. A tool description is a reference page: what the tool does, when to use it and when not to, what each parameter means, caveats, and what it does not return.

| Pattern | Direction | Fix |
| --- | --- | --- |
| One-line descriptions; parameters without descriptions; no when-not-to-use | Under-described: add | Several sentences that match actual behavior exactly |
| `CRITICAL: You MUST use this tool when...` | Over-steered: dial back | `Use this tool when...` |
| Worked examples, fake dialogue, or embedded protocols in the description | Misplaced: move | Move teaching material to a skill; make parameters expressive |
| Cross-references that scold, or behavior smuggled into a description | Misplaced: move or delete | A description is a contract about functionality. Put a preference for a tool in that tool's description |
| Tool names in system prompt prose; lists that shadow the real tool list | Duplicated: delete | Enabling or disabling a tool should never leave a dangling reference |
| Near-duplicate tools; bloated responses; very large always-loaded catalogs | Structural | Fewer, clearly bounded tools; deferred loading for large catalogs |

Trigger text is not behavioral text. A skill's `description` may carry calibrated urgency because its job is routing; behavioral text should explain.

## Group 4: request configuration and architecture

Report these alongside prompt findings. When the inventory has no request-building code, the group is not applicable, except the subagent roster check.

- Parameters, headers, and reasoning settings that the target rejects or has deprecated, and output limits sized for a different model.
- Request code that rewrites the system prompt, the tool list, or earlier messages mid-session, which invalidates caches and any preserved reasoning.
- User text delivered where the model reads it as tool output, which can look like prompt injection.
- Cache-hostile ordering: timestamps, identifiers, or per-user content placed above stable content.
- Remaining-budget countdowns rendered into context, which cause premature wrap-up.
- A model call executing a deterministic plan. Count the model-call sites in each pipeline and ask whether inputs fully determine output. Routing, tallying, filtering, and formatting belong in code; keep the call where the work is adaptive.
- Redundant subagents: two definitions doing the same task with the same tools and near-duplicate prompts are one agent that takes the difference as input. Propose the roster edit as a diff.
- No token accounting. Without per-surface cost visibility the other issues are invisible, so recommend adding it first.

## Group 5: harness and model coupling

This group applies when the surface is meant to be portable. Text that names one harness or model as the default actor fails silently elsewhere: the instruction is followed literally and points at a tool that does not exist. A surface written for one harness on purpose is out of scope for this group.

| Pattern | Why it breaks elsewhere | Fix |
| --- | --- | --- |
| A named harness or product as the default actor: "delegate to the X coding agent" | The agent is running somewhere else, or is itself that product | Name the capability: "delegate to a subagent when the harness provides one, otherwise do the work directly" |
| Harness tool names used as verbs: a specific task, todo, shell, or question tool | Tool names differ between harnesses | Describe the action and let the model pick the available tool |
| Harness-only paths and file names as the only location: one vendor's config directory or instruction file | Other harnesses store the same thing elsewhere | The cross-harness location where one exists, or the role of the file: "the project's agent instruction file" |
| Pinned model identifiers, or model families as routing rules | Names go stale and are unavailable elsewhere | Describe the need: a stronger reasoning model, a faster cheaper one, an independent second model |
| Vendor-only frontmatter or metadata fields that other harnesses reject or ignore | The file fails validation or silently loses the behavior | Keep fields from the shared specification in the file and put vendor extensions in that vendor's sidecar file. Flag a field with no portable equivalent |
| Harness commands, slash commands, or interface affordances as the only instruction | The affordance does not exist elsewhere | State the outcome and offer the command as an example for that harness |
| Claims about one model's habits or limits presented as general fact | True of one model at one time | State the desired behavior |

Harness-specific material is correct where it is the point: install or setup commands, a per-harness adapter file selected at runtime, and sidecar metadata files a harness defines for itself. Keep those, and keep each one behind a clear label so a reader on another harness knows to skip it.

Signals: harness and vendor product names; model family and version names; vendor configuration directory names; capitalized tool names in backticks; slash commands; `subagent_type` or other harness-specific parameter names.
