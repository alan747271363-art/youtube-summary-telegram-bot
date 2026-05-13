from __future__ import annotations

from app.summarizer import build_structured_summary, render_summary
from app.transcriber import Transcript, TranscriptSegment


def build_demo_outputs() -> list[tuple[str, str]]:
    demos = [
        (
            "English demo",
            Transcript(
                language="en",
                segments=[
                    TranscriptSegment(
                        0,
                        18,
                        "This video explains how a Telegram bot receives a YouTube link.",
                    ),
                    TranscriptSegment(
                        18,
                        44,
                        "The bot downloads audio, transcribes it with Whisper, and builds a "
                        "timestamped summary for the user.",
                    ),
                    TranscriptSegment(
                        44,
                        70,
                        "The Railway deployment keeps secrets outside the repository and uses "
                        "environment variables for the Telegram token.",
                    ),
                ],
            ),
        ),
        (
            "Chinese demo",
            Transcript(
                language="zh",
                segments=[
                    TranscriptSegment(0, 14, "这个视频介绍如何把 YouTube 链接发送给 Telegram 机器人。"),
                    TranscriptSegment(14, 36, "机器人会下载音频，使用 Whisper 转写，然后生成带时间戳的摘要。"),
                    TranscriptSegment(36, 58, "部署到 Railway 时，Telegram token 只放在环境变量里，不写进代码仓库。"),
                ],
            ),
        ),
    ]

    outputs: list[tuple[str, str]] = []
    for title, transcript in demos:
        summary = build_structured_summary(transcript, max_sections=3)
        rendered = render_summary(summary, title, "https://youtu.be/demo")
        outputs.append((title, rendered))
    return outputs


def main() -> None:
    for _, rendered in build_demo_outputs():
        print("=" * 72)
        print(rendered)


if __name__ == "__main__":
    main()
