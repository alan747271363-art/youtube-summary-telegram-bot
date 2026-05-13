from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import re

from app.transcriber import Transcript, TranscriptSegment


@dataclass(frozen=True)
class SummarySection:
    start: float
    end: float
    title: str
    bullets: list[str]


@dataclass(frozen=True)
class StructuredSummary:
    language: str
    overview: str
    sections: list[SummarySection]
    key_takeaways: list[str]


def build_structured_summary(
    transcript: Transcript,
    max_sections: int = 8,
) -> StructuredSummary:
    if not transcript.segments:
        return StructuredSummary(
            language=transcript.language,
            overview="No speech was detected in the video.",
            sections=[],
            key_takeaways=[],
        )

    section_groups = _group_segments(transcript.segments, max_sections=max_sections)
    sections = [_summarize_group(group) for group in section_groups]
    full_text = " ".join(segment.text for segment in transcript.segments)
    overview = _first_sentence(full_text, max_chars=260)
    takeaways = _key_takeaways(transcript.segments, limit=5)
    return StructuredSummary(
        language=transcript.language,
        overview=overview,
        sections=sections,
        key_takeaways=takeaways,
    )


def render_summary(summary: StructuredSummary, title: str, source_url: str) -> str:
    lines = [
        f"Video: {title}",
        f"Source: {source_url}",
        f"Detected language: {summary.language}",
        "",
        "Overview",
        summary.overview,
    ]
    if summary.sections:
        lines.extend(["", "Timestamped summary"])
        for section in summary.sections:
            lines.append(
                f"- {format_timestamp(section.start)}-{format_timestamp(section.end)}: {section.title}"
            )
            for bullet in section.bullets:
                lines.append(f"  - {bullet}")
    if summary.key_takeaways:
        lines.extend(["", "Key takeaways"])
        lines.extend(f"- {item}" for item in summary.key_takeaways)
    return "\n".join(lines)


def chunk_message(text: str, limit: int = 3900) -> list[str]:
    chunks: list[str] = []
    remaining = text
    while len(remaining) > limit:
        split_at = remaining.rfind("\n", 0, limit)
        if split_at < limit // 2:
            split_at = limit
        chunks.append(remaining[:split_at].rstrip())
        remaining = remaining[split_at:].lstrip()
    if remaining:
        chunks.append(remaining)
    return chunks


def format_timestamp(seconds: float) -> str:
    rounded = max(0, int(seconds))
    minutes, secs = divmod(rounded, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def _group_segments(
    segments: list[TranscriptSegment],
    max_sections: int,
) -> list[list[TranscriptSegment]]:
    if len(segments) <= max_sections:
        return [[segment] for segment in segments]

    total_duration = max(segments[-1].end - segments[0].start, 1)
    target_duration = max(total_duration / max_sections, 60)
    groups: list[list[TranscriptSegment]] = []
    current: list[TranscriptSegment] = []
    group_start = segments[0].start

    for segment in segments:
        current.append(segment)
        should_close = segment.end - group_start >= target_duration
        if should_close and len(groups) < max_sections - 1:
            groups.append(current)
            current = []
            group_start = segment.end

    if current:
        groups.append(current)
    return groups


def _summarize_group(group: list[TranscriptSegment]) -> SummarySection:
    text = " ".join(segment.text for segment in group)
    sentences = _sentences(text)
    bullets = [_clean_sentence(sentence) for sentence in sentences[:2]]
    if not bullets:
        bullets = [_first_sentence(text, max_chars=180)]
    title = _title_from_text(text)
    return SummarySection(
        start=group[0].start,
        end=group[-1].end,
        title=title,
        bullets=bullets,
    )


def _sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+|(?<=[\u3002\uff01\uff1f])", text)
    return [part.strip() for part in parts if part.strip()]


def _first_sentence(text: str, max_chars: int) -> str:
    candidates = _sentences(text) or [text.strip()]
    sentence = _clean_sentence(candidates[0])
    if len(sentence) <= max_chars:
        return sentence
    return sentence[: max_chars - 1].rstrip() + "..."


def _title_from_text(text: str) -> str:
    words = _important_words(text)
    if words:
        return " / ".join(word.title() for word, _ in words[:3])
    return _first_sentence(text, max_chars=72)


def _key_takeaways(segments: list[TranscriptSegment], limit: int) -> list[str]:
    scored = sorted(
        segments,
        key=lambda segment: len(_important_words(segment.text)),
        reverse=True,
    )
    takeaways: list[str] = []
    seen: set[str] = set()
    for segment in scored:
        sentence = _first_sentence(segment.text, max_chars=180)
        normalized = sentence.lower()
        if normalized in seen:
            continue
        seen.add(normalized)
        takeaways.append(f"{format_timestamp(segment.start)} - {sentence}")
        if len(takeaways) == limit:
            break
    return takeaways


def _important_words(text: str) -> list[tuple[str, int]]:
    tokens = re.findall(r"[A-Za-z][A-Za-z0-9_-]{3,}|[\u4e00-\u9fff]{2,}", text.lower())
    stop_words = {
        "that",
        "this",
        "with",
        "from",
        "have",
        "about",
        "your",
        "they",
        "there",
        "then",
        "when",
        "what",
        "were",
        "will",
    }
    counts = Counter(token for token in tokens if token not in stop_words)
    return counts.most_common()


def _clean_sentence(sentence: str) -> str:
    return re.sub(r"\s+", " ", sentence).strip()
