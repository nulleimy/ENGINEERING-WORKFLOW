---
id: EW-OPS-006
title: Release and Deployment Standard
status: proposed
owner: Eimy Herrer and Johny
version: 0.1.0
last-reviewed: 2026-07-24
---

# Release and Deployment Standard

## Release properties

Every release is identifiable, attributable, reproducible to an appropriate degree, verified, documented and recoverable.

## Required release record

- project and version;
- source/baseline identity;
- included change sets;
- build environment and method;
- artifact identities and hashes;
- verification evidence;
- approvals;
- compatibility and migration notes;
- rollback or safe-forward target;
- release and support status.

## Deployment strategies

Choose according to risk: direct controlled deployment, rolling, blue/green, canary, feature flag, shadow, isolated pilot or offline package delivery.

## Automatic deployment

Automation must enforce environment separation, least privilege, immutable inputs, approval requirements, health verification and rollback triggers. Production credentials must not be shared with development jobs.

## Progressive delivery

R2/R3 changes should reduce blast radius using staged exposure, health thresholds and automatic stop conditions.

## Failed deployment

Stop propagation, preserve evidence, restore service, communicate status, reconcile canonical state and create corrective work. Never silently patch production without recording the resulting state.
