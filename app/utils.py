"""Utility helpers for logging, caching, and formatting."""
from __future__ import annotations

import base64
import json
import logging
from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Tuple

from fastapi import Request

from app.config import get_settings

logger = logging.getLogger("nl2sql")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


class TTLCache:
    """A minimal in-memory TTL cache suitable for small datasets."""

    def __init__(self, ttl_seconds: int) -> None:
        self.ttl = timedelta(seconds=ttl_seconds)
        self._store: Dict[str, Tuple[datetime, Any]] = {}

    def get(self, key: str) -> Optional[Any]:
        record = self._store.get(key)
        if not record:
            return None
        ts, value = record
        if datetime.utcnow() - ts > self.ttl:
            self._store.pop(key, None)
            return None
        return value

    def set(self, key: str, value: Any) -> None:
        self._store[key] = (datetime.utcnow(), value)

    def clear(self) -> None:
        self._store.clear()


_settings = get_settings()
question_cache = TTLCache(ttl_seconds=_settings.question_cache_ttl_seconds)


def cache_with_ttl(cache: TTLCache) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True, default=str)
            cached = cache.get(key)
            if cached is not None:
                return cached
            result = func(*args, **kwargs)
            cache.set(key, result)
            return result

        return wrapper

    return decorator


def encode_plot(fig) -> str:
    buffer = BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")


def ensure_feedback_file(path: str) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.touch()
    return target


def log_feedback_event(path: str, event: Dict[str, Any]) -> None:
    ensure_feedback_file(path)
    with Path(path).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event) + "\n")


def log_ask_event(event: Dict[str, Any]) -> None:
    logger.info("ask_event", extra=event)


def summarize_rows(rows: list[dict[str, Any]], max_rows: int) -> list[dict[str, Any]]:
    return rows[:max_rows]


def format_answer_summary(question: str, rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "No rows were returned. Consider adjusting your filters."
    sample = rows[0]
    fields = ", ".join(sample.keys())
    return f"The query answered '{question}' and returned {len(rows)} row(s) with fields: {fields}."


def extract_user_agent(request: Request) -> Optional[str]:
    return request.headers.get("user-agent")


__all__ = [
    "TTLCache",
    "question_cache",
    "cache_with_ttl",
    "encode_plot",
    "ensure_feedback_file",
    "log_feedback_event",
    "log_ask_event",
    "summarize_rows",
    "format_answer_summary",
    "extract_user_agent",
]
