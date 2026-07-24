---
id: EW-ADR-0001
title: Select OPA and Conftest as the policy-as-code target
status: proposed
owner: Eimy Herrer and Johny
version: 0.2.0-rc.1
last-reviewed: 2026-07-24
---

# ADR-0001: Select OPA and Conftest as the policy-as-code target

## Context

The system needs portable policy evaluation across JSON, YAML, infrastructure and configuration without coupling policy definitions to GitHub.

## Decision

Use Open Policy Agent as the general policy engine and Conftest as the preferred structured-file adapter. Keep the dependency-free Python validator as the bootstrap and fallback layer.

## Constraints

- no runtime dependency until a pinned version and checksum are selected;
- Rego policies require tests and linting;
- policy output maps to stable control IDs;
- the bootstrap validator must work without network access.

## Consequences

A later governed slice will add version-pinned OPA/Conftest adapters and policy tests. This ADR selects the target architecture but does not activate either tool.