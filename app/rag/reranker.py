PRIORITY_SECTIONS = [
    "skills",
    "projects",
    "experience",
    "education"
]


def rerank_documents(documents):
    """
    documents: list of LangChain Document objects
    """

    def score(doc):
        section = doc.metadata.get("section", "")
        if section in PRIORITY_SECTIONS:
            return 1
        return 0

    # Sort: priority sections first
    return sorted(documents, key=score, reverse=True)
