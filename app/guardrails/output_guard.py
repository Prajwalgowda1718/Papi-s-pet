import re

SENSITIVE_OUTPUT = [
    r"\b\d{10}\b",
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    r"contact number",
    r"personal email",
    r"address"
]


def is_sensitive_output(text: str) -> bool:

    text_lower = text.lower()

    for pattern in SENSITIVE_OUTPUT:
        if re.search(pattern, text_lower):
            return True

    return False
