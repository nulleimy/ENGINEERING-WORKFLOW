---
id: EW-GOV-004
title: Document Control Standard
status: proposed
owner: Eimy Herrer and Johny
version: 0.1.0
last-reviewed: 2026-07-24
---

# Document Control Standard

Controlled documents must declare identity, title, status, owner, version and review date.

## Status values

- `draft`: incomplete working material;
- `proposed`: ready for review, not authoritative;
- `current`: approved and authoritative;
- `deprecated`: still readable, replacement identified;
- `archived`: preserved, no longer operational;
- `superseded`: replaced by a named document or version.

## Rules

- One fact has one canonical home.
- README files navigate; they do not duplicate entire standards.
- Proposed capability is not documented as available.
- Generated reference is not manually duplicated.
- Significant code or operational changes update affected documentation in the same change set.
- Controlled documents receive periodic or event-driven review.
- Archived records are immutable except for metadata correction with audit trail.
