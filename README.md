---
id: EW-README
title: ENGINEERING-WORKFLOW
status: current
owner: Eimy Herrer and Johny
version: 0.1.0
last-reviewed: 2026-07-24
---

# ENGINEERING-WORKFLOW

**ENGINEERING-WORKFLOW** is a portable, AI-native engineering operating system for creating, changing, verifying, releasing, operating, and retiring software products at a consistently high standard.

It is designed for Eimy and Johny, but its control model is deliberately independent of Git, GitHub, a specific cloud, programming language, or AI provider.

## What this repository provides

- a concise engineering constitution and governance model;
- a risk-based operating model with a fast lane and a governed lane;
- documentation architecture and reusable records;
- security, compliance, supply-chain, SRE, release, and incident rules;
- AI-assisted engineering controls;
- project and work templates;
- an implementation and adoption roadmap;
- automated repository validation and a CI quality gate.

## Core principle

> The process is defined by portable records, verifiable baselines, evidence, and clear authority. Tools are replaceable adapters.

## Operating flow

```text
FRAME → SLICE → BUILD → VERIFY → ACCEPT → RELEASE → OPERATE → LEARN
```

## Quick start

1. Read [`governance/ENGINEERING_CONSTITUTION.md`](governance/ENGINEERING_CONSTITUTION.md).
2. Select the correct lane using [`operating-model/RISK_AND_CHANGE_LANES.md`](operating-model/RISK_AND_CHANGE_LANES.md).
3. Create a work package from [`templates/WORK_PACKAGE.md`](templates/WORK_PACKAGE.md).
4. Follow the lifecycle in [`operating-model/ENGINEERING_LIFECYCLE.md`](operating-model/ENGINEERING_LIFECYCLE.md).
5. Validate the repository:

```bash
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests -v
```

## Repository map

- `governance/` — authority, invariants, ownership, change control;
- `operating-model/` — lifecycle, quality, security, release, SRE, AI workflow;
- `documentation/` — documentation structure, metadata, evidence and architecture;
- `templates/` — reusable control records and operational templates;
- `roadmap/` — implementation, adoption and maturity progression;
- `references/` — standards baseline and terminology;
- `scripts/`, `tests/`, `.github/` — automated enforcement.

## Current state

`0.1.0` is the **Foundation Release Candidate**. The control model, templates, validator and CI baseline are implemented. Organization-wide rollout, project scaffolding CLI, deployment adapters and compliance automation remain roadmap items.

## Language policy

English is the canonical normative language to keep the system portable and globally usable. Existing Czech normative material is preserved verbatim where required. Translations may be added, but they are non-normative unless explicitly promoted.
