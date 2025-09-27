def suggest_chart(columns, rows, viz_hints=None):
    viz_hints = viz_hints or {}
    if viz_hints.get('chartType'):
        return viz_hints['chartType']
    if viz_hints.get('isTimeSeries'):
        return 'line'

    values = [float(row[1]) for row in rows if len(row) > 1]
    total = sum(values) if values else 0
    percent_like = viz_hints.get('percentLike', abs(total - 100) < 5)
    if percent_like:
        return 'doughnut'

    if len(rows) < 15:
        return 'bar'
    return 'horizontalBar'
