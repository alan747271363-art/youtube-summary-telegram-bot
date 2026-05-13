from scripts.config_check import build_report


def test_config_check_hides_token_value() -> None:
    exit_code, lines = build_report({"TELEGRAM_BOT_TOKEN": "secret-token-value"})

    assert exit_code == 0
    report = "\n".join(lines)
    assert "secret-token-value" not in report
    assert "set (18 chars, value hidden)" in report


def test_config_check_allows_missing_token_for_offline_review() -> None:
    exit_code, lines = build_report({}, allow_missing_token=True)

    assert exit_code == 0
    assert "missing (allowed for offline review)" in "\n".join(lines)


def test_config_check_rejects_invalid_numeric_limits() -> None:
    exit_code, lines = build_report(
        {
            "TELEGRAM_BOT_TOKEN": "token",
            "MAX_VIDEO_SECONDS": "0",
            "MAX_SUMMARY_SECTIONS": "many",
        }
    )

    report = "\n".join(lines)
    assert exit_code == 1
    assert "MAX_VIDEO_SECONDS must be greater than 0" in report
    assert "MAX_SUMMARY_SECTIONS must be a positive integer" in report
