### Multi-phase or multi-PR plan

Write the delivery plan before implementation. This is the detailed form
of the Delivery stage in `refine-delivery.md` for work spanning phases or
stacked PRs. Read the accepted intent and approved specification first. The
deliverable is `delivery.md`; task files follow its approval. Don't implement.
Small, low-risk edits use Subspace's fast path unless a plan is explicitly requested.

1. When the change is one or two files with an obvious approach, use the short delivery template in `refine-delivery.md`. Keep delivery approval; skip only this multi-phase skeleton.
2. Resolve material implementation questions with a bounded prototype before
   writing the plan. Keep its commit SHA and relevant evidence for Appendix A.
   Use **architect**, design only, for a non-trivial or contested approach.
   Ask the owner about product or preference decisions that evidence cannot
   resolve. Return changed behavior requirements to specification.
3. Explore in independent agents using the host's available delegation mechanism (**principle-guard-the-context-window**). Each returns file pointers, conventions, test commands, and entry points. Do not inline large dumps.
4. Expand the change folder's `delivery.md` with the skeleton per [`change-artifacts.md`](../references/change-artifacts.md). Retain frontmatter, the shippable outcome, acceptance criteria, and a task index. Map each implementation section to `REQ-*` requirements, with one section per pull request. Include only applicable verification surfaces and explain omissions. Each PR's **Files** block names its bounded paths; update delivery scope when those boundaries change. Name the eventual execution playbook in **How to read this**. Record relevant external references when present, but do not publish tracker items before task refinement. PR sections describe implementation order; they do not replace bounded task files.
5. Apply the requested writing style. Use task-focused headings and direct,
   numbered instructions. Put supporting explanation in appendices.
6. Check the plan's structure, unresolved placeholders, and verification steps.
   Use existing repository checks when available; don't add a validator just
   to enforce prose formatting.
7. Hand back the delivery plan for approval. Record the decision in frontmatter, then return to `refine-delivery.md`, Tasks stage. Execution starts only after task readiness, with linked-tracker publication reconciled or explicitly deferred.

**Verification.** Use the smallest checks that cover the change's acceptance
criteria and material risks. Include live checks for a running surface and
performance checks when performance can change. For each applicable check,
name the command or procedure, expected result, and evidence. For a performance
comparison, include a measured baseline and failure threshold. Mark irrelevant
checks as not applicable with a reason. Keep any required interaction review
with screenshots or video before merge.

**Live controls.** Pick controls by surface. Use the host's browser, terminal, simulator, desktop, or service tools. A pull request that touches two surfaces gets scenarios on both. If the host cannot drive a surface, record that as a risk in Appendix C and name the manual or automated evidence still available.

````markdown
# <Program> plan

<Under ten lines. What changes, for whom, the rule the program enforces, and the PR ids in order.>

## How to read this

One box is one unit of work. Every box names the evidence that checks it. A nested box is a sub-step of the box above it. Check a box only when its evidence exists, a file, a log line, a screenshot, a test run, or a SHA. The body is a how-to. The appendices explain and record.

The program runs the Subspace `playbooks/<execution playbook>.md` playbook. <Who merges, and which pull request ids stop at merge-ready.>

Verify each acceptance criterion with the applicable checks. Record why an
omitted check is not applicable.

## Program checklist

### Arm the program

- [ ] State the protocol and this plan to the owner. Start implementation only
      under the owner's authorization; don't request a duplicate approval.
- [ ] Confirm `delivery.md` is approved and its `task-NN-<desc>.md` files are ready. Reconcile linked-tracker publication or record the owner's explicit deferral before execution.
- [ ] Record the authorized goal in the host's task record with this text. "<The plan path, the pull request ids in order, the verification rule, who merges, and the done condition.>"
- [ ] Use **check-change-readiness** before implementation.
- [ ] Read these at program start and re-read them at every tick, from the installed skill location. When the skills are versioned in this repository, read them from trunk with `git show origin/<default branch>:<path>` so a stale checkout cannot mislead.
  - [ ] The execution playbook, `playbooks/<execution playbook>.md` in the Subspace skill
  - [ ] The Subspace `SKILL.md`
  - [ ] <Host control instructions, when applicable>
  - [ ] The Opening a PR playbook, `playbooks/opening-a-pr.md`
  - [ ] <Each other leaf skill the program uses>
- [ ] Arm the 30-minute audit tick with the host's scheduler, repeat mechanism, or a documented manual checkpoint. Never leave the cadence to memory.
- [ ] Use this tick prompt, verbatim. "Re-read the execution playbook from trunk and the armed goal or task. Audit the operation against both and fix drift in this tick. Probe every active lane and judge progress by side effects only. Stand down a stuck lane and dispatch its replacement now. Then send the operator a status message, whether or not anything changed, with the queue table of pull request, owner, state, and head SHA, the verdicts since the last tick, what merged, open operator gates, and blockers."
- [ ] On the operator's hold or stand-down, send every owner a zero-writes order at once.

