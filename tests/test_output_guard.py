from app.guardrails.output_guard import validate_output


def test_blocks_email():
    text = "Contact him at test@example.com"
    result = validate_output(text)
    assert "sensitive" in result.lower()


def test_blocks_first_person():
    text = "I am an AI assistant."
    result = validate_output(text)
    assert "sensitive" in result.lower()


def test_allows_clean_response():
    text = "He has experience in machine learning."
    result = validate_output(text)
    assert result == text
