---
id: EW-CTRL-001
title: Control Model
status: proposed
owner: Eimy Herrer and Johny
version: 0.2.0-rc.1
last-reviewed: 2026-07-24
---

# Control Model

A control is a testable engineering obligation connecting policy to implementation and evidence.

Each control defines a stable ID, domain, objective, requirement level, minimum risk, accountable role, automation level, verification method, evidence type and exception policy.

## Control states

`NOT_APPLICABLE`, `PLANNED`, `IMPLEMENTED`, `VERIFIED`, `EXCEPTED`, `FAILED`, `UNKNOWN`.

Documentation alone never proves a control is verified.

## Exceptions

An exception is explicit, approved, risk-owned, compensating, expiring and connected to remediation. Controls marked as non-exceptable cannot be bypassed by project preference.

The canonical machine-readable catalog is `controls/catalog.json`.