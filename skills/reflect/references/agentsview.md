# AgentsView session-history option

AgentsView is an optional read-only source for recorded agent sessions. It is not required by this skill and might not contain the currently active session.

## Capability check

Check for the CLI before using it:

```bash
command -v agentsview
```

If it is absent, do not install it, do not ask the user to install it, and do not treat its absence as an error. Return to the native harness method or the digest fallback.

## Find a session

Use FTS for an exact opening prompt, path, error, or tool name. Use hybrid search for a conceptual request or a user-selected historical session.

```bash
agentsview session search "<opening prompt or exact phrase>" --fts --since 1d --context 2 --json --limit 8
agentsview session search "<concept query>" --hybrid --context 2 --json --limit 8
```

Inspect the result metadata and surrounding context. Require the project or working-directory evidence and opening request to match the intended session. A search hit is only a lead.

Deep-read only the strongest matching session:

```bash
agentsview session messages <session-id> --around <ordinal> --before 20 --after 20 --role user,assistant --json
```

Expand the window only when needed to cover the material task. Convert the verified messages into the digest consumed by the reviewer templates. Do not pass search snippets as if they were the full transcript.

If a hit is marked `subordinate`, confirm it against `parent_session_id` before treating it as the user's decision or instruction. If the active session is not indexed, stop searching and use the current-context digest.
