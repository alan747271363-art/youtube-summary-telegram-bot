from app.summarizer import chunk_message


def test_chunk_message_splits_long_text() -> None:
    chunks = chunk_message("a\n" * 5000, limit=1000)
    assert len(chunks) > 1
    assert all(len(chunk) <= 1000 for chunk in chunks)
