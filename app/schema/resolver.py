"""Schema resolver utilities for mapping user terms."""
from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

from app.schema.unity import Table, get_synonyms


def resolve_synonyms(question: str) -> Dict[str, str]:
    synonyms = get_synonyms()
    matched: Dict[str, str] = {}
    for alias, canonical in synonyms.items():
        if alias.lower() in question.lower():
            matched[alias] = canonical
    return matched


def surface_relevant_columns(question: str, tables: Iterable[Table]) -> List[Tuple[str, str]]:
    question_lower = question.lower()
    results: List[Tuple[str, str]] = []
    for table in tables:
        for column in table.columns:
            if column.name.lower() in question_lower:
                results.append((table.full_name, column.name))
    return results


__all__ = ["resolve_synonyms", "surface_relevant_columns"]
