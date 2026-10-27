#!/usr/bin/env python3
"""Check the fictional fixtures offline, including their expected review blocks."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ("demo-drama", "office-comedy-test")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_check(arguments: list[str], expected_code: int) -> None:
    result = subprocess.run([sys.executable, *arguments], cwd=ROOT, text=True,
                            encoding="utf-8", errors="replace", capture_output=True)
    if result.stdout:
        print(result.stdout.strip())
    if result.returncode != expected_code:
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        raise ValueError(f"Unexpected exit {result.returncode}, expected {expected_code}: {arguments[0]}")


def main() -> int:
    try:
        for name in PROJECTS:
            relative = f"projects/{name}"
            project = ROOT / relative
            episode = project / "episodes" / "ep01"
            if read_json(project / "project.json").get("status") != "synthetic_demo":
                raise ValueError(f"{name}: missing synthetic fixture marker")
            if read_json(project / "assets.json") or read_json(project / "cost.json"):
                raise ValueError(f"{name}: public fixture must not contain real media or spend records")
            tasks = read_json(episode / "tasks.json")
            if not tasks or any(task.get("status") != "pending" for task in tasks):
                raise ValueError(f"{name}: fixture tasks must be pending")
            prompts = read_json(episode / "prompts" / "prompt_index.json")
            if not prompts or any(prompt.get("review_status") != "pending" for prompt in prompts):
                raise ValueError(f"{name}: fixture must not represent a production prompt approval")

            run_check(["scripts/validate_all.py", relative], 0)
            run_check(["scripts/check_generation_readiness.py", relative, "--episode", "ep01",
                       "--task-type", "image_generation", "--require-prompt-review"], 1)
            readiness = read_json(episode / "reports" / "generation_readiness_image_generation.json")
            if readiness.get("result") != "Blocked" or not readiness.get("checked_tasks"):
                raise ValueError(f"{name}: expected a checked and blocked image task")
            if not any("reviewer has not passed" in finding.get("issue", "")
                       for finding in readiness.get("findings", [])):
                raise ValueError(f"{name}: expected missing-review evidence")

            run_check(["scripts/generate_gate_report.py", relative, "--episode", "ep01",
                       "--stage", "public_synthetic_demo"], 1)
            gate = read_json(episode / "reports" / "production_gate_report.json")
            if gate.get("Production Gate Result") != "Blocked":
                raise ValueError(f"{name}: synthetic fixture must remain blocked for production")
        print("Public example checks passed: two fictional fixtures; expected production blocks preserved.")
        return 0
    except (OSError, ValueError) as exc:
        print(f"Public example check failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
