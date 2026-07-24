---
id: EW-RM-004
title: World-Class 9-of-10 Execution Roadmap
status: proposed
owner: Eimy Herrer and Johny
version: 0.4.0-rc.1
last-reviewed: 2026-07-24
---

# World-Class 9-of-10 Execution Roadmap

## Objective

Raise every applicable engineering domain to an evidence-backed score of at least 9.0 without inflating scores, hiding weak domains behind averages, or replacing delivery with documentation.

## Phase 1 — Authority and repository trust

Close `GAP-001` and `GAP-002`:

- joint governance acceptance;
- Apache-2.0 or another explicitly approved license decision;
- ownership and contribution boundary;
- protected main branch;
- required CI and non-author review;
- CODEOWNERS and least-privilege workflow permissions.

Exit: governance reaches 9+ through independent acceptance and repository enforcement.

## Phase 2 — Security and supply-chain enforcement

Close `GAP-007`, `GAP-008` and `GAP-009`:

- version-pinned OPA/Conftest policy pack;
- policy unit and negative tests;
- secret, dependency and configuration gates;
- CycloneDX SBOM generation;
- SLSA-compatible provenance pilot;
- Cosign signature and verification;
- OpenSSF Scorecard assessment;
- independent threat-led review.

Exit: security and supply-chain domains have measured, blocking controls and independent review.

## Phase 3 — Portable golden paths

Close `GAP-005` and `GAP-010`:

- adapter contract;
- `ej doctor`, `ej new`, `ej adopt`, `ej check`, `ej evidence`, `ej release`, `ej recover`;
- offline bootstrap path;
- Python, Node and local-only reference adapters;
- deterministic integration tests.

Exit: a new project can be created, verified, packaged and recovered through one stable interface.

## Phase 4 — Release and operational proof

Close `GAP-011`, `GAP-012` and `GAP-017`:

- release candidate and promotion process;
- health verification and rollback automation;
- SLO and error-budget records;
- backup and restore rehearsal;
- incident command exercise;
- postmortem and corrective-action verification.

Exit: release, operations and incident domains have realistic rehearsal or production evidence.

## Phase 5 — Product, architecture and quality validation

Close `GAP-003`, `GAP-004` and `GAP-006`:

- real pilot product;
- outcome and user-task evidence;
- independent architecture assessment;
- performance, resilience and negative testing;
- compatibility and migration exercise.

Exit: product and architecture claims are validated by a functioning reference project.

## Phase 6 — AI and compliance assurance

Close `GAP-015` and `GAP-016`:

- executable AI context and permission boundaries;
- model/provider inventory;
- deterministic evaluations and red-team cases;
- human acceptance gates;
- evidence sampling and scoped independent compliance assessment.

Exit: AI and compliance domains exceed 9 with reviewed evidence rather than policy text alone.

## Phase 7 — Measured flow and documentation usability

Close `GAP-013` and `GAP-014`:

- at least three measured delivery cycles;
- DORA outcome baseline;
- rework and review-wait measurement;
- documentation usability test;
- freshness and discoverability review.

Exit: delivery and documentation are measured under real use.

## World-class release gate

The system may enter `CANDIDATE` only when every applicable domain is at least 9.0. It may enter `WORLD_CLASS_READY` only after final independent acceptance, zero open P0 gaps, current evidence and successful full-system recovery/release rehearsal.
