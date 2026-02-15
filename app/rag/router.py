def detect_target_section(query: str) -> str | None:
    query_lower = query.lower()

    if any(word in query_lower for word in ["cgpa", "degree", "education", "graduation", "university", "college"]):
        return "education"

    if any(word in query_lower for word in ["skill", "language", "framework", "technology", "library", "tool", "proficient", "familiar"]):
        return "skills"

    if any(word in query_lower for word in ["project", "built", "developed", "created", "implemented", "worked on"]):
        return "projects"

    if any(word in query_lower for word in ["experience", "internship", "job", "work", "employed", "company", "role"]):
        return "experience"

    return None
