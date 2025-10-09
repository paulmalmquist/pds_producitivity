"""Chart selection heuristics."""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

ChartChoice = Tuple[str, Dict[str, str]]


def _infer_types(rows: List[Dict[str, object]]) -> Dict[str, str]:
    if not rows:
        return {}
    sample = rows[0]
    types: Dict[str, str] = {}
    for key, value in sample.items():
        if isinstance(value, (int, float)):
            types[key] = "numeric"
        elif hasattr(value, "isoformat"):
            types[key] = "datetime"
        else:
            types[key] = "categorical"
    return types


def select_chart(rows: List[Dict[str, object]], preference: str = "auto") -> Optional[ChartChoice]:
    if not rows:
        return None
    inferred = _infer_types(rows)
    numeric_fields = [col for col, typ in inferred.items() if typ == "numeric"]
    datetime_fields = [col for col, typ in inferred.items() if typ == "datetime"]
    categorical_fields = [col for col, typ in inferred.items() if typ == "categorical"]

    def build(choice: str, x: str, y: Optional[str] = None, group: Optional[str] = None, note: Optional[str] = None) -> ChartChoice:
        spec = {"x": x}
        if y:
            spec["y"] = y
        if group:
            spec["group"] = group
        if note:
            spec["note"] = note
        return choice, spec

    if preference != "auto":
        if preference == "line" and datetime_fields and numeric_fields:
            return build("line", datetime_fields[0], numeric_fields[0])
        if preference == "bar" and categorical_fields and numeric_fields:
            return build("bar", categorical_fields[0], numeric_fields[0])
        if preference == "pie" and categorical_fields and numeric_fields:
            return build("pie", categorical_fields[0], numeric_fields[0])
        if preference == "scatter" and len(numeric_fields) >= 2:
            return build("scatter", numeric_fields[0], numeric_fields[1], categorical_fields[0] if categorical_fields else None)
        if preference == "kpi" and numeric_fields:
            return build("kpi", numeric_fields[0])

    if datetime_fields and numeric_fields:
        return build("line", datetime_fields[0], numeric_fields[0])
    if categorical_fields and numeric_fields:
        category = categorical_fields[0]
        note = None
        if len({row[category] for row in rows}) > 25:
            note = "Showing top categories by metric"
        return build("bar", category, numeric_fields[0], note=note)
    if len(numeric_fields) >= 2 and categorical_fields:
        return build("scatter", numeric_fields[0], numeric_fields[1], categorical_fields[0])
    if numeric_fields:
        return build("kpi", numeric_fields[0])
    return None


__all__ = ["select_chart"]
