import re


PII_PATTERNS = [
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",  # email
    r"\+?\d{10,15}",  # phone number
]


FORBIDDEN_PHRASES = [
    "i am",
    "i think",
    "as an ai",
    "i cannot",
    "my",
]


def contains_pii(text: str) -> bool:
    for pattern in PII_PATTERNS:
        if re.search(pattern, text):
            return True
    return False


def violates_third_person(text: str) -> bool:
    lower_text = text.lower()
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            return True
    return False


def validate_output(text: str) -> str:
    if contains_pii(text) or violates_third_person(text):
        return "He prefers not to share that information publicly."

    return text
