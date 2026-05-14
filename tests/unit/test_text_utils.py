"""Unit tests for text utilities."""

from taskforge.utils.text_utils import truncate_text, slugify


def test_truncate_text_short():
    """Test truncating short text."""
    result = truncate_text("Short text")
    assert result == "Short text"


def test_truncate_text_long():
    """Test truncating long text."""
    long_text = "This is a very long text that should be truncated"
    result = truncate_text(long_text, 20)
    assert result == "This is a very lo..."


def test_truncate_text_exact():
    """Test truncating text at exact length."""
    text = "Exactly 10 chars"
    result = truncate_text(text, 10)
    assert result == "Exactly 10 chars"


def test_slugify_simple():
    """Test slugifying simple text."""
    result = slugify("Hello World")
    assert result == "hello-world"


def test_slugify_special_chars():
    """Test slugifying text with special characters."""
    result = slugify("Hello, World! How are you?")
    assert result == "hello-world-how-are-you"


def test_slugify_multiple_spaces():
    """Test slugifying text with multiple spaces."""
    result = slugify("Hello   World")
    assert result == "hello-world"


def test_slugify_empty():
    """Test slugifying empty string."""
    result = slugify("")
    assert result == ""