#!/usr/bin/env python3
"""Write a markdown diff between two prompt versions."""

from __future__ import annotations

import difflib
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 4:
        print("Usage: compare_prompts.py <old_prompt.md> <new_prompt.md> <out.md>")
        return 2
    old_path = Path(sys.argv[1]).resolve()
    new_path = Path(sys.argv[2]).resolve()
    out_path = Path(sys.argv[3]).resolve()
    old_lines = old_path.read_text(encoding="utf-8").splitlines()
    new_lines = new_path.read_text(encoding="utf-8").splitlines()
    diff = difflib.unified_diff(old_lines, new_lines, fromfile=str(old_path), tofile=str(new_path), lineterm="")
    body = "\n".join(diff)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(f"# Prompt Diff\n\n```diff\n{body}\n```\n", encoding="utf-8")
    print(f"Wrote prompt diff: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
