from app.viz.selector import select_chart


def test_line_chart_detected():
    rows = [
        {"date": "2024-01-01", "value": 10.0},
        {"date": "2024-01-02", "value": 12.0},
    ]
    chart = select_chart(rows)
    assert chart is not None
    chart_type, spec = chart
    assert chart_type == "line"
    assert spec["x"] == "date"
    assert spec["y"] == "value"


def test_kpi_when_single_numeric():
    rows = [{"total": 42}]
    chart = select_chart(rows)
    assert chart is not None
    chart_type, spec = chart
    assert chart_type == "kpi"
    assert spec["x"] == "total"
