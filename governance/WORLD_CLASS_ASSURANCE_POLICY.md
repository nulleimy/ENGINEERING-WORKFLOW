---
id: EW-GOV-006
title: World-Class Assurance and Anti-Downgrade Policy
status: proposed
owner: Eimy Herrer and Johny
version: 0.2.0-rc.2
last-reviewed: 2026-07-24
---

# World-Class Assurance and Anti-Downgrade Policy

## Purpose

ENGINEERING-WORKFLOW accepts only professional, current and evidence-backed engineering practices. A project may use a lighter workflow only when its actual risk and operating context justify it; it may never lower assurance merely to reduce effort, avoid review or accelerate delivery artificially.

## Governing rule

> Every project MUST use the highest applicable assurance profile required by its real product, security, data, operational, legal and supply-chain risk.

The phrase **highest applicable** is intentional. Applying every critical-system control to a disposable experiment creates delay without increasing trust. Applying an experiment profile to production creates unacceptable risk. World-class engineering optimizes both flow and assurance through correct classification, automation and evidence.

## Anti-downgrade requirements

1. Profile selection MUST be based on actual risk and impact, not convenience.
2. A project MUST automatically escalate when it gains production users, sensitive data, external commitments, privileged access, persistent state, public interfaces or regulatory obligations.
3. Security-critical, identity, authorization, payment, confidential-data and irreversible-change work MUST use the highest critical assurance profile.
4. No profile may waive truthfulness, ownership, provenance, secret protection, deterministic validation, recovery or evidence integrity.
5. A lower profile MUST NOT be used to bypass independent review, release controls, threat modeling or tested recovery.
6. Exceptions MUST be temporary, explicitly approved, compensating, expiring and connected to remediation. Non-exceptable controls cannot be waived.
7. Draft standards may inform design but MUST NOT be represented as final or certified requirements.
8. Stable final standards are normative until a newer final version is evaluated, migrated and accepted.
9. Compliance or certification MUST NOT be claimed without scoped independent evidence and the required authority.
10. Highest assurance MUST be implemented primarily through golden paths and automated controls, not repeated manual paperwork.

## Assurance levels

### A1 — Professional Foundation

For experiments without production data, production credentials or external service commitments.

Mandatory outcomes include canonical ownership, bounded work, deterministic checks, no secrets, documented assumptions, AI output validation and reproducible handoff.

### A2 — Controlled Engineering

For internal tools and persistent team systems.

Adds dependency provenance, reproducible environments, controlled releases, recovery and maintained operational ownership.

### A3 — High-Assurance Product

For supported products, external integrations and public interfaces.

Adds architecture and trust-boundary review, contract compatibility, SBOM/provenance targets, independent review, security verification and compliance-to-evidence mapping.

### A4 — Production Assurance

For operated services and user-facing production systems.

Adds SLOs, observability, incident readiness, progressive delivery, tested restore, operational acceptance and production change evidence.

### A5 — Critical Trust

For authentication, authorization, privileged execution, sensitive or regulated data, critical infrastructure, destructive migrations and high-consequence AI autonomy.

Adds two-person acceptance, threat-led verification, isolated or progressive rollout, immutable release inputs, signed provenance targets, recovery rehearsal, residual-risk authority and complete evidence preservation.

## External assurance baseline

The system tracks and maps applicable controls to current authoritative standards, including:

- NIST SSDF final releases for secure software development;
- SLSA current stable Source and Build tracks for source and artifact integrity;
- OpenSSF OSPS Baseline and Scorecard for public open-source project security;
- OWASP ASVS current stable release for application-security verification;
- CycloneDX and SPDX current stable specifications for software transparency;
- DORA delivery-performance outcomes for flow and stability.

A reference does not constitute certification. Each adoption requires explicit scope, control mapping, implementation, verification and evidence.

## Acceptance criteria

A project is compliant with this policy only when:

- its assurance profile is declared and justified;
- every required control is implemented, verified or formally excepted where exceptions are allowed;
- profile escalation triggers are monitored;
- the project cannot silently select a lower profile;
- evidence demonstrates the real state;
- remaining gaps are explicit and block claims of higher maturity.
