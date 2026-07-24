---
id: EW-DOC-002
title: Document Metadata Standard
status: proposed
owner: Eimy Herrer and Johny
version: 0.1.0
last-reviewed: 2026-07-24
---

# Document Metadata Standard

Controlled Markdown documents use front matter:

```yaml
---
id: EW-DOC-000
title: Human-readable title
status: draft | proposed | current | deprecated | archived | superseded
owner: person or role
version: 1.0.0
last-reviewed: YYYY-MM-DD
supersedes: optional-id
---
```

## Identity

`id` is stable across filename moves. A new document that replaces an old one names the superseded ID.

## Versioning

- patch: clarification with no control impact;
- minor: backward-compatible new guidance or template capability;
- major: changed obligation, record shape or migration requirement.

## Review triggers

Review occurs on material system change, incident finding, compliance change, owner change, deprecation or scheduled freshness check.
