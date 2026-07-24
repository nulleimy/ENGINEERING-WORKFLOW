---
id: EW-OPS-003
title: Quality Gate Standard
status: proposed
owner: Eimy Herrer and Johny
version: 0.1.0
last-reviewed: 2026-07-24
---

# Quality Gate Standard

## Gate design

A gate must be deterministic where possible, fast enough for its position in the flow, and produce evidence with clear failure semantics.

### Fast gate

Target feedback: minutes.

- format and lint;
- targeted type/schema checks;
- targeted unit/regression tests;
- documentation metadata and link validation;
- obvious secret and unsafe-file checks.

### Integration gate

- complete relevant test suite;
- contract and integration tests;
- build/package verification;
- dependency and license review;
- documentation drift checks;
- compatibility assessment.

### Release gate

- immutable version and artifact identity;
- smoke test in release-like environment;
- vulnerability and supply-chain checks;
- release notes and migration information;
- provenance/SBOM target according to project risk;
- rollback or safe-forward verification;
- operational readiness approval.

### Critical gate

- threat-model review;
- backup and recovery rehearsal;
- migration rehearsal where relevant;
- explicit two-person approval;
- progressive delivery or controlled maintenance window;
- verified incident rollback path.

## Test strategy

Static checks → unit → contract → integration → end-to-end → smoke → production health. Every defect fix should add a regression test when practical.

## Evidence

Record commands or methods, environment, exit status, passed/failed/skipped checks, output reference, limitations and executor identity.
