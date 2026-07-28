---
name: parashari-judgement
description: Use for a cited, deterministic Vedic astrology reading from a saved personal chart.
license: MIT
---

# Cited Parashari judgement

Use this shared workflow for every interpretation of a saved chart.

1. Require one explicit saved name. For a comparison, require two explicit
   saved names. For a family reading, require `mother`, `father`, `sibling`,
   `child`, or `household`.
   **Complete when:** every requested record is an exact `persons/<name>`
   directory name.
2. Resolve the requested date. Use the supplied ISO 8601 moment with timezone;
   when absent, use the current UTC moment and retain the resolved timestamp.
   **Complete when:** the exact `as_of` moment is known.
3. Run the evaluator from the user's project directory.

   ```bash
   python3 <path-to-parashari-judgement-skill>/scripts/evaluate-reading.py \
     --name "<name>" --topic "<topic>" --date "<ISO-8601 date>"
   ```

   Add `--other-name "<name>"` for `relationship-compatibility`; add
   `--family-role "<role>"` for `family`.
   **Complete when:** the command exits successfully and returns its evidence
   ledger.
4. Render the ledger in its order: status, evidence, practical guidance, then
   sources. Copy the citations supplied for every factual or interpretive
   sentence exactly as emitted. Add only a direct restatement of a cited ledger
   item, retaining all of its citations.
   **Complete when:** every statement has one or more `[sources: ...]` markers;
   headings and direct questions are the only uncited text.
5. State any missing file, unavailable rule, or `insufficient evidence` result
   exactly as reported. Keep relationship, health, financial, and legal
   guidance within the cited practical boundary.
   **Complete when:** the response makes no claim beyond the ledger.

The evaluator applies the versioned `parashari_raman_v1` rule catalogue. Read
[`references/rule-catalogue.md`](references/rule-catalogue.md) for each rule's
predicate and [`references/sources.md`](references/sources.md) for its sources.
