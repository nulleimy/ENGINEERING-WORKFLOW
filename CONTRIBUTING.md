---
id: EW-CONTRIBUTING
title: Contributing
status: current
owner: Eimy Herrer and Johny
version: 0.1.0
last-reviewed: 2026-07-24
---

# Contributing

## Contribution contract

Every contribution must be tied to a defined work package or clearly classified as an R0 editorial correction.

### Required behavior

1. Establish the current baseline.
2. Declare the intended outcome and allowed scope.
3. Select a risk lane.
4. Keep the change small and logically coherent.
5. Run the applicable quality gates.
6. Update documentation in the same change set.
7. Record verification limitations honestly.
8. Provide rollback or recovery instructions where applicable.

### Change records

Use [`templates/WORK_PACKAGE.md`](templates/WORK_PACKAGE.md) for R1-R3 work and [`templates/ADR.md`](templates/ADR.md) for significant or difficult-to-reverse decisions.

### Review

R2 and R3 changes require independent review. The author must not be the only accepting authority for critical security, production, data, identity, compliance or irreversible changes.

### Commit and source-control adapters

Git is the default adapter for this repository, not the process definition. When Git is used, prefer short-lived branches, small commits with one logical responsibility, and conventional commit messages.
