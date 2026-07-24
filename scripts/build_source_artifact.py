#!/usr/bin/env python3
"""Build a deterministic source archive and file-integrity manifest."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import stat
import sys
import tarfile
from pathlib import Path

DEFAULT_EXCLUDED_PREFIXES = {
    ".git",
    ".tools",
    ".evidence",
    ".pytest_cache",
}
EXCLUDED_NAMES = {".DS_Store"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--baseline", default=os.environ.get("GITHUB_SHA", "UNKNOWN"))
    return parser.parse_args()


def digest_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while chunk := source.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def excluded(relative: Path) -> bool:
    if not relative.parts:
        return False
    if relative.parts[0] in DEFAULT_EXCLUDED_PREFIXES:
        return True
    if "__pycache__" in relative.parts:
        return True
    if relative.name in EXCLUDED_NAMES or relative.suffix == ".pyc":
        return True
    return False


def collect_files(root: Path, output: Path, manifest: Path) -> list[Path]:
    files: list[Path] = []
    protected = {output.resolve(), manifest.resolve()}
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if excluded(relative):
            continue
        if path.is_symlink():
            raise ValueError(f"symbolic links are not permitted in deterministic source artifacts: {relative}")
        if path.is_file() and path.resolve() not in protected:
            files.append(path)
    return sorted(files, key=lambda item: item.relative_to(root).as_posix())


def normalized_mode(path: Path) -> int:
    source_mode = stat.S_IMODE(path.stat().st_mode)
    return 0o755 if source_mode & 0o111 else 0o644


def build_archive(root: Path, output: Path, files: list[Path]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    with temporary.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0, compresslevel=9) as compressed:
            with tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as archive:
                for path in files:
                    relative = path.relative_to(root).as_posix()
                    info = tarfile.TarInfo(name=relative)
                    info.size = path.stat().st_size
                    info.mode = normalized_mode(path)
                    info.uid = 0
                    info.gid = 0
                    info.uname = "root"
                    info.gname = "root"
                    info.mtime = 0
                    with path.open("rb") as source:
                        archive.addfile(info, source)
    os.replace(temporary, output)


def write_manifest(root: Path, output: Path, manifest: Path, baseline: str, files: list[Path]) -> None:
    records = []
    for path in files:
        records.append(
            {
                "path": path.relative_to(root).as_posix(),
                "sha256": digest_file(path),
                "size": path.stat().st_size,
                "mode": oct(normalized_mode(path)),
            }
        )
    document = {
        "schema_version": 1,
        "baseline": baseline,
        "artifact": {
            "path": output.name,
            "format": "tar.gz",
            "sha256": digest_file(output),
            "size": output.stat().st_size,
            "deterministic": True,
        },
        "files": records,
    }
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    output = args.output.resolve()
    manifest = args.manifest.resolve()
    if not root.is_dir():
        print(f"ERROR: root is not a directory: {root}", file=sys.stderr)
        return 2
    try:
        files = collect_files(root, output, manifest)
        if not files:
            raise ValueError("source artifact would be empty")
        build_archive(root, output, files)
        write_manifest(root, output, manifest, args.baseline, files)
    except (OSError, ValueError, tarfile.TarError) as exc:
        print(f"ERROR: unable to build deterministic source artifact: {exc}", file=sys.stderr)
        return 1

    print("SOURCE_ARTIFACT=PASSED")
    print(f"FILES={len(files)}")
    print(f"SHA256={digest_file(output)}")
    print(f"OUTPUT={output}")
    print(f"MANIFEST={manifest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
