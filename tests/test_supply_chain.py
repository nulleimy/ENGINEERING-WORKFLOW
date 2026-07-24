from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SupplyChainTest(unittest.TestCase):
    def test_static_supply_chain_validator_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_supply_chain.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("SUPPLY_CHAIN_VALIDATION=PASSED", result.stdout)

    def test_reference_artifact_is_reproducible(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "first.tar.gz"
            second = Path(tmp) / "second.tar.gz"
            subprocess.run(
                [sys.executable, str(ROOT / "scripts/build_reference_artifact.py"), "--output", str(first.relative_to(ROOT) if first.is_relative_to(ROOT) else first), "--manifest", str(Path(tmp) / "first.sha")],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [sys.executable, str(ROOT / "scripts/build_reference_artifact.py"), "--output", str(second.relative_to(ROOT) if second.is_relative_to(ROOT) else second), "--manifest", str(Path(tmp) / "second.sha")],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(hashlib.sha256(first.read_bytes()).hexdigest(), hashlib.sha256(second.read_bytes()).hexdigest())

    def test_policy_blocks_high_critical_and_unknown(self) -> None:
        policy = json.loads((ROOT / "supply-chain/policy.json").read_text(encoding="utf-8"))
        self.assertEqual(set(policy["vulnerability"]["blocking_severities"]), {"critical", "high", "unknown"})
        self.assertFalse(policy["authority"]["pull_request_signing_allowed"])
        self.assertFalse(policy["vulnerability"]["vex"]["ai_may_accept"])


if __name__ == "__main__":
    unittest.main()
