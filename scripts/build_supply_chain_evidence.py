#!/usr/bin/env python3
"""Assemble a hashed supply-chain evidence bundle after SBOM and vulnerability evaluation."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "platform/toolchain.lock.json"
POLICY = ROOT / "supply-chain/policy.json"
EXCLUDED_FROM_SUMS = {"evidence-manifest.json", "SHA256SUMS"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--scan-exit-code", type=int, required=True)
    parser.add_argument("--baseline", default=os.environ.get("GITHUB_SHA", "UNKNOWN"))
    parser.add_argument("--run-id", default=os.environ.get("GITHUB_RUN_ID", "UNKNOWN"))
    parser.add_argument("--run-attempt", default=os.environ.get("GITHUB_RUN_ATTEMPT", "UNKNOWN"))
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while chunk := source.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def result_for_exit_code(value: int) -> str:
    if value == 0:
        return "PASSED"
    if value == 2:
        return "CONTROL_FAILED"
    return "TOOL_FAILED"


def main() -> int:
    args = parse_args()
    directory = args.directory.resolve()
    if not directory.is_dir():
        print(f"ERROR: evidence directory is missing: {directory}", file=sys.stderr)
        return 2

    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    tools = {item["id"]: item for item in lock.get("tools", []) if isinstance(item, dict) and item.get("id")}
    result = result_for_exit_code(args.scan_exit_code)

    scan_status = {
        "schema_version": 1,
        "scanner": "grype",
        "scanner_version": tools["grype"]["version"],
        "exit_code": args.scan_exit_code,
        "result": result,
        "blocking_threshold": policy["vulnerability"]["fail_on"],
        "silent_ignore_allowed": False,
    }
    (directory / "scan-status.json").write_text(
        json.dumps(scan_status, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    required = {
        "source.tar.gz",
        "source-manifest.json",
        "sbom.syft.json",
        "sbom.cyclonedx.json",
        "sbom.spdx.json",
        "vulnerabilities.json",
        "grype-db-status.json",
        "scan-status.json",
    }
    missing = sorted(name for name in required if not (directory / name).is_file())
    if missing:
        print(f"ERROR: missing supply-chain evidence files: {', '.join(missing)}", file=sys.stderr)
        return 1

    files = sorted(
        path
        for path in directory.iterdir()
        if path.is_file() and path.name not in EXCLUDED_FROM_SUMS
    )
    checksum_lines = [f"{sha256(path)}  {path.name}" for path in files]
    checksum_path = directory / "SHA256SUMS"
    checksum_path.write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")

    manifest = {
        "schema_version": 1,
        "state": "GENERATED_PENDING_ACCEPTANCE",
        "baseline": args.baseline,
        "workflow": {
            "run_id": args.run_id,
            "run_attempt": args.run_attempt,
        },
        "result": result,
        "policy_version": policy["version"],
        "tools": {
            "syft": tools["syft"]["version"],
            "grype": tools["grype"]["version"],
        },
        "artifacts": [
            {
                "path": path.name,
                "sha256": sha256(path),
                "size": path.stat().st_size,
            }
            for path in files
        ],
        "checksums": {
            "path": checksum_path.name,
            "sha256": sha256(checksum_path),
        },
        "claim": "This bundle records CI evidence only; it is not a SLSA or certification claim.",
    }
    manifest_path = directory / "evidence-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("SUPPLY_CHAIN_EVIDENCE=BUILT")
    print(f"RESULT={result}")
    print(f"FILES={len(files) + 2}")
    print(f"MANIFEST={manifest_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
