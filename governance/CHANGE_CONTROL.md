---
id: EW-GOV-003
title: Change Control Standard
status: proposed
owner: Eimy Herrer and Johny
version: 0.1.0
last-reviewed: 2026-07-24
---

# Change Control Standard

## Required objects

A governed change connects:

```text
Project Record → Work Package → Baseline → Change Set → Verification → Acceptance → Release/Evidence
```

## State model

`PROPOSED → AUTHORIZED → IN_PROGRESS → IMPLEMENTED → VERIFIED → ACCEPTED → RELEASED → OPERATING`

Alternative terminal states: `REJECTED`, `BLOCKED`, `FAILED`, `ROLLED_BACK`, `SUPERSEDED`.

## Scope control

A work package declares allowed and prohibited scope. Scope expansion requires an explicit update before implementation continues.

## Baseline control

R2/R3 work cannot begin without an identifiable baseline. A baseline can be a source revision, signed archive, filesystem snapshot with manifest, image, database snapshot or combined system record.

## Acceptance

Acceptance confirms the target outcome and residual risk. It does not merely acknowledge that implementation exists.

## Emergency change

Emergency work may compress design and review timing, but must preserve identity, baseline, evidence, recovery and post-change reconciliation. A post-incident review is mandatory for R3 emergency changes.
