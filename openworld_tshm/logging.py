from __future__ import annotations
import os
import json
import logging
from typing import Any
from rich.logging import RichHandler


_CONFIGURED = False


class _JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:  # noqa: D401
        payload: dict[str, Any] = {
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "time": self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%S"),
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def _level_from(env_val: str | None, default: str = "INFO") -> int:
    level_name = (env_val or default).upper()
    return getattr(logging, level_name, logging.INFO)


def configure_logging(level: str | None = None, fmt: str | None = None) -> None:
    global _CONFIGURED
    if _CONFIGURED and logging.getLogger().handlers:
        # Already configured
        return

    log_level = _level_from(level or os.getenv("LOG_LEVEL"), default="INFO")
    log_format = (fmt or os.getenv("LOG_FORMAT", "rich")).lower()

    root = logging.getLogger()
    root.setLevel(log_level)

    # Clear existing handlers if any (e.g., in interactive sessions)
    for h in list(root.handlers):
        root.removeHandler(h)

    if log_format == "json":
        handler = logging.StreamHandler()
        handler.setFormatter(_JsonFormatter())
        root.addHandler(handler)
    else:
        handler = RichHandler(rich_tracebacks=True)
        # Message only; RichHandler renders level/time separately
        fmt = logging.Formatter("%(message)s")
        handler.setFormatter(fmt)
        root.addHandler(handler)

    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    # Ensure configured according to env defaults before returning logger
    configure_logging()
    return logging.getLogger(name)

