#!/usr/bin/env python3
"""Download one active binary from the locked toolchain and verify SHA-256 before execution."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "platform/toolchain.lock.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("tool_id")
    parser.add_argument("--platform", required=True)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def download(url: str, destination: Path) -> str:
    digest = hashlib.sha256()
    request = urllib.request.Request(url, headers={"User-Agent": "ENGINEERING-WORKFLOW/0.5"})
    with urllib.request.urlopen(request, timeout=120) as response, destination.open("wb") as target:
        while chunk := response.read(1024 * 1024):
            target.write(chunk)
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    args = parse_args()
    data = json.loads(LOCK.read_text(encoding="utf-8"))
    tool = next((item for item in data.get("tools", []) if item.get("id") == args.tool_id), None)
    if tool is None:
        print(f"ERROR: unknown tool {args.tool_id!r}", file=sys.stderr)
        return 2
    if tool.get("state") != "active" or tool.get("tool_class") != "binary":
        print(f"ERROR: {args.tool_id} is not an active binary", file=sys.stderr)
        return 2

    artifact = tool.get("artifacts", {}).get(args.platform)
    if not isinstance(artifact, dict):
        print(f"ERROR: no locked artifact for {args.tool_id}/{args.platform}", file=sys.stderr)
        return 2

    expected = artifact["sha256"]
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix=f"ew-{args.tool_id}-") as tmpdir:
        candidate = Path(tmpdir) / args.tool_id
        actual = download(artifact["url"], candidate)
        if actual != expected:
            print(
                f"ERROR: checksum mismatch for {args.tool_id}/{args.platform}: expected {expected}, got {actual}",
                file=sys.stderr,
            )
            return 1
        candidate.chmod(candidate.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP)
        temp_output = output.with_suffix(output.suffix + ".tmp")
        shutil.copy2(candidate, temp_output)
        os.replace(temp_output, output)

    print("VERIFIED_TOOL_BOOTSTRAP=PASSED")
    print(f"TOOL={args.tool_id}")
    print(f"VERSION={tool['version']}")
    print(f"PLATFORM={args.platform}")
    print(f"SHA256={expected}")
    print(f"OUTPUT={output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
