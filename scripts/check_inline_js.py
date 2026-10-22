"""Check inline JavaScript snippets in app/static/workbench.html with Node's parser."""
from __future__ import annotations
import re
import subprocess
import tempfile
from pathlib import Path

page = Path(__file__).resolve().parents[1] / "app" / "static" / "workbench.html"
text = page.read_text(encoding="utf-8")
scripts = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", text, flags=re.I | re.S)
if not scripts:
    raise SystemExit("No inline JavaScript blocks found")
for i, block in enumerate(scripts, 1):
    with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as f:
        f.write(block)
        temp = Path(f.name)
    result = subprocess.run(["node", "--check", str(temp)], text=True, capture_output=True)
    temp.unlink(missing_ok=True)
    if result.returncode:
        print(result.stdout, end="")
        print(result.stderr, end="")
        raise SystemExit(f"Inline script {i} failed Node syntax check")
print(f"PASS: {len(scripts)} inline JavaScript block(s) parsed by node --check")
