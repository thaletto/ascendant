# Domain docs

This is a single-context repository.

## Before exploring

- Read `CONTEXT.md` at the repository root when it exists.
- Read relevant architectural decisions under `.docs/adr/`.
- If either location does not yet exist, proceed without creating it upfront.
  Domain-modeling and architecture workflows create records lazily when terms
  or decisions are resolved.

## Vocabulary

Use domain concepts as named in `CONTEXT.md`. Avoid drifting to synonyms that
the glossary rejects. When a needed concept is absent, reconsider whether it
belongs in the model or record the gap for domain-modeling.

## Architectural decisions

If proposed work contradicts an existing ADR, surface the conflict explicitly
instead of silently overriding the recorded decision.
