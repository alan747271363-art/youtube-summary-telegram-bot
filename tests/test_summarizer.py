from app.summarizer import build_structured_summary, format_timestamp, render_summary
from app.transcriber import Transcript, TranscriptSegment


def test_format_timestamp() -> None:
    assert format_timestamp(65.4) == "1:05"
    assert format_timestamp(3661) == "1:01:01"


def test_builds_summary_with_chinese_text() -> None:
    transcript = Transcript(
        language="zh",
        segments=[
            TranscriptSegment(0, 10, "\u4eca\u5929\u6211\u4eec\u8ba8\u8bba\u4eba\u5de5\u667a\u80fd\u4ee3\u7406\u3002"),
            TranscriptSegment(10, 25, "\u7b2c\u4e00\u4e2a\u8981\u70b9\u662f\u5de5\u5177\u8c03\u7528\u548c\u98ce\u9669\u63a7\u5236\u3002"),
        ],
    )
    summary = build_structured_summary(transcript, max_sections=2)
    rendered = render_summary(summary, "demo", "https://youtu.be/demo")

    assert summary.language == "zh"
    assert "\u4eba\u5de5\u667a\u80fd" in rendered
    assert "0:00-0:10" in rendered


def test_empty_transcript_is_handled() -> None:
    summary = build_structured_summary(Transcript(language="en", segments=[]))
    assert summary.overview == "No speech was detected in the video."
    assert summary.sections == []
