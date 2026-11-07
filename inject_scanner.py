import re
import sys
from pathlib import Path

# Patterns identifying hardcoded system prompts
SYSTEM_PROMPT_PATTERNS = [
    r"SYSTEM_PROMPT\s*=",
    r"SYSTEM_MESSAGE\s*=",
    r"system_message\s*=",
    r"role\s*=\s*['\"]system['\"]",
]

# Common prompt injection and jailbreak phrases
INJECTION_PHRASES = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "ignore prior instructions",
    "you are now",
    "pretend you are",
    "act as if you have no restrictions",
    "developer mode",
    "bypass safety restrictions",
    "reveal the system prompt",
]

def scan_repository(root="."):
    root = Path(root)
    findings = []

    for path in root.rglob("*.py"):

        # Do not scan this scanner or virtual environments
        if path.name == "inject_scanner.py":
            continue

        if any(part in {".git", "venv", ".venv", "__pycache__"}
               for part in path.parts):
            continue

        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        for line_number, line in enumerate(content.splitlines(), start=1):

            for pattern in SYSTEM_PROMPT_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    findings.append(
                        (path, line_number, "Hardcoded system prompt", line.strip())
                    )

            for phrase in INJECTION_PHRASES:
                if phrase.lower() in line.lower():
                    findings.append(
                        (path, line_number, "Prompt injection phrase", line.strip())
                    )

    print("\nAI Security Scanner")
    print("===================")

    if findings:
        print("\n[FAIL] Potential AI security issues detected:\n")

        for path, line, category, evidence in findings:
            print(f"File: {path}")
            print(f"Line: {line}")
            print(f"Issue: {category}")
            print(f"Evidence: {evidence}\n")

        print(f"Total findings: {len(findings)}")
        return 1

    print("[PASS] No configured AI security indicators detected.")
    return 0


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    sys.exit(scan_repository(target))
