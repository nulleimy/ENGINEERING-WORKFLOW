---
id: EW-RM-006
title: Supply-Chain Assurance v0.6 Closure Plan
status: proposed
owner: Security and Release Authorities
version: 0.6.0-rc.1
last-reviewed: 2026-07-24
---

# Supply-Chain Assurance v0.6 Closure Plan

## Implemented slice

1. deterministic source packaging;
2. SHA-256 artifact manifest;
3. CycloneDX SBOM generation;
4. Grype high/critical vulnerability blocking;
5. native unknown-severity blocking and report validation;
6. portable evidence bundle;
7. main/tag-only OIDC build and SBOM attestations;
8. Cosign keyless signing and repository-workflow identity verification.

## Closure sequence

- PR `quality` gate succeeds;
- PR `policy` gate succeeds;
- PR `supply-chain` build-and-scan gate succeeds;
- independent review accepts policy, action pins and trust boundaries;
- merge is explicitly authorized;
- `main` supply-chain run creates attestations and signature;
- verification output and evidence bundle are retained;
- only then may GAP-009 and related readiness scores be reassessed.

## Non-goals

- no unsupported SLSA-level claim;
- no certification claim;
- no automatic world-class score increase;
- no PR signing authority;
- no automatic vulnerability exception;
- no AI acceptance authority.
