import re

_SHOW_PATTERN = re.compile(r"(style\(fig[^\n]*?\)|fig)\.show\(\)")


def transform_cell_source(source: str, cell_index: int) -> tuple[str, int]:
    occurrence = [0]

    def _replace(match: "re.Match[str]") -> str:
        expr = match.group(1)
        chart_id = f"{cell_index}_{occurrence[0]}"
        occurrence[0] += 1
        return f'_export({expr}, "{chart_id}")'

    new_source = _SHOW_PATTERN.sub(_replace, source)
    return new_source, occurrence[0]
