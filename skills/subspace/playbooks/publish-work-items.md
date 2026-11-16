### Publish delivery and tasks

Publish the refined local artifacts to the project's linked tracker and
reconcile the result. This requires an approved `delivery.md` and ready task files.
This playbook uses existing tracker tools; it does not require a new integration.

1. Find the linked tracker, project or team, and board from repository
   configuration, project documentation, existing work-item links, or an
   explicit user selection. Credentials alone do not establish a project link.
   If no tracker is linked, retain local artifacts and report local-only
   delivery. If the target is ambiguous, ask which target to use before writes.
2. Load the matching provider skill or tool instructions and inspect supported
   types, required fields, workflow states, and parent-child relationships.
   Azure DevOps normally uses a product backlog item (PBI) with child Tasks.
   For Jira, use the project's
   configured story or delivery type with subtasks; for Linear use the configured
   parent issue and sub-issues. Adapt to the actual process. If the hierarchy
   cannot be represented, report the mismatch and obtain a mapping decision.
3. Read existing IDs and URLs from `delivery.md` and each task file. Fetch those
   items and verify their project and identity before choosing create or update.
   Include a stable source identity (repository identity plus artifact path)
   and a source link or path in each tracker item. Search that identity before
   creating an item whose ID was not recorded after a partial failure. Do not
   match by title alone. Ambiguous matches require reconciliation before writes.
4. Preview the exact target, new items, updates, parent-child links, and mapped
   title, description, acceptance, and required fields from the Markdown. Do
   not invent assignees, iterations, estimates, priority, or workflow state.
   Resolve conflicting remote edits with the owner before overwriting them.
5. Obtain approval of the preview, then publish the parent first. Immediately
   record its returned ID and URL in `delivery.md`. Publish or update each
   child, link it to that parent, and immediately record its ID, URL, and parent
   identity in its task file. Preserve returned identities even if a later
   write or read-back fails. Do not mark them verified yet.
6. Read back the parent and children. Verify title, scope, acceptance criteria,
   project, required fields, source identity, and actual parent-child links.
   Compare meaning rather than formatting if the provider transforms Markdown. Record
   verification dates in the source files; update existing `ext-refs.md` and
   downstream links when present. Never claim synchronization from write
   success alone.
7. On a partial failure, report exactly which items were created, updated,
   linked, or remain unverified. Preserve local work and successful IDs. Resume
   from fetched state rather than recreating the set. An inaccessible linked
   board is a publication blocker, not the same as having no tracker. Let the
   owner decide whether to defer publication and proceed locally.

External systems own live state; local Markdown owns the reviewed delivery
definition. Later refinements repeat preview, approval, update, and read-back.
Do not close or delete work items merely because publication finished.

After reconciliation, use **check-change-readiness** before implementation.
This check doesn't require another publication approval.

**Reply:** parent and child IDs with URLs, verified relationships, local paths
updated, remaining mismatches, and the next execution task.
