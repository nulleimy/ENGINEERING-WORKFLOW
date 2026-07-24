#!/usr/bin/env python3
"""Validate supply-chain policy against the locked toolchain and repository controls."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "supply-chain/policy.json"
LOCK = ROOT / "platform/toolchain.lock.json"
REQUIRED_FORMATS = {"syft-json", "cyclonedx-json", "spdx-json"}
REQUIRED_STATES = {"PASSED", "CONTROL_FAILED", "TOOL_FAILED", "BLOCKED"}
REQUIRED_PATHS = {
    "supply-chain/SUPPLY_CHAIN_EVIDENCE_STANDARD.md",
    "supply-chain/policy.json",
    "scripts/build_source_artifact.py",
    "scripts/build_supply_chain_evidence.py",
    "scripts/validate_supply_chain_policy.py",
    ".github/workflows/supply-chain.yml",
}


def main() -> int:
    errors: list[str] = []
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    tools = {item["id"]: item for item in lock.get("tools", []) if isinstance(item, dict) and item.get("id")}

    artifact = policy.get("artifact", {})
    if artifact.get("builder") != "scripts/build_source_artifact.py":
        errors.append("artifact builder must be scripts/build_source_artifact.py")
    if artifact.get("format") != "tar.gz" or artifact.get("deterministic") is not True:
        errors.append("source artifact must be deterministic tar.gz")
    if artifact.get("hash") != "sha256":
        errors.append("source artifact hash must be sha256")

    sbom = policy.get("sbom", {})
    if set(sbom.get("formats", [])) != REQUIRED_FORMATS:
        errors.append("SBOM formats must be syft-json, cyclonedx-json and spdx-json")
    if sbom.get("native_format_is_authoritative") is not True:
        errors.append("native Syft JSON must remain the authoritative SBOM")
    syft = tools.get("syft", {})
    if syft.get("state") != "active":
        errors.append("Syft must be active")
    if sbom.get("required_version") != syft.get("version"):
        errors.append("SBOM policy version does not match locked Syft version")

    vulnerability = policy.get("vulnerability", {})
    grype = tools.get("grype", {})
    if grype.get("state") != "active":
        errors.append("Grype must be active")
    if vulnerability.get("required_version") != grype.get("version"):
        errors.append("vulnerability policy version does not match locked Grype version")
    if vulnerability.get("input_format") != "syft-json":
        errors.append("Grype must consume the authoritative Syft JSON SBOM")
    if vulnerability.get("fail_on") != "high":
        errors.append("vulnerability threshold must block HIGH and CRITICAL findings")
    for key in (
        "vex_required_for_suppression",
        "governed_exception_required_for_suppression",
        "database_status_evidence_required",
    ):
        if vulnerability.get(key) is not True:
            errors.append(f"vulnerability policy {key} must be true")
    if vulnerability.get("silent_ignore_allowed") is not False:
        errors.append("silent vulnerability ignores must be prohibited")

    evidence = policy.get("evidence", {})
    if set(evidence.get("required_result_states", [])) != REQUIRED_STATES:
        errors.append("evidence result states are incomplete")
    if not isinstance(evidence.get("retention_days"), int) or evidence["retention_days"] < 30:
        errors.append("pull-request supply-chain evidence retention must be at least 30 days")

    for relative in REQUIRED_PATHS:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required supply-chain path: {relative}")

    if errors:
        print("SUPPLY_CHAIN_POLICY_VALIDATION=FAILED")
        for item in errors:
            print(f"ERROR: {item}")
        return 1

    print("SUPPLY_CHAIN_POLICY_VALIDATION=PASSED")
    print(f"SYFT_VERSION={syft['version']}")
    print(f"GRYPE_VERSION={grype['version']}")
    print("SBOM_FORMATS=3")
    print("VULNERABILITY_THRESHOLD=high")
    print("SILENT_IGNORE_ALLOWED=false")
    return 0


if __name__ == "__main__":
    sys.exit(main())
