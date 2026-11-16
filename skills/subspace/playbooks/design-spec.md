### Design the specification

Define precisely what behavior must exist. This full-workflow stage requires
an accepted `intent.md`. The deliverable is a behavioral or functional specification,
not an implementation design. Follow
[`change-artifacts.md`](../references/change-artifacts.md).

1. Read the intent and its evidence. Resolve questions that affect observable
   behavior with focused research, brainstorming, or questions for the user.
   Consider the Spec principles in
   [`principle-routing.md`](../references/principle-routing.md) before writing
   requirements. Explicitly load those whose triggers the evidence meets, reuse
   bodies already in context, and apply them to observable behavior only. Record
   a material effect in the owning spec section; add no principles section.
   A principle may reveal an open policy or recovery choice, not authorize its
   answer. Keep sourced behavior separate from proposals. Do not turn a
   plausible pattern into a new requirement without intent or evidence.
   Requirements and pass predicates contain only sourced behavior. Put proposed
   choices in unresolved decisions, not in normative REQ statements. Mark any
   acceptance example that depends on an unapproved choice as blocked.
2. Choose the clearest notation for the context: Easy Approach to Requirements
   Syntax (EARS), Gherkin
   scenarios, decision tables, state transitions, interface contracts, or
   precise functional prose. Load **writing-ears** or **writing-gherkin** when
   using those forms. State the choice briefly; no single format is mandatory.
   When requirements describe structure, flow, or state, load **create-ascii-diagram** and include a verified text diagram beside the requirement text.
3. Give each requirement a stable ID, such as `REQ-01`. Define the actor or
   system, preconditions, trigger or input, observable result, and acceptance
   condition. Define domain terms, units, thresholds, and boundary values.
   Include permissions, validation, failure behavior, and state transitions
   where relevant. Replace words such as "fast" with measurable conditions.
   When meaning differs across contexts, use [domain-modeling](../../domain-modeling/SKILL.md)
   and **principle-evolve-a-shared-domain-language**. Scope terms and scenarios
   to their bounded context. Record a new or redefined term in the project's
   glossary and link that entry from the spec. For cross-context contracts,
   specify meaning, ownership, and observable outcomes, not just field shapes.
4. Cover normal, boundary, and failure cases. Write examples where they resolve
   ambiguity; identify observable verification for every requirement. Include
   relevant functional constraints and exclusions from the intent. Do not
   invent policy, latency, volume, or reliability requirements.
5. Separate externally required contracts from implementation choices. An API
   response or file format can be specified here; a library, module layout, or
   algorithm normally belongs in `delivery.md`. Record a mandated technology
   as a sourced constraint rather than presenting it as required behavior.
6. Check for contradictory requirements, undefined terms, missing outcomes,
   and unresolved decisions. Each intent question is answered, explicitly out
   of scope, or carried forward with an owner. A behavior-defining question
   blocks approval; do not fill it with a guess.
7. Write `spec.md` with `status: draft` using the template. Ask for human
   approval. Record approval as `status: approved`, then route to
   `refine-delivery.md`. Do not implement or create tracker items.

**Reply:** spec path, chosen notation, requirement coverage, blocking questions,
and pending approval. Commit only when authorized.
