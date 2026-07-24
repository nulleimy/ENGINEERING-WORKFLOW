from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ToolchainLockTest(unittest.TestCase):
    def test_toolchain_validator_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_toolchain_lock.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("TOOLCHAIN_VALIDATION=PASSED", result.stdout)
        self.assertIn("TOOLS=15", result.stdout)
        self.assertIn("ACTIVE=8", result.stdout)
        self.assertIn("CONFIGURED=1", result.stdout)
        self.assertIn("SELECTED=4", result.stdout)
        self.assertIn("EVALUATE=1", result.stdout)
        self.assertIn("DEFERRED=1", result.stdout)
        self.assertIn("UNVERIFIED_EXECUTION_ALLOWED=false", result.stdout)

    def test_policy_input_builder_is_deterministic_json(self) -> None:
        first = subprocess.run(
            [sys.executable, str(ROOT / "scripts/build_policy_input.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        ).stdout
        second = subprocess.run(
            [sys.executable, str(ROOT / "scripts/build_policy_input.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        ).stdout
        self.assertEqual(first, second)
        payload = json.loads(first)
        self.assertEqual(set(payload), {"gap_register", "scorecard", "toolchain"})

    def test_bootstrap_refuses_non_active_binary_without_network(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "conftest"
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/bootstrap_verified_tool.py"),
                    "conftest",
                    "--platform",
                    "linux-amd64",
                    "--output",
                    str(output),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("not an active binary", result.stderr)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
