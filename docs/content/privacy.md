---
title: Privacy
description: How Ascendant handles hosted chart records and MCP requests.
---

## What Ascendant stores

When you use the hosted Ascendant connection, the service stores only the data
needed to provide the chart-record workflow:

- your OAuth account identifier;
- a display label and the birth details submitted for each hosted person record;
- your consent attestation that you are permitted to store and analyse those
  details;
- derived chart, timing, provenance, and evidence revisions; and
- tool-level Reading requests: selected record, topic, question, requested
  moment, evidence revision, and timestamp.

Ascendant does not store your complete ChatGPT conversation, ChatGPT's final
prose response, or a generic activity transcript.

## Access and consent

Hosted records are scoped to the OAuth account whose token created them. A
record is never shared with another account through a label or identifier.

You may create a record for another person only when you attest that you are
permitted to store and analyse the submitted birth details. That attestation is
your statement; it is not an identity check or proof of the other person's
consent.

## Deletion and retention

You can delete one hosted person record or use the account-data deletion tool
to remove every hosted record and its related evidence, consent attestation,
and Reading requests. Live service data is deleted immediately. Residual
encrypted database-backup copies are retained for no more than 30 days before
expiry and are not restored into the live service except for disaster recovery.

## Where the service operates

Ascendant is initially operated for users in India. The service uses Neon
PostgreSQL for hosted application data and a separately selected OAuth provider
for account identity. Their current operational regions and terms apply to the
infrastructure they provide.

## Questions and requests

For privacy questions or deletion support, open an issue in the
[Ascendant repository](https://github.com/thaletto/ascendant/issues).
