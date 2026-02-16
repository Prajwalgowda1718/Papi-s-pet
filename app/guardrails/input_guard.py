import re
from app.utils.fallbacks import malicious_query


SUSPICIOUS_PATTERNS = [
    r"ignore previous instructions",
    r"disregard the rules",
    r"reveal .* private",
    r"system prompt",
    r"act as",
    r"pretend to be",
    r"override",
    r"bypass",
    r"circumvent",
    r"disable security"
]


def is_malicious(query: str) -> bool:
    query_lower = query.lower()

    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, query_lower):
            return True

    return False


def handle_malicious():
    return malicious_query()
