---
id: EW-PLAT-003
title: EW CLI Foundation
status: proposed
owner: Eimy Herrer and Johny
version: 0.8.0-rc.1
last-reviewed: 2026-07-26
---

# EW CLI Foundation

`ew` is the portable, dependency-free bootstrap interface for ENGINEERING-WORKFLOW.

## Implemented commands

```text
ew init
ew doctor
ew self-test
```

`ew init` writes only `.engineering-workflow/`. It stages the complete controlled directory and atomically publishes it only when every record has been generated. It never overwrites an existing controlled project.

`ew doctor` verifies required records, profile/risk/reversibility consistency, manifest hashes, undeclared files, symlinks and lifecycle graph references.

`ew self-test` proves dry-run behavior, atomic creation, doctor success, idempotent re-execution, tamper detection and recovery inside an isolated temporary directory.

## Safety contract

- Git is not required.
- No product source file is modified.
- Existing controlled state is never silently replaced.
- Profile downgrade is rejected when risk or reversibility requires a stronger profile.
- `REV-3` and `REV-4` require a profile supporting R3.
- Generated records do not claim product, release or operational readiness.
- A failed write is cleaned up before returning.
- Existing inconsistent state returns `BLOCKED`.

## Execution

```bash
./bin/ew self-test --json
```

The repository-native script has no external runtime dependencies and does not require Git. Distribution packaging remains deferred until license and intellectual-property authority are accepted.

## Deliberately deferred

`ew adopt`, upgrades, migrations, provider adapters, release signing and remote evidence storage are separate governed slices.
