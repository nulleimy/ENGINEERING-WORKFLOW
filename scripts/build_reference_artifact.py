#!/usr/bin/env python3
"""Build a deterministic source artifact and SHA-256 manifest."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {".git", ".tools", "dist", "__pycache__", ".pytest_cache"}


def source_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in EXCLUDED_PARTS for part in path.relative_to(ROOT).parts):
            continue
        files.append(path)
    return sorted(files, key=lambda item: item.relative_to(ROOT).as_posix())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build(output: Path) -> int:
    output.parent.mkdir(parents=True, exist_ok=True)
    files = source_files()
    with output.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w") as archive:
                for path in files:
                    relative = path.relative_to(ROOT)
                    info = archive.gettarinfo(str(path), arcname=relative.as_posix())
                    info.uid = 0
                    info.gid = 0
                    info.uname = ""
                    info.gname = ""
                    info.mtime = 0
                    info.mode = 0o755 if os.access(path, os.X_OK) else 0o644
                    with path.open("rb") as handle:
                        archive.addfile(info, handle)
    return len(files)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="dist/engineering-workflow.tar.gz")
    parser.add_argument("--manifest", default="dist/SHA256SUMS")
    args = parser.parse_args()

    output = ROOT / args.output
    manifest = ROOT / args.manifest
    count = build(output)
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(f"{sha256(output)}  {output.name}\n", encoding="utf-8")
    metadata = {
        "artifact": output.name,
        "sha256": sha256(output),
        "source_files": count,
        "deterministic_epoch": 0,
    }
    (output.parent / "artifact-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("ARTIFACT_BUILD=PASSED")
    print(f"ARTIFACT={output.relative_to(ROOT)}")
    print(f"SOURCE_FILES={count}")
    print(f"SHA256={metadata['sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
