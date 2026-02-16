import re


SENSITIVE_PATTERNS = [
    r"\b\d{10}\b",                  # phone numbers
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",  # emails
    r"address",
    r"number",
    r"personal email"
]


def filter_sensitive_docs(docs: list[str]) -> list[str]:
    safe_docs = []

    for doc in docs:
        flagged = False

        for pattern in SENSITIVE_PATTERNS:
            if re.search(pattern, doc.lower()):
                flagged = True
                break

        if not flagged:
            safe_docs.append(doc)

    return safe_docs
