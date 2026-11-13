from chart_meta import strip_markdown, validate


def test_strip_markdown_removes_bold_and_backticks():
    assert strip_markdown("**SQL** is the `universal` requirement") == "SQL is the universal requirement"


def test_strip_markdown_removes_links():
    assert strip_markdown("see [Census data](https://example.com) for details") == "see Census data for details"


def test_validate_reports_missing_and_extra():
    import chart_meta
    chart_meta.CHART_META = {"1_0": {"section": "S", "subsection": None, "caption": "c"}}
    missing, extra = validate(["1_0", "2_0"])
    assert missing == ["2_0"]
    assert extra == []
