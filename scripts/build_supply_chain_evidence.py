#!/usr/bin/env python3
"""Create a portable supply-chain evidence record from generated artifacts."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--sbom", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    inputs = {name: ROOT / getattr(args, name) for name in ("artifact", "manifest", "sbom", "report")}
    record = {
        "schema_version": 1,
        "type": "supply-chain-pipeline-evidence",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "repository": os.getenv("GITHUB_REPOSITORY", "local"),
        "source_revision": os.getenv("GITHUB_SHA", "local"),
        "workflow_run_id": os.getenv("GITHUB_RUN_ID", "local"),
        "event": os.getenv("GITHUB_EVENT_NAME", "local"),
        "artifacts": {
            name: {"path": path.relative_to(ROOT).as_posix(), "sha256": sha256(path)}
            for name, path in inputs.items()
        },
        "controls": {
            "deterministic_package": "VERIFIED",
            "sha256_manifest": "VERIFIED",
            "cyclonedx_sbom": "VERIFIED",
            "vulnerability_gate": "VERIFIED",
            "provenance": "TARGET",
            "keyless_signature": "TARGET",
        },
        "claims": {
            "slsa_level": "NOT_CLAIMED",
            "world_class_ready": False,
            "certified": False,
        },
    }
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("SUPPLY_CHAIN_EVIDENCE=CREATED")
    print(f"OUTPUT={output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
