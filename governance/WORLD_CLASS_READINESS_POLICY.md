---
id: EW-GOV-READINESS-001
title: World-Class Readiness Policy
status: proposed
owner: Eimy Herrer and Johny
version: 0.4.0-rc.1
last-reviewed: 2026-07-24
---

# World-Class Readiness Policy

## Purpose

ENGINEERING-WORKFLOW shall not describe a project, domain, release, service or engineering capability as `WORLD_CLASS_READY` unless every applicable domain has an evidence-backed score of at least **9.0 out of 10**.

The threshold is a release invariant, not a marketing target.

## Non-negotiable rules

1. Every applicable domain has a target score of at least `9.0`.
2. Critical domains cannot be hidden by a high overall average.
3. Unknown or not-measured domains block world-class readiness.
4. A lower project profile cannot be selected to avoid a readiness requirement.
5. Scores must be supported by referenced evidence.
6. Documentation or design alone cannot prove operational readiness.
7. A failed, expired or missing critical control blocks readiness regardless of score.
8. A project may be useful, releasable or experimental below 9.0, but it must be labelled honestly.
9. Exceptions cannot authorize the `WORLD_CLASS_READY` claim below the threshold.
10. Certification claims remain prohibited without an authorized external certification.

## Evidence maturity score caps

| Evidence maturity | Maximum permitted score |
|---|---:|
| `UNKNOWN` | no score |
| `DESIGNED` | 5.0 |
| `IMPLEMENTED` | 7.0 |
| `VERIFIED` | 8.5 |
| `MEASURED` | 9.5 |
| `INDEPENDENTLY_REVIEWED` | 10.0 |

A score may be lower than the cap. It may never exceed the cap.

## Readiness states

- `UNASSESSED` — an assessment has not been completed;
- `GAP_CLOSURE` — baseline exists and gaps are being closed;
- `CANDIDATE` — every applicable domain is at least 9.0, but final independent acceptance is incomplete;
- `WORLD_CLASS_READY` — every applicable domain is at least 9.0, critical controls are verified, evidence is current and acceptance is recorded;
- `DEGRADED` — a previously ready system no longer meets the invariant;
- `RETIRED` — no longer operated or maintained.

## Critical domains

At minimum, security, supply chain, release, operations/SRE, compliance, incident management and AI engineering are critical whenever applicable. A project profile may add critical domains but may not remove an applicable critical domain.

## Scoring authority

The domain owner prepares the evidence. A separate acceptance authority approves a score of 9.0 or higher. A5 systems require independent review for every applicable critical domain.

## Reassessment triggers

Reassessment is required after a major architecture change, critical incident, material dependency or provider change, change of data classification, new regulatory obligation, failed recovery exercise, expired evidence, or significant deployment-model change.
