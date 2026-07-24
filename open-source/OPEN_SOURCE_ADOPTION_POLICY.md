---
id: EW-OSS-001
title: Open Source Adoption Policy
status: proposed
owner: Eimy Herrer and Johny
version: 0.2.0-rc.1
last-reviewed: 2026-07-24
---

# Open Source Adoption Policy

Open source is preferred when it reduces undifferentiated work, improves interoperability and has acceptable lifecycle cost.

## Adoption gate

Before adoption record the problem, alternatives, project health, license compatibility, security history, release integrity, permissions and data access, operational footprint, update path, exit strategy, pilot and acceptance evidence.

## States

`adopted`, `configuration-ready`, `selected`, `evaluate`, `hold`, `rejected`, `retired`.

## Rules

- No tool is adopted solely because it is popular.
- Critical CI dependencies are pinned to immutable full commit SHAs.
- Every dependency has an owner and removal path.
- AGPL and other strong-copyleft tools receive deployment/use-model review.
- SaaS terms are reviewed separately from the underlying open-source license.
- Selection is not activation; production use requires a tested, version-pinned adapter.