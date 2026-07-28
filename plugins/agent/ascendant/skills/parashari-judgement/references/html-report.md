# HTML report mode

Execute every step below when, and only when, the user's skill invocation
contains the exact `--html` flag.

1. Treat `--html` as an agent presentation flag. Remove it from the evaluator
   command and add `--format json`. Do not change the evaluator or ask it to
   produce HTML.
2. Generate the complete reading from the returned evidence ledger. Preserve
   the ledger order: status, evidence, practical guidance, then sources.
3. Keep every factual or interpretive statement next to its complete
   `[sources: ...]` marker. Escape all ledger values before inserting them into
   HTML. Never insert uncited claims to make the report more dramatic.
4. Build one complete, single-file HTML5 document. It must have a descriptive
   `<title>`, a UTF-8 charset, a responsive viewport, semantic landmarks,
   keyboard-readable content, useful print styles, and a restrictive Content
   Security Policy. Permit scripts only from the two required CDN hosts; block
   forms, objects, frames, and network connections.
5. Load Tailwind from `https://cdn.tailwindcss.com` and use Tailwind utilities
   for the page grid, spacing, typography, color, and responsive layout. Keep
   any hand-crafted CSS inside the same HTML document.
6. Load Mermaid from
   `https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs` only when
   a graph, dependency, sequence, or flow reliably communicates cited
   relationships. Initialize it after the document loads. Put the same
   citations shown by the diagram in its visible caption. Do not invent edges,
   ordering, causation, or chronology.
7. Use hand-built HTML, CSS, or inline SVG for editorial visuals such as
   comparison cards, mass diagrams, cross-sections, or state transitions.
   Inline SVG must have an accessible name and description.
8. Give each candidate or compared person a before/after visualization. Label
   the panels `Before` and `After`, state what the two states mean, and cite
   both. For a single-person reading, use the cited natal state as `Before` and
   the cited dated dasha/transit state as `After`. If either state is absent,
   show `Insufficient evidence` instead of fabricating a visualization.
9. Make the report visual without sacrificing meaning: include a strong
   summary, evidence cards, an explicit visual legend, the before/after
   visualization, practical guidance, and the full source bibliography. Color
   may reinforce a written label but must never carry meaning by itself.
10. Resolve the output directory without writing inside the repository:
    - macOS and Linux: use `$TMPDIR` when it is set and otherwise use `/tmp`.
    - Windows: use `%TEMP%`.
    Resolve the selected directory to an absolute path before writing.
11. Create a filesystem-safe name by replacing path separators, control
    characters, and characters forbidden by the current OS with `-`. Keep the
    saved person's recognizable name. Generate a UTC timestamp containing
    calendar date, time, and fractional seconds. Write exactly one new file at
    `<tmpdir>/<NAME>-report-<timestamp>.html`; never overwrite an earlier
    report.
12. Open the completed file for the user:
    - Linux: `xdg-open <absolute-path>`
    - macOS: `open <absolute-path>`
    - Windows: `start <absolute-path>`
    Quote the path according to the active shell. Opening the file is required
    unless the OS reports that no graphical opener is available.
13. Reply with the absolute path. If opening failed, retain the file, report the
    opener error, and still provide the absolute path. Do not paste the full
    HTML document into the chat.

The HTML file is temporary output and must not be staged, committed, copied
into the repository, or treated as a durable person record.
