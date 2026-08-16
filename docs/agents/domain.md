# Domain Docs

How the engineering skills should consume this repository's domain documentation when exploring the codebase.

## Before exploring, read these

- **`CONTEXT.md`** at the repository root before naming domain concepts.
- **`docs/adr/`** before proposing or implementing an architecture change; read
  the ADRs that affect the area about to be changed.

When either location is absent, continue the current workflow. Create a
`CONTEXT.md` only when domain-modeling resolves a term, and create an ADR only
when an architecture decision meets the ADR criteria.

## File structure

This is a single-context repository:

```
/
├── CONTEXT.md
├── src/
│   └── ascendant/
├── docs/
│   └── agents/
└── tests/
```

## Use the glossary's vocabulary

When output names a domain concept—in an issue title, refactor proposal, hypothesis, or test—use the term defined in `CONTEXT.md`. Do not drift to synonyms the glossary explicitly avoids.

If a needed concept is absent, reconsider whether it belongs in the model or note the gap for domain modeling.

## Flag ADR conflicts

If proposed work contradicts an existing ADR, surface the conflict explicitly instead of silently overriding it.
