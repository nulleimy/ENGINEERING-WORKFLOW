#!/usr/bin/env python3
"""Download one active binary from the locked toolchain and verify it before execution."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "platform/toolchain.lock.json"
ALLOWED_ARCHIVE_TYPES = {"raw", "deb", "tar.gz"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("tool_id")
    parser.add_argument("--platform", required=True)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def download(url: str, destination: Path) -> str:
    digest = hashlib.sha256()
    request = urllib.request.Request(url, headers={"User-Agent": "ENGINEERING-WORKFLOW/0.6"})
    with urllib.request.urlopen(request, timeout=120) as response, destination.open("wb") as target:
        while chunk := response.read(1024 * 1024):
            target.write(chunk)
            digest.update(chunk)
    return digest.hexdigest()


def validated_relative_path(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError(f"unsafe binary_path: {value!r}")
    return path


def extract_tar_binary(archive_path: Path, binary_path: str, destination: Path) -> None:
    expected = validated_relative_path(binary_path).as_posix()
    with tarfile.open(archive_path, mode="r:gz") as archive:
        matches = []
        for member in archive.getmembers():
            normalized = PurePosixPath(member.name.lstrip("./")).as_posix()
            if normalized == expected:
                matches.append(member)
        if len(matches) != 1:
            raise ValueError(f"expected exactly one archive member {expected!r}, found {len(matches)}")
        member = matches[0]
        if not member.isfile() or member.issym() or member.islnk():
            raise ValueError(f"archive member {expected!r} is not a regular file")
        source = archive.extractfile(member)
        if source is None:
            raise ValueError(f"unable to read archive member {expected!r}")
        with source, destination.open("wb") as target:
            shutil.copyfileobj(source, target)


def extract_deb_binary(archive_path: Path, binary_path: str, destination: Path, workdir: Path) -> None:
    validated = validated_relative_path(binary_path)
    dpkg_deb = shutil.which("dpkg-deb")
    if dpkg_deb is None:
        raise RuntimeError("dpkg-deb is required to extract a locked .deb artifact")
    extract_root = workdir / "deb-root"
    subprocess.run(
        [dpkg_deb, "--extract", str(archive_path), str(extract_root)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    root = extract_root.resolve()
    source = (extract_root / Path(*validated.parts)).resolve()
    source.relative_to(root)
    if not source.is_file() or source.is_symlink():
        raise ValueError(f"extracted binary {binary_path!r} is missing or not a regular file")
    shutil.copyfile(source, destination)


def materialize_binary(artifact_path: Path, artifact: dict[str, str], destination: Path, workdir: Path) -> None:
    archive_type = artifact.get("archive_type", "raw")
    if archive_type not in ALLOWED_ARCHIVE_TYPES:
        raise ValueError(f"unsupported archive_type: {archive_type!r}")
    if archive_type == "raw":
        shutil.copyfile(artifact_path, destination)
        return
    binary_path = artifact.get("binary_path")
    if not binary_path:
        raise ValueError(f"archive_type {archive_type!r} requires binary_path")
    if archive_type == "tar.gz":
        extract_tar_binary(artifact_path, binary_path, destination)
        return
    extract_deb_binary(artifact_path, binary_path, destination, workdir)


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

    try:
        with tempfile.TemporaryDirectory(prefix=f"ew-{args.tool_id}-") as tmpdir_value:
            tmpdir = Path(tmpdir_value)
            downloaded = tmpdir / "artifact"
            actual = download(artifact["url"], downloaded)
            if actual != expected:
                print(
                    f"ERROR: checksum mismatch for {args.tool_id}/{args.platform}: expected {expected}, got {actual}",
                    file=sys.stderr,
                )
                return 1

            materialized = tmpdir / args.tool_id
            materialize_binary(downloaded, artifact, materialized, tmpdir)
            materialized.chmod(materialized.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP)
            temp_output = output.with_suffix(output.suffix + ".tmp")
            shutil.copy2(materialized, temp_output)
            os.replace(temp_output, output)
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: failed to materialize {args.tool_id}/{args.platform}: {exc}", file=sys.stderr)
        return 1

    print("VERIFIED_TOOL_BOOTSTRAP=PASSED")
    print(f"TOOL={args.tool_id}")
    print(f"VERSION={tool['version']}")
    print(f"PLATFORM={args.platform}")
    print(f"ARTIFACT_SHA256={expected}")
    print(f"OUTPUT={output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
