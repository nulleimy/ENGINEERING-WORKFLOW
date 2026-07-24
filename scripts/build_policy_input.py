#!/usr/bin/env python3
"""Build a deterministic OPA input document from canonical repository records."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> object:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    payload = {
        "scorecard": load("readiness/domain-scorecard.json"),
        "gap_register": load("readiness/gap-register.json"),
        "toolchain": load("platform/toolchain.lock.json"),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
