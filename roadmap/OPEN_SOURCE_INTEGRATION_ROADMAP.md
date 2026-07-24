---
id: EW-RM-004
title: Open Source Integration Roadmap
status: proposed
owner: Eimy Herrer and Johny
version: 0.2.0-rc.1
last-reviewed: 2026-07-24
---

# Open Source Integration Roadmap

## Foundation

- machine-readable component and control catalogs;
- JSON Schema-compatible records;
- immutable SHA-pinned GitHub Actions;
- Renovate configuration without automatic activation;
- proposed OPA/Conftest and CycloneDX/SPDX decisions.

## Policy and supply-chain pilot

- select pinned OPA, Conftest and Regal versions with checksums;
- add tested Rego controls;
- activate Renovate after ownership and review rules are approved;
- generate CycloneDX SBOM with Syft on a reference project;
- scan artifacts with Trivy or an accepted equivalent.

## Repository hardening

- protect `main` and require quality checks;
- add OpenSSF Scorecard on the default branch;
- choose the repository license and contribution model.

## Release trust

- generate SBOM and provenance;
- sign and verify artifacts with Cosign/Sigstore;
- preserve evidence outside the CI interface.

## Platform scale

Evaluate Backstage only after at least three maintained projects use stable golden paths. Do not build a developer portal before the underlying interfaces are proven.