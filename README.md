---
id: EW-README
title: ENGINEERING-WORKFLOW
status: current
owner: Eimy Herrer and Johny
version: 0.8.0-rc.1
last-reviewed: 2026-07-26
---

# ENGINEERING-WORKFLOW

**ENGINEERING-WORKFLOW** is a portable, AI-native engineering operating system for creating, changing, verifying, releasing, operating and retiring software products at a consistently high standard.

## Primary engineering invariant

> Product cleanliness + Unix simplicity + DevOps automation + SRE reliability + zero-trust security + lifecycle-wide auditability.

Every change must be simple, purposeful, automated, secure, measurable, reversible and evidence-verifiable. The exact constitutional text and machine-readable interpretation are enforced by hash and CI.

## First executable product layer

The repository-native, dependency-free `ew` CLI provides:

```text
ew init
ew doctor
ew self-test
```

Run directly from a controlled checkout:

```bash
./bin/ew self-test --json
./bin/ew init ./my-project --name "My Project" --profile standard-product --risk R2 --reversibility REV-2 --dry-run
./bin/ew init ./my-project --name "My Project" --profile standard-product --risk R2 --reversibility REV-2
./bin/ew doctor ./my-project --json
```

`ew init` writes only `.engineering-workflow/`, publishes the full directory atomically, never overwrites controlled state and returns `NOOP` for an identical repeated request. Git is not required.

Distribution packaging remains blocked until the license and intellectual-property decision is accepted.

## Constitutional entry point

1. [`governance/WORLD_CLASS_SOFTWARE_DEVOPS_OPERATING_MODE.md`](governance/WORLD_CLASS_SOFTWARE_DEVOPS_OPERATING_MODE.md)
2. [`governance/PRODUCT_DECISION_EXECUTION_CONSTITUTION.md`](governance/PRODUCT_DECISION_EXECUTION_CONSTITUTION.md)
3. [`governance/PRIMARY_ENGINEERING_INVARIANT.json`](governance/PRIMARY_ENGINEERING_INVARIANT.json)
4. [`governance/CONSTITUTIONAL_AUTHORITY.json`](governance/CONSTITUTIONAL_AUTHORITY.json)
5. [`governance/ENGINEERING_CONSTITUTION.md`](governance/ENGINEERING_CONSTITUTION.md)
6. [`governance/CONSTITUTIONAL_COMPATIBILITY_REPORT.md`](governance/CONSTITUTIONAL_COMPATIBILITY_REPORT.md)

## Operating flow

```text
INTAKE → FRAME → CLASSIFY → DECIDE → SLICE → BUILD → VERIFY → ACCEPT → RELEASE → OPERATE → LEARN
```

## Framework validation

```bash
python3 scripts/validate_repository.py
python3 scripts/validate_constitutions.py
python3 scripts/validate_primary_invariant.py
./bin/ew self-test --json
python3 -m unittest discover -s tests -v
```

For R1-R3 work, evaluate [`config/complexity-budget.json`](config/complexity-budget.json), assign a class from [`config/reversibility-classes.json`](config/reversibility-classes.json), register repeated manual work and link lifecycle evidence beyond Git history.

## Repository map

- `governance/` — constitutions, authority, invariants, ownership and change control;
- `operating-model/` — lifecycle, quality, complexity, reversibility, security, release and SRE;
- `architecture/`, `controls/`, `profiles/`, `assurance/`, `readiness/` — machine-readable engineering control plane;
- `documentation/`, `evidence/` — documentation, lifecycle graph, evidence and retention;
- `bin/ew` — executable bootstrap and conformance layer;
- `templates/` — reusable product, decision, work and operational records;
- `platform/`, `policy/`, `open-source/` — verified enforcement adapters;
- `scripts/`, `tests/`, `.github/` — automated enforcement.

## Current state

The v0.1 foundation and v0.2-v0.5 control layers are integrated into `main`. Constitutional governance and the primary invariant are proposed in PR #8. The first repository-native `ew` CLI is proposed in a stacked PR. Supply-chain assurance remains separately reviewed in PR #7.

The system is not yet `WORLD_CLASS_READY`. `ew adopt`, upgrades, migrations, signed main/tag evidence, real pilots and independent assessment remain required.

## Language policy

English is canonical for portable framework material. The two exact Czech constitutions are normative by explicit governance decision and integrity binding.
