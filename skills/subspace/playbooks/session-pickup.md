### Session pickup

**You own the resume point. Read the prior trail, don't redo it.** For "take over this", "resume this conversation", "continue from <transcript path>", "you're taking over", "pick up where X left off", a cloud-agent URL handoff, or a pushed branch you're meant to continue.

A pickup is inheritance. The prior agent already paid the cost of reading the code, running the repros, making the design choices. Redoing loses the bias check and burns context. Resist the urge to re-derive; read.

1. Locate the prior trail. Use the active workspace's transcript or activity record, an agent handoff URL, or a pushed branch. Do not search other workspaces or sessions. Read the metadata overview and last messages first, then scan back for the decision points. Parse a long transcript in a subagent and keep the reduced timeline in the main thread (**principle-guard-the-context-window**).
2. Reconstruct operational state. The branch and worktree, what already landed (`git log`, `git diff` against the base), the open todos, the decisions made. The prior trail is authoritative input. Resist the bias to re-derive it.
3. Diff done vs pending. Compare what shipped against what was planned, name the resume point, do not redo completed work or re-derive settled decisions. The trail is authoritative for what was done and why; its outcome claims get one check on the real artifact in step 5.
4. Route the remaining work to the matching playbook and pick the verdict: continue the execution, ship a finished recommendation, ratify or override a prior conclusion, or postmortem a failed run. The pickup playbook ends here; the routed playbook owns the rest.
5. Verify the inherited claims against the original goal on the real artifact (**principle-verify-results**). A passing prior self-report is not the proof.

**Reply:** where the prior agent stopped, what you inherited vs redid (ideally nothing redone), the resume point, and the outcome.
