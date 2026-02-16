import re
from app.utils.fallbacks import sensitive_information


SENSITIVE_PATTERNS = [
    r"\b\d{10}\b",
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    r"address",
    r"personal email",
]


def filter_sensitive_docs(docs):
    safe_docs = []

    for doc in docs:
        flagged = False

        text = doc.page_content if hasattr(doc, "page_content") else doc

        for pattern in SENSITIVE_PATTERNS:
            if re.search(pattern, text.lower()):
                flagged = True
                break

        if not flagged:
            safe_docs.append(doc)

    return safe_docs
