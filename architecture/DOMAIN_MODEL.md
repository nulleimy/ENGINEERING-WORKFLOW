---
id: EW-ARCH-001
title: Engineering Domain Model
status: proposed
owner: Eimy Herrer and Johny
version: 0.2.0-rc.1
last-reviewed: 2026-07-24
---

# Engineering Domain Model

ENGINEERING-WORKFLOW separates stable obligations from procedures, tool adapters and evidence.

## Domains

| Code | Domain | Primary outcome |
|---|---|---|
| GOV | Governance | authority, ownership, exceptions and policy lifecycle |
| PROD | Product | verified problem, user value and product boundaries |
| ARCH | Architecture | explicit structure, contracts and trust boundaries |
| DEL | Delivery | small controlled work packages and fast flow |
| QUAL | Quality | verified behavior at the appropriate test level |
| SEC | Security | secure design, least privilege and threat-driven controls |
| SUP | Supply chain | dependency, license, SBOM, provenance and artifact integrity |
| PLAT | Platform | reproducible environments and golden paths |
| REL | Release | attributable, approved and recoverable releases |
| OPS | Operations/SRE | ownership, observability, reliability and recovery |
| DOC | Documentation | current, discoverable and controlled knowledge |
| AI | AI engineering | constrained AI use with deterministic validation |
| COMP | Compliance | obligations mapped to implementation and evidence |
| INC | Incident management | containment, recovery, learning and corrective action |

## Layer model

```text
CONSTITUTION
  → STANDARDS
    → PROCEDURES
      → TEMPLATES / SCHEMAS
        → CONTROLS / POLICIES
          → ADAPTERS / GOLDEN PATHS
            → EVIDENCE / METRICS
```

Lower layers may implement higher layers but may not redefine them. GitHub, Drive, CI platforms and AI providers remain replaceable adapters.