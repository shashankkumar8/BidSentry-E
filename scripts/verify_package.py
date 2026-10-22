#!/usr/bin/env python3
"""Package and environment verification script for BidSentry-E."""
import hashlib
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def check_reference_hashes():
    hashes_file = ROOT / "INPUT_HASHES.txt"
    if not hashes_file.exists():
        print("ERROR: INPUT_HASHES.txt missing")
        return False
    all_ok = True
    with open(hashes_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            expected_hash, rel_path = line.split(maxsplit=1)
            target = ROOT / rel_path
            if not target.exists():
                print(f"FAIL: Missing preserved reference file: {rel_path}")
                all_ok = False
                continue
            with open(target, "rb") as pf:
                actual_hash = hashlib.sha256(pf.read()).hexdigest()
            if actual_hash != expected_hash:
                print(f"FAIL: Hash mismatch for {rel_path}")
                all_ok = False
            else:
                print(f"OK: Verified {rel_path}")
    return all_ok

def check_js_syntax():
    js_checker = ROOT / "scripts" / "check_inline_js.py"
    if js_checker.exists():
        res = subprocess.run([sys.executable, str(js_checker)], capture_output=True, text=True)
        if res.returncode != 0:
            print("FAIL: Inline JS check failed:\n", res.stderr or res.stdout)
            return False
        print("OK: Inline JS syntax verified")
    app_js = ROOT / "app" / "static" / "app.js"
    if app_js.exists():
        try:
            res = subprocess.run(["node", "--check", str(app_js)], capture_output=True, text=True)
            if res.returncode != 0:
                print("FAIL: node --check failed for app.js:\n", res.stderr)
                return False
            print("OK: app.js syntax verified with node --check")
        except FileNotFoundError:
            print("WARN: node binary not found; skipping node --check")
    return True

def check_hygiene():
    forbidden_patterns = [".env", ".bidsentry.db", "audit_logs.db", "*.pyc"]
    violations = []
    for pattern in forbidden_patterns:
        for path in ROOT.glob(pattern):
            if "node_modules" not in str(path) and ".venv" not in str(path):
                violations.append(str(path))
    if violations:
        print("WARN: Found sensitive or untracked runtime files in workspace root:", violations)
    else:
        print("OK: Workspace root is clean of sensitive runtime artifacts")
    return True

def main():
    print("=== BidSentry-E Package & Verification Suite ===")
    ok1 = check_reference_hashes()
    ok2 = check_js_syntax()
    ok3 = check_hygiene()
    if ok1 and ok2 and ok3:
        print("=== Verification SUCCESSFUL ===")
        return 0
    else:
        print("=== Verification FAILED ===")
        return 1

if __name__ == "__main__":
    sys.exit(main())
