# Language Reference

Write the PR body in Simplified Technical English, as described by ASD-STE100.
The aim is text a reviewer cannot misread. The aim is not text that says less.

## Conflict Order

When these rules conflict, use this order:

1. Keep the technical meaning.
2. Keep facts, modality, logic, uncertainty, and ownership.
3. Keep code, identifiers, paths, commands, product names, and quoted errors
   unchanged.
4. Make the text clear and short.

Do not make a sentence shorter when the shorter sentence loses meaning. A PR
body that drops a risk is worse than a PR body that needs one more line to
state it. Concision applies to structure and repetition, not to substance.

## Rules

- Write one main action or condition in each sentence.
- Use one term for one thing. Do not rotate synonyms for variety.
- Name the actor when the actor is known. Write "the workflow uploads the
  artifact" rather than "the artifact is uploaded".
- Keep the passive voice when the actor is unknown or does not matter.
- Keep the meaning of each modal verb. `must` states a requirement, `should`
  states a recommendation, and `may` states permission or possibility. Do not
  exchange them, and do not use `will` for any of them.
- State exact versions, counts, limits, and units when relevant to the claim.
- Keep negative wording for a prohibition about safety, security, or data loss.
  "Never apply a plan from a failed run" is clearer than a positive rewrite.
- Do not use idioms, metaphors, slang, or rhetorical questions.
- Expand an acronym at first use in prose. Leave acronyms unchanged inside
  code, identifiers, and product names.
- Replace a pronoun with its noun when the reference is not certain.
- Keep a domain term that carries a precise meaning. Do not replace a security,
  protocol, database, or infrastructure term with a general synonym.

Before publishing, resolve wording that could give reviewers different
interpretations. These rules govern the prose, not the selected body shape.
