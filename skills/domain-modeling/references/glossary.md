# Glossary location

A project should keep a Markdown glossary of its domain terms, abbreviations,
acronyms, and preferred wording. Record a term where the project already keeps
documentation, not in a change artifact or a pull request body.

## Find the existing location

Decide the scope first, then the file within that scope. Search before creating
a file. Use the first match:

1. An existing glossary for that scope, under any case: `glossary.md`,
   `Glossary.md`, `GLOSSARY.md`, or a glossary section inside an existing
   domain record.
2. The project's documentation directory, such as `docs/`, `Documentation/`,
   `doc/`, or a published documentation site source. Prefer `docs/glossary.md`
   when the project has no contrary convention.
3. The repository root, as `GLOSSARY.md`, when no documentation location
   exists. Code with only docstrings and no documentation tree is the normal
   case for this.

Never write to generated output. When a documentation directory holds generated
files, use the source that produces them.

Match the surrounding file-naming case rather than imposing one. Use
`GLOSSARY.md` beside `README.md` and `CONTRIBUTING.md`; use `glossary.md`
beside `architecture.md` and `user-journeys.md`. With no comparable neighbors,
use `glossary.md` in a documentation directory and `GLOSSARY.md` at the root.

## Choose the scope

One glossary per bounded context, not per package. A separate documentation
folder does not by itself prove a separate language. In a monorepo, a separate
glossary belongs to a subproject that owns its own language, for example
`infra/network/docs/glossary.md` and `app/billing/docs/glossary.md`. Keep a
single shared glossary when the same terms mean the same thing across the
repository, and link to it from a subproject rather than copying entries.

## Ask when the location is unclear

Ask the user when several locations are plausible, the project mixes
conventions, or a term could belong to either a shared or a subproject
glossary. State the option you would choose and why. A user may decline a
glossary; record that decision in the project's agent or contributor
instructions so later work does not ask again. Discourage that outcome, and
keep terms anchored to identifiers in code.

## Write the entry

Keep entries short. Each one needs the term, its context, the identifier that
anchors it in code, and the contrast with the term it is confused with.

```markdown
### Ingest run (Ingestion)

One execution of a source pull, identified by `IngestRun.id`. An ingest run
processes new records only. A backfill replays records that an earlier run
already processed.

- **Discouraged**: `sync`, `import job`.
- **Exact identifiers**: `IngestRun`; `IngestRunId`; `ingest.run.started`.
```

Record abbreviations, acronyms, initialisms, and synonyms in the same file.
They cause the same failure as an undefined domain term, and an agent cannot
guess which expansion a project means.

```markdown
- **AI** *(ambiguous)*: Artificial intelligence or Application Insights. Write
  the intended term in full.
- **`azp`**: Authorized party. Access-token claim that identifies the client
  application that requested the token.
```

Name the preferred term when a project uses several words for one concept, and
list the discouraged alternatives with it. A synonym entry that only records
usage without choosing one term does not settle anything.

Add or revise an entry in the change that introduces or redefines the term.
Link the entry from change artifacts and pull requests instead of restating the
definition. Remove an entry when its term leaves the code.

## Split it only when it grows

One file is enough for most projects. When it becomes hard to scan, split by
kind or by feature, and keep the glossary as the entry point that links the
others, for example `ubiquitous-language.md`, `acronyms.md`, or a section per
feature. This is a judgement call; a link costs nothing, while a term recorded
in two files drifts.
