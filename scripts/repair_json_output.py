#!/usr/bin/env python3
"""Repair common malformed JSON output from LLM workflows."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def strip_fences(text: str) -> str:
    text = text.strip()
    fence = re.compile(r"^```(?:json)?\s*(.*?)\s*```$", re.DOTALL)
    match = fence.match(text)
    return match.group(1).strip() if match else text


def extract_candidate(text: str) -> str:
    text = strip_fences(text)
    start_positions = [i for i in [text.find("{"), text.find("[")] if i >= 0]
    if not start_positions:
        return text
    start = min(start_positions)
    end = max(text.rfind("}"), text.rfind("]"))
    return text[start:end + 1] if end >= start else text[start:]


def normalize(text: str) -> str:
    text = extract_candidate(text)
    text = text.replace("\ufeff", "")
    text = re.sub(r",\s*([}\]])", r"\1", text)
    return text.strip()


def main() -> int:
    if len(sys.argv) not in {2, 3}:
        print("Usage: repair_json_output.py <input_file> [output_file]")
        return 2
    input_path = Path(sys.argv[1]).resolve()
    output_path = Path(sys.argv[2]).resolve() if len(sys.argv) == 3 else input_path.with_suffix(".repaired.json")
    raw = input_path.read_text(encoding="utf-8")
    candidate = normalize(raw)
    try:
        data = json.loads(candidate)
    except json.JSONDecodeError as exc:
        data = {"repair_failed": True, "reason": str(exc), "raw_excerpt": raw[:1000]}
        output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Repair failed: {output_path}")
        return 1
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Repaired JSON: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
