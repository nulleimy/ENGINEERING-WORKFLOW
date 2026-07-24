---
id: EW-GOV-002
title: Governance Model
status: proposed
owner: Eimy Herrer and Johny
version: 0.1.0
last-reviewed: 2026-07-24
---

# Governance Model

## Governance layers

| Layer | Purpose | Change authority |
|---|---|---|
| Constitution | Non-negotiable invariants | Joint approval |
| Standards | Required outcomes and controls | Standard owner + reviewer |
| Procedures | Repeatable implementation steps | Procedure owner |
| Templates | Consistent records and handoffs | Maintainer |
| Adapters | Tool-specific automation | Technical owner |
| Evidence | Proof of execution and acceptance | Immutable after closure |

## Roles

- **Product Steward:** protects user value, product boundary and priority.
- **Technical Steward:** protects architecture, maintainability and engineering integrity.
- **Security Authority:** can block unacceptable security or privacy risk.
- **Change Owner:** accountable for one work package.
- **Independent Reviewer:** challenges correctness, scope, safety and evidence.
- **Release Authority:** authorizes an identified release.
- **Operator:** owns operational readiness and recovery.
- **Document Owner:** keeps a controlled document current.

One person may hold several roles, but R2/R3 work preserves independent acceptance where required.

## Decision rule

Decisions are ordered by:

1. safety and legal constraints;
2. verified evidence;
3. product outcome;
4. simplicity and reversibility;
5. reliability and operability;
6. cost of ownership;
7. preference.

## Exceptions

An exception must identify the control being bypassed, reason, owner, risk, compensating control, expiry and remediation work item. Permanent undocumented exceptions are prohibited.
