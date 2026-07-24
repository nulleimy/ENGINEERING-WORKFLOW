---
id: EW-ADR-0002
title: Select CycloneDX as the default BOM format
status: proposed
owner: Eimy Herrer and Johny
version: 0.2.0-rc.1
last-reviewed: 2026-07-24
---

# ADR-0002: Select CycloneDX as the default BOM format

## Context

Release evidence needs an interoperable inventory of components, services and dependencies while retaining license and ecosystem compatibility.

## Decision

Use CycloneDX 1.7 JSON as the default generated BOM format. Preserve export to SPDX where a consumer, legal process or ecosystem requires it.

## Consequences

R2/R3 release profiles target an SBOM. Syft is the default generator candidate because it can emit CycloneDX and SPDX. Generator activation remains a future version-pinned adapter decision.