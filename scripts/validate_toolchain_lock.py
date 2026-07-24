#!/usr/bin/env python3
"""Validate pinned open-source enforcement tool metadata."""
from __future__ import annotations

import json
import re
import sys
from pathlib import PurePosixPath
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "platform/toolchain.lock.json"
SHA256 = re.compile(r"^[a-f0-9]{64}$")
FULL_COMMIT = re.compile(r"^[a-f0-9]{40}$")
ALLOWED_STATES = {"active", "configured", "selected", "evaluate", "deferred"}
ALLOWED_CLASSES = {
    "binary",
    "github-action",
    "service-or-cli",
    "reusable-workflow",
    "standard-and-sdk",
    "developer-portal",
}
ALLOWED_ARCHIVE_TYPES = {"raw", "deb", "tar.gz"}
PROHIBITED_FLOATING = {"latest", "main", "master", "unlocked", "not-selected", "profile-specific"}


def safe_binary_path(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and all(part not in {"", ".", ".."} for part in path.parts)


def main() -> int:
    errors: list[str] = []
    data = json.loads(LOCK.read_text(encoding="utf-8"))
    policy = data.get("policy", {})
    tools = data.get("tools", [])

    required_policy = {
        "floating_versions_allowed": False,
        "unverified_binary_execution_allowed": False,
        "curl_pipe_shell_allowed": False,
        "tool_failure_mode": "fail-closed-or-blocked",
        "native_validator_required": True,
    }
    for key, expected in required_policy.items():
        if policy.get(key) != expected:
            errors.append(f"policy {key!r} must equal {expected!r}")

    ids = [tool.get("id") for tool in tools]
    if not tools:
        errors.append("toolchain is empty")
    if len(ids) != len(set(ids)):
        errors.append("tool IDs are not unique")

    state_counts = {state: 0 for state in ALLOWED_STATES}
    for tool in tools:
        tool_id = tool.get("id")
        state = tool.get("state")
        tool_class = tool.get("tool_class")
        version = str(tool.get("version", ""))
        source = str(tool.get("source", ""))

        if not isinstance(tool_id, str) or not tool_id:
            errors.append("tool has invalid ID")
            continue
        if state not in ALLOWED_STATES:
            errors.append(f"{tool_id}: unsupported state {state!r}")
            continue
        state_counts[state] += 1
        if tool_class not in ALLOWED_CLASSES:
            errors.append(f"{tool_id}: unsupported tool class {tool_class!r}")
        if not source.startswith("https://"):
            errors.append(f"{tool_id}: source must use HTTPS")
        if not tool.get("license"):
            errors.append(f"{tool_id}: license is required")
        if not version:
            errors.append(f"{tool_id}: version is required")
        if state in {"active", "configured"} and version in PROHIBITED_FLOATING:
            errors.append(f"{tool_id}: active/configured tool uses non-pinned version {version!r}")

        if state == "active" and tool_class == "github-action":
            ref = str(tool.get("immutable_ref", ""))
            if not FULL_COMMIT.fullmatch(ref):
                errors.append(f"{tool_id}: active GitHub Action requires a full commit SHA")

        if state == "active" and tool_class == "binary":
            artifacts = tool.get("artifacts")
            if not isinstance(artifacts, dict) or not artifacts:
                errors.append(f"{tool_id}: active binary requires verified artifacts")
                continue
            for platform, artifact in artifacts.items():
                if not isinstance(artifact, dict):
                    errors.append(f"{tool_id}/{platform}: artifact must be an object")
                    continue
                url = str(artifact.get("url", ""))
                digest = str(artifact.get("sha256", ""))
                archive_type = artifact.get("archive_type", "raw")
                if not url.startswith("https://"):
                    errors.append(f"{tool_id}/{platform}: artifact URL must use HTTPS")
                if "/latest/" in url or url.endswith("/latest"):
                    errors.append(f"{tool_id}/{platform}: floating latest URL is prohibited")
                if not SHA256.fullmatch(digest):
                    errors.append(f"{tool_id}/{platform}: invalid SHA-256 digest")
                if archive_type not in ALLOWED_ARCHIVE_TYPES:
                    errors.append(f"{tool_id}/{platform}: unsupported archive_type {archive_type!r}")
                if archive_type != "raw" and not safe_binary_path(artifact.get("binary_path")):
                    errors.append(f"{tool_id}/{platform}: archived artifact requires a safe binary_path")

        if state in {"selected", "evaluate", "deferred"} and not tool.get("activation_requirement"):
            errors.append(f"{tool_id}: non-active tool requires an activation requirement")

    active_ids = {tool.get("id") for tool in tools if tool.get("state") == "active"}
    for required in {"opa", "openssf-scorecard-action", "syft", "grype"}:
        if required not in active_ids:
            errors.append(f"required active enforcement tool missing: {required}")

    if errors:
        print("TOOLCHAIN_VALIDATION=FAILED")
        for item in errors:
            print(f"ERROR: {item}")
        return 1

    print("TOOLCHAIN_VALIDATION=PASSED")
    print(f"TOOLS={len(tools)}")
    print(f"ACTIVE={state_counts['active']}")
    print(f"CONFIGURED={state_counts['configured']}")
    print(f"SELECTED={state_counts['selected']}")
    print(f"EVALUATE={state_counts['evaluate']}")
    print(f"DEFERRED={state_counts['deferred']}")
    print("UNVERIFIED_EXECUTION_ALLOWED=false")
    return 0


if __name__ == "__main__":
    sys.exit(main())
