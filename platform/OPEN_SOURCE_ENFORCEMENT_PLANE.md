---
id: EW-PLAT-001
title: Open-Source Enforcement Plane
status: proposed
owner: Platform Owner and Security Authority
version: 0.5.0-rc.1
last-reviewed: 2026-07-24
---

# Open-Source Enforcement Plane

## Purpose

The Open-Source Enforcement Plane converts engineering standards into executable, portable and evidence-producing controls without making the operating model dependent on one vendor, cloud, source-control product or AI provider.

## Architecture

```text
Portable records and native validators
                ↓
Verified open-source adapters
                ↓
Blocking policy and supply-chain gates
                ↓
Evidence bundle and readiness scorecard
```

### Layer 1 — Repository-native core

Dependency-free Python validators and open JSON/Markdown records remain the bootstrap source of truth. They must work offline and must not be bypassed when an external tool is unavailable.

### Layer 2 — Verified open-source adapters

External tools are accepted only when they have:

- a clear open-source license;
- an active security policy and maintained release process;
- a pinned version or immutable commit;
- checksum, signature, provenance or equivalent integrity verification;
- least-privilege execution;
- bounded network and filesystem access;
- documented input, output and failure semantics;
- a removal or replacement path;
- no authority to silently weaken a native control.

### Layer 3 — Enforcement workflows

External tools run in isolated jobs. A tool failure is classified as:

- `CONTROL_FAILED` when the tool found a policy or security violation;
- `TOOL_FAILED` when the tool itself failed;
- `BLOCKED` when integrity, availability or trust cannot be established.

None of these states may be silently converted into success.

### Layer 4 — Evidence

Tool output must be connected to a project, baseline, change, environment, tool identity and configuration digest. Raw logs alone are insufficient when structured output exists.

## Active foundation

### Open Policy Agent

OPA is the active policy-as-code engine for repository and engineering control decisions. The first policy pack validates the world-class readiness invariant against the same machine-readable scorecard used by the native Python validator.

Activation requirements:

- exact release version;
- platform-specific SHA-256 digest;
- download over HTTPS;
- local digest verification before execution;
- `opa fmt --fail` and `opa test` in CI;
- native Python validation remains a separate implementation.

### OpenSSF Scorecard

OpenSSF Scorecard is the selected independent repository-security observer. It is not the authority for readiness and cannot replace project-specific security review. The action is pinned to an immutable commit and runs with least privilege.

Initial mode:

- scheduled and manual execution;
- SARIF output for security findings;
- no automatic project-readiness score change;
- findings become owned gaps or exceptions through the normal governance process.

## Selected next adapters

| Capability | Selected project | Initial state |
|---|---|---|
| Structured configuration testing | Conftest | selected, not active |
| SBOM generation | Syft | selected, not active |
| Vulnerability and VEX evaluation | Grype | selected, not active |
| Artifact and attestation signing | Cosign / Sigstore | selected, not active |
| Dependency update automation | Renovate | configured, not activated |
| Provenance generation | SLSA GitHub Generator or equivalent portable builder | evaluation |
| Telemetry | OpenTelemetry | evaluation |

## Explicitly deferred

Backstage is not introduced until multiple projects have stable golden paths and a measured developer-portal need. A platform must remove demonstrated cognitive load; it must not create a service that exists only to manage the process itself.

## Supply-chain rules

- No `curl | sh` execution.
- No unpinned GitHub Action reference.
- No floating container tag in an enforcement or release path.
- No binary execution before integrity verification.
- No automated remediation without a reviewable change set.
- No vulnerability suppression without a versioned exception or VEX decision.
- No release signing key stored in a repository secret when workload identity or an approved external key service is available.

## AI-native operation

AI may explain findings, propose policy changes, correlate evidence and prepare remediation work packages. AI must not:

- suppress a finding;
- approve its own change;
- change a policy threshold;
- mint a compliance or readiness claim;
- receive signing authority;
- use external network access outside its explicit task boundary.

## Success criteria

The enforcement plane is successful when it measurably reduces manual review, escaped control failures and remediation time while maintaining deterministic, independently reviewable results.
