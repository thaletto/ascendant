# Issue tracker: Linear

Issues and specs for this repository live in Linear. Use the Linear integration for all issue operations and associate work with the Ascendant project.

## Conventions

- Create one Linear issue per spec or ticket.
- Read the complete issue body, comments, labels, and relationships before acting.
- Use Linear comments for progress and completion notes.
- Apply and remove labels in Linear.
- Close issues only when their acceptance criteria are satisfied.
- Do not treat pull requests as incoming triage requests.

## When a skill says "publish to the issue tracker"

Create a Linear issue in the Ascendant project.

## When a skill says "fetch the relevant ticket"

Fetch the Linear issue, including its comments, labels, and relationships.

## Dependencies

Use Linear's native issue relationships for blocking dependencies. Create issues in dependency order so each blocker can be referenced by its issue identifier.

If native dependencies are unavailable, add a `Blocked by` section to the issue body.

## Wayfinding operations

Used by `/wayfinder`. The map is one Linear issue with related child issues as tickets.

- **Map:** A Linear issue containing the Notes, Decisions-so-far, and Fog sections.
- **Child ticket:** A related Linear issue labelled by type: `wayfinder:research`, `wayfinder:prototype`, `wayfinder:grilling`, or `wayfinder:task`.
- **Blocking:** Use Linear's native blocking relationships.
- **Frontier:** Select the first open, unassigned child whose blockers are all resolved.
- **Claim:** Assign the issue to the working developer before starting.
- **Resolve:** Add the answer or completion note, close the child issue, and add a context pointer to the map's Decisions-so-far section.
