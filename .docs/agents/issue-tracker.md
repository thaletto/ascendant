# Issue tracker: GitHub

Issues and PRDs for this repository live as GitHub issues. Use the `gh` CLI
for issue operations and infer the repository from the current Git remote.

## Conventions

- Create one GitHub issue per spec or ticket.
- Read the complete issue body, comments, and labels before acting on it.
- Apply or remove labels with `gh issue edit`.
- Close issues only when their acceptance criteria are satisfied.
- Do not treat pull requests as incoming requests for triage.

## Publishing

When a skill says to publish to the issue tracker, create a GitHub issue.
When a skill says to fetch a ticket, read the GitHub issue and its comments.

## Dependencies

Prefer GitHub's native issue dependencies for blocking relationships. Create
issues in dependency order so each blocker can be referenced by its issue
number. If native dependencies are unavailable, record a `Blocked by` section
in each issue body.
