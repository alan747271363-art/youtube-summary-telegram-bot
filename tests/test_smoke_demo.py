from scripts.smoke_demo import build_demo_outputs


def test_smoke_demo_includes_readable_chinese_output() -> None:
    rendered_outputs = dict(build_demo_outputs())

    assert "Chinese demo" in rendered_outputs
    assert "这个视频介绍" in rendered_outputs["Chinese demo"]
    assert "Telegram token" in rendered_outputs["Chinese demo"]
    assert "杩欎釜" not in rendered_outputs["Chinese demo"]


def test_smoke_demo_includes_english_output() -> None:
    rendered_outputs = dict(build_demo_outputs())

    assert "English demo" in rendered_outputs
    assert "Telegram bot receives a YouTube link" in rendered_outputs["English demo"]
