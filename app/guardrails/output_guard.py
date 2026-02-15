import re


PII_PATTERNS = [
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",  # email
    r"\+?\d{10,15}",  # phone number
]


FORBIDDEN_PATTERNS = [
    r"\bi am\b",
    r"\bi think\b",
    r"\bas an ai\b",
    r"\bi cannot\b",
    r"\bmy\b",
    
]


def contains_pii(text: str) -> bool:
    for pattern in PII_PATTERNS:
        if re.search(pattern, text):
            return True
    return False


def violates_third_person(text: str) -> bool:
    lower_text = text.lower()

    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, lower_text):
            return True

    return False


def validate_output(text: str) -> str:
    if contains_pii(text) or violates_third_person(text):
        return "He prefers not to share that information publicly."

    return text
