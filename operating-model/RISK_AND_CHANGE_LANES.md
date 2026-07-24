---
id: EW-OPS-002
title: Risk Classification and Change Lanes
status: proposed
owner: Eimy Herrer and Johny
version: 0.1.0
last-reviewed: 2026-07-24
---

# Risk Classification and Change Lanes

## Risk classes

| Class | Typical examples | Required lane |
|---|---|---|
| R0 | typo, link, metadata-only correction | Fast |
| R1 | isolated bug fix, small feature, internal refactor | Fast |
| R2 | public API, contract, dependency, data model, integration | Governed |
| R3 | auth, secrets, production data, infrastructure, irreversible migration, legal/compliance boundary | Critical |

## Fast lane

```text
FRAME → BUILD → FAST GATE → ACCEPT → CLOSE
```

Required: defined result, bounded scope, automated fast checks, known recovery and honest status.

## Governed lane

```text
FRAME → DESIGN → AUTHORIZE → BUILD → FULL GATE → INDEPENDENT REVIEW → ACCEPT → RELEASE/EVIDENCE
```

Required: baseline, work package, architecture/security impact, full relevant tests, documentation and rollback.

## Critical lane

Adds threat model, two-person approval, backup/recovery rehearsal, progressive or isolated deployment, explicit residual-risk acceptance and incident readiness.

## Risk escalation triggers

Escalate when a change touches identity, authorization, sensitive data, external contracts, persistence, production infrastructure, destructive actions, regulatory obligations or broad dependency updates.
