---
id: EW-RM-006
title: Open-Source Enforcement Plane v0.5 Roadmap
status: proposed
owner: Platform Owner and Security Authority
version: 0.5.0-rc.1
last-reviewed: 2026-07-24
---

# Open-Source Enforcement Plane v0.5 Roadmap

## Slice 1 — Active policy gate

- lock OPA version and platform digests;
- verify binary before execution;
- format and unit-test Rego;
- evaluate canonical repository records;
- preserve the independent native validator;
- close `GAP-007` only after the blocking workflow passes.

## Slice 2 — Repository security observer

- run immutable OpenSSF Scorecard action;
- publish authenticated results;
- triage findings into owned gaps;
- configure branch protection and non-author review;
- never translate Scorecard's aggregate number directly into readiness score.

## Slice 3 — Supply-chain evidence

- activate Syft with signed checksum verification;
- emit CycloneDX 1.7 and SPDX output;
- activate Grype with pinned database policy and OpenVEX support;
- generate artifact and configuration digests;
- retain structured evidence.

## Slice 4 — Provenance and signing

- produce SLSA provenance for a real release artifact;
- sign artifact and attestation through Sigstore/Cosign;
- verify signer identity, issuer, subject digest and bundle;
- rehearse offline verification and keyless-service outage handling.

## Slice 5 — Portable native developer path

- expose controls through `ej doctor`, `ej check`, `ej evidence` and `ej release`;
- keep adapters replaceable;
- measure gate duration, false positives, rework and remediation latency;
- remove tools whose value does not exceed their operational cost.
