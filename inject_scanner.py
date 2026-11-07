import re
import sys
from pathlib import Path

# AI-specific prompt injection indicators
PATTERNS = {
    "Instruction override": r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions",
    "System prompt disclosure": r"(reveal|print|show|expose)\s+(the\s+)?(system|internal)\s+prompt",
    "Developer mode activation": r"developer\s+mode",
    "Safety bypass": r"(bypass|disable|ignore)\s+(all\s+)?(safety|security)\s+(rules|filters|restrictions)",
    "Jailbreak indicator": r"\bjailbreak\b",
}

def scan_file(file_path):
    path = Path(file_path)

    if not path.is_file():
        print(f"[ERROR] File not found: {file_path}")
        return 2

    content = path.read_text(encoding="utf-8", errors="replace")
    findings = []

    for line_number, line in enumerate(content.splitlines(), start=1):
        for name, pattern in PATTERNS.items():
            if re.search(pattern, line, re.IGNORECASE):
                findings.append((line_number, name, line.strip()))

    print(f"\nScanning: {path}")

    if findings:
        print("\n[FAIL] Potential AI prompt security issues detected:\n")

        for line_number, name, line in findings:
            print(f"Line {line_number}: {name}")
            print(f"  Evidence: {line}")

        print(f"\nTotal findings: {len(findings)}")
        return 1

    print("[PASS] No configured prompt injection indicators detected.")
    return 0


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "app.py"
    sys.exit(scan_file(target))
