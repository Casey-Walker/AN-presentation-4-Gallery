import re

# The `style(fig, ...)` call's arguments may wrap onto continuation lines
# (indented), but must never cross into a new, unindented top-level
# statement -- that's how two separate charts in one cell (a style() call
# for the first, then a fresh `fig = ...` for the second) stay separate
# instead of being swallowed into one invalid expression. A leading
# negative lookbehind keeps `subfig.show()` / `fig2.show()` from matching
# as a substring of a different variable's name.
_SHOW_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_])"
    r"(style\(fig\b(?:[^\n]|\n[ \t]+)*?\)|fig\b)"
    r"\.show\(\)"
)


def transform_cell_source(source: str, cell_index: int) -> tuple[str, int]:
    occurrence = [0]

    def _replace(match: "re.Match[str]") -> str:
        expr = match.group(1)
        chart_id = f"{cell_index}_{occurrence[0]}"
        occurrence[0] += 1
        return f'_export({expr}, "{chart_id}")'

    new_source = _SHOW_PATTERN.sub(_replace, source)
    return new_source, occurrence[0]