### Spawn owners

- [ ] Spawn one owner per PR with the full lifecycle the execution playbook names.
- [ ] Follow this dependency graph. Start dependent work only after its parent merges, or base it on the parent branch when the execution playbook stacks.
  - [ ] <PR id> and <PR id> are independent and first. Both branch from `main`.
  - [ ] <PR id> after <PR id>.
- [ ] Hold the file boundaries. <PR id or class> touches only `<glob>`.
- [ ] Hold the review gate. <PR ids> change an interaction. They wait for the operator's review in chat with screenshots and a video before merge.

### PR mechanics, for every PR

- [ ] Open the pull request ready for review with GitHub CLI or the GitHub web interface. Set the base branch explicitly for dependent pull requests. Use `gh stacks` when the stack-management extension is installed and stacked pull requests are useful.
- [ ] Run the repo's lint and typecheck once before the PR-facing push. Push with hooks on.
- [ ] Run the repository's `deslop` and `unslop` checks before review when available.
- [ ] Read every automated and human review comment, then fix valid findings or record why a comment does not apply.
- [ ] Update the branch from its declared base before review and again before the merge-ready report.

### Verdict and merge, for every PR

- [ ] At the merge-ready head SHA, run the live checks and independent review checks named by the pull request. Include an audit pass that reads the diff and receipts instead of trusting the pull request body.
- [ ] Clean only when every required check is `PASS`. Findings go back to the owner. A new head gets fresh checks and a fresh verdict.
- [ ] <The merge or append rule from the execution playbook, with the patch-id rule from `playbooks/shipping.md`.>

### Boot recipe, for every live lane

Each live lane runs against the pull request head in an isolated environment when available. Drive it with the host's browser, terminal, simulator, desktop, or service controls.

- [ ] Select the project-local verification skill for the surface. If none exists, run **create-verification-skill**; if its feature map or harness is stale, run **maintain-verification-skill** before driving the lane.
- [ ] `git fetch origin <head-branch> && git checkout <head SHA>`.
- [ ] <Start the backend and the surface. Wait for ready.>
- [ ] <Deliver input only through the control skill's commands. Name the read-only diagnostics.>
- [ ] Save every screenshot to a stable artifact path and return the paths with the report.

## <Task as a verb phrase> (<PR id>)

**Depends on.** <PR id, or None.>

**Files.**

- [ ] Edit `<path>`.
- [ ] Create `<path>`.
- [ ] Delete `<path>`.

**Build.**

- [ ] <One change. Name the symbol and the file.>

**You see.**

- [ ] <One observable result, with the exact log line or screen state.>

**Verify with tests.** Run the tests that check the changed contract.

- [ ] <Test file and the case it gains.> Run `<command>`.

**Verify live behavior.** Run applicable live scenarios against the pull request head.

- [ ] Lane 1. <Scenario.> Save `<slug>.png`. Pass when <predicate>.
- [ ] Lane 2. <Scenario.> Save `<slug>.png`. Pass when <predicate>.

**Verify performance.** Measure when the change can affect performance; otherwise record why the check is not applicable.

- [ ] Metric. <What is measured.>
- [ ] Probe. <The command or procedure, run at trunk and at the head, interleaved.>
- [ ] Baseline. Record the trunk <value> first.
- [ ] Rule. <Head against trunk, with the number that fails.>

**Review gate.** The operator reviews before merge.

- [ ] Copy lane <n> screenshots into `<media path>/<pr-id>-review-<slug>.png`.
- [ ] Record a 30 to 60 second video of the change in a live lane. Save it as `<media path>/<pr-id>-review.mp4`.
- [ ] Post the screenshots and the video in chat. Stop at merge-ready. Wait for the operator's click.

**Merge.**

- [ ] Root's clean verdict at the exact head SHA.
- [ ] Automated and human review comments resolved or answered.
- [ ] Rebased onto current trunk after the verdict, patch-id unchanged.
- [ ] <The owner or repository maintainer merges the pull request after all gates pass.>

## Close the program

- [ ] Every box above is checked with its evidence.
- [ ] Reply to the operator with the report the execution playbook names.

## Appendix A. Prototype evidence

<Each open question a prototype answered, with the branch, the SHA, and the artifact links. Each question that stays unproven.>

## Appendix B. Alternatives rejected

<Each approach weighed and why it lost.>

## Appendix C. Risks

<Each risk with the PR it lands in and what the owner watches.>

## Appendix D. Links and reading list

<Docs to read before editing. Which pull requests need the **how** skill, the **architect** skill, or an independent decision review. The durable decision trail and verification-skill paths.>
````

**Reply:** the plan path, the PR ids with their dependencies and the review-gated set, what the prototypes proved and what stays unproven, and the check script's output.
