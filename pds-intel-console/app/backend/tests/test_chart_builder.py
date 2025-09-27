from utils.chart_builder import suggest_chart


def test_time_series_prefers_line():
    chart = suggest_chart(['month', 'value'], [['2024-01', 100], ['2024-02', 120]], {'isTimeSeries': True})
    assert chart == 'line'


def test_large_category_prefers_horizontal():
    rows = [[f'Item {i}', i] for i in range(25)]
    chart = suggest_chart(['label', 'value'], rows)
    assert chart == 'horizontalBar'
