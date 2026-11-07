import re


def scan_output(response, system_prompt):
    """
    Layer 3: Scan the AI response for potentially
    sensitive or unsafe content.

    Returns:
        (True, None) if output passes.
        (False, reason) if suspicious output is detected.
    """

    if not isinstance(response, str):
        return False, "Invalid model response"

    # Check for verbatim system prompt leakage
    if system_prompt and system_prompt.strip():
        if system_prompt.strip() in response:
            return False, "System prompt leakage detected"

    # Check for common credential patterns
    credential_patterns = [
        r"password\s*[:=]\s*\S+",
        r"api[_-]?key\s*[:=]\s*\S+",
        r"access[_-]?token\s*[:=]\s*\S+",
        r"secret[_-]?key\s*[:=]\s*\S+",
    ]

    for pattern in credential_patterns:
        if re.search(pattern, response, re.IGNORECASE):
            return False, "Potential credential exposure detected"

    # Check for unsolicited external URLs
    url_pattern = r"https?://[^\s<>\"']+"

    if re.search(url_pattern, response, re.IGNORECASE):
        return False, "External URL detected in model output"

    return True, None
