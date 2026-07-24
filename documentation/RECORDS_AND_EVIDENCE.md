---
id: EW-DOC-004
title: Records and Evidence Standard
status: proposed
owner: Eimy Herrer and Johny
version: 0.1.0
last-reviewed: 2026-07-24
---

# Records and Evidence Standard

## Portable records

- Project Record;
- Work Package;
- Decision Record;
- Baseline Record;
- Change Set Record;
- Verification Record;
- Release Record;
- Incident and Postmortem Record;
- Handoff Record;
- Exception Record.

## Evidence properties

Evidence is attributable, timestamped, integrity-verifiable, linked to its subject, exportable and retained according to risk and obligation.

## Recommended evidence bundle

```text
EVIDENCE_BUNDLE/
├── manifest.json
├── project-record.json
├── work-package.md
├── baseline.json
├── change-set.json
├── verification/
├── review/
├── release/
└── SHA256SUMS
```

## Storage

Git, CI artifacts, Drive, object storage and GOVERDOCS may store evidence. No single UI may be the only copy of critical long-term evidence. Closed evidence is immutable; corrections are additive and traceable.
