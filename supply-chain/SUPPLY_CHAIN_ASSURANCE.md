---
id: EW-SUP-001
title: Software Supply-Chain Assurance Standard
status: proposed
owner: Security and Release Authorities
version: 0.6.0-rc.1
last-reviewed: 2026-07-24
---

# Software Supply-Chain Assurance Standard

## Purpose

Every distributed artifact must be attributable to an exact source state, built through a controlled process, accompanied by a machine-readable SBOM, evaluated for known vulnerabilities, integrity-protected and independently verifiable.

## Mandatory flow

```text
SOURCE
→ DETERMINISTIC PACKAGE
→ SHA-256 MANIFEST
→ CYCLONEDX SBOM
→ VULNERABILITY POLICY
→ EVIDENCE RECORD
→ PROVENANCE ATTESTATION
→ KEYLESS SIGNATURE
→ INDEPENDENT VERIFICATION
```

## Trust boundaries

- Pull requests may build, inventory and scan artifacts but receive no signing or attestation authority.
- Only `main`, protected release branches or immutable tags may request OIDC signing credentials.
- Workflow actions use immutable full commit SHAs.
- Tool versions are explicit; floating `latest`, branch or major-tag execution is prohibited.
- External-tool success never replaces repository-native validation.
- A missing tool, database or evidence file produces `BLOCKED` or `FAILED`, never silent success.

## SBOM

CycloneDX JSON is the canonical operational SBOM. SPDX remains an interoperability target. The SBOM must identify the scanned subject, generator and component relationships and must be retained with the artifact.

## Vulnerability policy

- `critical` and `high` findings block the pipeline.
- `unknown` severity blocks until triaged.
- Unfixed findings are not ignored merely because no fix exists.
- A VEX statement may affect disposition only when it identifies the exact product/artifact, vulnerability, status, justification, owner, evidence, creation time and expiry/review trigger.
- AI-generated VEX is advisory until independently accepted.

## Provenance and signing

Release-capable runs create a signed SLSA-compatible build provenance attestation and an SBOM attestation using short-lived OIDC identity. The artifact also receives a Sigstore bundle through Cosign. Verification must bind the certificate identity to this repository and the controlled workflow path.

## Evidence

The retained bundle includes:

- artifact and SHA-256 manifest;
- CycloneDX SBOM;
- vulnerability report and policy result;
- build/source identity;
- provenance and SBOM attestations when authorized;
- Cosign bundle and verification result when authorized;
- tool versions and immutable action references.

## Claims

Pipeline execution proves only the recorded scope. It does not by itself establish an overall SLSA level, certification or 9/10 readiness score. Such claims require the separate assurance and readiness acceptance process.
