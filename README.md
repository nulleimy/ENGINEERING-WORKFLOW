---
id: EW-README
title: ENGINEERING-WORKFLOW
status: current
owner: Eimy Herrer and Johny
version: 0.7.0-rc.1
last-reviewed: 2026-07-26
---

# ENGINEERING-WORKFLOW

**ENGINEERING-WORKFLOW** is a portable, AI-native engineering operating system for creating, changing, verifying, releasing, operating, and retiring software products at a consistently high standard.

It is designed for Eimy and Johny, but its control model is deliberately independent of Git, GitHub, a specific cloud, programming language, or AI provider.

## What this repository provides

- an exact canonical technical operating mode;
- a Product, Decision and Execution Constitution;
- a machine-readable constitutional authority and conflict model;
- a risk-based operating model with fast, governed and critical lanes;
- documentation architecture and reusable records;
- security, compliance, supply-chain, SRE, release and incident rules;
- AI-assisted engineering controls;
- project, work, product, decision and authority templates;
- an implementation and adoption roadmap;
- automated repository, constitutional, policy and readiness gates.

## Core principle

> The process is defined by portable records, verifiable baselines, evidence and clear authority. Tools are replaceable adapters.

## Constitutional entry point

Read the governance sources in this order:

1. [`governance/WORLD_CLASS_SOFTWARE_DEVOPS_OPERATING_MODE.md`](governance/WORLD_CLASS_SOFTWARE_DEVOPS_OPERATING_MODE.md) — technical truth, execution discipline and protected operations;
2. [`governance/PRODUCT_DECISION_EXECUTION_CONSTITUTION.md`](governance/PRODUCT_DECISION_EXECUTION_CONSTITUTION.md) — product value, decision authority and realization discipline;
3. [`governance/CONSTITUTIONAL_AUTHORITY.json`](governance/CONSTITUTIONAL_AUTHORITY.json) — exact hashes, authority order and fail-closed conflict rules;
4. [`governance/ENGINEERING_CONSTITUTION.md`](governance/ENGINEERING_CONSTITUTION.md) — concise project invariants;
5. [`governance/CONSTITUTIONAL_COMPATIBILITY_REPORT.md`](governance/CONSTITUTIONAL_COMPATIBILITY_REPORT.md) — verified relationship and remaining acceptance actions.

## Operating flow

```text
INTAKE → FRAME → CLASSIFY → DECIDE → SLICE → BUILD → VERIFY → ACCEPT → RELEASE → OPERATE → LEARN
```

## Quick start

1. Verify constitutional integrity:

```bash
python3 scripts/validate_constitutions.py
```

2. Select the correct lane using [`operating-model/RISK_AND_CHANGE_LANES.md`](operating-model/RISK_AND_CHANGE_LANES.md).
3. Define the product or change using [`templates/PRODUCT_DEFINITION.md`](templates/PRODUCT_DEFINITION.md) and [`templates/WORK_PACKAGE.md`](templates/WORK_PACKAGE.md).
4. Record significant decisions using [`templates/DECISION_RECORD.md`](templates/DECISION_RECORD.md).
5. Follow the lifecycle in [`operating-model/ENGINEERING_LIFECYCLE.md`](operating-model/ENGINEERING_LIFECYCLE.md).
6. Validate the repository:

```bash
python3 scripts/validate_repository.py
python3 scripts/validate_constitutions.py
python3 -m unittest discover -s tests -v
```

## Repository map

- `governance/` — constitutional authority, invariants, ownership and change control;
- `operating-model/` — lifecycle, quality, security, release, SRE and AI workflow;
- `architecture/`, `controls/`, `profiles/`, `assurance/`, `readiness/` — machine-readable engineering control plane;
- `documentation/` — documentation structure, metadata, evidence and architecture;
- `templates/` — reusable control, product, decision and operational records;
- `platform/`, `policy/`, `open-source/` — verified enforcement adapters;
- `roadmap/` — implementation, adoption and maturity progression;
- `references/` — standards baseline and terminology;
- `scripts/`, `tests/`, `.github/` — automated enforcement.

## Current state

The v0.1 foundation and the v0.2-v0.5 control, assurance, readiness and OPA layers are integrated into `main`. Constitutional governance v0.7 is proposed in a review branch. Supply-chain assurance v0.6 remains a separate draft pull request until explicit merge authority and post-merge signing evidence exist.

The system is not yet `WORLD_CLASS_READY`. Project scaffolding CLI, adoption automation, signed main/tag evidence, operational pilots and independent assessment remain required.

## Language policy

English is the canonical normative language for portable framework material. The two canonical Czech constitutions are normative by explicit governance decision and exact integrity binding. Translations are non-normative unless explicitly promoted.
