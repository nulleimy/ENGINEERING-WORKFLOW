---
id: EW-DOC-001
title: Documentation Architecture
status: proposed
owner: Eimy Herrer and Johny
version: 0.1.0
last-reviewed: 2026-07-24
---

# Documentation Architecture

Documentation is organized by user need and engineering responsibility.

## Product control

- purpose, users, value, boundaries and roadmap;
- current status and support state.

## Architecture

- system context;
- container/deployment boundaries;
- significant components only where useful;
- runtime interactions for important flows;
- quality attributes, constraints and risks.

## Diátaxis content types

- **tutorials:** guided learning with a successful outcome;
- **how-to:** task-oriented operational steps;
- **reference:** precise descriptions of interfaces, configuration and schemas;
- **explanation:** rationale, domain knowledge and conceptual relationships.

## Operations and security

Runbooks, monitoring, backup, recovery, incidents, threat models, trust boundaries, data handling and release records.

## Rules

- do not create empty directories merely to satisfy the taxonomy;
- one fact has one canonical source;
- generated reference remains generated;
- documentation changes with the system;
- obsolete content is deprecated or archived, not left misleading;
- diagrams use a consistent notation and declared scope.
