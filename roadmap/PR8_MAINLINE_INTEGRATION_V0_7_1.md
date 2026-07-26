---
id: EW-RM-008
title: PR8 Mainline Constitutional Integration v0.7.1
status: proposed
owner: Eimy Herrer and Johny
version: 0.7.1-rc.1
last-reviewed: 2026-07-26
---

# PR8 Mainline Constitutional Integration v0.7.1

## Baseline

- main: `b4771d06850d1d76e5aab51f12eb24e267cf5666`
- source governance PR: #8 at `11b0762d02325de2baa8526afd92613aee710c2b`
- integration branch: `integration/pr8-governance-on-main-v0.7.1`

## Integration decision

The original PR #8 branch diverged after supply-chain PR #7 entered `main`. This integration rebuilds the constitutional governance change directly on the current mainline instead of mechanically overwriting newer supply-chain files.

## Preserved mainline controls

- deterministic artifact packaging;
- CycloneDX SBOM;
- vulnerability blocking;
- supply-chain evidence;
- provenance and signing workflow;
- immutable workflow references;
- supply-chain validator and tests.

## Integrated governance controls

- exact Product, Decision and Execution Constitution RC3;
- constitutional authority and integrity hashes;
- Article 0 primary engineering invariant;
- complexity budget;
- reversibility classes;
- manual-work register;
- lifecycle evidence graph;
- constitutional validators and negative tests;
- independent constitutional CI workflow.

## Acceptance

The integration remains `PROPOSED` until all CI gates pass and independent review confirms that no supply-chain control was weakened.
