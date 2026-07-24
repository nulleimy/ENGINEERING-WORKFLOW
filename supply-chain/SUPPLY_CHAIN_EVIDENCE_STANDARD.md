---
id: EW-SUP-002
title: Supply-Chain Evidence Standard
status: proposed
owner: Platform Owner and Security Authority
version: 0.6.0-rc.1
last-reviewed: 2026-07-24
---

# Supply-Chain Evidence Standard

## Purpose

This standard defines the minimum evidence required to prove what source was evaluated, which software components were discovered, which vulnerabilities were reported, which policy threshold was enforced, and which exact tools produced the result.

## Required flow

```text
Canonical checkout
→ deterministic source artifact
→ Syft native SBOM
→ CycloneDX SBOM
→ SPDX SBOM
→ Grype vulnerability evaluation
→ evidence manifest
→ blocking decision
```

## Invariants

1. Tools are executed only after version and artifact-integrity verification.
2. The source artifact is deterministic for identical repository contents.
3. The native Syft JSON SBOM is retained as the highest-fidelity machine record.
4. CycloneDX and SPDX outputs are generated in the same scan for interoperability.
5. Vulnerability evaluation consumes the generated SBOM, not an unrelated rescan.
6. `HIGH` and `CRITICAL` findings block acceptance unless a versioned VEX or governed exception applies.
7. A tool failure, database failure, malformed output or missing evidence is never converted into success.
8. Evidence records identify baseline, workflow run, tool versions, hashes, policy and result.
9. Evidence generation does not itself prove SLSA provenance or artifact signing.
10. Signing and provenance are introduced through a separate independently reviewed change.

## Evidence bundle

```text
.evidence/
├── source.tar.gz
├── source-manifest.json
├── sbom.syft.json
├── sbom.cyclonedx.json
├── sbom.spdx.json
├── vulnerabilities.json
├── grype-db-status.json
├── scan-status.json
├── evidence-manifest.json
└── SHA256SUMS
```

## Result semantics

- `PASSED`: scan completed and no finding met or exceeded the blocking threshold.
- `CONTROL_FAILED`: scan completed and at least one finding met or exceeded the threshold.
- `TOOL_FAILED`: a tool, database, parser or evidence step did not complete correctly.
- `BLOCKED`: tool integrity, source identity or required authority could not be established.

## Vulnerability exceptions

A finding may be suppressed only by:

- a valid VEX statement bound to the affected component and vulnerability; or
- a governed exception containing owner, scope, reason, compensating controls, expiry and remediation work.

Ad-hoc ignore lists and undocumented severity downgrades are prohibited.

## Retention

Pull-request evidence is retained for at least 30 days. Release evidence follows the release lifetime plus the retention period required by the applicable assurance profile.
