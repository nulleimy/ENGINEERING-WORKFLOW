#!/usr/bin/env python3
"""Validate supply-chain policy, workflow pins, artifacts, SBOM and Grype output."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "supply-chain/policy.json"
LOCK = ROOT / "platform/toolchain.lock.json"
WORKFLOW = ROOT / ".github/workflows/supply-chain.yml"
FULL_SHA = re.compile(r"@[a-f0-9]{40}(?:\s|#|$)")
BLOCKING = {"critical", "high", "unknown"}
REQUIRED_ACTIVE = {
    "anchore-sbom-action",
    "anchore-scan-action",
    "cosign-installer-action",
    "github-attest-action",
    "upload-artifact-action",
    "download-artifact-action",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def validate_static(errors: list[str]) -> None:
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    if policy.get("artifact", {}).get("deterministic") is not True:
        errors.append("artifact build must be deterministic")
    if policy.get("sbom", {}).get("canonical_format") != "cyclonedx-json":
        errors.append("canonical SBOM must be cyclonedx-json")
    severities = set(policy.get("vulnerability", {}).get("blocking_severities", []))
    if severities != BLOCKING:
        errors.append("blocking severities must be critical, high and unknown")
    if policy.get("vulnerability", {}).get("ignore_unfixed") is not False:
        errors.append("unfixed vulnerabilities must not be ignored")
    vex = policy.get("vulnerability", {}).get("vex", {})
    if vex.get("independent_acceptance_required") is not True or vex.get("ai_may_accept") is not False:
        errors.append("VEX requires independent human acceptance and prohibits AI acceptance")
    if policy.get("authority", {}).get("pull_request_signing_allowed") is not False:
        errors.append("pull-request signing must be prohibited")

    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    active = {item.get("id") for item in lock.get("tools", []) if item.get("state") == "active"}
    missing = sorted(REQUIRED_ACTIVE - active)
    if missing:
        errors.append(f"missing active supply-chain adapters: {', '.join(missing)}")

    workflow = WORKFLOW.read_text(encoding="utf-8")
    for line in workflow.splitlines():
        stripped = line.strip()
        if "uses:" in stripped and not FULL_SHA.search(stripped):
            errors.append(f"mutable workflow action reference: {stripped}")
    required_fragments = [
        "severity-cutoff: high",
        "fail-build: true",
        "pull_request_signing_allowed",
        "actions/attest@",
        "cosign verify-blob",
    ]
    for fragment in required_fragments:
        if fragment not in workflow:
            errors.append(f"workflow missing required fragment: {fragment}")


def validate_runtime(errors: list[str], artifact: Path | None, manifest: Path | None, sbom: Path | None, report: Path | None) -> None:
    if artifact and manifest:
        expected = manifest.read_text(encoding="utf-8").split()[0]
        actual = digest(artifact)
        if actual != expected:
            errors.append("artifact digest does not match manifest")
    if sbom:
        data = json.loads(sbom.read_text(encoding="utf-8"))
        if data.get("bomFormat") != "CycloneDX":
            errors.append("SBOM is not CycloneDX")
        if not data.get("specVersion"):
            errors.append("SBOM specVersion is missing")
    if report:
        data = json.loads(report.read_text(encoding="utf-8"))
        blocked: list[str] = []
        for match in data.get("matches", []):
            vulnerability = match.get("vulnerability", {})
            severity = str(vulnerability.get("severity", "unknown")).lower()
            if severity in BLOCKING:
                blocked.append(f"{vulnerability.get('id', 'UNKNOWN')}:{severity}")
        if blocked:
            errors.append("blocking vulnerabilities: " + ", ".join(sorted(blocked)))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact")
    parser.add_argument("--manifest")
    parser.add_argument("--sbom")
    parser.add_argument("--report")
    args = parser.parse_args()
    errors: list[str] = []
    validate_static(errors)
    validate_runtime(
        errors,
        ROOT / args.artifact if args.artifact else None,
        ROOT / args.manifest if args.manifest else None,
        ROOT / args.sbom if args.sbom else None,
        ROOT / args.report if args.report else None,
    )
    if errors:
        print("SUPPLY_CHAIN_VALIDATION=FAILED")
        for item in errors:
            print(f"ERROR: {item}")
        return 1
    print("SUPPLY_CHAIN_VALIDATION=PASSED")
    print("PR_SIGNING_ALLOWED=false")
    print("BLOCKING_SEVERITIES=critical,high,unknown")
    return 0


if __name__ == "__main__":
    sys.exit(main())
