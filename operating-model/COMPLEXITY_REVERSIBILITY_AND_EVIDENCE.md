---
id: EW-OPERATING-INVARIANT-001
title: Complexity, Reversibility and Lifecycle Evidence Standard
status: proposed
owner: Eimy Herrer and Johny
version: 0.7.0-rc.2
last-reviewed: 2026-07-26
---

# Complexity, Reversibility and Lifecycle Evidence Standard

## Purpose

This standard operationalizes Article 0 without turning the system into document-heavy bureaucracy.

## Complexity budget

Every R1-R3 change records the expected delta in runtime services, direct dependencies, trust boundaries, external data flows, manual steps, persistent state stores and monthly maintenance effort. A zero-value dimension may remain implicit only for R0 work.

Exceeding the configured budget requires a Decision Record, owner, measured benefit, security review, exit plan and review trigger. Adding a runtime service, trust boundary, external data flow or persistent state automatically escalates review.

## Reversibility

Every change uses exactly one class from `REV-0` through `REV-4`. Missing classification is `BLOCKED`. `REV-3` and `REV-4` require R3 handling, independent acceptance and explicit operator authorization before the protected operation.

## Manual work

Repeated manual work is visible debt, not a hidden runbook detail. A step performed more than twice in 30 days or taking at least 15 minutes becomes an automation candidate unless a documented safety reason makes manual control preferable.

Automation is complete only after the automated path is verified and the obsolete manual path is retired or explicitly retained as an emergency fallback.

## Lifecycle evidence graph

The graph links product problem, decision, Work Package, change, verification, review, acceptance, release, deployment, telemetry, incidents and learning. Git commits may be evidence references but are not the complete lifecycle record.

Release, deployment and incident nodes may not be orphaned. Every node has a stable identity, owner, status, timestamp, evidence reference and integrity digest.
