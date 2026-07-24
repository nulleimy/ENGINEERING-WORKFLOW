---
id: EW-OPS-005
title: AI-Assisted Engineering Standard
status: proposed
owner: Eimy Herrer and Johny
version: 0.1.0
last-reviewed: 2026-07-24
---

# AI-Assisted Engineering Standard

AI is an accelerator, not an authority.

## Required pipeline

```text
CONTEXT → PLAN → CONSTRAINED EXECUTION → DETERMINISTIC VALIDATION → ADVERSARIAL REVIEW → HUMAN ACCEPTANCE → EVIDENCE
```

## Context packet

An AI task receives only relevant authoritative material:

- project identity and current baseline;
- exact objective and acceptance criteria;
- allowed and prohibited scope;
- architecture and security constraints;
- test and validation commands;
- data classification and secret boundaries.

## Controls

- generated output is untrusted until validated;
- an AI must not claim tests or changes it did not execute;
- R2/R3 changes require human review and independent deterministic checks;
- sensitive data and secrets must not be placed into an unauthorized model context;
- source and license provenance must be reviewed for generated or suggested implementation;
- model/provider changes are treated as dependency and risk changes;
- prompt, context and output retention follow project data policy.

## Metrics

Measure accepted value, lead time, escaped defects, rework, review time and automation coverage. Do not use token count, generated lines or prompt count as performance metrics.
