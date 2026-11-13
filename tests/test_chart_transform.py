from chart_transform import transform_cell_source


def test_single_chained_show():
    src = (
        "fig = px.bar(missing[missing['% Missing'] > 0], x='% Missing', y='Column')\n"
        "style(fig, height=450, yaxis={'categoryorder': 'total ascending'}, "
        "coloraxis_showscale=False).show()\n"
    )
    new_src, n = transform_cell_source(src, cell_index=3)
    assert n == 1
    assert '_export(style(fig, height=450, yaxis={\'categoryorder\': \'total ascending\'}, coloraxis_showscale=False), "3_0")' in new_src
    assert ".show()" not in new_src


def test_multiple_show_same_cell_get_unique_ids():
    src = (
        "fig = px.bar(skill_share.sort_values('Share (%)'), x='Share (%)', y='Skill')\n"
        "style(fig, height=520, coloraxis_showscale=False).show()\n"
        "\n"
        "fig = px.histogram(df.dropna(subset=['years_required']), x='years_required', nbins=15)\n"
        "style(fig, bargap=0.08).show()\n"
    )
    new_src, n = transform_cell_source(src, cell_index=13)
    assert n == 2
    assert '"13_0"' in new_src
    assert '"13_1"' in new_src


def test_standalone_show_after_separate_style_call():
    src = (
        "style(fig, height=600, title_text='Executive Summary Dashboard')\n"
        "fig.show()\n"
    )
    new_src, n = transform_cell_source(src, cell_index=50)
    assert n == 1
    assert '_export(fig, "50_0")' in new_src
    assert ".show()" not in new_src


def test_no_show_call_is_unchanged():
    src = "df['cluster'] = kmeans.labels_\n"
    new_src, n = transform_cell_source(src, cell_index=24)
    assert n == 0
    assert new_src == src
