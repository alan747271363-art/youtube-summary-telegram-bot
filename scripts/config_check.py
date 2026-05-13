from __future__ import annotations

import argparse
from collections.abc import Mapping
import os


OPTIONAL_DEFAULTS = {
    "WHISPER_MODEL": "small",
    "WHISPER_DEVICE": "cpu",
    "WHISPER_COMPUTE_TYPE": "int8",
    "MAX_VIDEO_SECONDS": "3600",
    "MAX_SUMMARY_SECTIONS": "8",
    "DOWNLOAD_DIR": "downloads",
}

POSITIVE_INTEGER_VARS = ("MAX_VIDEO_SECONDS", "MAX_SUMMARY_SECTIONS")


def _is_set(value: str | None) -> bool:
    return bool(value and value.strip())


def build_report(
    env: Mapping[str, str],
    *,
    allow_missing_token: bool = False,
) -> tuple[int, list[str]]:
    lines = ["Configuration check"]
    exit_code = 0

    token = env.get("TELEGRAM_BOT_TOKEN")
    if _is_set(token):
        lines.append(f"- TELEGRAM_BOT_TOKEN: set ({len(token.strip())} chars, value hidden)")
    elif allow_missing_token:
        lines.append("- TELEGRAM_BOT_TOKEN: missing (allowed for offline review)")
    else:
        lines.append("- TELEGRAM_BOT_TOKEN: missing (required for live Telegram bot)")
        exit_code = 1

    for name, default in OPTIONAL_DEFAULTS.items():
        value = env.get(name, default).strip() if env.get(name) is not None else default
        source = "env" if name in env else "default"
        lines.append(f"- {name}: {value} ({source})")

    for name in POSITIVE_INTEGER_VARS:
        value = env.get(name, OPTIONAL_DEFAULTS[name]).strip()
        try:
            parsed = int(value)
        except ValueError:
            lines.append(f"- ERROR: {name} must be a positive integer, got {value!r}")
            exit_code = 1
            continue
        if parsed <= 0:
            lines.append(f"- ERROR: {name} must be greater than 0, got {parsed}")
            exit_code = 1

    if exit_code == 0:
        lines.append("Result: ready for offline review or live deployment.")
    else:
        lines.append("Result: configuration needs attention before live deployment.")

    return exit_code, lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate bot environment variables.")
    parser.add_argument(
        "--allow-missing-token",
        action="store_true",
        help="Do not fail when TELEGRAM_BOT_TOKEN is missing; useful for reviewer smoke checks.",
    )
    args = parser.parse_args()

    exit_code, lines = build_report(os.environ, allow_missing_token=args.allow_missing_token)
    print("\n".join(lines))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
