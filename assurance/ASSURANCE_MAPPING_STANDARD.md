---
id: EW-ASSURANCE-001
title: Assurance Mapping and Claim Standard
status: proposed
owner: Eimy Herrer and Johny
version: 0.3.0-rc.1
last-reviewed: 2026-07-24
---

# Assurance Mapping and Claim Standard

## Purpose

This standard connects ENGINEERING-WORKFLOW controls to authoritative external frameworks while preventing unsupported claims of compliance, certification or security maturity.

## Normative baselines

- NIST SP 800-218 / SSDF 1.1 — final;
- NIST SP 800-218A — final and applicable to AI-model or AI-system development;
- SLSA 1.2 — approved Source and Build tracks;
- OWASP ASVS 5.0.0 — stable and applicable to web applications, APIs and relied-upon application controls;
- OpenSSF OSPS Baseline 2026.02.19 — current for public open-source projects.

NIST SSDF 1.2 remains draft and may only be used for gap monitoring and migration preparation.

## Mapping semantics

- `direct`: substantially the same intended outcome;
- `supporting`: supplies part of an outcome or its evidence;
- `contextual`: informs implementation but is not equivalent.

No mapping automatically proves external-framework conformance.

## Claim states

External-framework claims MUST use one of:

- `NOT_APPLICABLE` — applicability decision is recorded;
- `TARGET` — selected future target without implementation claim;
- `IMPLEMENTED` — required mechanisms exist but verification is incomplete;
- `PARTIALLY_VERIFIED` — part of the scoped requirement is evidenced;
- `VERIFIED` — scoped requirements have current evidence and independent acceptance where required;
- `EXCEPTED` — a permitted, expiring exception exists;
- `FAILED` — the scoped requirement is not met;
- `UNKNOWN` — evidence is insufficient.

`CERTIFIED` MUST NOT be used unless an authorized external certification scheme and current certificate exist.

## Version qualification

Every external reference MUST identify its framework version. OWASP ASVS requirement identifiers MUST use the version-qualified form, for example `v5.0.0-1.2.5`, when individual requirements are recorded.

## Applicability

A framework may be non-applicable to a project or control, but non-applicability requires a reason, authority, date and review trigger. Applicability MUST be re-evaluated when the product adds public interfaces, production operation, sensitive data, AI autonomy, external users, regulated obligations or a new distribution model.

## Evidence

A `VERIFIED` claim requires evidence that is:

- linked to the exact project, baseline, change or release;
- attributable to a person or controlled system;
- timestamped;
- integrity-verifiable where technically possible;
- current for the claimed scope;
- retained according to the evidence catalog;
- independently accepted for A3-A5 controls where required.

Screenshots and narrative statements alone are not sufficient evidence when machine-readable output is available.

## SLSA claim rule

SLSA Source and Build levels are independent. A project MUST state each track separately and MUST NOT claim an overall unqualified “SLSA level.” The claim must identify the assessed source control system, build platform, artifact, provenance and verification policy.

## OSPS claim rule

OSPS Baseline level is selected according to the current version’s applicability conditions. The project must pin the baseline version and record every applicable control result. A mapping from another framework is not accepted as automatic OSPS satisfaction.

## ASVS claim rule

ASVS applies to the scoped application and its relied-upon technical controls. The project must record the selected ASVS level, exact version, requirement set, test method, result and accepted exclusions. Using ASVS as design guidance does not equal verified conformance.

## Continuous review

Framework versions are checked at least quarterly and on release announcements. Version updates enter through a governed change with delta analysis, migration plan, control impact and rollback.
