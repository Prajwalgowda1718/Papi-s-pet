def out_of_scope():
    return (
        "This assistant provides information only about Prajwal K Madegowda. "
        "Please ask questions related to his professional background, skills, or experience."
    )


def sensitive_information():
    return (
        "Certain personal or sensitive information is not shared publicly."
    )


def service_unavailable():
    return (
        "The service is temporarily unavailable. Please try again later."
    )


def malicious_query():
    return (
        "The request appears to violate system guidelines. "
        "Please ask a professional question related to Prajwal's background."
    )
