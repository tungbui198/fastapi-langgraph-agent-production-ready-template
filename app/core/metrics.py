"""Langfuse-based metrics utilities."""

from __future__ import annotations

import os
import time
import uuid
from contextlib import contextmanager
from typing import Any, Dict

from langfuse import Langfuse


langfuse_client = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "http://localhost:3000"),
)


def log_event(name: str, metadata: Dict[str, Any] | None = None) -> None:
    """Send a metric event to Langfuse."""
    try:
        langfuse_client.event(
            trace_id=str(uuid.uuid4()),
            name=name,
            metadata=metadata or {},
        )
    except Exception:
        # Ignore errors to not impact main flow
        pass


@contextmanager
def measure_llm_stream(model: str) -> None:
    """Context manager to measure LLM stream duration."""
    start = time.time()
    try:
        yield
    finally:
        duration = time.time() - start
        log_event(
            "llm_stream_duration",
            {"model": model, "duration": duration},
        )


def record_http_request(method: str, endpoint: str, status: int, duration: float) -> None:
    """Record an HTTP request metric."""
    log_event(
        "http_request",
        {
            "method": method,
            "endpoint": endpoint,
            "status": status,
            "duration": duration,
        },
    )


def setup_metrics(app) -> None:  # noqa: D401
    """Placeholder for compatibility."""
    # No-op since metrics are directly sent to Langfuse
    return None
