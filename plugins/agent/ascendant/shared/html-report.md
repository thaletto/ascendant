# HTML report mode

Execute every step below only when the user's invocation contains the exact
`--html` flag.

1. Complete the same direct-artifact reading and hierarchy application used
   for Markdown. HTML changes presentation only.
2. Build one complete, single-file HTML5 document from the selective natural
   reading. Keep each material claim beside its evidence and method citation.
   Escape every saved-artifact value before inserting it into HTML.
3. Include a descriptive `<title>`, UTF-8 charset, responsive viewport,
   semantic landmarks, keyboard-readable content, useful print styles, and a
   restrictive Content Security Policy. Permit scripts only from the required
   CDN hosts; block forms, objects, frames, and network connections.
4. Load Tailwind from `https://cdn.tailwindcss.com` for layout, spacing,
   typography, color, and responsive behavior. Keep hand-crafted CSS in the
   same document.
5. Load Mermaid from
   `https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs` only when
   a graph, dependency, sequence, or flow communicates cited relationships
   more clearly than prose. Put the same citations in a visible caption.
6. Use hand-built HTML, CSS, or inline SVG for editorial visuals. Inline SVG
   must have an accessible name and description. Color may reinforce a written
   label but never carry meaning alone.
7. When the evidence supports a dated comparison, show `Before` for the natal
   state and `After` for dasha or transit activation. If either state is
   absent, show `Insufficient evidence`; never invent a comparison.
8. Resolve the output directory outside the repository: use `$TMPDIR` with
   `/tmp` fallback on macOS and Linux, or `%TEMP%` on Windows. Resolve it to an
   absolute path.
9. Sanitize the saved person's recognizable name for the current filesystem.
   Add a UTC timestamp with date, time, and fractional seconds. Write exactly
   one new `<NAME>-report-<timestamp>.html` file without overwriting an earlier
   report.
10. Open the file with `xdg-open` on Linux, `open` on macOS, or `start` on
    Windows. Quote the absolute path for the active shell.
11. Return the absolute path. If opening fails, retain the file, report the
    opener error, and still provide the path. Do not paste the document into
    chat.

The HTML file is temporary output. It must never be staged, committed, copied
into the repository, or treated as a durable person record.
