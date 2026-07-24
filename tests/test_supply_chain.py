from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SupplyChainPolicyTest(unittest.TestCase):
    def test_policy_validator_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_supply_chain_policy.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("SUPPLY_CHAIN_POLICY_VALIDATION=PASSED", result.stdout)

    def test_source_artifact_is_reproducible(self) -> None:
        with tempfile.TemporaryDirectory() as temp_value:
            temp = Path(temp_value)
            source = temp / "source"
            source.mkdir()
            (source / "README.md").write_text("stable\n", encoding="utf-8")
            nested = source / "nested"
            nested.mkdir()
            script = nested / "run.sh"
            script.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            script.chmod(0o755)

            first = temp / "first.tar.gz"
            second = temp / "second.tar.gz"
            first_manifest = temp / "first.json"
            second_manifest = temp / "second.json"
            command = [sys.executable, str(ROOT / "scripts/build_source_artifact.py"), "--root", str(source)]

            first_result = subprocess.run(
                command + ["--output", str(first), "--manifest", str(first_manifest), "--baseline", "baseline"],
                text=True,
                capture_output=True,
                check=False,
            )
            second_result = subprocess.run(
                command + ["--output", str(second), "--manifest", str(second_manifest), "--baseline", "baseline"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(first_result.returncode, 0, msg=first_result.stdout + first_result.stderr)
            self.assertEqual(second_result.returncode, 0, msg=second_result.stdout + second_result.stderr)
            self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_tar_extraction_selects_only_locked_binary(self) -> None:
        module = load_module("bootstrap_verified_tool", ROOT / "scripts/bootstrap_verified_tool.py")
        with tempfile.TemporaryDirectory() as temp_value:
            temp = Path(temp_value)
            source = temp / "tool"
            source.write_text("binary", encoding="utf-8")
            archive = temp / "tool.tar.gz"
            with tarfile.open(archive, "w:gz") as bundle:
                bundle.add(source, arcname="tool")
            output = temp / "output"
            module.extract_tar_binary(archive, "tool", output)
            self.assertEqual(output.read_text(encoding="utf-8"), "binary")

    def test_evidence_records_control_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_value:
            evidence = Path(temp_value)
            for name in (
                "source.tar.gz",
                "source-manifest.json",
                "sbom.syft.json",
                "sbom.cyclonedx.json",
                "sbom.spdx.json",
                "vulnerabilities.json",
                "grype-db-status.json",
            ):
                (evidence / name).write_text("{}\n", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/build_supply_chain_evidence.py"),
                    "--directory",
                    str(evidence),
                    "--scan-exit-code",
                    "2",
                    "--database-exit-code",
                    "0",
                    "--baseline",
                    "baseline",
                    "--run-id",
                    "run",
                    "--run-attempt",
                    "1",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            status = json.loads((evidence / "scan-status.json").read_text(encoding="utf-8"))
            self.assertEqual(status["result"], "CONTROL_FAILED")
            self.assertTrue((evidence / "SHA256SUMS").is_file())
            self.assertTrue((evidence / "evidence-manifest.json").is_file())


if __name__ == "__main__":
    unittest.main()
