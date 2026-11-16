# Language-only review

Use this reference to review existing technical prose while respecting the
requested scope. General writing rules remain in the parent skill.

## Triage

Establish whether the user wants findings, edits, or both. Assess each document
before deciding to revise it. A pattern match alone does not justify a rewrite;
leave otherwise readable prose with isolated minor issues unchanged.

Use ratings only when requested or required by the publication. Define which
end of the scale means better prose, and use the task's agreed threshold.
Scores express editorial judgement, not measurements or punctuation counts.
Do not turn one task's numerical threshold into a universal rule.

Revise recurring weaknesses that obstruct the reader's task. Stop when the
document meets the agreed purpose; do not keep editing to eliminate every
detectable stylistic imperfection.

## Preservation

Identify the requested preservation constraints before applying general
structure advice. A language-only task does not authorise reorganising a page
or converting its bullet points into paragraphs.

For a formatting-preserving Markdown edit, retain heading text and levels,
list structure, emphasis, link targets, and code examples. Do not rename a
heading merely to apply sentence case: that can also change its anchor.

Use an available comparison tool for the requested structural invariants, then
read changed claims in context. Matching markup or a successful build does not
prove that the meaning is unchanged; a semantic review does not prove that the
formatting was preserved.

## Worked examples

### Completed prerequisite versus obsolete requirement

Original: "Step 8 requires the projection. The projection is now available."

Reject: "Step 8 previously required the projection."

Prefer: "The projection required by step 8 is now available."

The rejected version can imply that the requirement no longer applies. Keep
both facts: the component is still required, and it is now available.

### Missing feature versus blocking dependency

Original: "The manual check queries the database directly. A status API is
not yet available."

Reject: "The remaining dependency is the status API."

Retain the original wording. The missing API does not prevent the direct
database check. Calling it a dependency can make a working procedure sound
blocked.

### Conditional risk versus inevitable failure

Original: "Access may fail silently if a package upgrade changes the internal
API."

Reject: "The next package upgrade will fail silently."

Retain the condition and uncertainty. The original does not say that the next
upgrade will change the API or cause a failure. It also identifies the access,
rather than the upgrade itself, as the operation that may fail.

### Acceptable punctuation

Keep: "Use a table only for short, scannable cells — at most three or four
columns, each a few words."

The em dash introduces a relevant explanation, and the sentence is readable.
A language-only review need not change it. Apply the parent skill's contextual
punctuation rule rather than replacing every em dash mechanically.

## Review output

State which documents changed and which were left as written. Include scores
only when requested, with a short reason for material changes rather than a
list of every minor infringement.

Report unresolved technical contradictions separately from language quality.
Quote the conflicting claims and identify the decision needed. Do not silently
choose one claim or rewrite around the conflict to make the document sound
consistent. Resolve the claim only with source evidence and within the task's
scope; otherwise keep it visible as a finding.

A low language-problem score does not certify technical correctness. Flag a
material contradiction even when the rest of the document is readable, and
distinguish verified facts from statements that still need confirmation.
