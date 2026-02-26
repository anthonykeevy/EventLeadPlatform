"""
Block newly introduced datetime.utcnow() usage in changed Python files.

Usage (local/CI):
  python backend/scripts/check_no_new_datetime_utcnow.py --base-ref origin/master
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def changed_python_files(base_ref: str) -> list[str]:
    rc, out, _ = run(["git", "diff", "--name-only", "--diff-filter=AM", f"{base_ref}...HEAD"])
    if rc != 0:
        rc, out, _ = run(["git", "diff", "--name-only", "--diff-filter=AM"])
        if rc != 0:
            return []
    files = [line.strip() for line in out.splitlines() if line.strip().endswith(".py")]
    return files


def added_utcnow_lines(path: str, base_ref: str) -> list[str]:
    diff_cmd = ["git", "diff", "-U0", f"{base_ref}...HEAD", "--", path]
    rc, out, _ = run(diff_cmd)
    if rc != 0:
        rc, out, _ = run(["git", "diff", "-U0", "--", path])
        if rc != 0:
            return []

    violations: list[str] = []
    new_line_no = 0

    for raw in out.splitlines():
        if raw.startswith("@@"):
            # Example: @@ -10,0 +11,2 @@
            parts = raw.split()
            plus_part = next((p for p in parts if p.startswith("+")), "")
            if plus_part:
                plus_coords = plus_part[1:].split(",")
                new_line_no = int(plus_coords[0]) - 1
            continue

        if raw.startswith("+++"):
            continue

        if raw.startswith("+"):
            new_line_no += 1
            if "datetime.utcnow(" in raw:
                violations.append(f"{path}:{new_line_no}: {raw[1:].strip()}")
            continue

        if raw.startswith(" "):
            new_line_no += 1

    return violations


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-ref", default="origin/master")
    parser.add_argument("--files", nargs="*", default=[])
    args = parser.parse_args()

    files = [str(Path(f)) for f in args.files] if args.files else changed_python_files(args.base_ref)
    if not files:
        print("No changed Python files found for utcnow guard.")
        return 0

    violations: list[str] = []
    for file_path in files:
        violations.extend(added_utcnow_lines(file_path, args.base_ref))

    if violations:
        print("Detected newly introduced datetime.utcnow() usage:")
        for line in violations:
            print(f"  - {line}")
        print("Use timezone-aware UTC (e.g., datetime.now(datetime.UTC)) for new code.")
        return 1

    print("No newly introduced datetime.utcnow() usage detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
