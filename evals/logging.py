"""Logging utilities for the evaluation scripts."""

import logging
from datetime import datetime
from pathlib import Path

import structlog

from evals.config import settings

# Ensure log directory exists
settings.LOG_DIR.mkdir(parents=True, exist_ok=True)


def _get_log_file_path() -> Path:
    """Return the path to today's log file."""
    return settings.LOG_DIR / f"evaluation-{datetime.now().strftime('%Y-%m-%d')}.jsonl"


class JsonlFileHandler(logging.Handler):
    """Custom handler that writes JSONL logs to a file."""

    def __init__(self, file_path: Path) -> None:
        """Create a new handler writing to *file_path*."""
        super().__init__()
        self.file_path = file_path

    def emit(self, record: logging.LogRecord) -> None:
        """Write a formatted log record to the file."""
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if hasattr(record, "extra"):
            log_entry.update(record.extra)
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(structlog.processors.JSONRenderer()(None, None, log_entry) + "\n")


def setup_logging() -> None:
    """Configure structlog for the evaluation utilities."""
    file_handler = JsonlFileHandler(_get_log_file_path())
    file_handler.setLevel(settings.LOG_LEVEL)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(settings.LOG_LEVEL)

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer() if settings.LOG_FORMAT == "json" else structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, settings.LOG_LEVEL, logging.INFO)),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(handlers=[file_handler, console_handler], level=settings.LOG_LEVEL, format="%(message)s")


setup_logging()
logger = structlog.get_logger()
