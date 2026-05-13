from app.youtube import extract_youtube_url, is_youtube_url


def test_extracts_youtube_url_from_message() -> None:
    text = "Please summarize https://www.youtube.com/watch?v=dQw4w9WgXcQ thanks"
    assert extract_youtube_url(text) == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


def test_accepts_short_youtube_url() -> None:
    assert is_youtube_url("https://youtu.be/dQw4w9WgXcQ")


def test_rejects_non_youtube_url() -> None:
    assert extract_youtube_url("https://example.com/watch?v=dQw4w9WgXcQ") is None
