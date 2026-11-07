import re

# ==========================================
# LAYER 1: INPUT LENGTH VALIDATION
# ==========================================

MAX_LENGTH = 500


# ==========================================
# LAYER 2: REGEX INJECTION BLOCKLIST
# ==========================================

INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"you\s+are\s+now",
    r"pretend\s+you\s+are",
    r"act\s+as\s+if\s+you\s+have\s+no",
]

# Detect long Base64-like strings (40+ characters)
BASE64_PATTERN = r"\b[A-Za-z0-9+/]{40,}={0,2}\b"


def validate_input(message):

    # Check whether input is a string
    if not isinstance(message, str):
        return False, "Invalid input format"

    # Layer 1: Check maximum input length
    if len(message) > MAX_LENGTH:
        return False, "Input exceeds maximum length of 500 characters"

    # Layer 2: Check common prompt injection phrases
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, message, re.IGNORECASE):
            return False, "Prompt injection attempt detected"

    # Check for long Base64-like encoded payloads
    if re.search(BASE64_PATTERN, message):
        return False, "Suspicious Base64 payload detected"

    # Input passed all validation checks
    return True, None
